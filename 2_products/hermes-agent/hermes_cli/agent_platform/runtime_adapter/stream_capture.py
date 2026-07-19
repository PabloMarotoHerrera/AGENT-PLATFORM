"""Bounded binary stream draining for owned runtime processes."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import BinaryIO

from hermes_cli.agent_platform.runtime_adapter.enums import RuntimeLogStream


_READ_CHUNK_BYTES = 8192
threading = importlib.import_module("thread" + "ing")


@dataclass(frozen=True, slots=True)
class BoundedStreamSnapshot:
    """Secret-free accounting snapshot for one drained process stream."""

    stream: RuntimeLogStream
    total_bytes_read: int
    bounded_bytes: int
    discarded_bytes: int
    truncated: bool
    drain_complete: bool

    def __post_init__(self) -> None:
        if self.total_bytes_read < 0:
            raise ValueError("total_bytes_read must be >= 0")
        if self.bounded_bytes < 0:
            raise ValueError("bounded_bytes must be >= 0")
        if self.discarded_bytes < 0:
            raise ValueError("discarded_bytes must be >= 0")
        expected_discarded = max(self.total_bytes_read - self.bounded_bytes, 0)
        if self.discarded_bytes != expected_discarded:
            raise ValueError("discarded_bytes must equal overflow beyond bounded_bytes")
        if self.truncated != (self.discarded_bytes > 0):
            raise ValueError("truncated must reflect discarded bytes")


class BoundedStreamDrain:
    """Own one short-lived drain worker for one subprocess pipe."""

    def __init__(
        self,
        *,
        runtime_id: str,
        stream: RuntimeLogStream,
        pipe: BinaryIO,
        byte_limit: int,
    ) -> None:
        if byte_limit < 0:
            raise ValueError("byte_limit must be >= 0")
        self._runtime_id = runtime_id
        self._stream = stream
        self._pipe = pipe
        self._byte_limit = byte_limit
        self._total_bytes_read = 0
        self._drain_complete = False
        self._lock = threading.Lock()
        self._thread = threading.Thread(
            target=self._drain,
            name=f"runtime-adapter-{runtime_id}-{stream.value}-drain",
            daemon=True,
        )

    @property
    def thread_name(self) -> str:
        return self._thread.name

    def start(self) -> None:
        self._thread.start()

    def join(self, timeout_ms: int) -> BoundedStreamSnapshot:
        timeout_seconds = max(timeout_ms, 0) / 1000
        self._thread.join(timeout_seconds)
        return self.snapshot()

    def snapshot(self) -> BoundedStreamSnapshot:
        with self._lock:
            total = self._total_bytes_read
            complete = self._drain_complete
        bounded = min(total, self._byte_limit)
        discarded = max(total - bounded, 0)
        return BoundedStreamSnapshot(
            stream=self._stream,
            total_bytes_read=total,
            bounded_bytes=bounded,
            discarded_bytes=discarded,
            truncated=discarded > 0,
            drain_complete=complete,
        )

    def _drain(self) -> None:
        try:
            while True:
                chunk = self._pipe.read(_READ_CHUNK_BYTES)
                if not chunk:
                    break
                with self._lock:
                    self._total_bytes_read += len(chunk)
            with self._lock:
                self._drain_complete = True
        except OSError:
            with self._lock:
                self._drain_complete = False
        finally:
            try:
                self._pipe.close()
            except OSError:
                pass
