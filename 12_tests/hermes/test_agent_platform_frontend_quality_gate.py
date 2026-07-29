from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "10_scripts" / "hermes" / "agent_platform_frontend_quality_gate.py"
SPEC = importlib.util.spec_from_file_location(
    "agent_platform_frontend_quality_gate", SCRIPT_PATH
)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FakeProcess:
    def __init__(self, pid: int = 1234, polls: list[int | None] | None = None):
        self.pid = pid
        self._polls = list(polls or [None])
        self.returncode: int | None = None
        self.killed = False

    def poll(self):
        if len(self._polls) > 1:
            value = self._polls.pop(0)
        else:
            value = self._polls[0]
        if value is not None:
            self.returncode = value
        return value

    def wait(self, timeout=None):
        value = self.poll()
        if value is None:
            raise subprocess.TimeoutExpired("fake", timeout)
        return value

    def kill(self):
        self.killed = True
        self._polls = [-9]
        self.returncode = -9


class ConfigurationTests(unittest.TestCase):
    def test_rejects_unknown_lane_and_arbitrary_command_surface(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = gate.GateConfig(
                repo_root=Path(directory),
                result_path=Path(directory) / "result.json",
                lanes=("test", "arbitrary-shell"),
            )
            with self.assertRaises(gate.QualityGateError):
                gate._validate_config(config)
        parser_actions = {action.dest for action in gate._build_parser()._actions}
        self.assertNotIn("command", parser_actions)
        self.assertNotIn("args", parser_actions)

    def test_browser_scenario_rejects_external_url_and_unsafe_viewport(self) -> None:
        with self.assertRaises(gate.QualityGateError):
            gate._validate_scenario(
                gate.BrowserScenario("external", "https://example.com", ("x",))
            )
        with self.assertRaises(gate.QualityGateError):
            gate._validate_scenario(
                gate.BrowserScenario("tiny", "/local", ("x",), viewport_width=100)
            )
        with self.assertRaisesRegex(gate.QualityGateError, "credential-like"):
            gate._validate_scenario(
                gate.BrowserScenario(
                    "secret", "/local?access_token=do-not-retain", ("x",)
                )
            )

    def test_runtime_lane_dependencies_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            product = root / "2_products" / "pepper-agent"
            (product / "web").mkdir(parents=True)
            (product / "hermes_cli").mkdir()
            (product / "web" / "package.json").write_text("{}", encoding="utf-8")
            (product / "hermes_cli" / "main.py").write_text("", encoding="utf-8")
            (product / "AGENT_PLATFORM_MODIFICATIONS.tsv").write_text(
                "\t".join(gate.REGISTER_HEADERS) + "\n", encoding="utf-8"
            )
            browser_only = gate.GateConfig(
                root, root / "result.json", lanes=("browser",)
            )
            dashboard_only = gate.GateConfig(
                root, root / "result.json", lanes=("dashboard",)
            )
            with self.assertRaisesRegex(gate.QualityGateError, "dashboard lane"):
                gate._validate_config(browser_only)
            with self.assertRaisesRegex(gate.QualityGateError, "build lane"):
                gate._validate_config(dashboard_only)


class CommandAndEnvironmentTests(unittest.TestCase):
    def test_fixed_npm_command_uses_node_and_npm_cli_without_shell(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            product = Path(directory)
            node = product / "node.exe"
            npm_cli = product / "npm-cli.js"
            node.write_text("", encoding="utf-8")
            npm_cli.write_text("", encoding="utf-8")
            with mock.patch.object(
                gate, "_resolve_node_npm", return_value=(node, npm_cli)
            ):
                argv, evidence, cwd = gate._lane_command("build", product)
        self.assertEqual(argv, [str(node), str(npm_cli), "run", "build"])
        self.assertEqual(evidence, ["<node>", "<npm-cli.js>", "run", "build"])
        self.assertEqual(cwd, product / "web")

    def test_lint_command_is_fixed_to_product_owned_frontend_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            product = Path(directory)
            node = product / "node.exe"
            npm_cli = product / "npm-cli.js"
            eslint = product / "node_modules" / "eslint" / "bin" / "eslint.js"
            eslint.parent.mkdir(parents=True)
            for path in (node, npm_cli, eslint):
                path.write_text("", encoding="utf-8")
            with mock.patch.object(
                gate, "_resolve_node_npm", return_value=(node, npm_cli)
            ):
                argv, evidence, _ = gate._lane_command("lint", product)
        self.assertEqual(argv, [str(node), str(eslint), "src/agent-platform"])
        self.assertEqual(evidence, ["<node>", "<eslint.js>", "src/agent-platform"])

    def test_isolated_environment_drops_credentials_and_proxy_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.dict(
                gate.os.environ,
                {
                    "PATH": "safe-path",
                    "EXAMPLE_API_KEY": "secret",
                    "EXAMPLE_TOKEN": "secret",
                    "HTTPS_PROXY": "https://credential.invalid",
                    "HERMES_DASHBOARD_SESSION_TOKEN": "secret",
                },
                clear=True,
            ):
                env = gate._isolated_environment(Path(directory))
        self.assertEqual(env["PATH"], "safe-path")
        self.assertNotIn("EXAMPLE_API_KEY", env)
        self.assertNotIn("EXAMPLE_TOKEN", env)
        self.assertNotIn("HTTPS_PROXY", env)
        self.assertNotIn("HERMES_DASHBOARD_SESSION_TOKEN", env)
        self.assertEqual(env["NPM_CONFIG_OFFLINE"], "true")

    def test_command_timeout_is_bounded_and_records_hashed_logs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            product = root / "product"
            web = product / "web"
            web.mkdir(parents=True)
            env = os.environ.copy()
            command = [
                sys.executable,
                "-c",
                "import time; print('started'); time.sleep(5)",
            ]
            with mock.patch.object(
                gate,
                "_lane_command",
                return_value=(command, ["<python>", "fixture"], web),
            ):
                result = gate._run_command_lane("test", product, env, root, 0.1, 4096)
        self.assertEqual(result["status"], "failed")
        self.assertTrue(result["timed_out"])
        self.assertEqual(result["failure"], "timeout")
        self.assertRegex(result["logs"]["stdout"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertTrue(result["cleanup"]["exited"])


class ProcessLifecycleTests(unittest.TestCase):
    def test_windows_cleanup_uses_bounded_taskkill_tree_argv(self) -> None:
        process = FakeProcess(polls=[None, None, 1])
        completed = subprocess.CompletedProcess([], 0, b"", b"")
        with (
            mock.patch.object(gate, "IS_WINDOWS", True),
            mock.patch.object(gate.subprocess, "run", return_value=completed) as run,
        ):
            result = gate._terminate_process_tree(process, 2.0)
        self.assertEqual(
            run.call_args.args[0], ["taskkill", "/PID", "1234", "/T", "/F"]
        )
        self.assertEqual(run.call_args.kwargs["timeout"], 2.0)
        self.assertIs(run.call_args.kwargs["stdin"], subprocess.DEVNULL)
        self.assertTrue(result["exited"])

    def test_posix_cleanup_targets_owned_process_group_and_escalates(self) -> None:
        process = FakeProcess(polls=[None, None, None, -9])
        with (
            mock.patch.object(gate, "IS_WINDOWS", False),
            mock.patch.object(gate.os, "killpg", create=True) as killpg,
        ):
            result = gate._terminate_process_tree(process, 0.2)
        self.assertEqual(killpg.call_args_list[0], mock.call(1234, signal.SIGTERM))
        self.assertEqual(killpg.call_args_list[1], mock.call(1234, gate.POSIX_SIGKILL))
        self.assertTrue(result["escalated"])
        self.assertTrue(result["exited"])

    def test_dashboard_readiness_fails_on_early_exit_and_malformed_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ready = Path(directory) / "ready.json"
            with self.assertRaisesRegex(gate.QualityGateError, "exited"):
                gate._wait_dashboard_ready(FakeProcess(polls=[2]), ready, 0.1)
            ready.write_text('{"port":"not-an-int"}', encoding="utf-8")
            with self.assertRaisesRegex(gate.QualityGateError, "invalid port"):
                gate._read_ready_port(ready)


class BrowserProtocolTests(unittest.TestCase):
    def test_devtools_active_port_is_strict_and_cdp_url_is_redacted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "DevToolsActivePort"
            path.write_text("53210\n/devtools/browser/abc123\n", encoding="utf-8")
            self.assertEqual(
                gate._read_devtools_active_port(path),
                (53210, "/devtools/browser/abc123"),
            )
            path.write_text(
                "53210\nws://attacker.invalid/devtools/browser/x\n", encoding="utf-8"
            )
            with self.assertRaises(gate.QualityGateError):
                gate._read_devtools_active_port(path)
        message = gate._safe_error(
            RuntimeError("ws://127.0.0.1:53210/devtools/browser/abc")
        )
        self.assertNotIn("abc", message)
        self.assertIn("<redacted-cdp-url>", message)

    def test_synthetic_browser_activation_is_complete_and_in_memory_only(self) -> None:
        payload = gate._synthetic_product_configuration()
        self.assertEqual(
            payload["feature_flags"]["agent_platform.product_ui"], "experimental"
        )
        self.assertEqual(
            tuple(payload["extension_modules"]), gate.PRODUCT_EXTENSION_IDS
        )
        self.assertFalse(any("path" in key for key in payload))

    def test_local_network_error_evidence_drops_query_values(self) -> None:
        client = gate._CDPClient(mock.Mock(), {})
        client._handle_event(
            {
                "method": "Log.entryAdded",
                "params": {
                    "entry": {
                        "level": "error",
                        "source": "network",
                        "url": "http://127.0.0.1:1234/api/status?token=do-not-retain",
                    }
                },
            }
        )
        self.assertEqual(client.local_network_error_paths, {"/api/status": 1})
        self.assertNotIn("do-not-retain", json.dumps(client.local_network_error_paths))

    def test_exact_local_provider_null_auth_401_is_nonblocking(self) -> None:
        client = gate._CDPClient(mock.Mock(), {})
        client._handle_event(
            {
                "method": "Log.entryAdded",
                "params": {
                    "entry": {
                        "level": "error",
                        "source": "network",
                        "url": "http://127.0.0.1:1234/api/auth/me",
                        "text": "Failed to load resource: the server responded with a status of 401 (Unauthorized)",
                    }
                },
            }
        )
        self.assertEqual(client.events["expected_provider_null_auth_responses"], 1)
        self.assertEqual(client.events["local_network_console_errors"], 0)


class RegisterAndResultTests(unittest.TestCase):
    def _write_register(self, product: Path, target: Path) -> None:
        row = {header: "fixture" for header in gate.REGISTER_HEADERS}
        row.update(
            {
                "modification_id": "P13.8-FIXTURE-001",
                "path": target.relative_to(product).as_posix(),
                "change_class": "AGENT_PLATFORM_product_addition",
                "baseline_upstream_commit": "0" * 40,
                "baseline_source_object_or_none": "none",
                "baseline_source_sha256_or_none": "none",
                "current_product_sha256_or_none": sha256(target),
                "upstream_disposition": "retain_product_divergence",
            }
        )
        with (product / "AGENT_PLATFORM_MODIFICATIONS.tsv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(
                handle, fieldnames=gate.REGISTER_HEADERS, delimiter="\t"
            )
            writer.writeheader()
            writer.writerow(row)

    def test_register_reconciliation_hashes_owned_paths_and_rejects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            product = Path(directory)
            target = product / "web" / "src" / "agent-platform" / "fixture.ts"
            target.parent.mkdir(parents=True)
            target.write_text("export const fixture = true;\n", encoding="utf-8")
            self._write_register(product, target)
            result = gate._reconcile_modification_register(product)
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["product_owned_additions"], 1)
            target.write_text("export const fixture = false;\n", encoding="utf-8")
            with self.assertRaisesRegex(gate.QualityGateError, "hash mismatch"):
                gate._reconcile_modification_register(product)

    def test_atomic_json_replaces_destination_and_leaves_no_temp_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "result.json"
            target.write_text('{"old":true}', encoding="utf-8")
            gate._write_json_atomic(target, {"status": "passed"})
            self.assertEqual(
                json.loads(target.read_text(encoding="utf-8")), {"status": "passed"}
            )
            self.assertEqual(list(root.glob(".*.tmp")), [])

    def test_run_writes_failed_result_when_repository_validation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result_path = root / "result.json"
            result = gate.run_quality_gate(
                gate.GateConfig(repo_root=root, result_path=result_path, lanes=())
            )
            retained = json.loads(result_path.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "failed")
        self.assertEqual(retained["gate_id"], "P13.8")
        self.assertEqual(retained["failures"][0]["reason"], "internal_error")
        self.assertNotIn(str(root), json.dumps(retained))

    def test_orchestrator_cleans_dashboard_when_browser_lane_raises(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            product = root / "2_products" / "pepper-agent"
            target = product / "web" / "src" / "agent-platform" / "fixture.ts"
            target.parent.mkdir(parents=True)
            target.write_text("export const fixture = true;\n", encoding="utf-8")
            (product / "hermes_cli").mkdir()
            (product / "hermes_cli" / "main.py").write_text("", encoding="utf-8")
            (product / "web" / "package.json").write_text("{}", encoding="utf-8")
            self._write_register(product, target)
            fake_owned = mock.Mock()
            fake_owned.process = FakeProcess()
            fake_owned.finish_captures.return_value = {
                "stdout": {},
                "stderr": {},
            }
            dashboard = {"lane": "dashboard", "status": "passed"}
            result_path = root / "result.json"
            config = gate.GateConfig(
                repo_root=root,
                result_path=result_path,
                artifact_dir=root / "artifacts",
                lanes=("build", "dashboard", "browser"),
            )
            with (
                mock.patch.object(
                    gate,
                    "_run_command_lane",
                    return_value={"lane": "build", "status": "passed"},
                ),
                mock.patch.object(
                    gate,
                    "_start_dashboard",
                    return_value=(fake_owned, dashboard, 54321),
                ),
                mock.patch.object(
                    gate,
                    "_run_browser_lane",
                    side_effect=RuntimeError("fixture failure"),
                ),
                mock.patch.object(
                    gate,
                    "_terminate_process_tree",
                    return_value={"exited": True, "method": "fixture"},
                ) as terminate,
            ):
                result = gate.run_quality_gate(config)
            result_written = result_path.is_file()
        terminate.assert_called_once_with(
            fake_owned.process, config.cleanup_timeout_seconds
        )
        fake_owned.finish_captures.assert_called_once()
        self.assertEqual(result["cleanup"]["status"], "passed")
        self.assertEqual(result["status"], "failed")
        self.assertTrue(result_written)


if __name__ == "__main__":
    unittest.main()
