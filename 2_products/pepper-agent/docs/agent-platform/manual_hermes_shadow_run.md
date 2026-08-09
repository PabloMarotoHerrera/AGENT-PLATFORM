# P18.7 Manual Versus Hermes Shadow Run

Final verdict: hermes_0_19_pepper_manual_versus_hermes_shadow_run_ready_with_end_to_end_semantic_comparison_and_explicit_cutover_gap_detection

## Purpose

P18.7 records a bounded manual-versus-Pepper shadow comparison for one representative non-critical work item. It measures whether the accepted P18.1 through P18.6 workflow contracts can represent the same operator flow currently handled through manual ChatGPT/OpenCode copy and paste.

P18.7 is measurement only. It does not switch Pepper to default mode, auto-approve tickets, invoke providers or models, start OpenCode, mutate Kanban, mutate Git, run Docker, run Graphify, write G-Brain memory, operate Paperclip, or perform production deployment.

## Selected Shadow Ticket

- `shadow_ticket_id`: `P18.UI-A-SHADOW-ROUTE-SMOKE`
- `shadow_ticket_title`: `Agent Platform route-readiness shadow smoke`
- `project_id`: `PEPPER`
- `macroproject_id`: `P18`
- `repository_scope`: `Agent Platform UI route and backend readiness projection`
- `risk_classification`: `non_critical`
- `why_selected`: bounded read-only validation of accepted product UI activation surfaces.
- `expected_candidate_paths`: `web/src/agent-platform/product-ui-activation-canonical.test.ts`
- `expected_validation`: frontend route activation smoke and P18 workflow regression lane.
- `destructive_side_effects`: `false`

This work item is not P18.7 or P18.8, requires no credentials, requires no provider/model setup, and does not perform a broad refactor.

## P18.6 Continuation Identity

- `P18_6_commit`: `4658fd1576e546fc3029a6125e41186c7e5cbe26`
- `P18_6_result_SHA256`: `54ca05cf9bfdb99047b94954a57571ce94c9afeb4fbc5ac7600a73d5b3000b2c`
- `project_id`: `PEPPER`
- `macroproject_id`: `P18`
- `implementation_lineage_ticket_id`: `P18.2`
- `recovery_boundary`: `RECOVERY_DECISION_ONLY`

The implementation lineage remains the governed P18 workflow chain. The selected shadow ticket identity is separate and is `P18.UI-A-SHADOW-ROUTE-SMOKE`.

## Manual Baseline

- `manual_project_context_source`: bounded roadmap state from current operator conversation.
- `manual_ticket_generation_method`: lead agent summarizes the next bounded ticket.
- `manual_executor`: OpenCode operator session.
- `manual_execution_trigger`: human sends ticket to executor.
- `manual_result_collection_method`: bounded evidence pasted back by operator.
- `manual_validation_method`: operator runs focused validation commands.
- `manual_review_method`: human and lead agent review bounded evidence.
- `manual_approval_method`: human textual approval.
- `manual_Git_handoff_method`: lead agent gives exact human Git commands.
- `manual_commit_authority`: `human`
- `manual_push_authority`: `human`
- `manual_copy_paste_steps`: `5`
- `manual_context_restatement_steps`: `2`
- `manual_confirmation_steps`: `2`
- `manual_shell_steps`: `4`
- `manual_review_steps`: `2`
- `manual_total_human_decisions`: `4`
- `raw_conversation_history_persisted`: `false`
- `raw_OpenCode_transcript_persisted`: `false`

Only bounded summaries and SHA-256 references are stored. Raw ChatGPT and OpenCode transcripts are not persisted.

## Manual Authority Map

Manual authority remains human-owned for project selection, ticket approval, execution authorization, retry and rollback decisions, Git staging, Git commit, Git push, and next-ticket selection. The executor and validation commands can be machine-assisted, but the operator still performs transfer, authorization, collection, review, and Git execution.

## Pepper Path

P18.7 binds the same shadow ticket through the accepted Pepper workflow evidence sequence:

- P18.1 Project Intake
- P18.2 Ticket Factory Runtime
- P18.3 Approval Workflow
- P18.4 Dependency-Aware Queue
- accepted P17 execution and outcome substrate
- P18.5 Review and Validation
- P18.6 Recovery Governance over deterministic fixture evidence when the real shadow ticket succeeds
- P17.7 Human Git Handoff boundary

The Pepper path creates no duplicate project-intake, ticket-factory, approval, dependency-queue, executor, validation-runner, review, recovery, or Git-handoff engines.

## Workspace Isolation

- `manual_execution_workspace`: `manual-shadow-read-only-projection`
- `Pepper_execution_workspace`: `pepper-shadow-read-only-projection`
- `isolation_method`: deterministic read-only evidence mode over common committed checkout.
- `common_parent_commit`: `4658fd1576e546fc3029a6125e41186c7e5cbe26`
- `equivalent_initial_state`: `true`
- `cleanup_required`: `false`
- `cleanup_performed`: `false`
- `destructive_cleanup_performed`: `false`

The selected work item is validation/readiness evidence and does not mutate either workspace.

## Semantic Comparison

| Dimension | Result | Notes |
|---|---|---|
| project_context | EQUIVALENT | Pepper preserves bounded project context without raw chats. |
| ticket_semantics | EQUIVALENT | Objective, scope, constraints and authority boundaries are preserved semantically. |
| approval | EQUIVALENT | Backend contract records independent human approval evidence. |
| dependency_gate | MATCH | The selected work item is dependency-satisfied. |
| execution | EQUIVALENT | Execution evidence is bounded to read-only route smoke. |
| validation | MATCH | Both paths rely on deterministic route and workflow validation. |
| review | EQUIVALENT | P18.5 review semantics match manual review classification. |
| recovery | MATCH | No natural failure is fabricated; recovery comparison uses deterministic P18.6 fixture evidence. |
| Git_handoff | MATCH | Human-only Git handoff boundaries remain exact. |
| workflow_state | EQUIVALENT | Pepper records deterministic state progression. |
| UI_visibility | BLOCKED | UI lacks required live approval and execution operation visibility. |
| operator_effort | MANUAL_BETTER | Manual chat and OpenCode transfer remain required today. |
| authority | PEPPER_BETTER | Pepper authority is stricter or equal to manual authority. |
| security | MATCH | Neither path persists credentials, tokens, raw transcripts or hidden reasoning. |
| evidence_completeness | PEPPER_BETTER | Pepper evidence is deterministic and digest-bound across stages. |

`semantic_shadow_equivalence`: `true`

## UI And Backend Evidence

| Surface | Route | Backend/API | Classification |
|---|---|---|---|
| Projects | `/agent-platform/projects` | `/api/plugins/kanban/boards` | `functional_read_only_projection` |
| Project board | `/agent-platform/projects/:boardSlug` | `/api/plugins/kanban/board` | `functional_read_only_projection` |
| Ticket detail | `/agent-platform/projects/:boardSlug/tickets/:taskId` | `/api/plugins/kanban/tasks/{task_id}` | `functional_read_only_projection` |
| Approvals | `/agent-platform/approvals` | not-yet-established approval HTTP backend | `unavailable_backend` |
| Executions | `/agent-platform/executions` | qualified Kanban task projection | `functional_read_only_projection` |
| Execution detail | `/agent-platform/executions/:executionId` | qualified Kanban task projection | `functional_read_only_projection` |

Source inspection confirms product UI routes are active, but approvals have no production HTTP approval source and executions are limited to qualified read-only Kanban task evidence. Mutating workflow actions must remain authenticated and are not made public by P18.7.

`HUMAN_UI_SMOKE_BLOCKED` is recorded because a real human visual smoke with live approve/reject and execution state controls cannot pass against the current product surfaces.

## Readiness Gates

- `semantic_shadow_equivalence`: `true`
- `governance_equivalence`: `true`
- `authority_equivalence`: `true`
- `Pepper_authority_stricter_or_equal`: `true`
- `Projects_operational`: `true`
- `Tickets_operational`: `false`
- `Approvals_operational`: `false`
- `Executions_operational`: `false`
- `review_visibility_operational`: `false`
- `next_action_visible`: `false`
- `normal_workflow_requires_chat`: `true`
- `manual_OpenCode_ticket_copy_required`: `true`
- `manual_OpenCode_result_copy_required`: `true`
- `cutover_blocking_gap_count`: `4`

P18.8 readiness decision: `P18_8_BLOCKED`

This is a successful P18.7 measurement outcome, not a P18.7 failure.

## Migration Gaps

| Gap | Category | Stage | Required P18.8 Correction | Blocks Cutover |
|---|---|---|---|---|
| P18-8-GAP-001 | UI_BACKEND_GAP | approval | Add authenticated approval list, detail, approve and reject actions. | true |
| P18-8-GAP-002 | EXECUTOR_INTEGRATION_GAP | execution | Add live governed execution collection, detail and status projection. | true |
| P18-8-GAP-003 | CONTEXT_GAP | project_context | Surface roadmap state, current ticket and next action in Pepper UI. | true |
| P18-8-GAP-004 | HUMAN_ACTION_GAP | execution | Bridge accepted worker invocation and result ingestion through Pepper. | true |

## Chat And OpenCode Dependency

Chat dependency audit:

- `roadmap_state`: `REQUIRED`
- `project_context`: `REQUIRED`
- `ticket_generation`: `REQUIRED`
- `approval_decision_storage`: `NOT_REQUIRED`
- `review`: `REQUIRED`
- `recovery_decision`: `NOT_REQUIRED`
- `next_action`: `REQUIRED`
- `Git_handoff_construction`: `REQUIRED`
- `normal_workflow_requires_this_chat`: `true`

OpenCode manual dependency audit:

- `manual_OpenCode_ticket_paste`: `true`
- `manual_OpenCode_start`: `true`
- `manual_OpenCode_result_copy`: `true`
- `manual_OpenCode_result_interpretation`: `true`

## Context And Paperclip Boundary

Minimum project context currently captured without G-Brain:

- project identity
- roadmap position
- workflow result digests
- repository branch identity

`GBrain_required_for_P18_8`: `false`

`Paperclip_required_for_P18_8`: `false`

P18.8 is blocked by workflow-control context still being centered in chat, not by the absence of P19 G-Brain or P20 Paperclip.

## Git Safety

- `automatic_git_add`: `false`
- `automatic_git_commit`: `false`
- `automatic_git_push`: `false`
- `candidate_paths_exact`: `true`
- `staging_boundaries_exact`: `true`
- `diff_check_present`: `true`
- `staged_verification_present`: `true`
- `commit_message_present`: `true`
- `push_target_present`: `true`
- `human_only_execution_preserved`: `true`

P18.7 prepares comparison evidence only. Human Git authority remains intact.

## Validation Evidence

Focused P18.7 tests cover request determinism, manual evidence normalization, Pepper evidence normalization, semantic equivalence, equivalent-but-not-identical prose, authority comparison, stricter Pepper authority, authority regression rejection, UI blocker detection, approval UI blocker, execution UI blocker, context blocker, manual copy/paste counting, chat dependency audit, OpenCode dependency audit, P18.8 readiness and blocked decisions, gap taxonomy, stale evidence, wrong parent commit, wrong ticket, wrong project, wrong WorkPacket, security, serialization stability, digest determinism and tamper rejection.

## Residual Limitations

- P18.7 does not implement approval HTTP backend or approval UI actions.
- P18.7 does not implement live governed execution backend or worker invocation bridge.
- P18.7 does not remove normal workflow dependence on this chat.
- P18.7 does not remove manual OpenCode transfer.
- P18.7 does not start P18.8 default-mode cutover.
- P18.7 does not implement G-Brain or Paperclip.
