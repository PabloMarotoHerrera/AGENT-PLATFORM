# P18.0 - Governed Workflow State Machine

P18.0 starts P18, Manual-to-Hermes Workflow Migration, by defining one canonical Pepper workflow state machine over the accepted P17 WorkPacket Execution MVP closure and existing Hermes/Pepper runtime lifecycle mechanics. It is a declarative governance and mapping layer only: it introduces no new runtime dispatcher, no Kanban replacement, no heartbeat loop, no retry loop, no reclaim loop, no workspace allocator, no provider dispatch, no model inference, no Git mutation, no Docker, no Graphify mutation, no database mutation, no filesystem authority, no rollback execution, and no production deployment authority.

Final verdict: hermes_0_19_pepper_governed_workflow_state_machine_ready_with_reused_customized_runtime_lifecycle_and_preserved_human_authority

## P18.0 Purpose

P18.0 normalizes the current manual workflow into a governed state vocabulary that later P18 tickets can connect to Pepper UI intake, Ticket Factory, WorkPacket execution, validation, review, approval, human Git handoff, and next-ticket progression.

The state machine does not execute that workflow. It declares states, transitions, runtime projections, P17 closure binding, reuse findings, and deterministic digests so later tickets can integrate existing runtime mechanics without creating a parallel workflow engine.

## P17 Binding

P18.0 consumes the accepted P17.R closure posture. A valid `P17WorkflowBinding` requires:

| Boundary | Required Value |
| --- | --- |
| P17 closure state | `closed` |
| P17 closure decision | `accepted` |
| WorkPacket Execution MVP | available |
| Human Git authority | required |
| Scope | non-critical |
| Production readiness | not claimed |

P18.0 cannot reinterpret P17.R as production authority. It cannot consume a rejected, open, production-claiming, critical-scope, or Git-automation closure.

## Canonical State Inventory

P18.0 defines 21 governed states. They are intentionally broader than the existing Kanban columns because they include governance-only and human-boundary states that are not runtime columns.

| Order | State | Owner | Runtime Posture |
| --- | --- | --- | --- |
| 1 | `draft` | Pepper governance | Governance-only intake state |
| 2 | `intake_ready` | Pepper governance | Governance-only project intake completion |
| 3 | `awaiting_ticket_approval` | Human | Human approval boundary |
| 4 | `ticket_approved` | Pepper governance | Governance-only approval result |
| 5 | `work_packet_ready` | Pepper governance | WorkPacket compilation boundary |
| 6 | `queued` | Pepper runtime | Maps to Kanban `todo` |
| 7 | `blocked` | Shared | Maps to Kanban `blocked` or dependency-gated `todo` |
| 8 | `allocating` | Pepper runtime | Existing workspace lifecycle customization point |
| 9 | `ready_to_execute` | Pepper runtime | Maps to Kanban `ready` |
| 10 | `executing` | Pepper runtime | Maps to Kanban `running` with heartbeat/reclaim evidence |
| 11 | `validating` | Pepper runtime | Governance state over accepted validation evidence |
| 12 | `reviewing` | Shared | Maps to Kanban `review` |
| 13 | `awaiting_correction` | Human | Human correction boundary |
| 14 | `awaiting_human_approval` | Human | Human final approval boundary |
| 15 | `awaiting_human_git_handoff` | Human | Human-only Git handoff boundary |
| 16 | `completed` | Pepper governance | Maps to Kanban `done` |
| 17 | `failed` | Shared | Maps to runtime-adapter failure evidence |
| 18 | `cancelled` | Human | Terminal cancellation posture |
| 19 | `incident` | Shared | Governance-only incident state |
| 20 | `retry_pending` | Human | Retry is authorized but not automatically executed |
| 21 | `rollback_required` | Human | Rollback is represented but not executed |

The transition table contains 24 deterministic transitions. Human-only triggers remain human-authorized and non-automatic. Terminal states do not transition in P18.0.

## Runtime Mapping

P18.0 maps governed states to existing Hermes/Pepper runtime surfaces through `HermesWorkflowProjection` and `WorkflowRuntimeStateMapping`. Runtime projection is explicitly non-authoritative for governance state; it is evidence used by the declarative state machine, not the source of truth.

The current mapping inventory contains 28 mappings and covers every governed state. It includes Kanban mappings for relevant task states, runtime-adapter mappings for failure/cancellation/rollback posture, WorkPacket mappings for compilation and evidence boundaries, and governance-only mappings where no runtime column should exist.

## Reuse Decisions

P18.0 reuses or customizes existing Hermes/Pepper lifecycle mechanics instead of duplicating them.

| Capability | P18.0 Disposition |
| --- | --- |
| Kanban Swarm | Customize |
| Kanban task lifecycle | Retain |
| Dispatcher | Retain |
| Heartbeat | Retain |
| Retry evidence | Customize |
| Reclaim | Retain |
| Workspace lifecycle | Customize |
| Planner and Ticket Factory dependency planning | Retain |
| Approval surfaces | Customize |
| Dashboard and TUI surfaces | Customize |
| Runtime adapter state machine | Retain |
| Provider failure policy | Retain |
| Execution inspector | Defer |
| P19 G-Brain memory | Defer |
| P20 Paperclip control plane | Defer |

Replacement is not used in P18.0 because no assessed capability requires a parallel runtime implementation. Deferred capabilities grant no hidden P18.0 authority.

## Authority Boundary

P18.0 preserves the human authority boundary inherited from P17. Git handoff remains human-only. Ticket approval, human approval, human rejection, retry authorization, rollback authorization, and Git completion cannot be performed by the governed runtime.

P18.0 does not authorize provider-backed execution, model-backed execution, production execution, critical-ticket execution, automatic retry, automatic fallback, automatic cleanup, automatic rollback, automatic staging, automatic commit, automatic push, or multi-agent execution.

## Security Boundary

P18.0 records bounded identifiers, enum values, booleans, digest strings, state names, transition evidence references, blocker codes, capability summaries, and reuse findings only. It rejects credential-shaped text, raw runtime content, personal absolute paths, raw provider responses, raw model outputs, raw diffs, raw stdout, raw stderr, tracebacks, runtime handles, filesystem handles, and Git handles.

Deterministic SHA-256 values are integrity evidence for stable contract objects. They are not digital signatures.

## Validation Evidence

The focused P18.0 suite validates the import boundary, model immutability, state inventory, transition table, P17 binding, deterministic digest behavior, runtime projection mapping, reuse findings, human authority preservation, invalid mapping rejection, and no-runtime-authority posture.

Focused P18.0 result after implementation: `704 passed`.

## P18.1 Handoff

P18.1 may consume the P18.0 state machine to build governed intake integration. It must continue the reuse-first rule from P17.R and P18.0. It must not create a duplicate dispatcher, Kanban database, heartbeat engine, retry engine, reclaim engine, workspace allocator, provider runtime, model runtime, Git executor, G-Brain, Paperclip control plane, or production deployment path.

P18.0 does not claim that the manual workflow has been fully migrated. It defines the state machine that later P18 tickets must integrate, compare, cut over, and close.
