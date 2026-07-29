from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    ROOT / "10_scripts" / "hermes" / "agent_platform_runtime_adapter_lifecycle_gate.py"
)
SPEC = importlib.util.spec_from_file_location(
    "agent_platform_runtime_adapter_lifecycle_gate", SCRIPT_PATH
)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def _write_product_root(root: Path) -> Path:
    product = root / "2_products" / "pepper-agent"
    (product / "hermes_cli").mkdir(parents=True)
    (product / "hermes_cli" / "main.py").write_text("", encoding="utf-8")
    return product


def _write_editable_product_python(product: Path) -> Path:
    environment = product / ".venv"
    product_python = environment / "Scripts" / "python.exe"
    product_python.parent.mkdir(parents=True)
    product_python.write_text("", encoding="utf-8")
    (environment / "pyvenv.cfg").write_text(
        "include-system-site-packages = false\n",
        encoding="utf-8",
    )
    site_packages = environment / "Lib" / "site-packages"
    site_packages.mkdir(parents=True)
    (site_packages / "__editable__.hermes_agent-0.0.0.pth").write_text(
        str(product),
        encoding="utf-8",
    )
    (site_packages / "hermes_agent-0.0.0.dist-info").mkdir()
    return product_python


def _readiness_lifecycle_fields() -> dict[str, object]:
    check_ids = list(gate.EXPECTED_READINESS_CHECK_IDS)
    statuses = {
        "dashboard.root": 200,
        "dashboard.status": 200,
        "dashboard.product_config_unauthenticated": 401,
        "dashboard.product_config_authenticated": 200,
        "dashboard.plugin_manifest": 200,
        "dashboard.files_root": 200,
        "dashboard.files_outside_root": 403,
    }
    return {
        "readiness_check_count": 7,
        "readiness_check_ids": check_ids,
        "readiness_checks": [
            {
                "check_id": check_id,
                "status_code": statuses[check_id],
                "passed": True,
                "evidence": {},
            }
            for check_id in check_ids
        ],
        "event_count": 15,
        "audit_projection_count": 15,
        "gateway_running": False,
        "active_agent_count": 0,
        "active_session_count": 0,
        "provider_count": 0,
        "unauthenticated_config_status": 401,
        "authenticated_config_status": 200,
        "product_feature_state": "experimental",
        "extension_module_count": 9,
        "extension_module_order_valid": True,
        "plugin_manifest_valid": True,
        "plugin_route_conflict_count": 0,
        "managed_files_root_matches": True,
        "outside_files_root_denied": True,
    }


def _assert_bounded_output(text: str, *forbidden_paths: Path) -> None:
    lowered = text.lower()
    for value in (
        "session-token",
        "cookie",
        "set-cookie",
        "hermes_dashboard_session_token",
        "response_body",
        "raw_body",
        "command",
        "environment",
        " pid",
        '"pid"',
    ):
        assert value not in lowered
    for path in forbidden_paths:
        raw = str(path)
        assert raw not in text
        assert raw.replace("\\", "/") not in text


class ConfigurationTests(unittest.TestCase):
    def test_rejects_missing_product_and_arbitrary_command_surface(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = gate.GateConfig(repo_root=root, result_path=root / "result.json")
            with self.assertRaises(gate.LifecycleGateError):
                gate._validate_config(config)
        parser_actions = {action.dest for action in gate._build_parser()._actions}
        self.assertNotIn("command", parser_actions)
        self.assertNotIn("args", parser_actions)
        parsed = gate._build_parser().parse_args(
            ["--repository-root", ".", "--port", "9130"]
        )
        self.assertEqual(parsed.repo_root, Path("."))
        self.assertEqual(parsed.dashboard_port, 9130)

    def test_web_dist_short_circuits_build_when_prebuilt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            product = Path(directory) / "2_products" / "pepper-agent"
            dist = product / "hermes_cli" / "web_dist"
            dist.mkdir(parents=True)
            (dist / "index.html").write_text("<html></html>", encoding="utf-8")
            result = gate._ensure_web_dist(
                product,
                Path(directory) / "artifacts",
                timeout_seconds=1.0,
            )
        self.assertEqual(result["status"], "passed")
        self.assertFalse(result["built"])

    def test_build_uses_fixed_node_npm_argv_without_shell(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            product = Path(directory) / "2_products" / "pepper-agent"
            web = product / "web"
            web.mkdir(parents=True)
            (product / "hermes_cli").mkdir()
            node = Path(directory) / "node.exe"
            npm_cli = Path(directory) / "npm-cli.js"
            node.write_text("", encoding="utf-8")
            npm_cli.write_text("", encoding="utf-8")

            def fake_run(argv, **kwargs):
                (product / "hermes_cli" / "web_dist").mkdir()
                (product / "hermes_cli" / "web_dist" / "index.html").write_text(
                    "<html></html>", encoding="utf-8"
                )
                return mock.Mock(returncode=0, stdout=b"", stderr=b"")

            with (
                mock.patch.object(
                    gate, "_resolve_node_npm", return_value=(node, npm_cli)
                ),
                mock.patch.object(gate.subprocess, "run", side_effect=fake_run) as run,
            ):
                result = gate._ensure_web_dist(
                    product,
                    Path(directory) / "artifacts",
                    timeout_seconds=10.0,
                )

        self.assertEqual(result["status"], "passed")
        self.assertEqual(
            run.call_args.args[0], [str(node), str(npm_cli), "run", "build"]
        )
        self.assertIs(run.call_args.kwargs["stdin"], gate.subprocess.DEVNULL)


class GateResultTests(unittest.TestCase):
    def test_success_prints_one_bounded_json_summary_without_result_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            product = _write_product_root(root)
            product_python = _write_editable_product_python(product)
            result_path = root / "result.json"
            with (
                mock.patch.object(
                    gate, "_ensure_web_dist", return_value={"status": "passed"}
                ),
                mock.patch.object(
                    gate,
                    "_run_adapter_lifecycle",
                    return_value={
                        "status": "passed",
                        "runtime_id": "rt.p148.fixture",
                        "correlation_id": "corr.p148.fixture",
                        **_readiness_lifecycle_fields(),
                    },
                ) as lifecycle,
                mock.patch("builtins.print") as printed,
            ):
                exit_code = gate.main(
                    [
                        "--repository-root",
                        str(root),
                        "--result",
                        str(result_path),
                        "--port",
                        "9130",
                    ]
                )

            printed.assert_called_once()
            output = printed.call_args.args[0]
            result = json.loads(output)

        self.assertEqual(exit_code, 0)
        self.assertFalse(result_path.exists())
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["verdict"], gate.VERDICT)
        self.assertEqual(result["python_executable"], "<product-python>")
        self.assertEqual(result["repo_root"], "<repository-root>")
        self.assertEqual(result["artifact_dir"], "<artifact-dir>")
        _assert_bounded_output(output, root, product_python.resolve(), result_path)
        self.assertEqual(result["lifecycle"]["readiness_check_count"], 7)
        self.assertEqual(
            result["lifecycle"]["readiness_check_ids"],
            list(gate.EXPECTED_READINESS_CHECK_IDS),
        )
        self.assertEqual(result["lifecycle"]["event_count"], 15)
        self.assertEqual(result["lifecycle"]["audit_projection_count"], 15)
        self.assertFalse(result["lifecycle"]["gateway_running"])
        self.assertEqual(
            lifecycle.call_args.kwargs["python_executable"], product_python.resolve()
        )
        self.assertEqual(lifecycle.call_args.kwargs["dashboard_port"], 9130)

    def test_rejects_incomplete_readiness_summary(self) -> None:
        summary = {
            "check_count": 6,
            "check_ids": [
                "dashboard.root",
                "dashboard.status",
                "dashboard.product_config_unauthenticated",
                "dashboard.product_config_authenticated",
                "dashboard.plugin_manifest",
                "dashboard.files_root",
            ],
            "checks": [],
        }

        with self.assertRaises(gate.LifecycleGateError):
            gate._validate_readiness_summary(
                summary,
                gate.EXPECTED_READINESS_CHECK_IDS,
            )

    def test_passed_verdict_requires_seven_readiness_checks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            product = _write_product_root(root)
            _write_editable_product_python(product)
            bad_lifecycle = {
                "status": "passed",
                "runtime_id": "rt.p148.fixture",
                "correlation_id": "corr.p148.fixture",
                **_readiness_lifecycle_fields(),
            }
            bad_lifecycle["readiness_check_count"] = 6
            bad_lifecycle["readiness_check_ids"] = bad_lifecycle["readiness_check_ids"][
                :-1
            ]
            bad_lifecycle["readiness_checks"] = bad_lifecycle["readiness_checks"][:-1]
            with (
                mock.patch.object(
                    gate, "_ensure_web_dist", return_value={"status": "passed"}
                ),
                mock.patch.object(
                    gate,
                    "_run_adapter_lifecycle",
                    return_value=bad_lifecycle,
                ),
            ):
                result = gate.run_lifecycle_gate(
                    gate.GateConfig(repo_root=root, result_path=root / "result.json")
                )

        self.assertEqual(result["status"], "failed")
        self.assertIsNone(result["verdict"])
        self.assertIn("seven checks", result["failures"][0]["reason"])

    def test_failure_prints_sanitized_json_without_result_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            product = _write_product_root(root)
            _write_editable_product_python(product)
            result_path = root / "result.json"
            with (
                mock.patch.object(
                    gate,
                    "_ensure_web_dist",
                    side_effect=gate.LifecycleGateError("failure in " + str(root)),
                ),
                mock.patch("builtins.print") as printed,
            ):
                exit_code = gate.main(
                    [
                        "--repository-root",
                        str(root),
                        "--result",
                        str(result_path),
                    ]
                )
            printed.assert_called_once()
            output = printed.call_args.args[0]
            result = json.loads(output)

        self.assertEqual(exit_code, 1)
        self.assertFalse(result_path.exists())
        self.assertEqual(result["status"], "failed")
        self.assertIsNone(result["verdict"])
        _assert_bounded_output(output, root, result_path)


class ProductPythonResolutionTests(unittest.TestCase):
    def test_missing_product_python_writes_prerequisite_without_ambient_fallback(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _write_product_root(root)
            ambient_python = root / "ambient" / "python.exe"
            ambient_python.parent.mkdir()
            ambient_python.write_text("", encoding="utf-8")
            result_path = root / "result.json"
            with (
                mock.patch.object(gate.sys, "executable", str(ambient_python)),
                mock.patch.object(gate, "_ensure_web_dist") as ensure,
                mock.patch.object(gate, "_resolve_node_npm") as resolve_npm,
                mock.patch.object(gate.subprocess, "run") as subprocess_run,
            ):
                result = gate.run_lifecycle_gate(
                    gate.GateConfig(repo_root=root, result_path=result_path)
                )

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["exit_code"], gate.PREREQUISITE_EXIT_CODE)
        self.assertFalse(result_path.exists())
        self.assertIsNone(result["verdict"])
        self.assertIsNone(result["python_executable"])
        self.assertNotIn(str(ambient_python), json.dumps(result))
        ensure.assert_not_called()
        resolve_npm.assert_not_called()
        subprocess_run.assert_not_called()

    def test_rejects_non_editable_product_environment_before_build(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            product = _write_product_root(root)
            environment = product / ".venv"
            product_python = environment / "Scripts" / "python.exe"
            product_python.parent.mkdir(parents=True)
            product_python.write_text("", encoding="utf-8")
            (environment / "pyvenv.cfg").write_text("", encoding="utf-8")
            result_path = root / "result.json"
            with mock.patch.object(gate, "_ensure_web_dist") as ensure:
                result = gate.run_lifecycle_gate(
                    gate.GateConfig(repo_root=root, result_path=result_path)
                )

        self.assertEqual(result["exit_code"], gate.PREREQUISITE_EXIT_CODE)
        self.assertIn("editable Hermes package", result["failures"][0]["reason"])
        ensure.assert_not_called()

    def test_rejects_requested_python_outside_product_environment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _write_product_root(root)
            outside_python = root / "outside" / "python.exe"
            outside_python.parent.mkdir()
            outside_python.write_text("", encoding="utf-8")
            result_path = root / "result.json"
            with mock.patch.object(gate, "_ensure_web_dist") as ensure:
                result = gate.run_lifecycle_gate(
                    gate.GateConfig(
                        repo_root=root,
                        result_path=result_path,
                        python_executable=outside_python,
                    )
                )

        self.assertEqual(result["exit_code"], gate.PREREQUISITE_EXIT_CODE)
        self.assertIn(
            "outside the editable product environment", result["failures"][0]["reason"]
        )
        ensure.assert_not_called()

    def test_main_returns_prerequisite_exit_code(self) -> None:
        with (
            mock.patch.object(
                gate,
                "run_lifecycle_gate",
                return_value={
                    "status": "failed",
                    "verdict": None,
                    "exit_code": gate.PREREQUISITE_EXIT_CODE,
                },
            ),
            mock.patch("builtins.print"),
        ):
            exit_code = gate.main([])

        self.assertEqual(exit_code, gate.PREREQUISITE_EXIT_CODE)


if __name__ == "__main__":
    unittest.main()
