# P17.R - WorkPacket Execution MVP Closure

P17.R closes P17, the Governed WorkPacket Execution MVP, by binding P17.0 through P17.8 into one deterministic closure contract. It is a reconciliation layer only: it introduces no new runtime execution authority, no Git execution, no provider dispatch, no model inference, no network access, no Docker, no Graphify, no automatic retry, no automatic fallback, no automatic cleanup, no automatic rollback, and no production deployment authority.

Final verdict: hermes_0_19_pepper_governed_work_packet_execution_mvp_closed_with_non_critical_pilot_and_bounded_human_authority

## P17 Purpose

P17 establishes a governed WorkPacket Execution MVP for Pepper. The accepted chain compiles approved TicketSpec evidence into WorkPacket evidence, binds a human-provisioned workspace, applies deny-first permissions, records externally driven single-agent execution, runs exact human-authorized validation commands through the accepted runner, creates terminal outcome envelopes, records human-observed diff and artifact review, emits a non-executing human Git handoff, and proves the full chain with one accepted non-critical pilot.

P17.R does not claim that Pepper workflow migration is complete. It does not claim that Pepper UI is already the default execution surface. It does not authorize generic upstream Hermes setup as Pepper authority, critical-ticket execution, arbitrary-ticket execution, provider-backed execution, model-backed execution, automatic retry, automatic fallback, automatic cleanup, automatic rollback, automatic Git staging, automatic Git commit, automatic Git push, production operation, multi-agent execution, or parallel execution.

## Accepted Inventory

| Ticket | Title | Verdict |
| --- | --- | --- |
| P17.0 | TicketSpec to WorkPacket Compiler | `hermes_0_19_pepper_ticket_spec_to_work_packet_compiler_ready_with_compile_only_non_executing_authority` |
| P17.1 | Workspace Allocator | `hermes_0_19_pepper_work_packet_workspace_allocator_ready_with_human_provisioned_exclusive_non_executing_authority` |
| P17.2 | Tool Permission Profiles | `hermes_0_19_pepper_tool_permission_profiles_ready_with_deterministic_deny_first_non_executing_authority` |
| P17.3 | Single-Agent Ticket Executor | `hermes_0_19_pepper_single_agent_work_packet_execution_ready_with_externally_driven_permission_gated_filesystem_only_authority` |
| P17.4 | Validation Command Runner | `hermes_0_19_pepper_validation_command_runner_ready_with_exact_human_authorized_shell_free_bounded_subprocess_authority` |
| P17.5 | Result, Failure and Cancellation Envelopes | `hermes_0_19_pepper_result_failure_cancellation_envelopes_ready_with_deterministic_bounded_terminal_outcome_authority` |
| P17.6 | Diff and Artifact Review | `hermes_0_19_pepper_diff_and_artifact_review_ready_with_deterministic_human_observed_non_mutating_candidate_and_artifact_authority` |
| P17.7 | Human Git Handoff | `hermes_0_19_pepper_human_git_handoff_ready_with_exact_review_bound_non_executing_human_only_git_authority` |
| P17.8 | Non-Critical Ticket Pilot | `hermes_0_19_pepper_non_critical_ticket_pilot_ready_with_complete_governed_work_packet_chain_and_human_only_git_handoff_evidence` |

The closure contract accepts exactly these nine tickets in P17.0 through P17.8 order. No synthetic P17 ticket is inserted and no accepted prerequisite verdict is reinterpreted.

## WorkPacket Chain

The closure binds the exact prerequisite chain recorded by `P17TicketAcceptance`. P17.0 has no P17 prerequisite. P17.1 depends on P17.0. P17.2 depends on P17.1. P17.3 depends on P17.0, P17.1, and P17.2. P17.4 depends on P17.3. P17.5 depends on P17.3 and P17.4. P17.6 depends on P17.5. P17.7 depends on P17.6. P17.8 depends on P17.0 through P17.7.

Each acceptance record carries a bounded title, primary contract, capability summary, authority summary, and deterministic SHA-256 digest. Digests are integrity evidence, not digital signatures.

## Capability Reconciliation

P17.R records 18 capabilities. `CAP-P17-001` through `CAP-P17-009` are satisfied by P17.0 through P17.8. Provider-backed execution, model-backed execution, automatic Git execution, critical-ticket support, and production readiness are absent by design. Workflow migration is deferred to P18. Persistent shared governed memory is deferred to P19. Durable work-control authority is deferred to P20. Governed multi-agent automation is deferred to P21.

Deferred capabilities grant no P17 runtime authority. They are handoff constraints for later projects, not hidden P17 implementation.

## Authority Boundary

`P17AuthorityBoundary` keeps provider dispatch, model inference, network access, Docker, Graphify mutation, automatic retry, automatic fallback, automatic cleanup, automatic rollback, automatic staging, automatic commit, automatic push, critical-ticket execution, production execution, multi-agent execution, and parallel execution unauthorized. Human Git authority remains required.

P17.R does not execute Git and does not claim that Git was executed. The accepted P17.7 and P17.8 posture remains human-only and non-executing.

## Security Boundary

`P17SecurityBoundary` disallows credential contents, raw provider responses, raw prompts, reasoning traces, raw stdout, raw stderr, raw diffs, source snapshots, environment values, personal absolute paths, runtime handles, Git handles, digital-signature claims, and digest-as-signature claims.

The closure result contains bounded identifiers, titles, summaries, authority flags, security flags, deferred project IDs, pilot identifiers, pilot digests, finding summaries, and closure readiness booleans only.

## Accepted Limitations

P17.R accepts 13 residual limitations. The non-critical pilot is the only pilot. Critical tickets are unsupported. Provider dispatch and model inference are absent from the WorkPacket MVP. Git remains human-only. Automatic retry, automatic fallback, automatic cleanup, automatic rollback, and workflow migration are deferred to P18. Persistent shared agent memory is deferred to P19. Durable work control is deferred to P20. Multi-agent automation is deferred to P21. Production readiness is not claimed.

Each limitation is accepted and non-blocking for P17 closure. A blocking limitation would reject closure.

## Non-Critical Pilot Evidence

P17.R consumes one accepted `NonCriticalTicketPilotResult`. The pilot must be completed, accepted, non-critical, WorkPacket MVP satisfied, P17 closure ready, production readiness false, provider dispatch count zero, model inference count zero, and Git command count zero.

Pending manual validation IDs from the accepted P17.8 pilot remain warnings. They are not silently converted into successes and they do not block P17 closure.

## P18 Readiness

P17.R hands off to P18, Manual-to-Hermes Workflow Migration. The first ticket is P18.0, Governed Workflow State Machine. P18 may begin only after P17.R is reviewed, committed, and pushed.

P18 must not assume greenfield reimplementation. P18 must inspect existing Pepper and Hermes capabilities before implementing new workflow-engine logic. Direct reuse is preferred when existing contracts satisfy Pepper requirements. Customization of inherited Hermes logic is allowed when Pepper requires different behavior. Replacement is allowed only when concrete gap evidence justifies it. Duplicate runtime logic without gap evidence is prohibited.

P18 must assess existing Hermes Kanban Swarm, planner, dispatcher, workspace handling, heartbeat, retry, reclaim, task lifecycle, approval hooks, and existing dashboard or TUI workflow surfaces. P17.R does not assert that all of these will be adopted unchanged. The rule is reuse, customize, or replace based on evidence, not duplicate blindly.

## Pepper Identity

Pepper is a customized Hermes-derived product, not an external governance wrapper around Hermes and not a parallel runtime beside Hermes. Hermes upstream remains the reference and source. Pepper may retain inherited Hermes logic, customize inherited Hermes logic, replace inherited Hermes logic when gap evidence requires it, and add Pepper-specific capabilities.

Conceptually:

```text
Hermes upstream
    -> controlled fork and productization
Pepper
    -> retained Hermes logic
    -> customized Hermes logic
    -> replaced Hermes logic
    -> Pepper-specific capabilities
```

Generic upstream setup state and generic dashboard provider state are not P17 authority for Pepper.

## Future Boundaries

P19 is G-Brain Knowledge Integration. Its purpose is persistent shared governed memory for the Pepper ecosystem. Future memory must be persistent, shared across authorized agents, continuously updated, provenance aware, versioned, supersession aware, authority aware, and context-selection enabled. Agent context must not depend solely on one chat or session context window. Intended consumers include Lead Agent, Ticket Factory, execution agents, review agents, workflow engine, and Pepper UI. P17.R does not claim G-Brain exists yet and does not implement memory.

P20 is Paperclip Work Control Plane Integration. Paperclip is planned but not available now. P17.R does not make Hermes Kanban SQLite the irreversible long-term source of truth. P18 may use or customize Hermes operational task-state capabilities, while P20 may later establish durable work-control authority.

P21 is Governed Multi-Agent Automation. P17.R records multi-agent automation as deferred and does not claim multi-agent or parallel execution readiness.

## Manual Workflow Migration Target

The current manual workflow remains external to P17.R: context and planning, manually generated ticket, copy to OpenCode, execution, copy evidence back, external review, correction ticket, human Git handoff, and manual next-ticket progression.

The P18 target is Pepper UI intake, governed project and ticket intake, Ticket Factory, WorkPacket, Pepper and Hermes runtime workflow, governed execution, validation, review, approval, human Git handoff, and next workflow transition. P18.7 should perform shadow comparison with the manual workflow. P18.8 should perform controlled default-mode cutover. P18.R should close the migration. P17.R does not claim this migration already exists.
