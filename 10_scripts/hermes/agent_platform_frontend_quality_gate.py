#!/usr/bin/env python3
"""Bounded, evidence-preserving frontend quality gate for Hermes P13.8."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO, Iterable


SCHEMA_VERSION = 1
GATE_ID = "P13.8"
LANE_ORDER = ("test", "typecheck", "lint", "build", "dashboard", "browser")
COMMAND_LANES = LANE_ORDER[:4]
IS_WINDOWS = os.name == "nt"
POSIX_SIGKILL = getattr(signal, "SIGKILL", signal.SIGTERM)
MAX_READY_FILE_BYTES = 4096
DEFAULT_MAX_LOG_BYTES = 2_000_000

REGISTER_HEADERS = (
    "modification_id",
    "path",
    "change_class",
    "owner_ticket",
    "baseline_upstream_commit",
    "baseline_source_object_or_none",
    "baseline_source_sha256_or_none",
    "current_product_sha256_or_none",
    "intent",
    "reapplication_predicate",
    "conflict_owner",
    "security_or_compatibility_impact",
    "validation_lane_ids",
    "upstream_disposition",
    "rollback_target",
    "retirement_condition",
    "approval_reference",
    "status",
)

PRODUCT_EXTENSION_IDS = (
    "agent_platform.ui.overview",
    "agent_platform.ui.projects",
    "agent_platform.ui.project_detail",
    "agent_platform.ui.ticket_detail",
    "agent_platform.ui.approvals",
    "agent_platform.ui.approval_detail",
    "agent_platform.ui.executions",
    "agent_platform.ui.execution_detail",
    "agent_platform.ui.settings",
)


class QualityGateError(RuntimeError):
    """Raised when a gate invariant cannot be evaluated safely."""


@dataclass(frozen=True, slots=True)
class BrowserScenario:
    """One local dashboard deep-link and viewport contract."""

    name: str
    path: str
    required_text: tuple[str, ...]
    viewport_width: int = 1440
    viewport_height: int = 900
    check_mobile_navigation: bool = False


DEFAULT_BROWSER_SCENARIOS = (
    BrowserScenario(
        "overview-desktop",
        "/agent-platform/overview?profile=default",
        ("Runtime Overview",),
    ),
    BrowserScenario(
        "projects-desktop",
        "/agent-platform/projects?profile=default",
        ("Projects",),
    ),
    BrowserScenario(
        "project-detail-desktop",
        "/agent-platform/projects/quality-gate-board?profile=default",
        ("Project",),
    ),
    BrowserScenario(
        "ticket-detail-desktop",
        "/agent-platform/projects/quality-gate-board/tickets/quality-gate-task?profile=default",
        ("Ticket",),
    ),
    BrowserScenario(
        "approvals-desktop",
        "/agent-platform/approvals?profile=default",
        ("Approval Inbox",),
    ),
    BrowserScenario(
        "approval-detail-desktop",
        "/agent-platform/approvals/quality-gate-approval?profile=default",
        ("Approval",),
    ),
    BrowserScenario(
        "executions-desktop",
        "/agent-platform/executions?profile=default&board=quality-gate-board&task=quality-gate-task",
        ("Executions",),
    ),
    BrowserScenario(
        "execution-detail-desktop",
        "/agent-platform/executions/quality-gate-run?profile=default&board=quality-gate-board&task=quality-gate-task",
        ("Execution",),
    ),
    BrowserScenario(
        "settings-desktop",
        "/agent-platform/settings?profile=default",
        ("Safe Settings",),
    ),
    BrowserScenario(
        "overview-mobile",
        "/agent-platform/overview?profile=default",
        ("Runtime Overview",),
        viewport_width=390,
        viewport_height=844,
    ),
)


@dataclass(frozen=True, slots=True)
class GateConfig:
    """Configuration for one governed quality-gate run."""

    repo_root: Path
    result_path: Path
    artifact_dir: Path | None = None
    lanes: tuple[str, ...] = LANE_ORDER
    browser_scenarios: tuple[BrowserScenario, ...] = DEFAULT_BROWSER_SCENARIOS
    command_timeout_seconds: float = 600.0
    dashboard_timeout_seconds: float = 90.0
    browser_timeout_seconds: float = 45.0
    cleanup_timeout_seconds: float = 10.0
    total_timeout_seconds: float = 2400.0
    max_log_bytes: int = DEFAULT_MAX_LOG_BYTES
    browser_executable: Path | None = None
    python_executable: Path | None = None


@dataclass(slots=True)
class _StreamCapture:
    stream: BinaryIO
    path: Path
    limit: int
    total_bytes: int = 0
    retained_bytes: int = 0
    digest: str = ""
    _thread: threading.Thread = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        hasher = hashlib.sha256()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.path.open("wb") as handle:
                while True:
                    chunk = self.stream.read(65536)
                    if not chunk:
                        break
                    hasher.update(chunk)
                    self.total_bytes += len(chunk)
                    remaining = self.limit - self.retained_bytes
                    if remaining > 0:
                        retained = chunk[:remaining]
                        handle.write(retained)
                        self.retained_bytes += len(retained)
        except (OSError, ValueError):
            pass
        finally:
            try:
                self.stream.close()
            except OSError:
                pass
        self.digest = hasher.hexdigest()

    def finish(self, timeout: float = 2.0) -> dict[str, Any]:
        self._thread.join(timeout=max(0.0, timeout))
        if self._thread.is_alive():
            try:
                self.stream.close()
            except OSError:
                pass
            self._thread.join(timeout=1.0)
        if not self.path.exists():
            self.path.write_bytes(b"")
        if not self.digest:
            self.digest = hashlib.sha256(b"").hexdigest()
        return {
            "sha256": self.digest,
            "total_bytes": self.total_bytes,
            "retained_bytes": self.retained_bytes,
            "truncated": self.total_bytes > self.retained_bytes,
            "artifact": self.path.name,
        }


@dataclass(slots=True)
class _OwnedProcess:
    process: subprocess.Popen[bytes]
    stdout: _StreamCapture
    stderr: _StreamCapture

    def finish_captures(self) -> dict[str, Any]:
        return {
            "stdout": self.stdout.finish(),
            "stderr": self.stderr.finish(),
        }


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(
            json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _safe_error(error: BaseException, replacements: Iterable[Path] = ()) -> str:
    text = f"{type(error).__name__}: {error}"
    for path in replacements:
        raw = str(path)
        if raw:
            text = text.replace(raw, "<path>")
            text = text.replace(raw.replace("\\", "/"), "<path>")
    text = re.sub(r"wss?://[^\s\"']+", "<redacted-cdp-url>", text)
    text = re.sub(
        r"(?i)(token|secret|password|api[_-]?key)=([^&\s]+)",
        r"\1=<redacted>",
        text,
    )
    return text[:500]


def _validate_scenario(scenario: BrowserScenario) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", scenario.name):
        raise QualityGateError(f"Invalid browser scenario name: {scenario.name!r}")
    parsed = urllib.parse.urlsplit(scenario.path)
    if (
        parsed.scheme
        or parsed.netloc
        or parsed.fragment
        or not parsed.path.startswith("/")
        or parsed.path.startswith("//")
        or "\\" in scenario.path
        or any(ord(char) < 32 for char in scenario.path)
    ):
        raise QualityGateError(
            f"Browser scenario {scenario.name!r} must use a local absolute path"
        )
    sensitive_query_names = {
        "api_key",
        "apikey",
        "auth",
        "authorization",
        "credential",
        "key",
        "password",
        "secret",
        "token",
    }
    if any(
        name.lower().replace("-", "_") in sensitive_query_names
        or any(
            marker in name.lower().replace("-", "_")
            for marker in (
                "api_key",
                "authorization",
                "credential",
                "password",
                "secret",
                "token",
            )
        )
        for name, _ in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    ):
        raise QualityGateError(
            f"Browser scenario {scenario.name!r} cannot contain credential-like query fields"
        )
    if not 240 <= scenario.viewport_width <= 3840:
        raise QualityGateError(f"Invalid viewport width for {scenario.name!r}")
    if not 320 <= scenario.viewport_height <= 2160:
        raise QualityGateError(f"Invalid viewport height for {scenario.name!r}")
    if not scenario.required_text or any(
        not text or len(text) > 200 for text in scenario.required_text
    ):
        raise QualityGateError(f"Invalid required text for {scenario.name!r}")


def _validate_config(config: GateConfig) -> tuple[Path, Path]:
    repo_root = config.repo_root.resolve()
    product_root = repo_root / "2_products" / "pepper-agent"
    required = (
        product_root / "web" / "package.json",
        product_root / "AGENT_PLATFORM_MODIFICATIONS.tsv",
        product_root / "hermes_cli" / "main.py",
    )
    missing = [path for path in required if not path.is_file()]
    if missing:
        raise QualityGateError("Repository does not contain the governed Hermes inputs")
    if not config.lanes:
        raise QualityGateError("At least one fixed lane must be selected")
    if len(config.lanes) != len(set(config.lanes)):
        raise QualityGateError("Lane IDs must be unique")
    unknown = sorted(set(config.lanes) - set(LANE_ORDER))
    if unknown:
        raise QualityGateError(f"Unknown fixed lane IDs: {', '.join(unknown)}")
    if "browser" in config.lanes and "dashboard" not in config.lanes:
        raise QualityGateError("The browser lane requires the dashboard lane")
    if "dashboard" in config.lanes and "build" not in config.lanes:
        raise QualityGateError("The dashboard lane requires the build lane")
    names = [scenario.name for scenario in config.browser_scenarios]
    if len(names) != len(set(names)):
        raise QualityGateError("Browser scenario names must be unique")
    for scenario in config.browser_scenarios:
        _validate_scenario(scenario)
    for value in (
        config.command_timeout_seconds,
        config.dashboard_timeout_seconds,
        config.browser_timeout_seconds,
        config.cleanup_timeout_seconds,
        config.total_timeout_seconds,
    ):
        if value <= 0:
            raise QualityGateError("All timeout values must be positive")
    if config.max_log_bytes < 1024:
        raise QualityGateError("max_log_bytes must be at least 1024")
    return repo_root, product_root


def _isolated_environment(runtime_root: Path) -> dict[str, str]:
    safe_names = {
        "COMSPEC",
        "NUMBER_OF_PROCESSORS",
        "OS",
        "PATH",
        "PATHEXT",
        "PROCESSOR_ARCHITECTURE",
        "PROGRAMFILES",
        "PROGRAMFILES(X86)",
        "PROGRAMW6432",
        "SYSTEMDRIVE",
        "SYSTEMROOT",
        "WINDIR",
    }
    env = {
        name: value for name, value in os.environ.items() if name.upper() in safe_names
    }
    home = runtime_root / "home"
    temp = runtime_root / "temp"
    appdata = home / "AppData" / "Roaming"
    local_appdata = home / "AppData" / "Local"
    for path in (home, temp, appdata, local_appdata):
        path.mkdir(parents=True, exist_ok=True)
    env.update(
        {
            "APPDATA": str(appdata),
            "CI": "1",
            "HERMES_HOME": str(home / ".hermes"),
            "HOME": str(home),
            "LOCALAPPDATA": str(local_appdata),
            "NO_COLOR": "1",
            "NPM_CONFIG_AUDIT": "false",
            "NPM_CONFIG_FUND": "false",
            "NPM_CONFIG_OFFLINE": "true",
            "NPM_CONFIG_UPDATE_NOTIFIER": "false",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "TEMP": str(temp),
            "TMP": str(temp),
            "TZ": "UTC",
            "USERPROFILE": str(home),
        }
    )
    return env


def _resolve_node_npm() -> tuple[Path, Path]:
    node_raw = shutil.which("node")
    if not node_raw:
        raise QualityGateError(
            "Node.js was not found; dependency installation is disabled"
        )
    node = Path(node_raw).resolve()
    npm_raw = shutil.which("npm")
    candidates = [
        node.parent / "node_modules" / "npm" / "bin" / "npm-cli.js",
        node.parent.parent / "lib" / "node_modules" / "npm" / "bin" / "npm-cli.js",
        node.parent.parent / "share" / "nodejs" / "npm" / "bin" / "npm-cli.js",
    ]
    if npm_raw:
        npm = Path(npm_raw).resolve()
        if npm.suffix.lower() in {".js", ".mjs"}:
            candidates.insert(0, npm)
        candidates.extend(
            [
                npm.parent / "node_modules" / "npm" / "bin" / "npm-cli.js",
                npm.parent.parent / "node_modules" / "npm" / "bin" / "npm-cli.js",
            ]
        )
    npm_cli = next((candidate for candidate in candidates if candidate.is_file()), None)
    if npm_cli is None:
        raise QualityGateError(
            "npm-cli.js was not found; the gate will not invoke a shell or npm.cmd"
        )
    return node, npm_cli.resolve()


def _lane_command(lane: str, product_root: Path) -> tuple[list[str], list[str], Path]:
    if lane not in COMMAND_LANES:
        raise QualityGateError(f"No fixed command exists for lane {lane!r}")
    node, npm_cli = _resolve_node_npm()
    if lane == "lint":
        eslint = product_root / "node_modules" / "eslint" / "bin" / "eslint.js"
        if not eslint.is_file():
            raise QualityGateError(
                "The installed ESLint entry point is missing; dependency installation is disabled"
            )
        return (
            [str(node), str(eslint), "src/agent-platform"],
            ["<node>", "<eslint.js>", "src/agent-platform"],
            product_root / "web",
        )
    script = {
        "test": "test",
        "typecheck": "typecheck",
        "build": "build",
    }[lane]
    argv = [str(node), str(npm_cli), "run", script]
    evidence_argv = ["<node>", "<npm-cli.js>", "run", script]
    return argv, evidence_argv, product_root / "web"


def _spawn_owned_process(
    argv: list[str],
    cwd: Path,
    env: dict[str, str],
    stdout_path: Path,
    stderr_path: Path,
    max_log_bytes: int,
) -> _OwnedProcess:
    kwargs: dict[str, Any] = {}
    if IS_WINDOWS:
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    else:
        kwargs["start_new_session"] = True
    process = subprocess.Popen(
        argv,
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        **kwargs,
    )
    assert process.stdout is not None and process.stderr is not None
    return _OwnedProcess(
        process,
        _StreamCapture(process.stdout, stdout_path, max_log_bytes),
        _StreamCapture(process.stderr, stderr_path, max_log_bytes),
    )


def _terminate_process_tree(
    process: subprocess.Popen[Any], timeout_seconds: float
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "requested": False,
        "method": "already-exited",
        "exited": process.poll() is not None,
    }
    if record["exited"]:
        return record
    record["requested"] = True
    if IS_WINDOWS:
        record["method"] = "taskkill-tree-force"
        try:
            completed = subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=timeout_seconds,
            )
            record["tree_kill_exit_code"] = completed.returncode
        except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
            record["tree_kill_exit_code"] = None
    else:
        record["method"] = "posix-process-group"
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError, OSError):
            pass
    grace = max(0.1, timeout_seconds / 2)
    try:
        process.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        if IS_WINDOWS:
            try:
                process.kill()
            except OSError:
                pass
        else:
            try:
                os.killpg(process.pid, POSIX_SIGKILL)
                record["escalated"] = True
            except (ProcessLookupError, PermissionError, OSError):
                pass
        try:
            process.wait(timeout=max(0.1, timeout_seconds - grace))
        except subprocess.TimeoutExpired:
            pass
    record["exited"] = process.poll() is not None
    return record


def _run_command_lane(
    lane: str,
    product_root: Path,
    env: dict[str, str],
    artifact_dir: Path,
    timeout_seconds: float,
    max_log_bytes: int,
) -> dict[str, Any]:
    started = time.monotonic()
    record: dict[str, Any] = {
        "lane": lane,
        "status": "failed",
        "cwd": "2_products/pepper-agent/web",
        "timeout_seconds": timeout_seconds,
    }
    try:
        argv, evidence_argv, cwd = _lane_command(lane, product_root)
        record["argv"] = evidence_argv
        owned = _spawn_owned_process(
            argv,
            cwd,
            env,
            artifact_dir / f"{lane}-stdout.log",
            artifact_dir / f"{lane}-stderr.log",
            max_log_bytes,
        )
    except Exception as error:
        record["failure"] = "spawn_failed"
        record["error"] = _safe_error(error, (product_root,))
        record["duration_seconds"] = time.monotonic() - started
        return record
    timed_out = False
    cleanup: dict[str, Any] | None = None
    try:
        return_code = owned.process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        cleanup = _terminate_process_tree(owned.process, min(10.0, timeout_seconds))
        return_code = owned.process.poll()
    record.update(
        {
            "duration_seconds": time.monotonic() - started,
            "exit_code": return_code,
            "timed_out": timed_out,
            "status": "passed" if return_code == 0 and not timed_out else "failed",
            "logs": owned.finish_captures(),
        }
    )
    if cleanup is not None:
        record["cleanup"] = cleanup
    if timed_out:
        record["failure"] = "timeout"
    elif return_code != 0:
        record["failure"] = "nonzero_exit"
    return record


def _register_owned_candidates(product_root: Path) -> set[str]:
    candidates: set[str] = set()
    roots = (
        product_root / "hermes_cli" / "agent_platform",
        product_root / "web" / "src" / "agent-platform",
    )
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                candidates.add(path.relative_to(product_root).as_posix())
    tests_root = product_root / "tests" / "hermes_cli"
    if tests_root.exists():
        for path in tests_root.glob("test_agent_platform*.py"):
            if path.is_file():
                candidates.add(path.relative_to(product_root).as_posix())
    return candidates


def _reconcile_modification_register(product_root: Path) -> dict[str, Any]:
    register = product_root / "AGENT_PLATFORM_MODIFICATIONS.tsv"
    with register.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != REGISTER_HEADERS:
            raise QualityGateError(
                "Modification register columns do not match the contract"
            )
        rows = list(reader)
    if not rows:
        raise QualityGateError("Modification register is empty")
    ids: set[str] = set()
    paths: set[str] = set()
    product_owned = 0
    upstream_derived = 0
    normalized_rows: list[dict[str, str]] = []
    root = product_root.resolve()
    for row in rows:
        if None in row or any(value is None or value == "" for value in row.values()):
            raise QualityGateError("Modification register contains a missing field")
        modification_id = row["modification_id"]
        relative = row["path"]
        if modification_id in ids or relative in paths:
            raise QualityGateError(
                "Modification register contains a duplicate ID or path"
            )
        ids.add(modification_id)
        paths.add(relative)
        if (
            relative.startswith(("/", "\\"))
            or "\\" in relative
            or any(part in {"", ".", ".."} for part in relative.split("/"))
        ):
            raise QualityGateError("Modification register contains a noncanonical path")
        target = (product_root / relative).resolve()
        if (
            (product_root / relative).is_symlink()
            or not target.is_relative_to(root)
            or not target.is_file()
        ):
            raise QualityGateError(f"Registered product path is missing: {relative}")
        if not re.fullmatch(r"[0-9a-f]{40}", row["baseline_upstream_commit"]):
            raise QualityGateError(f"Registered upstream commit is invalid: {relative}")
        expected_hash = row["current_product_sha256_or_none"]
        if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise QualityGateError(f"Registered product hash is invalid: {relative}")
        if _sha256_file(target) != expected_hash:
            raise QualityGateError(f"Modification register hash mismatch: {relative}")
        change_class = row["change_class"]
        if change_class == "AGENT_PLATFORM_product_addition":
            product_owned += 1
            if (
                row["baseline_source_object_or_none"] != "none"
                or row["baseline_source_sha256_or_none"] != "none"
                or row["upstream_disposition"] != "retain_product_divergence"
            ):
                raise QualityGateError(
                    f"Product-owned classification is inconsistent: {relative}"
                )
        elif change_class == "AGENT_PLATFORM_product_modification":
            upstream_derived += 1
            if (
                not re.fullmatch(r"[0-9a-f]{40}", row["baseline_source_object_or_none"])
                or not re.fullmatch(
                    r"[0-9a-f]{64}", row["baseline_source_sha256_or_none"]
                )
                or row["upstream_disposition"] != "reapply_product_integration"
            ):
                raise QualityGateError(
                    f"Upstream-derived classification is inconsistent: {relative}"
                )
        else:
            raise QualityGateError(f"Unknown modification class: {change_class}")
        normalized_rows.append({header: row[header] for header in REGISTER_HEADERS})
    unregistered = _register_owned_candidates(product_root) - paths
    if unregistered:
        raise QualityGateError(
            f"Product-owned source is absent from the modification register: {sorted(unregistered)[0]}"
        )
    return {
        "status": "passed",
        "rows": len(rows),
        "columns": len(REGISTER_HEADERS),
        "product_owned_additions": product_owned,
        "upstream_derived_modifications": upstream_derived,
        "duplicate_ids": 0,
        "duplicate_paths": 0,
        "missing_fields": 0,
        "hash_mismatches": 0,
        "register_sha256": _sha256_file(register),
        "normalized_rows_sha256": _canonical_hash(normalized_rows),
    }


def _resolve_python(config: GateConfig, product_root: Path) -> Path:
    if config.python_executable is not None:
        candidate = config.python_executable.resolve()
        if not candidate.is_file():
            raise QualityGateError("Configured Python executable does not exist")
        return candidate
    candidates = (
        product_root / ".venv" / ("Scripts/python.exe" if IS_WINDOWS else "bin/python"),
        product_root / "venv" / ("Scripts/python.exe" if IS_WINDOWS else "bin/python"),
        Path(sys.executable),
    )
    candidate = next((path.resolve() for path in candidates if path.is_file()), None)
    if candidate is None:
        raise QualityGateError("No Python interpreter is available for the dashboard")
    return candidate


def _read_ready_port(path: Path) -> int:
    if not path.is_file() or path.stat().st_size > MAX_READY_FILE_BYTES:
        raise QualityGateError("Dashboard ready file is missing or oversized")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise QualityGateError("Dashboard ready file is not valid JSON") from error
    if not isinstance(payload, dict) or set(payload) != {"port"}:
        raise QualityGateError("Dashboard ready file has an unexpected shape")
    port = payload["port"]
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise QualityGateError("Dashboard ready file contains an invalid port")
    return port


def _wait_dashboard_ready(
    process: subprocess.Popen[Any], ready_file: Path, timeout_seconds: float
) -> tuple[int, float]:
    started = time.monotonic()
    deadline = started + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise QualityGateError("Dashboard exited before publishing readiness")
        if ready_file.exists():
            try:
                return _read_ready_port(ready_file), time.monotonic() - started
            except QualityGateError as error:
                last_error = error
        time.sleep(0.05)
    if last_error is not None:
        raise QualityGateError(str(last_error))
    raise QualityGateError("Dashboard readiness timed out")


def _http_json(
    url: str,
    timeout_seconds: float,
    headers: dict[str, str] | None = None,
) -> tuple[int, Any]:
    request = urllib.request.Request(url, headers=headers or {})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            body = response.read(1_000_001)
            if len(body) > 1_000_000:
                raise QualityGateError(
                    "Dashboard probe response exceeded its size bound"
                )
            return int(response.status), json.loads(body.decode("utf-8"))
    except urllib.error.HTTPError as error:
        return int(error.code), None


def _http_status(url: str, timeout_seconds: float) -> int:
    request = urllib.request.Request(url)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            response.read(1024)
            return int(response.status)
    except urllib.error.HTTPError as error:
        return int(error.code)


def _probe_dashboard(
    port: int, session_token: str, timeout_seconds: float
) -> dict[str, Any]:
    root = f"http://127.0.0.1:{port}"
    status_code, status_payload = _http_json(f"{root}/api/status", timeout_seconds)
    config_url = f"{root}/api/agent-platform/product-configuration"
    config_code, config_payload = _http_json(
        config_url,
        timeout_seconds,
        {"X-Hermes-Session-Token": session_token},
    )
    unauthenticated_code = _http_status(config_url, timeout_seconds)
    expected_keys = {
        "schema_version",
        "product_id",
        "product_display_name",
        "product_version",
        "upstream_product_name",
        "upstream_version",
        "upstream_commit",
        "feature_flags",
        "extension_modules",
        "documentation_url",
        "support_url",
    }
    provider_null = (
        isinstance(status_payload, dict)
        and isinstance(config_payload, dict)
        and set(config_payload) == expected_keys
        and config_payload.get("feature_flags", {}).get("agent_platform.product_ui")
        == "disabled"
        and config_payload.get("extension_modules") == []
    )
    result = {
        "status_http": status_code,
        "root_http": _http_status(root, timeout_seconds),
        "product_configuration_http": config_code,
        "unauthenticated_product_configuration_http": unauthenticated_code,
        "provider_null_configuration": provider_null,
    }
    result["passed"] = (
        result["status_http"] == 200
        and result["root_http"] == 200
        and result["product_configuration_http"] == 200
        and result["unauthenticated_product_configuration_http"] == 401
        and provider_null
    )
    return result


def _start_dashboard(
    config: GateConfig,
    product_root: Path,
    env: dict[str, str],
    runtime_root: Path,
    artifact_dir: Path,
) -> tuple[_OwnedProcess | None, dict[str, Any], int | None]:
    started = time.monotonic()
    record: dict[str, Any] = {
        "lane": "dashboard",
        "status": "failed",
        "cwd": "2_products/pepper-agent",
        "argv": [
            "<python>",
            "-B",
            "-m",
            "hermes_cli.main",
            "dashboard",
            "--host",
            "127.0.0.1",
            "--port",
            "0",
            "--no-open",
            "--skip-build",
        ],
        "timeout_seconds": config.dashboard_timeout_seconds,
    }
    ready_file = runtime_root / "dashboard-ready.json"
    session_token = uuid.uuid4().hex + uuid.uuid4().hex
    dashboard_env = dict(env)
    dashboard_env["HERMES_DESKTOP_READY_FILE"] = str(ready_file)
    dashboard_env["HERMES_DASHBOARD_SESSION_TOKEN"] = session_token
    try:
        python = _resolve_python(config, product_root)
        owned = _spawn_owned_process(
            [
                str(python),
                "-B",
                "-m",
                "hermes_cli.main",
                "dashboard",
                "--host",
                "127.0.0.1",
                "--port",
                "0",
                "--no-open",
                "--skip-build",
            ],
            product_root,
            dashboard_env,
            artifact_dir / "dashboard-stdout.log",
            artifact_dir / "dashboard-stderr.log",
            config.max_log_bytes,
        )
        port, readiness_seconds = _wait_dashboard_ready(
            owned.process, ready_file, config.dashboard_timeout_seconds
        )
        probe = _probe_dashboard(
            port, session_token, min(5.0, config.dashboard_timeout_seconds)
        )
        record.update(
            {
                "status": "passed" if probe["passed"] else "failed",
                "readiness_seconds": readiness_seconds,
                "readiness": probe,
                "duration_seconds": time.monotonic() - started,
            }
        )
        if not probe["passed"]:
            record["failure"] = "readiness_probe_failed"
        return owned, record, port
    except Exception as error:
        record.update(
            {
                "failure": "startup_failed",
                "error": _safe_error(error, (product_root, runtime_root)),
                "duration_seconds": time.monotonic() - started,
            }
        )
        return locals().get("owned"), record, None


def _resolve_browser(config: GateConfig) -> Path:
    if config.browser_executable is not None:
        candidate = config.browser_executable.resolve()
        if not candidate.is_file():
            raise QualityGateError("Configured Chromium executable does not exist")
        return candidate
    system = platform.system()
    candidates: list[Path] = []
    names: tuple[str, ...]
    if system == "Windows":
        names = ("chrome.exe", "msedge.exe", "chromium.exe", "brave.exe")
        bases = (
            os.environ.get("ProgramFiles"),
            os.environ.get("ProgramFiles(x86)"),
            os.environ.get("LOCALAPPDATA"),
        )
        suffixes = (
            ("Google", "Chrome", "Application", "chrome.exe"),
            ("Microsoft", "Edge", "Application", "msedge.exe"),
            ("Chromium", "Application", "chrome.exe"),
            ("BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
        )
        for base in filter(None, bases):
            candidates.extend(Path(base).joinpath(*suffix) for suffix in suffixes)
    elif system == "Darwin":
        names = ("google-chrome", "chromium", "brave", "msedge")
        candidates.extend(
            Path(path)
            for path in (
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            )
        )
    else:
        names = (
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
            "microsoft-edge",
            "brave-browser",
        )
    for name in names:
        found = shutil.which(name)
        if found:
            candidates.insert(0, Path(found))
    candidate = next((path.resolve() for path in candidates if path.is_file()), None)
    if candidate is None:
        raise QualityGateError(
            "No Chromium-family browser was found; automatic installation is disabled"
        )
    return candidate


def _read_devtools_active_port(path: Path) -> tuple[int, str]:
    if not path.is_file() or path.stat().st_size > MAX_READY_FILE_BYTES:
        raise QualityGateError("DevToolsActivePort is missing or oversized")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        port = int(lines[0])
        websocket_path = lines[1]
    except (OSError, UnicodeError, ValueError, IndexError) as error:
        raise QualityGateError("DevToolsActivePort is malformed") from error
    if not 1 <= port <= 65535 or not websocket_path.startswith("/devtools/browser/"):
        raise QualityGateError("DevToolsActivePort contains invalid endpoint data")
    if any(char in websocket_path for char in ("?", "#", "@", "\\")):
        raise QualityGateError("DevToolsActivePort contains unsafe endpoint data")
    return port, websocket_path


def _wait_devtools_active_port(
    process: subprocess.Popen[Any], profile: Path, timeout_seconds: float
) -> tuple[int, str, float]:
    started = time.monotonic()
    deadline = started + timeout_seconds
    path = profile / "DevToolsActivePort"
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise QualityGateError("Chromium exited before CDP readiness")
        if path.exists():
            try:
                port, websocket_path = _read_devtools_active_port(path)
                return port, websocket_path, time.monotonic() - started
            except QualityGateError as error:
                last_error = error
        time.sleep(0.05)
    if last_error is not None:
        raise QualityGateError(str(last_error))
    raise QualityGateError("Chromium CDP readiness timed out")


def _connect_websocket(url: str, timeout_seconds: float) -> Any:
    try:
        from websockets.sync.client import connect
    except ImportError as error:
        raise QualityGateError(
            "Browser lane requires the declared websockets dependency; run with the Hermes product interpreter"
        ) from error
    return connect(url, open_timeout=timeout_seconds, close_timeout=2, max_size=2**20)


class _CDPClient:
    def __init__(self, websocket: Any, synthetic_configuration: dict[str, Any]):
        self.websocket = websocket
        self.synthetic_configuration = synthetic_configuration
        self.next_id = 0
        self.pending: dict[int, dict[str, Any]] = {}
        self.events = {
            "console_errors": 0,
            "local_network_console_errors": 0,
            "external_network_console_errors": 0,
            "expected_provider_null_auth_responses": 0,
            "page_errors": 0,
            "external_requests": 0,
            "resource_failures": 0,
        }
        self.local_network_error_paths: dict[str, int] = {}

    def command(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout_seconds: float = 10.0,
    ) -> dict[str, Any]:
        self.next_id += 1
        command_id = self.next_id
        message: dict[str, Any] = {
            "id": command_id,
            "method": method,
            "params": params or {},
        }
        if session_id is not None:
            message["sessionId"] = session_id
        self.websocket.send(json.dumps(message, separators=(",", ":")))
        return self._wait_response(command_id, time.monotonic() + timeout_seconds)

    def _wait_response(self, command_id: int, deadline: float) -> dict[str, Any]:
        while time.monotonic() < deadline:
            if command_id in self.pending:
                response = self.pending.pop(command_id)
            else:
                remaining = max(0.01, deadline - time.monotonic())
                try:
                    raw = self.websocket.recv(timeout=remaining)
                except TimeoutError as error:
                    raise QualityGateError("CDP command timed out") from error
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8")
                try:
                    response = json.loads(raw)
                except (TypeError, UnicodeError, json.JSONDecodeError) as error:
                    raise QualityGateError("CDP returned an invalid message") from error
                response_id = response.get("id")
                if isinstance(response_id, int):
                    if response_id != command_id:
                        self.pending[response_id] = response
                        continue
                else:
                    self._handle_event(response)
                    continue
            if "error" in response:
                error_code = response.get("error", {}).get("code", "unknown")
                raise QualityGateError(
                    f"CDP command {command_id} failed with code {error_code}"
                )
            result = response.get("result", {})
            if not isinstance(result, dict):
                raise QualityGateError("CDP command returned an invalid result")
            return result
        raise QualityGateError("CDP command timed out")

    def _handle_event(self, event: dict[str, Any]) -> None:
        method = event.get("method")
        params = event.get("params", {})
        session_id = event.get("sessionId")
        if method == "Fetch.requestPaused":
            request_id = params.get("requestId")
            request_url = params.get("request", {}).get("url", "")
            path = urllib.parse.urlsplit(request_url).path
            if path == "/api/agent-platform/product-configuration":
                payload = base64.b64encode(
                    json.dumps(
                        self.synthetic_configuration, separators=(",", ":")
                    ).encode("utf-8")
                ).decode("ascii")
                self.command(
                    "Fetch.fulfillRequest",
                    {
                        "requestId": request_id,
                        "responseCode": 200,
                        "responseHeaders": [
                            {"name": "Content-Type", "value": "application/json"},
                            {"name": "Cache-Control", "value": "no-store"},
                        ],
                        "body": payload,
                    },
                    session_id,
                )
            else:
                self.command(
                    "Fetch.continueRequest", {"requestId": request_id}, session_id
                )
            return
        if method == "Network.requestWillBeSent":
            url = str(params.get("request", {}).get("url", ""))
            parsed = urllib.parse.urlsplit(url)
            if parsed.scheme in {
                "http",
                "https",
                "ws",
                "wss",
            } and parsed.hostname not in {
                "127.0.0.1",
                "localhost",
                "::1",
            }:
                self.events["external_requests"] += 1
            return
        if method == "Network.loadingFailed" and params.get("type") in {
            "Document",
            "Script",
            "Stylesheet",
        }:
            self.events["resource_failures"] += 1
            return
        if method == "Runtime.consoleAPICalled" and params.get("type") in {
            "error",
            "assert",
        }:
            self.events["console_errors"] += 1
            return
        if (
            method == "Log.entryAdded"
            and params.get("entry", {}).get("level") == "error"
        ):
            entry = params.get("entry", {})
            if entry.get("source") == "network":
                parsed = urllib.parse.urlsplit(str(entry.get("url", "")))
                if (
                    parsed.hostname in {"127.0.0.1", "localhost", "::1"}
                    and parsed.path == "/api/auth/me"
                    and re.search(r"\b401\b", str(entry.get("text", "")))
                ):
                    self.events["expected_provider_null_auth_responses"] += 1
                    return
                counter = (
                    "local_network_console_errors"
                    if parsed.hostname in {"127.0.0.1", "localhost", "::1"}
                    else "external_network_console_errors"
                )
                self.events[counter] += 1
                if counter == "local_network_console_errors":
                    path = parsed.path
                    safe_path = (
                        path
                        if re.fullmatch(r"/[A-Za-z0-9._~!$&'()*+,;=:@%/-]{1,200}", path)
                        else "<other-local-path>"
                    )
                    self.local_network_error_paths[safe_path] = (
                        self.local_network_error_paths.get(safe_path, 0) + 1
                    )
            else:
                self.events["console_errors"] += 1
            return
        if method in {"Runtime.exceptionThrown", "Inspector.targetCrashed"}:
            self.events["page_errors"] += 1


def _evaluate(
    client: _CDPClient, session_id: str, expression: str, timeout_seconds: float = 10.0
) -> Any:
    result = client.command(
        "Runtime.evaluate",
        {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        },
        session_id,
        timeout_seconds,
    )
    if "exceptionDetails" in result:
        raise QualityGateError("Browser evaluation raised an exception")
    return result.get("result", {}).get("value")


def _page_state_expression(required_text: tuple[str, ...]) -> str:
    required = json.dumps(list(required_text), ensure_ascii=True)
    return f"""
        (() => {{
          const body = document.body?.innerText || "";
          const required = {required};
          return {{
            ready: document.readyState,
            rootPresent: Boolean(document.getElementById("root")),
            bodyLength: body.length,
            requiredPresent: required.every((text) => body.includes(text)),
            pathname: location.pathname,
            search: location.search,
            hash: location.hash,
          }};
        }})()
    """


def _wait_for_page(
    client: _CDPClient,
    session_id: str,
    required_text: tuple[str, ...],
    timeout_seconds: float,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    expression = _page_state_expression(required_text)
    last: Any = None
    while time.monotonic() < deadline:
        last = _evaluate(client, session_id, expression, min(5.0, timeout_seconds))
        if (
            isinstance(last, dict)
            and last.get("ready") in {"interactive", "complete"}
            and last.get("rootPresent")
            and last.get("bodyLength", 0) > 0
            and last.get("requiredPresent")
        ):
            time.sleep(0.2)
            _evaluate(client, session_id, "0", min(5.0, timeout_seconds))
            return last
        time.sleep(0.1)
    raise QualityGateError("Browser page did not reach its bounded content contract")


_SEMANTICS_EXPRESSION = r"""
    (() => {
      const visible = (element) => {
        const style = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
      };
      const mains = [...document.querySelectorAll("main")].filter(visible);
      const scope = mains[mains.length - 1] || document.body;
      const name = (element) => {
        const labelledBy = element.getAttribute("aria-labelledby");
        const labelled = labelledBy ? labelledBy.split(/\s+/).map((id) => document.getElementById(id)?.textContent || "").join(" ") : "";
        return (element.getAttribute("aria-label") || labelled || element.textContent || element.getAttribute("title") || "").trim();
      };
      const controls = [...scope.querySelectorAll("button, a[href], input, select, textarea")].filter(visible);
      const images = [...scope.querySelectorAll("img")].filter(visible);
      const ids = [...document.querySelectorAll("[id]")].map((element) => element.id);
      const dialogs = [...document.querySelectorAll('[role="dialog"], dialog[open]')].filter(visible);
      const text = scope.innerText || "";
      return {
        documentLanguage: Boolean(document.documentElement.lang.trim()),
        visibleMainCount: mains.length,
        nestedMainCount: document.querySelectorAll("main main").length,
        scopedH1Count: [...scope.querySelectorAll("h1")].filter(visible).length,
        controlsWithoutName: controls.filter((element) => !name(element) && !(element.labels && element.labels.length)).length,
        imagesWithoutAlt: images.filter((element) => !element.hasAttribute("alt")).length,
        duplicateIds: ids.length - new Set(ids).size,
        dialogsWithoutName: dialogs.filter((element) => !name(element)).length,
        dialogsWithoutModal: dialogs.filter((element) => element.getAttribute("aria-modal") !== "true").length,
        horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
        secretLikeText: /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk-[A-Za-z0-9_-]{16,}\b|\bBearer\s+[A-Za-z0-9._~-]{16,}\b/i.test(text),
      };
    })()
"""


def _semantics_checks(
    client: _CDPClient, session_id: str, mobile: bool
) -> dict[str, Any]:
    audit = _evaluate(client, session_id, _SEMANTICS_EXPRESSION)
    if not isinstance(audit, dict):
        raise QualityGateError("Browser semantics audit returned invalid data")
    violations: dict[str, int | bool] = {}
    zero_fields = (
        "nestedMainCount",
        "controlsWithoutName",
        "imagesWithoutAlt",
        "duplicateIds",
        "dialogsWithoutName",
        "dialogsWithoutModal",
    )
    for name in zero_fields:
        value = audit.get(name)
        if isinstance(value, int) and value != 0:
            violations[name] = value
    if not audit.get("documentLanguage"):
        violations["documentLanguage"] = False
    if audit.get("visibleMainCount", 0) < 1:
        violations["visibleMainCount"] = int(audit.get("visibleMainCount", 0))
    if audit.get("scopedH1Count") != 1:
        violations["scopedH1Count"] = int(audit.get("scopedH1Count", 0))
    if mobile and audit.get("horizontalOverflow"):
        violations["horizontalOverflow"] = True
    if audit.get("secretLikeText"):
        violations["secretLikeText"] = True
    return {"passed": not violations, "violations": violations, "audit": audit}


def _keyboard_check(client: _CDPClient, session_id: str) -> dict[str, Any]:
    _evaluate(
        client,
        session_id,
        "document.activeElement instanceof HTMLElement && document.activeElement.blur(); true",
    )
    client.command(
        "Input.dispatchKeyEvent",
        {"type": "keyDown", "key": "Tab", "code": "Tab"},
        session_id,
    )
    client.command(
        "Input.dispatchKeyEvent",
        {"type": "keyUp", "key": "Tab", "code": "Tab"},
        session_id,
    )
    result = _evaluate(
        client,
        session_id,
        r"""
        (() => {
          const active = document.activeElement;
          if (!(active instanceof HTMLElement) || active === document.body) return {advanced: false, named: false};
          const labelledBy = active.getAttribute("aria-labelledby");
          const labelled = labelledBy ? labelledBy.split(/\s+/).map((id) => document.getElementById(id)?.textContent || "").join(" ") : "";
          const named = Boolean((active.getAttribute("aria-label") || labelled || active.textContent || active.getAttribute("title") || "").trim() || (active.labels && active.labels.length));
          const style = getComputedStyle(active);
          return {
            advanced: true,
            named,
            focusIndicator: style.outlineStyle !== "none" || style.boxShadow !== "none",
          };
        })()
        """,
    )
    if not isinstance(result, dict):
        raise QualityGateError("Keyboard audit returned invalid data")
    result["passed"] = bool(result.get("advanced") and result.get("named"))
    return result


def _mobile_navigation_check(client: _CDPClient, session_id: str) -> dict[str, Any]:
    opened = _evaluate(
        client,
        session_id,
        r"""
        (() => {
          const trigger = document.querySelector('[aria-controls="app-sidebar"]');
          if (!(trigger instanceof HTMLElement)) return false;
          trigger.click();
          return true;
        })()
        """,
    )
    time.sleep(0.2)
    initial = _evaluate(
        client,
        session_id,
        r"""
        (() => {
          const sidebar = document.getElementById("app-sidebar");
          return {
            visible: Boolean(sidebar && getComputedStyle(sidebar).visibility !== "hidden" && !sidebar.className.includes("-translate-x-full")),
            focusInside: Boolean(sidebar && sidebar.contains(document.activeElement)),
          };
        })()
        """,
    )
    client.command(
        "Input.dispatchKeyEvent",
        {"type": "keyDown", "key": "Tab", "code": "Tab"},
        session_id,
    )
    client.command(
        "Input.dispatchKeyEvent",
        {"type": "keyUp", "key": "Tab", "code": "Tab"},
        session_id,
    )
    tab_focus_inside = _evaluate(
        client,
        session_id,
        "document.getElementById('app-sidebar')?.contains(document.activeElement) === true",
    )
    client.command(
        "Input.dispatchKeyEvent",
        {"type": "keyDown", "key": "Escape", "code": "Escape"},
        session_id,
    )
    client.command(
        "Input.dispatchKeyEvent",
        {"type": "keyUp", "key": "Escape", "code": "Escape"},
        session_id,
    )
    time.sleep(0.1)
    closed = _evaluate(
        client,
        session_id,
        "document.querySelector('[aria-controls=\"app-sidebar\"]')?.getAttribute('aria-expanded') === 'false'",
    )
    initial = initial if isinstance(initial, dict) else {}
    result = {
        "trigger_present": bool(opened),
        "opened": bool(initial.get("visible")),
        "initial_focus_inside": bool(initial.get("focusInside")),
        "tab_focus_inside": bool(tab_focus_inside),
        "escape_closed": bool(closed),
    }
    result["passed"] = all(result.values())
    return result


def _history_checks(
    client: _CDPClient,
    session_id: str,
    scenario: BrowserScenario,
    timeout_seconds: float,
) -> dict[str, bool]:
    expected = urllib.parse.urlsplit(scenario.path)
    before_reload = _wait_for_page(
        client, session_id, scenario.required_text, timeout_seconds
    )
    client.command("Page.reload", {"ignoreCache": True}, session_id, timeout_seconds)
    after_reload = _wait_for_page(
        client, session_id, scenario.required_text, timeout_seconds
    )
    expected_search = f"?{expected.query}" if expected.query else ""
    reload_preserved = (
        before_reload.get("pathname") == expected.path
        and before_reload.get("search") == expected_search
        and after_reload.get("pathname") == expected.path
        and after_reload.get("search") == expected_search
    )
    _evaluate(
        client,
        session_id,
        "history.pushState({}, '', location.pathname + location.search + '#quality-gate-history'); true",
    )
    _evaluate(client, session_id, "history.back(); true")
    deadline = time.monotonic() + timeout_seconds
    back_ok = False
    while time.monotonic() < deadline:
        if _evaluate(client, session_id, "location.hash") == "":
            back_ok = True
            break
        time.sleep(0.05)
    _evaluate(client, session_id, "history.forward(); true")
    forward_ok = False
    while time.monotonic() < deadline:
        if _evaluate(client, session_id, "location.hash") == "#quality-gate-history":
            forward_ok = True
            break
        time.sleep(0.05)
    _evaluate(
        client,
        session_id,
        "history.replaceState({}, '', location.pathname + location.search); true",
    )
    return {
        "direct_deep_link": before_reload.get("pathname") == expected.path,
        "query_persisted_on_reload": reload_preserved,
        "back_navigation": back_ok,
        "forward_navigation": forward_ok,
    }


def _run_browser_scenario(
    client: _CDPClient,
    session_id: str,
    dashboard_port: int,
    scenario: BrowserScenario,
    timeout_seconds: float,
) -> dict[str, Any]:
    started = time.monotonic()
    event_start = dict(client.events)
    local_network_error_start = dict(client.local_network_error_paths)
    parsed_scenario = urllib.parse.urlsplit(scenario.path)
    record: dict[str, Any] = {
        "name": scenario.name,
        "path": parsed_scenario.path,
        "query_keys": sorted(
            {
                name
                for name, _ in urllib.parse.parse_qsl(
                    parsed_scenario.query, keep_blank_values=True
                )
            }
        ),
        "viewport": {
            "width": scenario.viewport_width,
            "height": scenario.viewport_height,
        },
        "status": "failed",
    }
    try:
        client.command(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": scenario.viewport_width,
                "height": scenario.viewport_height,
                "deviceScaleFactor": 1,
                "mobile": scenario.viewport_width < 600,
            },
            session_id,
        )
        navigation = client.command(
            "Page.navigate",
            {"url": f"http://127.0.0.1:{dashboard_port}{scenario.path}"},
            session_id,
            timeout_seconds,
        )
        if navigation.get("errorText"):
            raise QualityGateError("Browser navigation failed")
        _wait_for_page(client, session_id, scenario.required_text, timeout_seconds)
        semantics = _semantics_checks(client, session_id, scenario.viewport_width < 600)
        keyboard = _keyboard_check(client, session_id)
        history = _history_checks(client, session_id, scenario, timeout_seconds)
        mobile_navigation = (
            _mobile_navigation_check(client, session_id)
            if scenario.check_mobile_navigation
            else {"passed": True, "not_applicable": True}
        )
        event_delta = {
            key: client.events[key] - event_start[key] for key in client.events
        }
        local_network_error_paths = {
            path: count - local_network_error_start.get(path, 0)
            for path, count in client.local_network_error_paths.items()
            if count - local_network_error_start.get(path, 0) > 0
        }
        no_browser_errors = all(
            value == 0
            for key, value in event_delta.items()
            if key != "expected_provider_null_auth_responses"
        )
        checks = {
            "semantics": semantics,
            "keyboard": keyboard,
            "history": history,
            "mobile_navigation": mobile_navigation,
            "browser_events": event_delta,
            "local_network_error_paths": local_network_error_paths,
            "no_console_page_network_errors": no_browser_errors,
        }
        passed = (
            semantics["passed"]
            and keyboard["passed"]
            and all(history.values())
            and mobile_navigation["passed"]
            and no_browser_errors
        )
        record.update(
            {
                "status": "passed" if passed else "failed",
                "checks": checks,
                "duration_seconds": time.monotonic() - started,
            }
        )
        if not passed:
            record["failure"] = "browser_contract_failed"
    except Exception as error:
        record.update(
            {
                "failure": "browser_scenario_error",
                "error": _safe_error(error),
                "duration_seconds": time.monotonic() - started,
            }
        )
    return record


def _synthetic_product_configuration() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "product_id": "agent-platform-hermes",
        "product_display_name": "AGENT PLATFORM Hermes",
        "product_version": "quality-gate",
        "upstream_product_name": "Hermes Agent",
        "upstream_version": "quality-gate",
        "upstream_commit": "0" * 40,
        "feature_flags": {"agent_platform.product_ui": "experimental"},
        "extension_modules": list(PRODUCT_EXTENSION_IDS),
        "documentation_url": None,
        "support_url": None,
    }


def _run_browser_lane(
    config: GateConfig,
    dashboard_port: int,
    env: dict[str, str],
    runtime_root: Path,
    artifact_dir: Path,
) -> dict[str, Any]:
    started = time.monotonic()
    record: dict[str, Any] = {
        "lane": "browser",
        "status": "failed",
        "timeout_seconds": config.browser_timeout_seconds,
        "synthetic_activation": {
            "scope": "browser-request-interception-only",
            "tracked_configuration_changed": False,
            "backend_configuration_changed": False,
        },
    }
    owned: _OwnedProcess | None = None
    websocket: Any = None
    try:
        browser = _resolve_browser(config)
        profile = runtime_root / "browser-profile"
        profile.mkdir(parents=True, exist_ok=True)
        owned = _spawn_owned_process(
            [
                str(browser),
                "--headless=new",
                "--disable-background-networking",
                "--disable-component-update",
                "--disable-default-apps",
                "--disable-domain-reliability",
                "--disable-extensions",
                "--disable-features=MediaRouter,OptimizationHints,AutofillServerCommunication",
                "--disable-gpu",
                "--disable-sync",
                "--metrics-recording-only",
                "--no-default-browser-check",
                "--no-first-run",
                "--no-proxy-server",
                "--password-store=basic",
                "--remote-debugging-port=0",
                f"--user-data-dir={profile}",
                "about:blank",
            ],
            runtime_root,
            env,
            artifact_dir / "browser-stdout.log",
            artifact_dir / "browser-stderr.log",
            config.max_log_bytes,
        )
        cdp_port, websocket_path, readiness_seconds = _wait_devtools_active_port(
            owned.process, profile, config.browser_timeout_seconds
        )
        websocket = _connect_websocket(
            f"ws://127.0.0.1:{cdp_port}{websocket_path}",
            min(10.0, config.browser_timeout_seconds),
        )
        client = _CDPClient(websocket, _synthetic_product_configuration())
        target = client.command("Target.createTarget", {"url": "about:blank"})
        target_id = target.get("targetId")
        if not isinstance(target_id, str):
            raise QualityGateError("CDP did not create a browser target")
        attached = client.command(
            "Target.attachToTarget", {"targetId": target_id, "flatten": True}
        )
        session_id = attached.get("sessionId")
        if not isinstance(session_id, str):
            raise QualityGateError("CDP did not attach to the browser target")
        for method, params in (
            ("Page.enable", {}),
            ("Runtime.enable", {}),
            ("Log.enable", {}),
            ("Network.enable", {}),
            (
                "Fetch.enable",
                {
                    "patterns": [
                        {
                            "urlPattern": "*/api/agent-platform/product-configuration*",
                            "requestStage": "Request",
                        }
                    ]
                },
            ),
        ):
            client.command(method, params, session_id)
        scenarios = [
            _run_browser_scenario(
                client,
                session_id,
                dashboard_port,
                scenario,
                config.browser_timeout_seconds,
            )
            for scenario in config.browser_scenarios
        ]
        record.update(
            {
                "readiness_seconds": readiness_seconds,
                "browser_family": browser.stem.lower(),
                "scenarios": scenarios,
                "status": "passed"
                if scenarios and all(item["status"] == "passed" for item in scenarios)
                else "failed",
            }
        )
        if record["status"] != "passed":
            record["failure"] = "one_or_more_scenarios_failed"
        try:
            client.command("Browser.close", timeout_seconds=2.0)
        except Exception:
            pass
    except Exception as error:
        record.update(
            {
                "failure": "browser_startup_or_cdp_failed",
                "error": _safe_error(error, (runtime_root,)),
            }
        )
    finally:
        if websocket is not None:
            try:
                websocket.close()
            except Exception:
                pass
        if owned is not None:
            record["cleanup"] = _terminate_process_tree(
                owned.process, config.cleanup_timeout_seconds
            )
            record["logs"] = owned.finish_captures()
            if not record["cleanup"]["exited"]:
                record["status"] = "failed"
                record["failure"] = "browser_cleanup_failed"
        record["duration_seconds"] = time.monotonic() - started
    return record


def _skipped_lane(lane: str, reason: str) -> dict[str, str]:
    return {"lane": lane, "status": "skipped", "reason": reason}


def run_quality_gate(config: GateConfig) -> dict[str, Any]:
    """Run selected fixed lanes and atomically write redacted JSON evidence."""

    started = time.monotonic()
    default_scenario_names = {scenario.name for scenario in DEFAULT_BROWSER_SCENARIOS}
    selected_scenario_names = {scenario.name for scenario in config.browser_scenarios}
    full_scope = set(config.lanes) == set(
        LANE_ORDER
    ) and default_scenario_names.issubset(selected_scenario_names)
    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "-"
        + uuid.uuid4().hex[:8]
    )
    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "gate_id": GATE_ID,
        "run_id": run_id,
        "started_at": _utc_now(),
        "status": "failed",
        "scope": "full" if full_scope else "partial",
        "full_gate_passed": False,
        "selected_lanes": list(config.lanes),
        "source_integrity": {"status": "not-run"},
        "lanes": [],
        "failures": [],
        "cleanup": {"status": "not-run"},
    }
    repo_root = config.repo_root.resolve()
    artifact_root = (
        config.artifact_dir or config.result_path.parent / "quality-gate-artifacts"
    ).resolve()
    run_artifacts = artifact_root / run_id
    runtime_root: Path | None = None
    dashboard_owned: _OwnedProcess | None = None
    dashboard_record: dict[str, Any] | None = None
    try:
        repo_root, product_root = _validate_config(config)
        run_artifacts.mkdir(parents=True, exist_ok=False)
        runtime_root = Path(tempfile.mkdtemp(prefix="hermes-p13-8-quality-gate-"))
        env = _isolated_environment(runtime_root)
        result["inputs"] = {
            "gate_script_sha256": _sha256_file(Path(__file__).resolve()),
            "package_json_sha256": _sha256_file(product_root / "web" / "package.json"),
        }
        try:
            result["source_integrity"] = _reconcile_modification_register(product_root)
        except Exception as error:
            result["source_integrity"] = {
                "status": "failed",
                "error": _safe_error(error, (repo_root,)),
            }
            for lane in config.lanes:
                result["lanes"].append(_skipped_lane(lane, "source_integrity_failed"))
        else:
            deadline = started + config.total_timeout_seconds
            lane_records: dict[str, dict[str, Any]] = {}
            for lane in COMMAND_LANES:
                if lane not in config.lanes:
                    continue
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    lane_records[lane] = _skipped_lane(lane, "total_timeout_exceeded")
                else:
                    lane_records[lane] = _run_command_lane(
                        lane,
                        product_root,
                        env,
                        run_artifacts,
                        min(config.command_timeout_seconds, remaining),
                        config.max_log_bytes,
                    )
                result["lanes"].append(lane_records[lane])
            build_passed = lane_records.get("build", {}).get("status") == "passed"
            if "dashboard" in config.lanes:
                if not build_passed:
                    dashboard_record = _skipped_lane("dashboard", "build_failed")
                    result["lanes"].append(dashboard_record)
                    if "browser" in config.lanes:
                        result["lanes"].append(
                            _skipped_lane("browser", "dashboard_not_ready")
                        )
                elif time.monotonic() >= deadline:
                    dashboard_record = _skipped_lane(
                        "dashboard", "total_timeout_exceeded"
                    )
                    result["lanes"].append(dashboard_record)
                    if "browser" in config.lanes:
                        result["lanes"].append(
                            _skipped_lane("browser", "dashboard_not_ready")
                        )
                else:
                    dashboard_owned, dashboard_record, dashboard_port = (
                        _start_dashboard(
                            config,
                            product_root,
                            env,
                            runtime_root,
                            run_artifacts,
                        )
                    )
                    result["lanes"].append(dashboard_record)
                    if "browser" in config.lanes:
                        if (
                            dashboard_record["status"] == "passed"
                            and dashboard_port is not None
                        ):
                            result["lanes"].append(
                                _run_browser_lane(
                                    config,
                                    dashboard_port,
                                    env,
                                    runtime_root,
                                    run_artifacts,
                                )
                            )
                        else:
                            result["lanes"].append(
                                _skipped_lane("browser", "dashboard_not_ready")
                            )
    except BaseException as error:
        result["failures"].append(
            {
                "lane": "gate",
                "reason": "internal_error",
                "error": _safe_error(
                    error,
                    tuple(
                        path for path in (repo_root, runtime_root) if path is not None
                    ),
                ),
            }
        )
    finally:
        cleanup_passed = True
        cleanup: dict[str, Any] = {"status": "passed"}
        if dashboard_owned is not None:
            dashboard_cleanup = _terminate_process_tree(
                dashboard_owned.process, config.cleanup_timeout_seconds
            )
            cleanup["dashboard"] = dashboard_cleanup
            cleanup_passed = bool(dashboard_cleanup["exited"])
            if dashboard_record is not None:
                dashboard_record["cleanup"] = dashboard_cleanup
                dashboard_record["logs"] = dashboard_owned.finish_captures()
                if not cleanup_passed:
                    dashboard_record["status"] = "failed"
                    dashboard_record["failure"] = "dashboard_cleanup_failed"
        if runtime_root is not None:
            shutil.rmtree(runtime_root, ignore_errors=True)
            cleanup["runtime_root_removed"] = not runtime_root.exists()
            cleanup_passed = cleanup_passed and cleanup["runtime_root_removed"]
        cleanup["status"] = "passed" if cleanup_passed else "failed"
        result["cleanup"] = cleanup
        for lane in result["lanes"]:
            if lane.get("status") != "passed":
                result["failures"].append(
                    {
                        "lane": lane.get("lane", "unknown"),
                        "reason": lane.get("failure", lane.get("reason", "failed")),
                    }
                )
        if result["source_integrity"].get("status") != "passed":
            result["failures"].append(
                {"lane": "source_integrity", "reason": "register_reconciliation_failed"}
            )
        if not cleanup_passed:
            result["failures"].append({"lane": "cleanup", "reason": "cleanup_failed"})
        result["status"] = "passed" if not result["failures"] else "failed"
        result["full_gate_passed"] = full_scope and result["status"] == "passed"
        result["finished_at"] = _utc_now()
        result["duration_seconds"] = time.monotonic() - started
        try:
            _write_json_atomic(config.result_path.resolve(), result)
        except OSError as error:
            raise QualityGateError(
                "Could not atomically write the quality-gate result"
            ) from error
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--result",
        type=Path,
        default=Path("9_artifacts/hermes/p13.8/frontend-quality-gate.json"),
    )
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument(
        "--lane",
        action="append",
        choices=LANE_ORDER,
        help="Run one fixed lane; repeat to select several (default: all)",
    )
    parser.add_argument(
        "--scenario",
        action="append",
        choices=tuple(scenario.name for scenario in DEFAULT_BROWSER_SCENARIOS),
        help="Run one built-in browser scenario; repeat to select several",
    )
    parser.add_argument("--command-timeout", type=float, default=600.0)
    parser.add_argument("--dashboard-timeout", type=float, default=90.0)
    parser.add_argument("--browser-timeout", type=float, default=45.0)
    parser.add_argument("--cleanup-timeout", type=float, default=10.0)
    parser.add_argument("--total-timeout", type=float, default=2400.0)
    parser.add_argument("--browser-executable", type=Path)
    parser.add_argument("--python-executable", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    lanes = tuple(lane for lane in LANE_ORDER if not args.lane or lane in args.lane)
    scenarios = tuple(
        scenario
        for scenario in DEFAULT_BROWSER_SCENARIOS
        if not args.scenario or scenario.name in args.scenario
    )
    config = GateConfig(
        repo_root=args.repo_root,
        result_path=args.result,
        artifact_dir=args.artifact_dir,
        lanes=lanes,
        browser_scenarios=scenarios,
        command_timeout_seconds=args.command_timeout,
        dashboard_timeout_seconds=args.dashboard_timeout,
        browser_timeout_seconds=args.browser_timeout,
        cleanup_timeout_seconds=args.cleanup_timeout,
        total_timeout_seconds=args.total_timeout,
        browser_executable=args.browser_executable,
        python_executable=args.python_executable,
    )
    result = run_quality_gate(config)
    print(
        f"{GATE_ID} frontend quality gate ({result['scope']}): {result['status']} "
        f"({len(result['failures'])} failure(s)); result={args.result}"
    )
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
