"""Inert subprocess fixture for P14.2 runtime process-owner tests."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


_PROHIBITED_ENVIRONMENT_NAMES = frozenset({
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AWS_ACCESS_KEY_ID",
    "AZURE_CLIENT_SECRET",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "GITHUB_TOKEN",
    "SSH_AUTH_SOCK",
    "MCP_TOKEN",
    "HTTP_PROXY",
    "PYTHONPATH",
    "NODE_OPTIONS",
})


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be >= 0")
    return parsed


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inert runtime adapter probe")
    parser.add_argument("--stdout-bytes", type=_positive_int, default=0)
    parser.add_argument("--stderr-bytes", type=_positive_int, default=0)
    parser.add_argument("--sleep-ms", type=_positive_int, default=0)
    parser.add_argument("--exit-code", type=int, default=0)
    parser.add_argument("--spawn-child", action="store_true")
    parser.add_argument("--child-sleep-ms", type=_positive_int, default=5000)
    parser.add_argument("--ignore-graceful-stop", action="store_true")
    parser.add_argument("--graceful-exit-code", type=int, default=0)
    parser.add_argument("--verify-managed-environment", action="store_true")
    parser.add_argument("--verify-provider-null", action="store_true")
    parser.add_argument("--expected-workspace-root")
    parser.add_argument("--expect-no-path", action="store_true")
    return parser


def _write_bytes(stream, byte_count: int, token: bytes) -> None:
    remaining = byte_count
    while remaining > 0:
        chunk = token[: min(len(token), remaining)]
        stream.write(chunk)
        stream.flush()
        remaining -= len(chunk)


def _sleep_bounded(sleep_ms: int) -> None:
    deadline = time.monotonic() + (sleep_ms / 1000)
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return
        time.sleep(min(remaining, 0.05))


def _install_signal_handler(
    *, ignore_graceful_stop: bool, graceful_exit_code: int
) -> None:
    def _handle_termination(_signum, _frame) -> None:
        if ignore_graceful_stop:
            return
        raise SystemExit(graceful_exit_code)

    if sys.platform == "win32":
        sigbreak = getattr(signal, "SIGBREAK", None)
        if sigbreak is not None:
            signal.signal(sigbreak, _handle_termination)
        return

    signal.signal(signal.SIGTERM, _handle_termination)


def _canonical_text_path(value: str) -> str:
    return os.path.normcase(os.path.abspath(value))


def _child_managed_environment_exit_code(workspace_root: str | None) -> int:
    if not workspace_root:
        return 28
    root = Path(workspace_root)
    expected = {
        "HERMES_HOME": root / "hermes-home",
        "HOME": root / "home",
        "USERPROFILE": root / "user-profile",
        "APPDATA": root / "appdata",
        "LOCALAPPDATA": root / "localappdata",
        "TEMP": root / "temp",
        "TMP": root / "temp",
        "TMPDIR": root / "temp",
    }
    for name, expected_path in expected.items():
        value = os.environ.get(name)
        if value is None:
            return 21
        if _canonical_text_path(value) != _canonical_text_path(str(expected_path)):
            return 24
        try:
            common = os.path.commonpath([
                _canonical_text_path(str(root)),
                _canonical_text_path(value),
            ])
        except ValueError:
            return 24
        if common != _canonical_text_path(str(root)):
            return 24

    home_expected = (
        expected["USERPROFILE"] if sys.platform == "win32" else expected["HOME"]
    )
    if _canonical_text_path(str(Path.home())) != _canonical_text_path(
        str(home_expected)
    ):
        return 23
    if _canonical_text_path(os.path.expanduser("~")) != _canonical_text_path(
        str(home_expected)
    ):
        return 23
    if _canonical_text_path(os.getcwd()) != _canonical_text_path(str(root / "workdir")):
        return 25

    if sys.platform == "win32":
        drive, suffix = os.path.splitdrive(str(expected["USERPROFILE"]))
        suffix = suffix or "\\"
        if os.environ.get("HOMEDRIVE") != drive or os.environ.get("HOMEPATH") != suffix:
            return 27
    return 0


def _child_provider_null_exit_code(*, expect_no_path: bool) -> int:
    normalized = {name.upper() for name in os.environ}
    if normalized & _PROHIBITED_ENVIRONMENT_NAMES:
        return 22
    if expect_no_path and "PATH" in normalized:
        return 26
    return 0


def main() -> int:
    args = _parser().parse_args()
    _install_signal_handler(
        ignore_graceful_stop=args.ignore_graceful_stop,
        graceful_exit_code=args.graceful_exit_code,
    )

    if args.verify_managed_environment:
        exit_code = _child_managed_environment_exit_code(args.expected_workspace_root)
        if exit_code != 0:
            return exit_code
    if args.verify_provider_null:
        exit_code = _child_provider_null_exit_code(expect_no_path=args.expect_no_path)
        if exit_code != 0:
            return exit_code

    child: subprocess.Popen[bytes] | None = None
    if args.spawn_child:
        child = subprocess.Popen(
            [
                sys.executable,
                __file__,
                "--sleep-ms",
                str(args.child_sleep_ms),
                "--exit-code",
                "0",
                *(("--ignore-graceful-stop",) if args.ignore_graceful_stop else ()),
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
        )

    _write_bytes(sys.stdout.buffer, args.stdout_bytes, b"O")
    _write_bytes(sys.stderr.buffer, args.stderr_bytes, b"E")
    _sleep_bounded(args.sleep_ms)

    if child is not None and child.poll() is not None:
        child.wait(timeout=0)
    return args.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
