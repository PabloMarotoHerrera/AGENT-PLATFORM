#!/usr/bin/env python3
"""Live controlled-lifecycle gate for the Hermes runtime adapter P14.8."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
GATE_ID = "P14.8"
VERDICT = "hermes_runtime_adapter_controlled_lifecycle_passed"
PREREQUISITE_EXIT_CODE = 20
EXPECTED_READINESS_CHECK_IDS = (
    "dashboard.root",
    "dashboard.status",
    "dashboard.product_config_unauthenticated",
    "dashboard.product_config_authenticated",
    "dashboard.plugin_manifest",
    "dashboard.files_root",
    "dashboard.files_outside_root",
)


class LifecycleGateError(RuntimeError):
    """Raised when the controlled lifecycle cannot be proven safely."""


class LifecycleGatePrerequisiteError(LifecycleGateError):
    """Raised when a required local prerequisite is missing or invalid."""


@dataclass(frozen=True, slots=True)
class GateConfig:
    repo_root: Path
    result_path: Path
    artifact_dir: Path | None = None
    build_timeout_seconds: float = 600.0
    lifecycle_timeout_seconds: float = 120.0
    python_executable: Path | None = None
    dashboard_port: int | None = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_error(error: BaseException, *paths: Path) -> str:
    text = f"{type(error).__name__}: {error}"
    for path in paths:
        raw = str(path)
        text = text.replace(raw, "<path>")
        text = text.replace(raw.replace("\\", "/"), "<path>")
    for marker in ("token", "secret", "password", "api_key"):
        text = text.replace(marker.upper(), marker)
    return text[:500]


def _validate_config(config: GateConfig) -> None:
    repo_root = config.repo_root.resolve()
    product_root = repo_root / "2_products" / "pepper-agent"
    if not product_root.is_dir():
        raise LifecycleGatePrerequisiteError("Hermes product root was not found")
    if not (product_root / "hermes_cli" / "main.py").is_file():
        raise LifecycleGatePrerequisiteError("Hermes CLI entry point was not found")
    if config.build_timeout_seconds <= 0 or config.lifecycle_timeout_seconds <= 0:
        raise LifecycleGatePrerequisiteError("Gate timeouts must be positive")
    if config.dashboard_port is not None and not 1 <= config.dashboard_port <= 65_535:
        raise LifecycleGatePrerequisiteError(
            "Dashboard port must be between 1 and 65535"
        )


def _product_root(repo_root: Path) -> Path:
    return repo_root.resolve() / "2_products" / "pepper-agent"


def _resolve_product_python_executable(
    product_root: Path, requested: Path | None = None
) -> Path:
    candidates = (
        (requested,)
        if requested is not None
        else _product_python_candidates(product_root)
    )
    observed_product_candidate = False
    for candidate in candidates:
        if candidate is None:
            continue
        resolved = candidate.resolve(strict=False)
        if not _is_inside_product_environment(product_root, resolved):
            if requested is not None:
                raise LifecycleGatePrerequisiteError(
                    "Python executable is outside the editable product environment"
                )
            continue
        observed_product_candidate = True
        if not resolved.is_file():
            continue
        _validate_product_python_executable(product_root, resolved)
        return resolved
    if observed_product_candidate or requested is not None:
        raise LifecycleGatePrerequisiteError(
            "Product Python executable is invalid for the editable product environment"
        )
    raise LifecycleGatePrerequisiteError(
        "Product Python executable was not found in the editable product environment"
    )


def _product_python_candidates(product_root: Path) -> tuple[Path, ...]:
    return (
        product_root / ".venv" / "Scripts" / "python.exe",
        product_root / ".venv" / "bin" / "python",
        product_root / "venv" / "Scripts" / "python.exe",
        product_root / "venv" / "bin" / "python",
    )


def _validate_product_python_executable(
    product_root: Path, python_executable: Path
) -> None:
    if _is_reparse_point_or_symlink(python_executable):
        raise LifecycleGatePrerequisiteError(
            "Product Python executable must not be a symlink or reparse point"
        )
    environment_root = _product_environment_root(product_root, python_executable)
    if environment_root is None or not (environment_root / "pyvenv.cfg").is_file():
        raise LifecycleGatePrerequisiteError(
            "Product Python executable is not inside a product virtual environment"
        )
    if not _has_editable_product_marker(environment_root):
        raise LifecycleGatePrerequisiteError(
            "Product virtual environment does not contain the editable Hermes package"
        )


def _is_inside_product_environment(product_root: Path, candidate: Path) -> bool:
    return _product_environment_root(product_root, candidate) is not None


def _product_environment_root(product_root: Path, candidate: Path) -> Path | None:
    product_root = product_root.resolve(strict=False)
    candidate = candidate.resolve(strict=False)
    for name in (".venv", "venv"):
        environment_root = (product_root / name).resolve(strict=False)
        try:
            candidate.relative_to(environment_root)
        except ValueError:
            continue
        return environment_root
    return None


def _is_reparse_point_or_symlink(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, OSError):
        return False
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return bool(attributes & reparse_flag)


def _has_editable_product_marker(environment_root: Path) -> bool:
    site_packages_roots = [environment_root / "Lib" / "site-packages"]
    site_packages_roots.extend((environment_root / "lib").glob("python*/site-packages"))
    for site_packages in site_packages_roots:
        if not site_packages.is_dir():
            continue
        editable_markers = tuple(site_packages.glob("__editable__.hermes_agent-*.pth"))
        dist_infos = tuple(site_packages.glob("hermes_agent-*.dist-info"))
        if editable_markers and dist_infos:
            return True
    return False


def _artifact_dir(config: GateConfig) -> Path:
    return (
        config.artifact_dir
        or config.result_path.parent / "runtime-adapter-lifecycle-artifacts"
    ).resolve()


def _resolve_node_npm() -> tuple[Path, Path]:
    node_raw = shutil.which("node")
    if not node_raw:
        raise LifecycleGatePrerequisiteError(
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
            (
                npm.parent / "node_modules" / "npm" / "bin" / "npm-cli.js",
                npm.parent.parent / "node_modules" / "npm" / "bin" / "npm-cli.js",
            )
        )
    npm_cli = next((candidate for candidate in candidates if candidate.is_file()), None)
    if npm_cli is None:
        raise LifecycleGatePrerequisiteError(
            "npm-cli.js was not found; the gate will not invoke a shell or npm.cmd"
        )
    return node, npm_cli.resolve()


def _build_environment(artifact_dir: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for name in ("PATH", "SystemRoot", "WINDIR"):
        if name in os.environ:
            env[name] = os.environ[name]
    home = artifact_dir / "home"
    temp = artifact_dir / "temp"
    appdata = home / "AppData" / "Roaming"
    localappdata = home / "AppData" / "Local"
    for path in (home, temp, appdata, localappdata):
        path.mkdir(parents=True, exist_ok=True)
    env.update(
        {
            "APPDATA": str(appdata),
            "CI": "1",
            "HERMES_HOME": str(home / ".hermes"),
            "HOME": str(home),
            "LOCALAPPDATA": str(localappdata),
            "NO_COLOR": "1",
            "NPM_CONFIG_AUDIT": "false",
            "NPM_CONFIG_FUND": "false",
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


def _ensure_web_dist(
    product_root: Path,
    artifact_dir: Path,
    *,
    timeout_seconds: float,
) -> dict[str, Any]:
    index = product_root / "hermes_cli" / "web_dist" / "index.html"
    if index.is_file():
        return {"status": "passed", "built": False, "dist": "hermes_cli/web_dist"}
    node, npm_cli = _resolve_node_npm()
    env = _build_environment(artifact_dir / "build-env")
    argv = [str(node), str(npm_cli), "run", "build"]
    started = time.monotonic()
    completed = subprocess.run(
        argv,
        cwd=product_root / "web",
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_seconds,
        check=False,
    )
    result = {
        "status": "passed"
        if completed.returncode == 0 and index.is_file()
        else "failed",
        "built": True,
        "returncode": completed.returncode,
        "duration_seconds": time.monotonic() - started,
        "stdout_bytes": len(completed.stdout),
        "stderr_bytes": len(completed.stderr),
    }
    if result["status"] != "passed":
        result["failure"] = "web_dist_missing_after_build"
    return result


def _run_adapter_lifecycle(
    product_root: Path,
    artifact_dir: Path,
    *,
    timeout_seconds: float,
    python_executable: Path,
    dashboard_port: int | None,
) -> dict[str, Any]:
    sys.path.insert(0, str(product_root))
    try:
        from hermes_cli.agent_platform.runtime_adapter.adapter import (
            GovernedRuntimeAdapter,
        )
        from hermes_cli.agent_platform.runtime_adapter.audit_normalization import (
            project_runtime_operation_audit,
        )
        from hermes_cli.agent_platform.runtime_adapter.contracts import (
            HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID,
            RuntimeLaunchRequest,
            RuntimeRollbackRequest,
            RuntimeStopRequest,
        )
        from hermes_cli.agent_platform.runtime_adapter.enums import (
            RuntimeOperationOutcome,
        )
        from hermes_cli.agent_platform.runtime_adapter.profiles import (
            get_runtime_profile,
        )
    finally:
        try:
            sys.path.remove(str(product_root))
        except ValueError:
            pass

    profile = get_runtime_profile(HERMES_DASHBOARD_EXPERIMENTAL_PROFILE_ID)
    workspace_base = artifact_dir / "workspaces"
    workspace_base.mkdir(parents=True, exist_ok=True)
    adapter = GovernedRuntimeAdapter(
        runtime_base_root=workspace_base,
        source_environment=_build_environment(artifact_dir / "runtime-env"),
        python_executable=str(python_executable),
        dashboard_port=dashboard_port or 0,
    )
    correlation_id = "corr.p148.live." + uuid.uuid4().hex[:16]
    runtime_id = ""
    launch = stop = rollback = None
    readiness_summary: dict[str, Any] | None = None
    started = time.monotonic()
    try:
        launch = adapter.launch(
            RuntimeLaunchRequest(
                schema_version=1,
                runtime_profile_id=profile.profile_ref.profile_id,
                workspace_binding=profile.default_workspace_binding,
                correlation_id=correlation_id,
                requested_by="agent-platform.lifecycle-gate",
                timeout_policy=profile.timeout_policy,
                evidence_context=(),
            )
        )
        runtime_id = launch.runtime_handle.runtime_id
        if launch.outcome is not RuntimeOperationOutcome.READY:
            failure_code = launch.failure.failure_code if launch.failure else "none"
            event_types = ",".join(event.event_type.value for event in launch.events)
            raise LifecycleGateError(
                "launch outcome was "
                f"{launch.outcome.value}; failure_code={failure_code}; "
                f"events={event_types}"
            )
        readiness_summary = adapter.readiness_summary(runtime_id, correlation_id)
        _validate_readiness_summary(readiness_summary, EXPECTED_READINESS_CHECK_IDS)
        stop = adapter.shutdown(
            RuntimeStopRequest(
                schema_version=1,
                runtime_id=runtime_id,
                correlation_id=correlation_id,
                requested_by="agent-platform.lifecycle-gate",
                reason_code="gate.shutdown",
            )
        )
        if stop.outcome is not RuntimeOperationOutcome.STOPPED:
            raise LifecycleGateError(f"shutdown outcome was {stop.outcome.value}")
        rollback = adapter.rollback(
            RuntimeRollbackRequest(
                schema_version=1,
                runtime_id=runtime_id,
                correlation_id=correlation_id,
                requested_by="agent-platform.lifecycle-gate",
                reason_code="gate.rollback",
            )
        )
        if rollback.outcome is not RuntimeOperationOutcome.ROLLED_BACK:
            raise LifecycleGateError(f"rollback outcome was {rollback.outcome.value}")
    finally:
        if runtime_id in adapter.active_runtime_ids():
            try:
                adapter.shutdown(
                    RuntimeStopRequest(
                        schema_version=1,
                        runtime_id=runtime_id,
                        correlation_id=correlation_id,
                        requested_by="agent-platform.lifecycle-gate",
                        reason_code="gate.cleanup.shutdown",
                    )
                )
            except Exception:
                pass
            try:
                adapter.rollback(
                    RuntimeRollbackRequest(
                        schema_version=1,
                        runtime_id=runtime_id,
                        correlation_id=correlation_id,
                        requested_by="agent-platform.lifecycle-gate",
                        reason_code="gate.cleanup.rollback",
                    )
                )
            except Exception:
                pass
    duration = time.monotonic() - started
    if duration > timeout_seconds:
        raise LifecycleGateError("adapter lifecycle exceeded gate timeout")
    event_count = len(rollback.events if rollback else launch.events if launch else ())
    audit_projection = project_runtime_operation_audit(rollback)
    if audit_projection.runtime_id != runtime_id:
        raise LifecycleGateError("audit projection runtime identity mismatch")
    if audit_projection.correlation_id != correlation_id:
        raise LifecycleGateError("audit projection correlation identity mismatch")
    if audit_projection.event_count != event_count:
        raise LifecycleGateError("audit projection count did not match event count")
    if readiness_summary is None:
        raise LifecycleGateError("readiness summary was not captured")
    bounded_readiness = _bounded_readiness_lifecycle_fields(readiness_summary)
    return {
        "status": "passed",
        "runtime_id": runtime_id,
        "correlation_id": correlation_id,
        "duration_seconds": duration,
        "launch_outcome": launch.outcome.value if launch else None,
        "shutdown_outcome": stop.outcome.value if stop else None,
        "rollback_outcome": rollback.outcome.value if rollback else None,
        "event_count": event_count,
        "audit_projection_count": audit_projection.event_count,
        **bounded_readiness,
    }


def _validate_readiness_summary(
    summary: dict[str, Any], expected_check_ids: tuple[str, ...]
) -> None:
    if summary.get("check_count") != len(expected_check_ids):
        raise LifecycleGateError("readiness summary did not contain seven checks")
    if tuple(summary.get("check_ids") or ()) != expected_check_ids:
        raise LifecycleGateError("readiness summary check IDs did not match contract")
    checks = summary.get("checks")
    if not isinstance(checks, list) or len(checks) != len(expected_check_ids):
        raise LifecycleGateError("readiness check details were incomplete")
    for expected_check_id, check in zip(expected_check_ids, checks):
        if not isinstance(check, dict):
            raise LifecycleGateError("readiness check detail was invalid")
        if (
            check.get("check_id") != expected_check_id
            or check.get("passed") is not True
        ):
            raise LifecycleGateError("readiness check detail did not pass")
        status_code = check.get("status_code")
        if not isinstance(status_code, int) or not 100 <= status_code <= 599:
            raise LifecycleGateError("readiness check status was invalid")


def _bounded_readiness_lifecycle_fields(summary: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "gateway_running",
        "active_agent_count",
        "active_session_count",
        "provider_count",
        "unauthenticated_config_status",
        "authenticated_config_status",
        "product_feature_state",
        "extension_module_count",
        "extension_module_order_valid",
        "plugin_manifest_valid",
        "plugin_route_conflict_count",
        "managed_files_root_matches",
        "outside_files_root_denied",
    )
    return {
        "readiness_check_count": summary["check_count"],
        "readiness_check_ids": list(summary["check_ids"]),
        "readiness_checks": summary["checks"],
        **{key: summary[key] for key in keys},
    }


def _validate_lifecycle_summary(summary: dict[str, Any]) -> None:
    if summary.get("status") != "passed":
        raise LifecycleGateError("adapter lifecycle did not pass")
    readiness = {
        "check_count": summary.get("readiness_check_count"),
        "check_ids": summary.get("readiness_check_ids"),
        "checks": summary.get("readiness_checks"),
    }
    _validate_readiness_summary(readiness, EXPECTED_READINESS_CHECK_IDS)
    event_count = summary.get("event_count")
    audit_projection_count = summary.get("audit_projection_count")
    if not isinstance(event_count, int) or event_count <= 0:
        raise LifecycleGateError("lifecycle event count was invalid")
    if audit_projection_count != event_count:
        raise LifecycleGateError("audit projection count did not match event count")


def run_lifecycle_gate(config: GateConfig) -> dict[str, Any]:
    started = time.monotonic()
    repo_root = config.repo_root.resolve()
    artifact_dir = _artifact_dir(config)
    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "gate_id": GATE_ID,
        "status": "failed",
        "verdict": None,
        "exit_code": 1,
        "started_at": _utc_now(),
        "repo_root": "<repository-root>",
        "artifact_dir": "<artifact-dir>",
        "python_executable": None,
        "dashboard_port": config.dashboard_port,
        "failures": [],
    }
    try:
        _validate_config(config)
        product_root = _product_root(repo_root)
        python_executable = _resolve_product_python_executable(
            product_root,
            config.python_executable,
        )
        result["python_executable"] = "<product-python>"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        build = _ensure_web_dist(
            product_root,
            artifact_dir,
            timeout_seconds=config.build_timeout_seconds,
        )
        result["build"] = build
        if build.get("status") != "passed":
            raise LifecycleGateError("web build prerequisite failed")
        lifecycle = _run_adapter_lifecycle(
            product_root,
            artifact_dir,
            timeout_seconds=config.lifecycle_timeout_seconds,
            python_executable=python_executable,
            dashboard_port=config.dashboard_port,
        )
        _validate_lifecycle_summary(lifecycle)
        result["lifecycle"] = lifecycle
        result["status"] = "passed"
        result["verdict"] = VERDICT
        result["exit_code"] = 0
    except LifecycleGatePrerequisiteError as exc:
        result["exit_code"] = PREREQUISITE_EXIT_CODE
        result["failures"].append(
            {
                "classification": "prerequisite",
                "reason": _safe_error(exc, repo_root, artifact_dir),
            }
        )
    except Exception as exc:
        result["failures"].append({"reason": _safe_error(exc, repo_root, artifact_dir)})
    finally:
        result["finished_at"] = _utc_now()
        result["duration_seconds"] = time.monotonic() - started
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        "--repository-root",
        dest="repo_root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--result",
        type=Path,
        default=Path("9_artifacts/hermes/p14.8/runtime-adapter-lifecycle-gate.json"),
    )
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument("--build-timeout", type=float, default=600.0)
    parser.add_argument("--lifecycle-timeout", type=float, default=120.0)
    parser.add_argument("--python-executable", type=Path)
    parser.add_argument("--port", dest="dashboard_port", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = run_lifecycle_gate(
        GateConfig(
            repo_root=args.repo_root,
            result_path=args.result,
            artifact_dir=args.artifact_dir,
            build_timeout_seconds=args.build_timeout,
            lifecycle_timeout_seconds=args.lifecycle_timeout,
            python_executable=args.python_executable,
            dashboard_port=args.dashboard_port,
        )
    )
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return int(result.get("exit_code") or (0 if result["status"] == "passed" else 1))


if __name__ == "__main__":
    raise SystemExit(main())
