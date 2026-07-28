from __future__ import annotations

import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    ROOT
    / "10_scripts"
    / "hermes"
    / "agent_platform_pepper_windows_credential_store_protection_smoke.py"
)
SPEC = importlib.util.spec_from_file_location(
    "agent_platform_pepper_windows_credential_store_protection_smoke",
    SCRIPT_PATH,
)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)

PRODUCT_ROOT = ROOT / "2_products" / "pepper-agent"


class PepperWindowsCredentialStoreProtectionSmokeTests(unittest.TestCase):
    def test_parser_exposes_format_and_status_without_path_authority(self) -> None:
        parser = gate._build_parser()
        parser_actions = {action.dest for action in parser._actions}
        self.assertNotIn("repository_root", parser_actions)
        self.assertNotIn("repo_root", parser_actions)
        self.assertNotIn("product_root", parser_actions)
        self.assertNotIn("trusted_store_root", parser_actions)
        self.assertNotIn("auth_file", parser_actions)
        parsed_default = parser.parse_args(["--format", "json"])
        self.assertIsNone(parsed_default.action)
        self.assertEqual(parsed_default.format, "json")
        parsed = parser.parse_args(["status"])
        self.assertEqual(parsed.action, "status")
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            parser.parse_args(["status", "--product-root", "x"])

    def test_status_uses_temporary_synthetic_store_and_pathless_json(self) -> None:
        case = self
        calls: list[tuple[str, str]] = []

        def report(path_role: str):
            return SimpleNamespace(
                path_role=path_role,
                platform="windows",
                protected=True,
                dacl_inspected=True,
                allowed_principal_count=3,
            )

        class FakeBackend:
            def prepare_directory(self, path: Path):
                calls.append(("prepare_directory", path.name))
                path.mkdir(parents=True, exist_ok=True)
                return report("store_directory")

            def prepare_file(self, path: Path):
                calls.append(("prepare_file", path.name))
                case.assertTrue(path.is_file())
                return report("auth_file")

            def validate_directory(self, path: Path):
                calls.append(("validate_directory", path.name))
                case.assertTrue(path.is_dir())
                return report("store_directory")

            def validate_file(self, path: Path):
                calls.append(("validate_file", path.name))
                case.assertTrue(path.is_file())
                return report("auth_file")

        fake_backend = FakeBackend()
        fake_store = SimpleNamespace(StoreProtectionBackend=lambda: fake_backend)
        config = gate.WindowsProtectionSmokeConfig(product_root=PRODUCT_ROOT)

        result = gate.run_status(
            config,
            module_loader=lambda product_root: fake_store,
            platform_name="win32",
        )
        output = json.dumps(result, sort_keys=True)

        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["verdict"], gate.VERDICT)
        self.assertEqual(
            result["verdict"],
            "pepper_windows_credential_store_protection_smoke_passed",
        )
        self.assertEqual(result["platform"], "windows")
        self.assertEqual(result["directory"]["path_role"], "store_directory")
        self.assertEqual(result["file"]["path_role"], "auth_file")
        self.assertEqual(result["forbidden_principal_count"], 0)
        self.assertEqual(result["runtime_residue"], 0)
        self.assertEqual(result["credential_operations"], 0)
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["OAuth_attempts"], 0)
        self.assertTrue(result["temporary_root_removed"])
        self.assertTrue(result["synthetic_store"]["cleanup_removed"])
        self.assertFalse(result["synthetic_store"]["payload_contains_credentials"])
        self.assertEqual(
            calls,
            [
                ("prepare_directory", "store"),
                ("prepare_file", "auth.json"),
                ("validate_directory", "store"),
                ("validate_file", "auth.json"),
            ],
        )
        for summary in result["protection_reports"].values():
            self.assertEqual(summary["platform"], "windows")
            self.assertTrue(summary["protected"])
            self.assertTrue(summary["dacl_inspected"])
            self.assertEqual(summary["allowed_principal_count"], 3)
        self.assertEqual(result["forbidden_activity"]["provider_calls"], 0)
        self.assertEqual(result["forbidden_activity"]["real_auth_store_reads"], 0)
        lowered = output.lower()
        for forbidden in (
            str(ROOT).lower(),
            str(PRODUCT_ROOT).lower(),
            "access_token",
            "refresh_token",
            "session-token",
            "cookie",
            "openai_api_key",
            "authorization",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_status_requires_native_windows(self) -> None:
        config = gate.WindowsProtectionSmokeConfig(product_root=PRODUCT_ROOT)
        with self.assertRaises(gate.WindowsProtectionSmokeError):
            gate.run_status(
                config,
                module_loader=lambda _product_root: None,
                platform_name="linux",
            )

    def test_main_can_be_validated_without_native_acl_by_patching_status(self) -> None:
        fake_result = {
            "schema_version": gate.SCHEMA_VERSION,
            "gate_id": gate.GATE_ID,
            "status": "passed",
            "verdict": gate.VERDICT,
            "forbidden_activity": {"provider_calls": 0},
        }
        with (
            mock.patch.object(gate, "run_status", return_value=fake_result) as status,
            mock.patch("builtins.print") as printed,
        ):
            exit_code = gate.main(["--format", "json"])
        status.assert_called_once_with()
        printed.assert_called_once()
        output = json.loads(printed.call_args.args[0])
        self.assertEqual(exit_code, 0)
        self.assertEqual(output["verdict"], gate.VERDICT)


if __name__ == "__main__":
    unittest.main()
