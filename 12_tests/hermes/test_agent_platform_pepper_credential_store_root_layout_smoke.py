from __future__ import annotations

import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    ROOT
    / "10_scripts"
    / "hermes"
    / "agent_platform_pepper_credential_store_root_layout_smoke.py"
)
SPEC = importlib.util.spec_from_file_location(
    "agent_platform_pepper_credential_store_root_layout_smoke",
    SCRIPT_PATH,
)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)

PRODUCT_ROOT = ROOT / "2_products" / "pepper-agent"


class PepperCredentialStoreRootLayoutSmokeTests(unittest.TestCase):
    def assert_success_result(self, result: dict[str, object]) -> None:
        self.assertEqual(
            result["verdict"], "pepper_credential_store_root_layout_smoke_passed"
        )
        canonical = result["canonical_layout"]
        legacy = result["legacy_layout"]
        ambiguous = result["ambiguous_layout"]
        self.assertTrue(canonical["exact_segments"])
        self.assertEqual(canonical["duplicate_segments"], 0)
        self.assertTrue(canonical["selected_when_absent"])
        self.assertTrue(canonical["selected_when_present"])
        self.assertTrue(legacy["exact_segments"])
        self.assertTrue(legacy["selected_when_canonical_absent"])
        self.assertFalse(legacy["created_by_resolver"])
        self.assertTrue(ambiguous["fail_closed"])
        self.assertEqual(
            ambiguous["failure_category"],
            "ambiguous_canonical_and_legacy_credential_store_roots",
        )
        self.assertTrue(result["temporary_root_removed"])
        self.assertEqual(result["runtime_residue"], 0)
        self.assertEqual(result["real_credential_reads"], 0)
        self.assertEqual(result["real_credential_writes"], 0)
        self.assertEqual(result["credential_copies"], 0)
        self.assertEqual(result["credential_moves"], 0)
        self.assertEqual(result["credential_deletes"], 0)
        self.assertEqual(result["OAuth_attempts"], 0)
        self.assertEqual(result["provider_calls"], 0)

    def test_module_import_and_parser_defaults_to_text(self) -> None:
        parser = gate._build_parser()
        self.assertEqual(parser.parse_args([]).format, "text")
        self.assertEqual(parser.parse_args(["--format", "json"]).format, "json")

    def test_status_validates_canonical_legacy_and_ambiguous_layouts(self) -> None:
        result = gate._build_status()
        self.assert_success_result(result)

    def test_text_output_is_pathless_and_secret_free(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = gate.main(["--format", "text"])
        text = output.getvalue().lower()

        self.assertEqual(exit_code, 0)
        self.assertIn("verdict=pepper_credential_store_root_layout_smoke_passed", text)
        self.assertIn("ambiguous_fail_closed=True".lower(), text)
        self.assertNotIn(str(ROOT).lower(), text)
        self.assertNotIn(str(PRODUCT_ROOT).lower(), text)
        for forbidden in (
            "access_token",
            "refresh_token",
            "authorization",
            "auth.json",
        ):
            self.assertNotIn(forbidden, text)

    def test_json_output_is_pathless_secret_free_and_validated(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = gate.main(["--format", "json"])
        text = output.getvalue()
        result = json.loads(text)

        self.assertEqual(exit_code, 0)
        self.assert_success_result(result)
        lowered = text.lower()
        self.assertNotIn(str(ROOT).lower(), lowered)
        self.assertNotIn(str(PRODUCT_ROOT).lower(), lowered)
        for forbidden in (
            "access_token",
            "refresh_token",
            "authorization",
            "auth.json",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_real_home_and_credential_access_are_absent(self) -> None:
        with mock.patch.object(gate.Path, "home", side_effect=AssertionError):
            result = gate._build_status()

        self.assert_success_result(result)


if __name__ == "__main__":
    unittest.main()
