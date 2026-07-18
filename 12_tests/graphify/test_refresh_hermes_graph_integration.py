from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "10_scripts" / "graphify" / "refresh_hermes_graph.py"

POLICY = """\
*
!README.md
!0_architecture/
!0_architecture/**/
!0_architecture/**/*.md
!3_platform/
!3_platform/_governed_skeleton/
!3_platform/_governed_skeleton/**/
!3_platform/_governed_skeleton/**/*.py
!2_products/
!2_products/hermes-agent/
!2_products/hermes-agent/**
node_modules/
.venv/
dist/
build/
coverage/
4_external/
9_artifacts/
graphify-out/
.env*
credentials/
secrets/
tokens/
package-lock.json
"""


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", "core.longpaths=true", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def write(repo: Path, relative: str, content: str) -> None:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def track(repo: Path, relative: str) -> None:
    blob = run_git(repo, "hash-object", "-w", "--", relative)
    run_git(repo, "update-index", "--add", "--cacheinfo", "100644", blob, relative)


def untrack(repo: Path, relative: str) -> None:
    run_git(repo, "update-index", "--force-remove", "--", relative)


def git_snapshot(repo: Path) -> tuple[str, str]:
    return run_git(repo, "ls-files", "-s"), run_git(repo, "status", "--porcelain=v1")


def source_records(graph: dict, source: str) -> tuple[set[str], set[str]]:
    nodes = {
        node["id"]
        for node in graph.get("nodes", [])
        if node.get("source_file") == source
    }
    related_edges = {
        json.dumps(edge, sort_keys=True)
        for edge in graph.get("links", graph.get("edges", []))
        if edge.get("source") in nodes
        or edge.get("target") in nodes
        or edge.get("source_file") == source
    }
    return nodes, related_edges


class MaintainedPipelineIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="graphify-scale-integration-")
        cls.base = Path(cls.temp.name)
        cls.repo = cls.base / "repo"
        cls.repo.mkdir()
        run_git(cls.repo, "init", "--quiet")
        write(cls.repo, ".graphifyignore", POLICY)
        write(cls.repo, "README.md", "# Fixture\n")
        write(cls.repo, "0_architecture/design.md", "# Fixture Design\n")
        write(
            cls.repo,
            "3_platform/_governed_skeleton/core.py",
            "def governed():\n    return True\n",
        )
        write(
            cls.repo,
            "2_products/hermes-agent/a.py",
            "from b import helper\n\ndef run():\n    return helper()\n",
        )
        write(cls.repo, "2_products/hermes-agent/b.py", "def helper():\n    return 1\n")
        write(cls.repo, "2_products/hermes-agent/fixture.json", "{}")
        write(cls.repo, "2_products/sibling/app.py", "def denied():\n    return 0\n")
        for relative in (
            ".graphifyignore",
            "README.md",
            "0_architecture/design.md",
            "3_platform/_governed_skeleton/core.py",
            "2_products/hermes-agent/a.py",
            "2_products/hermes-agent/b.py",
            "2_products/hermes-agent/fixture.json",
            "2_products/sibling/app.py",
        ):
            track(cls.repo, relative)
        cls.original_snapshot = git_snapshot(cls.repo)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def run_command(
        self, *arguments: str, expected: int = 0, timeout: int = 240
    ) -> subprocess.CompletedProcess[str]:
        before = git_snapshot(self.repo)
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertEqual(
            before, git_snapshot(self.repo), "The maintained pipeline mutated Git state"
        )
        return result

    def full_run(
        self,
        run_id: str,
        batch_size: int,
        cache_mode: str = "cold",
        warm_from: Path | None = None,
    ) -> tuple[Path, Path, dict]:
        output = self.base / f"output-{run_id}"
        evidence = self.base / f"evidence-{run_id}"
        command = [
            "run",
            "--repo-root",
            str(self.repo),
            "--output-dir",
            str(output),
            "--evidence-dir",
            str(evidence),
            "--run-id",
            run_id,
            "--scope",
            "full",
            "--cache-mode",
            cache_mode,
            "--batch-size",
            str(batch_size),
            "--batch-timeout",
            "120",
            "--pipeline-timeout",
            "240",
            "--max-workers",
            "2",
        ]
        if warm_from is not None:
            command.extend(["--warm-from", str(warm_from)])
        self.run_command(*command)
        return (
            output,
            evidence,
            json.loads((evidence / "run-result.json").read_text(encoding="utf-8")),
        )

    def incremental(self, output: Path, name: str) -> dict:
        evidence = self.base / f"evidence-incremental-{name}"
        self.run_command(
            "incremental",
            "--repo-root",
            str(self.repo),
            "--output-dir",
            str(output),
            "--evidence-dir",
            str(evidence),
            "--batch-timeout",
            "120",
            "--max-workers",
            "2",
        )
        return json.loads(
            (evidence / "incremental-result.json").read_text(encoding="utf-8")
        )

    def test_actual_pipeline_pruning_cross_batch_and_restoration(self) -> None:
        multi_output, multi_evidence, multi = self.full_run("multi", batch_size=1)
        single_output, single_evidence, single = self.full_run("single", batch_size=100)
        warm_output, warm_evidence, warm = self.full_run(
            "warm",
            batch_size=1,
            cache_mode="warm",
            warm_from=multi_output,
        )

        for key in (
            "node_id_set_sha256",
            "node_content_sha256",
            "relationship_endpoint_type_set_sha256",
            "relationship_content_sha256",
            "normalized_complete_graph_sha256",
        ):
            self.assertEqual(
                multi["fingerprints"][key], single["fingerprints"][key], key
            )
            self.assertEqual(multi["fingerprints"][key], warm["fingerprints"][key], key)
        self.assertTrue(multi["integrity_passed"])
        self.assertEqual(multi["integrity"]["sibling_product_source_paths"], 0)
        self.assertGreater(warm["cache_input"]["file_count"], 0)
        self.assertGreater(
            warm["cache_metrics"]["priming_hits"],
            multi["cache_metrics"]["priming_hits"],
        )
        finalize_evidence = self.base / "evidence-finalize"
        final_output = self.base / "output-final"
        self.run_command(
            "finalize",
            "--repo-root",
            str(self.repo),
            "--source-output",
            str(single_output),
            "--output-dir",
            str(final_output),
            "--evidence-dir",
            str(finalize_evidence),
            "--timeout",
            "120",
            "--visualization-node-limit",
            "100",
        )
        finalized = json.loads(
            (finalize_evidence / "finalization-result.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            finalized["normalized_graph"]["normalized_complete_graph_sha256"],
            single["fingerprints"]["normalized_complete_graph_sha256"],
        )
        self.assertTrue((final_output / "graph.html").is_file())
        self.assertFalse((final_output / "cache").exists())
        self.assertEqual(finalized["source_graph_sha256"], single["graph_sha256"])

        initial_graph = json.loads(
            (multi_output / "graph.json").read_text(encoding="utf-8")
        )
        initial_fingerprint = multi["fingerprints"]["normalized_complete_graph_sha256"]
        initial_a_nodes, _ = source_records(
            initial_graph, "2_products/hermes-agent/a.py"
        )
        initial_b_nodes, initial_b_edges = source_records(
            initial_graph, "2_products/hermes-agent/b.py"
        )
        self.assertTrue(initial_a_nodes)
        self.assertTrue(initial_b_nodes)
        for name in (
            "provenance.json",
            "GRAPH_REPORT.md",
            "graph.html",
            ".graphify_labels.json",
            ".graphify_labels.json.sig",
        ):
            (multi_output / name).write_text("stale-derived-fixture", encoding="utf-8")

        b_path = self.repo / "2_products/hermes-agent/b.py"
        b_path.unlink()
        untrack(self.repo, "2_products/hermes-agent/b.py")
        deleted = self.incremental(multi_output, "delete")
        after_delete = json.loads(
            (multi_output / "graph.json").read_text(encoding="utf-8")
        )
        deleted_nodes, deleted_edges = source_records(
            after_delete, "2_products/hermes-agent/b.py"
        )
        self.assertEqual(deleted_nodes, set())
        self.assertEqual(deleted_edges, set())
        self.assertIn("2_products/hermes-agent/b.py", deleted["deleted"])
        self.assertFalse((multi_output / "manifest.json").exists())
        for name in (
            "provenance.json",
            "GRAPH_REPORT.md",
            "graph.html",
            ".graphify_labels.json",
            ".graphify_labels.json.sig",
        ):
            self.assertFalse((multi_output / name).exists())
            self.assertIn(name, deleted["derived_outputs_invalidated"])
        remaining_a_nodes, _ = source_records(
            after_delete, "2_products/hermes-agent/a.py"
        )
        self.assertEqual(initial_a_nodes, remaining_a_nodes)

        write(
            self.repo, "2_products/hermes-agent/b.py", "def helper():\n    return 1\n"
        )
        track(self.repo, "2_products/hermes-agent/b.py")
        restored = self.incremental(multi_output, "restore-delete")
        self.assertEqual(
            restored["fingerprints"]["normalized_complete_graph_sha256"],
            initial_fingerprint,
        )

        policy_path = self.repo / ".graphifyignore"
        policy_path.write_text(
            POLICY + "2_products/hermes-agent/b.py\n", encoding="utf-8"
        )
        track(self.repo, ".graphifyignore")
        newly_ignored = self.incremental(multi_output, "new-ignore")
        self.assertIn("2_products/hermes-agent/b.py", newly_ignored["deleted"])
        self.assertEqual(
            source_records(
                json.loads((multi_output / "graph.json").read_text(encoding="utf-8")),
                "2_products/hermes-agent/b.py",
            )[0],
            set(),
        )
        policy_path.write_text(POLICY, encoding="utf-8")
        track(self.repo, ".graphifyignore")
        unignored = self.incremental(multi_output, "remove-ignore")
        self.assertEqual(
            unignored["fingerprints"]["normalized_complete_graph_sha256"],
            initial_fingerprint,
        )

        renamed_path = self.repo / "2_products/hermes-agent/renamed.py"
        b_path.replace(renamed_path)
        untrack(self.repo, "2_products/hermes-agent/b.py")
        track(self.repo, "2_products/hermes-agent/renamed.py")
        renamed = self.incremental(multi_output, "rename")
        self.assertIn("2_products/hermes-agent/b.py", renamed["deleted"])
        self.assertIn("2_products/hermes-agent/renamed.py", renamed["changed"])
        renamed_path.replace(b_path)
        untrack(self.repo, "2_products/hermes-agent/renamed.py")
        track(self.repo, "2_products/hermes-agent/b.py")
        rename_restored = self.incremental(multi_output, "restore-rename")
        self.assertEqual(
            rename_restored["fingerprints"]["normalized_complete_graph_sha256"],
            initial_fingerprint,
        )

        b_path.write_text(
            "def helper():\n    return 2\n\ndef added():\n    return helper()\n",
            encoding="utf-8",
        )
        track(self.repo, "2_products/hermes-agent/b.py")
        changed = self.incremental(multi_output, "change")
        self.assertIn("2_products/hermes-agent/b.py", changed["changed"])
        self.assertNotEqual(
            changed["fingerprints"]["normalized_complete_graph_sha256"],
            initial_fingerprint,
        )
        b_path.write_text("def helper():\n    return 1\n", encoding="utf-8")
        track(self.repo, "2_products/hermes-agent/b.py")
        change_restored = self.incremental(multi_output, "restore-change")
        self.assertEqual(
            change_restored["fingerprints"]["normalized_complete_graph_sha256"],
            initial_fingerprint,
        )

        fixture_path = self.repo / "2_products/hermes-agent/fixture.json"
        fixture_path.unlink()
        untrack(self.repo, "2_products/hermes-agent/fixture.json")
        no_node_delete = self.incremental(multi_output, "delete-zero-node")
        self.assertIn("2_products/hermes-agent/fixture.json", no_node_delete["deleted"])
        self.assertEqual(
            no_node_delete["fingerprints"]["normalized_complete_graph_sha256"],
            initial_fingerprint,
        )
        write(self.repo, "2_products/hermes-agent/fixture.json", "{}")
        track(self.repo, "2_products/hermes-agent/fixture.json")
        no_node_restore = self.incremental(multi_output, "restore-zero-node")
        self.assertEqual(
            no_node_restore["fingerprints"]["normalized_complete_graph_sha256"],
            initial_fingerprint,
        )

        self.assertEqual(
            source_records(initial_graph, "2_products/hermes-agent/b.py")[1],
            initial_b_edges,
        )
        self.assertEqual(git_snapshot(self.repo), self.original_snapshot)

        shutil.rmtree(single_output)
        shutil.rmtree(single_evidence)
        shutil.rmtree(finalize_evidence)
        shutil.rmtree(warm_output)
        shutil.rmtree(warm_evidence)
        shutil.rmtree(multi_evidence)


class ActualHermesFixtureIntegrationTests(unittest.TestCase):
    def test_real_hermes_sources_prune_and_restore_exactly(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="graphify-scale-hermes-fixture-"
        ) as directory:
            base = Path(directory)
            repo = base / "repo"
            repo.mkdir()
            run_git(repo, "init", "--quiet")
            write(repo, ".graphifyignore", POLICY)
            representatives = (
                "hermes_cli/web_server.py",
                "gateway/platforms/api_server.py",
                "plugins/kanban/dashboard/plugin_api.py",
            )
            original_bytes: dict[str, bytes] = {}
            for relative in representatives:
                source = ROOT / "2_products" / "hermes-agent" / relative
                target_relative = f"2_products/hermes-agent/{relative}"
                target = repo / target_relative
                target.parent.mkdir(parents=True, exist_ok=True)
                payload = source.read_bytes()
                target.write_bytes(payload)
                original_bytes[target_relative] = payload
            for relative in (".graphifyignore", *original_bytes):
                track(repo, relative)

            output = base / "output"
            evidence = base / "evidence-initial"

            def invoke(*arguments: str) -> None:
                before = git_snapshot(repo)
                result = subprocess.run(
                    [sys.executable, "-B", str(SCRIPT), *arguments],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=240,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )
                self.assertEqual(before, git_snapshot(repo))

            invoke(
                "run",
                "--repo-root",
                str(repo),
                "--output-dir",
                str(output),
                "--evidence-dir",
                str(evidence),
                "--run-id",
                "real_hermes_fixture",
                "--scope",
                "full",
                "--cache-mode",
                "cold",
                "--batch-size",
                "1",
                "--batch-timeout",
                "120",
                "--pipeline-timeout",
                "240",
                "--max-workers",
                "2",
            )
            initial = json.loads(
                (evidence / "run-result.json").read_text(encoding="utf-8")
            )
            initial_hash = initial["fingerprints"]["normalized_complete_graph_sha256"]
            graph = json.loads((output / "graph.json").read_text(encoding="utf-8"))
            web_nodes, _ = source_records(
                graph, "2_products/hermes-agent/hermes_cli/web_server.py"
            )
            plugin_nodes, _ = source_records(
                graph,
                "2_products/hermes-agent/plugins/kanban/dashboard/plugin_api.py",
            )
            self.assertTrue(web_nodes)
            self.assertTrue(plugin_nodes)

            deleted_relative = "2_products/hermes-agent/gateway/platforms/api_server.py"
            (repo / deleted_relative).unlink()
            untrack(repo, deleted_relative)
            delete_evidence = base / "evidence-delete"
            invoke(
                "incremental",
                "--repo-root",
                str(repo),
                "--output-dir",
                str(output),
                "--evidence-dir",
                str(delete_evidence),
                "--batch-timeout",
                "120",
                "--max-workers",
                "2",
            )
            after_delete = json.loads(
                (output / "graph.json").read_text(encoding="utf-8")
            )
            self.assertEqual(source_records(after_delete, deleted_relative)[0], set())
            self.assertEqual(
                source_records(
                    after_delete, "2_products/hermes-agent/hermes_cli/web_server.py"
                )[0],
                web_nodes,
            )
            self.assertEqual(
                source_records(
                    after_delete,
                    "2_products/hermes-agent/plugins/kanban/dashboard/plugin_api.py",
                )[0],
                plugin_nodes,
            )

            restored = repo / deleted_relative
            restored.parent.mkdir(parents=True, exist_ok=True)
            restored.write_bytes(original_bytes[deleted_relative])
            track(repo, deleted_relative)
            restore_evidence = base / "evidence-restore"
            invoke(
                "incremental",
                "--repo-root",
                str(repo),
                "--output-dir",
                str(output),
                "--evidence-dir",
                str(restore_evidence),
                "--batch-timeout",
                "120",
                "--max-workers",
                "2",
            )
            restored_result = json.loads(
                (restore_evidence / "incremental-result.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                restored_result["fingerprints"]["normalized_complete_graph_sha256"],
                initial_hash,
            )


if __name__ == "__main__":
    unittest.main()
