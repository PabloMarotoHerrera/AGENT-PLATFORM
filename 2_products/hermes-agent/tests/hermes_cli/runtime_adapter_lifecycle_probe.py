"""Inert subprocess fixture for P14.2 runtime process-owner tests."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time


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


def _install_signal_handler() -> None:
    if sys.platform == "win32":
        return

    def _handle_termination(_signum, _frame) -> None:
        raise SystemExit(143)

    signal.signal(signal.SIGTERM, _handle_termination)


def main() -> int:
    args = _parser().parse_args()
    _install_signal_handler()

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
