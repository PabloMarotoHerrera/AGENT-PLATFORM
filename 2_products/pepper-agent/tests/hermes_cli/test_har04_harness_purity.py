"""Enforce dependency direction in a new interpreter, before harness import."""

import os
from pathlib import Path
import subprocess
import sys

import pytest


# No source-text assertions: the imported code really runs with blocked edges.
PROBE = r'''
import builtins, importlib.abc, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
allowed_project = {"hermes_cli", "hermes_cli.agent_platform"}
allowed_roots = {"enum", "typing", "pydantic", "hashlib", "hmac", "json"}
forbidden_roots = {"tools", "sqlite3", "_sqlite3", "openai", "anthropic", "litellm",
                   "requests", "httpx", "docker", "graphify", "kanban", "product_runtime"}
original_import = builtins.__import__
def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    caller = (globals or {}).get("__name__", "")
    harness_caller = caller.startswith("hermes_cli.agent_platform.harness")
    if name.split(".")[0] in forbidden_roots:
        raise RuntimeError("forbidden dependency: " + name)
    if name.startswith("hermes_cli") and name not in allowed_project and not name.startswith("hermes_cli.agent_platform.harness"):
        raise RuntimeError("private implementation dependency: " + name)
    if harness_caller and level == 0 and name.split(".")[0] not in allowed_roots:
        raise RuntimeError("outbound harness dependency: " + name)
    return original_import(name, globals, locals, fromlist, level)
class ImportGuard(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in forbidden_roots:
            raise RuntimeError("forbidden dynamic dependency: " + fullname)
        if fullname.startswith("hermes_cli") and fullname not in allowed_project and not fullname.startswith("hermes_cli.agent_platform.harness"):
            raise RuntimeError("private dynamic dependency: " + fullname)
        return None
def audit(event, args):
    if event == "open":
        mode, flags = args[1:3]
        if (isinstance(mode, str) and any(c in mode for c in "wax+")) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)):
            raise RuntimeError("filesystem write")
    if event.startswith(("socket.", "subprocess.", "sqlite3.", "os.exec", "os.spawn")) or event in {"os.system", "os.mkdir", "os.remove", "os.rename", "os.rmdir", "os.putenv", "os.unsetenv"}:
        raise RuntimeError("external effect: " + event)
builtins.__import__ = guarded_import
sys.meta_path.insert(0, ImportGuard())
sys.addaudithook(audit)
from hermes_cli.agent_platform import harness
assert harness.__file__.startswith(sys.argv[1] + os.sep)
assert harness.canonical_json(harness.ContractRef(contract_id="probe", version=1))
if len(sys.argv) > 2:
    canary = sys.argv[2]
    if canary == "write":
        open(os.path.join(os.environ["HOME"], "must-not-exist"), "w")
    elif canary == "database":
        __import__("sqlite3")
    elif canary == "provider":
        __import__("openai")
    elif canary == "private":
        __import__("hermes_cli.agent_platform.product_runtime")
    elif canary == "registry":
        __import__("tools.registry")
    elif canary == "network":
        audit("socket.connect", ())
    elif canary == "process":
        audit("subprocess.Popen", ())
    raise AssertionError("guard failed to reject canary")
print("HAR04_IMPORT_PURE")
'''


def run_probe(tmp_path, canary=None):
    root = str(Path(__file__).resolve().parents[2])
    env = {"HOME": str(tmp_path), "HERMES_HOME": str(tmp_path / "hermes"),
           "PATH": os.defpath, "LANG": "C.UTF-8", "TZ": "UTC"}
    return subprocess.run([sys.executable, "-I", "-B", "-c", PROBE, root,
                           *([canary] if canary else [])], cwd=tmp_path,
                          env=env, capture_output=True, text=True, timeout=30)


def test_fresh_import_has_no_private_dependencies_or_external_effects(tmp_path):
    probe_home = tmp_path / "probe"
    probe_home.mkdir()
    result = run_probe(probe_home)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "HAR04_IMPORT_PURE"
    assert list(probe_home.iterdir()) == []


@pytest.mark.parametrize("canary", ("write", "database", "provider", "private", "registry", "network", "process"))
def test_isolated_probe_detects_forbidden_imports_and_effects(tmp_path, canary):
    probe_home = tmp_path / "probe"
    probe_home.mkdir()
    result = run_probe(probe_home, canary)
    assert result.returncode != 0
    assert "RuntimeError:" in result.stderr
    assert "guard failed" not in result.stderr
    expected = {"write": "filesystem write", "database": "sqlite3", "provider": "openai",
                "private": "private implementation dependency", "registry": "tools.registry",
                "network": "socket.connect", "process": "subprocess.Popen"}
    assert expected[canary] in result.stderr
    assert list(probe_home.iterdir()) == []
