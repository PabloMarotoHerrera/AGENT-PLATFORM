"""Immutable in-memory SQLite read image; never open live SQLite sidecars for write.

WAL framing/checksums follow https://sqlite.org/fileformat2.html#wal_format.
A changing, unsupported or corrupt image is unavailable, never repaired.
"""

import sqlite3
import struct
from pathlib import Path

MAX_BYTES = 512 * 1024 * 1024


def _stamp(path):
    if not path.exists():
        return None
    if path.is_symlink():
        raise ValueError("SQLite sidecar redirect rejected")
    stat = path.stat()
    if stat.st_size > MAX_BYTES:
        raise ValueError("SQLite evidence exceeds memory bound")
    return stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns


def _checksum(data, endian, state=(0, 0)):
    a, b = state
    for x, y in struct.iter_unpack(endian + "II", data):
        a = (a + x + b) & 0xFFFFFFFF
        b = (b + y + a) & 0xFFFFFFFF
    return a, b


def connect(path):
    """Snapshot committed DB/WAL bytes, then query only an isolated memory image."""
    path = Path(path)
    wal_path, journal = Path(str(path) + "-wal"), Path(str(path) + "-journal")
    paths = (path, wal_path, journal)
    before = [_stamp(p) for p in paths]
    if before[0] is None or (before[2] and before[2][1]):
        raise ValueError("database absent or rollback journal requires recovery")
    image = bytearray(path.read_bytes())
    wal = wal_path.read_bytes() if before[1] else b""
    if before != [_stamp(p) for p in paths]:
        raise ValueError("SQLite evidence changed while reading")
    if image[:16] != b"SQLite format 3\x00" or len(image) < 100:
        raise ValueError("invalid SQLite evidence header")
    size = int.from_bytes(image[16:18], "big")
    size = 65536 if size == 1 else size
    if size < 512 or size > 65536 or size & (size - 1) or len(image) % size:
        raise ValueError("invalid SQLite page size")
    if wal:
        if len(wal) < 32:
            raise ValueError("incomplete SQLite WAL header")
        magic, version, page, _, salt1, salt2, c1, c2 = struct.unpack(">8I", wal[:32])
        if magic not in (0x377F0682, 0x377F0683) or version != 3007000 or page != size:
            raise ValueError("unsupported SQLite WAL")
        endian = "<" if magic == 0x377F0682 else ">"
        state = _checksum(wal[:24], endian)
        if state != (c1, c2):
            raise ValueError("SQLite WAL header checksum mismatch")
        pending, committed, final_pages = {}, {}, None
        frame_size = 24 + size
        for start in range(32, len(wal), frame_size):
            frame = wal[start : start + frame_size]
            if len(frame) != frame_size:
                raise ValueError("incomplete SQLite WAL frame")
            number, commit, s1, s2, c1, c2 = struct.unpack(">6I", frame[:24])
            if (s1, s2) != (salt1, salt2):
                break  # Stale tail after a WAL reset; never part of this generation.
            state = _checksum(frame[:8] + frame[24:], endian, state)
            if state != (c1, c2) or not 0 < number <= MAX_BYTES // size:
                raise ValueError("SQLite WAL frame integrity mismatch")
            pending[number] = frame[24:]
            if commit:
                if commit > MAX_BYTES // size:
                    raise ValueError("SQLite committed image exceeds bound")
                committed.update(pending)
                pending.clear()
                final_pages = commit
        if final_pages is not None:
            length = final_pages * size
            image = image[:length]
            image.extend(b"\0" * (length - len(image)))
            for number, data in committed.items():
                if number <= final_pages:
                    image[(number - 1) * size : number * size] = data
    # Deserialize needs a standalone rollback-format image; only memory is changed.
    image[18:20] = b"\x01\x01"
    conn = sqlite3.connect(":memory:")
    conn.deserialize(bytes(image))
    conn.execute("PRAGMA query_only=ON")
    conn.row_factory = sqlite3.Row
    return conn
