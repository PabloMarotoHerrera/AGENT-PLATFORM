import pytest
from hermes_cli.agent_platform.harness.contracts import AuthorityCurrentness
from hermes_cli.agent_platform.harness.journal_recovery import assess_recovery
from hermes_cli.agent_platform.harness.replay_policy import assess_replay
from hermes_cli.agent_platform.isolated_journal_recovery import read_snapshot
from hermes_cli.agent_platform.isolated_effect_adapter import run_fixture,transition,IsolatedAppendAdapter
from hermes_cli.agent_platform.isolated_operation_journal import JournalConflict
from tests.hermes_cli.har13_test_helpers import setup
from tests.hermes_cli.test_har12_operation_journal import change,content


@pytest.mark.parametrize('field',['source','authority','validation','human','currentness','historical','resource','payload'])
def test_changed_request_never_inherits_prior_recovery_or_consent(tmp_path,field):
    s,r,q,p=setup(tmp_path);run_fixture(s,r,p,writer='writer-a',authorization=q,observed_context=r.context,failure='after_effect')
    a=assess_recovery(read_snapshot(s,r,provenance=content('fixture')))
    ctx=r.context
    if field=='source':ctx=change(ctx,implementation=change(ctx.implementation,content=content('new-source')))
    elif field=='authority':ctx=change(ctx,authority=change(ctx.authority,content=content('new-authority')))
    elif field=='validation':ctx=change(ctx,validation_inputs=(change(ctx.validation_inputs[0],content=content('new-input')),))
    elif field=='human':ctx=change(ctx,workflow_context=change(ctx.workflow_context,human_decision_target='wrong-target'))
    elif field=='currentness':ctx=change(ctx,currentness=AuthorityCurrentness.UNVERIFIED)
    elif field=='historical':ctx=change(ctx,currentness=AuthorityCurrentness.HISTORICAL)
    elif field=='resource':ctx=change(ctx,resource=change(ctx.resource,content=content('foreign-resource')))
    proposed=change(r,context=ctx,effect=change(r.effect,payload=content('changed-payload')) if field=='payload' else r.effect)
    advice=assess_replay(a,proposed,writer='writer-a')
    assert advice.reason=='CONFLICTING_REQUEST' and not advice.retry_admissible
    with pytest.raises(JournalConflict):s.request(proposed)
    assert s.effect_count()==1


def test_same_writer_text_does_not_authenticate_and_exit_does_not_transfer(tmp_path):
    s,r,q,p=setup(tmp_path);h=s.request(r);s.claim(r.operation_id,'writer-a',1)
    a=assess_recovery(read_snapshot(s,r,provenance=content(),owner_process='EXITED'))
    same=assess_replay(a,r,writer='writer-a');other=assess_replay(a,r,writer='writer-b')
    assert same.reason=='SAME_WRITER_NOT_AUTHENTICATED' and other.reason=='OWNER_CONFLICT'
    assert not same.retry_admissible and not other.takeover_admissible
    with pytest.raises(JournalConflict):s.claim(r.operation_id,'writer-b',1)
