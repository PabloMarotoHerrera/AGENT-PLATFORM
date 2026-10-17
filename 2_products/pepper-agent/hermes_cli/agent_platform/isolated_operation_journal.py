"""Explicit disposable SQLite substrate. No ambient paths or production owners.

One file, local BEGIN IMMEDIATE transactions, permanent owner per operation.
No leases, owner takeover, recovery or cross-store atomicity is implemented.
"""

from contextlib import contextmanager
from pathlib import Path
import sqlite3
import tempfile

from .harness.contracts import ContractRef
from .harness.journal_protocol import advance, checked, initial, owner_for, qualify, verify_receipt
from .harness.operation_journal import (ConflictReport, EffectReceipt, ExpectedVersion,
    JournalEntry, OperationRequest, StageTransition)
from .harness.validation import canonical_json, parse_contract, verify_content_digest

STORE = ContractRef(contract_id="isolated-sqlite-aggregate", version=1)
_CREATED = object()


class JournalConflict(ValueError):
    def __init__(self, report):
        self.report = report
        super().__init__(report.reason)


class IsolatedJournal:
    __slots__ = ('_root', '_path')

    def __init__(self, root, token):
        if token is not _CREATED:
            raise ValueError("explicit_disposable_initialization_required")
        self._root = Path(root)
        self._path = self.root / 'journal.sqlite3'

    @property
    def root(self):
        return self._root

    @property
    def path(self):
        return self._path

    @classmethod
    def create_disposable(cls, parent):
        parent = Path(parent).resolve(strict=True)
        root = Path(tempfile.mkdtemp(prefix='har12-disposable-', dir=parent))
        result = cls(root, _CREATED)
        with sqlite3.connect(result.path) as c:
            c.executescript('''
                BEGIN IMMEDIATE;
                PRAGMA user_version=1;
                CREATE TABLE aggregates(id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE operations(id TEXT PRIMARY KEY, request TEXT NOT NULL, owner TEXT);
                CREATE TABLE entries(op TEXT NOT NULL, revision INTEGER NOT NULL, body TEXT NOT NULL,
                    PRIMARY KEY(op,revision));
                CREATE TABLE conflicts(sequence INTEGER PRIMARY KEY, op TEXT NOT NULL, body TEXT NOT NULL);
                CREATE TABLE effects(id TEXT PRIMARY KEY, attempt TEXT NOT NULL, payload BLOB NOT NULL,
                    receipt TEXT NOT NULL);
                COMMIT;
            ''')
        return result

    def reconnect(self):
        # Only an already-created substrate capability can reopen this path.
        return type(self)(self.root, _CREATED)

    @contextmanager
    def transaction(self):
        if self.root.resolve(strict=True) != self.root or self.path.is_symlink() or not self.path.is_file():
            raise ValueError("disposable_substrate_path_changed")
        c = sqlite3.connect(self.path.as_uri()+'?mode=rw', uri=True, isolation_level=None, timeout=10)
        try:
            c.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 1_048_576)
            c.execute('PRAGMA synchronous=FULL')
            if c.execute('PRAGMA user_version').fetchone()[0] != 1:
                raise ValueError("unsupported_store_schema")
            c.execute('BEGIN IMMEDIATE')
            yield c
            c.commit()
        except BaseException:
            c.rollback()
            raise
        finally:
            c.close()

    def initialize_aggregate(self, version):
        v = checked(ExpectedVersion, version)
        if v.store != STORE:
            raise ValueError("unsupported_aggregate_store")
        with self.transaction() as c:
            c.execute('INSERT INTO aggregates VALUES (?,?)', (v.aggregate, canonical_json(v)))

    def _observed(self, c, expected):
        row = c.execute('SELECT body FROM aggregates WHERE id=?', (expected.aggregate,)).fetchone()
        if row is None:
            raise ValueError("aggregate_missing")
        observed = parse_contract(ExpectedVersion, row[0])
        if observed.scope != expected.scope or observed.store != STORE or expected.store != STORE:
            raise ValueError("aggregate_scope_or_store_mismatch")
        return observed

    def observe_version(self, expected):
        with self.transaction() as c:
            return self._observed(c, expected)

    def _entries(self, c, operation_id):
        rows = c.execute('SELECT revision,body FROM entries WHERE op=? ORDER BY revision LIMIT 33', (operation_id,)).fetchall()
        if len(rows) > 32:
            raise ValueError("journal_read_bound")
        entries = tuple(parse_contract(JournalEntry, r[1]) for r in rows)
        if entries:
            request_row = c.execute('SELECT request FROM operations WHERE id=?', (operation_id,)).fetchone()
            if (request_row is None or parse_contract(OperationRequest, request_row[0]) != entries[0].request
                    or any(row[0] != entry.journal_version or entry.request.operation_id != operation_id for row, entry in zip(rows, entries))
                    or entries[0] != initial(entries[0].request)):
                raise ValueError("invalid_journal_genesis")
            for a, b in zip(entries, entries[1:]):
                if b.transition is None or b.owner is None or advance(a, b.transition, b.owner) != b:
                    raise ValueError("invalid_journal_chain")
                if b.transition.receipt is not None and self._receipt(c, b.request.effect.effect_id) != b.transition.receipt:
                    raise ValueError("journal_durable_receipt_mismatch")
        return entries

    def trace(self, operation_id):
        with self.transaction() as c:
            return self._entries(c, operation_id)

    def head(self, operation_id):
        return self.trace(operation_id)[-1]

    def _append(self, c, entry):
        c.execute('INSERT INTO entries VALUES (?,?,?)', (entry.request.operation_id, entry.journal_version, canonical_json(entry)))

    def _conflict(self, c, request, writer, reason, wanted, head, observed=None):
        report = ConflictReport(operation_id=request.operation_id, request=request.identity(), writer=writer,
            reason=reason, expected_journal_version=wanted, observed_journal_version=head.journal_version,
            expected=request.expected, observed=observed)
        # Commit the conflict audit without losing or replacing the valid owner/head.
        c.execute('INSERT INTO conflicts(op,body) VALUES (?,?)', (request.operation_id, canonical_json(report)))
        return report

    def conflicts(self, operation_id):
        with self.transaction() as c:
            rows = c.execute('SELECT body FROM conflicts WHERE op=? ORDER BY sequence DESC LIMIT 128', (operation_id,)).fetchall()
            return tuple(parse_contract(ConflictReport, r[0]) for r in rows)

    def request(self, request):
        r = checked(OperationRequest, request)
        conflict = None
        with self.transaction() as c:
            row = c.execute('SELECT request FROM operations WHERE id=?', (r.operation_id,)).fetchone()
            if row:
                head = self._entries(c, r.operation_id)[-1]
                if parse_contract(OperationRequest, row[0]) != r:
                    conflict = self._conflict(c, r, r.actor.actor_id, 'request_payload_conflict', 0, head)
            else:
                c.execute('INSERT INTO operations VALUES (?,?,NULL)', (r.operation_id, canonical_json(r)))
                head = initial(r)
                self._append(c, head)
        if conflict:
            raise JournalConflict(conflict)
        return head

    def claim(self, operation_id, writer, expected_journal_version):
        conflict = None
        with self.transaction() as c:
            head = self._entries(c, operation_id)[-1]
            owner = owner_for(head.request, writer)
            row = c.execute('SELECT owner FROM operations WHERE id=?', (operation_id,)).fetchone()
            if row[0] is not None and row[0] != canonical_json(owner):
                conflict = self._conflict(c, head.request, writer, 'writer_conflict', expected_journal_version, head)
            elif expected_journal_version != head.journal_version:
                conflict = self._conflict(c, head.request, writer, 'journal_version_conflict', expected_journal_version, head)
            elif row[0] is None:
                c.execute('UPDATE operations SET owner=? WHERE id=? AND owner IS NULL', (canonical_json(owner), operation_id))
        if conflict:
            raise JournalConflict(conflict)
        return owner

    def move(self, operation_id, writer, transition, *, authorization=None, observed_context=None):
        conflict = None
        with self.transaction() as c:
            head = self._entries(c, operation_id)[-1]
            t = checked(StageTransition, transition)
            row = c.execute('SELECT owner FROM operations WHERE id=?', (operation_id,)).fetchone()
            owner = owner_for(head.request, writer)
            if row[0] != canonical_json(owner):
                conflict = self._conflict(c, head.request, writer, 'writer_conflict', t.expected_journal_version, head)
            elif t.expected_journal_version != head.journal_version or t.previous != head.identity():
                conflict = self._conflict(c, head.request, writer, 'journal_version_conflict', t.expected_journal_version, head)
            else:
                if t.stage in {'PREPARED', 'EFFECT_INTENT_RECORDED', 'EFFECT_ATTEMPTED'}:
                    qualify(head.request, authorization, observed_context)
                    observed = self._observed(c, head.request.expected)
                    if observed != head.request.expected:
                        conflict = self._conflict(c, head.request, writer, 'aggregate_version_conflict', t.expected_journal_version, head, observed)
                if conflict is None:
                    if t.receipt is not None:
                        # A self-consistent receipt object alone is not durable effect evidence.
                        stored = self._receipt(c, head.request.effect.effect_id)
                        if stored is None or stored != t.receipt:
                            raise ValueError('durable_receipt_missing_or_mismatched')
                    result = advance(head, t, owner)
                    self._append(c, result)
        if conflict:
            raise JournalConflict(conflict)
        return result

    def observe_effect(self, effect_id):
        with self.transaction() as c:
            return self._receipt(c, effect_id)

    def _receipt(self, c, effect_id):
        row = c.execute('SELECT attempt,payload,receipt FROM effects WHERE id=?', (effect_id,)).fetchone()
        if row is None:
            return None
        receipt = parse_contract(EffectReceipt, row[2])
        request_row = c.execute('SELECT request FROM operations WHERE id=?', (receipt.attempt.effect.operation_id,)).fetchone()
        if (request_row is None or receipt.attempt.effect.effect_id != effect_id
                or canonical_json(receipt.attempt) != row[0]
                or not verify_content_digest(row[1], receipt.attempt.effect.payload)):
            raise ValueError('durable_effect_record_mismatch')
        request = parse_contract(OperationRequest, request_row[0])
        verify_receipt(request, receipt.attempt.owner, receipt)
        return receipt

    def effect_count(self):
        with self.transaction() as c:
            return c.execute('SELECT count(*) FROM effects').fetchone()[0]
