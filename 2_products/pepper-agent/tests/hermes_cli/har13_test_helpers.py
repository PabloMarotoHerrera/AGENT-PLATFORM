import json
import os
from pathlib import Path
import select
import subprocess
import sys

from hermes_cli.agent_platform.isolated_operation_journal import IsolatedJournal
from tests.hermes_cli.test_har12_operation_journal import case

DRIVER=Path(__file__).with_name('har13_process_fixture.py')


def setup(tmp_path):
    r,q,p=case();s=IsolatedJournal.create_disposable(tmp_path);s.initialize_aggregate(r.expected)
    return s,r,q,p


def spawn(action,root,*args):
    env={'HOME':str(root),'HERMES_HOME':str(root/'forbidden-live'),'PATH':os.defpath,
        'LANG':'C.UTF-8','TZ':'UTC','PYTHONDONTWRITEBYTECODE':'1'}
    return subprocess.Popen([sys.executable,'-I','-B',str(DRIVER),action,str(root),*args],cwd=root,env=env,
        stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)


def handshake(child,root,window):
    ready,_,_=select.select([child.stdout],[],[],20)
    if not ready:raise AssertionError('child handshake timeout')
    line=child.stdout.readline()
    if not line:raise AssertionError(child.stderr.read())
    event=json.loads(line)
    assert event==dict(ready=True,pid=child.pid,window=window,root=str(root))
    return event


def reap(child):
    if child.poll() is None:child.kill()
    child.communicate(timeout=15)


def invoke(action,root,*args):
    child=spawn(action,root,*args)
    try:
        out,err=child.communicate(timeout=25)
        assert child.returncode==0,err
        return json.loads(out)
    finally:reap(child)


def crash(tmp_path,window):
    s,r,q,p=setup(tmp_path);child=spawn('crash',s.root,window)
    try:
        event=handshake(child,s.root,window)
        child.kill();child.communicate(timeout=15)
        assert child.returncode<0
        result=invoke('read',s.root)
        assert result['pid']!=child.pid and result['dispatch_calls']==0
        result['termination']=dict(**event,exit_code=child.returncode,mechanism='SIGKILL_OWN_POPEN_CHILD')
        return s,r,result
    finally:reap(child)
