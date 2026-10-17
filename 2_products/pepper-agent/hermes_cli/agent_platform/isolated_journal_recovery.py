"""Read-only consistent snapshot of an explicitly injected disposable handle."""
import sqlite3
from .isolated_operation_journal import IsolatedJournal
from .harness.journal_recovery import DurableSnapshot, StoredEntry
from .harness.validation import canonical_json, parse_contract
from .harness.operation_journal import OperationRequest


def read_snapshot(journal, expected, *, provenance, owner_process="UNKNOWN"):
    if type(journal) is not IsolatedJournal:
        raise TypeError("injected_disposable_handle_required")
    r = parse_contract(OperationRequest, canonical_json(expected))
    common = dict(expected=r, provenance=provenance, owner_process=owner_process)
    empty = dict(operation=None, owner=None, entries=(), aggregate=None, effect_key=None,
        attempt=None, payload_hex=None, receipt=None)
    if journal.root.resolve(strict=True) != journal.root or journal.path.is_symlink() or not journal.path.is_file():
        raise ValueError("disposable_path_changed")
    c = sqlite3.connect(journal.path.as_uri()+"?mode=ro", uri=True, isolation_level=None, timeout=5)
    try:
        c.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 1_048_576)
        c.execute("PRAGMA query_only=ON")
        c.execute("BEGIN")
        schema = c.execute("PRAGMA user_version").fetchone()[0]
        if schema != 1:
            return DurableSnapshot(**common, **empty, store_schema=schema)
        op = c.execute("SELECT request,owner FROM operations WHERE id=?", (r.operation_id,)).fetchone()
        rows = c.execute("SELECT revision,body FROM entries WHERE op=? ORDER BY revision LIMIT 33", (r.operation_id,)).fetchall()
        aggregate = c.execute("SELECT body FROM aggregates WHERE id=?", (r.expected.aggregate,)).fetchone()
        effect = c.execute("SELECT id,attempt,payload,receipt FROM effects WHERE id=?", (r.effect.effect_id,)).fetchone()
        conflicts = c.execute("SELECT body FROM conflicts WHERE op=? ORDER BY sequence LIMIT 129", (r.operation_id,)).fetchall()
        return DurableSnapshot(**common, store_schema=schema, operation=op[0] if op else None,
            owner=op[1] if op else None, entries=tuple(StoredEntry(revision=n,body=b) for n,b in rows),
            aggregate=aggregate[0] if aggregate else None, effect_key=effect[0] if effect else None,
            attempt=effect[1] if effect else None, payload_hex=bytes(effect[2]).hex() if effect else None,
            receipt=effect[3] if effect else None, conflicts=tuple(row[0] for row in conflicts),
            complete=len(rows)<=32 and len(conflicts)<=128)
    except (sqlite3.Error, ValueError, TypeError):
        return DurableSnapshot(**common, **empty, store_schema=1, complete=False, read_error="UNREADABLE")
    finally:
        c.close()
