from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    ROOT / "10_scripts" / "hermes" / "agent_platform_openai_codex_worker_profile.py"
)
SPEC = importlib.util.spec_from_file_location(
    "agent_platform_openai_codex_worker_profile",
    SCRIPT_PATH,
)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)

PRODUCT_ROOT = ROOT / "2_products" / "pepper-agent"
if str(PRODUCT_ROOT) not in sys.path:
    sys.path.insert(0, str(PRODUCT_ROOT))


class WorkerProfileGateTests(unittest.TestCase):
    def test_parser_exposes_status_only_without_runtime_authority(self) -> None:
        parser = gate._build_parser()
        parser_actions = {action.dest for action in parser._actions}
        for forbidden in (
            "provider",
            "model",
            "endpoint",
            "token",
            "prompt",
            "repository_root",
            "product_root",
            "credential_path",
            "lease_path",
            "command",
            "argv",
            "workspace",
        ):
            self.assertNotIn(forbidden, parser_actions)
        parsed = parser.parse_args(["status"])
        self.assertEqual(parsed.action, "status")
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            parser.parse_args(["status", "--provider", "openai-codex"])

    def test_status_uses_injected_product_root_and_prints_bounded_json(self) -> None:
        from hermes_cli.agent_platform import provider_worker

        with tempfile.TemporaryDirectory() as directory:
            synthetic_product_root = Path(directory) / "product"
            config = gate.WorkerProfileGateConfig(product_root=synthetic_product_root)

            def fake_loader(product_root: Path):
                self.assertEqual(product_root, synthetic_product_root)
                return gate.WorkerProfileModules(provider_worker=provider_worker)

            result = gate.run_status(config, module_loader=fake_loader)
            output = json.dumps(result, sort_keys=True)

        self.assertEqual(result["verdict"], gate.VERDICT)
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(
            result["worker_profile_id"],
            "worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1",
        )
        self.assertEqual(
            result["worker_profile_state"], "profile_ready_runtime_unverified"
        )
        self.assertEqual(
            result["provider_runtime_profile_id"],
            "provider.openai-codex.chatgpt-oauth.gpt-5.5.v1",
        )
        self.assertEqual(result["credential_store_id"], "openai-codex.primary")
        self.assertEqual(result["maximum_concurrent_workers"], 1)
        self.assertEqual(result["maximum_concurrent_requests"], 1)
        self.assertEqual(result["maximum_requests_per_worker_lifetime"], 1)
        self.assertEqual(result["request_queue_capacity"], 0)
        self.assertEqual(result["provider_calls_per_request_maximum"], 1)
        self.assertEqual(result["model_list_calls_per_request_maximum"], 0)
        self.assertEqual(result["credential_refresh_calls_per_request_maximum"], 0)
        self.assertEqual(result["input_kind"], "text")
        self.assertEqual(result["output_kind"], "text")
        self.assertFalse(result["streaming_enabled"])
        self.assertFalse(result["tools_enabled"])
        self.assertFalse(result["hosted_tools_enabled"])
        self.assertFalse(result["MCP_enabled"])
        self.assertFalse(result["automatic_retry_enabled"])
        self.assertFalse(result["automatic_fallback_enabled"])
        self.assertFalse(result["persistent_memory_enabled"])
        self.assertFalse(result["process_reuse_enabled"])
        self.assertTrue(result["inference_gate_required"])
        self.assertTrue(result["controlled_lifecycle_gate_required"])
        self.assertFalse(result["runtime_entitlement_verified"])
        self.assertFalse(result["runtime_transport_verified"])
        self.assertFalse(result["worker_runtime_verified"])

        lowered = output.lower()
        for forbidden in (
            str(ROOT).lower(),
            str(synthetic_product_root).lower(),
            "forbidden-sensitive-value",
            "session-token",
            "cookie",
            "authorization",
            "auth" + ".json",
            "endpoint_url",
            "command",
            "argv",
            "prompt",
            "output_text",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_main_can_be_validated_without_real_imports_by_patching_status(
        self,
    ) -> None:
        fake_result = {
            "schema_version": gate.SCHEMA_VERSION,
            "verdict": gate.VERDICT,
            "worker_profile_id": gate.WORKER_PROFILE_ID,
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

    def test_exit_codes_are_stable_for_bounded_failures(self) -> None:
        error_classes = {
            gate.WorkerProfileGateError: gate.UNEXPECTED_EXIT_CODE,
            gate.WorkerProfileRegistryError: gate.REGISTRY_EXIT_CODE,
            gate.WorkerProfileContractError: gate.CONTRACT_EXIT_CODE,
            gate.WorkerProviderProfileMismatchError: (
                gate.PROVIDER_PROFILE_MISMATCH_EXIT_CODE
            ),
            gate.WorkerProtocolPolicyError: gate.PROTOCOL_POLICY_EXIT_CODE,
        }
        for error_class, exit_code in error_classes.items():
            self.assertEqual(error_class.exit_code, exit_code)


if __name__ == "__main__":
    unittest.main()
