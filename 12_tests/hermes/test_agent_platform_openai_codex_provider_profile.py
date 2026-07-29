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
    ROOT / "10_scripts" / "hermes" / "agent_platform_openai_codex_provider_profile.py"
)
SPEC = importlib.util.spec_from_file_location(
    "agent_platform_openai_codex_provider_profile",
    SCRIPT_PATH,
)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)

PRODUCT_ROOT = ROOT / "2_products" / "pepper-agent"
if str(PRODUCT_ROOT) not in sys.path:
    sys.path.insert(0, str(PRODUCT_ROOT))


class ProviderProfileGateTests(unittest.TestCase):
    def test_parser_exposes_status_only_without_path_authority(self) -> None:
        parser = gate._build_parser()
        parser_actions = {action.dest for action in parser._actions}
        self.assertNotIn("repository_root", parser_actions)
        self.assertNotIn("repo_root", parser_actions)
        self.assertNotIn("product_root", parser_actions)
        self.assertNotIn("trusted_store_root", parser_actions)
        parsed = parser.parse_args(["status"])
        self.assertEqual(parsed.action, "status")
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            parser.parse_args(["status", "--product-root", "x"])

    def test_status_uses_injected_product_root_and_prints_bounded_json(self) -> None:
        from hermes_cli import auth, codex_models, providers
        from hermes_cli.agent_platform import provider_runtime

        with tempfile.TemporaryDirectory() as directory:
            synthetic_product_root = Path(directory) / "product"
            config = gate.ProviderProfileGateConfig(product_root=synthetic_product_root)

            def fake_loader(product_root: Path):
                self.assertEqual(product_root, synthetic_product_root)
                return gate.ProviderProfileModules(
                    provider_runtime=provider_runtime,
                    auth=auth,
                    providers=providers,
                    codex_models=codex_models,
                )

            result = gate.run_status(config, module_loader=fake_loader)
            output = json.dumps(result, sort_keys=True)

        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["verdict"], gate.VERDICT)
        self.assertEqual(result["registry"]["profile_count"], 1)
        self.assertEqual(
            result["registry"]["profile_ids"],
            ["provider.openai-codex.chatgpt-oauth.gpt-5.5.v1"],
        )
        profile = result["provider_runtime_profile"]
        self.assertEqual(profile["profile_id"], result["registry"]["profile_ids"][0])
        self.assertEqual(profile["state"], "runtime_unverified")
        self.assertEqual(profile["provider"], "openai-codex")
        self.assertEqual(profile["authentication"], "chatgpt_oauth")
        self.assertEqual(profile["transport"], "codex_responses")
        self.assertEqual(profile["model_id"], "gpt-5.5")
        self.assertEqual(
            profile["provider_endpoint"], "https://chatgpt.com/backend-api/codex"
        )
        self.assertTrue(profile["worker_profile_required"])
        self.assertFalse(profile["runtime_entitlement_verified"])
        self.assertFalse(profile["runtime_transport_verified"])
        self.assertFalse(result["endpoint_policy"]["base_url_override_allowed"])
        self.assertEqual(result["generation_policy"]["streaming"], "disabled")
        self.assertEqual(result["generation_policy"]["tools"], "disabled")
        self.assertEqual(result["generation_policy"]["MCP"], "disabled")
        self.assertEqual(result["generation_policy"]["automatic_retry"], "disabled")
        self.assertEqual(result["generation_policy"]["automatic_fallback"], "disabled")
        self.assertEqual(
            result["usage_evidence_policy"]["exact_marginal_request_cost"],
            "unavailable_by_default",
        )
        self.assertTrue(
            result["hermes_evidence"]["auth_default_endpoint_matches_profile"]
        )
        self.assertTrue(result["hermes_evidence"]["codex_catalog_contains_model"])
        self.assertTrue(result["hermes_evidence"]["profile_transport_matches_overlay"])
        self.assertEqual(result["forbidden_activity"]["provider_calls"], 0)
        lowered = output.lower()
        for forbidden in (
            str(ROOT).lower(),
            str(synthetic_product_root).lower(),
            "forbidden-sensitive-value",
            "session-token",
            "cookie",
            "openai_api_key",
            "authorization",
            "auth.json",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_main_can_be_validated_without_real_imports_by_patching_status(
        self,
    ) -> None:
        fake_result = {
            "schema_version": gate.SCHEMA_VERSION,
            "gate_id": gate.GATE_ID,
            "status": "passed",
            "verdict": gate.VERDICT,
            "provider_runtime_profile": {
                "hermes_provider_id": "openai-codex",
                "model_id": "gpt-5.5",
            },
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
