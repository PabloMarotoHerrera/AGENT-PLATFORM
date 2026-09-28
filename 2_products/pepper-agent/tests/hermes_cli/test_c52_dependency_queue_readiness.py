"""Queue admission must consume canonical wave readiness, including SERIAL."""

import pytest
from pydantic import ValidationError

from hermes_cli.agent_platform.ticket_factory import (
    DependencyScope,
    ParallelizationHint,
    WaveDisposition,
)
from hermes_cli.agent_platform.ticket_factory.dependency_planning import (
    is_ticket_dependency_wave_ready,
)
from hermes_cli.agent_platform.workflow import dependency_execution_queue as queue
from tests.hermes_cli import (
    test_agent_platform_ticket_factory_dependency_planning as fixtures,
)


def assert_admission(plan, ticket_id, ready, evidence=()):
    result = queue.derive_dependency_queue_admission_for_ticket(
        dependency_plan=plan,
        ticket_id=ticket_id,
        dependency_satisfaction_evidence=evidence,
    )
    assert result["decision"] == ("admit" if ready else "blocked"), result
    assert result["dependencies_satisfied"] is ready
    assert result["queue_eligible"] is ready
    assert result["queue_admitted"] is ready
    assert result["dependency_plan_SHA256"] == plan.plan_SHA256
    assert result["dependency_bypass"] is False
    assert result["approval_bypass"] is False
    assert result["execution_started"] is False
    assert result["dispatch_eligible"] is False
    assert result["worker_dispatch_count"] == 0
    return result


@pytest.mark.parametrize(
    "hint, disposition",
    [
        (ParallelizationHint.SERIAL, WaveDisposition.SERIAL),
        (ParallelizationHint.UNSPECIFIED, WaveDisposition.DEPENDENCY_READY),
    ],
)
def test_c52_single_ticket_wave_matches_canonical_readiness(hint, disposition):
    plan = fixtures.plan(fixtures.ticket(hint=hint))
    ticket_id = plan.ticket_ids[0]
    assert plan.ticket_ids == plan.topological_order == (ticket_id,)
    assert plan.edges == plan.blockers == plan.blocked_ticket_ids == ()
    assert plan.unresolved_soft_external_dependency_ids == plan.scope_collisions == ()
    assert len(plan.waves) == 1
    assert plan.waves[0].disposition is disposition
    assert plan.waves[0].scope_collision_ids == ()
    assert is_ticket_dependency_wave_ready(plan, ticket_id=ticket_id) is True
    assert_admission(plan, ticket_id, True)


def test_c52_scope_review_remains_blocked():
    plan = fixtures.plan(
        fixtures.ticket("P16.1", paths=("src/*.py",)),
        fixtures.ticket("P16.2", paths=("src/a.py",)),
    )
    for ticket_id in plan.ticket_ids:
        wave = next(w for w in plan.waves if ticket_id in w.ticket_ids)
        assert wave.disposition is WaveDisposition.SCOPE_REVIEW_REQUIRED
        assert wave.scope_collision_ids
        assert is_ticket_dependency_wave_ready(plan, ticket_id=ticket_id) is False
        assert_admission(plan, ticket_id, False)


def test_c52_unresolved_hard_dependency_preserves_explicit_blocker():
    dep = fixtures.dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    plan = fixtures.plan(fixtures.ticket(deps=(dep,), hint=ParallelizationHint.SERIAL))
    ticket_id = plan.ticket_ids[0]
    assert ticket_id in plan.blocked_ticket_ids
    assert any(blocker.ticket_id == ticket_id for blocker in plan.blockers)
    assert is_ticket_dependency_wave_ready(plan, ticket_id=ticket_id) is False
    assert assert_admission(plan, ticket_id, False)["dependency_blockers"]


@pytest.mark.parametrize("state", list(queue.DependencySatisfactionState))
def test_c52_satisfaction_evidence_is_still_required_to_be_satisfied(state):
    dep = fixtures.dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
    plan = fixtures.plan(
        fixtures.ticket(deps=(dep,), hint=ParallelizationHint.SERIAL),
        resolutions=(fixtures.resolution(),),
    )
    ticket_id = plan.ticket_ids[0]
    assert is_ticket_dependency_wave_ready(plan, ticket_id=ticket_id) is True
    evidence = queue.build_dependency_satisfaction_evidence(
        dependency_ticket_id=dep.ticket_id,
        required_relationship="hard_prerequisite",
        satisfaction_state=state,
        evidence_reference="isolated dependency evidence",
        evidence_SHA256="a" * 64,
    )
    assert_admission(
        plan,
        ticket_id,
        state is queue.DependencySatisfactionState.SATISFIED,
        (evidence,),
    )


def test_c52_ticket_absent_from_plan_fails_closed():
    plan = fixtures.plan(fixtures.ticket(hint=ParallelizationHint.SERIAL))
    assert is_ticket_dependency_wave_ready(plan, ticket_id="P16.99") is False
    with pytest.raises(queue.DependencyAwareQueueInputError, match="not present"):
        queue.derive_dependency_queue_admission_for_ticket(
            dependency_plan=plan, ticket_id="P16.99"
        )


@pytest.mark.parametrize(
    "damage",
    [
        "missing_topology",
        "zero_waves",
        "multiple_waves",
        "serial_collision",
        "invalid_disposition",
        "digest",
        "blocked_without_blocker",
        "blocker_without_blocked",
    ],
)
def test_c52_malformed_plan_never_admitted(damage):
    plan = fixtures.plan(fixtures.ticket(hint=ParallelizationHint.SERIAL))
    data = plan.model_dump(mode="json")
    ticket_id = plan.ticket_ids[0]
    if damage == "missing_topology":
        data["topological_order"] = []
    elif damage == "zero_waves":
        data["waves"] = []
    elif damage == "multiple_waves":
        data["waves"].append({
            **data["waves"][0],
            "wave_index": 2,
            "wave_id": "WAVE-002",
        })
    elif damage == "serial_collision":
        data["waves"][0]["scope_collision_ids"] = ["SCOPE-001"]
    elif damage == "invalid_disposition":
        data["waves"][0]["disposition"] = "unknown"
    elif damage == "digest":
        data["plan_SHA256"] = "0" * 64
    elif damage == "blocked_without_blocker":
        data["blocked_ticket_ids"] = [ticket_id]
    else:
        dep = fixtures.dependency("P15.1", dep_scope=DependencyScope.EXTERNAL_PROJECT)
        blocked = fixtures.plan(fixtures.ticket(deps=(dep,)))
        data["blockers"] = blocked.model_dump(mode="json")["blockers"]
    with pytest.raises(ValidationError):
        queue.derive_dependency_queue_admission_for_ticket(
            dependency_plan=data, ticket_id=ticket_id
        )
