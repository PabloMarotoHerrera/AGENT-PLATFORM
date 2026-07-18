from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "10_scripts" / "graphify" / "refresh_hermes_graph.py"
SPEC = importlib.util.spec_from_file_location("refresh_hermes_graph", SCRIPT_PATH)
assert SPEC and SPEC.loader
refresh = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(refresh)


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


def write(repo: Path, relative: str, content: str) -> Path:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def track(repo: Path, relative: str) -> None:
    blob = run_git(repo, "hash-object", "-w", "--", relative)
    run_git(repo, "update-index", "--add", "--cacheinfo", "100644", blob, relative)


class RepositoryFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="graphify-scale-unit-")
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        run_git(self.repo, "init", "--quiet")
        write(self.repo, ".graphifyignore", POLICY)
        write(self.repo, "README.md", "# Root\n")
        write(self.repo, "0_architecture/design.md", "# Design\n")
        write(
            self.repo,
            "3_platform/_governed_skeleton/core.py",
            "def governed():\n    return True\n",
        )
        write(self.repo, "2_products/hermes-agent/app.py", "def run():\n    return 1\n")
        write(
            self.repo,
            "2_products/other-product/app.py",
            "def denied():\n    return 0\n",
        )
        write(self.repo, "4_external/vendor.py", "def external():\n    return 0\n")
        write(self.repo, "9_artifacts/result.py", "def generated():\n    return 0\n")
        write(
            self.repo,
            "2_products/hermes-agent/node_modules/pkg/index.js",
            "export default 1\n",
        )
        write(
            self.repo,
            "2_products/hermes-agent/credentials/secret.py",
            "TOKEN = 'not-read'\n",
        )
        write(self.repo, "2_products/hermes-agent/id_rsa", "fixture-only\n")
        write(
            self.repo, "graphify-out/inside.py", "def self_ingested():\n    return 0\n"
        )
        for relative in (
            ".graphifyignore",
            "README.md",
            "0_architecture/design.md",
            "3_platform/_governed_skeleton/core.py",
            "2_products/hermes-agent/app.py",
            "2_products/other-product/app.py",
            "4_external/vendor.py",
            "9_artifacts/result.py",
            "2_products/hermes-agent/node_modules/pkg/index.js",
            "2_products/hermes-agent/credentials/secret.py",
            "2_products/hermes-agent/id_rsa",
            "graphify-out/inside.py",
        ):
            track(self.repo, relative)

    def tearDown(self) -> None:
        self.temp.cleanup()


class InventoryTests(RepositoryFixture):
    def test_installed_ignore_parser_opens_only_hermes_product(self) -> None:
        inventory = refresh.build_inventory(self.repo, "full", batch_size=2)
        accepted = {item["path"] for item in inventory["accepted"]}
        self.assertEqual(
            accepted,
            {
                "README.md",
                "0_architecture/design.md",
                "3_platform/_governed_skeleton/core.py",
                "2_products/hermes-agent/app.py",
            },
        )
        ignored = {item["path"] for item in inventory["ignored"]}
        self.assertIn("2_products/other-product/app.py", ignored)
        self.assertIn("4_external/vendor.py", ignored)
        self.assertIn("9_artifacts/result.py", ignored)
        self.assertIn("2_products/hermes-agent/node_modules/pkg/index.js", ignored)
        self.assertIn("2_products/hermes-agent/credentials/secret.py", ignored)
        self.assertIn("graphify-out/inside.py", ignored)
        self.assertEqual(
            {item["path"] for item in inventory["sensitive"]},
            {"2_products/hermes-agent/id_rsa"},
        )

    def test_baseline_scope_excludes_all_products(self) -> None:
        inventory = refresh.build_inventory(self.repo, "baseline", batch_size=50)
        accepted = {item["path"] for item in inventory["accepted"]}
        self.assertEqual(
            accepted,
            {
                "README.md",
                "0_architecture/design.md",
                "3_platform/_governed_skeleton/core.py",
            },
        )

    def test_manifest_and_batch_assignment_are_deterministic(self) -> None:
        first = refresh.build_inventory(self.repo, "full", batch_size=2)
        second = refresh.build_inventory(self.repo, "full", batch_size=2)
        self.assertEqual(first["accepted"], second["accepted"])
        self.assertEqual(first["batches"], second["batches"])
        self.assertEqual(
            first["accepted_manifest_sha256"], second["accepted_manifest_sha256"]
        )
        self.assertEqual(
            first["batch_definition_sha256"], second["batch_definition_sha256"]
        )
        self.assertEqual(
            [item["path"] for item in first["accepted"]],
            sorted(item["path"] for item in first["accepted"]),
        )

    def test_cache_modes_are_explicit_and_credential_environment_is_removed(
        self,
    ) -> None:
        with mock.patch.dict(
            refresh.os.environ,
            {
                "EXAMPLE_API_KEY": "secret",
                "EXAMPLE_TOKEN": "secret",
                "SAFE_VALUE": "kept",
            },
            clear=False,
        ):
            env = refresh.sanitized_environment(self.base / "output", 3)
        self.assertNotIn("EXAMPLE_API_KEY", env)
        self.assertNotIn("EXAMPLE_TOKEN", env)
        self.assertEqual(env["SAFE_VALUE"], "kept")
        self.assertEqual(env["PYTHONHASHSEED"], "0")
        self.assertEqual(env["GRAPHIFY_MAX_WORKERS"], "3")

    def test_tracked_symlink_cannot_escape_repository(self) -> None:
        outside = self.base / "outside.py"
        outside.write_text("SECRET = 'fixture'\n", encoding="utf-8")
        link = self.repo / "2_products/hermes-agent/leak.py"
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"Windows symlink creation unavailable: {error}")
        track(self.repo, "2_products/hermes-agent/leak.py")
        inventory = refresh.build_inventory(self.repo, "full", batch_size=50)
        self.assertNotIn(
            "2_products/hermes-agent/leak.py",
            {item["path"] for item in inventory["accepted"]},
        )
        reasons = {item["path"]: item["reason"] for item in inventory["ignored"]}
        self.assertEqual(
            reasons["2_products/hermes-agent/leak.py"],
            "tracked_symlink_or_root_escape_denied",
        )

    def test_zero_node_json_must_remain_zero_under_fresh_extraction(self) -> None:
        write(self.repo, "2_products/hermes-agent/fixture.json", "{}")
        evidence = refresh.validate_zero_node_sources(
            self.repo, ["2_products/hermes-agent/fixture.json"]
        )
        self.assertEqual(evidence[0]["fresh_nodes"], 0)
        write(self.repo, "2_products/hermes-agent/package.json", "{}")
        with self.assertRaises(refresh.PipelineError):
            refresh.validate_zero_node_sources(
                self.repo, ["2_products/hermes-agent/package.json"]
            )

    def test_official_manifest_requires_exact_accepted_source_coverage(self) -> None:
        inventory = refresh.build_inventory(self.repo, "full", batch_size=50)
        output = self.base / "candidate"
        output.mkdir()
        expected = {item["path"]: {} for item in inventory["accepted"]}
        (output / "manifest.json").write_text(json.dumps(expected), encoding="utf-8")
        result = refresh.validate_official_manifest(output, inventory)
        self.assertEqual(result["source_count"], len(expected))
        (output / "manifest.json").write_text("{}", encoding="utf-8")
        with self.assertRaises(refresh.PipelineError):
            refresh.validate_official_manifest(output, inventory)


class ActualPolicyTests(unittest.TestCase):
    def test_repository_candidate_policy_with_installed_parser(self) -> None:
        from graphify.detect import _is_ignored, _load_graphifyignore

        patterns = _load_graphifyignore(ROOT)
        cache: dict[Path, bool] = {}
        included = (
            "README.md",
            "0_architecture/governance/example.md",
            "3_platform/_governed_skeleton/example.py",
            "2_products/hermes-agent/hermes_cli/web_server.py",
        )
        excluded = (
            "2_products/backend-energyplus/app.py",
            "2_products/cli/app.py",
            "2_products/desktop/app.py",
            "2_products/experimental/app.py",
            "2_products/omniverse-app/app.py",
            "2_products/web-platform/app.py",
            "4_external/sources/hermes-agent/app.py",
            "9_artifacts/result.py",
            "graphify-out/graph.json",
            ".opencode/plugin.py",
            ".git/config",
            "2_products/hermes-agent/node_modules/pkg/index.js",
            "2_products/hermes-agent/.venv/lib.py",
            "2_products/hermes-agent/.pytest_cache/state.py",
            "2_products/hermes-agent/dist/bundle.js",
            "2_products/hermes-agent/build/output.py",
            "2_products/hermes-agent/coverage/index.py",
            "2_products/hermes-agent/logs/runtime.py",
            "2_products/hermes-agent/state.sqlite",
            "2_products/hermes-agent/credentials/key.py",
            "2_products/hermes-agent/secrets/key.py",
            "2_products/hermes-agent/.env.production",
            "2_products/hermes-agent/provider_config/local.py",
            "2_products/hermes-agent/package-lock.json",
            "2_products/hermes-agent/image.png",
        )
        for relative in included:
            self.assertFalse(
                _is_ignored(ROOT / relative, ROOT, patterns, _cache=cache), relative
            )
        for relative in excluded:
            self.assertTrue(
                _is_ignored(ROOT / relative, ROOT, patterns, _cache=cache), relative
            )

    def test_candidate_and_evidence_paths_must_be_disjoint(self) -> None:
        with tempfile.TemporaryDirectory(prefix="graphify-paths-") as directory:
            parent = Path(directory) / "candidate"
            child = parent / "evidence"
            with self.assertRaises(refresh.PipelineError):
                refresh.ensure_disjoint_paths(parent, child)


class NormalizationTests(unittest.TestCase):
    def graph(self, relation: str = "calls", community: int = 1) -> dict:
        return {
            "nodes": [
                {
                    "id": "a",
                    "label": "A",
                    "file_type": "code",
                    "source_file": "2_products/hermes-agent/a.py",
                    "type": "function",
                    "community": community,
                    "x": community * 10,
                },
                {
                    "id": "b",
                    "label": "B",
                    "file_type": "code",
                    "source_file": "2_products/hermes-agent/b.py",
                    "type": "function",
                    "community": community,
                },
            ],
            "links": [
                {
                    "source": "a",
                    "target": "b",
                    "relation": relation,
                    "confidence": "EXTRACTED",
                    "source_file": "2_products/hermes-agent/a.py",
                }
            ],
        }

    def test_derived_fields_do_not_change_normalized_hashes(self) -> None:
        first = refresh.graph_fingerprints(self.graph(community=1))
        second = refresh.graph_fingerprints(self.graph(community=99))
        self.assertEqual(first, second)

    def test_relationship_semantics_change_normalized_hashes(self) -> None:
        first = refresh.graph_fingerprints(self.graph(relation="calls"))
        second = refresh.graph_fingerprints(self.graph(relation="imports"))
        self.assertEqual(first["node_content_sha256"], second["node_content_sha256"])
        self.assertNotEqual(
            first["relationship_endpoint_type_set_sha256"],
            second["relationship_endpoint_type_set_sha256"],
        )
        self.assertNotEqual(
            first["normalized_complete_graph_sha256"],
            second["normalized_complete_graph_sha256"],
        )

    def test_graph_direction_semantics_change_normalized_hash(self) -> None:
        undirected = self.graph()
        directed = self.graph()
        directed["directed"] = True
        self.assertNotEqual(
            refresh.graph_fingerprints(undirected)["normalized_complete_graph_sha256"],
            refresh.graph_fingerprints(directed)["normalized_complete_graph_sha256"],
        )

    def test_record_level_difference_reports_relationship_change(self) -> None:
        with tempfile.TemporaryDirectory(prefix="graphify-normalize-") as directory:
            left = Path(directory) / "left.json"
            right = Path(directory) / "right.json"
            left.write_text(json.dumps(self.graph("calls")), encoding="utf-8")
            right.write_text(json.dumps(self.graph("imports")), encoding="utf-8")
            result = refresh.record_differences(left, right)
        self.assertEqual(result["nodes"]["left_only_count"], 0)
        self.assertEqual(result["relationships"]["left_only_count"], 1)
        self.assertEqual(result["relationships"]["right_only_count"], 1)

    def test_unsupported_custom_schema_is_rejected_by_official_validator(self) -> None:
        from graphify.validate import validate_extraction

        invalid = self.graph()
        del invalid["links"][0]["relation"]
        errors = validate_extraction(invalid)
        self.assertTrue(
            any("missing required field 'relation'" in error for error in errors)
        )

    def test_graph_source_must_be_bound_to_authorized_manifest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="graphify-manifest-bind-") as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            graph_path = Path(directory) / "graph.json"
            graph_path.write_text(json.dumps(self.graph()), encoding="utf-8")
            inventory = {
                "scope": "full",
                "accepted": [],
                "direct_product_children": ["hermes-agent"],
            }
            result = refresh.analyze_graph(repo, graph_path, inventory)
        self.assertGreater(result["integrity"]["unmanifested_source_paths"], 0)
        self.assertFalse(result["integrity_passed"])

    def test_rooted_traversal_and_hyperedge_sources_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="graphify-source-path-") as directory:
            repo = Path(directory) / "repo"
            source = repo / "2_products/hermes-agent/a.py"
            source.parent.mkdir(parents=True)
            source.write_text("def a():\n    pass\n", encoding="utf-8")
            inventory = {
                "scope": "full",
                "accepted": [{"path": "2_products/hermes-agent/a.py"}],
                "direct_product_children": ["hermes-agent"],
            }
            for malicious in (
                "../2_products/hermes-agent/a.py",
                "/2_products/hermes-agent/a.py",
                "\\2_products\\hermes-agent\\a.py",
            ):
                graph = self.graph()
                graph["nodes"][0]["source_file"] = malicious
                graph_path = Path(directory) / "graph.json"
                graph_path.write_text(json.dumps(graph), encoding="utf-8")
                result = refresh.analyze_graph(repo, graph_path, inventory)
                self.assertGreater(result["integrity"]["noncanonical_source_paths"], 0)
                self.assertFalse(result["integrity_passed"])
            graph = self.graph()
            graph["hyperedges"] = [
                {
                    "id": "h",
                    "members": ["a"],
                    "source_file": "../2_products/hermes-agent/a.py",
                }
            ]
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            result = refresh.analyze_graph(repo, graph_path, inventory)
            self.assertGreater(result["integrity"]["noncanonical_source_paths"], 0)

    def test_empty_baseline_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="graphify-empty-baseline-"
        ) as directory:
            baseline = Path(directory) / "baseline.json"
            candidate = Path(directory) / "candidate.json"
            baseline.write_text('{"nodes": [], "links": []}', encoding="utf-8")
            candidate.write_text(json.dumps(self.graph()), encoding="utf-8")
            with self.assertRaises(refresh.PipelineError):
                refresh.baseline_subset_result(baseline, candidate)

    def test_aggregated_html_counts_unique_community_pairs(self) -> None:
        from graphify.cluster import community_member_sigs

        with tempfile.TemporaryDirectory(prefix="graphify-derived-") as directory:
            output = Path(directory)
            graph = {
                "nodes": [
                    {
                        "id": node_id,
                        "community": community,
                        "community_name": f"Community {community}",
                    }
                    for node_id, community in (("a", 0), ("b", 1), ("c", 2))
                ],
                "links": [
                    {"source": "a", "target": "b"},
                    {"source": "a", "target": "b", "relation": "second"},
                    {"source": "b", "target": "c"},
                ],
            }
            labels = {str(index): f"Community {index}" for index in range(3)}
            (output / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
            (output / ".graphify_labels.json").write_text(
                json.dumps(labels), encoding="utf-8"
            )
            (output / ".graphify_labels.json.sig").write_text(
                json.dumps(
                    {
                        str(key): value
                        for key, value in community_member_sigs(
                            {0: ["a"], 1: ["b"], 2: ["c"]}
                        ).items()
                    }
                ),
                encoding="utf-8",
            )
            (output / "GRAPH_REPORT.md").write_text(
                "- 3 nodes · 3 edges · 3 communities\n", encoding="utf-8"
            )
            (output / "graph.html").write_text(
                "<title>graphify - fixture</title>"
                "<div>3 nodes &middot; 2 edges &middot; 3 communities</div>",
                encoding="utf-8",
            )
            result = refresh.validate_derived_outputs(output)
            self.assertEqual(result["cross_community_relationships"], 3)
            self.assertEqual(result["aggregated_community_edges"], 2)


def create_promotable_candidate(repo: Path, candidate: Path) -> dict[str, object]:
    from graphify.cluster import community_member_sigs

    run_git(repo, "init", "--quiet")
    source_path = repo / "2_products/hermes-agent/a.py"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("def a():\n    return 1\n", encoding="utf-8")
    (repo / ".graphifyignore").write_text(
        "*\n!README.md\n!2_products/\n!2_products/hermes-agent/\n"
        "!2_products/hermes-agent/**\n",
        encoding="utf-8",
    )
    (repo / "README.md").write_text("# Fixture\n", encoding="utf-8")
    track(repo, ".graphifyignore")
    track(repo, "README.md")
    track(repo, "2_products/hermes-agent/a.py")
    candidate.mkdir()
    (candidate / "cache").mkdir()
    graph = {
        "nodes": [
            {
                "id": "a",
                "label": "a",
                "file_type": "code",
                "source_file": "2_products/hermes-agent/a.py",
                "community": 0,
                "community_name": "a",
            },
            {
                "id": "readme",
                "label": "README",
                "file_type": "document",
                "source_file": "README.md",
                "community": 0,
                "community_name": "a",
            },
        ],
        "links": [],
        "directed": False,
        "multigraph": False,
    }
    (candidate / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
    for name, content in (
        (".graphify_labels.json", json.dumps({"0": "a"})),
        (
            ".graphify_labels.json.sig",
            json.dumps(
                {
                    str(key): value
                    for key, value in community_member_sigs(
                        {0: ["a", "readme"]}
                    ).items()
                }
            ),
        ),
        ("GRAPH_REPORT.md", "# Fixture\n- 2 nodes · 0 edges · 1 communities\n"),
        (
            "graph.html",
            "<html><head><title>graphify - fixture</title></head>"
            '<body><div id="stats">2 nodes &middot; 0 edges &middot; 1 communities</div></body></html>',
        ),
    ):
        (candidate / name).write_text(content, encoding="utf-8")
    scale_manifest = refresh.build_inventory(repo, "full", refresh.DEFAULT_BATCH_SIZE)
    (candidate / "scale-manifest.json").write_text(
        json.dumps(scale_manifest), encoding="utf-8"
    )
    full_manifest = {item["path"]: {} for item in scale_manifest["accepted"]}
    (candidate / "manifest.json").write_text(
        json.dumps(full_manifest), encoding="utf-8"
    )

    process = {"exit_code": 0, "timed_out": False, "duration_seconds": 0.1}
    run_paths = []
    run_outputs: dict[str, Path] = {}
    for run_id in ("cold_run_1", "cold_run_2", "warm_run_1", "warm_run_2"):
        output = candidate.parent / run_id
        output.mkdir()
        (output / "cache").mkdir()
        (output / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
        (output / "scale-manifest.json").write_text(
            json.dumps(scale_manifest), encoding="utf-8"
        )
        (output / "manifest.json").write_text(
            json.dumps(full_manifest), encoding="utf-8"
        )
        run_outputs[run_id] = output
        mode = "cold" if run_id.startswith("cold") else "warm"
        cold_id = "cold_run_1" if run_id.endswith("1") else "cold_run_2"
        analysis = refresh.analyze_graph(repo, output / "graph.json", scale_manifest)
        result = {
            "run_id": run_id,
            "scope": "full",
            "git_commit": scale_manifest["git_commit"],
            "graphify_version": refresh.SUPPORTED_GRAPHIFY_VERSION,
            "pipeline_version": refresh.PIPELINE_VERSION,
            "pipeline_script_sha256": refresh.sha256_file(SCRIPT_PATH),
            "graphifyignore_sha256": refresh.sha256_file(repo / ".graphifyignore"),
            "cache_mode": mode,
            "warm_cache_source": str(run_outputs[cold_id] / "cache")
            if mode == "warm"
            else None,
            "cache_input": refresh.directory_inventory(output / "cache"),
            "cache_output": refresh.directory_inventory(output / "cache"),
            "cache_metrics": {
                "priming_hits": 1 if mode == "warm" else 0,
                "priming_misses": 1,
                "resolve_hits": 1,
                "resolve_misses": 1,
            },
            "inventory_hashes": {
                key: scale_manifest[key]
                for key in (
                    "accepted_manifest_sha256",
                    "ignored_manifest_sha256",
                    "sensitive_manifest_sha256",
                    "unsupported_manifest_sha256",
                    "batch_definition_sha256",
                )
            },
            "counts": scale_manifest["counts"],
            "fingerprints": analysis["fingerprints"],
            "graph_path": str(output / "graph.json"),
            "graph_sha256": refresh.sha256_file(output / "graph.json"),
            "integrity_passed": True,
            "integrity": analysis["integrity"],
            "parser_failures": [],
            "zero_node_files": [],
            "zero_node_evidence": [],
            "official_manifest": refresh.validate_official_manifest(
                output, scale_manifest
            ),
            "source_coverage": analysis["source_coverage"],
            "batch_processes": [process],
            "resolve_process": process,
            "build_process": process,
            "validate_process": process,
            "duration_seconds": 1.0,
            "cpu_seconds": 0.5,
            "peak_memory_bytes": 1024,
            "files_per_second": 1.0,
            "largest_batch_duration_seconds": 0.5,
            "largest_operation_duration_seconds": 0.5,
        }
        result_path = candidate.parent / f"{run_id}.json"
        result_path.write_text(json.dumps(result), encoding="utf-8")
        run_paths.append(str(result_path))

    comparison = candidate.parent / "comparison.json"
    refresh.compare_runs(
        type("Args", (), {"run_results": run_paths, "output": str(comparison)})()
    )
    baseline_output = candidate.parent / "baseline-output"
    baseline_output.mkdir()
    baseline_graph = {
        "nodes": [graph["nodes"][1] | {"community": 0, "community_name": "a"}],
        "links": [],
        "directed": False,
        "multigraph": False,
    }
    (baseline_output / "graph.json").write_text(
        json.dumps(baseline_graph), encoding="utf-8"
    )
    baseline_manifest = refresh.build_inventory(
        repo, "baseline", refresh.DEFAULT_BATCH_SIZE
    )
    (baseline_output / "scale-manifest.json").write_text(
        json.dumps(baseline_manifest), encoding="utf-8"
    )
    (baseline_output / "manifest.json").write_text(
        json.dumps({item["path"]: {} for item in baseline_manifest["accepted"]}),
        encoding="utf-8",
    )
    baseline_analysis = refresh.analyze_graph(
        repo, baseline_output / "graph.json", baseline_manifest
    )
    baseline_result = {
        "run_id": "baseline_run",
        "scope": "baseline",
        "cache_mode": "cold",
        "git_commit": baseline_manifest["git_commit"],
        "graphify_version": refresh.SUPPORTED_GRAPHIFY_VERSION,
        "pipeline_version": refresh.PIPELINE_VERSION,
        "pipeline_script_sha256": refresh.sha256_file(SCRIPT_PATH),
        "graphifyignore_sha256": refresh.sha256_file(repo / ".graphifyignore"),
        "graph_path": str(baseline_output / "graph.json"),
        "graph_sha256": refresh.sha256_file(baseline_output / "graph.json"),
        "fingerprints": baseline_analysis["fingerprints"],
        "integrity_passed": True,
        "integrity": baseline_analysis["integrity"],
        "parser_failures": [],
        "zero_node_files": [],
        "zero_node_evidence": [],
        "source_coverage": baseline_analysis["source_coverage"],
        "official_manifest": refresh.validate_official_manifest(
            baseline_output, baseline_manifest
        ),
    }
    baseline_result_path = candidate.parent / "baseline-run-result.json"
    baseline_result_path.write_text(json.dumps(baseline_result), encoding="utf-8")
    baseline_comparison = candidate.parent / "baseline-comparison.json"
    refresh.compare_baseline(
        type(
            "Args",
            (),
            {
                "repo_root": str(repo),
                "baseline_graph": str(baseline_output / "graph.json"),
                "candidate_graph": str(run_outputs["cold_run_1"] / "graph.json"),
                "baseline_run_result": str(baseline_result_path),
                "candidate_run_result": run_paths[0],
                "output": str(baseline_comparison),
            },
        )()
    )
    finalization = candidate.parent / "finalization.json"
    finalization.write_text(
        json.dumps(
            {
                "pipeline_script_sha256": refresh.sha256_file(SCRIPT_PATH),
                "graphify_version": refresh.SUPPORTED_GRAPHIFY_VERSION,
                "source_graph_sha256": refresh.sha256_file(
                    run_outputs["cold_run_1"] / "graph.json"
                ),
                "initial_graph_sha256": refresh.sha256_file(
                    run_outputs["cold_run_1"] / "graph.json"
                ),
                "final_graph_sha256": refresh.sha256_file(candidate / "graph.json"),
                "normalized_graph": refresh.graph_fingerprints(graph),
                "derived_validation": refresh.validate_derived_outputs(candidate),
                "cluster_execution": process,
                "html_execution": process,
                "visualization_node_limit": 100,
                "output_hashes": {
                    path.name: {
                        "sha256": refresh.sha256_file(path),
                        "bytes": path.stat().st_size,
                    }
                    for path in candidate.iterdir()
                    if path.is_file()
                },
            }
        ),
        encoding="utf-8",
    )
    refresh.generate_provenance(
        type(
            "Args",
            (),
            {
                "repo_root": str(repo),
                "output_dir": str(candidate),
                "run_results": run_paths,
                "comparison": str(comparison),
                "baseline_comparison": str(baseline_comparison),
                "baseline_graph": str(baseline_output / "graph.json"),
                "baseline_run_result": str(baseline_result_path),
                "finalization_result": str(finalization),
            },
        )()
    )
    return {
        "run_results": run_paths,
        "comparison": str(comparison),
        "baseline_comparison": str(baseline_comparison),
        "baseline_graph": str(baseline_output / "graph.json"),
        "baseline_run_result": str(baseline_result_path),
        "finalization_result": str(finalization),
    }


class PromotionTests(unittest.TestCase):
    def promotion_fixture(
        self, base: Path
    ) -> tuple[Path, Path, Path, Path, dict[str, object]]:
        repo = base / "repo"
        current = repo / "graphify-out"
        candidate = base / "candidate"
        backup = base / "backup"
        current.mkdir(parents=True)
        (current / "graph.json").write_text(
            '{"nodes": [{"id": "old"}]}', encoding="utf-8"
        )
        evidence = create_promotable_candidate(repo, candidate)
        return repo, current, candidate, backup, evidence

    def test_atomic_promotion_verifies_then_retains_backup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="graphify-promote-") as directory:
            repo, current, candidate, backup, evidence = self.promotion_fixture(
                Path(directory)
            )
            args = type(
                "Args",
                (),
                {
                    "repo_root": str(repo),
                    "candidate_output": str(candidate),
                    "backup_output": str(backup),
                    **evidence,
                },
            )()
            refresh.promote_candidate(args)
            self.assertIn(
                '"id": "a"', (current / "graph.json").read_text(encoding="utf-8")
            )
            self.assertTrue(backup.exists())
            self.assertIn("old", (backup / "graph.json").read_text(encoding="utf-8"))
            self.assertFalse((current / "cache").exists())

    def test_failed_promotion_restores_previous_output(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="graphify-promote-rollback-"
        ) as directory:
            repo, current, candidate, backup, evidence = self.promotion_fixture(
                Path(directory)
            )
            args = type(
                "Args",
                (),
                {
                    "repo_root": str(repo),
                    "candidate_output": str(candidate),
                    "backup_output": str(backup),
                    **evidence,
                },
            )()
            real_replace = refresh.os.replace
            calls = 0

            def fail_second_replace(source: Path, target: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("simulated promotion failure")
                real_replace(source, target)

            with mock.patch.object(
                refresh.os, "replace", side_effect=fail_second_replace
            ):
                with self.assertRaises(OSError):
                    refresh.promote_candidate(args)
            self.assertIn("old", (current / "graph.json").read_text(encoding="utf-8"))
            self.assertFalse(backup.exists())

    def test_unattested_candidate_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="graphify-promote-reject-"
        ) as directory:
            base = Path(directory)
            repo = base / "repo"
            (repo / "graphify-out").mkdir(parents=True)
            candidate = base / "candidate"
            candidate.mkdir()
            (candidate / "graph.json").write_text("{}", encoding="utf-8")
            args = type(
                "Args",
                (),
                {
                    "repo_root": str(repo),
                    "candidate_output": str(candidate),
                    "backup_output": str(base / "backup"),
                },
            )()
            with self.assertRaises(refresh.PipelineError):
                refresh.promote_candidate(args)

    def test_html_title_sanitization_removes_absolute_path(self) -> None:
        with tempfile.TemporaryDirectory(prefix="graphify-html-") as directory:
            html = Path(directory) / "graph.html"
            html.write_text(
                "<html><head><title>graphify - C:\\private\\candidate</title></head></html>",
                encoding="utf-8",
            )
            args = type(
                "Args",
                (),
                {"html": str(html), "title": "graphify - AGENT PLATFORM"},
            )()
            refresh.sanitize_html_title(args)
            text = html.read_text(encoding="utf-8")
            self.assertIn("<title>graphify - AGENT PLATFORM</title>", text)
            self.assertNotIn("C:\\private", text)


class ProvenanceTests(unittest.TestCase):
    def test_provenance_recomputes_four_distinct_runs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="graphify-provenance-") as directory:
            base = Path(directory)
            repo = base / "repo"
            output = base / "candidate"
            repo.mkdir()
            evidence = create_promotable_candidate(repo, output)
            provenance = json.loads(
                (output / "provenance.json").read_text(encoding="utf-8")
            )
            self.assertEqual(provenance["ticket"], "GRAPHIFY-SCALE-01")
            self.assertEqual(
                set(provenance["determinism"]["runs"]),
                {"cold_run_1", "cold_run_2", "warm_run_1", "warm_run_2"},
            )
            self.assertTrue(provenance["baseline"]["accepted"])
            self.assertEqual(
                provenance["determinism"]["comparison_sha256"],
                refresh.sha256_file(Path(str(evidence["comparison"]))),
            )
            self.assertNotIn(str(repo), json.dumps(provenance))

    def test_duplicate_run_evidence_is_rejected(self) -> None:
        fake = {"run_id": "cold_run_1"}
        with self.assertRaises(refresh.PipelineError):
            refresh.verify_run_results([fake, fake, fake, fake])


if __name__ == "__main__":
    unittest.main()
