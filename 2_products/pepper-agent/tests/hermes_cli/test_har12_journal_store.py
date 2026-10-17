from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from hermes_cli.agent_platform.harness.operation_journal import JournalEntry
from hermes_cli.agent_platform.harness.validation import canonical_json
from hermes_cli.agent_platform.isolated_effect_adapter import transition
from hermes_cli.agent_platform.isolated_operation_journal import IsolatedJournal, JournalConflict
from tests.hermes_cli.test_har12_operation_journal import case, change


def prepared(tmp_path, stage='EFFECT_INTENT_RECORDED'):
    r,q,p=case();s=IsolatedJournal.create_disposable(tmp_path);s.initialize_aggregate(r.expected)
    h=s.request(r);o=s.claim(r.operation_id,'writer-a',h.journal_version)
    for target in ('PREPARED','EFFECT_INTENT_RECORDED'):
        h=s.move(r.operation_id,'writer-a',transition(h,target),authorization=q,observed_context=r.context)
        if stage==target:break
    return s,r,q,p,h,o


def test_explicit_initialization_and_durable_readback(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path)
    assert s.root.parent==tmp_path and s.path.is_file()
    assert s.reconnect().head(r.operation_id)==h
    assert len(s.trace(r.operation_id))==3 and not s.conflicts(r.operation_id)
    with pytest.raises(ValueError):IsolatedJournal(tmp_path,None)


def test_identical_request_is_idempotent_but_conflicting_payload_audited(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path)
    assert s.request(r)==h
    r2=change(r,effect=change(r.effect,payload=change(r.effect.payload,sha256='b'*64)))
    with pytest.raises(JournalConflict):s.request(r2)
    assert s.head(r.operation_id)==h and s.conflicts(r.operation_id)[0].reason=='request_payload_conflict'


def test_conflicting_writer_does_not_replace_owner_or_head(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path)
    with pytest.raises(JournalConflict):s.claim(r.operation_id,'writer-b',h.journal_version)
    assert s.claim(r.operation_id,'writer-a',h.journal_version)==o
    assert s.reconnect().head(r.operation_id)==h


def test_independent_connections_race_for_one_owner(tmp_path):
    r,q,p=case();s=IsolatedJournal.create_disposable(tmp_path);s.initialize_aggregate(r.expected);h=s.request(r);barrier=Barrier(2)
    def claim(name):
        peer=s.reconnect();barrier.wait()
        try:return peer.claim(r.operation_id,name,h.journal_version).writer
        except JournalConflict:return 'conflict'
    with ThreadPoolExecutor(max_workers=2) as pool:out=list(pool.map(claim,('writer-a','writer-b')))
    assert out.count('conflict')==1 and len(s.conflicts(r.operation_id))==1


def test_stale_journal_revision_and_aggregate_version_no_effect(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path,stage='PREPARED')
    stale=transition(s.trace(r.operation_id)[0],'PREPARED')
    with pytest.raises(JournalConflict):s.move(r.operation_id,'writer-a',stale,authorization=q,observed_context=r.context)
    with s.transaction() as c:c.execute('UPDATE aggregates SET body=?',(canonical_json(change(r.expected,value=1)),))
    with pytest.raises(JournalConflict) as e:s.move(r.operation_id,'writer-a',transition(h,'EFFECT_INTENT_RECORDED'),authorization=q,observed_context=r.context)
    assert e.value.report.reason=='aggregate_version_conflict' and not s.effect_count()
    assert s.head(r.operation_id)==h and s.head(r.operation_id).request.expected.value==0


def test_sql_transaction_rollback_is_real(tmp_path):
    r,_,_=case();s=IsolatedJournal.create_disposable(tmp_path);s.initialize_aggregate(r.expected)
    with pytest.raises(RuntimeError):
        with s.transaction() as c:
            c.execute('UPDATE aggregates SET body=?',(canonical_json(change(r.expected,value=1)),))
            raise RuntimeError('before-commit')
    assert s.reconnect().observe_version(r.expected)==r.expected


def test_unknown_schema_and_corrupt_predecessor_fail_closed(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path)
    with s.transaction() as c:c.execute('UPDATE entries SET body=? WHERE revision=?',(canonical_json(change(h,predecessor=change(h.predecessor,sha256='b'*64),transition=change(h.transition,previous=change(h.predecessor,sha256='b'*64)))),h.journal_version))
    with pytest.raises(ValueError):s.head(r.operation_id)
    peer=IsolatedJournal.create_disposable(tmp_path)
    with peer.transaction() as c:c.execute('PRAGMA user_version=2')
    with pytest.raises(ValueError):peer.trace('missing')


def test_resource_scope_cannot_alias_aggregate(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path)
    with pytest.raises(ValueError):s.observe_version(change(r.expected,scope=change(r.expected.scope,project_id='other')))


def test_interrupted_owner_is_never_reclaimed(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path)
    peer=s.reconnect()
    with pytest.raises(JournalConflict):peer.claim(r.operation_id,'replacement-writer',h.journal_version)
    assert peer.head(r.operation_id)==h


def test_disposable_destination_is_not_retargetable_via_public_attributes(tmp_path):
    s,r,q,p,h,o=prepared(tmp_path)
    with pytest.raises(AttributeError):s.path=tmp_path/'foreign.sqlite3'
    with pytest.raises(AttributeError):s.root=tmp_path


def test_foreign_receipt_cannot_be_injected_by_a_dispatch_callback(tmp_path):
    from hermes_cli.agent_platform.isolated_effect_adapter import IsolatedAppendAdapter
    with pytest.raises(TypeError):IsolatedAppendAdapter().apply(object(),None,b'',authorization=None,observed_context=None)
