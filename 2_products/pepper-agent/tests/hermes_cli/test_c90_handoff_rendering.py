"""Exact persisted rendering retrieval, with isolated real handoff authority."""

import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from hermes_cli.agent_platform import handoff_rendering as rendering
from hermes_cli.agent_platform import product_runtime as pr, post_accept_material_revision as revision
from tests.hermes_cli.test_c73_post_accept_material_revision import (
    accepted as accepted, flow as flow, projection_home as projection_home,
)
from tools import pepper_workflow_tools as tools
from tests.hermes_cli import test_agent_platform_work_packet_kanban_projection as fixtures


@pytest.fixture
def prepared(accepted):
    accepted.path = pr.human_git_handoff_prepare_record_path_for_ticket(accepted.projection["ticket_id"])
    accepted.record = json.loads(accepted.path.read_bytes())
    accepted.guards = {key: accepted.record[key] for key in rendering.GUARDS}
    return accepted


def retrieve(f, **changes):
    return json.loads(tools._inspect_current_ticket_review_candidate({"operation": "handoff_script", **f.guards, **changes}))


def test_exact_script_is_deterministic_read_only_and_does_not_render_again(prepared, projection_home, monkeypatch):
    f = prepared
    def forbidden(*args, **kwargs):
        pytest.fail("retrieval must not execute Git, prepare, materialize or render a new script")
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    for name in ("prepare_current_ticket_human_git_handoff", "prepare_current_ticket_review",
                 "_build_p17_7_current_human_git_handoff_result", "_build_human_candidate_materialization_plan",
                 "_render_c12_human_git_handoff_powershell", "_current_handoff_execution_git_snapshot"):
        monkeypatch.setattr(pr, name, forbidden)
    def files():
        return {str(p): p.read_bytes() for p in Path(projection_home).rglob("*") if p.is_file()}
    before = files()
    output = retrieve(f)
    assert output["success"], output
    assert output == retrieve(f)
    body = output["rendered_handoff_powershell"]
    assert body == f.record["rendered_handoff_powershell"]
    assert output["recomputed_rendered_powershell_SHA256"] == f.record["rendered_powershell_SHA256"]
    assert output["script_bytes_SHA256"] == hashlib.sha256(body.encode("utf-8")).hexdigest()
    assert output["script_bytes_SHA256"] != output["rendered_powershell_SHA256"]
    preimage = pr.PEPPER_HUMAN_GIT_HANDOFF_C12_RENDERED_DIGEST_ALGORITHM + "\n" + json.dumps(
        {"rendered_handoff_powershell": body}, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    )
    assert hashlib.sha256(preimage.encode("utf-8")).hexdigest() == output["rendered_powershell_SHA256"]
    assert output["byte_count"] == len(body.encode("utf-8"))
    assert output["character_count"] == len(body)
    assert output["line_endings"] == "LF" and "\r" not in body and body.endswith("\n")
    assert output["script_encoding"] == "UTF-8" and output["script_bom"] is False
    assert output["candidate_paths"] == f.record["candidate_paths"]
    assert output["expected_parent_commit"] == f.record["expected_parent_commit"]
    assert output["expected_branch"] == f.record["branch"]
    assert output["expected_commit_message"] == f.record["commit_message"]
    assert output["post_execution_next_action"]["id"] == f.record["next_action"]["id"]
    assert not output["materialization_performed"] and not output["handoff_regenerated"]
    assert output["Git_commands_executed"] == 0 and not output["workflow_mutation"]
    assert files() == before


@pytest.mark.parametrize("key", rendering.GUARDS)
def test_every_exact_guard_is_a_comparison_not_evidence(prepared, key):
    wrong = "P99.999" if key == "ticket_id" else prepared.guards[key] + 1 if key == "reviewed_run_id" else "0" * 64
    output = retrieve(prepared, **{key: wrong})
    assert not output["success"]
    assert output["blocker_code"] == "HANDOFF_SCRIPT_UNAVAILABLE"
    assert "rendered_handoff_powershell" not in output


@pytest.mark.parametrize("mutation", ["null", "object", "text", "crlf", "bom", "terminal_newline", "digest", "paths"])
def test_corrupt_rendering_and_paths_fail_closed(prepared, mutation):
    f = prepared
    record = dict(f.record)
    body = record["rendered_handoff_powershell"]
    if mutation == "null":
        record["rendered_handoff_powershell"] = None
    elif mutation == "object":
        record["rendered_handoff_powershell"] = {"text": body}
    elif mutation == "text":
        record["rendered_handoff_powershell"] = body + "# changed\n"
    elif mutation == "crlf":
        record["rendered_handoff_powershell"] = body.replace("\n", "\r\n")
    elif mutation == "bom":
        record["rendered_handoff_powershell"] = "\ufeff" + body
    elif mutation == "terminal_newline":
        record["rendered_handoff_powershell"] = body.rstrip("\n")
    elif mutation == "digest":
        record["rendered_powershell_SHA256"] = "0" * 64
    else:
        record["candidate_paths"] = record["candidate_paths"][:-1]
    # Even resealing the outer record cannot substitute malformed inner evidence.
    record["handoff_prepare_record_SHA256"] = pr._human_git_handoff_prepare_record_digest(record)
    f.path.write_text(json.dumps(record))
    output = retrieve(f, handoff_prepare_record_SHA256=record["handoff_prepare_record_SHA256"])
    assert not output["success"] and "rendered_handoff_powershell" not in output


def test_optional_transition_absence_is_not_current_handoff_absence(prepared):
    f = prepared
    assert not revision.path_for(f.projection).exists()
    assert retrieve(f)["success"]
    historical = json.loads(tools._inspect_current_ticket_review_candidate({
        "operation": "post_accept_history", "ticket_id": f.record["ticket_id"],
        "work_packet_SHA256": f.record["work_packet_SHA256"], "evidence_section": "handoff",
    }))
    assert not historical["success"]
    assert historical["blocker_code"] == "POST_ACCEPT_HISTORY_UNAVAILABLE"
    assert "handoff_script" in historical["blocker_detail"]


def test_required_review_provenance_missing_still_blocks(prepared):
    pr.review_prepare_record_path_for_ticket(prepared.record["ticket_id"]).unlink()
    output = retrieve(prepared)
    assert not output["success"] and "rendered_handoff_powershell" not in output


def test_superseded_handoff_cannot_be_retrieved_as_current(prepared):
    revision.request(**prepared.args)
    assert not retrieve(prepared)["success"]


@pytest.mark.parametrize("extra", [{"candidate_path": "arbitrary.ps1"}, {"evidence_offset": 1}, {"reviewed_run_id": True}])
def test_no_arbitrary_paths_partial_body_or_coerced_run(prepared, extra):
    assert not retrieve(prepared, **extra)["success"]


def test_complete_body_bound_never_returns_truncated_script(prepared, monkeypatch):
    monkeypatch.setattr(rendering, "MAX_SCRIPT_BYTES", 10)
    output = retrieve(prepared)
    assert not output["success"] and "rendered_handoff_powershell" not in output


def test_ten_accepted_paths_remain_exactly_bound(monkeypatch, request):
    paths = ["2_products/pepper-agent/web/src/" + path for path in (
        "App.tsx", "agent-platform/design-system/brand.ts", "agent-platform/design-system/design-system.test.ts",
        "agent-platform/design-system/index.ts", "agent-platform/design-system/tokens.css",
        "agent-platform/design-system/tokens.ts", "agent-platform/shell/brand-lockup.tsx",
        "agent-platform/shell/shell.test.tsx", "index.css", "themes/presets.ts",
    )]
    original = fixtures._write_synthetic_terminal_candidate_manifest
    def candidate(*args, **kwargs):
        fixture = original(*args, **kwargs)
        for path in paths:
            fixtures._write_fixture_file(fixture["source_root"], path, "original\n")
            fixtures._write_fixture_file(fixture["workspace"], path, "accepted candidate\n")
        manifest = json.loads(fixture["manifest_path"].read_text())
        manifest["writable_allowed_paths"] = paths
        fixture["manifest_path"].write_text(json.dumps(manifest))
        fixture["writable_rel"] = paths[0]
        return fixture
    monkeypatch.setattr(fixtures, "_write_synthetic_terminal_candidate_manifest", candidate)
    f = request.getfixturevalue("prepared")
    output = retrieve(f)
    assert output["success"], output
    assert output["candidate_paths"] == sorted(paths)
    assert output["candidate_count"] == 10
    assert output["ticket_id"] != "P18.9.12"  # generic authority path
