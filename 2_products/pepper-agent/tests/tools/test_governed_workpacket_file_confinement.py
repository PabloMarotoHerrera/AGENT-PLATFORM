from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tools import governed_workpacket_file_guard as guard


def _authority(
    workspace: Path,
    *,
    allowed_paths=("src/**",),
    forbidden_paths=(),
    ticket_id="PX.1",
) -> guard.WorkPacketFileAuthority:
    return guard.WorkPacketFileAuthority(
        ticket_id=ticket_id,
        work_packet_id="WP-P999-SYNTHETIC-R0001-123456789abc",
        work_packet_SHA256="a" * 64,
        ticket_spec_SHA256="b" * 64,
        projection_SHA256="c" * 64,
        allowed_paths=tuple(allowed_paths),
        forbidden_paths=tuple(forbidden_paths),
        workspace_root=workspace,
        resolved_workspace_root=workspace.resolve(strict=True),
    )


def _write_result(**values):
    result = MagicMock()
    result.to_dict.return_value = dict(values)
    return result


def _record_authority(
    *,
    ticket_id="P18.9.1",
    work_packet_id="WP-P18-9-1-R0001-123456789abc",
    work_packet_SHA256="a" * 64,
    ticket_spec_SHA256="b" * 64,
    projection_SHA256="c" * 64,
    allowed_paths=("src/**",),
    forbidden_paths=(),
) -> tuple[dict, dict, dict]:
    generation = {
        "ticket_id": ticket_id,
        "work_packet_id": work_packet_id,
        "work_packet_SHA256": work_packet_SHA256,
        "ticket_spec_SHA256": ticket_spec_SHA256,
        "work_packet_compilation_result": {
            "work_packet": {
                "repository_scope": {
                    "allowed_paths": list(allowed_paths),
                    "forbidden_paths": list(forbidden_paths),
                }
            }
        },
    }
    decision = {"ticket_id": ticket_id, "status": "approved"}
    projection = {
        "ticket_id": ticket_id,
        "work_packet_id": work_packet_id,
        "work_packet_SHA256": work_packet_SHA256,
        "ticket_spec_SHA256": ticket_spec_SHA256,
        "projection_SHA256": projection_SHA256,
    }
    return generation, decision, projection


def _write_authority_records(tmp_path: Path, generation: dict, decision: dict, projection: dict) -> dict[str, Path]:
    paths = {
        "generation": tmp_path / "generation.json",
        "approval": tmp_path / "approval.json",
        "projection": tmp_path / "projection.json",
    }
    paths["generation"].write_text(json.dumps(generation), encoding="utf-8")
    paths["approval"].write_text(json.dumps(decision), encoding="utf-8")
    paths["projection"].write_text(json.dumps(projection), encoding="utf-8")
    return paths


def _authority_env(workspace: Path, paths: dict[str, Path], generation: dict, projection: dict) -> dict[str, str]:
    return {
        guard.GOVERNED_WORKER_ENV: guard.GOVERNED_WORKER_MODE,
        "HERMES_AGENT_PLATFORM_GOVERNED_TICKET_ID": "P18.9.0",
        "HERMES_KANBAN_WORKSPACE": str(workspace),
        guard.WORKPACKET_ID_ENV: str(generation["work_packet_id"]),
        guard.WORKPACKET_SHA256_ENV: str(generation["work_packet_SHA256"]),
        guard.TICKET_SPEC_SHA256_ENV: str(generation["ticket_spec_SHA256"]),
        guard.KANBAN_PROJECTION_SHA256_ENV: str(projection["projection_SHA256"]),
        guard.GENERATION_RECORD_PATH_ENV: str(paths["generation"]),
        guard.APPROVAL_DECISION_RECORD_PATH_ENV: str(paths["approval"]),
        guard.KANBAN_PROJECTION_RECORD_PATH_ENV: str(paths["projection"]),
    }


def _patch_authority_validators(monkeypatch, generation: dict, decision: dict, projection: dict) -> None:
    from hermes_cli.agent_platform.workflow import ticket_architect_bridge as bridge
    from hermes_cli.agent_platform.workflow import work_packet_kanban_projection as kanban_projection

    def validate_generation_record(record):
        assert record == generation
        return dict(record)

    def validate_approval_decision_record(record, *, ticket_id, generation_record):
        assert record == decision
        assert ticket_id == generation["ticket_id"]
        assert generation_record["work_packet_id"] == generation["work_packet_id"]
        return dict(record)

    def validate_kanban_projection_record(record, *, ticket_id, generation_record, decision_record):
        assert record == projection
        assert ticket_id == generation["ticket_id"]
        assert generation_record["work_packet_id"] == generation["work_packet_id"]
        assert decision_record == decision
        return dict(record)

    monkeypatch.setattr(bridge, "validate_generation_record", validate_generation_record)
    monkeypatch.setattr(bridge, "validate_approval_decision_record", validate_approval_decision_record)
    monkeypatch.setattr(kanban_projection, "validate_kanban_projection_record", validate_kanban_projection_record)


@pytest.fixture
def governed_workspace(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.setenv(guard.GOVERNED_WORKER_ENV, guard.GOVERNED_WORKER_MODE)
    monkeypatch.setenv("HERMES_KANBAN_WORKSPACE", str(workspace))
    monkeypatch.setenv("TERMINAL_CWD", str(workspace))
    return workspace


def test_governed_write_allows_workpacket_subtree(governed_workspace, monkeypatch):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(
            governed_workspace,
            allowed_paths=("2_products/pepper-agent/web/src/agent-platform/shell/**",),
        ),
    )
    mock_ops = MagicMock()
    mock_ops.write_file.return_value = _write_result(bytes_written=5)

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool(
            "2_products/pepper-agent/web/src/agent-platform/shell/App.tsx",
            "hello",
        ))

    expected = governed_workspace / "2_products/pepper-agent/web/src/agent-platform/shell/App.tsx"
    assert "error" not in result
    assert result["resolved_path"] == str(expected)
    mock_ops.write_file.assert_called_once_with(str(expected), "hello")


def test_governed_write_denies_similar_prefix(governed_workspace, monkeypatch):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(governed_workspace, allowed_paths=("src/app/**",)),
    )
    mock_ops = MagicMock()

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool("src/application/file.txt", "nope"))

    assert guard.WORKPACKET_WRITE_PATH_DENIED in result["error"]
    mock_ops.write_file.assert_not_called()


def test_governed_write_denies_forbidden_before_allowed(governed_workspace, monkeypatch):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(
            governed_workspace,
            allowed_paths=("src/**",),
            forbidden_paths=("src/secret/**",),
        ),
    )
    mock_ops = MagicMock()

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool("src/secret/key.txt", "nope"))

    assert guard.WORKPACKET_FORBIDDEN_PATH in result["error"]
    assert "src/secret/**" in result["error"]
    mock_ops.write_file.assert_not_called()


def test_governed_write_denies_absolute_outside_workspace(governed_workspace, tmp_path, monkeypatch):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(governed_workspace, allowed_paths=("src/**",)),
    )
    outside = tmp_path / "sibling" / "src" / "file.txt"
    mock_ops = MagicMock()

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool(str(outside), "nope"))

    assert guard.WORKSPACE_PATH_ESCAPE in result["error"]
    mock_ops.write_file.assert_not_called()


def test_governed_write_denies_parent_traversal(governed_workspace, monkeypatch):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(governed_workspace, allowed_paths=("src/**",)),
    )
    mock_ops = MagicMock()

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool("../workspace/src/file.txt", "nope"))

    assert guard.WORKSPACE_PATH_ESCAPE in result["error"]
    mock_ops.write_file.assert_not_called()


def test_governed_write_denies_symlink_escape(governed_workspace, tmp_path, monkeypatch):
    outside = tmp_path / "outside"
    outside.mkdir()
    link = governed_workspace / "src"
    try:
        os.symlink(outside, link, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")

    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(governed_workspace, allowed_paths=("src/**",)),
    )
    mock_ops = MagicMock()

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool("src/file.txt", "nope"))

    assert guard.WORKSPACE_PATH_ESCAPE in result["error"]
    mock_ops.write_file.assert_not_called()


def test_governed_patch_authorizes_add_update_delete_and_move(governed_workspace, monkeypatch):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(governed_workspace, allowed_paths=("src/**",)),
    )
    patch_text = """*** Begin Patch
*** Add File: src/new.txt
+new
*** Update File: src/edit.txt
@@ old @@
-old
+new
*** Delete File: src/remove.txt
*** Move File: src/from.txt -> src/to.txt
*** End Patch"""
    mock_ops = MagicMock()
    mock_ops.patch_v4a.return_value = _write_result(success=True)

    from tools.file_tools import patch_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(patch_tool(mode="patch", patch=patch_text))

    assert "error" not in result
    mock_ops.patch_v4a.assert_called_once_with(patch_text)


def test_governed_patch_rejects_mixed_targets_before_backend(governed_workspace, monkeypatch):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(governed_workspace, allowed_paths=("src/**",)),
    )
    patch_text = """*** Begin Patch
*** Add File: src/ok.txt
+ok
*** Add File: docs/no.txt
+no
*** End Patch"""
    mock_ops = MagicMock()

    from tools.file_tools import patch_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(patch_tool(mode="patch", patch=patch_text))

    assert guard.WORKPACKET_PATCH_ATOMICITY_DENIED in result["error"]
    assert guard.WORKPACKET_WRITE_PATH_DENIED in result["error"]
    mock_ops.patch_v4a.assert_not_called()


def test_governed_worker_without_authority_denies_mutation(governed_workspace):
    mock_ops = MagicMock()

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool("src/file.txt", "nope"))

    assert guard.WORKPACKET_WRITE_AUTHORITY_UNAVAILABLE in result["error"]
    mock_ops.write_file.assert_not_called()


def test_record_authority_uses_workpacket_ticket_not_hardcoded_credential_ticket(
    governed_workspace,
    tmp_path,
    monkeypatch,
):
    generation, decision, projection = _record_authority(ticket_id="P18.9.1")
    paths = _write_authority_records(tmp_path, generation, decision, projection)
    _patch_authority_validators(monkeypatch, generation, decision, projection)

    denial = guard.governed_write_denial(
        "src/file.txt",
        env=_authority_env(governed_workspace, paths, generation, projection),
    )

    assert denial is None


def test_record_authority_denies_stale_workpacket_digest(governed_workspace, tmp_path, monkeypatch):
    generation, decision, projection = _record_authority()
    paths = _write_authority_records(tmp_path, generation, decision, projection)
    _patch_authority_validators(monkeypatch, generation, decision, projection)
    env = _authority_env(governed_workspace, paths, generation, projection)
    env[guard.WORKPACKET_SHA256_ENV] = "d" * 64

    denial = guard.governed_write_denial("src/file.txt", env=env)

    assert guard.WORKPACKET_WRITE_AUTHORITY_UNAVAILABLE in denial
    assert "WorkPacket digest mismatch" in denial


def test_non_governed_write_behavior_is_preserved(tmp_path, monkeypatch):
    monkeypatch.delenv(guard.GOVERNED_WORKER_ENV, raising=False)
    monkeypatch.setenv("TERMINAL_CWD", str(tmp_path))
    mock_ops = MagicMock()
    mock_ops.write_file.return_value = _write_result(bytes_written=2)

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool("outside.txt", "ok"))

    assert "error" not in result
    mock_ops.write_file.assert_called_once()


def test_governed_write_does_not_grant_git_file_authority(governed_workspace, monkeypatch):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(governed_workspace, allowed_paths=(".git/**",)),
    )
    mock_ops = MagicMock()

    from tools.file_tools import write_file_tool

    with patch("tools.file_tools._get_file_ops", return_value=mock_ops):
        result = json.loads(write_file_tool(".git/config", "nope"))

    assert guard.WORKPACKET_FORBIDDEN_PATH in result["error"]
    mock_ops.write_file.assert_not_called()


def test_governed_write_denies_dependency_substrate_and_lockfile_noise(
    governed_workspace,
    monkeypatch,
):
    monkeypatch.setattr(
        guard,
        "resolve_governed_workpacket_file_authority",
        lambda _env=None: _authority(
            governed_workspace,
            allowed_paths=("2_products/pepper-agent/web/**",),
        ),
    )

    node_modules_denial = guard.governed_write_denial(
        "2_products/pepper-agent/web/node_modules/vitest/vitest.mjs"
    )
    lockfile_denial = guard.governed_write_denial(
        "2_products/pepper-agent/web/package-lock.json"
    )

    assert guard.WORKPACKET_FORBIDDEN_PATH in node_modules_denial
    assert "node_modules/**" in node_modules_denial
    assert guard.WORKPACKET_FORBIDDEN_PATH in lockfile_denial
    assert "package-lock.json" in lockfile_denial


def test_authority_matching_is_ticket_generic(governed_workspace):
    ticket_a = _authority(governed_workspace, allowed_paths=("a/**",), ticket_id="PA.1")
    ticket_b = _authority(governed_workspace, allowed_paths=("b/**",), ticket_id="PB.1")

    assert guard.evaluate_write_target(ticket_a, "a/file.txt") is None
    denial = guard.evaluate_write_target(ticket_b, "a/file.txt")
    assert denial is not None
    assert denial.code == guard.WORKPACKET_WRITE_PATH_DENIED
