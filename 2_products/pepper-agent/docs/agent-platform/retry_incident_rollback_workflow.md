# P18.6 Retry, Incident And Rollback Workflow

Final verdict: hermes_0_19_pepper_retry_incident_rollback_workflow_ready_with_bounded_recovery_authority_and_no_autonomous_repair

## Purpose

P18.6 consumes a non-accept P18.5 `ReviewValidationLoopIntegrationResult` and its deterministic `ReviewValidationP18_6Handoff`. It records a bounded recovery decision for validation/review correction, execution incidents, human-authorized retry state, human-authorized rollback state, or cancellation.

This is a recovery governance layer only. It does not execute a retry, requeue a task, reclaim a claim, reassign a task, allocate or restore a workspace, mutate Git, run validation commands, call providers or models, run Docker, run Graphify, write G-Brain memory, operate Paperclip, persist incident state, or claim production readiness.

## Inputs

P18.6 requires:

- A P18.5 result with decision other than `accept`.
- `P18_6_ready: true` and a present `ReviewValidationP18_6Handoff`.
- Matching P18.5 result digest, P18.6 handoff digest, WorkPacket ID and WorkPacket digest.
- Canonical identity `project_id: PEPPER`, `macroproject_id: P18`, and `ticket_id: P18.2`.
- Matching expected workflow state from the P18.5 result and the P18.6 handoff.
- Optional explicit human authorization for `authorize_retry` or `authorize_rollback`, accepted only for execution-incident sources in P18.0 `failed` state.

Accepted P18.5 results are rejected by P18.6 because they proceed through the P17.7 human Git handoff path instead of recovery handling.

## Recovery Decisions

The P18.6 decision is deterministic:

- `await_human_correction` for P18.5 `needs_correction` outcomes; the workflow remains `awaiting_correction`.
- `record_incident` for execution-failure incidents without usable human retry/rollback authorization, or when retry budget is exhausted; the workflow remains `failed`.
- `retry_pending` when an execution incident has explicit human retry authorization and the bounded attempt budget is not exhausted; P18.6 reuses P18.0 `GWT-023` from `failed` to `retry_pending`.
- `rollback_required` when an execution incident has explicit human rollback authorization; P18.6 reuses P18.0 `GWT-024` from `failed` to `rollback_required`.
- `cancelled` for P18.5 cancellation outcomes; the workflow remains terminal `cancelled`.

Retry and rollback transitions are state projections only. P18.6 does not start an agent, enqueue work, restore files, or run Git commands.

## Reuse Matrix

P18.6 retains accepted P17/P18 contracts instead of creating replacements:

- P18.5 `ReviewValidationP18_6Handoff` remains the non-accept handoff authority.
- P18.5 `ReviewValidationLoopIntegrationResult` remains the source decision and workflow-state authority.
- P17.5 `OutcomeEnvelope` remains terminal result, failure and cancellation evidence authority.
- P17.3 `SingleAgentExecutionResult` remains execution evidence authority.
- P17.1 workspace allocation evidence remains prior workspace binding authority; P18.6 creates no workspace restorer.
- P17.7 `GitHandoffResult` remains the human-only Git handoff boundary.
- P18.0 `GovernedWorkflowTransitionResult` remains retry/rollback state-transition authority.

Existing Kanban retry counters, failure limits, requeue, reclaim, reassign, dashboard recovery endpoints and repeated-failure diagnostics are assessed but not invoked. They are runtime mutation or operator surfaces, not canonical P18.6 governance authority.

## Authority Boundary

The P18.6 result records these fixed authority-boundary invariants:

- Git commands executed: `0`
- Git staging performed: `false`
- Git commit performed: `false`
- Git push performed: `false`
- staging calls: `0`
- commit calls: `0`
- push calls: `0`
- retry execution count: `0`
- automatic retry count: `0`
- automatic requeue count: `0`
- Kanban requeue calls: `0`
- Kanban reclaim calls: `0`
- Kanban reassign calls: `0`
- rollback execution count: `0`
- workspace allocation calls in P18.6: `0`
- workspace cleanup calls in P18.6: `0`
- workspace restore calls in P18.6: `0`
- provider dispatch count: `0`
- model inference count: `0`
- Docker commands executed: `0`
- Graphify commands executed: `0`
- G-Brain calls: `0`
- Paperclip calls: `0`
- Kanban SQLite canonical authority: `false`

The runtime boundary classification is `RECOVERY_DECISION_ONLY`: P18.6 records recovery posture and optional human-authorized workflow state, but all operational recovery remains outside this module.

## Replay Policy

P18.6 is single-pass for a given P18.5 handoff. A request carrying prior P18.6 recovery result evidence is rejected. Duplicate builds of the same request remain deterministic, but replay must be explicit and externally governed.

## Validation Evidence

Focused tests validate P18.6 exports, additive workflow export compatibility, immutable Pydantic models, P18.5 non-accept binding, correction handling, incident recording, human-authorized retry and rollback state projection, retry-budget exhaustion, cancellation handling, replay rejection, tamper rejection, deterministic digests, reuse matrix classification and zero runtime authority.

## Residual Limitations

- P18.6 does not perform retry execution, task requeue, task reclaim, task reassignment or dispatcher ticks.
- P18.6 does not perform Git rollback, workspace cleanup, workspace restoration, staging, commit or push.
- P18.6 does not persist incident records into Kanban, SQLite, logs, G-Brain or Paperclip.
- Manual-versus-Hermes shadow run remains deferred to P18.7.
- Controlled default-mode cutover remains deferred to P18.8.
- Workflow migration closure remains deferred to P18.R.
- Durable queue persistence and operator runbooks remain outside P18.6.
