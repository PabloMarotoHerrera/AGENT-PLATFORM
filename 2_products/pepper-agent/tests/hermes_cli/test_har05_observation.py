"""HAR-05 uses synthetic durable JSON and SQLite, never live authority."""

from dataclasses import replace
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.harness import (
    ActorRef, AuthorityCurrentness, AuthorityReference, ContentRef, ContractRef,
    ExecutionRequest, Scope, canonical_json, parse_contract, sha256_bytes,
)
from hermes_cli.agent_platform.harness.observation import (
    CheckStatus, Observation, ObservationPort, ObservationRequest, ObservationStatus,
    ObservedRecord, SourceKind, SourceRef,
)
from hermes_cli.agent_platform import observation_adapter as adapter
from hermes_cli.agent_platform.observation_adapter import (
    BoundObservationReader, RecordFormat, SourceBinding,
)


def request(source_id="source", format=RecordFormat.AUTHORITY_V1, version=1):
    kind = {RecordFormat.AUTHORITY_V1: SourceKind.AUTHORITY,
            RecordFormat.PROJECTION_V1: SourceKind.AUTHORITY,
            RecordFormat.EVIDENCE_JSON: SourceKind.EVIDENCE,
            RecordFormat.KANBAN_TASK: SourceKind.FACT}[format]
    return ObservationRequest(source=SourceRef(source_id=source_id, kind=kind,
        format=ContractRef(contract_id=format.value, version=version)),
        scope=Scope(project_id="project", workflow_id="ticket", resource_ids=("task",)),
        actor=ActorRef(actor_id="operator"))


def bind(tmp_path, req=None, format=RecordFormat.AUTHORITY_V1, components=("record.json",)):
    req = req or request(format=format)
    return SourceBinding(request=req, root=tmp_path, components=components,
        record_format=format, task_id="task" if format == RecordFormat.KANBAN_TASK else None)


def authority(req, currentness=AuthorityCurrentness.CURRENT):
    return AuthorityReference(authority_id="approval", kind="approval", issuer=req.actor,
        subject=req.actor, scope=req.scope, policy=ContractRef(contract_id="policy", version=1),
        record=ContentRef(content_id="approval-record", sha256="0"*64), dependencies=(),
        currentness=currentness)


def footprint(root):
    return {p.relative_to(root).as_posix(): ("dir" if p.is_dir() else p.read_bytes())
            for p in root.rglob("*") if not p.is_symlink()}


def write_authority(binding, **updates):
    data=json.loads(canonical_json(authority(binding.request)))
    data.update(updates)
    binding.path.write_text(json.dumps(data), encoding="utf-8")


def sqlite_source(tmp_path, *, wal=False, runs=1):
    b=bind(tmp_path, format=RecordFormat.KANBAN_TASK, components=("kanban.db",))
    conn=sqlite3.connect(b.path)
    if wal:
        assert conn.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
        conn.execute("PRAGMA wal_autocheckpoint=0")
    conn.executescript("CREATE TABLE tasks(id TEXT PRIMARY KEY,status TEXT,body TEXT);"
                       "CREATE TABLE task_runs(id INTEGER PRIMARY KEY,task_id TEXT,status TEXT,outcome TEXT,metadata TEXT);")
    body=json.dumps(dict(project_id="project",ticket_id="ticket",task_id="task"))
    conn.execute("INSERT INTO tasks VALUES(?,?,?)",("task","running",body))
    # An unrelated task must never be published merely because it shares a DB.
    conn.execute("INSERT INTO tasks VALUES(?,?,?)",("unrelated","secret",body))
    for i in range(runs):
        conn.execute("INSERT INTO task_runs VALUES(?,?,?,?,?)",(i+1,"task","running",None,'{"ticket_id":"ticket"}'))
    conn.commit()
    return b,conn


@pytest.mark.parametrize("format", list(RecordFormat))
def test_cold_missing_sources_and_missing_parents_stay_missing(tmp_path, format):
    cold=tmp_path/"never-created"/"nested"
    b=bind(cold,format=format)
    before=footprint(tmp_path)
    result=BoundObservationReader((b,)).observe_fact(b.request)
    assert result.status == ObservationStatus.ABSENT
    assert result.currentness == AuthorityCurrentness.UNVERIFIED
    assert not cold.exists()
    assert footprint(tmp_path)==before


@pytest.mark.parametrize("claim", (AuthorityCurrentness.CURRENT, AuthorityCurrentness.HISTORICAL,
                                   AuthorityCurrentness.UNVERIFIED))
def test_authority_integrity_structure_binding_and_currentness_are_distinct(tmp_path, claim):
    b=bind(tmp_path);write_authority(b,currentness=claim.value)
    before=footprint(tmp_path);reader=BoundObservationReader((b,))
    result=reader.observe_authority(b.request)
    assert result.status == ObservationStatus.PRESENT
    assert result.currentness == AuthorityCurrentness.UNVERIFIED
    assert result.authority.currentness == (AuthorityCurrentness.UNVERIFIED if claim == AuthorityCurrentness.CURRENT else claim)
    assert result.integrity == CheckStatus.UNVERIFIED
    assert result.structure == result.binding == CheckStatus.VERIFIED
    expected=ContentRef(content_id=b.request.source.source_id,sha256=sha256_bytes(b.path.read_bytes()))
    req=ObservationRequest(**{**dict(b.request),"expected_content":expected})
    assert reader.observe_authority(req).integrity == CheckStatus.VERIFIED
    assert canonical_json(reader.observe_authority(req))==canonical_json(reader.observe_authority(req))
    with pytest.raises(ValidationError):
        parse_contract(ExecutionRequest,canonical_json(result))
    assert footprint(tmp_path)==before


@pytest.mark.parametrize("raw,status", [
    (b"broken",ObservationStatus.INVALID),
    (b"{}",ObservationStatus.INVALID),
    (b'{"schema_version":true}',ObservationStatus.INVALID),
    (b'{"schema_version":2}',ObservationStatus.UNSUPPORTED),
    (b'{"schema_version":1,"schema_version":2}',ObservationStatus.INVALID),
    (b'{"schema_version":NaN}',ObservationStatus.INVALID),
    (b"["*17+b"]"*17,ObservationStatus.INVALID),
    (b"\xff",ObservationStatus.INVALID),
])
def test_malformed_old_and_unsupported_records_are_not_repaired(tmp_path,raw,status):
    b=bind(tmp_path);b.path.write_bytes(raw);before=footprint(tmp_path)
    result=BoundObservationReader((b,)).observe_authority(b.request)
    assert result.status == status
    assert result.authority is None
    assert result.completeness == "INCOMPLETE"
    assert footprint(tmp_path)==before


def test_record_and_request_scope_mismatches_and_tampering_fail_closed(tmp_path):
    b=bind(tmp_path);write_authority(b);reader=BoundObservationReader((b,))
    for key,val in (("project_id","other"),("workflow_id","other"),("resource_ids",("other",))):
        scope=Scope(**{**dict(b.request.scope),key:val})
        query=ObservationRequest(**{**dict(b.request),"scope":scope})
        assert reader.observe_authority(query).status == ObservationStatus.CONFLICT
    wrong=ObservationRequest(**{**dict(b.request),"actor":ActorRef(actor_id="other")})
    assert reader.observe_authority(wrong).status == ObservationStatus.CONFLICT
    expected=ContentRef(content_id="source",sha256="f"*64)
    bad=ObservationRequest(**{**dict(b.request),"expected_content":expected})
    assert reader.observe_authority(bad).reason_code == "content_digest_mismatch"
    write_authority(b,subject={"actor_id":"other"})
    assert reader.observe_authority(b.request).reason_code == "record_binding_conflict"


@pytest.mark.parametrize('field',('project','workflow','resource','actor','source'))
def test_unbound_requests_are_rejected_before_any_source_read(tmp_path,monkeypatch,field):
    b=bind(tmp_path);write_authority(b);data=dict(b.request)
    if field in ('project','workflow','resource'):
        key={'project':'project_id','workflow':'workflow_id','resource':'resource_ids'}[field]
        value=('other',) if field=='resource' else 'other'
        data['scope']=Scope(**{**dict(b.request.scope),key:value})
    elif field=='actor':data['actor']=ActorRef(actor_id='other')
    else:data['source']=request(source_id='other').source
    def forbidden_read(*args):raise AssertionError('unbound source was accessed')
    monkeypatch.setattr(adapter,'_capture',forbidden_read)
    result=BoundObservationReader((b,)).observe_fact(ObservationRequest(**data))
    assert result.status==ObservationStatus.CONFLICT


def test_projection_is_observed_without_claiming_domain_validation(tmp_path):
    b=bind(tmp_path,format=RecordFormat.PROJECTION_V1)
    data=dict(schema_version=1,policy_id="pepper-workpacket-kanban-projection-v1",
              project_id="project",ticket_id="ticket",kanban_task_id="task",
              next_action={"id":"START_ticket_EXECUTION"},approval_status="approved")
    b.path.write_text(json.dumps(data));before=footprint(tmp_path)
    result=BoundObservationReader((b,)).observe_authority(b.request)
    assert result.status == ObservationStatus.PRESENT
    assert result.structure == CheckStatus.UNVERIFIED
    assert result.authority is None
    assert result.currentness == AuthorityCurrentness.UNVERIFIED
    assert footprint(tmp_path)==before
    data['kanban_task_id']='other';b.path.write_text(json.dumps(data))
    assert BoundObservationReader((b,)).observe_authority(b.request).status == ObservationStatus.CONFLICT


def test_previous_allow_is_only_unverified_evidence(tmp_path):
    b=bind(tmp_path,format=RecordFormat.EVIDENCE_JSON)
    data=dict(schema_version=1,project_id="project",workflow_id="ticket",resource_ids=["task"],
              actor_id="operator",outcome="ALLOW",execution_authorized=True)
    b.path.write_text(json.dumps(data));before=footprint(tmp_path)
    result=BoundObservationReader((b,)).observe_fact(b.request)
    assert result.status == ObservationStatus.PRESENT
    assert result.structure == CheckStatus.UNVERIFIED
    assert result.authority is None and result.currentness == AuthorityCurrentness.UNVERIFIED
    assert BoundObservationReader((b,)).observe_authority(b.request).status == ObservationStatus.CONFLICT
    assert footprint(tmp_path)==before


@pytest.mark.parametrize("wal", (False,True))
def test_real_sqlite_observation_preserves_db_wal_shm_and_lifecycle(tmp_path,wal):
    b,conn=sqlite_source(tmp_path,wal=wal)
    try:
        before=footprint(tmp_path);reader=BoundObservationReader((b,))
        result=reader.observe_fact(b.request)
        assert result.status == ObservationStatus.PRESENT
        assert [r.record_id for r in result.records] == ["task","run:1"]
        assert result.records[0].state == "running"
        assert result.currentness == AuthorityCurrentness.UNVERIFIED
        assert canonical_json(reader.observe_fact(b.request)) == canonical_json(result)
        assert footprint(tmp_path)==before
        assert conn.execute("SELECT status FROM tasks WHERE id='task'").fetchone()[0] == "running"
    finally:conn.close()


def test_reading_wal_does_not_create_missing_shm(tmp_path):
    b,conn=sqlite_source(tmp_path,wal=True)
    # Copy only fixture DB/WAL while its fixture writer retains the originals.
    copy=tmp_path/"copy";copy.mkdir()
    copy.joinpath('kanban.db').write_bytes(b.path.read_bytes())
    copy.joinpath('kanban.db-wal').write_bytes(Path(str(b.path)+'-wal').read_bytes())
    binding=replace(b,root=copy);before=footprint(copy)
    try:
        assert BoundObservationReader((binding,)).observe_fact(binding.request).status == ObservationStatus.PRESENT
        assert not (copy/'kanban.db-shm').exists()
        assert footprint(copy)==before
    finally:conn.close()


@pytest.mark.parametrize("sidecar", ("database","wal","journal","orphan","shm"))
def test_corrupt_sidecars_or_database_are_not_repaired(tmp_path,sidecar):
    b,conn=sqlite_source(tmp_path);conn.close()
    if sidecar=='database':b.path.write_bytes(b'not sqlite')
    elif sidecar=='orphan':
        b.path.unlink();Path(str(b.path)+'-wal').write_bytes(b'broken')
    else:Path(str(b.path)+'-'+sidecar).write_bytes(b'broken')
    before=footprint(tmp_path);result=BoundObservationReader((b,)).observe_fact(b.request)
    # SHM is advisory and ignored by the immutable page reconstruction, not fixed.
    assert result.status == (ObservationStatus.PRESENT if sidecar=='shm' else ObservationStatus.INVALID)
    assert footprint(tmp_path)==before


def test_actual_image_reader_instability_is_preserved(tmp_path,monkeypatch):
    b,conn=sqlite_source(tmp_path);conn.close();before=footprint(tmp_path)
    original=adapter.evidence_sqlite._stamp;calls=0
    def unstable(path):
        nonlocal calls
        calls+=1
        value=original(path)
        return (*value[:-1],value[-1]+1) if value and calls>3 else value
    monkeypatch.setattr(adapter.evidence_sqlite,'_stamp',unstable)
    result=BoundObservationReader((b,)).observe_fact(b.request)
    assert result.status == ObservationStatus.UNSTABLE
    assert footprint(tmp_path)==before


def test_actual_durable_change_during_read_is_reported_not_reconciled(tmp_path,monkeypatch):
    b=bind(tmp_path);write_authority(b);original=adapter._json
    def change(raw):
        b.path.write_bytes(raw+b' ')
        return original(raw)
    monkeypatch.setattr(adapter,'_json',change)
    result=BoundObservationReader((b,)).observe_authority(b.request)
    assert result.status == ObservationStatus.UNSTABLE
    # The synthetic competing writer's bytes persist; observer did not restore them.
    assert b.path.read_bytes().endswith(b' ')


def test_size_record_count_and_query_budget_are_bounded(tmp_path,monkeypatch):
    b=bind(tmp_path);write_authority(b)
    monkeypatch.setattr(adapter,'MAX_JSON_BYTES',16)
    before=footprint(tmp_path)
    assert BoundObservationReader((b,)).observe_fact(b.request).reason_code == "source_size_bound"
    assert footprint(tmp_path)==before
    monkeypatch.undo()
    sql,conn=sqlite_source(tmp_path,runs=32);conn.close();before=footprint(tmp_path)
    assert BoundObservationReader((sql,)).observe_fact(sql.request).reason_code == "record_count_bound"
    assert footprint(tmp_path)==before
    monkeypatch.setattr(adapter,'MAX_SOURCE_BYTES',16)
    assert BoundObservationReader((sql,)).observe_fact(sql.request).reason_code == "source_size_bound"


def test_query_step_budget_and_io_failure_preserve_sources(tmp_path,monkeypatch):
    b,conn=sqlite_source(tmp_path,runs=1);conn.close()
    # Enough unrelated rows to exercise the real VM progress callback.
    conn=sqlite3.connect(b.path)
    conn.executemany("INSERT INTO task_runs VALUES(?,?,?,?,?)",[(i,'other','done',None,'{}') for i in range(2,1002)])
    conn.commit();conn.close();before=footprint(tmp_path)
    monkeypatch.setattr(adapter,'MAX_SQL_STEPS',0)
    assert BoundObservationReader((b,)).observe_fact(b.request).status == ObservationStatus.UNAVAILABLE
    assert footprint(tmp_path)==before
    monkeypatch.undo()
    def denied(*args):raise PermissionError('synthetic denial')
    monkeypatch.setattr(adapter,'_capture',denied)
    assert BoundObservationReader((b,)).observe_fact(b.request).status == ObservationStatus.UNAVAILABLE
    assert footprint(tmp_path)==before


@pytest.mark.parametrize("components", (("..",),("/absolute",),("a/b",),("C:drive",),(".",),(),("a",)*9))
def test_source_path_escape_is_rejected(tmp_path,components):
    with pytest.raises(ValueError):bind(tmp_path,components=components)


def test_symlinks_and_unbound_sources_cannot_expand_scope(tmp_path):
    outside=tmp_path/'outside';outside.mkdir();b=bind(outside);write_authority(b)
    link=tmp_path/'redirect'
    try:link.symlink_to(outside,target_is_directory=True)
    except OSError:pytest.skip('symlinks unavailable on this test substrate')
    redirect=replace(b,root=link)
    assert BoundObservationReader((redirect,)).observe_fact(redirect.request).reason_code == 'source_redirect'
    unknown=request(source_id='unknown')
    assert BoundObservationReader((b,)).observe_fact(unknown).reason_code == 'source_scope_not_bound'
    assert list(outside.iterdir()) == [b.path]


def test_related_reads_are_explicit_and_depth_one(tmp_path):
    b=bind(tmp_path);write_authority(b)
    second=bind(tmp_path,req=request(source_id='related'),components=('related.json',))
    reader: ObservationPort=BoundObservationReader((b,second))
    req=ObservationRequest(**{**dict(b.request),'related_sources':(second.request.source,)})
    result=reader.observe_related(req)
    assert len(result)==1 and result[0].status == ObservationStatus.ABSENT
    assert not second.path.exists()
    assert reader.observe_related(b.request)==()
    with pytest.raises(ValueError):BoundObservationReader((b,b))
    with pytest.raises(ValueError):BoundObservationReader((b,)*17)
    with pytest.raises(ValidationError):
        ObservationRequest(**{**dict(b.request),'related_sources':(b.request.source,)})


def test_unsupported_database_and_scope_conflicts_fail_closed(tmp_path):
    b,conn=sqlite_source(tmp_path)
    conn.execute("UPDATE tasks SET body='{}' WHERE id='task'");conn.commit();conn.close()
    before=footprint(tmp_path)
    assert BoundObservationReader((b,)).observe_fact(b.request).reason_code=='task_binding_conflict'
    assert footprint(tmp_path)==before
    conn=sqlite3.connect(b.path);conn.execute('DROP TABLE task_runs');conn.commit();conn.close()
    before=footprint(tmp_path)
    assert BoundObservationReader((b,)).observe_fact(b.request).status==ObservationStatus.UNSUPPORTED
    assert footprint(tmp_path)==before


@pytest.mark.parametrize('table,column,value',(('tasks','body',b'{}'),
                                               ('task_runs','metadata',b'{}'),
                                               ('task_runs','metadata',None)))
def test_malformed_sqlite_json_column_types_are_qualified_failures(tmp_path,table,column,value):
    b,conn=sqlite_source(tmp_path)
    conn.execute(f'UPDATE {table} SET {column}=?',(value,));conn.commit();conn.close()
    before=footprint(tmp_path)
    result=BoundObservationReader((b,)).observe_fact(b.request)
    assert result.status==ObservationStatus.INVALID
    assert footprint(tmp_path)==before


def test_all_observation_models_are_strict_immutable_versioned_roundtrippable():
    req=request();ref=ContentRef(content_id='source',sha256='0'*64)
    record=ObservedRecord(record_id='record',content=ref)
    obs=Observation(source=req.source,scope=req.scope,actor=req.actor,
        status=ObservationStatus.ABSENT,reason_code='absent')
    for model in (req.source,req,record,obs):
        assert parse_contract(type(model),canonical_json(model))==model
        for update in ({'schema_version':2},{'schema_version':True},{'execute':lambda:True}):
            with pytest.raises(ValidationError):type(model).model_validate({**dict(model),**update})
        with pytest.raises(ValidationError):model.schema_version=2
    for update in ({'currentness':AuthorityCurrentness.CURRENT},{'observational':False},
                   {'status':ObservationStatus.PRESENT},{'records':(record,)}):
        with pytest.raises(ValidationError):Observation.model_validate({**dict(obs),**update})


def test_port_accepts_injected_readers_without_starting_product_runtime():
    req=request()
    class SyntheticReader:
        def __init__(self, observation):self.observation=observation
        def observe_fact(self, request):return self.observation
        def observe_authority(self, request):return self.observation
        def observe_related(self, request):return ()
    for status in ObservationStatus:
        fields=dict(source=req.source,scope=req.scope,actor=req.actor,status=status,reason_code='synthetic')
        if status==ObservationStatus.PRESENT:
            fields.update(source_content=ContentRef(content_id='source',sha256='0'*64),
                binding=CheckStatus.VERIFIED,consistency='STABLE_CAPTURE',completeness='BOUND_SOURCE_ONLY')
        reader: ObservationPort=SyntheticReader(Observation(**fields))
        assert reader.observe_fact(req).status==status
        assert reader.observe_authority(req).currentness==AuthorityCurrentness.UNVERIFIED
        assert reader.observe_related(req)==()


def test_observation_port_import_remains_pure_in_fresh_process(tmp_path):
    # Reuse the accepted HAR-04 behavioral guard, without editing its tests.
    from tests.hermes_cli.test_har04_harness_purity import PROBE
    code=PROBE+'\nfrom hermes_cli.agent_platform.harness.observation import ObservationRequest, ObservationPort\n'
    home=tmp_path/'probe';home.mkdir()
    result=subprocess.run([sys.executable,'-I','-B','-c',code,str(Path(__file__).resolve().parents[2])],
        cwd=home,env={'HOME':str(home),'HERMES_HOME':str(home/'hermes'),'PATH':os.defpath,'LANG':'C.UTF-8'},
        text=True,capture_output=True,timeout=30)
    assert result.returncode==0,result.stderr
    assert list(home.iterdir())==[]


def test_fresh_adapter_observation_cannot_initialize_dispatch_or_use_provider(tmp_path):
    b,conn=sqlite_source(tmp_path,wal=True)
    json_binding=bind(tmp_path,req=request(source_id='authority'));write_authority(json_binding)
    before=footprint(tmp_path)
    code=r'''
import builtins, importlib.abc, os, sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
original=builtins.__import__
allowed={"hermes_cli","hermes_cli.agent_platform","hermes_cli.agent_platform.evidence_sqlite",
         "hermes_cli.agent_platform.observation_adapter"}
class ImportGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in {"tools","model_tools","openai","anthropic","litellm","docker"}:
            raise RuntimeError('runtime/provider dynamic import forbidden')
        if fullname.startswith('hermes_cli') and fullname not in allowed and not fullname.startswith('hermes_cli.agent_platform.harness'):
            raise RuntimeError('private runtime dynamic import forbidden: '+fullname)
        return None
def guard(name,globals=None,locals=None,fromlist=(),level=0):
    if name.split('.')[0] in {"tools","model_tools","openai","anthropic","litellm","docker"}:
        raise RuntimeError("runtime/provider import forbidden")
    if name.startswith('hermes_cli') and name not in allowed and not name.startswith('hermes_cli.agent_platform.harness'):
        raise RuntimeError("private runtime import forbidden: "+name)
    return original(name,globals,locals,fromlist,level)
def audit(event,args):
    if event=='open':
        mode,flags=args[1:3]
        if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):
            raise RuntimeError('write forbidden')
    if event=='sqlite3.connect' and args[0] != ':memory:':
        raise RuntimeError('disk SQLite connection forbidden')
    if event.startswith(('socket.','subprocess.','os.spawn','os.exec')) or event in {'os.mkdir','os.remove','os.rename','os.system','os.chmod','os.symlink','os.link'}:
        raise RuntimeError('external effect forbidden: '+event)
builtins.__import__=guard
sys.meta_path.insert(0,ImportGuard())
sys.addaudithook(audit)
from hermes_cli.agent_platform.harness import parse_contract,canonical_json
from hermes_cli.agent_platform.harness.observation import ObservationRequest,ObservationStatus
from hermes_cli.agent_platform.observation_adapter import BoundObservationReader,SourceBinding,RecordFormat
root=Path(sys.argv[2]);sql=parse_contract(ObservationRequest,sys.argv[3]);auth=parse_contract(ObservationRequest,sys.argv[4])
reader=BoundObservationReader((SourceBinding(sql,root,('kanban.db',),RecordFormat.KANBAN_TASK,'task'),
                               SourceBinding(auth,root,('record.json',),RecordFormat.AUTHORITY_V1)))
for request in (sql,auth):
    a=reader.observe_fact(request);b=reader.observe_fact(request)
    assert a.status==ObservationStatus.PRESENT
    assert canonical_json(a)==canonical_json(b)
cold=BoundObservationReader((SourceBinding(sql,root/'missing'/'parent',('kanban.db',),RecordFormat.KANBAN_TASK,'task'),))
assert cold.observe_fact(sql).status==ObservationStatus.ABSENT
print('HAR05_NO_EFFECTS')
'''
    home=tmp_path/'cold-home'
    try:
        result=subprocess.run([sys.executable,'-I','-B','-c',code,str(Path(__file__).resolve().parents[2]),
            str(tmp_path),canonical_json(b.request),canonical_json(json_binding.request)],cwd=tmp_path,
            env={'HOME':str(home),'HERMES_HOME':str(home/'hermes'),'PATH':os.defpath,'LANG':'C.UTF-8'},
            text=True,capture_output=True,timeout=30)
        assert result.returncode==0,result.stderr
        assert result.stdout.strip()=='HAR05_NO_EFFECTS'
        assert not home.exists()
        assert footprint(tmp_path)==before
    finally:conn.close()
