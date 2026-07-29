from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    ROOT / "10_scripts" / "hermes" / "agent_platform_openai_codex_oauth_boundary.py"
)
SPEC = importlib.util.spec_from_file_location(
    "agent_platform_openai_codex_oauth_boundary",
    SCRIPT_PATH,
)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)

PRODUCT_ROOT = ROOT / "2_products" / "pepper-agent"
if str(PRODUCT_ROOT) not in sys.path:
    sys.path.insert(0, str(PRODUCT_ROOT))
from hermes_cli.agent_platform.provider_credentials import contracts, delivery  # noqa: E402


class BoundaryGateTests(unittest.TestCase):
    def test_parser_exposes_status_only_without_path_authority(self) -> None:
        parser = gate._build_parser()
        parser_actions = {action.dest for action in parser._actions}
        self.assertNotIn("repository_root", parser_actions)
        self.assertNotIn("repo_root", parser_actions)
        self.assertNotIn("synthetic_hermes_home", parser_actions)
        self.assertNotIn("trusted_store_root", parser_actions)
        self.assertNotIn("lease_root", parser_actions)
        parsed = parser.parse_args(["status"])
        self.assertEqual(parsed.action, "status")
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            parser.parse_args(["status", "--synthetic-hermes-home", "x"])

    def test_status_uses_injected_synthetic_root_and_prints_bounded_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            synthetic_root = Path(directory) / "synthetic-store"
            config = gate.BoundaryGateConfig(
                product_root=PRODUCT_ROOT,
                trusted_store_root=synthetic_root,
            )

            def fake_reader(root: Path):
                self.assertEqual(root, synthetic_root)
                return contracts.ProviderCredentialStatus(
                    configured=False,
                    durable_store_present=False,
                    durable_store_valid=False,
                    protection_valid=False,
                    provider_state_present=False,
                    pool_state_present=False,
                    token_pair_present=False,
                    credential_count=0,
                    active_provider_matches=False,
                )

            def fake_planner(*, product_root: Path, trusted_acquisition_root: Path):
                self.assertEqual(product_root, PRODUCT_ROOT)
                self.assertEqual(trusted_acquisition_root, synthetic_root)
                return SimpleNamespace(
                    public_plan=contracts.ProviderCredentialAcquisitionPlan(
                        command_argv_suffix=(
                            "-m",
                            "hermes_cli.main",
                            "auth",
                            "add",
                            "openai-codex",
                            "--type",
                            "oauth",
                        ),
                        environment_keys=(
                            "HERMES_HOME",
                            "HOME",
                            "USERPROFILE",
                            "APPDATA",
                            "LOCALAPPDATA",
                            "PYTHONIOENCODING",
                            "PYTHONUTF8",
                        ),
                    )
                )

            result = gate.run_status(
                config,
                status_reader=fake_reader,
                acquisition_planner=fake_planner,
            )
            output = json.dumps(result, sort_keys=True)

        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["verdict"], gate.VERDICT)
        self.assertEqual(result["credential_contract"]["provider"], "openai_codex")
        self.assertEqual(
            result["credential_contract"]["auth_kind"], "chatgpt_oauth_device"
        )
        self.assertEqual(result["delivery_boundary"]["maximum_active_leases"], 1)
        self.assertFalse(result["oauth_acquisition_boundary"]["caller_label_allowed"])
        self.assertFalse(
            result["oauth_acquisition_boundary"]["endpoint_override_allowed"]
        )
        self.assertFalse(result["forbidden_activity"]["browser_opened"])
        lowered = output.lower()
        for forbidden in (
            str(ROOT).lower(),
            str(synthetic_root).lower(),
            "access_token",
            "refresh_token",
            "session-token",
            "cookie",
            "openai_api_key",
            "authorization",
            "auth.json",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_main_can_be_validated_without_real_store_by_patching_status(self) -> None:
        fake_result = {
            "schema_version": gate.SCHEMA_VERSION,
            "gate_id": gate.GATE_ID,
            "status": "passed",
            "verdict": gate.VERDICT,
            "credential_contract": {
                "provider": contracts.ProviderCredentialProvider.OPENAI_CODEX.value,
                "auth_kind": contracts.ProviderCredentialAuthKind.CHATGPT_OAUTH_DEVICE.value,
            },
            "delivery_boundary": {"lease_marker_name": delivery.LEASE_MARKER_NAME},
            "forbidden_activity": {"provider_calls": 0},
        }
        with (
            mock.patch.object(gate, "run_status", return_value=fake_result) as status,
            mock.patch("builtins.print") as printed,
        ):
            exit_code = gate.main(["status"])
        status.assert_called_once_with()
        printed.assert_called_once()
        output = json.loads(printed.call_args.args[0])
        self.assertEqual(exit_code, 0)
        self.assertEqual(output["verdict"], gate.VERDICT)


if __name__ == "__main__":
    unittest.main()
