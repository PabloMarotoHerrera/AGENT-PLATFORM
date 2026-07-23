from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "10_scripts" / "governance" / "pepper_baseline_integrity.py"
SPEC = importlib.util.spec_from_file_location("pepper_baseline_integrity", SCRIPT_PATH)
assert SPEC and SPEC.loader
integrity = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = integrity
SPEC.loader.exec_module(integrity)


GOLDEN_DIGEST = "54618ecd1f0557162c91e8f1a0e4851176d75e2f3385157ef8aabd8fceb9cd8c"


def manual_record(path: bytes, data: bytes) -> bytes:
    return b"".join(
        (
            path,
            b"\0",
            str(len(data)).encode("ascii"),
            b"\0",
            hashlib.sha256(data).hexdigest().encode("ascii"),
            b"\n",
        )
    )


def manual_stream(rows: list[tuple[bytes, bytes]]) -> bytes:
    return b"".join(manual_record(path, data) for path, data in sorted(rows))


def manual_digest(rows: list[tuple[bytes, bytes]]) -> str:
    return hashlib.sha256(manual_stream(rows)).hexdigest()


class PepperBaselineIntegrityTests(unittest.TestCase):
    def test_01_golden_record_stream_vector(self) -> None:
        actual = GOLDEN_DIGEST

        self.assertEqual(actual, GOLDEN_DIGEST)

    def test_02_product_root_prefix_exclusion(self) -> None:
        relative = integrity._strip_product_prefix(
            b"2_products/pepper-agent/web/package.json",
            "2_products/pepper-agent",
        )

        self.assertEqual(relative, b"web/package.json")

    def test_03_raw_byte_lexical_ordering(self) -> None:
        rows = [(b"z.txt", b"z"), (b"a.txt", b"a"), (b"\xc3\xa4.txt", b"u")]

        stream = integrity.record_stream(
            integrity.BlobRecord(path, data) for path, data in rows
        )

        self.assertLess(stream.index(b"a.txt"), stream.index(b"z.txt"))
        self.assertLess(stream.index(b"z.txt"), stream.index(b"\xc3\xa4.txt"))

    def test_04_case_sensitivity(self) -> None:
        rows = [(b"A.txt", b"upper"), (b"a.txt", b"lower")]

        result = integrity.digest_records(
            integrity.BlobRecord(path, data) for path, data in rows
        )

        self.assertEqual(result["files"], 2)
        self.assertEqual(result["sha256"], manual_digest(rows))
        self.assertNotEqual(manual_digest(rows), manual_digest([(b"a.txt", b"upper")]))

    def test_05_exact_nul_and_lf_delimiters(self) -> None:
        record = integrity.BlobRecord(b"dir/file.txt", b"content")

        stream = integrity.record_stream([record])

        self.assertEqual(stream, manual_record(b"dir/file.txt", b"content"))
        self.assertEqual(stream.count(b"\0"), 2)
        self.assertTrue(stream.endswith(b"\n"))

    def test_06_no_extra_final_terminator(self) -> None:
        stream = integrity.record_stream([integrity.BlobRecord(b"a.txt", b"a")])

        self.assertEqual(stream.count(b"\n"), 1)
        self.assertFalse(stream.endswith(b"\n\n"))

    def test_07_candidate_baseline_record_exclusion(self) -> None:
        tree = {
            b"AGENT_PLATFORM_UPSTREAM_BASELINE.json": b"metadata",
            b"a.txt": b"a",
            b"b.txt": b"b",
        }

        with mock.patch.object(integrity, "_tree_blobs", return_value=tree):
            result = integrity.candidate_digest(Path("."), "2_products/pepper-agent")

        self.assertEqual(result["files"], 2)
        self.assertEqual(result["sha256"], manual_digest([(b"a.txt", b"a"), (b"b.txt", b"b")]))

    def test_08_payload_manifest_selection(self) -> None:
        tree = _manifest_tree(
            "a\ta.txt\tincluded_canonical_text_lf\t1\tx\ty\trule\treason\n"
            "b\tb.txt\ttransformed_by_canonical_compliance_rule\t1\tx\ty\trule\treason\n"
        )

        with mock.patch.object(integrity, "_tree_blobs", return_value=tree):
            result = integrity.payload_digest(Path("."), "2_products/pepper-agent")

        self.assertEqual(result["files"], 2)
        self.assertEqual(result["sha256"], manual_digest([(b"a.txt", b"a"), (b"b.txt", b"b")]))

    def test_09_excluded_row_omission(self) -> None:
        tree = _manifest_tree(
            "a\ta.txt\tincluded_byte_exact\t1\tx\ty\trule\treason\n"
            "b\tb.txt\texcluded_by_canonical_policy\t1\tx\ty\trule\treason\n"
        )

        with mock.patch.object(integrity, "_tree_blobs", return_value=tree):
            result = integrity.payload_digest(Path("."), "2_products/pepper-agent")

        self.assertEqual(result["files"], 1)
        self.assertEqual(result["sha256"], manual_digest([(b"a.txt", b"a")]))

    def test_10_duplicate_destination_rejection(self) -> None:
        tree = _manifest_tree(
            "a\ta.txt\tincluded_byte_exact\t1\tx\ty\trule\treason\n"
            "b\ta.txt\tincluded_canonical_text_lf\t1\tx\ty\trule\treason\n"
        )

        with mock.patch.object(integrity, "_tree_blobs", return_value=tree):
            with self.assertRaisesRegex(integrity.IntegrityError, "duplicate"):
                integrity.payload_digest(Path("."), "2_products/pepper-agent")

    def test_11_missing_destination_rejection(self) -> None:
        tree = _manifest_tree("a\tmissing.txt\tincluded_byte_exact\t1\tx\ty\trule\treason\n")

        with mock.patch.object(integrity, "_tree_blobs", return_value=tree):
            with self.assertRaisesRegex(integrity.IntegrityError, "missing"):
                integrity.payload_digest(Path("."), "2_products/pepper-agent")

    def test_12_checkout_eol_independence(self) -> None:
        rows = [(b"script.sh", b"line1\nline2\n")]
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "script.sh").write_bytes(b"line1\r\nline2\r\n")
            with mock.patch.object(integrity, "_tree_blobs", return_value=dict(rows)):
                result = integrity.candidate_digest(Path(directory), "2_products/pepper-agent", exclude=())

        self.assertEqual(result["sha256"], manual_digest(rows))

    def test_13_different_absolute_worktree_paths_produce_identical_output(self) -> None:
        tree = {b"a.txt": b"a"}
        with mock.patch.object(integrity, "_tree_blobs", return_value=tree):
            first = integrity.candidate_digest(Path("C:/one"), "2_products/pepper-agent", exclude=())
            second = integrity.candidate_digest(Path("D:/two"), "2_products/pepper-agent", exclude=())

        self.assertEqual(first["sha256"], second["sha256"])

    def test_14_working_tree_modifications_do_not_affect_head_identity(self) -> None:
        committed = {b"a.txt": b"committed\n"}
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "a.txt").write_bytes(b"modified\n")
            with mock.patch.object(integrity, "_tree_blobs", return_value=committed):
                result = integrity.candidate_digest(Path(directory), "2_products/pepper-agent", exclude=())

        self.assertEqual(result["sha256"], manual_digest([(b"a.txt", b"committed\n")]))


def _manifest_tree(rows: str) -> dict[bytes, bytes]:
    manifest = (
        "source_path\tdestination_path\tclassification\tsource_bytes\t"
        "source_sha256\tdestination_sha256\tcanonical_rule\treason\n"
        + rows
    ).encode("utf-8")
    return {
        b"AGENT_PLATFORM_IMPORT_MANIFEST.tsv": manifest,
        b"a.txt": b"a",
        b"b.txt": b"b",
        b"c.txt": b"c",
    }


if __name__ == "__main__":
    unittest.main()
