# P18.4 Dependency-Aware Execution Queue

Final verdict: hermes_0_19_pepper_dependency_aware_execution_queue_ready_with_governed_approval_dependency_gating_and_zero_runtime_execution

## Purpose

P18.4 consumes the approved P18.3 `ApprovalWorkflowIntegrationResult`, verifies that the bound P18.2 `TicketDependencyPlan` is queue-admissible, and emits deterministic queue-admission evidence for the next governed workflow step.

This is a governance result envelope only. It does not write a live Kanban task, claim a worker, allocate a workspace, execute a WorkPacket, call providers or models, mutate Git, run Docker, run Graphify, write G-Brain memory, operate Paperclip, or claim production readiness.

## Inputs

P18.4 requires:

- Completed P18.3 approval result with decision `approved`.
- Human approval authority and `approval_granted: true`.
- P18.3 resulting workflow state `ticket_approved`.
- `P18_4_ready: true` from the P18.3 handoff.
- Bound canonical identity `project_id: PEPPER`, `macroproject_id: P18`, and `ticket_id: P18.2`.
- Bound P18.2 `TicketSpec` digest, WorkPacket ID, WorkPacket digest, dependency-plan digest and workflow snapshot.

Rejected P18.3 results are not accepted by P18.4. They remain in `awaiting_correction` until a later governed correction path exists.

## Dependency Planning

P18.4 reuses the accepted P16.3/P18.2 `TicketDependencyPlan`. It does not create another dependency planner, another cycle detector, another DAG model or another wave planner.

The queue request binds the P18.2 dependency plan object and its `plan_SHA256`. The result records `dependency_planner_reused: true`, `dependency_plan_recomputed_unnecessarily: false`, `cycle_detection_reused: true`, and `duplicate_cycle_detector_created: false`.

Optional `DependencySatisfactionEvidence` can mark an allowed dependency as `satisfied`, `unsatisfied`, or `unknown`. Satisfied evidence requires a digest. Unsatisfied or unknown evidence produces a deterministic dependency blocker instead of queue admission.

## Queue Decision

The P18.4 decision is deterministic:

- `admit` when the accepted dependency plan places `P18.2` in a dependency-ready wave and no dependency blockers remain.
- `blocked` when dependency evidence or planner blockers prevent admission.

The admitted path advances through P18.0 transitions `GWT-004` and `GWT-005`, ending in `queued`.

The blocked path advances through `GWT-004` and additive transition `GWT-026`, ending in `blocked` with blocker code `dependency_blocked`.

`GWT-026` is the P18.4 additive state-machine transition from `work_packet_ready` to `blocked` with trigger `dependencies_blocked`, authority `policy`, evidence `dependency_blocker`, and `automatic: true`. Existing `GWT-006` remains the post-queue `queued` to `blocked` path.

## Queue Boundary

P18.4 records a `QueueAdmissionBoundary` with these fixed values:

- queue persistence mechanism: `result_envelope_only`
- provisional runtime authority: `kanban_projection_deferred`
- canonical long-term authority: `p20_paperclip_deferred`
- Kanban SQLite canonical: `false`
- does not dispatch: `true`
- does not execute: `true`

Existing Kanban SQLite state, `recompute_ready`, `dispatch_once`, heartbeat, reclaim and gateway dispatcher wiring remain runtime projection mechanics only. P18.4 does not call them.

## Authority Boundary

The P18.4 result records these authority-boundary invariants:

- dispatch eligible: `false`
- ticket execution authorized: `false`
- WorkPacket execution authorized: `false`
- execution started: `false`
- WorkPacket execution started: `false`
- worker dispatch count: `0`
- command execution count: `0`
- provider dispatch count: `0`
- model inference count: `0`
- Git commands executed: `0`
- Docker commands executed: `0`
- Graphify commands executed: `0`
- claim count: `0`
- heartbeat count: `0`
- reclaim count: `0`
- workspace allocation count: `0`
- G-Brain calls: `0`
- Paperclip calls: `0`
- production readiness claimed: `false`

The P17 WorkPacket substrate is reused for identity and policy binding only. P18.4 does not invoke WorkPacket execution.

## P18.5 Handoff

P18.4 emits `DependencyAwareQueueP18_5Handoff` evidence. `P18_5_ready` is `true` only for admitted queue candidates. Blocked candidates carry the same immutable artifact bindings but have `P18_5_ready: false` and must wait for a later unblock path.

The handoff binds the TicketSpec digest, WorkPacket ID, WorkPacket digest, approval decision digest, dependency-plan digest, queue result digest and resulting workflow state.

## Validation Evidence

Focused tests validate P18.4 exports, immutable Pydantic models, digest round trips, approved-handoff admission, rejected-handoff rejection, dependency-blocked routing, replay rejection, zero runtime authority, `GWT-026`, and deterministic result digests.

## Residual Limitations

- Durable queue persistence remains deferred to the P20 Paperclip control-plane boundary.
- Live Kanban task projection remains deferred to a later controlled runtime coupling step.
- Validation and review loop integration remains deferred to P18.5.
- Retry, incident and rollback workflow remain deferred to P18.6.
- Manual-versus-Hermes shadow run remains deferred to P18.7.
- Controlled default-mode cutover remains deferred to P18.8.
- Workflow migration closure remains deferred to P18.R.
