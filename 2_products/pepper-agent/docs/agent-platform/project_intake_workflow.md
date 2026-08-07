# P18.1 Project Intake Workflow

Final verdict: hermes_0_19_pepper_project_intake_workflow_ready_with_bounded_explicit_context_and_governed_intake_transition

## Purpose

P18.1 migrates the first manual workflow context step into Pepper as a deterministic governed project-intake contract.  The contract captures explicit project identity, P18 roadmap posture, repository-relative product binding, project constraints, bounded context references and declarative human intake approval.

The intake result initializes the P18.0 governed workflow state machine by moving a valid initial workflow snapshot from `draft` to `intake_ready`.  Intake readiness means enough governed project context exists to continue workflow planning.  It does not authorize execution, provider dispatch, model inference, Git mutation, retry, rollback or production deployment.

## Relationship To P18.0

P18.0 remains the workflow state-machine authority.  P18.1 consumes the public P18.0 snapshot and transition contracts and invokes the pure P18.0 transition builder for `DRAFT -> INTAKE_READY` using `project_intake_completed` evidence.

P18.1 does not define a second workflow lifecycle and does not mutate workflow state directly.

## Manual Context Problem

Before P18.1, project execution context could be restated across ticket text, conversations, repository documentation, governance contracts and copied manual notes.  P18.1 replaces that repeated manual restatement for bounded project intake data only.

P18.1 does not ingest arbitrary conversation history, chat transcripts, raw prompts, source snapshots, stdout, stderr, diffs, provider responses, credentials or reasoning traces.

## Reuse-First Analysis

Pepper is a customized Hermes-derived product.  P18.1 reuses and customizes existing Pepper/Hermes capabilities rather than creating parallel runtime owners.

| capability | existing owner | P18.1 decision | gap addressed |
|---|---|---|---|
| project metadata | Ticket Factory `ProjectSpec` | CUSTOMIZE | Normalize Pepper-only project intake before Ticket Factory runtime integration. |
| roadmap representation | Ticket Factory dependency planning | CUSTOMIZE | Represent P18 roadmap posture without creating a roadmap engine. |
| project/task boards | Kanban board/task metadata | RETAIN | Operational board persistence remains Kanban-owned. |
| repository/workspace metadata | P17 workspace and repository contracts | CUSTOMIZE | Bind repository-relative product root and P18 branch policy without Git inspection. |
| configuration/project profiles | Hermes config/profile machinery | RETAIN | User/runtime setup remains Hermes-owned and is not P18 authority. |
| dashboard project surfaces | Dashboard product/config projections | DEFER | Display surfaces remain informational, not governance authority. |
| workflow templates/state | P18.0 workflow package | CUSTOMIZE | Reuse P18.0 transition contract for intake readiness. |

Duplicate project registry created: false.  Duplicate roadmap engine created: false.  Duplicate workflow state machine created: false.

## Project Identity

Canonical P18.1 intake supports only the current Pepper development project:

- `project_id`: `PEPPER`
- `project_name`: `Pepper`
- `project_kind`: `pepper`
- `macroproject_id`: `P18`
- `macroproject_title`: `Manual-to-Hermes Workflow Migration`
- `roadmap_id`: `P18-manual-to-hermes-workflow-migration`

Pepper is not modeled as an external wrapper, external governance service or parallel runtime.

## P18 Roadmap Binding

The canonical roadmap contains exactly ten items:

1. `P18.0` Governed Workflow State Machine, completed.
2. `P18.1` Project Intake Workflow, current.
3. `P18.2` Ticket Factory Runtime Integration, next.
4. `P18.3` Approval Workflow Integration.
5. `P18.4` Dependency-Aware Execution Queue.
6. `P18.5` Review and Validation Loop.
7. `P18.6` Retry, Incident and Rollback Workflow.
8. `P18.7` Manual-versus-Hermes Shadow Run.
9. `P18.8` Controlled Default-Mode Cutover.
10. `P18.R` Workflow Migration Closure.

P18.1 does not derive completion from Git or filesystem state at runtime.

## Repository Binding

The repository binding is durable and repository-relative:

- repository display name: `AGENT PLATFORM`
- expected branch: `p18-manual-to-hermes-workflow-migration`
- product root: `2_products/pepper-agent`
- branch parent commit: committed P18.0
- upstream main commit: `92d1e790e70176ed542b1ae44d6e8af771be512b`
- branch policy: one branch per macroproject and one commit per ticket

No personal absolute Windows path is encoded in the public model.

## Constraints

Canonical constraints include:

- Pepper is a customized Hermes-derived product.
- Reuse inherited Pepper/Hermes capability first.
- Duplicate equivalent runtime logic is prohibited.
- Human Git authority remains required.
- Upstream Hermes setup is not Pepper workflow authority.
- Generic dashboard provider state is not P17/P18 authority.
- Production readiness is not claimed.
- G-Brain is deferred to P19.
- Paperclip is deferred to P20.
- Multi-agent automation is deferred to P21.

## Context References

Context references are bounded pointers, not copied content.  Canonical references cover P18.0 workflow contracts, P17.R closure evidence, P18 roadmap posture, repository metadata, the P18.0 prerequisite commit and current capability reconciliation.

P18.1 does not copy entire documents or chats into the intake result.

## Human Intake Approval

Human intake approval is explicit declarative evidence.  It is required, approved and human-confirmed for the accepted canonical intake.  It is not authentication, cryptographic identity or a digital signature.

The canonical request builder requires a caller-supplied `ProjectIntakeApproval`; it does not fabricate human approval.

## Governed Transition

The accepted flow is:

1. Initial P18.0 workflow snapshot state is `draft`.
2. Bounded Pepper project intake request validates.
3. Human intake approval is present.
4. P18.1 builds a P18.0 `project_intake_completed` transition request.
5. P18.0 transition builder returns accepted `DRAFT -> INTAKE_READY` evidence.
6. `ProjectIntakeResult` is accepted and `P18_2_ready` is true.

## P17 Authority Preservation

Project intake preserves P17 authority boundaries:

- provider dispatch authorized: false
- model inference authorized: false
- automatic Git authority: false
- human Git authority required: true
- production readiness claimed: false

## Deterministic Identity

Project intake IDs and digests bind schema, policy, project identity, roadmap, repository binding, constraints, references, approval, previous workflow snapshot, transition result, resulting workflow snapshot, findings, summary, state and decision.

They do not bind wall clock, hostname, process, thread, UUID, randomness, environment, filesystem state, runtime-discovered Git state or raw command output.  Digests are deterministic integrity records, not signatures.

## Context Boundary

P18.1 intake may contain explicit project identity, macroproject identity, roadmap posture, current ticket, prerequisites, repository-relative product root, expected branch, known commit identities, constraints, bounded source references and human intake approval.

P18.1 intake must not contain raw conversation history, raw ChatGPT transcripts, raw OpenCode transcripts, entire Markdown documents, source file snapshots, stdout, stderr, diffs, environment variables, credentials, auth files, prompts, provider responses or reasoning traces.

This is explicit workflow context.  It is not G-Brain.

## P19 G-Brain Boundary

G-Brain is not available in P18.1.  P19 owns persistent shared memory, cross-session durable knowledge, provenance-aware context retrieval, supersession-aware knowledge and continuously updated agent memory.

P18.1 creates no vector store, memory database, semantic memory, chat-history memory, persistent knowledge graph or long-term context store.

## P20 Paperclip Boundary

Paperclip is not available in P18.1.  P20 owns the durable work-control plane.

P18.1 is a governed contract, not a competing durable project/work management database.  Operational Hermes/Kanban persistence remains reused where appropriate.

## P18.2 Handoff

P18.2 may consume the accepted project intake identity, roadmap, repository binding, constraints, context references, approval, request, result, summary and resulting governed workflow snapshot.

Accepted handoff requirements:

- project intake requirement satisfied: true
- resulting workflow state: `intake_ready`
- P18.2 ready: true

P18.2 owns Ticket Factory runtime integration, TicketSpec production from governed intake/context, TicketSpec-to-WorkPacket continuation and workflow progression toward ticket approval.  P18.1 does not execute Ticket Factory.

## Residual Limitations

- Pepper-only intake scope.
- Explicit context only.
- Persistent memory absent, deferred to P19.
- Durable work control absent, deferred to P20.
- Ticket Factory runtime integration absent, deferred to P18.2.
- Full approval workflow absent, deferred to P18.3.
- Dependency queue not reimplemented; owner is P18.4.
- Provider dispatch absent.
- Model inference absent.
- Git execution absent.
- Production readiness false.
