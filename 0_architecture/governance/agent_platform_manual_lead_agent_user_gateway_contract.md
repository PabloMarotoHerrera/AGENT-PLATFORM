# Manual Lead Agent / User Gateway Contract

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Manual Lead Agent / User Gateway Contract |
| Ticket | P7.0.A |
| Status | Accepted Manual Lead Agent / User Gateway Contract |
| Date | 2026-07-05 |
| Scope | Manual workflow contract for AGENT PLATFORM / Siamese, moving toward AL-1.5 manual controlled agentic workflow. |
| Authority | Manual workflow design only, not agent runtime activation, autonomous orchestration, automatic dispatch, automatic handoff, automatic reviewer assignment, automatic Git mutation, provider/auth/API/MCP activation, Hermes runtime, GBrain runtime, Cadence, live connector activation, product/Siamese source inspection, persistence, vector DB, graph DB, Graphify adoption, Codegraph adoption, Cognitive Semantic System substrate selection, or publication. |
| Related documents | P6.7, P6.1, P6.2, P6.3, P6.4, P6.5, P6.6 if present, P5.R, P5.1-P5.7, P3.BR, P3.3, P3.4, P3.5, P2.1, P2.2, P2.3, P2.KR, P1.1-P1.5, P0.1-P0.3, S-03, S-04, CSS ADR/audit. |
| Optional sibling inputs | P7.0.B, P7.0.C, and P7.0.D are present and aligned by P7.0-NATIVE-ALIGN-01 as `manual_bridge_layer` peers; P7.0.E-P7.0.R remain downstream future consumers only. |
| Output | Manual Lead Agent / User Gateway Contract |

P7 designs the manual operating model. P7.0.A does not activate agent runtime. P7.0.A does not automate orchestration. Manual workflow design is not runtime activation.

## 2. Purpose

P7 formalizes the manual agentic workflow currently used by the user and lead planning chat. P7.0.A defines the manual lead agent / user gateway role.

The Manual Lead Agent receives user objectives, generates roadmaps, generates work packets and tickets, synthesizes returned outputs, routes review needs, integrates results, and provides exact Git command advice. The user manually runs tickets in external agents or harnesses. The user returns outputs to the Manual Lead Agent. The user performs Git manually.

P7.0.A does not activate runtime. P7.0.A does not automate orchestration. P7.0.A does not execute agents, tools, providers, MCP, GBrain, Hermes, Cadence, or product behavior. P7.0.A does not mutate Git.

## 3. Current Posture

| Area | Current state | P7.0.A interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM activation level | AL-1 metadata skeleton moving toward AL-1.5 manual controlled agentic workflow. | Manual workflow contract only. | AL-2 autonomous runtime. |
| AL-1.5 manual controlled workflow | Target posture. | User-mediated planning, ticketing, review, integration, and Git advice. | Autonomous orchestration. |
| lead agent role | Main planning chat role. | Manual Lead Agent coordination. | Internal agent runtime. |
| user gateway | Human boundary. | User controls objectives, execution, approvals, and Git. | Automatic gateway or daemon. |
| roadmap generation | Manual planning advice. | RoadmapDraft generation. | Automatic dispatch. |
| work packet generation | Manual ticket text. | WorkPacketGenerationRequest output. | Automatic task execution. |
| parallel manual agents | User-run external agents/harnesses. | Manual execution by user. | Internal parallel orchestration. |
| reviewer agents | Manually invoked reviewers. | ReviewRoutingRequest prompts. | Automatic reviewer assignment, auto-review. |
| integrator role | Manual synthesis role. | IntegrationRequest support. | Automatic merge or mutation. |
| commit advice | Exact command advice. | CommitAdviceRequest output. | automatic commit, auto-commit, automatic push, auto-push. |
| user Git authority | User final authority. | User decides and runs Git. | Agent Git mutation. |
| context packs | Manual context artifacts. | Allowed as markdown/manual packs. | Source loading or persistence DB. |
| memory manifests | Manual manifest artifacts. | Allowed as manual records. | Vector DB, graph DB, live retrieval. |
| external harness usage | Manual harness operation. | OpenCode/Codex/Claude/Cursor as H0 manual candidates. | H2/H3 adapters or autonomous orchestration. |
| OpenCode/Codex/Claude/Cursor/Hermes candidates | External/manual candidates. | Manual harness or future design references. | active Hermes runtime. |
| GBrain candidate | External memory architecture candidate. | Reference only, future inactive. | active GBrain runtime. |
| Graphify evidence | Curated generated supporting evidence. | Evidence only. | Graphify Authority, Graphify truth engine, Graphify substrate. |
| product/Siamese | Product vision. | Product boundary retained. | product/Siamese source readable by default. |
| provider/auth/API/MCP | Not active. | Metadata only. | active provider/auth, active MCP. |
| autonomous orchestration | Not active. | Blocked. | autonomous orchestrator. |

P7.0.A is manual workflow design only. Manual lead agent is a role, not a runtime process. The user remains final authority.

## 4. Inputs Reviewed

| Input group | Document | Review mode | User gateway use | Limitation |
| --- | --- | --- | --- | --- |
| P6 operational readiness and contracts | P6.7, P6.1-P6.6 paths | operational_contract_review | Operational planning baseline. | No runtime activation. |
| P5 skeleton audit and implementation docs | P5.R and P5.1-P5.7 paths | implementation_skeleton_review | Skeleton baseline and blockers. | No skeleton activation. |
| P3 activation decisions | P3.BR, P3.3, P3.4, P3.5 paths | activation_decision_review | Activation boundaries. | Deferred decisions remain deferred. |
| P2/P2.K cross-lane and retrieval architecture | P2.1, P2.2, P2.3, P2.KR paths | metadata_contract_review | Vocabulary, evidence, retention, retrieval boundaries. | No substrate or runtime approval. |
| P1 metadata contracts | P1.1-P1.5 paths | governance_markdown_review | Context/provider/tool/agent/CSS boundaries. | Metadata is not execution. |
| P0 gates/security/validation | P0.1-P0.3 paths | governance_markdown_review | Gate and validation/security constraints. | No gate execution. |
| S-03/S-04 policies | Security policy paths | governance_markdown_review | Secret, credential, shell, tool, network, MCP boundaries. | No enforcement activation. |
| optional P7 sibling docs | P7.0.B-P7.0.R paths | not_reviewed_blocked | Future downstream consumers. | Absent; not created. |

## 5. Manual Lead Agent / User Gateway Model

| Component | Meaning | Allowed use | Blocked use | Downstream consumer |
| --- | --- | --- | --- | --- |
| Manual Lead Agent | Role of the main planning chat. | Interpret objectives, draft roadmaps, create tickets, synthesize outputs. | Internal agent runtime. | P7.0.B-P7.0.G. |
| User Gateway | Governed boundary between user intent and manual workflow. | Capture objective, constraints, decisions, and final authority. | Autonomous gateway. | All P7 manual workflow contracts. |
| Manual Planning Session | Human-mediated session metadata. | Track phase, packets, review, integration, commit advice. | Persistent runtime state. | P7.0.R. |
| Manual Work Packet Generation | Ticket text generation. | Produce exact manual tickets. | Automatic dispatch. | P7.0.B/P7.0.C. |
| Manual Agent Execution Boundary | User-run external agents/harnesses. | User manually runs tickets and returns outputs. | Agent execution by platform. | P7.0.E. |
| Manual Review Routing | Human-directed review prompt routing. | Generate reviewer prompts and checklists. | Automatic reviewer assignment. | P7.0.F. |
| Manual Integration | Lead/integrator synthesis. | Reconcile returned outputs and reviews. | Automatic merge/mutation. | P7.0.G. |
| Manual Commit Advisory | Exact Git command advice. | Provide explicit paths and commit message. | Git mutation by agent. | P7.0.G. |
| Human Decision Point | Explicit user decision moment. | Require user choice before expansion/approval/Git. | Inferred approval from silence. | All P7 contracts. |

Lead Agent is the role of the main planning chat. User Gateway is the governed boundary between user intent and manual agentic workflow. This is not a runtime orchestrator. This is not an autonomous agent.

## Manual Bridge Layer Classification

This document belongs to the `manual_bridge_layer`.

Lead Agent = user gateway / manual control plane.

The Lead Agent is the `user_gateway` and `manual_control_plane`.

The Lead Agent is part of the `manual_bridge_layer` and is the manual bridge layer entry point for user-facing planning.

The Lead Agent is not the `agent_native_internal_organization_layer`.

Lead Agent is not the agent-native internal organization layer.

The Lead Agent translates user objectives into manual planning artifacts. It projects user-facing intent into roadmap, work packet, review, integration, and commit-advice structures.

The Lead Agent is not the final internal agent architecture, a human-style boss agent, an autonomous orchestrator, a runtime scheduler, an execution engine, a provider/tool activator, or a Git actor.

The Lead Agent does not command runtime agents.

The Lead Agent does not define the optimal internal topology.

The Lead Agent may request topology selection metadata but does not activate topology.

The Lead Agent may prepare manual tickets but does not dispatch agents.

The Lead Agent does not activate orchestration.

The Lead Agent may advise Git commands but never mutates Git.

## 6. Manual Workflow Lifecycle

| Step | Actor | Input | Output | Allowed action | Blocked action | Human decision point |
| --- | --- | --- | --- | --- | --- | --- |
| User objective | User | Goal and constraints. | UserObjective. | State desired outcome. | Execution approval by objective alone. | Confirm scope. |
| Lead agent / main planning chat | Manual Lead Agent | UserObjective. | LeadAgentSession. | Clarify and structure. | Runtime start. | Confirm assumptions. |
| Roadmap generation | Manual Lead Agent | RoadmapRequest. | RoadmapDraft. | Planning advice. | Dispatch work. | Accept roadmap. |
| Work packet decomposition | Manual Lead Agent | RoadmapDraft. | Candidate tickets. | Manual decomposition. | Automatic task creation in runtime. | Select ticket. |
| Manual ticket generation | Manual Lead Agent | WorkPacketGenerationRequest. | Ticket text. | Exact manual ticket. | Automatic dispatch. | User chooses harness. |
| User runs tickets manually | User | Ticket text. | External agent output. | Run in external harness. | Internal platform execution. | User decides what to run. |
| User returns outputs | User | Agent output. | Output refs/context. | Paste or summarize outputs. | Automatic ingest. | Decide what to submit. |
| Reviewer agents review outputs manually | User and reviewer harness | ReviewRoutingRequest. | Reviewer verdict. | Manual review. | Automatic reviewer assignment. | User accepts review route. |
| Integrator / lead agent reconciles outputs | Manual Lead Agent | IntegrationRequest. | Final verdict. | Synthesis and advice. | File mutation unless explicitly requested and allowed. | User accepts integration. |
| Final verdict | Manual Lead Agent | Integrated evidence. | Accepted/rejected register. | State outcome. | Runtime approval. | User final decision. |
| Exact git add / commit / push command advice | Manual Lead Agent | CommitAdviceRequest. | Exact command block. | Advice only. | Git mutation. | User decides whether to commit. |
| User performs Git manually | User | Command advice. | Commit/push if user chooses. | Manual Git. | Agent commit/push. | User final authority. |

## 7. Object Model

| Object | Meaning | Required fields | Forbidden fields | Allowed use | Blocked interpretation |
| --- | --- | --- | --- | --- | --- |
| `UserObjective` | User-supplied goal object. | objective id/text/scope/constraints/boundaries/owner/decisions. | Credentials, API keys, source contents. | Capture intent. | Execution approval. |
| `LeadAgentSession` | Main planning session metadata. | session id, objective ref, phase, refs, blockers, limitations. | Daemon state, scheduler id. | Manual coordination. | Runtime state. |
| `RoadmapRequest` | Request to generate roadmap. | objective ref, scope, granularity, required inputs/boundaries. | Dispatch targets. | Planning prompt. | Automatic orchestration. |
| `RoadmapDraft` | Proposed roadmap output. | phases, workstreams, tickets, dependencies, groups, blockers. | Runtime queue entries. | Planning advice. | Work dispatch. |
| `WorkPacketGenerationRequest` | Ticket/work packet generation request. | target ticket, lane, scope, inputs, allowed/blocked actions, commands, sections, stop rules. | Live assignment ids. | Manual ticket generation. | Automatic dispatch. |
| `ReviewRoutingRequest` | Manual reviewer routing request. | output ref, review type, reviewer role, checklist, verdict format, escalation. | Reviewer daemon config. | Manual review prompt. | Automatic reviewer assignment. |
| `IntegrationRequest` | Manual synthesis request. | output refs, verdict refs, registers, reconciliation scope, final verdict, commit advice. | Merge automation. | Manual integration. | Automatic mutation. |
| `CommitAdviceRequest` | Exact Git command advice request. | accepted refs, exact paths, git add paths, message, push target, rollback note, blocked patterns. | Git token, automatic commit flag. | Advice only. | Git mutation. |
| `HumanDecisionPoint` | Explicit user decision moment. | id, label, scope, owner, options, recommendation, risks, evidence, blocked auto-action. | Silent approval flag. | Require explicit choice. | Automatic approval. |

## 8. UserObjective Contract

Required fields: `objective_id`, `objective_text`, `objective_scope`, `project_area`, `desired_output`, `constraints`, `blocked_actions`, `source_boundaries`, `product_boundaries`, `external_boundaries`, `sensitivity`, `human_owner`, `decision_points`, and `limitations`.

UserObjective is not execution approval. UserObjective is not source loading permission. UserObjective is not product activation. UserObjective is not provider/auth approval.

## 9. LeadAgentSession Contract

Required fields: `session_id`, `user_objective_ref`, `lead_agent_role`, `session_scope`, `active_phase`, `roadmap_refs`, `work_packet_refs`, `review_refs`, `integration_refs`, `commit_advice_refs`, `context_refs`, `memory_manifest_refs`, `harness_refs`, `blockers`, `limitations`, and `human_decision_points`.

LeadAgentSession is a manual coordination record. LeadAgentSession is not runtime state. LeadAgentSession is not persistence. LeadAgentSession is not autonomous orchestration.

## 10. RoadmapRequest / RoadmapDraft Contract

`RoadmapRequest` fields: `roadmap_request_id`, `user_objective_ref`, `requested_scope`, `desired_granularity`, `parallelization_preference`, `blocked_work_types`, `required_inputs`, `required_boundaries`, and `human_decision_points`.

`RoadmapDraft` fields: `roadmap_draft_id`, `roadmap_request_ref`, `phases`, `workstreams`, `candidate_tickets`, `dependency_map`, `parallelization_groups`, `integrator_tickets`, `reviewer_tickets`, `blockers`, `limitations`, and `recommended_next_ticket`.

RoadmapDraft is planning advice. RoadmapDraft does not dispatch work. RoadmapDraft does not activate agents.

## 11. WorkPacketGenerationRequest Contract

Required fields: `work_packet_generation_request_id`, `roadmap_ref`, `target_ticket`, `agent_lane`, `scope`, `target_document_or_files`, `mandatory_inputs`, `allowed_actions`, `blocked_actions`, `allowed_commands`, `forbidden_commands`, `required_sections`, `expected_response_format`, `commit_advice_requirement`, `stop_rules`, and `human_approval_required`.

WorkPacketGenerationRequest produces manual ticket text only. It does not assign or dispatch work automatically. The user manually runs the ticket.

## 12. ReviewRoutingRequest Contract

Required fields: `review_routing_request_id`, `agent_output_ref`, `review_type`, `reviewer_role`, `review_checklist_ref`, `required_inputs`, `blocked_review_actions`, `required_verdict_format`, `escalation_route`, and `human_decision_points`.

Review types: architecture review, security review, validation review, consistency review, memory/context review, external boundary review, and product boundary review.

ReviewRoutingRequest is manual routing. It does not automatically assign reviewers. Reviewer verdict is not Git approval.

## 13. IntegrationRequest Contract

Required fields: `integration_request_id`, `input_output_refs`, `review_verdict_refs`, `drift_register_required`, `accepted_output_register_required`, `rejected_output_register_required`, `reconciliation_scope`, `final_verdict_required`, `commit_advice_required`, and `human_decision_points`.

IntegrationRequest supports manual reconciliation. It does not mutate files. It does not approve Git automatically.

## 14. CommitAdviceRequest Contract

Required fields: `commit_advice_request_id`, `accepted_output_refs`, `exact_paths`, `git_status_required`, `git_add_paths`, `commit_message`, `push_target`, `rollback_note`, `blocked_git_patterns`, and `human_commit_authority`.

Mandatory Git rules: The agent never mutates Git. The user commits and pushes manually. The agent gives exact `git add` paths. Never recommend git add . Never stage, commit, push, force-add, or publish on behalf of the user.

## 15. HumanDecisionPoint Contract

Required fields: `decision_point_id`, `decision_label`, `decision_scope`, `decision_owner`, `options`, `recommended_option`, `risks`, `required_evidence`, `blocked_automatic_action`, and `decision_required_before`.

HumanDecisionPoint is required before scope expansion, review acceptance, product-bound work, external source review, runtime activation, tool/provider/agent activation, publication, and Git mutation. Human decision is not inferred from silence.

## 16. Manual Execution Boundary

The user manually copies tickets into external agents/harnesses. The user manually returns outputs. The lead agent may synthesize outputs. The lead agent may generate reviewer prompts. The lead agent may generate integrator prompts. The lead agent may generate exact Git advice. No automatic dispatch exists. No automatic handoff exists. No internal runtime exists.

| Manual action | Allowed actor | Allowed use | Blocked automation |
| --- | --- | --- | --- |
| Copy ticket to external harness | User | Manual execution outside AGENT PLATFORM runtime. | Automatic dispatch. |
| Return output | User | Paste or summarize output. | Automatic ingest. |
| Synthesize output | Manual Lead Agent | Summarize and reconcile. | File mutation by default. |
| Generate reviewer prompt | Manual Lead Agent | Manual review routing. | Automatic reviewer assignment. |
| Generate integrator prompt | Manual Lead Agent | Manual integration. | Automatic merge. |
| Generate Git advice | Manual Lead Agent | Exact command advice. | Git mutation. |

## 17. Git Advisory Boundary

| Git advisory item | Required rule | Blocked pattern |
| --- | --- | --- |
| exact path commit advice | Include only exact paths. | `git add .` |
| command blocks | Use explicit path commands. | Staging broad paths. |
| prohibited broad add | Never recommend git add . | `git add .` |
| no Git mutation by agent | Advice only. | Agent-run stage/commit/push. |
| user final authority | User decides and runs Git. | Reviewer verdict as Git approval. |
| rollback note | Include rollback caution where useful. | Automatic rollback. |
| dirty tree warning | Warn if unrelated changes appear. | Reverting user changes. |
| generated output caution | Avoid tracking generated outputs unless explicitly approved. | Generated output tracking expansion. |

Required command pattern:

```powershell
git status --short

git add <exact_path_1> `
        <exact_path_2>

git commit -m "<exact ticket message>"

git push origin main
```

Commands are advice only. The user performs them manually.

## 18. Context / Memory Boundary

| Context/memory surface | P7.0.A use | Blocked interpretation |
| --- | --- | --- |
| Manual context packs | Allowed as manually curated context. | Source loading permission. |
| Manual memory manifests | Allowed as markdown/manual manifests. | Persistent memory runtime. |
| Markdown canonical context | Allowed. | Database-backed memory. |
| Curated Graphify evidence refs | Evidence only if already approved. | Graphify Authority or substrate. |
| GBrain-style refs | Candidate notation only. | Active GBrain runtime. |
| Vector DB / graph DB / embeddings | Blocked. | Cognitive Semantic System substrate selected. |
| Live retrieval / Cadence | Blocked. | Active Cadence or always-on memory. |

Manual context packs are allowed. Manual memory manifests are allowed. Markdown canonical context is allowed. Curated Graphify evidence refs may be used only as evidence if already approved. GBrain-style refs may be candidate notation only. Active GBrain runtime is blocked. Vector DB, graph DB, embeddings, persistent memory, live retrieval, and Cadence are blocked.

## 19. Harness Boundary

| Harness | Classification | Allowed P7.0.A use | Blocked use | Required future review |
| --- | --- | --- | --- | --- |
| OpenCode | Manual external development harness candidate. | H0 manual use. | H2/H3 adapter activation. | P7.0.E. |
| Codex | External coding/review harness candidate. | Manual ticket execution by user. | Internal runtime. | P7.0.E. |
| Claude | External coding/review harness candidate. | Manual review or generation by user. | Provider/API activation by platform. | P7.0.E/P3.4. |
| Cursor | External coding/review harness candidate. | Manual IDE/harness use by user. | Runtime orchestration. | P7.0.E. |
| Hermes | External agent runtime / orchestration / Cadence candidate only. | H1 design reference. | active Hermes runtime, active Cadence. | P7.0.E/future exact review. |
| GBrain | External memory architecture candidate only. | Manual reference notation. | active GBrain runtime. | Future EXT review. |
| Graphify | Generated evidence tooling / repo map evidence. | Curated evidence refs only. | Graphify rerun/adoption/authority. | Future exact evidence review. |

P7.0.A allows manual H0 harness use and H1 design only. P7.0.A blocks H2 controlled tool execution adapter and H3 autonomous orchestration adapter.

## 20. Interfaces With P7.0.B-P7.0.R

| Downstream ticket | What it consumes from P7.0.A | Required alignment | Blocked shortcut |
| --- | --- | --- | --- |
| P7.0.B Roadmap Generation / Work Breakdown Contract | UserObjective, RoadmapRequest, RoadmapDraft. | Manual planning only. | Automatic dispatch. |
| P7.0.C Parallel Agent Lane / Work Packet Taxonomy | WorkPacketGenerationRequest and lane boundary. | Manual parallelization only. | Internal orchestration. |
| P7.0.D Manual Context / Memory Manifest Strategy | Context/memory boundary. | Manual markdown manifests. | Persistent memory runtime. |
| P7.0.E Manual Harness Strategy / OpenCode-Hermes Boundary | Harness boundary. | H0/H1 only. | H2/H3 activation. |
| P7.0.F Reviewer Agent / Approval Pipeline Contract | ReviewRoutingRequest and HumanDecisionPoint. | Manual review routing. | Automatic approval or assignment. |
| P7.0.G Integrator / Reconciliation / Commit Advisory Protocol | IntegrationRequest and CommitAdviceRequest. | Manual integration and exact Git advice. | Git mutation. |
| P7.0.H First Manual Pilot Playbook | Lifecycle and stop rules. | Manual pilot only. | Runtime launch. |
| P7.0.R Manual Agentic Workflow Planning Closure | All P7.0.A objects and blockers. | Closure audit. | Activation by closure alone. |

P7.0.A does not start downstream tickets.

## 21. Interfaces With Prior Governance

| Upstream document group | P7.0.A consumption | Preserved boundary |
| --- | --- | --- |
| P6 operational contracts | AL-1.5 planning baseline. | Operational contracts do not activate runtime. |
| P5 skeleton baseline | Manual workflow references skeletons. | Skeletons are not active services. |
| P3 activation decisions | Activation constraints. | Deferred decisions remain deferred. |
| P2/P2.K knowledge/retrieval architecture | Vocabulary, evidence, retention, retrieval posture. | No substrate selection. |
| P1 metadata contracts | Context/provider/tool/agent/CSS boundaries. | Metadata is not execution. |
| P0 gates | Gate and validation/security constraints. | Gates are not bypassed. |
| S-03/S-04 | Secrets, credentials, shell, network, MCP constraints. | No credential or tool execution. |
| CSS ADR/audit | Accepted naming and substrate posture. | Cognitive Semantic System substrate remains deferred. |

## 22. Stop Rules

Stop on autonomous orchestration request. Stop on internal agent runtime request. Stop on automatic dispatch request. Stop on automatic handoff request. Stop on automatic reviewer assignment request. Stop on automatic commit/push request. Stop on provider/auth/API/MCP activation request. Stop on credential request. Stop on API call request. Stop on MCP activation request. Stop on Hermes runtime request. Stop on GBrain runtime request. Stop on Cadence request. Stop on live connector request. Stop on product/Siamese source request. Stop on persistence DB request. Stop on vector DB request. Stop on graph DB request. Stop on source loading request. Stop on source inspection request. Stop on Graphify rerun/adoption request. Stop on Codegraph execution/adoption request. Stop on tool execution request. Stop on agent execution request. Stop on publication request. Stop on source tracking expansion request. Stop on generated output tracking request. Stop on Cognitive Semantic System substrate selection request. Stop on Git mutation by agent request. Stop on `git add .` recommendation request.

## 23. Future Validation Targets

Future validation targets, not executed:

| Target | Status |
| --- | --- |
| UserObjective required field completeness. | Future only. |
| LeadAgentSession required field completeness. | Future only. |
| RoadmapRequest required field completeness. | Future only. |
| RoadmapDraft required field completeness. | Future only. |
| WorkPacketGenerationRequest required field completeness. | Future only. |
| ReviewRoutingRequest required field completeness. | Future only. |
| IntegrationRequest required field completeness. | Future only. |
| CommitAdviceRequest required field completeness. | Future only. |
| HumanDecisionPoint required field completeness. | Future only. |
| Manual workflow lifecycle completeness. | Future only. |
| No autonomous orchestration invariant. | Future only. |
| No internal runtime invariant. | Future only. |
| No automatic dispatch invariant. | Future only. |
| No automatic reviewer assignment invariant. | Future only. |
| No automatic Git mutation invariant. | Future only. |
| Exact git path command invariant. | Future only. |
| No `git add .` invariant. | Future only. |
| User final authority invariant. | Future only. |
| P7.0.B consumption readiness. | Future only. |
| P7.0.G commit advisory alignment readiness. | Future only. |
| P7.0.R planning closure readiness. | Future only. |

## 24. Future Hardening Candidates

Future tickets, not started:

| Candidate | Description |
| --- | --- |
| P7-HARD-01 | UserObjective Schema Candidate. |
| P7-HARD-02 | LeadAgentSession Schema Candidate. |
| P7-HARD-03 | Manual Ticket Generation Checklist. |
| P7-HARD-04 | Manual Human Decision Point Matrix. |
| P7-HARD-05 | Manual Git Advisory Checklist. |
| P7-HARD-06 | No-Autonomous-Orchestration Invariant Checklist. |
| P7-HARD-07 | Lead Agent Session Context Pack Format. |
| P7-HARD-08 | P7.1 Pilot Gateway Checklist. |
| P7-HARD-09 | User Final Authority Checklist. |
| P7-HARD-10 | Manual Workflow Closure Audit Input. |

## 25. Created / Not Created Register

Created:

| File |
| --- |
| `0_architecture/governance/agent_platform_manual_lead_agent_user_gateway_contract.md` |

Modified:

| Scope |
| --- |
| none |

Not created / not approved:

| Item | Posture |
| --- | --- |
| runtime activation | Not created or approved. |
| autonomous orchestration | Not created or approved. |
| internal agent runtime | Not created or approved. |
| automatic task dispatch | Not created or approved. |
| automatic handoff | Not created or approved. |
| automatic reviewer assignment | Not created or approved. |
| automatic commits | Not created or approved. |
| automatic pushes | Not created or approved. |
| provider/auth/API/MCP activation | Not created or approved. |
| credential use | Not performed. |
| API calls | Not performed. |
| MCP activation | Not created or approved. |
| Hermes runtime | Not created or approved. |
| GBrain runtime | Not created or approved. |
| Cadence | Not created or approved. |
| live connectors | Not created or approved. |
| product/Siamese source inspection | Not performed. |
| source loading | Not created or approved. |
| source inspection | Not performed. |
| persistence DB | Not created or approved. |
| vector DB | Not created or approved. |
| graph DB | Not created or approved. |
| telemetry | Not created or approved. |
| event streaming | Not created or approved. |
| Graphify rerun/adoption | Not created or approved. |
| Codegraph execution/adoption | Not created or approved. |
| tool execution | Not created or approved. |
| agent execution | Not created or approved. |
| validation execution | Not created or approved. |
| security enforcement activation | Not created or approved. |
| generated output tracking | Not created or approved. |
| source tracking expansion | Not created or approved. |
| publication | Not created or approved. |
| Git mutation by the agent | Not performed. |
| Cognitive Semantic System substrate selection | Not performed. |

## 26. Recommended Next Ticket

After P7.0.A, the recommended parallel queue is:

| Ticket | Sequence posture |
| --- | --- |
| P7.0.B - Roadmap Generation / Work Breakdown Contract | Recommended actual next ticket. |
| P7.0.C - Parallel Agent Lane / Work Packet Taxonomy | Parallel downstream. |
| P7.0.D - Manual Context / Memory Manifest Strategy | Parallel downstream. |
| P7.0.E - Manual Harness Strategy / OpenCode-Hermes Boundary | Parallel downstream. |
| P7.0.F - Reviewer Agent / Approval Pipeline Contract | Parallel downstream. |
| P7.0.G - Integrator / Reconciliation / Commit Advisory Protocol | Parallel downstream. |

Recommended actual: P7.0.B - Roadmap Generation / Work Breakdown Contract.

Do not start P7.0.B. Do not start P7.0.C. Do not start P7.0.D. Do not start P7.0.E. Do not start P7.0.F. Do not start P7.0.G. Do not start P7.0.H. Do not start P7.0.R.

## 27. Final Verdict

| Question | Answer |
| --- | --- |
| What did P7.0.A create? | The canonical Manual Lead Agent / User Gateway Contract. |
| What Manual Lead Agent contract was defined? | The main planning chat role that receives objectives, creates roadmaps/tickets, synthesizes outputs, routes review, integrates results, and provides Git advice manually. |
| What User Gateway contract was defined? | The human-mediated boundary where the user supplies objectives, chooses tickets/harnesses, returns outputs, makes decisions, and remains final authority. |
| What UserObjective object was defined? | A user-supplied goal object with scope, constraints, boundaries, sensitivity, owner, decision points, and limitations. |
| What LeadAgentSession object was defined? | A manual coordination record, not runtime state or persistence. |
| What RoadmapRequest object was defined? | A request to generate roadmap advice. |
| What RoadmapDraft object was defined? | A planning output with phases, workstreams, tickets, dependencies, and next-ticket advice. |
| What WorkPacketGenerationRequest object was defined? | A request to create manual ticket/work packet text. |
| What ReviewRoutingRequest object was defined? | A manual reviewer routing request, not automatic reviewer assignment. |
| What IntegrationRequest object was defined? | A manual reconciliation/synthesis request, not file mutation. |
| What CommitAdviceRequest object was defined? | A request for exact Git command advice with explicit paths only. |
| What HumanDecisionPoint object was defined? | An explicit user decision requirement before scope expansion, acceptance, runtime/product/external work, publication, or Git mutation. |
| What manual workflow lifecycle was defined? | User objective to lead planning chat to roadmap to tickets to user-run external agents to returned outputs to manual review to integration to final verdict to Git advice to user-run Git. |
| How does the user interact with the lead agent? | By giving objectives, constraints, returned outputs, decisions, and final Git authority. |
| How does the lead agent generate roadmaps? | As planning advice from RoadmapRequest into RoadmapDraft. |
| How does the lead agent generate tickets? | As manual WorkPacketGenerationRequest outputs, not dispatched tasks. |
| How does the user manually run tickets? | By copying tickets into external agents/harnesses and returning outputs. |
| How are outputs returned? | Manually by the user to the lead planning chat. |
| How are reviews routed? | Through manual ReviewRoutingRequest prompts and user-mediated reviewer invocation. |
| How are integrations requested? | Through IntegrationRequest for manual reconciliation and final verdict. |
| How are Git commands advised? | Exact path command blocks only; never recommend git add . |
| Who performs Git commits and pushes? | The human user. |
| Did P7.0.A activate agent runtime? | No. |
| Did P7.0.A automate orchestration? | No. |
| Did P7.0.A dispatch tasks automatically? | No. |
| Did P7.0.A execute agents, tools, providers, MCP, GBrain, Hermes, Cadence, or product behavior? | No. |
| Did P7.0.A mutate Git? | No. |
| Did P7.0.A inspect product/Siamese source? | No. |
| Did P7.0.A activate provider/auth/API/MCP? | No. |
| Did P7.0.A create persistence, vector DB, graph DB, or live retrieval? | No. |
| What is the next recommended ticket? | P7.0.B - Roadmap Generation / Work Breakdown Contract. |

Stop after P7.0.A. Do not start P7.0.B, P7.0.C, P7.0.D, P7.0.E, P7.0.F, P7.0.G, P7.0.H, P7.0.R, P7.1, P8, P4, or EXT.*.
