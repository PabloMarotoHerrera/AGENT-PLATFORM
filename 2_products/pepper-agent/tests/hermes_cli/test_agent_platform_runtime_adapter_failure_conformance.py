from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from hermes_cli.agent_platform import runtime_adapter as ra
from hermes_cli.agent_platform.runtime_adapter.process_tree import ProcessTreeBackend
from tests.hermes_cli.runtime_adapter_conformance_harness import (
    RuntimeAdapterConformanceHarness,
    RuntimeAdapterConformanceOutcome,
)


def test_failure_conformance_matrix(tmp_path: Path) -> None:
    harness = RuntimeAdapterConformanceHarness(tmp_path=tmp_path)

    rollback = harness.run_case("ROLLBACK-002")
    failure = harness.run_case("FAILURE-001")

    assert rollback.outcome is RuntimeAdapterConformanceOutcome.PASSED
    assert failure.outcome is RuntimeAdapterConformanceOutcome.PASSED
    assert "marker_failure_closed" in rollback.evidence
    assert "runtime_rollback_marker_error" in failure.evidence
    assert all("raw-message" not in item for item in failure.evidence)


def test_failed_assertion_still_triggers_exact_cleanup(tmp_path: Path) -> None:
    harness = RuntimeAdapterConformanceHarness(tmp_path=tmp_path)
    ctx = harness._allocate_context("failure.assertion.cleanup")

    with pytest.raises(AssertionError):
        try:
            harness._sanitize(ctx)
            harness._launch(ctx, "--sleep-ms", "5000")
            raise AssertionError("synthetic conformance assertion")
        finally:
            harness._cleanup_context(ctx)

    assert ctx.runtime_id not in ctx.owner.owned_runtime_ids()
    assert not ctx.allocation.paths.workspace_root.exists()
    assert not tuple(tmp_path.rglob(".agent-platform-runtime-workspace.json"))


def test_cleanup_failure_is_not_converted_to_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness = RuntimeAdapterConformanceHarness(tmp_path=tmp_path)
    ctx = harness._allocate_context("failure.cleanup.not.success")
    original_rollback = harness._rollback

    def failed_rollback(*_args, **_kwargs):
        return SimpleNamespace(outcome=ra.RuntimeOperationOutcome.ROLLBACK_FAILED)

    monkeypatch.setattr(harness, "_rollback", failed_rollback)
    with pytest.raises(AssertionError):
        harness._cleanup_context(ctx)
    monkeypatch.setattr(harness, "_rollback", original_rollback)
    harness._cleanup_context(ctx)

    assert not ctx.allocation.paths.workspace_root.exists()


def test_failure_paths_preserve_sibling_and_unrelated_process(tmp_path: Path) -> None:
    harness = RuntimeAdapterConformanceHarness(tmp_path=tmp_path)
    backend = ProcessTreeBackend()
    current_pid = __import__("os").getpid()
    assert backend.pid_exists(current_pid)

    result = harness.run_case("ROLLBACK-002")

    assert result.outcome is RuntimeAdapterConformanceOutcome.PASSED
    assert backend.pid_exists(current_pid)
    assert not tuple(tmp_path.rglob(".agent-platform-runtime-workspace.json"))
