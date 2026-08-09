# P18.5 Review And Validation Loop

Final verdict: hermes_0_19_pepper_review_validation_loop_ready_with_reused_p17_validation_diff_review_and_human_git_handoff_boundaries

## Purpose

P18.5 consumes an admitted P18.4 `DependencyAwareQueueIntegrationResult` and already-produced P17 WorkPacket evidence. It deterministically binds P17 outcome envelopes, validation results, diff/artifact review results and human Git handoff evidence into one governed review result.

This is a post-execution review integration only. It does not execute WorkPackets, run validation commands, inspect diffs, allocate workspaces, call providers or models, mutate Git, retry, roll back, run Docker, run Graphify, write G-Brain memory, operate Paperclip, persist a live queue, or claim production readiness.

## Inputs

P18.5 requires:

- Completed P18.4 queue result with decision `admit`.
- P18.4 resulting workflow state `queued`.
- `P18_5_ready: true` from the P18.4 handoff.
- Bound canonical identity `project_id: PEPPER`, `macroproject_id: P18`, and `ticket_id: P18.2`.
- Bound TicketSpec digest, WorkPacket ID, WorkPacket digest, approval decision digest and dependency-plan digest.
- One P17.5 `OutcomeEnvelope` with terminal result, failure or cancellation evidence.
- One P17.6 `DiffArtifactReviewResult` bound to the same WorkPacket and outcome envelope.
- One P17.7 `GitHandoffResult` for accepted reviews, or no handoff for non-accept reviews.

Blocked P18.4 queue results are not accepted by P18.5. They remain governed queue evidence until a later unblock or correction path exists.

## P17 Reuse

P18.5 retains accepted P17/P18 contracts instead of creating replacements:

- P17.3 `SingleAgentExecutionResult` remains the execution-result authority.
- P17.4 `ValidationCommandRunnerResult` and `ValidationCommandExecutionResult` remain validation evidence authority.
- P17.5 `OutcomeEnvelope` remains terminal result, failure and cancellation authority.
- P17.6 `DiffArtifactReviewResult`, `DiffReviewVerdict` and `ArtifactReviewVerdict` remain review authority.
- P17.7 `GitHandoffResult` remains human-only Git handoff authority.
- P18.0 `GovernedWorkflowTransitionResult` remains workflow transition authority.

The result records `P17_validation_runner_reused`, `P17_outcome_envelopes_reused`, `P17_diff_artifact_review_reused` and `P17_human_Git_handoff_reused_or_deferred_with_evidence` as true. Duplicate validation runners, outcome envelopes, diff review engines, artifact review engines, Git handoffs, WorkPacket executors, workflow state machines and workspace allocators are all recorded as false.

## Review Decisions

The P18.5 decision is deterministic:

- `accept` when the P17.5 outcome is a validation-runner result, validation passed, P17.6 diff/artifact review passed and a completed approved P17.7 human Git handoff is present.
- `needs_correction` when validation fails or diff/artifact review blocks acceptance after execution completed.
- `incident` when the P17.5 outcome is a single-agent execution failure.
- `cancelled` when the P17.5 outcome is cancellation.

Accepted reviews advance through P18.0 transitions from `queued` to `awaiting_human_git_handoff`. P18.5 does not perform the human Git commands and does not transition through `human_git_completed`.

Non-accept reviews produce a deterministic `ReviewValidationP18_6Handoff` containing blocker codes, terminal classification and workflow state. That handoff starts no retry and no rollback.

## Authority Boundary

The P18.5 result records these authority-boundary invariants:

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
- rollback count: `0`
- autonomous correction count: `0`
- provider dispatch count: `0`
- model inference count: `0`
- Docker commands executed: `0`
- Graphify commands executed: `0`
- G-Brain calls: `0`
- Paperclip calls: `0`
- executor calls in P18.5: `0`
- workspace allocation calls in P18.5: `0`
- validation command execution count: `0`

The runtime boundary classification is `REVIEW_POST_EXECUTION_ONLY`: P18.5 consumes evidence that already exists and never starts the P17 execution sequence itself.

## Replay Policy

P18.5 is single-pass for a given P18.4 handoff. A request carrying prior review result evidence is rejected. There is no autonomous retry, rollback, cleanup, staging, commit or push path in P18.5.

## Validation Evidence

Focused tests validate P18.5 exports, additive workflow export segment compatibility, immutable Pydantic models, P18.4 admitted-handoff binding, P17 outcome/diff/handoff evidence binding, accept flow, validation-failure flow, diff-blocker flow, execution-failure flow, cancellation flow, replay rejection, tamper rejection, deterministic digests and zero runtime authority.

## Residual Limitations

- Retry, incident and rollback workflow remain deferred to P18.6.
- Manual-versus-Hermes shadow run remains deferred to P18.7.
- Controlled default-mode cutover remains deferred to P18.8.
- Workflow migration closure remains deferred to P18.R.
- Durable queue persistence remains outside P18.5.
- P18.5 does not perform human Git staging, commit or push.
