"""Explicitly bound Pepper reads; no runtime/bootstrap imports or live discovery.

The trusted local caller supplies every source, scope and actor. No environment
variable, default home, directory search, registry or writable fallback is used.
Legacy projection checking covers its header/bindings only, not domain validity.
"""

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import stat

from . import evidence_sqlite
from .harness import AuthorityCurrentness, AuthorityReference, ContentRef, canonical_json, parse_contract
from .harness.observation import (
    CheckStatus, Observation, ObservationRequest, ObservationStatus, ObservedRecord,
    SourceKind,
)

MAX_SOURCE_BYTES = 16 * 1024 * 1024  # per DB/sidecar, pre/post capture
MAX_JSON_BYTES = 1_048_576
MAX_SOURCES = 16
MAX_RECORDS = 32  # includes the task itself
MAX_JSON_DEPTH = 16
MAX_SQL_STEPS = 100_000
_COMPONENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


class RecordFormat(str, Enum):
    AUTHORITY_V1 = "harness-authority"
    PROJECTION_V1 = "pepper-projection"
    EVIDENCE_JSON = "json-evidence"
    KANBAN_TASK = "kanban-task"


@dataclass(frozen=True)
class SourceBinding:
    request: ObservationRequest
    root: Path
    components: tuple[str, ...]
    record_format: RecordFormat
    task_id: str | None = None

    def __post_init__(self):
        # Revalidate unchecked copies at this trusted adapter boundary as well.
        parse_contract(ObservationRequest, canonical_json(self.request))
        if (not isinstance(self.root, Path) or not self.root.is_absolute()
                or ".." in self.root.parts or not isinstance(self.components, tuple)
                or not 1 <= len(self.components) <= 8
                or any(not isinstance(p, str) or not _COMPONENT.fullmatch(p) for p in self.components)):
            raise ValueError("explicit absolute root and bounded literal path components required")
        if not isinstance(self.record_format, RecordFormat):
            raise ValueError("unsupported binding format")
        if self.request.related_sources or self.request.expected_content:
            raise ValueError("binding declares identity/scope only, not an observation query")
        expected_kind = {RecordFormat.AUTHORITY_V1: SourceKind.AUTHORITY,
                         RecordFormat.PROJECTION_V1: SourceKind.AUTHORITY,
                         RecordFormat.EVIDENCE_JSON: SourceKind.EVIDENCE,
                         RecordFormat.KANBAN_TASK: SourceKind.FACT}[self.record_format]
        if (self.request.source.kind != expected_kind
                or self.request.source.format.contract_id != self.record_format.value):
            raise ValueError("source kind/format mismatch")
        if self.record_format == RecordFormat.KANBAN_TASK:
            if (not isinstance(self.task_id, str) or not _COMPONENT.fullmatch(self.task_id)
                    or self.request.scope.resource_ids != (self.task_id,)):
                raise ValueError("task observation requires exactly its bound resource")
        elif self.task_id is not None:
            raise ValueError("task selector is only valid for a Kanban source")

    @property
    def path(self) -> Path:
        return self.root.joinpath(*self.components)


class _ReadFailure(Exception):
    def __init__(self, status, reason):
        self.status, self.reason = status, reason


def _stamp(path):
    # No resolution through symlinks, even if the target would remain in root.
    for part in (path, *path.parents):
        if part.is_symlink():
            raise _ReadFailure(ObservationStatus.CONFLICT, "source_redirect")
    try:
        info = path.stat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode):
        raise _ReadFailure(ObservationStatus.INVALID, "source_not_regular")
    if info.st_size > MAX_SOURCE_BYTES:
        raise _ReadFailure(ObservationStatus.UNAVAILABLE, "source_size_bound")
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def _capture(paths, limit):
    before = tuple(_stamp(p) for p in paths)
    contents = []
    for path, stamp in zip(paths, before):
        if stamp is None:
            contents.append(None)
        else:
            with path.open("rb") as stream:
                raw = stream.read(limit + 1)
            if len(raw) > limit:
                raise _ReadFailure(ObservationStatus.UNAVAILABLE, "source_size_bound")
            contents.append(raw)
    if before != tuple(_stamp(p) for p in paths):
        raise _ReadFailure(ObservationStatus.UNSTABLE, "source_changed")
    return before, tuple(contents)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _json(raw):
    # A depth scan precedes parsing, handles quoted/escaped braces, and bounds
    # nesting independently of the Python interpreter recursion limit.
    depth, quoted, escaped = 0, False, False
    for char in raw.decode("utf-8"):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise ValueError("JSON depth bound")
        elif char in "]}":
            depth -= 1
    def invalid_constant(value):
        raise ValueError("nonfinite JSON constant")
    result = json.loads(raw, object_pairs_hook=_pairs, parse_constant=invalid_constant)
    if not isinstance(result, dict):
        raise ValueError("record must be a JSON object")
    return result


def _content(identity, raw):
    return ContentRef(content_id=identity, sha256=hashlib.sha256(raw).hexdigest())


def _json_column(value):
    if not isinstance(value, str):
        raise ValueError("JSON column must contain text")
    return _json(value.encode("utf-8"))


def _record(identity, data, state=None):
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return ObservedRecord(record_id=identity, content=_content(identity, raw), state=state)


class BoundObservationReader:
    """At most 16 sources, fixed table queries, depth-one explicit related reads.

    Existing immutable DB/WAL reconstruction is retained unchanged. Pre/post
    captures include SHM/journal bytes; SHM is advisory and is never trusted as
    page authority. There is no global multi-source transaction or future grant.
    """

    def __init__(self, bindings: tuple[SourceBinding, ...]):
        if (not isinstance(bindings, tuple) or not 1 <= len(bindings) <= MAX_SOURCES
                or any(not isinstance(b, SourceBinding) for b in bindings)
                or len({b.request.source.source_id for b in bindings}) != len(bindings)):
            raise ValueError("bounded unique explicit source bindings required")
        self._bindings = tuple(bindings)

    def _binding(self, request):
        for binding in self._bindings:
            base = binding.request
            if (base.source == request.source and base.scope == request.scope
                    and base.actor == request.actor):
                return binding
        raise _ReadFailure(ObservationStatus.CONFLICT, "source_scope_not_bound")

    def observe_fact(self, request: ObservationRequest) -> Observation:
        request = parse_contract(ObservationRequest, canonical_json(request))
        try:
            binding = self._binding(request)
            if request.source.format.version != 1:
                raise _ReadFailure(ObservationStatus.UNSUPPORTED, "unsupported_source_version")
            if binding.record_format == RecordFormat.KANBAN_TASK:
                return self._sqlite(binding, request)
            return self._file(binding, request)
        except _ReadFailure as exc:
            return self._failure(request, exc.status, exc.reason)
        except (OSError, sqlite3.Error):
            return self._failure(request, ObservationStatus.UNAVAILABLE, "source_io_unavailable")
        except (ValueError, UnicodeError, RecursionError):
            return self._failure(request, ObservationStatus.INVALID, "source_invalid")

    def observe_authority(self, request: ObservationRequest) -> Observation:
        if request.source.kind != SourceKind.AUTHORITY:
            return self._failure(request, ObservationStatus.CONFLICT, "authority_source_required")
        return self.observe_fact(request)

    def observe_related(self, request: ObservationRequest) -> tuple[Observation, ...]:
        request = parse_contract(ObservationRequest, canonical_json(request))
        try:
            self._binding(request)
        except _ReadFailure as exc:
            return (self._failure(request, exc.status, exc.reason),)
        # No graph walk, discovery, inherited expected digest or recursive query.
        return tuple(self.observe_fact(ObservationRequest(source=source, scope=request.scope,
                     actor=request.actor)) for source in request.related_sources)

    @staticmethod
    def _failure(request, status, reason):
        return Observation(source=request.source, scope=request.scope, actor=request.actor,
                           status=status, reason_code=reason)

    @staticmethod
    def _present(request, content, **fields):
        integrity = CheckStatus.UNVERIFIED
        if request.expected_content:
            if content != request.expected_content:
                raise _ReadFailure(ObservationStatus.CONFLICT, "content_digest_mismatch")
            integrity = CheckStatus.VERIFIED
        return Observation(source=request.source, scope=request.scope, actor=request.actor,
            status=ObservationStatus.PRESENT, reason_code="bound_source_observed",
            source_content=content, integrity=integrity, binding=CheckStatus.VERIFIED,
            consistency="STABLE_CAPTURE", completeness="BOUND_SOURCE_ONLY", **fields)

    def _file(self, binding, request):
        paths = (binding.path,)
        before, contents = _capture(paths, MAX_JSON_BYTES)
        if contents[0] is None:
            if _capture(paths, MAX_JSON_BYTES) != (before, contents):
                raise _ReadFailure(ObservationStatus.UNSTABLE, "source_changed")
            return self._failure(request, ObservationStatus.ABSENT, "source_absent")
        raw = contents[0]
        try:
            data = _json(raw)
            version = data.get("schema_version")
            if type(version) is not int or version < 1:
                raise ValueError("missing/invalid schema version")
            if version != 1:
                raise _ReadFailure(ObservationStatus.UNSUPPORTED, "unsupported_record_version")
            authority = None
            structure = CheckStatus.UNVERIFIED
            if binding.record_format == RecordFormat.AUTHORITY_V1:
                claim = parse_contract(AuthorityReference, raw)
                if claim.scope != request.scope or claim.subject != request.actor:
                    raise _ReadFailure(ObservationStatus.CONFLICT, "record_binding_conflict")
                # Preserve the original bytes; qualify only the new observation.
                authority = claim if claim.currentness != AuthorityCurrentness.CURRENT else AuthorityReference.model_validate(
                    {**dict(claim), "currentness": AuthorityCurrentness.UNVERIFIED})
                structure = CheckStatus.VERIFIED
            elif binding.record_format == RecordFormat.PROJECTION_V1:
                if data.get("policy_id") != "pepper-workpacket-kanban-projection-v1":
                    raise _ReadFailure(ObservationStatus.UNSUPPORTED, "unsupported_record_policy")
                if (data.get("project_id") != request.scope.project_id
                        or data.get("ticket_id") != request.scope.workflow_id
                        or request.scope.resource_ids != (data.get("kanban_task_id"),)):
                    raise _ReadFailure(ObservationStatus.CONFLICT, "record_binding_conflict")
                # Full legacy schema/digest/dependency interpretation stays with
                # future domain adapters; a matching header is not full validity.
            else:
                if (data.get("project_id") != request.scope.project_id
                        or data.get("workflow_id") != request.scope.workflow_id
                        or data.get("resource_ids") != list(request.scope.resource_ids)
                        or data.get("actor_id") != request.actor.actor_id):
                    raise _ReadFailure(ObservationStatus.CONFLICT, "record_binding_conflict")
            return self._present(request, _content(request.source.source_id, raw),
                observed_schema_version=version, authority=authority, structure=structure)
        finally:
            if _capture(paths, MAX_JSON_BYTES) != (before, contents):
                raise _ReadFailure(ObservationStatus.UNSTABLE, "source_changed")

    def _sqlite(self, binding, request):
        path = binding.path
        paths = (path, Path(str(path)+"-wal"), Path(str(path)+"-shm"), Path(str(path)+"-journal"))
        before, contents = _capture(paths, MAX_SOURCE_BYTES)
        if contents[0] is None:
            if any(c is not None for c in contents[1:]):
                raise _ReadFailure(ObservationStatus.INVALID, "orphan_database_sidecars")
            if _capture(paths, MAX_SOURCE_BYTES) != (before, contents):
                raise _ReadFailure(ObservationStatus.UNSTABLE, "source_changed")
            return self._failure(request, ObservationStatus.ABSENT, "database_absent")
        conn = None
        try:
            # Never kb.connect(), mode=ro on live files, or a writable fallback.
            conn = evidence_sqlite.connect(path)
            conn.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, MAX_JSON_BYTES)
            conn.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 4096)
            ticks = 0
            def budget():
                nonlocal ticks
                ticks += 1000
                return int(ticks > MAX_SQL_STEPS)
            conn.set_progress_handler(budget, 1000)
            types = dict(conn.execute("SELECT name,type FROM sqlite_master WHERE name IN ('tasks','task_runs')"))
            if types != {"tasks": "table", "task_runs": "table"}:
                raise _ReadFailure(ObservationStatus.UNSUPPORTED, "unsupported_database_schema")
            def authorize(action, table, column, db, trigger):
                return sqlite3.SQLITE_OK if (action == sqlite3.SQLITE_SELECT or
                    action == sqlite3.SQLITE_READ and table in {"tasks", "task_runs"}) else sqlite3.SQLITE_DENY
            conn.set_authorizer(authorize)
            task = conn.execute("SELECT id,status,body FROM tasks WHERE id=?", (binding.task_id,)).fetchall()
            if len(task) != 1:
                raise _ReadFailure(ObservationStatus.ABSENT if not task else ObservationStatus.CONFLICT,
                                   "task_absent" if not task else "duplicate_task")
            body = _json_column(task[0]["body"])
            if (body.get("project_id") != request.scope.project_id
                    or body.get("ticket_id") != request.scope.workflow_id
                    or body.get("task_id") != binding.task_id):
                raise _ReadFailure(ObservationStatus.CONFLICT, "task_binding_conflict")
            runs = conn.execute("SELECT id,task_id,status,outcome,metadata FROM task_runs WHERE task_id=? ORDER BY id LIMIT ?",
                                (binding.task_id, MAX_RECORDS)).fetchall()
            if len(runs) >= MAX_RECORDS:
                raise _ReadFailure(ObservationStatus.UNAVAILABLE, "record_count_bound")
            records = [_record(binding.task_id, dict(task[0]), task[0]["status"])]
            for run in runs:
                metadata = _json_column(run["metadata"])
                if metadata.get("ticket_id") != request.scope.workflow_id:
                    raise _ReadFailure(ObservationStatus.CONFLICT, "run_binding_unresolved")
                records.append(_record(f"run:{run['id']}", dict(run), run["status"]))
            # Domain-separated framing preserves distinction between missing and
            # empty files. This new capture digest does not replace legacy hashes.
            digest = hashlib.sha256(b"harness-observation-sqlite-capture-v1\0")
            for raw in contents:
                digest.update(b"absent\0" if raw is None else str(len(raw)).encode()+b":"+raw)
            return self._present(request, ContentRef(content_id=request.source.source_id,
                sha256=digest.hexdigest()), records=tuple(records))
        except ValueError as exc:
            if "changed while reading" in str(exc):
                raise _ReadFailure(ObservationStatus.UNSTABLE, "source_changed") from exc
            raise
        finally:
            if conn is not None:
                conn.close()
            if _capture(paths, MAX_SOURCE_BYTES) != (before, contents):
                raise _ReadFailure(ObservationStatus.UNSTABLE, "source_changed")
