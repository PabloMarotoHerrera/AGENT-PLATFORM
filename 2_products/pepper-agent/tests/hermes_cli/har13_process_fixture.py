"""Child-only fixture driver; never imported by production recovery code."""
import json
import os
from pathlib import Path
import sqlite3
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from hermes_cli.agent_platform.isolated_operation_journal import IsolatedJournal, _CREATED, JournalConflict
from hermes_cli.agent_platform.isolated_effect_adapter import IsolatedAppendAdapter, attempt_for, transition, run_fixture
from hermes_cli.agent_platform.isolated_journal_recovery import read_snapshot
from hermes_cli.agent_platform.harness.journal_recovery import assess_recovery
from hermes_cli.agent_platform.harness.replay_policy import assess_replay
from hermes_cli.agent_platform.harness.validation import canonical_json
from tests.hermes_cli.test_har12_operation_journal import case, change, content


def gate(window,root):
    print(json.dumps(dict(ready=True,pid=os.getpid(),window=window,root=str(root))),flush=True)
    if sys.stdin.readline()!='continue\n':
        raise RuntimeError('fixture_parent_not_present')


def derived(which='first',same_key=False):
    r,q,p=case()
    if which=='second':
        r=change(r,operation_id='second-operation',effect=change(r.effect,operation_id='second-operation',
            effect_id=r.effect.effect_id if same_key else 'second-effect'))
        q=change(q,request=r.identity())
    return r,q,p


def drive(root,window):
    r,q,p=case();s=IsolatedJournal(root,_CREATED)
    original=sqlite3.connect
    class Proxy:
        def __init__(self,c):self.c=c;self.effect=False
        def __getattr__(self,k):return getattr(self.c,k)
        def execute(self,sql,args=()):
            if window=='W06' and sql.startswith('UPDATE aggregates SET body='):gate(window,root)
            result=self.c.execute(sql,args)
            if sql.startswith('INSERT INTO effects'):
                self.effect=True
                if window=='W07':gate(window,root)
            if window=='W11' and sql.startswith('INSERT INTO conflicts'):gate(window,root)
            return result
        def commit(self):
            self.c.commit()
            if window=='W08' and self.effect:gate(window,root)
    sqlite3.connect=lambda *a,**k:Proxy(original(*a,**k))
    if window=='W00':gate(window,root)
    h=s.request(r)
    if window=='W01':gate(window,root)
    owner=s.claim(r.operation_id,'writer-a',h.journal_version)
    if window=='W02':gate(window,root)
    if window=='W11':s.claim(r.operation_id,'writer-b',h.journal_version)
    for stage,w in [('PREPARED','W03'),('EFFECT_INTENT_RECORDED','W04')]:
        h=s.move(r.operation_id,owner.writer,transition(h,stage),authorization=q,observed_context=r.context)
        if window==w:gate(window,root)
    attempt=attempt_for(r,owner,'first-attempt')
    h=s.move(r.operation_id,owner.writer,transition(h,'EFFECT_ATTEMPTED',attempt=attempt),authorization=q,observed_context=r.context)
    if window=='W05':gate(window,root)
    receipt=IsolatedAppendAdapter().apply(s,attempt,p,authorization=q,observed_context=r.context)
    h=s.move(r.operation_id,owner.writer,transition(h,'EFFECT_CONFIRMED',attempt=attempt,receipt=receipt))
    if window=='W09':gate(window,root)
    h=s.move(r.operation_id,owner.writer,transition(h,'COMPLETED',attempt=attempt,receipt=receipt))
    if window=='W10':gate(window,root)


def main():
    action,root=sys.argv[1],Path(sys.argv[2]).resolve(strict=True)
    # Every process receives the exact newly-created disposable root explicitly.
    assert root.name.startswith('har12-disposable-')
    def audit(event,args):
        if event.startswith(('socket.','subprocess.')):raise RuntimeError('forbidden fixture effect '+event)
    sys.addaudithook(audit)
    if action=='crash':drive(root,sys.argv[3]);return
    r,q,p=derived(sys.argv[3] if action=='effect' else 'first',len(sys.argv)>4 and sys.argv[4]=='same-key')
    s=IsolatedJournal(root,_CREATED)
    if action=='exception':
        try:
            if sys.argv[3]=='before':raise RuntimeError('before_transaction')
            with s.transaction() as c:
                c.execute('UPDATE aggregates SET body=?',(canonical_json(change(r.expected,value=1)),))
                raise RuntimeError('during_transaction')
        except RuntimeError as exc:print(json.dumps(dict(exception=str(exc),pid=os.getpid())),flush=True)
        return
    if action=='read':
        # Explicit disposable fixture owner allows SQLite's hot-journal rollback.
        # No application rows are deleted, fabricated or repaired by the adapter.
        with sqlite3.connect(s.path.as_uri()+'?mode=rw',uri=True) as c:c.execute('SELECT count(*) FROM sqlite_master').fetchone()
        snapshot=read_snapshot(s,r,provenance=content('independent-process-readback'),owner_process='EXITED')
        assessment=assess_recovery(snapshot)
        with sqlite3.connect(s.path.as_uri()+'?mode=ro',uri=True) as c:
            count=c.execute('SELECT count(*) FROM effects').fetchone()[0]
            conflict_count=c.execute('SELECT count(*) FROM conflicts').fetchone()[0]
        print(json.dumps(dict(pid=os.getpid(),snapshot=json.loads(canonical_json(snapshot)),
            assessment=json.loads(canonical_json(assessment)),effect_count=count,conflict_count=conflict_count,
            dispatch_calls=0,provenance='INDEPENDENT_DISPOSABLE_PROCESS_SQLITE_READBACK')),flush=True);return
    if action=='claim':
        gate('claim-ready',root)
        try:out=s.claim(r.operation_id,sys.argv[3],s.head(r.operation_id).journal_version).writer
        except JournalConflict:out='CONFLICT'
        print(json.dumps(dict(result=out,pid=os.getpid(),qualification='ISOLATED_TRUSTED_FIXTURE_ONLY_NOT_AUTHENTICATION')),flush=True);return
    if action=='effect':
        gate('effect-ready',root)
        h=s.head(r.operation_id);a=h.transition.attempt
        try:out=IsolatedAppendAdapter().apply(s,a,p,authorization=q,observed_context=r.context).outcome
        except JournalConflict:out='CONFLICT'
        print(json.dumps(dict(result=out,pid=os.getpid())),flush=True);return
    if action=='replay':
        snap=read_snapshot(s,r,provenance=content('fixture-replay-probe'),owner_process='EXITED')
        assessment=assess_recovery(snap);advice=assess_replay(assessment,r,writer='writer-a')
        print(canonical_json(advice),flush=True);return
    raise ValueError('unknown_fixture_action')


if __name__=='__main__':main()
