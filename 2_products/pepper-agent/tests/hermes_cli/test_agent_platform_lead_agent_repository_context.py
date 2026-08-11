from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest


def _install_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import tools.pepper_repository_tools as repo_tools

    repo = tmp_path / "AGENT PLATFORM"
    (repo / "0_architecture").mkdir(parents=True)
    (repo / "2_products" / "pepper-agent").mkdir(parents=True)
    (repo / "Contexto Módulos Siamese").mkdir(parents=True)
    monkeypatch.setattr(repo_tools, "_REPOSITORY_ROOT", repo)
    monkeypatch.setattr(
        repo_tools,
        "_git_snapshot",
        lambda _root: {"available": True, "read_only": True, "status_entries": []},
    )
    return repo, repo_tools


def _tool_result(name: str, args: dict | None = None) -> dict:
    import tools.pepper_repository_tools  # noqa: F401
    from model_tools import handle_function_call

    return json.loads(handle_function_call(name, args or {}))


def test_repository_context_reports_only_approved_relative_roots(
    tmp_path,
    monkeypatch,
) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)

    result = _tool_result("get_repository_context")

    assert result["success"] is True
    assert result["access_mode"] == "bounded_read_only"
    assert result["write_authority"] is False
    assert result["shell_authority"] is False
    assert result["git_mutation_authority"] is False
    roots = {item["root"]: item for item in result["allowed_roots"]}
    assert set(roots) == {"architecture", "pepper-agent", "siamese-context"}
    assert roots["architecture"]["path"] == "0_architecture"
    assert roots["pepper-agent"]["path"] == "2_products/pepper-agent"
    assert roots["siamese-context"]["path"] == "Contexto Módulos Siamese"
    assert all(item["available"] for item in roots.values())
    assert str(repo) not in json.dumps(result, ensure_ascii=False)


def test_reads_architecture_product_and_siamese_roots(tmp_path, monkeypatch) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    (repo / "0_architecture" / "roadmap.md").write_text(
        "Architecture Roadmap\n",
        encoding="utf-8",
    )
    (repo / "2_products" / "pepper-agent" / "README.md").write_text(
        "Pepper Product\n",
        encoding="utf-8",
    )
    (repo / "Contexto Módulos Siamese" / "overview.md").write_text(
        "Siamese Context\n",
        encoding="utf-8",
    )

    architecture = _tool_result(
        "read_repository_file",
        {"root": "architecture", "path": "roadmap.md"},
    )
    product = _tool_result(
        "read_repository_file",
        {"root": "pepper-agent", "path": "README.md"},
    )
    siamese = _tool_result(
        "read_repository_file",
        {"root": "siamese-context", "path": "overview.md"},
    )

    assert "Architecture Roadmap" in architecture["content"]
    assert "Pepper Product" in product["content"]
    assert "Siamese Context" in siamese["content"]


def test_repository_read_rejects_traversal_and_absolute_paths(tmp_path, monkeypatch) -> None:
    _repo, _repo_tools = _install_repo(tmp_path, monkeypatch)

    traversal = _tool_result(
        "read_repository_file",
        {"root": "pepper-agent", "path": "../outside.txt"},
    )
    absolute = _tool_result(
        "read_repository_file",
        {"root": "pepper-agent", "path": str(tmp_path / "x.txt")},
    )

    assert traversal["category"] in {"dot_segment", "parent_segment"}
    assert "error" in traversal
    assert absolute["category"] == "absolute_path"
    assert "error" in absolute


def test_repository_tools_deny_secret_paths_and_allow_env_examples(
    tmp_path,
    monkeypatch,
) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    product = repo / "2_products" / "pepper-agent"
    secret_filenames = (
        ".env",
        "auth.json",
        "credentials.json",
        "session-token.json",
        "api_key.yaml",
        "private.pem",
        "cookies.sqlite",
    )
    for filename in secret_filenames:
        (product / filename).write_text("TOPSECRET\n", encoding="utf-8")
    (product / ".env.example").write_text("DOCUMENTED_SHAPE=1\n", encoding="utf-8")

    for filename in secret_filenames:
        result = _tool_result(
            "read_repository_file",
            {"root": "pepper-agent", "path": filename},
        )
        assert result["category"] == "secret_path"
        assert "TOPSECRET" not in json.dumps(result)

    example = _tool_result(
        "read_repository_file",
        {"root": "pepper-agent", "path": ".env.example"},
    )
    assert example["success"] is True
    assert "DOCUMENTED_SHAPE" in example["content"]

    listing = _tool_result("list_repository_tree", {"root": "pepper-agent"})
    names = {entry["name"] for entry in listing["entries"]}
    assert ".env" not in names
    assert "auth.json" not in names
    assert ".env.example" in names
    assert listing["skipped"]["blocked_paths"] >= 7


def test_repository_search_skips_secret_and_generated_content(tmp_path, monkeypatch) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    product = repo / "2_products" / "pepper-agent"
    (product / "normal.txt").write_text("visible planning phrase\n", encoding="utf-8")
    (product / ".env").write_text("hidden planning phrase\n", encoding="utf-8")
    generated = product / "node_modules" / "pkg"
    generated.mkdir(parents=True)
    (generated / "generated.txt").write_text("generated planning phrase\n", encoding="utf-8")

    visible = _tool_result(
        "search_repository",
        {"query": "visible planning", "root": "pepper-agent"},
    )
    hidden = _tool_result(
        "search_repository",
        {"query": "hidden planning", "root": "pepper-agent"},
    )
    generated_result = _tool_result(
        "search_repository",
        {"query": "generated planning", "root": "pepper-agent"},
    )

    assert visible["match_count"] == 1
    assert visible["matches"][0]["path"] == "normal.txt"
    assert hidden["match_count"] == 0
    assert generated_result["match_count"] == 0
    assert hidden["skipped"]["blocked_paths"] >= 1
    assert generated_result["skipped"]["blocked_paths"] >= 1


def test_repository_tree_skips_generated_directories_by_default(tmp_path, monkeypatch) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    product = repo / "2_products" / "pepper-agent"
    (product / "src").mkdir()
    (product / "node_modules").mkdir()
    (product / "graphify-out").mkdir()

    result = _tool_result("list_repository_tree", {"root": "pepper-agent"})

    names = {entry["name"] for entry in result["entries"]}
    assert "src" in names
    assert "node_modules" not in names
    assert "graphify-out" not in names
    assert result["skipped"]["blocked_paths"] == 2


def test_repository_read_rejects_redirect_detected_by_containment_helper(
    tmp_path,
    monkeypatch,
) -> None:
    repo, repo_tools = _install_repo(tmp_path, monkeypatch)
    product = repo / "2_products" / "pepper-agent"
    (product / "linked.txt").write_text("redirect target text\n", encoding="utf-8")
    original = repo_tools.assert_existing_path_contained

    from hermes_cli.agent_platform.runtime_adapter.path_containment import PathRedirectDetectedError

    def fake_assert_existing_path_contained(
        candidate,
        *,
        containment_root,
        platform_family=None,
    ):
        if Path(candidate).name == "linked.txt":
            raise PathRedirectDetectedError(
                validation_category="redirect_in_path_chain",
                path_role="candidate",
                basename="linked.txt",
            )
        return original(
            candidate,
            containment_root=containment_root,
            platform_family=platform_family,
        )

    monkeypatch.setattr(
        repo_tools,
        "assert_existing_path_contained",
        fake_assert_existing_path_contained,
    )

    result = _tool_result(
        "read_repository_file",
        {"root": "pepper-agent", "path": "linked.txt"},
    )

    assert result["category"] == "redirect_in_path_chain"
    assert "error" in result


def test_repository_git_snapshot_uses_only_fixed_read_only_argv(tmp_path, monkeypatch) -> None:
    repo, repo_tools = _install_repo(tmp_path, monkeypatch)
    calls = []
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-be-forwarded")

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        assert argv[0] == "git"
        assert tuple(argv[1:]) in repo_tools._READONLY_GIT_COMMANDS
        assert not ({"add", "commit", "push", "reset", "checkout"} & set(argv))
        assert kwargs["cwd"] == str(repo)
        assert kwargs["shell"] is False
        assert kwargs["check"] is False
        assert kwargs["env"]["GIT_OPTIONAL_LOCKS"] == "0"
        assert kwargs["env"]["GIT_TERMINAL_PROMPT"] == "0"
        assert "OPENAI_API_KEY" not in kwargs["env"]
        command = tuple(argv[1:])
        if command == ("rev-parse", "--abbrev-ref", "HEAD"):
            stdout = "p18-manual-to-hermes-workflow-migration\n"
        elif command == ("rev-parse", "HEAD"):
            stdout = "9e6ca2efda31ef0517e413d81cc7fbe3c3f4545b\n"
        else:
            stdout = (
                "## p18-manual-to-hermes-workflow-migration\n"
                " M 2_products/pepper-agent/toolsets.py\n"
                "?? 2_products/pepper-agent/auth.json\n"
                "?? Contexto Módulos Siamese/\n"
                "?? README.md\n"
            )
        return SimpleNamespace(returncode=0, stdout=stdout, stderr="")

    monkeypatch.setattr(repo_tools.subprocess, "run", fake_run)

    snapshot = repo_tools._git_snapshot(repo)

    assert len(calls) == 3
    assert snapshot["available"] is True
    assert snapshot["read_only"] is True
    assert snapshot["shell"] is False
    assert snapshot["branch"] == "p18-manual-to-hermes-workflow-migration"
    assert snapshot["head"] == "9e6ca2efda31ef0517e413d81cc7fbe3c3f4545b"
    assert {entry["path"] for entry in snapshot["status_entries"]} == {
        "2_products/pepper-agent/toolsets.py",
        "Contexto Módulos Siamese",
    }
    assert snapshot["skipped_status_entries"]["blocked_paths"] == 1
    assert snapshot["skipped_status_entries"]["outside_allowed_roots"] == 1


def test_pepper_repository_toolset_resolves_without_generic_file_or_shell_tools() -> None:
    from toolsets import resolve_toolset

    tools = set(resolve_toolset("pepper_repository"))

    assert tools == {
        "get_repository_context",
        "list_repository_tree",
        "read_repository_file",
        "search_repository",
        "resolve_repository_authority",
    }
    assert not (
        tools & {"terminal", "process", "read_file", "write_file", "patch", "search_files"}
    )


def _write_architecture_doc(repo: Path, relative_path: str, text: str) -> None:
    path = repo / "0_architecture" / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def _candidate_by_repository_path(result: dict, repository_path: str) -> dict:
    return next(
        candidate
        for candidate in result["candidates"]
        if candidate["repository_path"] == repository_path
    )


def test_authority_resolution_roadmap_regression_prefers_p18r_updated_contract(
    tmp_path,
    monkeypatch,
) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    g00_path = "governance/agent_platform_active_platform_direction_decision.md"
    roadmap_path = "governance/agent_platform_roadmap_generation_work_breakdown_contract.md"
    _write_architecture_doc(
        repo,
        g00_path,
        """
        # G-00 - Active Platform Direction Decision

        | Field | Value |
        | --- | --- |
        | Status | Accepted direction decision |
        | Scope | Decide the post-I-A direction toward a future active platform. |
        | Authority | Governance direction only, not implementation or activation authority. |

        ## Roadmap FASE 7-17
        The roadmap below is a direction sequence. G-00 does not authorize any listed phase to start.
        """,
    )
    _write_architecture_doc(
        repo,
        roadmap_path,
        """
        # P7.0.B - Roadmap Generation / Work Breakdown Contract

        | Field | Value |
        | --- | --- |
        | Status | Accepted roadmap generation / work breakdown contract |
        | Scope | Current roadmap and work-breakdown authority for AGENT PLATFORM. |
        | Authority | Documentation-only roadmap and work-breakdown contract. |
        | Output | Canonical P7.0.B contract for manual roadmap generation and work breakdown. |

        P7.0.B establishes the canonical contract for turning a user objective into a bounded roadmap.

        ## P18.R Roadmap Sequencing Freeze
        P18.R records the post-migration roadmap sequence.
        | Field | Value |
        | --- | --- |
        | roadmap_update_owner | P18.R |
        | inserted_project | P18.9 - Pepper Product Personalization |
        Accepted sequence after P18.R: P18.R -> P18.9 -> P19 -> P20 -> P21.
        """,
    )

    result = _tool_result(
        "resolve_repository_authority",
        {
            "query": "current canonical Agent Platform roadmap",
            "root": "architecture",
            "max_candidates": 5,
        },
    )

    assert result["resolution_state"] == "resolved"
    assert result["canonical"]["repository_path"] == f"0_architecture/{roadmap_path}"
    assert [candidate["repository_path"] for candidate in result["candidates"]] == [
        f"0_architecture/{roadmap_path}",
        f"0_architecture/{g00_path}",
    ]
    g00 = _candidate_by_repository_path(result, f"0_architecture/{g00_path}")
    assert g00["classification"] == "supporting_historical_directional_authority"
    assert "historical or directional-only marker found" in g00["cautions"]
    assert "P18.9" in json.dumps(result["canonical"], ensure_ascii=False)


def test_authority_resolution_historical_vs_current_prefers_current_document(
    tmp_path,
    monkeypatch,
) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    historical_path = "governance/security_direction_decision.md"
    current_path = "security/current_security_authority.md"
    _write_architecture_doc(
        repo,
        historical_path,
        """
        # Security Direction Decision
        | Field | Value |
        | --- | --- |
        | Status | Accepted direction decision |
        | Authority | Historical governance direction only, not implementation authority. |
        Security roadmap below is a direction sequence and does not authorize current work.
        """,
    )
    _write_architecture_doc(
        repo,
        current_path,
        """
        # Current Security Authority
        | Field | Value |
        | --- | --- |
        | Status | Accepted current security authority |
        | Scope | Current canonical security policy authority. |
        | Authority | Current canonical source of truth for security policy. |
        This current canonical security source was updated by the latest governance pass.
        """,
    )

    result = _tool_result(
        "resolve_repository_authority",
        {"query": "current canonical security authority", "root": "architecture"},
    )

    assert result["resolution_state"] == "resolved"
    assert result["canonical"]["repository_path"] == f"0_architecture/{current_path}"


def test_authority_resolution_broad_vs_specific_prefers_specific_owner(
    tmp_path,
    monkeypatch,
) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    broad_path = "governance/platform_direction_authority.md"
    specific_path = "governance/provider_activation_authority.md"
    _write_architecture_doc(
        repo,
        broad_path,
        """
        # Platform Direction Authority
        | Field | Value |
        | --- | --- |
        | Status | Accepted direction decision |
        | Authority | Governance direction only, not implementation or activation authority. |
        This broad platform direction mentions provider activation as future work.
        """,
    )
    _write_architecture_doc(
        repo,
        specific_path,
        """
        # Provider Activation Authority
        | Field | Value |
        | --- | --- |
        | Status | Accepted provider activation authority |
        | Scope | Current canonical provider activation authority. |
        | Authority | Current canonical source of truth for provider activation. |
        Provider activation current sequence and OAuth boundaries are defined here.
        """,
    )

    result = _tool_result(
        "resolve_repository_authority",
        {"query": "current canonical provider activation authority", "root": "architecture"},
    )

    assert result["resolution_state"] == "resolved"
    assert result["canonical"]["repository_path"] == f"0_architecture/{specific_path}"


def test_authority_resolution_accepted_but_noncanonical_is_supporting(
    tmp_path,
    monkeypatch,
) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    note_path = "governance/accepted_roadmap_note.md"
    canonical_path = "governance/current_roadmap_authority.md"
    _write_architecture_doc(
        repo,
        note_path,
        """
        # Accepted Roadmap Note
        | Field | Value |
        | --- | --- |
        | Status | Accepted |
        | Scope | Supporting evidence only for roadmap discussion. |
        | Authority | Not canonical authority. |
        This accepted note does not create authority.
        """,
    )
    _write_architecture_doc(
        repo,
        canonical_path,
        """
        # Current Roadmap Authority
        | Field | Value |
        | --- | --- |
        | Status | Accepted current roadmap authority |
        | Scope | Current canonical roadmap authority. |
        | Authority | Current canonical source of truth for roadmap sequence. |
        The current roadmap sequence was updated by P18.R and includes P18.9 before P19.
        """,
    )

    result = _tool_result(
        "resolve_repository_authority",
        {"query": "current canonical roadmap authority", "root": "architecture"},
    )

    note = _candidate_by_repository_path(result, f"0_architecture/{note_path}")
    assert result["canonical"]["repository_path"] == f"0_architecture/{canonical_path}"
    assert note["classification"] == "accepted_supporting_evidence_not_canonical"
    assert "noncanonical/supporting-only marker found" in note["cautions"]


def test_authority_resolution_ambiguity_returns_uncertainty(
    tmp_path,
    monkeypatch,
) -> None:
    repo, _repo_tools = _install_repo(tmp_path, monkeypatch)
    for relative_path in (
        "governance/alpha_roadmap_authority.md",
        "governance/beta_roadmap_authority.md",
    ):
        _write_architecture_doc(
            repo,
            relative_path,
            """
            # Roadmap Authority
            | Field | Value |
            | --- | --- |
            | Status | Accepted current roadmap authority |
            | Scope | Current canonical roadmap authority. |
            | Authority | Current canonical source of truth for roadmap sequence. |
            The current roadmap sequence was updated by P18.R and includes P18.9 before P19.
            """,
        )

    result = _tool_result(
        "resolve_repository_authority",
        {"query": "current canonical roadmap authority", "root": "architecture"},
    )

    assert result["resolution_state"] == "ambiguous"
    assert result["canonical"] is None
    assert result["uncertainty"]
    assert [candidate["repository_path"] for candidate in result["candidates"]] == [
        "0_architecture/governance/alpha_roadmap_authority.md",
        "0_architecture/governance/beta_roadmap_authority.md",
    ]
