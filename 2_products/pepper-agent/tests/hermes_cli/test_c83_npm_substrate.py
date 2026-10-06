import json
from pathlib import Path
import shutil
from types import SimpleNamespace
import subprocess

import pytest

from hermes_cli.agent_platform.work_packet import npm_substrate as ns
from hermes_cli.agent_platform import product_runtime as pr


def put(root, rel, value):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


@pytest.fixture
def tree(tmp_path, monkeypatch):
    source = tmp_path / "source"
    root = source / "product"
    root.mkdir(parents=True)
    package = {"name": "web", "devDependencies": {"@vitejs/plugin-react": "1.0.0"}}
    plugin = {"version": "1.0.0", "dependencies": {"transitive": "2.0.0"}}
    transitive = {"version": "2.0.0"}
    put(root, "package.json", {"workspaces": ["web"], "packageManager": "npm@10.0.0"})
    put(root, "web/package.json", package)
    put(root, "package-lock.json", {"lockfileVersion": 3, "packages": {
        "": {}, "web": package, "node_modules/@vitejs/plugin-react": plugin,
        "node_modules/transitive": transitive,
    }})
    put(root, "node_modules/@vitejs/plugin-react/package.json", plugin)
    put(root, "node_modules/transitive/package.json", transitive)
    monkeypatch.setattr(ns, "node_version", lambda node: "v22.23.2")
    monkeypatch.setattr(ns, "npm_runtime", lambda node, engines: "10.0.0")
    return source


def retain(source, tmp_path):
    contract = ns.inspect(source, "product/web", Path("node"))
    workspace = tmp_path / "workspace"
    shutil.copytree(source, workspace)
    put(workspace, "product/web/node_modules/.pepper-validation-substrate.json", contract)
    return workspace


def test_complete_closure_is_retained_and_rechecked(tree, tmp_path):
    workspace = retain(tree, tmp_path)
    ns.verify(workspace, "product/web", Path("node"))
    contract = ns.inspect(workspace, "product/web", Path("node"))
    assert set(contract["packages"]) == {
        "node_modules/@vitejs/plugin-react", "node_modules/transitive",
    }
    assert contract["node_version"] == "v22.23.2"
    assert contract["package_manager"] == "npm@10.0.0"


@pytest.mark.parametrize("relative", [
    "node_modules/@vitejs/plugin-react/package.json",
    "node_modules/transitive/package.json", "package-lock.json",
])
def test_missing_substrate_fails_closed(tree, relative):
    (tree / "product" / relative).unlink()
    with pytest.raises(ns.SubstrateError):
        ns.inspect(tree, "product/web", Path("node"))


@pytest.mark.parametrize("relative", ["web/package.json", "package.json", "package-lock.json"])
def test_definition_digest_drift_rejected(tree, tmp_path, relative):
    workspace = retain(tree, tmp_path)
    path = workspace / "product" / relative
    value = json.loads(path.read_text())
    value["description"] = "changed"
    put(workspace / "product", relative, value)
    with pytest.raises(ns.SubstrateError):
        ns.verify(workspace, "product/web", Path("node"))


def test_node_version_drift_rejected(tree, tmp_path, monkeypatch):
    workspace = retain(tree, tmp_path)
    monkeypatch.setattr(ns, "node_version", lambda node: "v24.0.0")
    with pytest.raises(ns.SubstrateError):
        ns.verify(workspace, "product/web", Path("node"))


def test_other_package_manager_rejected(tree):
    put(tree, "product/package.json", {"packageManager": "pnpm@9"})
    with pytest.raises(ns.SubstrateError, match="not npm"):
        ns.inspect(tree, "product/web", Path("node"))


def test_npm_version_drift_rejected(tree, monkeypatch):
    monkeypatch.setattr(ns, "npm_runtime", lambda node, engines: "11.0.0")
    with pytest.raises(ns.SubstrateError, match="npm version"):
        ns.inspect(tree, "product/web", Path("node"))


def test_unlocked_nearer_package_cannot_shadow_dependency(tree):
    put(tree, "product/web/node_modules/@vitejs/plugin-react/package.json", {"version": "1.0.0"})
    with pytest.raises(ns.SubstrateError, match="shadows"):
        ns.inspect(tree, "product/web", Path("node"))


def test_governed_command_classifies_missing_substrate_before_launch(tree, monkeypatch):
    from tools import workpacket_validation_tool as tool

    monkeypatch.setattr(tool, "_script_identity_drift_reason", lambda command: None)
    monkeypatch.setattr(tool, "_run_launch_payload", lambda *a, **kw: pytest.fail("command launched"))
    authority = SimpleNamespace(resolved_workspace_root=tree, ticket_id="T", work_packet_id="WP", work_packet_SHA256="a")
    command = tool.GovernedValidationCommandSpec(
        command_id="GVCMD-001", validation_id="V1", source="work_packet",
        source_command="npm test", effective_argv=("node", str(tree / "product/node_modules/vitest/vitest.mjs"), "run"),
        working_directory=str(tree / "product/web"),
    )
    result = json.loads(tool._run_command(authority, command))
    assert result["failure_reason"] == "validation_infrastructure_failed"
    assert result["process_started"] is False
    assert result["exit_code"] is None


def test_installed_version_must_match_lock(tree):
    put(tree, "product/node_modules/transitive/package.json", {"version": "3.0.0"})
    with pytest.raises(ns.SubstrateError, match="differs from lock"):
        ns.inspect(tree, "product/web", Path("node"))


def test_no_network_or_install_during_offline_inspection(tree, monkeypatch):
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: pytest.fail("unexpected subprocess"))
    assert ns.inspect(tree, "product/web", Path("node"))["packages"]


def test_missing_receipt_does_not_fall_back_to_source(tree, tmp_path):
    workspace = retain(tree, tmp_path)
    ns.receipt_path(workspace, "product/web").unlink()
    with pytest.raises(ns.SubstrateError):
        ns.verify(workspace, "product/web", Path("node"))


def test_external_dependency_link_rejected(tree, tmp_path):
    path = tree / "product/node_modules/transitive/package.json"
    path.unlink()
    outside = put(tmp_path, "outside.json", {"version": "2.0.0"})
    path.symlink_to(outside)
    with pytest.raises(ns.SubstrateError, match="escapes"):
        ns.inspect(tree, "product/web", Path("node"))


def test_bin_wrapper_preserves_real_package_relative_entry(tmp_path):
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node required")
    source = tmp_path / "source"
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    modules = source / "node_modules"
    cli = modules / "vite/bin/vite.js"
    cli.parent.mkdir(parents=True)
    cli.write_text('#!/usr/bin/env node\nrequire("../dist/cli.js");\n')
    cli.chmod(0o755)
    payload = modules / "vite/dist/cli.js"
    payload.parent.mkdir()
    payload.write_text('console.log("candidate-runtime-ok");\n')
    (modules / ".bin").mkdir()
    (modules / ".bin/vite").symlink_to("../vite/bin/vite.js")
    record = pr._copy_dependency_substrate_root(
        modules, workspace / "node_modules", source_root=source,
        workspace_root=workspace, package_rel="web",
        authority=SimpleNamespace(ticket_id="T", work_packet_id="WP", work_packet_SHA256="a", projection_SHA256="b"),
    )
    result = subprocess.run([str(workspace / "node_modules/.bin/vite")], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "candidate-runtime-ok"
    assert record["dependency_install_performed"] is False
    assert not (workspace / "node_modules/.bin/vite").is_symlink()


def test_real_npm_engine_check_rejects_incompatible_node():
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node required")
    assert ns.npm_runtime(Path(node), [">=20"])
    with pytest.raises(ns.SubstrateError, match="incompatible"):
        ns.npm_runtime(Path(node), [">=999"])


def test_retained_snapshot_survives_source_removal(tree, tmp_path):
    workspace = retain(tree, tmp_path)
    retained = tmp_path / "retained"
    retained.mkdir()
    pr._copy_source_authority_snapshot_root(
        workspace, retained, relative_root="product", copied_files=set(), copied_directories=set(),
    )
    shutil.rmtree(tree)
    ns.verify(retained, "product/web", Path("node"))


def test_fresh_recovery_is_deterministic_and_does_not_repair_old_workspace(tree, tmp_path):
    old = retain(tree, tmp_path)
    before = {p.relative_to(old): p.read_bytes() for p in old.rglob("*") if p.is_file()}
    a = ns.inspect(tree, "product/web", Path("node"))
    b = ns.inspect(tree, "product/web", Path("node"))
    assert a == b
    assert before == {p.relative_to(old): p.read_bytes() for p in old.rglob("*") if p.is_file()}
