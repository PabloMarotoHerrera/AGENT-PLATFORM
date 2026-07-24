from __future__ import annotations

from pathlib import Path

from hermes_cli.agent_platform import runtime_adapter as ra
from tests.hermes_cli.runtime_adapter_conformance_harness import (
    ALLOWED_SKIP_REASONS,
    EXPECTED_CASE_IDS,
    RuntimeAdapterConformanceHarness,
    RuntimeAdapterConformanceOutcome,
)


PRIMARY_CASE_IDS = tuple(
    case_id
    for case_id in EXPECTED_CASE_IDS
    if case_id not in {"ROLLBACK-002", "FAILURE-001"}
)


def test_conformance_case_registry_is_stable_and_complete(tmp_path: Path) -> None:
    harness = RuntimeAdapterConformanceHarness(tmp_path=tmp_path)

    assert EXPECTED_CASE_IDS == (
        "CONTRACT-001",
        "CONTRACT-002",
        "PROFILE-001",
        "PROFILE-002",
        "ENVIRONMENT-001",
        "ENVIRONMENT-002",
        "ENVIRONMENT-003",
        "WORKSPACE-001",
        "WORKSPACE-002",
        "PATH-001",
        "PROCESS-001",
        "PROCESS-002",
        "STREAM-001",
        "CANCELLATION-001",
        "CANCELLATION-002",
        "SHUTDOWN-001",
        "SHUTDOWN-002",
        "ROLLBACK-001",
        "ROLLBACK-002",
        "EVENT-001",
        "AUDIT-001",
        "FAILURE-001",
        "CONCURRENCY-001",
        "CLEANUP-001",
    )
    assert len(EXPECTED_CASE_IDS) == 24
    assert len(set(EXPECTED_CASE_IDS)) == 24
    assert (
        tuple(case.case_id for case in harness.registered_cases()) == EXPECTED_CASE_IDS
    )


def test_primary_runtime_adapter_conformance_matrix(tmp_path: Path) -> None:
    harness = RuntimeAdapterConformanceHarness(tmp_path=tmp_path)
    results = tuple(harness.run_case(case_id) for case_id in PRIMARY_CASE_IDS)

    failed = [
        result
        for result in results
        if result.outcome is RuntimeAdapterConformanceOutcome.FAILED
    ]
    skipped = [
        result
        for result in results
        if result.outcome is RuntimeAdapterConformanceOutcome.SKIPPED_CAPABILITY
    ]

    assert not failed, failed
    assert all(result.reason_code in ALLOWED_SKIP_REASONS for result in skipped)
    assert {result.case_id for result in results} == set(PRIMARY_CASE_IDS)


def test_event_and_audit_conformance_have_no_readiness_or_persistence(
    tmp_path: Path,
) -> None:
    harness = RuntimeAdapterConformanceHarness(tmp_path=tmp_path)

    event_result = harness.run_case("EVENT-001")
    audit_result = harness.run_case("AUDIT-001")

    assert event_result.outcome is RuntimeAdapterConformanceOutcome.PASSED
    assert audit_result.outcome is RuntimeAdapterConformanceOutcome.PASSED
    assert "cross_component_event_sequence" in event_result.evidence
    assert "in_memory_audit_projection" in audit_result.evidence
    assert not tuple(tmp_path.rglob("*.db"))
    assert not tuple(tmp_path.rglob("*.sqlite"))
    assert not tuple(path for path in tmp_path.rglob("*audit*") if path.is_file())
    assert not tuple(path for path in tmp_path.rglob("*spool*") if path.is_file())


def test_conformance_source_safety_and_root_exports() -> None:
    harness_source = (
        Path(__file__)
        .with_name("runtime_adapter_conformance_harness.py")
        .read_text(encoding="utf-8")
    )
    probe_source = (
        Path(__file__)
        .with_name("runtime_adapter_lifecycle_probe.py")
        .read_text(encoding="utf-8")
    )
    runtime_adapter_root = (
        Path(__file__).resolve().parents[2]
        / "hermes_cli"
        / "agent_platform"
        / "runtime_adapter"
        / "__init__.py"
    ).read_text(encoding="utf-8")

    forbidden_harness_patterns = {
        "shell=True",
        "os.system",
        "os.popen",
        "PowerShell",
        "cmd.exe",
        "taskkill /IM",
        "process-name termination",
        "requests",
        "httpx",
        "urllib.request",
        "socket server",
        "shutil.rmtree",
        "Path.home(",
        "expanduser(",
        "os.environ.copy",
        "provider invocation",
        "worker launch",
        "agent launch",
        "MCP execution",
        "git command",
    }
    for pattern in forbidden_harness_patterns:
        assert pattern not in harness_source

    assert "Path.home()" in probe_source
    assert 'os.path.expanduser("~")' in probe_source
    assert "--verify-managed-environment" in probe_source
    assert "RuntimeAdapterConformanceHarness" not in runtime_adapter_root
    assert "GovernedRuntimeAdapter" not in runtime_adapter_root
    assert not hasattr(ra, "RuntimeAdapterConformanceHarness")
    assert not hasattr(ra, "GovernedRuntimeAdapter")
    assert "RuntimeAdapterConformanceHarness" not in ra.__all__
