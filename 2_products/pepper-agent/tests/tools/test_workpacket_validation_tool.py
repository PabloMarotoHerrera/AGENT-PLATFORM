from __future__ import annotations

from dataclasses import dataclass, replace
from io import BytesIO
import json
from pathlib import Path
import sys
import time

import pytest

from tools import governed_workpacket_file_guard as file_guard
from tools import workpacket_validation_tool as tool


@dataclass(frozen=True)
class _Ticket:
    ticket_type: str = "implementation"


@dataclass(frozen=True)
class _Step:
    validation_id: str
    description: str
    expected_result: str
    command: str | None = None


@dataclass(frozen=True)
class _WorkPacket:
    validation_steps: tuple[_Step, ...]
    source_ticket: _Ticket = _Ticket()
    ticket_id: str = "P18.9.1"


class _FakeProcess:
    def __init__(self, stdout: bytes = b"ok\n", stderr: bytes = b"", code: int = 0):
        self.stdout = BytesIO(stdout)
        self.stderr = BytesIO(stderr)
        self.code = code
        self.terminated = False
        self.killed = False

    def poll(self):
        return self.code

    def wait(self):
        return self.code

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True


def _authority(
    workspace: Path,
    *,
    allowed_paths: tuple[str, ...],
    forbidden_paths: tuple[str, ...] = (),
) -> file_guard.WorkPacketFileAuthority:
    return file_guard.WorkPacketFileAuthority(
        ticket_id="P18.9.1",
        work_packet_id="WP-P18-9-1-R0001-123456789abc",
        work_packet_SHA256="a" * 64,
        ticket_spec_SHA256="b" * 64,
        projection_SHA256="c" * 64,
        allowed_paths=allowed_paths,
        forbidden_paths=forbidden_paths,
        workspace_root=workspace,
        resolved_workspace_root=workspace.resolve(strict=True),
    )


def _workpacket_with_steps(*steps: _Step) -> _WorkPacket:
    return _WorkPacket(validation_steps=tuple(steps))


def _write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _install_review_prepare_current_run_authority(
    projection: dict[str, object],
    completion: dict[str, object],
    *,
    task_status: str = "done",
    task_current_run_id: int | None = None,
    runs: tuple[dict[str, object], ...] | None = None,
) -> None:
    from hermes_cli import kanban_db

    board = str(projection["kanban_board_slug"])
    task_id = str(projection["kanban_task_id"])
    workspace = Path(str(completion.get("kanban_task_workspace_path") or ".")).as_posix()
    run_id = int(completion["run_id"])
    now = int(time.time())
    if runs is None:
        runs = ({
            "id": run_id,
            "status": str(completion.get("run_status") or "done"),
            "outcome": str(completion.get("run_outcome") or "completed"),
            "started_at": now - 60,
            "ended_at": now,
            "summary": "synthetic exact current terminal run",
            "metadata": {},
        },)
    kanban_db.create_board(board)
    conn = kanban_db.connect(board=board)
    try:
        conn.execute("DELETE FROM task_runs WHERE task_id = ?", (task_id,))
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.execute(
            """
            INSERT INTO tasks (
                id, title, status, created_at, completed_at, workspace_kind,
                workspace_path, current_run_id
            ) VALUES (?, ?, ?, ?, ?, 'dir', ?, ?)
            """,
            (
                task_id,
                "Synthetic current terminal run authority",
                task_status,
                now - 120,
                now if task_status == "done" else None,
                workspace,
                task_current_run_id,
            ),
        )
        for run in runs:
            metadata = run.get("metadata")
            conn.execute(
                """
                INSERT INTO task_runs (
                    id, task_id, profile, step_key, status, started_at, ended_at,
                    outcome, summary, metadata
                ) VALUES (?, ?, ?, NULL, ?, ?, ?, ?, ?, ?)
                """,
                (
                    int(run["id"]),
                    task_id,
                    "implementation_product",
                    str(run.get("status") or "done"),
                    int(run.get("started_at") or now - 60),
                    run.get("ended_at"),
                    run.get("outcome"),
                    run.get("summary"),
                    json.dumps(metadata) if isinstance(metadata, dict) else None,
                ),
            )
        conn.commit()
    finally:
        conn.close()


def _review_prepare_projection_contract_completion(
    command_steps: list[dict[str, object]],
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    projection = {
        "project_id": "PEPPER",
        "ticket_id": "P18.9.1",
        "ticket_spec_SHA256": "b" * 64,
        "work_packet_id": "WP-P18-9-1-R0001-123456789abc",
        "work_packet_SHA256": "a" * 64,
        "projection_SHA256": "c" * 64,
        "kanban_board_slug": "pepper",
        "kanban_task_id": "t_p18_9_1",
    }
    contract = {
        **projection,
        "acceptance_criteria": ["synthetic acceptance"],
        "response_contract": {"completion_verdict": "synthetic_ready"},
        "work_packet_validation_steps": command_steps,
        "validation_steps": [],
    }
    contract["criteria_revision_SHA256"] = tool._criteria_revision_digest_if_possible(contract)
    contract["acceptance_contract_SHA256"] = tool._digest_payload(
        tool._ACCEPTANCE_CONTRACT_DIGEST_ALGORITHM,
        {key: value for key, value in contract.items() if key != "acceptance_contract_SHA256"},
    )
    completion = {
        "blocker_code": None,
        "blocker_detail": None,
        "kanban_board_slug": projection["kanban_board_slug"],
        "kanban_task_id": projection["kanban_task_id"],
        "kanban_task_current_run_id": None,
        "run_id": 7,
        "run_status": "done",
        "run_outcome": "completed",
        "kanban_task_workspace_path": "synthetic-validation-workspace",
        "run_metadata": {},
    }
    completion["kanban_completion_result_SHA256"] = tool._digest_payload(
        tool._KANBAN_COMPLETION_RESULT_DIGEST_ALGORITHM,
        {key: value for key, value in completion.items() if key != "kanban_completion_result_SHA256"},
    )
    _install_review_prepare_current_run_authority(projection, completion)
    return projection, contract, completion


def _refresh_completion_digest(completion: dict[str, object]) -> None:
    completion["kanban_completion_result_SHA256"] = tool._digest_payload(
        tool._KANBAN_COMPLETION_RESULT_DIGEST_ALGORITHM,
        {key: value for key, value in completion.items() if key != "kanban_completion_result_SHA256"},
    )


def _refresh_contract_digests(contract: dict[str, object]) -> None:
    contract["criteria_revision_SHA256"] = tool._criteria_revision_digest_if_possible(contract)
    contract["acceptance_contract_SHA256"] = tool._digest_payload(
        tool._ACCEPTANCE_CONTRACT_DIGEST_ALGORITHM,
        {key: value for key, value in contract.items() if key != "acceptance_contract_SHA256"},
    )


def _rematerialized_validation_context(
    tmp_path: Path,
    workspace: Path,
    completion: dict[str, object],
) -> dict[str, object]:
    return {
        "validation_origin": "review_prepare_rematerialized_source_authority",
        "validation_workspace_policy_id": "pepper-review-prepare-validation-rematerialized-workspace-v1",
        "workspace_path": workspace.as_posix(),
        "terminal_workspace_path": completion.get("kanban_task_workspace_path"),
        "terminal_workspace_available": False,
        "rematerialized_from_terminal_run_id": completion["run_id"],
        "durable_source_authority_reference": {
            "authority_path": (tmp_path / "source-authority.json").as_posix(),
            "authority_SHA256": "d" * 64,
            "snapshot_SHA256": "e" * 64,
        },
        "durable_source_authority_SHA256": "d" * 64,
    }


def _passing_result(
    contract: dict[str, object],
    spec: tool.GovernedValidationCommandSpec,
) -> dict[str, object]:
    return {
        "success": True,
        "policy_id": tool.GOVERNED_VALIDATION_POLICY_ID,
        "work_packet_id": contract["work_packet_id"],
        "work_packet_SHA256": contract["work_packet_SHA256"],
        "ticket_id": contract["ticket_id"],
        "command": {
            "command_id": spec.command_id,
            "validation_id": spec.validation_id,
            "source": spec.source,
            "source_command": spec.source_command,
            "working_directory": spec.working_directory,
            "timeout_seconds": spec.timeout_seconds,
            "expected_exit_codes": list(spec.expected_exit_codes),
            "runtime_available": True,
            "runtime_unavailable_reason": None,
        },
        "disposition": "passed",
        "failure_reason": "none",
        "exit_code": 0,
        "process_started": True,
    }


def test_non_governed_tool_fails_closed(monkeypatch) -> None:
    monkeypatch.delenv(file_guard.GOVERNED_WORKER_ENV, raising=False)

    result = json.loads(tool.workpacket_validation_tool(action="list"))

    assert result["error_code"] == tool.WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE


def test_registry_dispatch_accepts_session_metadata(monkeypatch) -> None:
    authority = _authority(
        Path(__file__).resolve().parent,
        allowed_paths=("tests/**",),
    )
    work_packet = _workpacket_with_steps()
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, work_packet),
    )

    result = json.loads(
        tool.registry.dispatch(
            "workpacket_validation",
            {"action": "list"},
            task_id="t_d5b19f78",
            session_id="session-1",
            user_task="P18.9.1",
        )
    )

    assert result["success"] is True
    assert result["command_count"] == 0


def test_python_command_run_uses_shell_false_and_minimal_env(tmp_path, monkeypatch) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    authority = _authority(workspace, allowed_paths=("tests/**",))
    work_packet = _workpacket_with_steps(
        _Step(
            "V1",
            "Run focused Python tests.",
            "The focused pytest command passes.",
            command="python -m pytest tests/example_test.py",
        )
    )
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, work_packet),
    )

    from hermes_cli.agent_platform.work_packet import validation_command_runner as vcr

    calls = []

    def fake_popen(*args, **kwargs):
        calls.append((args, kwargs))
        return _FakeProcess()

    monkeypatch.setattr(vcr.subprocess, "Popen", fake_popen)

    result = json.loads(tool.workpacket_validation_tool(action="run", command_id="GVCMD-001"))

    assert result["success"] is True
    assert result["disposition"] == "passed"
    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args[0][:3] == (Path(sys.executable).resolve().as_posix(), "-m", "pytest")
    assert args[0][-2:] == ("-p", "no:cacheprovider")
    assert kwargs["shell"] is False
    assert kwargs["stdin"] is vcr.subprocess.DEVNULL
    assert kwargs["cwd"] == workspace.resolve().as_posix()
    assert kwargs["env"]["CI"] == "1"
    assert "PATH" not in kwargs["env"]


def test_python_command_outside_workpacket_scope_is_not_authorized(tmp_path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    authority = _authority(workspace, allowed_paths=("src/**",))
    work_packet = _workpacket_with_steps(
        _Step(
            "V1",
            "Run focused Python tests.",
            "The focused pytest command passes.",
            command="python -m pytest tests/outside_test.py",
        )
    )

    specs = tool.build_governed_validation_command_specs(authority, work_packet)

    assert specs == ()


def test_unlisted_command_id_is_denied(tmp_path, monkeypatch) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    authority = _authority(workspace, allowed_paths=("tests/**",))
    work_packet = _workpacket_with_steps(
        _Step("V1", "Run focused Python tests.", "The focused pytest command passes.", command="python -m unittest --help")
    )
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, work_packet),
    )

    result = json.loads(tool.workpacket_validation_tool(action="run", command_id="GVCMD-999"))

    assert result["error_code"] == tool.WORKPACKET_VALIDATION_COMMAND_DENIED


def test_review_prepare_validation_api_runs_exact_authorized_requirement(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    requirements = tool.review_prepare_validation_requirements(contract)
    authority = _authority(workspace, allowed_paths=("tests/**",))
    spec = tool.GovernedValidationCommandSpec(
        command_id="GVCMD-001",
        validation_id="V1",
        source="workpacket.validation_steps.command",
        source_command=command,
        effective_argv=(Path(sys.executable).resolve().as_posix(), "-m", "pytest", "tests/example_test.py"),
        working_directory=workspace.as_posix(),
    )
    observed: list[tool.GovernedValidationCommandSpec] = []
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "build_governed_validation_command_specs",
        lambda _authority, _work_packet: (spec,),
    )

    def fake_run(_authority, selected):
        observed.append(selected)
        return json.dumps({
            "success": True,
            "policy_id": tool.GOVERNED_VALIDATION_POLICY_ID,
            "work_packet_id": contract["work_packet_id"],
            "work_packet_SHA256": contract["work_packet_SHA256"],
            "ticket_id": contract["ticket_id"],
            "command": {
                "command_id": selected.command_id,
                "validation_id": selected.validation_id,
                "source": selected.source,
                "source_command": selected.source_command,
                "working_directory": selected.working_directory,
                "timeout_seconds": selected.timeout_seconds,
                "expected_exit_codes": list(selected.expected_exit_codes),
                "runtime_available": True,
                "runtime_unavailable_reason": None,
            },
            "disposition": "passed",
            "failure_reason": "none",
            "exit_code": 0,
            "process_started": True,
        })

    monkeypatch.setattr(tool, "_run_command", fake_run)

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={"HERMES_AGENT_PLATFORM_WORKPACKET_ID": contract["work_packet_id"]},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requirements=requirements,
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert observed == [spec]
    assert result["validation_executed"] is True
    assert result["validation_complete"] is True
    assert result["validation_passed"] is True
    authority_record = result["review_prepare_validation_authority"]
    assert authority_record["policy_id"] == tool.REVIEW_PREPARE_VALIDATION_AUTHORITY_POLICY_ID
    assert authority_record["command_execution_authority"] == "explicit_human_review_preparation_action"
    assert result["validation_command_results"][0]["validation_result_SHA256"]


def test_review_prepare_validation_authority_narrows_manifest_to_selected_requirements(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    v1 = "python -m pytest tests/v1_test.py"
    v2 = "python -m pytest tests/v2_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": v1, "expected_exit_codes": [0]},
    ])
    authority = _authority(workspace, allowed_paths=("tests/**",))
    specs = (
        tool.GovernedValidationCommandSpec(
            command_id="GVCMD-001",
            validation_id="V1",
            source="workpacket.validation_steps.command",
            source_command=v1,
            effective_argv=(Path(sys.executable).resolve().as_posix(), "-m", "pytest", "tests/v1_test.py"),
            working_directory=workspace.as_posix(),
        ),
        tool.GovernedValidationCommandSpec(
            command_id="GVCMD-002",
            validation_id="V2",
            source="workpacket.validation_steps.command",
            source_command=v2,
            effective_argv=(Path(sys.executable).resolve().as_posix(), "-m", "pytest", "tests/v2_test.py"),
            working_directory=workspace.as_posix(),
        ),
    )
    captured: list[tool.GovernedValidationCommandSpec] = []
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(tool, "build_governed_validation_command_specs", lambda *_args: specs)

    def fake_run(_authority, selected):
        captured.append(selected)
        return json.dumps(_passing_result(contract, selected))

    monkeypatch.setattr(tool, "_run_command", fake_run)

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    authority_record = result["review_prepare_validation_authority"]
    assert captured == [specs[0]]
    assert [
        item["validation_id"]
        for item in authority_record["workpacket_capability_manifest"]
    ] == ["V1", "V2"]
    assert [
        item["validation_id"]
        for item in authority_record["review_prepare_authorized_command_manifest"]
    ] == ["V1"]
    assert authority_record["authorized_command_manifest"] == authority_record[
        "review_prepare_authorized_command_manifest"
    ]
    assert authority_record["workpacket_capability_manifest_SHA256"] != authority_record[
        "review_prepare_authorized_command_manifest_SHA256"
    ]


def test_review_prepare_validation_records_rematerialized_origin_context(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "rematerialized"
    workspace.mkdir()
    terminal_workspace = tmp_path / "deleted-terminal-workspace"
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    completion["kanban_task_workspace_path"] = terminal_workspace.as_posix()
    _refresh_completion_digest(completion)
    _install_review_prepare_current_run_authority(projection, completion)
    context = {
        "validation_origin": "review_prepare_rematerialized_source_authority",
        "validation_workspace_policy_id": "pepper-review-prepare-validation-rematerialized-workspace-v1",
        "workspace_path": workspace.as_posix(),
        "terminal_workspace_path": terminal_workspace.as_posix(),
        "terminal_workspace_available": False,
        "rematerialized_from_terminal_run_id": completion["run_id"],
        "durable_source_authority_reference": {
            "authority_path": (tmp_path / "source-authority.json").as_posix(),
            "authority_SHA256": "d" * 64,
            "snapshot_SHA256": "e" * 64,
        },
        "durable_source_authority_SHA256": "d" * 64,
    }
    authority = _authority(workspace, allowed_paths=("tests/**",))
    spec = tool.GovernedValidationCommandSpec(
        command_id="GVCMD-001",
        validation_id="V1",
        source="workpacket.validation_steps.command",
        source_command=command,
        effective_argv=(Path(sys.executable).resolve().as_posix(), "-m", "pytest", "tests/example_test.py"),
        working_directory=workspace.as_posix(),
    )
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(tool, "build_governed_validation_command_specs", lambda *_args: (spec,))
    monkeypatch.setattr(tool, "_run_command", lambda _authority, selected: json.dumps(_passing_result(contract, selected)))

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=context,
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    authority_record = result["review_prepare_validation_authority"]
    assert result["validation_passed"] is True
    assert result["validation_origin"] == "review_prepare_rematerialized_source_authority"
    assert authority_record["validation_origin"] == "review_prepare_rematerialized_source_authority"
    assert authority_record["validation_workspace_path"] == workspace.as_posix()
    assert authority_record["durable_source_authority_SHA256"] == "d" * 64


def test_review_prepare_validation_context_is_mandatory(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    authority = _authority(workspace, allowed_paths=("tests/**",))
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("missing context ran")),
    )

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_executed"] is False
    assert result["validation_passed"] is False
    assert result["error_code"] == tool.REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED
    assert "validation context" in result["failure_detail"]


def test_review_prepare_validation_context_denies_workspace_mismatch(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    other_workspace = tmp_path / "other"
    other_workspace.mkdir()
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    completion["kanban_task_workspace_path"] = (tmp_path / "terminal").as_posix()
    _refresh_completion_digest(completion)
    _install_review_prepare_current_run_authority(projection, completion)
    authority = _authority(workspace, allowed_paths=("tests/**",))
    context = {
        "validation_origin": "review_prepare_rematerialized_source_authority",
        "workspace_path": other_workspace.as_posix(),
        "rematerialized_from_terminal_run_id": completion["run_id"],
        "durable_source_authority_reference": {
            "authority_path": (tmp_path / "source-authority.json").as_posix(),
            "authority_SHA256": "d" * 64,
            "snapshot_SHA256": "e" * 64,
        },
        "durable_source_authority_SHA256": "d" * 64,
    }
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("mismatch executed")),
    )

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=context,
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_executed"] is False
    assert result["error_code"] == tool.REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED
    assert "workspace authority mismatch" in result["failure_detail"]


def test_review_prepare_validation_context_requires_rematerialized_policy(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    completion["kanban_task_workspace_path"] = (tmp_path / "terminal").as_posix()
    _refresh_completion_digest(completion)
    _install_review_prepare_current_run_authority(projection, completion)
    authority = _authority(workspace, allowed_paths=("tests/**",))
    context = {
        "validation_origin": "review_prepare_rematerialized_source_authority",
        "workspace_path": workspace.as_posix(),
        "rematerialized_from_terminal_run_id": completion["run_id"],
        "durable_source_authority_reference": {
            "authority_path": (tmp_path / "source-authority.json").as_posix(),
            "authority_SHA256": "d" * 64,
            "snapshot_SHA256": "e" * 64,
        },
        "durable_source_authority_SHA256": "d" * 64,
    }
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("policy mismatch executed")),
    )

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=context,
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_executed"] is False
    assert result["error_code"] == tool.REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED
    assert "policy mismatch" in result["failure_detail"]


def test_review_prepare_validation_authority_denies_stale_current_terminal_run(
    tmp_path,
    monkeypatch,
) -> None:
    from hermes_cli import kanban_db

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    kanban_db.create_board("pepper")
    conn = kanban_db.connect(board="pepper")
    try:
        task_id = kanban_db.create_task(
            conn,
            title="Synthetic validation current-run test",
            body="binds validation to latest terminal run",
            assignee="implementation_product",
            workspace_kind="dir",
            workspace_path=workspace.as_posix(),
            initial_status="running",
        )
        assert kanban_db.complete_task(
            conn,
            task_id,
            summary="first terminal completion",
            metadata={},
        )
        stale_run = kanban_db.list_runs(conn, task_id)[-1]
        conn.execute(
            """
            INSERT INTO task_runs (
                task_id, profile, step_key, status, started_at, ended_at,
                outcome, summary, metadata
            ) VALUES (?, ?, NULL, 'done', ?, ?, 'completed', ?, ?)
            """,
            (
                task_id,
                "implementation_product",
                int(stale_run.started_at) + 10,
                int(stale_run.started_at) + 20,
                "newer terminal completion",
                json.dumps({}),
            ),
        )
        conn.commit()
    finally:
        conn.close()

    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    projection["kanban_task_id"] = task_id
    contract["kanban_task_id"] = task_id
    _refresh_contract_digests(contract)
    completion["kanban_task_id"] = task_id
    completion["run_id"] = stale_run.id
    _refresh_completion_digest(completion)
    authority = _authority(workspace, allowed_paths=("tests/**",))
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("stale run executed")),
    )

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_executed"] is False
    assert result["validation_passed"] is False
    assert result["error_code"] == tool.REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED
    assert "current terminal Kanban run" in result["failure_detail"]


@pytest.mark.parametrize(
    ("case", "expected_denied"),
    (
        ("connect_failure", True),
        ("task_absent", True),
        ("no_runs", True),
        ("stale_completion", True),
        ("active_current_run", True),
        ("exact_current_run", False),
    ),
)
def test_review_prepare_validation_current_run_authority_matrix(
    tmp_path,
    monkeypatch,
    case,
    expected_denied,
) -> None:
    from hermes_cli import kanban_db

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    run_id = int(completion["run_id"])
    board = str(projection["kanban_board_slug"])
    task_id = str(projection["kanban_task_id"])
    if case == "connect_failure":
        monkeypatch.setattr(
            kanban_db,
            "connect",
            lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("db unavailable")),
        )
    elif case == "task_absent":
        conn = kanban_db.connect(board=board)
        try:
            conn.execute("DELETE FROM task_runs WHERE task_id = ?", (task_id,))
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
        finally:
            conn.close()
    elif case == "no_runs":
        conn = kanban_db.connect(board=board)
        try:
            conn.execute("DELETE FROM task_runs WHERE task_id = ?", (task_id,))
            conn.commit()
        finally:
            conn.close()
    elif case == "stale_completion":
        now = int(time.time())
        _install_review_prepare_current_run_authority(
            projection,
            completion,
            runs=(
                {
                    "id": run_id,
                    "status": "done",
                    "outcome": "completed",
                    "started_at": now - 60,
                    "ended_at": now - 30,
                    "summary": "stale terminal completion",
                    "metadata": {},
                },
                {
                    "id": run_id + 1,
                    "status": "done",
                    "outcome": "completed",
                    "started_at": now - 20,
                    "ended_at": now - 10,
                    "summary": "latest terminal completion",
                    "metadata": {},
                },
            ),
        )
    elif case == "active_current_run":
        now = int(time.time())
        _install_review_prepare_current_run_authority(
            projection,
            completion,
            task_status="running",
            task_current_run_id=run_id,
            runs=(
                {
                    "id": run_id,
                    "status": "running",
                    "outcome": None,
                    "started_at": now - 60,
                    "ended_at": None,
                    "summary": "active run",
                    "metadata": {},
                },
            ),
        )
    authority = _authority(workspace, allowed_paths=("tests/**",))
    spec = tool.GovernedValidationCommandSpec(
        command_id="GVCMD-001",
        validation_id="V1",
        source="workpacket.validation_steps.command",
        source_command=command,
        effective_argv=(
            Path(sys.executable).resolve().as_posix(),
            "-m",
            "pytest",
            "tests/example_test.py",
        ),
        working_directory=workspace.as_posix(),
    )
    observed: list[tool.GovernedValidationCommandSpec] = []
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(tool, "build_governed_validation_command_specs", lambda *_args: (spec,))

    def fake_run(_authority, selected):
        observed.append(selected)
        return json.dumps(_passing_result(contract, selected))

    monkeypatch.setattr(tool, "_run_command", fake_run)

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    if expected_denied:
        assert observed == []
        assert result["validation_executed"] is False
        assert result["validation_passed"] is False
        assert result["process_started"] is False
        assert result["error_code"] == tool.REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED
        assert "current" in result["failure_detail"] or "authority" in result["failure_detail"]
    else:
        assert observed == [spec]
        assert result["validation_executed"] is True
        assert result["validation_passed"] is True


def test_review_prepare_validation_reuses_existing_evidence_immutably(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    requirement = tool.review_prepare_validation_requirements(contract)[0]
    authority = _authority(workspace, allowed_paths=("tests/**",))
    spec = tool.GovernedValidationCommandSpec(
        command_id="GVCMD-001",
        validation_id="V1",
        source="workpacket.validation_steps.command",
        source_command=command,
        effective_argv=(Path(sys.executable).resolve().as_posix(), "-m", "pytest", "tests/example_test.py"),
        working_directory=workspace.as_posix(),
    )
    prior_authority = tool.build_review_prepare_validation_authority_record(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        requirements=(requirement,),
        authorized_specs=(spec,),
        workpacket_capability_specs=(spec,),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )
    existing = tool.review_prepare_validation_result_record(
        _passing_result(contract, spec),
        requirement=requirement,
        authority_record=prior_authority,
    )
    completion["run_metadata"] = {"validation_command_results": [existing]}
    _refresh_completion_digest(completion)
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(tool, "build_governed_validation_command_specs", lambda *_args: (spec,))
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("reused evidence executed")),
    )

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    reused = result["validation_command_results"][0]
    assert result["validation_executed"] is False
    assert result["validation_passed"] is True
    assert reused["review_prepare_validation_evidence_mode"] == "existing_evidence_reused"
    assert reused["reused_validation_evidence"] == existing
    assert reused["reused_validation_evidence_SHA256"] == existing["validation_result_SHA256"]
    assert reused["validation_result_SHA256"] == existing["validation_result_SHA256"]
    assert reused["review_prepare_validation_reuse_SHA256"]
    assert "review_prepare_validation_acceptance_authority" not in existing


def test_review_prepare_validation_does_not_reuse_tampered_existing_evidence(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    requirement = tool.review_prepare_validation_requirements(contract)[0]
    authority = _authority(workspace, allowed_paths=("tests/**",))
    spec = tool.GovernedValidationCommandSpec(
        command_id="GVCMD-001",
        validation_id="V1",
        source="workpacket.validation_steps.command",
        source_command=command,
        effective_argv=(Path(sys.executable).resolve().as_posix(), "-m", "pytest", "tests/example_test.py"),
        working_directory=workspace.as_posix(),
    )
    prior_authority = tool.build_review_prepare_validation_authority_record(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        requirements=(requirement,),
        authorized_specs=(spec,),
        workpacket_capability_specs=(spec,),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )
    existing = tool.review_prepare_validation_result_record(
        _passing_result(contract, spec),
        requirement=requirement,
        authority_record=prior_authority,
    )
    tampered = dict(existing)
    tampered["exit_code"] = 2
    completion["run_metadata"] = {"validation_command_results": [tampered]}
    _refresh_completion_digest(completion)
    captured: list[tool.GovernedValidationCommandSpec] = []
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(tool, "build_governed_validation_command_specs", lambda *_args: (spec,))

    def fake_run(_authority, selected):
        captured.append(selected)
        return json.dumps(_passing_result(contract, selected))

    monkeypatch.setattr(tool, "_run_command", fake_run)

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert captured == [spec]
    assert result["validation_executed"] is True
    assert result["validation_passed"] is True
    assert result["validation_command_results"][0].get(
        "review_prepare_validation_evidence_mode"
    ) != "existing_evidence_reused"


@pytest.mark.parametrize(
    "case",
    [
        "missing_prepare_action",
        "wrong_project",
        "wrong_ticket",
        "wrong_action",
        "wrong_ticket_spec",
        "wrong_workpacket_id",
        "wrong_workpacket_sha",
        "wrong_projection_sha",
        "wrong_board",
        "wrong_task",
        "wrong_run",
        "wrong_completion_sha",
        "wrong_acceptance_contract_sha",
    ],
)
def test_review_prepare_validation_authority_negative_matrix_denied(
    tmp_path,
    monkeypatch,
    case,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/example_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    authority = _authority(workspace, allowed_paths=("tests/**",))
    project_id = "PEPPER"
    ticket_id = "P18.9.1"
    next_action_id: str | None = "PREPARE_P18_9_1_REVIEW"
    if case == "missing_prepare_action":
        next_action_id = None
    elif case == "wrong_project":
        project_id = "WRONG"
    elif case == "wrong_ticket":
        ticket_id = "P18.9.2"
    elif case == "wrong_action":
        next_action_id = "PREPARE_P18_9_2_REVIEW"
    elif case == "wrong_ticket_spec":
        authority = replace(authority, ticket_spec_SHA256="9" * 64)
    elif case == "wrong_workpacket_id":
        authority = replace(authority, work_packet_id="WP-P18-9-2-R0001-123456789abc")
    elif case == "wrong_workpacket_sha":
        authority = replace(authority, work_packet_SHA256="9" * 64)
    elif case == "wrong_projection_sha":
        authority = replace(authority, projection_SHA256="9" * 64)
    elif case == "wrong_board":
        completion["kanban_board_slug"] = "wrong"
        _refresh_completion_digest(completion)
    elif case == "wrong_task":
        completion["kanban_task_id"] = "wrong-task"
        _refresh_completion_digest(completion)
    elif case == "wrong_run":
        completion["run_id"] = 8
    elif case == "wrong_completion_sha":
        completion["kanban_completion_result_SHA256"] = "9" * 64
    elif case == "wrong_acceptance_contract_sha":
        contract["acceptance_contract_SHA256"] = "9" * 64
    work_packet = _workpacket_with_steps(
        _Step("V1", "Run focused Python tests.", "The focused pytest command passes.", command=command),
    )
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, work_packet),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("denied authority ran")),
    )

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id=project_id,
        requested_ticket_id=ticket_id,
        requested_next_action_id=next_action_id,
    )

    assert result["validation_executed"] is False
    assert result["validation_passed"] is False
    assert result["error_code"] == tool.REVIEW_PREPARE_VALIDATION_AUTHORITY_DENIED


def test_review_prepare_validation_api_rejects_acceptance_only_package_command(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = (
        "cd 2_products/pepper-agent/web && npm run test -- "
        "src/agent-platform/projects-tickets/projects-tickets.test.tsx"
    )
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",),
    )
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("acceptance-only command ran")),
    )

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_executed"] is False
    assert result["validation_passed"] is None
    assert result["missing_requirements"]


def test_review_prepare_validation_api_runs_workpacket_origin_package_test_plan(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    package_dir = workspace / "2_products/pepper-agent/web"
    test_rel = "2_products/pepper-agent/web/src/agent-platform/projects-tickets/projects-tickets.test.tsx"
    _write(package_dir / "package.json", json.dumps({"scripts": {"test": "vitest run"}}))
    _write(workspace / test_rel, "test('synthetic', () => {})\n")
    node = tmp_path / "node"
    vitest = tmp_path / "vitest.mjs"
    _write(node, "")
    _write(vitest, "")
    command = (
        "cd 2_products/pepper-agent/web && npm run test -- "
        "src/agent-platform/projects-tickets/projects-tickets.test.tsx"
    )
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "command": command, "expected_exit_codes": [0]},
    ])
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",),
    )
    work_packet = _workpacket_with_steps(
        _Step("V1", "Run frontend test.", "The focused test passes.", command=command),
    )
    captured: list[tool.GovernedValidationCommandSpec] = []
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, work_packet),
    )
    monkeypatch.setattr(tool, "_resolve_node_executable", lambda: node)
    monkeypatch.setattr(
        tool,
        "_resolve_node_module_entry",
        lambda _workspace, _package, _entry: vitest,
    )

    def fake_run(_authority, selected):
        captured.append(selected)
        return json.dumps({
            "success": True,
            "policy_id": tool.GOVERNED_VALIDATION_POLICY_ID,
            "work_packet_id": contract["work_packet_id"],
            "work_packet_SHA256": contract["work_packet_SHA256"],
            "ticket_id": contract["ticket_id"],
            "command": {
                "command_id": selected.command_id,
                "validation_id": selected.validation_id,
                "source": selected.source,
                "source_command": selected.source_command,
                "working_directory": selected.working_directory,
                "timeout_seconds": selected.timeout_seconds,
                "expected_exit_codes": list(selected.expected_exit_codes),
                "runtime_available": True,
                "runtime_unavailable_reason": None,
            },
            "disposition": "passed",
            "failure_reason": "none",
            "exit_code": 0,
            "process_started": True,
        })

    monkeypatch.setattr(tool, "_run_command", fake_run)

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_passed"] is True
    assert len(captured) == 1
    selected = captured[0]
    assert selected.source == "workpacket.validation_steps.package_command"
    assert selected.source_command == command
    assert selected.effective_argv == (
        node.as_posix(),
        vitest.as_posix(),
        "run",
        "src/agent-platform/projects-tickets/projects-tickets.test.tsx",
    )
    assert "npm" not in selected.effective_argv
    assert selected.execution_plan_SHA256
    manifest = result["review_prepare_validation_authority"]["authorized_command_manifest"]
    assert manifest[0]["source_command"] == command


def test_review_prepare_validation_api_does_not_auto_execute_manual_commands(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/manual_review_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "kind": "manual", "command": command},
    ])
    authority = _authority(workspace, allowed_paths=("tests/**",))
    spec = tool.GovernedValidationCommandSpec(
        command_id="GVCMD-001",
        validation_id="V1",
        source="workpacket.validation_steps.command",
        source_command=command,
        effective_argv=(Path(sys.executable).resolve().as_posix(), "-m", "pytest", "tests/manual_review_test.py"),
        working_directory=workspace.as_posix(),
    )
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "build_governed_validation_command_specs",
        lambda _authority, _work_packet: (spec,),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("manual command ran")),
    )

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_executed"] is False
    assert result["validation_complete"] is False
    assert result["validation_passed"] is None
    assert result["missing_requirements"][0]["manual"] is True


def test_review_prepare_validation_api_manual_command_accepts_existing_skipped_evidence(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/manual_review_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {"validation_id": "V1", "kind": "manual", "command": command},
    ])
    completion["run_metadata"] = {
        "validation_command_results": [
            {
                "success": True,
                "ticket_id": contract["ticket_id"],
                "work_packet_id": contract["work_packet_id"],
                "work_packet_SHA256": contract["work_packet_SHA256"],
                "command": {
                    "validation_id": "V1",
                    "source_command": command,
                },
                "disposition": "skipped",
                "process_started": False,
                "exit_code": 0,
            }
        ]
    }
    _refresh_completion_digest(completion)
    authority = _authority(workspace, allowed_paths=("tests/**",))
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("manual command ran")),
    )

    assert tool.review_prepare_validation_contract_satisfied(completion, contract) is True

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_executed"] is False
    assert result["validation_complete"] is True
    assert result["validation_passed"] is True
    assert result["validation_command_results"][0]["disposition"] == "skipped"


def test_review_prepare_validation_api_preserves_not_applicable_evidence(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = "python -m pytest tests/not_applicable_test.py"
    projection, contract, completion = _review_prepare_projection_contract_completion([
        {
            "validation_id": "V1",
            "command": command,
            "applicability": "not_applicable",
        },
    ])
    completion["run_metadata"] = {
        "validation_command_results": [
            {
                "success": True,
                "ticket_id": contract["ticket_id"],
                "work_packet_id": contract["work_packet_id"],
                "work_packet_SHA256": contract["work_packet_SHA256"],
                "command": {
                    "validation_id": "V1",
                    "source_command": command,
                },
                "disposition": "not_applicable",
                "process_started": False,
                "exit_code": 0,
            }
        ]
    }
    _refresh_completion_digest(completion)
    authority = _authority(workspace, allowed_paths=("tests/**",))
    monkeypatch.setattr(
        tool,
        "resolve_governed_workpacket_validation_authority",
        lambda _env=None: (authority, _workpacket_with_steps()),
    )
    monkeypatch.setattr(
        tool,
        "_run_command",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("not_applicable ran")),
    )

    assert tool.review_prepare_validation_contract_satisfied(completion, contract) is True

    result = tool.run_review_prepare_validation_commands(
        projection=projection,
        completion=completion,
        acceptance_contract=contract,
        worker_env={},
        validation_context=_rematerialized_validation_context(
            tmp_path,
            workspace,
            completion,
        ),
        requested_project_id="PEPPER",
        requested_ticket_id="P18.9.1",
        requested_next_action_id="PREPARE_P18_9_1_REVIEW",
    )

    assert result["validation_executed"] is False
    assert result["validation_complete"] is True
    assert result["validation_passed"] is True
    assert result["validation_command_results"][0]["command"]["source_command"] == command


def test_workpacket_frontend_package_command_uses_exact_workpacket_source(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    _write(package_dir / "package.json", json.dumps({"scripts": {"test": "vitest run"}}))
    node = tmp_path / "node"
    vitest = tmp_path / "vitest.mjs"
    _write(node, "")
    _write(vitest, "")
    command = (
        "cd 2_products/pepper-agent/web && npm run test -- "
        "src/agent-platform/projects-tickets/projects-tickets.test.tsx"
    )
    test_file = (
        "2_products/pepper-agent/web/src/agent-platform/projects-tickets/"
        "projects-tickets.test.tsx"
    )
    _write(workspace / test_file, "test('synthetic', () => {})\n")
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",),
    )
    work_packet = _workpacket_with_steps(
        _Step(
            "V1",
            "Focused frontend tests validate route compatibility.",
            "The exact WorkPacket frontend test command passes.",
            command=command,
        ),
    )
    monkeypatch.setattr(tool, "_resolve_node_executable", lambda: node)
    monkeypatch.setattr(
        tool,
        "_resolve_node_module_entry",
        lambda _workspace, _package, _entry: vitest,
    )

    specs = tool.build_governed_validation_command_specs(authority, work_packet)

    assert len(specs) == 1
    spec = specs[0]
    assert spec.command_id == "GVCMD-001"
    assert spec.validation_id == "V1"
    assert spec.source_command == command
    assert spec.effective_argv[:3] == (node.as_posix(), vitest.as_posix(), "run")
    assert spec.effective_argv[3:] == (
        "src/agent-platform/projects-tickets/projects-tickets.test.tsx",
    )


def test_workpacket_typecheck_package_command_derives_direct_tsc_plan(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    _write(package_dir / "package.json", json.dumps({"scripts": {"typecheck": "tsc -p . --noEmit"}}))
    node = tmp_path / "node"
    tsc = tmp_path / "tsc.js"
    _write(node, "")
    _write(tsc, "")
    command = "cd 2_products/pepper-agent/web && npm run typecheck"
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",),
    )
    work_packet = _workpacket_with_steps(
        _Step("V2", "Typecheck frontend.", "Typecheck passes.", command=command),
    )
    monkeypatch.setattr(tool, "_resolve_node_executable", lambda: node)
    monkeypatch.setattr(
        tool,
        "_resolve_node_module_entry",
        lambda _workspace, _package, entry: tsc if entry == "typescript/lib/tsc.js" else None,
    )

    specs = tool.build_governed_validation_command_specs(authority, work_packet)

    assert len(specs) == 1
    assert specs[0].source_command == command
    assert specs[0].effective_argv == (node.as_posix(), tsc.as_posix(), "-p", ".", "--noEmit")
    assert specs[0].execution_plan_SHA256


def test_workpacket_build_package_command_derives_sequential_tsc_vite_plan(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    _write(package_dir / "package.json", json.dumps({"scripts": {"build": "tsc -b && vite build"}}))
    node = tmp_path / "node"
    tsc = tmp_path / "tsc.js"
    vite = tmp_path / "vite.js"
    for path in (node, tsc, vite):
        _write(path, "")
    command = "cd 2_products/pepper-agent/web && npm run build"
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",),
    )
    work_packet = _workpacket_with_steps(
        _Step("V3", "Build frontend.", "Build passes.", command=command),
    )
    entries = {"typescript/lib/tsc.js": tsc, "vite/bin/vite.js": vite}
    monkeypatch.setattr(tool, "_resolve_node_executable", lambda: node)
    monkeypatch.setattr(
        tool,
        "_resolve_node_module_entry",
        lambda _workspace, _package, entry: entries.get(entry),
    )

    specs = tool.build_governed_validation_command_specs(authority, work_packet)

    assert len(specs) == 1
    spec = specs[0]
    assert spec.source_command == command
    assert len(spec.execution_plan) == 2
    assert tuple(spec.execution_plan[0]["effective_argv"]) == (node.as_posix(), tsc.as_posix(), "-b")
    assert tuple(spec.execution_plan[1]["effective_argv"]) == (node.as_posix(), vite.as_posix(), "build")
    assert spec.execution_plan[0]["package_script_SHA256"] == spec.execution_plan[1][
        "package_script_SHA256"
    ]


def test_workpacket_build_package_command_stops_after_first_segment_failure(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    _write(package_dir / "package.json", json.dumps({"scripts": {"build": "tsc -b && vite build"}}))
    node = tmp_path / "node"
    tsc = tmp_path / "tsc.js"
    vite = tmp_path / "vite.js"
    for path in (node, tsc, vite):
        _write(path, "")
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",),
    )
    work_packet = _workpacket_with_steps(
        _Step("V3", "Build frontend.", "Build passes.", command="cd 2_products/pepper-agent/web && npm run build"),
    )
    entries = {"typescript/lib/tsc.js": tsc, "vite/bin/vite.js": vite}
    monkeypatch.setattr(tool, "_resolve_node_executable", lambda: node)
    monkeypatch.setattr(
        tool,
        "_resolve_node_module_entry",
        lambda _workspace, _package, entry: entries.get(entry),
    )
    spec = tool.build_governed_validation_command_specs(authority, work_packet)[0]

    from hermes_cli.agent_platform.work_packet import validation_command_runner as vcr

    calls = []

    def fake_popen(*args, **kwargs):
        calls.append((args, kwargs))
        return _FakeProcess(code=1)

    monkeypatch.setattr(vcr.subprocess, "Popen", fake_popen)

    result = json.loads(tool._run_command(authority, spec))

    assert result["success"] is False
    assert result["completed_subcommand_count"] == 1
    assert result["subcommand_count"] == 2
    assert len(calls) == 1
    assert calls[0][0][0] == (node.as_posix(), tsc.as_posix(), "-b")


def test_workpacket_package_script_drift_blocks_before_process_start(
    tmp_path,
    monkeypatch,
) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    package_json = package_dir / "package.json"
    _write(package_json, json.dumps({"scripts": {"typecheck": "tsc -p . --noEmit"}}))
    node = tmp_path / "node"
    tsc = tmp_path / "tsc.js"
    _write(node, "")
    _write(tsc, "")
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",),
    )
    work_packet = _workpacket_with_steps(
        _Step("V2", "Typecheck frontend.", "Typecheck passes.", command="cd 2_products/pepper-agent/web && npm run typecheck"),
    )
    monkeypatch.setattr(tool, "_resolve_node_executable", lambda: node)
    monkeypatch.setattr(
        tool,
        "_resolve_node_module_entry",
        lambda _workspace, _package, entry: tsc if entry == "typescript/lib/tsc.js" else None,
    )
    spec = tool.build_governed_validation_command_specs(authority, work_packet)[0]
    _write(package_json, json.dumps({"scripts": {"typecheck": "tsc -p ."}}))
    monkeypatch.setattr(
        tool,
        "_run_launch_payload",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("drift ran")),
    )

    result = json.loads(tool._run_command(authority, spec))

    assert result["error_code"] == tool.WORKPACKET_VALIDATION_SCRIPT_IDENTITY_DRIFT
    assert result["process_started"] is False


@pytest.mark.parametrize(
    "command",
    [
        "cd /tmp/example && npm run test",
        "cd C:/temp/example && npm run test",
        "cd ../escape && npm run test",
        "cd 2_products/pepper-agent/web/../escape && npm run test",
        "cd ./2_products/pepper-agent/web && npm run test",
        "cd 2_products/pepper-agent/web && npm run test -- $(pwd)",
        "cd 2_products/pepper-agent/web && npm run test -- src/a.test.ts > out.txt",
        "cd 2_products/pepper-agent/web && npm run test -- src/a.test.ts | cat",
        "cd 2_products/pepper-agent/web && npm run test; git status",
        "cd 2_products/pepper-agent/web && FOO=bar npm run test",
        "cd 2_products/pepper-agent/web && npm install",
        "cd 2_products/pepper-agent/web && npm exec vite",
        "cd 2_products/pepper-agent/web && npx eslint .",
        "cd 2_products/pepper-agent/web && pnpm test",
        "cd 2_products/pepper-agent/web && npm run unknown",
    ],
)
def test_workpacket_package_command_negative_matrix_denied(tmp_path, command) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    _write(package_dir / "package.json", json.dumps({"scripts": {"test": "vitest run"}}))
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/projects-tickets/**",),
    )
    work_packet = _workpacket_with_steps(
        _Step("V1", "Run package command.", "The command is safe.", command=command),
    )

    assert tool.build_governed_validation_command_specs(authority, work_packet) == ()


def test_frontend_package_script_must_be_safe_vitest_run(tmp_path) -> None:
    workspace = tmp_path / "workspace"
    package_dir = workspace / "2_products/pepper-agent/web"
    _write(package_dir / "package.json", json.dumps({"scripts": {"test": "vitest run && git status"}}))
    _write(
        workspace / "2_products/pepper-agent/web/src/agent-platform/extensions.test.ts",
        "test('synthetic', () => {})\n",
    )
    authority = _authority(
        workspace,
        allowed_paths=("2_products/pepper-agent/web/src/agent-platform/extensions.test.ts",),
    )
    work_packet = _workpacket_with_steps(
        _Step(
            "V2",
            "Focused frontend tests.",
            "The focused frontend tests pass.",
            command="cd 2_products/pepper-agent/web && npm run test -- src/agent-platform/extensions.test.ts",
        )
    )

    specs = tool.build_governed_validation_command_specs(authority, work_packet)

    assert specs == ()


def test_pepper_validation_toolset_is_not_a_core_terminal_surface() -> None:
    from toolsets import _HERMES_CORE_TOOLS, resolve_toolset

    assert resolve_toolset("pepper_validation") == ["workpacket_validation"]
    assert "workpacket_validation" not in _HERMES_CORE_TOOLS
    assert "terminal" not in resolve_toolset("pepper_validation")
    assert "process" not in resolve_toolset("pepper_validation")


def test_model_tools_auto_adds_validation_toolset_only_for_governed_workers(
    monkeypatch,
) -> None:
    import model_tools

    captured: list[set[str]] = []

    def fake_get_definitions(tool_names, quiet=False):
        _ = quiet
        captured.append(set(tool_names))
        return []

    monkeypatch.setattr(model_tools.registry, "get_definitions", fake_get_definitions)
    monkeypatch.delenv(file_guard.GOVERNED_WORKER_ENV, raising=False)

    model_tools._compute_tool_definitions(
        enabled_toolsets=["pepper_repository", "file"],
        quiet_mode=True,
        skip_tool_search_assembly=True,
    )

    assert "workpacket_validation" not in captured[-1]

    monkeypatch.setenv(file_guard.GOVERNED_WORKER_ENV, file_guard.GOVERNED_WORKER_MODE)
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_WORKPACKET_ID", "WP-P18-9-1-R0001-123456789abc")
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_WORKPACKET_SHA256", "a" * 64)

    model_tools._compute_tool_definitions(
        enabled_toolsets=["pepper_repository", "file"],
        quiet_mode=True,
        skip_tool_search_assembly=True,
    )

    assert "workpacket_validation" in captured[-1]
    assert "terminal" not in captured[-1]
    assert "process" not in captured[-1]


def test_governed_worker_exposes_validation_schema_when_authority_is_unavailable(
    monkeypatch,
) -> None:
    import model_tools
    from tools.registry import invalidate_check_fn_cache

    monkeypatch.setenv(file_guard.GOVERNED_WORKER_ENV, file_guard.GOVERNED_WORKER_MODE)
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_WORKPACKET_ID", "WP-P18-9-1-R0001-123456789abc")
    monkeypatch.setenv("HERMES_AGENT_PLATFORM_WORKPACKET_SHA256", "a" * 64)
    monkeypatch.delenv(file_guard.GENERATION_RECORD_PATH_ENV, raising=False)
    model_tools._clear_tool_defs_cache()
    invalidate_check_fn_cache()

    try:
        definitions = model_tools.get_tool_definitions(
            enabled_toolsets=["pepper_validation"],
            quiet_mode=True,
            skip_tool_search_assembly=True,
        )
    finally:
        model_tools._clear_tool_defs_cache()
        invalidate_check_fn_cache()

    assert {definition["function"]["name"] for definition in definitions} == {
        "workpacket_validation"
    }

    result = json.loads(tool.registry.dispatch("workpacket_validation", {"action": "list"}))
    assert result["error_code"] == tool.WORKPACKET_VALIDATION_AUTHORITY_UNAVAILABLE
