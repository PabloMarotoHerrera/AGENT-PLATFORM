# P18.2 Ticket Factory Runtime Integration

Final verdict: hermes_0_19_pepper_ticket_factory_runtime_integration_ready_with_deterministic_ticket_spec_work_packet_binding_and_pending_human_approval

## Purpose

P18.2 consumes the accepted P18.1 project-intake result and the committed P18.UI-A parent, then produces bounded Ticket Factory planning evidence for the next governed workflow step. It creates a validated `ProjectSpec`, a validated `TicketSpec` for `P18.2`, a bounded `ContextPack`, a `TicketDependencyPlan`, a `TicketLintReport`, one deterministic P17 `WorkPacketCompilationResult`, and WorkPacket continuation evidence.

The workflow transition stops at `awaiting_ticket_approval` through P18.0 transition `GWT-002`. P18.2 does not approve the ticket for execution, allocate a workspace, execute commands, dispatch providers or models, mutate Git, run Docker, run Graphify, or claim production readiness.

## Inputs

P18.2 requires:

- Accepted P18.1 `ProjectIntakeResult`.
- Resulting P18.1 workflow snapshot in `intake_ready`.
- `P18_2_ready: true` from the P18.1 summary.
- Committed P18.UI-A parent commit `f55b8a2cc62c9ba0620a14f51b968107b75a78f1`.

The request rejects any different P18.UI-A parent. This binds the Ticket Factory runtime integration to the human-validated product UI activation baseline instead of the earlier stale-dashboard failure.

## Ticket Factory Evidence

P18.2 uses the existing P16 Ticket Factory contracts rather than adding a second ticket generator:

| Evidence | Existing Owner | P18.2 Use |
| --- | --- | --- |
| `ProjectSpec` | P16.0 | Project-level P18 migration identity and constraints. |
| `TicketSpec` | P16.0 | Canonical P18.2 ticket candidate. |
| `ContextPack` | P16.1 | Bounded intake and activation context pointers. |
| `TicketDependencyPlan` | P16.3 | Single-ticket dependency-ready wave for P18.2. |
| `TicketLintReport` | P16.4 | Governed-standard policy pass evidence. |
| `WorkPacketCompilationResult` | P17.0 | Compile-only WorkPacket evidence for the generated P18.2 ticket. |

The generated `TicketSpec` and compiled WorkPacket are planning evidence only. They are not execution authority.

## Workflow Transition

P18.2 builds a P18.0 `GovernedWorkflowTransitionRequest` with:

- current state: `intake_ready`
- trigger: `ticket_generated`
- authority: `governed_runtime`
- evidence ref: `ticket_factory_candidate`
- target state: `awaiting_ticket_approval`

The resulting snapshot has `pending_human_action: ticket_approval`. This is intentional: P18.3 owns human ticket approval workflow integration.

## WorkPacket Continuation

P18.2 records `TicketFactoryWorkPacketContinuation` evidence that binds the dependency-plan digest, lint-report digest, compilation-result digest, `work_packet_id`, and `work_packet_SHA256`. The continuation states that logical publication and compilation authorization are present for compile-only evidence, while future execution still requires:

- human ticket approval,
- workspace allocation,
- tool permission profiling,
- explicit execution authorization.

`work_packet_compilation_completed` is `true`, `compiler_invocation_count` is `1`, `command_execution_authorized` remains `false`, `runtime_execution_authorized` remains `false`, and `WorkPacket_compilation_count` is `1`.

## Authority Boundary

The P18.2 result records these authority-boundary invariants:

- provider dispatch count: `0`
- model inference count: `0`
- Git commands executed: `0`
- Docker commands executed: `0`
- Graphify commands executed: `0`
- WorkPacket compilation count: `1`
- WorkPacket execution authorized: `false`
- production readiness claimed: `false`

P18.2 creates no persistent database, no G-Brain memory, no Paperclip control plane, no queue dispatcher, no workspace allocator and no runtime worker.

## P18.3 Handoff

P18.3 may consume the P18.2 `TicketFactoryRuntimeIntegrationResult`, including the `TicketSpec`, context-pack digest, dependency-plan digest, lint-report digest, compile-only WorkPacket evidence, WorkPacket-continuation digest, and the resulting workflow snapshot in `awaiting_ticket_approval`.

P18.3 owns human ticket approval integration. P18.2 does not perform or simulate that approval.

## Residual Limitations

- Ticket approval workflow integration remains deferred to P18.3.
- Dependency-aware queue integration remains deferred to P18.4.
- Validation and review loop integration remains deferred to P18.5.
- Retry, incident and rollback workflow remain deferred to P18.6.
- Manual-versus-Hermes shadow run remains deferred to P18.7.
- Controlled default-mode cutover remains deferred to P18.8.
- Workflow migration closure remains deferred to P18.R.
