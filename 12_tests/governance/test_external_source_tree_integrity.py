from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "10_scripts" / "governance" / "external_source_tree_integrity.py"
SPEC = importlib.util.spec_from_file_location("external_source_tree_integrity", SCRIPT_PATH)
assert SPEC and SPEC.loader
integrity = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = integrity
SPEC.loader.exec_module(integrity)


GOLDEN_DIGEST = "f7946e3f418e07edabc08a18183c6fd4759c8406730fc4dfa846af718ca32a0c"


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


class ExternalSourceTreeIntegrityTests(unittest.TestCase):
    def test_01_golden_record_stream_vector(self) -> None:
        rows = [(b"b.txt", b"Beta\n"), (b"a.txt", b"Alpha\n"), (b"dir/zero.bin", b"")]

        actual = hashlib.sha256(
            integrity.record_stream(integrity.FileRecord(path, data) for path, data in rows)
        ).hexdigest()

        self.assertEqual(actual, GOLDEN_DIGEST)

    def test_02_empty_digest_vector(self) -> None:
        result = integrity.SourceScan(integrity.MATERIALIZED_SOURCE_ALGORITHM, (), 0, 0)

        self.assertEqual(result.files, 0)
        self.assertEqual(result.bytes, 0)
        self.assertEqual(result.sha256, hashlib.sha256(b"").hexdigest())

    def test_03_raw_byte_lexical_ordering(self) -> None:
        rows = [(b"z.txt", b"z"), (b"a.txt", b"a"), (b"dir/file.txt", b"d")]

        stream = integrity.record_stream(integrity.FileRecord(path, data) for path, data in rows)

        self.assertLess(stream.index(b"a.txt"), stream.index(b"dir/file.txt"))
        self.assertLess(stream.index(b"dir/file.txt"), stream.index(b"z.txt"))

    def test_04_case_sensitivity(self) -> None:
        rows = [(b"A.txt", b"upper"), (b"a.txt", b"lower")]

        scan = integrity.SourceScan(
            integrity.MATERIALIZED_SOURCE_ALGORITHM,
            tuple(integrity.FileRecord(path, data) for path, data in rows),
            0,
            0,
        )

        self.assertEqual(scan.files, 2)
        self.assertEqual(scan.sha256, manual_digest(rows))
        self.assertNotEqual(manual_digest(rows), manual_digest([(b"a.txt", b"upper")]))

    def test_05_exact_nul_and_lf_delimiters(self) -> None:
        record = integrity.FileRecord(b"dir/file.txt", b"content")

        stream = integrity.record_stream([record])

        self.assertEqual(stream, manual_record(b"dir/file.txt", b"content"))
        self.assertEqual(stream.count(b"\0"), 2)
        self.assertTrue(stream.endswith(b"\n"))

    def test_06_no_extra_final_terminator(self) -> None:
        stream = integrity.record_stream([integrity.FileRecord(b"a.txt", b"a")])

        self.assertEqual(stream.count(b"\n"), 1)
        self.assertFalse(stream.endswith(b"\n\n"))

    def test_07_invalid_absolute_path_rejected(self) -> None:
        with self.assertRaisesRegex(integrity.IntegrityError, "unsafe"):
            integrity.record_stream([integrity.FileRecord(b"/absolute.txt", b"")])

    def test_08_invalid_parent_segment_rejected(self) -> None:
        with self.assertRaisesRegex(integrity.IntegrityError, "unsafe"):
            integrity.record_stream([integrity.FileRecord(b"dir/../file.txt", b"")])

    def test_09_tsv_unsafe_path_rejected(self) -> None:
        with self.assertRaisesRegex(integrity.IntegrityError, "TSV-safe"):
            integrity.record_stream([integrity.FileRecord(b"bad\tname.txt", b"")])

    def test_10_non_utf8_path_rejected(self) -> None:
        with self.assertRaisesRegex(integrity.IntegrityError, "UTF-8"):
            integrity.record_stream([integrity.FileRecord(b"bad\xffname.txt", b"")])

    def test_11_parse_ls_tree_classifies_entries(self) -> None:
        raw = (
            b"040000 tree aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\tdir\0"
            b"100644 blob bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\tdir/file.txt\0"
            b"120000 blob cccccccccccccccccccccccccccccccccccccccc\tlink\0"
            b"160000 commit dddddddddddddddddddddddddddddddddddddddd\tsubmodule\0"
        )

        entries = integrity._parse_ls_tree(raw)

        self.assertEqual([entry.object_type for entry in entries], ["tree", "blob", "blob", "commit"])
        self.assertEqual(entries[1].path_bytes, b"dir/file.txt")

    def test_12_parse_ls_tree_rejects_unexpected_output(self) -> None:
        with self.assertRaisesRegex(integrity.IntegrityError, "unexpected"):
            integrity._parse_ls_tree(b"not-a-tree-record\0")

    def test_13_materialized_scan_counts_files_dirs_bytes_and_zeroes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "dir").mkdir()
            (root / "dir" / "a.txt").write_bytes(b"abc")
            (root / "zero.bin").write_bytes(b"")

            scan = integrity.materialized_source_scan(root)

        self.assertEqual(scan.files, 2)
        self.assertEqual(scan.directories, 1)
        self.assertEqual(scan.bytes, 3)
        self.assertEqual(scan.zero_byte_files, 1)

    def test_14_materialized_digest_independent_of_absolute_root(self) -> None:
        with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
            Path(one, "a.txt").write_bytes(b"same")
            Path(two, "a.txt").write_bytes(b"same")

            first = integrity.materialized_source_scan(Path(one))
            second = integrity.materialized_source_scan(Path(two))

        self.assertEqual(first.sha256, second.sha256)

    def test_15_materialized_scan_detects_nested_git_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested").mkdir()
            (root / "nested" / ".git").mkdir()
            (root / "other").mkdir()
            (root / "other" / ".git").write_bytes(b"gitdir: ../actual.git\n")

            scan = integrity.materialized_source_scan(root)

        self.assertEqual(scan.nested_git_directories, 1)
        self.assertEqual(scan.nested_git_files, 1)

    def test_16_materialized_scan_rejects_missing_root(self) -> None:
        with self.assertRaisesRegex(integrity.IntegrityError, "not a directory"):
            integrity.materialized_source_scan(Path("definitely-missing-source-root"))

    def test_17_git_scan_uses_regular_blobs_only(self) -> None:
        raw = (
            b"040000 tree aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\tdir\0"
            b"100644 blob bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\tdir/file.txt\0"
            b"120000 blob cccccccccccccccccccccccccccccccccccccccc\tlink\0"
        )
        blob_output = b"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb blob 4\nfile\n"

        with mock.patch.object(integrity, "resolve_commit", return_value="commit"):
            with mock.patch.object(integrity, "_run_git", side_effect=[raw, blob_output]):
                scan = integrity.git_source_scan(Path("repo"), "commit")

        self.assertEqual(scan.files, 1)
        self.assertEqual(scan.directories, 1)
        self.assertEqual(scan.symlinks, 1)
        self.assertEqual(scan.records[0].path_bytes, b"dir/file.txt")

    def test_18_lfs_pointer_detection(self) -> None:
        data = b"version https://git-lfs.github.com/spec/v1\noid sha256:" + b"a" * 64 + b"\nsize 1\n"

        self.assertTrue(integrity._is_lfs_pointer(data))
        self.assertFalse(integrity._is_lfs_pointer(b"plain file"))

    def test_19_compare_scans_match(self) -> None:
        git_scan = scan(integrity.GIT_SOURCE_ALGORITHM, [(b"a.txt", b"a")], directories=0)
        materialized_scan = scan(integrity.MATERIALIZED_SOURCE_ALGORITHM, [(b"a.txt", b"a")], directories=0)

        result = integrity.compare_scans(git_scan, materialized_scan)

        self.assertEqual(result["status"], "match")
        self.assertTrue(result["sha256_match"])

    def test_20_compare_scans_detects_missing_materialized(self) -> None:
        git_scan = scan(integrity.GIT_SOURCE_ALGORITHM, [(b"a.txt", b"a")], directories=0)
        materialized_scan = scan(integrity.MATERIALIZED_SOURCE_ALGORITHM, [], directories=0)

        result = integrity.compare_scans(git_scan, materialized_scan)

        self.assertEqual(result["status"], "mismatch")
        self.assertEqual(result["missing_materialized_count"], 1)

    def test_21_compare_scans_detects_extra_materialized(self) -> None:
        git_scan = scan(integrity.GIT_SOURCE_ALGORITHM, [], directories=0)
        materialized_scan = scan(integrity.MATERIALIZED_SOURCE_ALGORITHM, [(b"extra.txt", b"x")], directories=0)

        result = integrity.compare_scans(git_scan, materialized_scan)

        self.assertEqual(result["status"], "mismatch")
        self.assertEqual(result["extra_materialized_count"], 1)

    def test_22_compare_scans_detects_content_mismatch(self) -> None:
        git_scan = scan(integrity.GIT_SOURCE_ALGORITHM, [(b"a.txt", b"a")], directories=0)
        materialized_scan = scan(integrity.MATERIALIZED_SOURCE_ALGORITHM, [(b"a.txt", b"b")], directories=0)

        result = integrity.compare_scans(git_scan, materialized_scan)

        self.assertEqual(result["status"], "mismatch")
        self.assertEqual(result["different_file_count"], 1)

    def test_23_compare_scans_detects_directory_mismatch(self) -> None:
        git_scan = scan(integrity.GIT_SOURCE_ALGORITHM, [(b"dir/a.txt", b"a")], directories=1)
        materialized_scan = scan(integrity.MATERIALIZED_SOURCE_ALGORITHM, [(b"dir/a.txt", b"a")], directories=0)

        result = integrity.compare_scans(git_scan, materialized_scan)

        self.assertEqual(result["status"], "mismatch")
        self.assertFalse(result["directories_match"])

    def test_24_manifest_rows_use_exact_schema_and_statuses(self) -> None:
        git_scan = scan(integrity.GIT_SOURCE_ALGORITHM, [(b"a.txt", b"a"), (b"missing.txt", b"m")], directories=0)
        materialized_scan = scan(integrity.MATERIALIZED_SOURCE_ALGORITHM, [(b"a.txt", b"a"), (b"extra.txt", b"x")], directories=0)

        rows = integrity.manifest_rows(
            git_scan,
            materialized_scan,
            repository="https://example.invalid/repo.git",
            tag="v1.0.0",
            commit="abc123",
        )

        self.assertEqual(set(rows[0]), set(integrity.MANIFEST_COLUMNS))
        self.assertEqual([row["verification_status"] for row in rows], ["exact_match", "extra_materialized", "missing_materialized"])

    def test_25_compare_scans_requires_no_lfs_pointers(self) -> None:
        pointer = b"version https://git-lfs.github.com/spec/v1\noid sha256:" + b"a" * 64 + b"\nsize 1\n"
        git_scan = scan(integrity.GIT_SOURCE_ALGORITHM, [(b"pointer.bin", pointer)], directories=0)
        materialized_scan = scan(integrity.MATERIALIZED_SOURCE_ALGORITHM, [(b"pointer.bin", pointer)], directories=0)
        git_scan = integrity.SourceScan(
            git_scan.algorithm,
            git_scan.records,
            git_scan.directories,
            git_scan.zero_byte_files,
            lfs_pointers=1,
        )

        result = integrity.compare_scans(git_scan, materialized_scan)

        self.assertEqual(result["status"], "mismatch")
        self.assertFalse(result["lfs_pointers_clear"])


def scan(algorithm: str, rows: list[tuple[bytes, bytes]], *, directories: int) -> object:
    return integrity.SourceScan(
        algorithm,
        tuple(integrity.FileRecord(path, data, "100644", "oid") for path, data in rows),
        directories,
        sum(1 for _path, data in rows if data == b""),
    )


if __name__ == "__main__":
    unittest.main()
