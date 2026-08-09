# P18.3 Approval Workflow Integration

Final verdict: hermes_0_19_pepper_approval_workflow_integration_ready_with_explicit_human_ticket_decision_artifact_binding_and_no_execution_authority

## Purpose

P18.3 consumes the accepted P18.2 `TicketFactoryRuntimeIntegrationResult` and records one explicit human ticket decision over the generated `TicketSpec` and compile-only WorkPacket evidence. It supports only `APPROVE` and `REJECT` for this workflow step.

The integration reuses the existing Ticket Factory approval and publication contracts. It does not create another approval engine, another `TicketSpec` model, another WorkPacket model, a dispatcher, a queue, a workspace allocator, a provider runtime, a model runtime, a Git executor, G-Brain, Paperclip, or production deployment authority.

## Inputs

P18.3 requires:

- Accepted P18.2 `TicketFactoryRuntimeIntegrationResult`.
- P18.2 state `completed` and decision `accepted`.
- P18.2 resulting workflow state `awaiting_ticket_approval`.
- `P18_3_ready: true` from P18.2.
- Exactly one P18.2 WorkPacket compilation.
- No existing human ticket approval on the P18.2 result.
- No ticket or WorkPacket execution authorization on the P18.2 result.
- An explicit human decision input with reviewer evidence, reason code and decision timestamp.

`REQUEST_REVISION` is rejected in P18.3 because revision orchestration is outside this ticket's ownership boundary. Correction routing is represented by a human rejection transition only.

## Artifact Binding

`ApprovalWorkflowArtifactBinding` binds the P18.2 result digest, `TicketSpec` digest, WorkPacket ID, WorkPacket digest, compile-only publication evidence and workflow snapshot digest.

The binding preserves canonical identity as `project_id: PEPPER`, `macroproject_id: P18`, and `ticket_id: P18.2`; `project_id: P18` is rejected as a project/macroproject transposition.

The binding is deterministic and non-transferable. If any of the bound `TicketSpec`, WorkPacket, publication, policy or workflow snapshot fields are changed, request validation fails before an approval result is built.

## Human Decision Boundary

`ApprovalWorkflowDecisionInput` requires `authority: human`. The following non-human authorities are rejected:

- `provider`
- `model`
- `autonomous_agent`
- `worker`
- `scheduler`
- `runtime`
- `generated_default`

Decision evidence rejects credential-shaped text, raw context, personal absolute paths and execution-shaped content. This prevents approval rationale fields from being used as a hidden command or provider channel.

## Approval Flow

For `APPROVE`, P18.3:

- Builds an existing `TicketApprovalRecord` with `HumanApprovalDecision.APPROVE`.
- Recomputes and binds the existing Ticket Factory synthesis and dependency evidence.
- Applies the existing in-memory canonical ticket publication contract.
- Advances the P18.0 workflow through `GWT-003` from `awaiting_ticket_approval` to `ticket_approved`.
- Produces a P18.4 handoff with `P18_4_ready: true` and `execution_started: false`.

Approval publication is logical evidence only. It does not authorize execution or persist a runtime task.

## Rejection Flow

For `REJECT`, P18.3:

- Builds an existing `TicketApprovalRecord` with `HumanApprovalDecision.REJECT`.
- Does not publish or revise a canonical ticket.
- Advances the P18.0 workflow through `GWT-025` from `awaiting_ticket_approval` to `awaiting_correction`.
- Produces a P18.4 handoff with `P18_4_ready: false` and `execution_started: false`.

`GWT-025` is an additive P18.0 transition required by P18.3 because the prior P18.0 table had approval from `awaiting_ticket_approval` but no rejection path from the same state.

## Replay Policy

P18.3 accepts exactly one first human ticket decision for the bound P18.2 artifact set. Any prior approval evidence blocks the request, including exact duplicate replay, stale artifact replay and conflicting second decision replay.

## Authority Boundary

The P18.3 result records these authority-boundary invariants:

- human ticket approval required: `true`
- human ticket approval present: `true`
- ticket execution authorized: `false`
- WorkPacket execution authorized: `false`
- ticket execution started: `false`
- WorkPacket execution started: `false`
- worker dispatch count: `0`
- command execution count: `0`
- provider dispatch count: `0`
- model inference count: `0`
- Git commands executed: `0`
- Docker commands executed: `0`
- Graphify commands executed: `0`
- G-Brain calls: `0`
- Paperclip calls: `0`
- production readiness claimed: `false`

P18.3 does not allocate workspaces, enqueue tasks, run workers, execute commands, call providers or models, mutate Git, run Docker, run Graphify, write G-Brain memory, operate Paperclip, or claim production readiness.

## P18.4 Handoff

P18.4 may consume the approved P18.3 result only when `approval_granted` and `P18_4_ready` are both `true`. The handoff includes the bound `TicketSpec` digest, WorkPacket ID, WorkPacket digest, approval decision digest, approval result digest and resulting workflow state.

Rejected P18.3 results are not queue-eligible and must remain in `awaiting_correction` until a later governed correction path is implemented.

## Deferred Surfaces

- Approval UI backend routing remains deferred; existing approval UI client code is display/provisional evidence only.
- Durable approval persistence remains deferred; P18.3 emits deterministic in-memory result evidence.
- Dependency-aware queue integration is implemented by P18.4 and consumes approved handoffs only.
- Validation and review loop integration remains deferred to P18.5.
- Retry, incident and rollback workflow remain deferred to P18.6.
- Manual-versus-Hermes shadow run remains deferred to P18.7.
- Controlled default-mode cutover remains deferred to P18.8.
- Workflow migration closure remains deferred to P18.R.
