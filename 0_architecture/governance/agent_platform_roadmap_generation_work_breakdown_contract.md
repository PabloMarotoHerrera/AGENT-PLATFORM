# P7.0.B - Roadmap Generation / Work Breakdown Contract

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Roadmap Generation / Work Breakdown Contract |
| Ticket | P7.0.B |
| Status | Accepted roadmap generation / work breakdown contract |
| Date | 2026-07-05 |
| Scope | Manual workflow design for converting a user objective into roadmap phases, workstreams, work packets, dependencies, parallelization groups, review objects, integration summaries, and exact commit advice metadata for AGENT PLATFORM / Siamese. |
| Authority | Documentation-only roadmap and work-breakdown contract. Not runtime orchestration, agent runtime activation, task execution, handoff execution, validation execution, security enforcement, provider/auth/API/MCP activation, source loading, product activation, external adoption, substrate selection, generated-output tracking, source tracking expansion, publication, or Git mutation. |
| Related documents | P6.7-REFRESH, P6.1-P6.6, EXT.GB-01, P5.R, P5.1-P5.7, P3.BR, P3.R, P3.0-P3.5, P2.KR, P2.R, P2.1-P2.3, P1.1-P1.5, P0.1-P0.3, G-01, G-19, S-03, S-04, Cognitive Semantic System ADR/audit, README.md, `.gitignore`, `.graphifyignore`. |
| Output | Canonical P7.0.B contract for manual roadmap generation and work breakdown. |

P7.0.B defines how AGENT PLATFORM may plan work. It does not perform the work.

## 2. Purpose

P7.0.B establishes the canonical contract for turning a user objective into a bounded roadmap and work breakdown that can be reviewed by humans and later executed only through explicit, separate instructions.

The contract exists because P6 readiness is accepted for operational planning, but AGENT PLATFORM remains AL-1 metadata skeleton. The next safe posture is a manual controlled agentic workflow design: agents may draft structured plans, packets, reviews, integration summaries, and exact commit advice, while the user remains final execution authority and final Git authority.

P7.0.B is not a task runner, scheduler, orchestrator, dispatch protocol, approval engine, validation runner, source loader, or runtime implementation.

## 3. Current Baseline

| Area | Current baseline inherited by P7.0.B |
| --- | --- |
| Activation posture | AGENT PLATFORM remains AL-1 metadata skeleton. |
| P6 readiness | Accepted for operational planning only. |
| P6 output | `p6_operational_contract_set_complete`, `no_unresolved_p6_operational_readiness_drift`, and `future_activation_level_review_eligible_as_planning_only`. |
| Activation transition | `activation_level_transition: not_approved`. |
| Runtime activation | `runtime_activation: not_approved`. |
| Product posture | Product-bound work remains blocked pending P4. |
| External posture | EXT.* reviews remain required before external adoption. |
| GBrain posture | Strongest current external candidate class only; not adopted, executed, dependency-approved, provider/auth-approved, MCP-active, Cadence-active, or substrate. |
| Graphify posture | Supporting generated evidence only, not authority, not source, not substrate, not adopted. |
| Cognitive Semantic System posture | Substrate deferred; markdown canonical docs plus metadata refs remain baseline. |
| Security posture | S-03 and S-04 blocked defaults remain active. |
| Git posture | Exact human approval required; no broad staging and no `git add .` recommendation. |

P7.0.B may describe an AL-1.5 manual controlled workflow posture, but it does not approve an activation-level transition.

## 4. Inputs Reviewed

Inputs were reviewed as governance metadata and documentation only. No product source, external source, GBrain source, Graphify source, raw generated output, secrets, credentials, provider config, token store, browser auth, local credential store, API key, validation runtime, tests, scripts, package manager, provider/API/network/MCP call, runtime, or Git mutation was used.

| Input | P7.0.B use | Boundary preserved |
| --- | --- | --- |
| P6.7-REFRESH | Accepted operational readiness audit and P6 closure. | Planning only; no activation. |
| P6.1 Agent Registry / Capability Registry | Agent/capability metadata precedent. | Registry is not runtime. |
| P6.2 Agent-to-Agent Communication Protocol | Message and handoff metadata precedent. | Protocol is not dispatch. |
| P6.3 Shared Context / Evidence Bus | SourceRef, EvidenceRef, context/evidence bus metadata precedent. | Bus is not persistence. |
| P6.4 Human Approval / Review Loop | ApprovalRef and review metadata precedent. | ApprovalRef is not approval. |
| P6.5 Runtime Monitoring / Incident Handling | Monitoring and incident metadata precedent. | Monitoring model is not monitoring runtime. |
| P6.6 Cognitive Semantic System Substrate Decision | Substrate deferred and GBrain/Graphify boundaries. | No substrate selected. |
| EXT.GB-01 | Present limited read-only external intake. | GBrain not adopted; future EXT.GB-HARD required. |
| P5.R and P5.1-P5.7 | AL-1 skeleton audit and non-active component baseline. | Skeletons are not activation. |
| P3.BR and P3.0-P3.5/P3.R | Activation decisions and readiness blockers. | Tool/provider/agent activation remains blocked. |
| P2.KR, P2.R, P2.1-P2.3 | Knowledge/retrieval boundary, vocabulary, EvidenceRef, audit/retention/rollback. | No retrieval runtime or persistence. |
| P1.1-P1.5 | Context, provider, tool, agent, and CSS metadata hardening. | Metadata contracts are not runtime activation. |
| P0.1-P0.3 | Gate map, validation gate design, and security hardening design. | Gates are not approvals. |
| G-01 | Activation gate charter and no-loose-project fields. | Roadmap phase is not permission. |
| G-19 | Parallel lane and work packet dependency model. | Parallel lanes are planning lanes only. |
| S-03 | Local-only, secrets, credentials, generated output, product/external handling. | No secret/credential content inspection or local-only publication. |
| S-04 | Tool, shell, network, MCP, package, build, test, Git execution policy. | No execution by availability. |
| Cognitive Semantic System ADR/audit | Naming and substrate neutrality. | Cognitive Semantic System not implemented; substrate undecided. |
| README.md | Root workspace descriptor. | No runtime effect. |
| `.gitignore` | Local-only/generated/secrets/provider-auth hygiene. | Hygiene is not security. |
| `.graphifyignore` | Default-deny Graphify input posture. | Not permission to run Graphify. |

## 5. Non-Action Statement

P7.0.B creates a manual planning contract only.

| Not performed by P7.0.B | Reason |
| --- | --- |
| Runtime orchestration | Requires future runtime activation gate and implementation approval. |
| Agent execution, task execution, handoff execution, dispatch, queues, or scheduler | P6/P3 boundaries keep agent runtime blocked. |
| Automated review, approval, integration, or merge workflow | P6.4 remains metadata-only; user remains final authority. |
| Validation/test/build/script/package execution | S-04 and P0.2 require future exact gates. |
| Security enforcement or scanning | P0.3 is design only; no enforcement runtime. |
| Tool/shell/network/API/provider/MCP execution | S-04, GT-07, and GT-08 keep these blocked. |
| Source loading, product source inspection, external source inspection, GBrain source inspection, or raw generated output inspection | P6.7 and S-03 preserve these exclusions. |
| Product-bound work | P4 remains required before product-bound work. |
| External adoption, GBrain adoption, Hermes/Cadence activation, Graphify adoption, Codegraph execution | EXT.* or exact future gates remain required. |
| Cognitive Semantic System substrate selection | P6.6 deferred substrate remains active. |
| Persistence, graph DB, vector DB, embeddings, ontology runtime, event stream, telemetry, monitoring runtime, or generated output tracking | Not approved by P6.7. |
| Source tracking expansion, staging, commit, push, force-add, or publication | GT-12 and explicit human approval remain required. |

## 6. Authority Model

| Layer | P7.0.B authority |
| --- | --- |
| User | Final objective authority, execution authority, approval authority, and Git authority. |
| Lead planning agent | May draft roadmap, decomposition, ticket queue, review request metadata, integration summaries, and exact commit advice metadata. |
| Reviewer role | May draft findings, risks, test/validation recommendations, and acceptance blockers. |
| Integrator role | May draft integration summaries and exact file-specific commit advice. |
| Governance | Decides promotion, activation, exceptions, lifecycle, source tracking, product activation, provider activation, publication, and substrate decisions. |
| Validation | Evaluates evidence; does not decide activation or approval. |
| Security | Constrains local-only material, secrets, credentials, execution, provider/auth, products, external sources, generated outputs, publication, and Git posture. |
| Git | Records approved artifacts after explicit human action; Git does not create semantic truth. |
| Evidence | Supports decisions; does not decide. |

No agent role created by this contract may self-approve, execute runtime work, perform Git mutation, or bypass user/governance authority.

## 7. AL-1.5 Manual Workflow Boundary

P7.0.B defines a planning posture named `AL-1.5_manual_controlled_agentic_workflow` for vocabulary only.

| Boundary | Meaning |
| --- | --- |
| AL-1.5 is manual | The workflow produces human-readable plans and records only. |
| AL-1.5 is controlled | Each work packet must include exact scope, blockers, dependencies, and stop rules. |
| AL-1.5 is agentic in drafting only | Agents may propose, review, summarize, and advise. They do not execute runtime tasks. |
| AL-1.5 is not AL-2 | No source classification promotion, runtime activation, or controlled execution is approved. |
| AL-1.5 does not change P6.7 | `activation_level_transition: not_approved` remains active. |

Any future activation-level transition requires a separate exact ticket, human approval, validation targets, security review, rollback/incident posture, source classification, and applicable gates.

## Agent-Native Planning Projection

This document belongs to the `manual_bridge_layer` and adds conceptual references to the `agent_native_internal_organization_layer`.

Roadmap generation should consider agent-native topology before manual work packet projection.

The decomposition path is objective → topology selection → task graph / blackboard model → capability cell / reviewer mesh mapping → work packet projection → manual execution projection.

Roadmap is not merely a list of phases. Roadmap decomposition should consider agent-native topology before projecting work into manual tickets.

WorkPacket is a manual execution projection, not necessarily the internal unit of future agentic cognition.

ParallelizationGroup is a manual governance projection, not runtime scheduling.

ParallelizationGroup is a manual execution grouping, not necessarily a runtime scheduling primitive.

SequencingRule is a manual governance rule, not autonomous orchestration.

| Agent-native planning object | P7.0.B definition | Blocked interpretation |
| --- | --- | --- |
| `AgentNativeTopologySelection` | Manual metadata describing the conceptual topology considered for an objective before work packet projection. | Runtime topology activation or autonomous router. |
| `TaskGraphProjection` | Manual projection of objective work into task nodes, dependency edges, blocker edges, review edges, and integration edges. | Scheduler graph or runnable task queue. |
| `BlackboardPlanningRef` | Metadata reference to shared claims, evidence, blockers, contradictions, and unresolved questions used during planning. | Persistence runtime, graph DB, vector DB, or live shared state. |
| `CapabilityCellProjection` | Mapping from task needs to conceptual capability cells before selecting manual lanes or harnesses. | Active capability cell runtime. |
| `ReviewerMeshProjection` | Mapping from task risk, contradiction, and boundary needs to manual reviewer mesh metadata. | Automatic reviewer assignment or auto-review. |
| `ManualWorkPacketProjection` | Projection from task graph/cell/reviewer metadata into human-readable WorkPacket records. | Runnable task object. |
| `ManualExecutionProjection` | Projection from internal conceptual organization into manual tickets, manual lanes, manual harnesses, manual review, manual integration, and commit advice. | Autonomous dispatch, handoff, or runtime execution. |

## P7.0-NATIVE-ALIGN-01 Canonical Marker Evidence

This document intentionally carries the exact P7.0-NATIVE-ALIGN-01 marker `TaskGraphRef`.

`TaskGraphRef` is the canonical alias for the task graph metadata represented in this document through `TaskGraphProjection`.

`TaskGraphRef` is metadata only. It is not a scheduler graph, runnable task set, queue, graph DB, or task execution permission.

This document intentionally carries the exact P7.0-NATIVE-ALIGN-01 marker `BlackboardRef`.

`BlackboardRef` is the canonical alias for the shared claim/evidence/finding metadata represented in this document through `BlackboardPlanningRef`.

`BlackboardRef` is metadata only. It is not persistence, live shared state, vector DB, graph DB, event stream, or live retrieval.

This document intentionally carries the exact P7.0-NATIVE-ALIGN-01 marker `ManualExecutionProjection`.

`ManualExecutionProjection` is the projection from agent-native conceptual organization into manual tickets, manual lanes, manual harnesses, manual review, manual integration, and user-owned Git advice.

`ManualExecutionProjection` is not autonomous dispatch, runtime orchestration, task execution, handoff execution, automatic reviewer assignment, or Git mutation.

## 8. Roadmap Generation Contract

Roadmap generation converts a user objective into a structured planning artifact.

| Step | Required behavior | Blocked inference |
| --- | --- | --- |
| Capture objective | Restate the user objective, scope, non-goals, constraints, and authority. | Restatement is not approval to execute. |
| Classify scope | Identify governance, validation, security, context, provider, tool, agent, CSS, Graphify, external, and product surfaces. | Surface mention is not permission. |
| Identify gates | Map objective to G-01 gate types and P0/P1/P2/P3/P6 baselines. | Gate mapping is not gate approval. |
| Decompose phases | Split into ordered phases that can be reviewed. | Phase order is not command execution. |
| Create workstreams | Group related work without crossing blocked boundaries. | Workstream grouping is not runtime orchestration. |
| Create work packets | Define exact packet scope, dependencies, blockers, completion criteria, and review needs. | Work packet is not a running task. |
| Identify parallelization | Name safe parallel groups where no hard dependency exists. | Parallelizable does not mean concurrent execution runtime. |
| Create ticket queue | Recommend future ticket sequence and ticket kinds. | Recommendation does not start tickets. |
| Create review route | Define reviewer metadata and acceptance blockers. | Review route is not automated review. |
| Create integration route | Define integration-summary and commit-advice metadata. | Integration route is not staging, commit, push, or publication. |

## 9. Work Breakdown Contract

A work breakdown is valid only if each packet is small enough to review manually and explicit enough to prevent hidden activation.

| Required field | Rule |
| --- | --- |
| objective_ref | Reference to the user objective or roadmap objective. |
| exact_scope | Named files, docs, surfaces, or decisions included. |
| excluded_scope | Named exclusions, especially product, external, generated, credential, provider/auth, runtime, and Git surfaces. |
| lane | Planning lane or domain. |
| dependencies | Hard and soft dependencies. |
| blockers | Active blockers and expected future blockers. |
| stop_rules | Conditions requiring immediate stop. |
| completion_criteria | Observable completion conditions. |
| review_required | Human, governance, validation, security, product, or release review needs. |
| output_posture | Documentation, metadata, safe summary, generated-sensitive, local-only, or not applicable. |

If exact scope, owner, blockers, or stop rules are unknown, the packet remains `blocked_missing_scope` or `needs_review`.

## 10. UserObjective Object Model

`UserObjective` captures the user request before roadmap decomposition.

| Field | Meaning |
| --- | --- |
| `objective_id` | Stable objective identifier. |
| `objective_text` | User objective as restated without expanding permission. |
| `requester` | User or governance requester. |
| `desired_outcome` | Target planning or documentation outcome. |
| `in_scope` | Explicitly allowed docs, decisions, or metadata surfaces. |
| `out_of_scope` | Explicit exclusions and inherited blocked surfaces. |
| `constraints` | Security, validation, Git, source, product, external, runtime, and substrate constraints. |
| `authority_boundary` | Who may approve, execute, review, and commit. |
| `activation_posture` | Current AL posture and whether transition is approved. |
| `evidence_refs` | EvidenceRef-compatible inputs. |
| `blockers` | Known blockers before decomposition. |
| `stop_rules` | Stop triggers inherited by every downstream packet. |

`UserObjective` is planning metadata only.

## 11. Roadmap Object Model

`Roadmap` is the top-level planning artifact.

| Field | Meaning |
| --- | --- |
| `roadmap_id` | Stable roadmap identifier. |
| `objective_ref` | UserObjective reference. |
| `title` | Human-readable roadmap title. |
| `status` | `draft`, `candidate_for_review`, `accepted_for_planning`, `blocked`, `superseded`, or `retired`. |
| `activation_posture` | AL posture and non-activation statement. |
| `phases` | RoadmapPhase list. |
| `workstreams` | Workstream list. |
| `work_packets` | WorkPacket list. |
| `dependencies` | Dependency list. |
| `parallelization_groups` | ParallelizationGroup list. |
| `sequencing_rules` | SequencingRule list. |
| `blockers` | Blocker list. |
| `completion_criteria` | CompletionCriterion list. |
| `review_route` | Review object references. |
| `integration_route` | Integration object references. |
| `commit_advice` | CommitAdvice reference if a file change is proposed. |

`accepted_for_planning` does not mean active execution approval.

## 12. RoadmapPhase Object Model

`RoadmapPhase` organizes sequenced work.

| Field | Meaning |
| --- | --- |
| `phase_id` | Stable phase identifier. |
| `phase_name` | Human-readable phase name. |
| `purpose` | Phase purpose and decision target. |
| `entry_criteria` | Required prior records or approvals. |
| `exit_criteria` | CompletionCriterion refs required to close the phase. |
| `work_packet_refs` | Work packets included in this phase. |
| `hard_dependencies` | Dependencies that must be satisfied first. |
| `parallel_allowed` | Whether same-phase packets may proceed independently after human selection. |
| `blocked_scope` | Actions not allowed inside this phase. |
| `review_required` | Review needs before phase closure. |
| `next_phase_condition` | Exact condition before moving to a later phase. |

Phase progression is manual and requires user direction.

## 13. Workstream Object Model

`Workstream` groups related packets by domain or lane.

| Field | Meaning |
| --- | --- |
| `workstream_id` | Stable workstream identifier. |
| `lane` | Planning lane, such as governance, validation, security, context, provider, tool, agent, CSS, audit, Graphify support, product, or external review. |
| `scope` | Included docs/surfaces. |
| `excluded_scope` | Excluded sources/surfaces. |
| `owner_role` | Human/governance role expected to own decisions. |
| `packet_refs` | WorkPacket refs. |
| `shared_dependencies` | Dependencies shared by included packets. |
| `shared_blockers` | Blockers shared by included packets. |
| `evidence_requirements` | EvidenceRef, ValidationRef, SecurityRef, ApprovalRef needs. |
| `coordination_notes` | Manual coordination guidance. |

Workstreams are not runtime lanes.

## 14. WorkPacket Object Model

`WorkPacket` is the smallest unit P7.0.B may recommend for later manual selection.

| Field | Meaning |
| --- | --- |
| `work_packet_id` | Stable packet identifier. |
| `ticket_kind` | TicketKind value. |
| `title` | Human-readable packet title. |
| `objective_ref` | UserObjective or Roadmap ref. |
| `phase_ref` | RoadmapPhase ref. |
| `workstream_ref` | Workstream ref. |
| `allowed_scope` | Exact allowed docs, metadata surfaces, or decisions. |
| `blocked_scope` | Explicit non-goals and inherited blocked surfaces. |
| `dependency_refs` | Dependency refs. |
| `parallel_group_ref` | ParallelizationGroup ref if applicable. |
| `sequencing_rule_refs` | SequencingRule refs. |
| `blocker_refs` | Blocker refs. |
| `completion_criteria_refs` | CompletionCriterion refs. |
| `review_required` | Required review route. |
| `output_artifacts` | Expected documentation or metadata outputs. |
| `git_posture` | No Git mutation, exact-path advice only, or not applicable. |
| `status` | `draft`, `needs_review`, `blocked`, `eligible_for_user_selection`, `completed_by_separate_ticket`, `superseded`, or `retired`. |

`eligible_for_user_selection` means the user may explicitly ask to start it later. It does not start execution.

## 15. Dependency Object Model

`Dependency` records ordering and gating relationships.

| Field | Meaning |
| --- | --- |
| `dependency_id` | Stable dependency identifier. |
| `dependency_type` | `hard_sequence`, `soft_coordination`, `gate_required`, `evidence_required`, `review_required`, `human_approval_required`, `external_blocker`, `product_blocker`, `substrate_blocker`, or `git_blocker`. |
| `from_ref` | Upstream phase, packet, document, gate, or evidence ref. |
| `to_ref` | Downstream phase or packet. |
| `required_state` | State required before downstream work can begin. |
| `current_state` | Present, absent, blocked, accepted limitation, pending alignment, or unknown. |
| `blocking_effect` | What remains blocked. |
| `resolution_route` | Future ticket, review, gate, or human decision needed. |
| `evidence_refs` | Evidence supporting the dependency status. |

Dependencies record constraints; they do not enforce them technically.

## 16. ParallelizationGroup Object Model

`ParallelizationGroup` names work that may be planned in parallel without runtime concurrency.

| Field | Meaning |
| --- | --- |
| `parallelization_group_id` | Stable group identifier. |
| `group_name` | Human-readable group name. |
| `packet_refs` | Packets included in the group. |
| `parallelization_class` | `metadata_design_parallel`, `review_parallel`, `blocked_activation_parallel`, `evidence_support_parallel`, or `not_parallelizable`. |
| `shared_prerequisites` | Prerequisites each packet must satisfy. |
| `conflict_rules` | Conditions that prevent parallel planning. |
| `integration_required` | Whether a later integration summary is required. |
| `manual_coordination_notes` | Human coordination instructions. |

Parallelization groups are planning groups only. They do not create workers, queues, background jobs, or handoffs.

## 17. SequencingRule Object Model

`SequencingRule` constrains packet order.

| Field | Meaning |
| --- | --- |
| `sequencing_rule_id` | Stable rule identifier. |
| `rule_type` | `must_precede`, `must_follow`, `may_parallelize_after`, `blocked_until_gate`, `blocked_until_review`, `blocked_until_user_selection`, or `never_in_same_ticket`. |
| `subject_ref` | Packet, phase, workstream, or gate being constrained. |
| `constraint_ref` | Upstream condition or conflicting scope. |
| `rationale` | Why the rule exists. |
| `violation_stop_rule` | Stop trigger if the rule would be violated. |
| `evidence_refs` | Supporting governance/security/validation references. |

Required sequencing defaults: governance and security gates precede activation; P4 precedes product-bound work; EXT.* precedes external adoption; GT-10/GT-13 precede substrate/state decisions; GT-12 and human approval precede Git mutation or publication.

## 18. Blocker Object Model

`Blocker` preserves explicit stop conditions.

| Field | Meaning |
| --- | --- |
| `blocker_id` | Stable blocker identifier. |
| `blocker_type` | `scope_missing`, `owner_missing`, `evidence_missing`, `security_blocker`, `validation_blocker`, `product_blocker`, `external_blocker`, `runtime_blocker`, `execution_blocker`, `provider_auth_blocker`, `credential_blocker`, `source_loading_blocker`, `git_blocker`, `substrate_blocker`, or `peer_alignment_pending`. |
| `description` | Safe blocker description. |
| `affected_refs` | Roadmap, phase, workstream, or packet refs. |
| `current_status` | `open`, `accepted_limitation`, `expected_future_blocker`, `resolved`, `superseded`, or `unknown`. |
| `resolution_required` | Future gate, review, document, user decision, or exact approval required. |
| `must_stop_if_triggered` | Whether active work must stop. |
| `safe_reporting` | How to report without exposing sensitive content. |

Blockers remain active until a future authorized record resolves them.

## 19. CompletionCriterion Object Model

`CompletionCriterion` defines how a planning packet may be closed.

| Field | Meaning |
| --- | --- |
| `criterion_id` | Stable criterion identifier. |
| `target_ref` | Roadmap, phase, or packet. |
| `required_observable` | Exact observable documentation or metadata condition. |
| `proof_posture` | `document_reviewed`, `metadata_declared`, `reviewed_by_human`, `accepted_for_planning`, or future proof state. |
| `evidence_refs` | Evidence required. |
| `review_required` | Review required before closure. |
| `non_activation_confirmation` | Required statement that completion does not activate runtime or permissions. |
| `git_posture_confirmation` | Required statement if commit advice exists. |
| `residual_risks` | Known limitations after completion. |

Completion means the planning artifact is done. It does not mean implementation or execution is complete.

## 20. TicketKind Object Model

`TicketKind` classifies future tickets or packets.

| TicketKind | Allowed use | Blocked inference |
| --- | --- | --- |
| `governance_contract` | Create or update governance documentation. | Not activation. |
| `roadmap_planning` | Produce roadmap phases, dependencies, and packet queues. | Not task execution. |
| `validation_design` | Design validation route, criteria, and command proposals. | Not validation execution. |
| `security_hardening_design` | Design security posture and stop rules. | Not enforcement or scanning. |
| `metadata_contract_hardening` | Harden metadata-only contracts. | Not runtime implementation. |
| `review_packet` | Review docs, diffs, risks, or evidence within exact scope. | Not approval by itself. |
| `integration_summary` | Summarize completed manual changes and residual blockers. | Not merge automation. |
| `commit_advice` | Recommend exact file-specific Git commands for the user. | Not Git mutation. |
| `product_readiness_planning` | Plan product gates without inspecting product source. | Not product activation. |
| `external_review_planning` | Plan external review without executing or adopting external material. | Not external adoption. |
| `substrate_decision_planning` | Plan future CSS substrate evidence review. | Not substrate selection. |
| `activation_review_planning` | Plan activation-level review requirements. | Not activation-level transition. |

Any ticket kind that needs execution, source inspection, provider/auth, product work, external adoption, substrate selection, persistence, publication, or Git mutation must stop and route to the relevant future gate.

## 21. Review Object Models

Review objects capture manual review metadata only.

| Object | Fields | Boundary |
| --- | --- | --- |
| `ReviewRequest` | `review_id`, `target_ref`, `review_type`, `reviewer_role`, `scope`, `excluded_scope`, `criteria`, `evidence_refs`, `stop_rules`, `status` | Request is not approval. |
| `ReviewFinding` | `finding_id`, `review_id`, `severity`, `summary`, `evidence_refs`, `affected_refs`, `risk`, `recommendation`, `blocker_ref`, `status` | Finding is evidence, not automatic change. |
| `ReviewDecision` | `decision_id`, `review_id`, `decision_status`, `accepted_scope`, `limitations`, `required_follow_up`, `approval_ref`, `human_authority_required` | Decision metadata is not self-executing approval. |
| `ReviewBundle` | `bundle_id`, `review_request_refs`, `finding_refs`, `decision_refs`, `residual_risks`, `next_packet_refs` | Bundle is a summary, not dispatch. |

Review statuses include `draft`, `requested`, `in_manual_review`, `findings_reported`, `needs_changes`, `accepted_for_planning`, `blocked`, `superseded`, and `retired`.

## 22. Integration And Commit Advice Object Models

Integration objects summarize results after a separate authorized work item has occurred. P7.0.B does not perform that work.

| Object | Fields | Boundary |
| --- | --- | --- |
| `IntegrationSummary` | `integration_id`, `source_packet_refs`, `changed_artifacts`, `accepted_outputs`, `residual_blockers`, `review_refs`, `validation_refs`, `security_refs`, `next_recommendation`, `commit_advice_ref` | Summary is not merge automation. |
| `IntegrationDecision` | `decision_id`, `integration_id`, `decision_status`, `accepted_scope`, `deferred_items`, `rollback_notes`, `human_authority_required` | Decision metadata is not Git mutation. |
| `CommitAdvice` | `commit_advice_id`, `scope`, `exact_paths_to_stage`, `paths_not_to_stage`, `recommended_status_command`, `recommended_stage_command`, `recommended_commit_command`, `recommended_push_command`, `prohibited_commands`, `human_final_authority` | Advice is not executed. |

Commit advice rules:

| Rule | Requirement |
| --- | --- |
| Exact paths only | Recommend `git add <exact path>` only for intended files. |
| No broad staging | Never recommend `git add .`. |
| No force-add by default | Never recommend force-adding ignored/local-only files unless a future exact gate approves it. |
| User final authority | The user decides whether to run status, stage, commit, or push commands. |
| Sensitive blocker | If secrets, local-only content, generated-sensitive output, product source, external source, or unknown sensitivity is implicated, stop and do not recommend commit. |

## 23. Roadmap-To-Ticket Decomposition Procedure

The lead planning agent may use this deterministic manual procedure when asked to plan a roadmap.

| Step | Procedure |
| --- | --- |
| 1 | Create `UserObjective` from the user request and inherited constraints. |
| 2 | Identify in-scope and out-of-scope surfaces before reading or editing anything. |
| 3 | Map the objective to G-01 gate types and P0/P1/P2/P3/P5/P6/P7 boundaries. |
| 4 | Identify whether P4, EXT.*, GT-10, GT-12, GT-07, GT-08, or GT-15 is required before any part may proceed. |
| 5 | Record `AgentNativeTopologySelection` metadata before manual ticket projection. |
| 6 | Create `TaskGraphProjection` and `BlackboardPlanningRef` metadata for nodes, edges, blockers, evidence, review, and integration posture. |
| 7 | Map `CapabilityCellProjection` and `ReviewerMeshProjection` metadata before selecting manual lanes or reviewers. |
| 8 | Project the selected graph/cell/reviewer posture into `ManualWorkPacketProjection` records with exact allowed and blocked scope. |
| 9 | Split projected work into RoadmapPhases and Workstreams as human-facing manual planning views. |
| 10 | Create Dependencies and SequencingRules for every hard order constraint. |
| 11 | Create ParallelizationGroups only for metadata/design/review work that has no hard dependency conflict. |
| 12 | Attach Blockers and CompletionCriteria to each packet. |
| 13 | Create ReviewRequest metadata for packets that need human, validation, security, governance, product, or release review. |
| 14 | Create IntegrationSummary and CommitAdvice metadata only after separate authorized changes exist. |
| 15 | Preserve `ManualExecutionProjection` posture: no step authorizes runtime dispatch, autonomous handoff, automatic review, automatic integration, or Git mutation. |

No step authorizes execution, source loading, product work, external adoption, substrate selection, generated output tracking, source tracking expansion, publication, or Git mutation.

## 24. Parallelization And Sequencing Rules

| Rule | P7.0.B contract |
| --- | --- |
| Governance first | Gate and scope clarity must precede activation-sensitive work. |
| Security before exposure | Security review is required before local-only, secrets, credentials, provider/auth, product, external, generated output, publication, or Git-sensitive work. |
| Validation evaluates | Validation plans and evidence can support decisions but never approve activation or Git mutation. |
| Product work waits for P4 | Product-bound work, product source inspection, product execution, and product output handling remain blocked pending P4. |
| External adoption waits for EXT.* | External source/tool/provider/Cadence adoption remains blocked pending future exact reviews. |
| Substrate waits for GT-10/GT-13 | Cognitive Semantic System substrate, persistence, graph/vector/ontology runtime, and state stores remain blocked. |
| Runtime waits for activation gates | Runtime, scheduler, queue, worker, task execution, handoff execution, monitoring runtime, and incident automation remain blocked. |
| Git waits for human approval | Commit advice may be exact and file-specific, but user performs any Git action. |
| Parallel planning is not concurrency | Parallelization groups are manual planning convenience only. |

## 25. Required Boundaries And Stop Rules

STOP if any roadmap packet requires:

| Trigger | Required route |
| --- | --- |
| Runtime activation, scheduler, queue, worker, daemon, autonomous loop, task execution, handoff execution, or orchestration | Future GT-06/runtime gate and explicit instruction. |
| Tool, shell, subprocess, package, build, test, CI, Git mutation, or generated command execution | GT-07/GT-14/GT-12 and exact human approval as applicable. |
| Provider/auth/API/network/MCP call, credential use, token refresh, browser auth, local credential store, provider config, or API key use | GT-08 and explicit secure approval. |
| Secret or credential content | Stop; safe metadata only under S-03. |
| Product source inspection, product execution, product dependency, product output tracking, or product activation | P4/GT-09. |
| External source inspection beyond authorized metadata, external execution, source copying, dependency adoption, or external instruction adoption | EXT.* and GT-11. |
| GBrain/Hermes/Cadence adoption, execution, MCP activation, provider/auth approval, or Cadence/always-on behavior | EXT.GB-HARD or relevant EXT.* plus future exact gates. |
| Graphify rerun, raw output inspection, provider-labelled output, generated output tracking, or Graphify adoption | Future Graphify-specific gate; S-03/S-04/GT-12 as applicable. |
| Cognitive Semantic System substrate selection, graph DB, vector DB, embeddings, ontology runtime, persistence, event stream, telemetry, or semantic memory | GT-10/GT-13 and future substrate decision. |
| Source tracking expansion, force-add, staging, commit, push, or publication | GT-12 and explicit human approval. |
| P7.0.A/C/D/E/F/G/H/R, P7.1, P8, P4, EXT.*, runtime work, or product work inside P7.0.B | Stop; separate explicit instruction required. |

## 26. Product, External, Graphify, GBrain, And CSS Boundaries

| Surface | P7.0.B posture |
| --- | --- |
| Siamese | Product vision only. No product source inspection or product activation. P4 required before product-bound work. |
| Product workspaces | Local-only and inactive until product gate. |
| External sources | Evidence/review candidates only. No adoption, execution, copying, installation, or instruction adoption. |
| GBrain | Strongest current external candidate class by P6.6, but not adopted, executed, dependency-approved, provider/auth-approved, MCP-active, Cadence-active, persistent, or substrate. |
| Hermes/Cadence | Future/inactive references only. No always-on, scheduler, dream cycle, or runtime. |
| Graphify | Supporting generated evidence only. No rerun, raw output inspection, adoption, source authority, or substrate inference. |
| Cognitive Semantic System | Accepted name; substrate deferred; markdown canonical docs plus metadata refs remain baseline. |
| Graph/vector/database/ontology | Candidate concepts only; no runtime or persistence selected. |

## 27. Evidence, Validation, Security, And Approval Interfaces

| Interface | P7.0.B rule |
| --- | --- |
| EvidenceRef | Evidence supports planning and review; it does not decide. |
| ValidationRef | Validation evaluates; it does not approve execution, activation, product work, publication, or Git mutation. |
| SecurityRef | Security constrains exposure and action; it does not activate runtime by itself. |
| ApprovalRef | ApprovalRef is metadata; only explicit human/governance approval can approve exact scope. |
| SourceRef | SourceRef is metadata; it is not source loading permission. |
| ProductRef | ProductRef is product-scope metadata; it is not product activation. |
| GraphifyRef | GraphifyRef is generated evidence metadata; it is not authority. |
| CommitAdviceRef | CommitAdviceRef is user-facing advice only; it is not Git execution. |

All roadmap outputs must retain limitations, blockers, source posture, sensitivity posture, and non-activation language.

## 28. P7 Peer Alignment Register

Some optional P7 peer documents are present in the worktree as unreviewed, unconsumed files outside the P7.0.B authorized scope. Their presence is not treated as alignment, authority, or permission. P7.0.B preserves pending alignment markers until a future exact review consumes accepted peer records.

| Peer | Current status | Required marker | P7.0.B handling |
| --- | --- | --- | --- |
| P7.0.A Lead Gateway Alignment | Present and aligned by P7.0-NATIVE-ALIGN-01 | `resolved_by_alignment` | Consume Lead Agent as `user_gateway` / `manual_control_plane` in the `manual_bridge_layer`. |
| P7.0.C Lane Taxonomy Alignment | Present and aligned by P7.0-NATIVE-ALIGN-01 | `resolved_by_alignment` | Consume lane taxonomy as `manual_lane_projection` and `manual_execution_projection`, not final internal runtime taxonomy. |
| P7.0.D Memory Manifest Alignment | Present and aligned by P7.0-NATIVE-ALIGN-01 | `resolved_by_alignment` | Consume MemoryManifest as manual context metadata extended toward Context & Memory Fabric, not runtime memory. |
| P7.0.E Harness Boundary Alignment | Absent | `pending_P7.0.E_harness_boundary_alignment` | No harness runtime, OpenCode/MCP integration, hooks, or watch mode. |
| P7.0.F Reviewer Pipeline Alignment | Absent | `pending_P7.0.F_reviewer_pipeline_alignment` | Review objects are metadata only; no automated pipeline. |
| P7.0.G Integrator Commit Protocol Alignment | Absent | `pending_P7.0.G_integrator_commit_protocol_alignment` | Commit advice is exact-path only and never executed by this contract. |
| P7.0.H Roadmap Execution or Successor | Not started | `P7.0.H_not_started_expected` | Do not start from P7.0.B. |
| P7.0.R P7 reconciliation | Not started | `P7.0.R_not_started_expected` | Future reconciliation only if explicitly requested. |

If a future P7 peer contradicts this contract, create an explicit reconciliation record rather than silently changing execution posture.

## 29. Blocker And Pending Register

| Blocker | Status | Blocks |
| --- | --- | --- |
| `activation_level_transition_not_approved` | Active | AL transition and runtime activation. |
| `runtime_activation_not_approved` | Active | Scheduler, queue, worker, daemon, process lifecycle, autonomous loop. |
| `agent_task_handoff_execution_blocked` | Active | Agent execution, task execution, handoff execution, dispatch. |
| `tool_execution_blocked` | Active | Shell, subprocess, package, build, test, tool, Git execution by agents. |
| `provider_auth_api_mcp_blocked` | Active | Provider calls, auth, network/API, MCP activation. |
| `secret_credential_content_blocked` | Active | Secret/credential inspection, use, printing, summarization, validation. |
| `source_loading_blocked` | Active | Source loading, product source inspection, external source inspection, GBrain source inspection. |
| `p4_required_before_product_bound_work` | Expected future blocker | Product-bound work and product activation. |
| `future_EXT_reviews_required_before_external_adoption` | Expected future blocker | External adoption/execution/copying/dependency approval. |
| `future_EXT.GB_HARD_reviews_required_before_selection` | Expected future blocker | GBrain selection/adoption/dependency/provider/MCP/Cadence/substrate. |
| `cognitive_semantic_system_substrate_deferred` | Active | Graph/vector/database/ontology/runtime substrate selection. |
| `generated_output_tracking_blocked` | Active | Generated/local-only output tracking and publication. |
| `source_tracking_git_publication_blocked` | Active | Staging, commit, push, force-add, publication without human gate. |
| `pending_P7.0.A_lead_gateway_alignment` | resolved_by_alignment | Lead gateway classified as `user_gateway` / `manual_control_plane` in the `manual_bridge_layer`. |
| `pending_P7.0.C_lane_taxonomy_alignment` | resolved_by_alignment | Lane taxonomy classified as manual execution projection, not final internal agent taxonomy. |
| `pending_P7.0.D_memory_manifest_alignment` | resolved_by_alignment | MemoryManifest extended toward Context & Memory Fabric metadata. |
| `pending_P7.0.E_harness_boundary_alignment` | Pending peer alignment | Harness and integration boundaries. |
| `pending_P7.0.F_reviewer_pipeline_alignment` | Pending peer alignment | Reviewer pipeline details. |
| `pending_P7.0.G_integrator_commit_protocol_alignment` | Pending peer alignment | Integrator and commit protocol details. |
| `P7.0.H_not_started_expected` | Expected absence | P7 successor/execution work. |

## 30. Created / Not Created Register

| Artifact or action | P7.0.B status |
| --- | --- |
| `0_architecture/governance/agent_platform_roadmap_generation_work_breakdown_contract.md` | Created. |
| P7.0.A, P7.0.C, P7.0.D, P7.0.E, P7.0.F, P7.0.G, P7.0.H, P7.0.R | Not created. |
| P7.1, P8, P4, EXT.* | Not created or started. |
| Runtime implementation | Not created or modified. |
| Agent runtime, task execution, handoff execution, scheduler, orchestration, autonomous loop | Not activated. |
| Review automation, integration automation, dispatch, handoff workflow | Not created. |
| Validation, tests, CI, scripts, builds, package managers | Not run or approved. |
| Security enforcement, scanners, policy engines | Not run, created, or approved. |
| Provider/auth/API/MCP, network, credentials | Not configured, called, inspected, or used. |
| Product source, external source, GBrain source, Graphify source, raw generated output | Not inspected. |
| `9_artifacts/`, Graphify outputs, generated outputs | Not inspected, modified, or tracked. |
| Cognitive Semantic System substrate, graph DB, vector DB, embeddings, ontology runtime, persistence, telemetry, event stream | Not selected, created, or approved. |
| `.gitignore`, `.graphifyignore`, README.md, P6/P5/P4/P3/P2/P1/P0 docs | Not modified by P7.0.B. |
| Source tracking, staging, commit, push, force-add, publication | Not performed or approved. |

## 31. P18.R Roadmap Sequencing Freeze

P18.R records the post-migration roadmap sequence after the accepted P18.8 controlled default-mode cutover. This section updates roadmap sequencing only; it does not start P18.9, P19, P20, P21, runtime automation, provider/auth work, product implementation, source loading, Graphify, Docker, staging, commit or push.

| Field | Value |
| --- | --- |
| roadmap_update_owner | `P18.R` |
| closed_macroproject | `P18 Manual-to-Hermes Workflow Migration` |
| completed_P18_tickets_renumbered | `false` |
| P18_5_title_preserved | `Review and Validation Loop` |
| prohibited_title | `P18.5 - Hermes Personalization` |
| inserted_project | `P18.9 - Pepper Product Personalization` |
| P18_9_ready | `true` |

Accepted sequence after P18.R:

| Order | Phase | Purpose |
| --- | --- | --- |
| 1 | `P18.R - Workflow Migration Closure` | Close P18 after committed P18.8 cutover evidence. |
| 2 | `P18.9 - Pepper Product Personalization` | Transform the current hybrid Hermes/Pepper dashboard into a coherent Pepper product control plane. |
| 3 | `P19 - GBrain Knowledge Integration` | Add durable semantic project memory, cross-session knowledge and provenance-aware retrieval. |
| 4 | `P20 - Paperclip Work Control Plane Integration` | Add durable canonical project/task/work authority and migrate beyond provisional Kanban authority. |
| 5 | `P21 - Governed Multi-Agent Automation` | Add broad autonomous multi-agent coordination and durable delegated planning/execution loops. |

P18.9 is not a reopening of P18 workflow migration. It is product/control-plane personalization for the already migrated Pepper workflow.

## 32. P18.9 Implementation Roadmap Authority

This section is the accepted implementation-roadmap authority for P18.9 ticket generation after the P18.9.0 inventory, IA decision, and acceptance contract. It supersedes any P18.9 advisory decomposition in `2_products/pepper-agent/docs/agent-platform/workflow_migration_closure.md` for generated Ticket Architect targets. It does not generate, approve, project, dispatch, execute, run Docker, run Graphify, stage, commit, or push any ticket.

| Field | Value |
| --- | --- |
| authority_owner | `PEPPER-P18_9-IMPLEMENTATION-ROADMAP-AUTHORITY-01P` |
| authority_status | `accepted_implementation_roadmap` |
| supersedes_for_generation | `workflow_migration_closure.md#Advisory decomposition only, not implementation tickets` |
| macroproject | `P18.9 - Pepper Product Personalization` |
| generation_boundary | `Ticket generation only; human approval remains required before execution.` |

Accepted P18.9 implementation sequence:

| Ticket | Title | Dependencies | Purpose |
| --- | --- | --- | --- |
| `P18.9.0` | `Product Inventory, IA Decision, and Acceptance Contract` | `none` | Inventory Pepper product surfaces, make the first information-architecture decision, and define the acceptance contract for P18.9 personalization. |
| `P18.9.1` | `Pepper Shell, Routing, and Compact Navigation` | `P18.9.0` | Implement the first coherent Pepper control-plane shell and compact workflow-first navigation under `/agent-platform`, without a permanent `Legacy Hermes Tools` product domain. |
| `P18.9.2` | `Projects, Tickets, and Workflow State Workspace` | `P18.9.1` | Consolidate project, ticket, workflow-control, and next-action state into a Pepper-owned workspace. |
| `P18.9.3` | `Approvals and Human Gates Workspace` | `P18.9.2` | Personalize governed approval, review, and human gate surfaces while preserving explicit human authority. |
| `P18.9.4` | `Execution and Recovery Workspace` | `P18.9.3` | Rationalize execution, retry, recovery, and validation visibility without adding worker or dispatch authority. |
| `P18.9.5` | `Repository Evidence and Planning Workspace` | `P18.9.2` | Present bounded repository-context and planning evidence as read-only Pepper product capability. |
| `P18.9.6` | `Lead Agent Chat Personalization` | `P18.9.3` | Align Pepper Lead Agent chat prompts, affordances, and status copy with the governed control-plane workflow. |
| `P18.9.7` | `Legacy Hermes Surface Rationalization` | `P18.9.1` | Classify and consolidate legacy Hermes tool surfaces so they appear as governed capabilities, not as a permanent top-level product domain. |
| `P18.9.8` | `Safe Settings and Product Configuration UX` | `P18.9.1` | Refine safe settings and product configuration presentation while preserving deterministic, credential-free configuration boundaries. |
| `P18.9.9` | `Operational Overview Personalization` | `P18.9.4` | Improve the Pepper operational overview around current status, blockers, and next governed action. |
| `P18.9.10` | `Cross-Surface Empty, Blocked, and Recovery States` | `P18.9.4` | Normalize empty, blocked, failed, retry, and recovery-state UX across Pepper control-plane surfaces. |
| `P18.9.11` | `Product-Wide Personalization Smoke` | `P18.9.2; P18.9.3; P18.9.4; P18.9.5; P18.9.6; P18.9.7; P18.9.8; P18.9.9; P18.9.10` | Validate the personalized Pepper control plane end to end without adding Git, Docker, Graphify, provider, or worker authority. |
| `P18.9.12` | `Pepper Visual Identity and Design System` | `P18.9.1` | Resolve Pepper visual identity and design-system refinements separately from the first shell/navigation ticket. |
| `P18.9.R` | `Personalization Closure` | `P18.9.11; P18.9.12` | Close P18.9 with evidence, residual risks, and next-roadmap handoff while preserving human Git authority. |

Accepted P18.9 implementation ticket contracts:

| Ticket | Field | Value |
| --- | --- | --- |
| `P18.9.1` | `ticket_type` | `implementation` |
| `P18.9.1` | `objective` | Implement the first coherent Pepper control-plane shell, route ownership, protected namespace, and compact workflow-first navigation under `/agent-platform` while preserving existing backend authority boundaries. |
| `P18.9.1` | `context` | P18.9.0 IA decision selects `/agent-platform` as the first coherent Pepper product-control-plane boundary.<br>Existing descriptors already expose Overview, Projects, Approvals, Executions, Settings, and contextual detail routes under `/agent-platform`.<br>Existing shell/navigation seams include `mergeProductNavigation`, `groupShellNavigation`, `filterProtectedPluginManifests`, `isAgentPlatformRoutePath`, and the static product extension registry. |
| `P18.9.1` | `predecessor_evidence` | `pepper-review-prepare-action/P18.9.0.review-prepare.json` records `P18.9.0-IA-001`, the `/agent-platform` boundary, current descriptors, shell namespace protection, and downstream acceptance gates.<br>`pepper-review-human-acceptance-action/P18.9.0.review-acceptance.json` records accepted P18.9.0 closure with no Git, Docker, Graphify, Kanban dispatch, worker execution, or provider execution. |
| `P18.9.1` | `dependency_context` | Roadmap dependency `P18.9.0` must be accepted before P18.9.1 execution; this remains roadmap metadata and must not create a compile-only dependency-plan edge in the single-ticket generation packet.<br>`P18.9.12 - Pepper Visual Identity and Design System` remains separate and must not be pulled into this shell/routing/navigation ticket. |
| `P18.9.1` | `information_architecture` | CONTROL: Overview, Lead Agent.<br>WORK: Projects, Approvals, Executions.<br>AGENTS: Agents.<br>AUTOMATION: Automation, Integrations.<br>RESOURCES: Resources.<br>SYSTEM: Settings. |
| `P18.9.1` | `required_surfaces` | Sidebar groups and ordering for the compact Pepper control plane.<br>Protected `/agent-platform/*` route namespace.<br>Dynamic plugin collision protection for product-owned routes.<br>Inherited Hermes surfaces mapped into Pepper groups without a permanent top-level `Legacy Hermes Tools` product domain.<br>Contextual/detail routes remain contextual and are not promoted into primary navigation. |
| `P18.9.1` | `allowed_paths` | `2_products/pepper-agent/web/src/App.tsx`<br>`2_products/pepper-agent/web/src/agent-platform/extensions.ts`<br>`2_products/pepper-agent/web/src/agent-platform/extensions.test.ts`<br>`2_products/pepper-agent/web/src/agent-platform/shell/**`<br>`2_products/pepper-agent/web/src/agent-platform/runtime-overview/**`<br>`2_products/pepper-agent/web/src/agent-platform/projects-tickets/**`<br>`2_products/pepper-agent/web/src/agent-platform/approval-inbox/**`<br>`2_products/pepper-agent/web/src/agent-platform/execution-inspector/**`<br>`2_products/pepper-agent/web/src/agent-platform/safe-settings/**` |
| `P18.9.1` | `allowed_actions` | Reuse and adapt existing shell, route, navigation, descriptor, and plugin-protection primitives.<br>Add focused frontend tests for route ownership, group ordering, plugin collision protection, detail-route contextual behavior, and visual-design boundary preservation.<br>Inspect bounded P18.9.0 IA and accepted review evidence only as implementation authority. |
| `P18.9.1` | `constraints` | Do not create a second router, sidebar runtime, plugin loader, route registry, or navigation runtime.<br>Preserve `/agent-platform/*` ownership and reject dynamic plugin claims that collide with product-owned routes or namespace patterns.<br>Preserve route compatibility; do not delete or redirect existing built-in routes without explicit accepted authority.<br>Do not move contextual/detail routes into primary navigation.<br>Do not change backend API authority, provider behavior, worker dispatch, Kanban projection, Docker, Graphify, or Git authority.<br>Do not implement Pepper visual identity or design-system refinements reserved for `P18.9.12`. |
| `P18.9.1` | `non_goals` | No permanent top-level `Legacy Hermes Tools` product domain.<br>No backend authority changes.<br>No provider, model, worker, Kanban, Docker, Graphify, or Git mutation authority.<br>No visual identity or design-system implementation beyond preserving existing tokens and shell seams.<br>No broad route deletion or unauthorized route renaming. |
| `P18.9.1` | `risk` | Route compatibility regression if existing Hermes routes are removed or redirected.<br>Namespace regression if dynamic plugins can claim `/agent-platform/*` routes.<br>Product IA regression if contextual detail routes become primary navigation.<br>Scope drift if P18.9.12 visual identity or backend authority changes are pulled forward. |
| `P18.9.1` | `tasks` | Inventory the current App route/nav composition and product extension descriptors before editing.<br>Implement compact Pepper sidebar grouping in the existing shell/navigation flow using the accepted IA group order.<br>Keep `/agent-platform/*` protected against dynamic plugin and extension collisions.<br>Map inherited Hermes surfaces into Pepper groups while avoiding a permanent `Legacy Hermes Tools` top-level domain.<br>Preserve existing detail routes as contextual routes and preserve backend/API authority boundaries.<br>Add focused tests for the route, namespace, grouping, reuse, and P18.9.12 boundary contracts. |
| `P18.9.1` | `acceptance_criteria` | TicketSpec type is `implementation`, not `architecture` or `documentation`.<br>The implementation reuses existing shell/navigation/extension primitives rather than adding a second router, sidebar, plugin loader, route registry, or navigation runtime.<br>Sidebar groups and ordering implement CONTROL, WORK, AGENTS, AUTOMATION, RESOURCES, and SYSTEM with Overview, Lead Agent, Projects, Approvals, Executions, Agents, Automation, Integrations, Resources, and Settings mapped as specified.<br>`/agent-platform/*` remains protected and dynamic plugin collisions are blocked.<br>Existing routes remain compatible unless a route deletion or redirect has separate accepted authority.<br>No permanent top-level `Legacy Hermes Tools` product domain is introduced.<br>Contextual/detail routes remain contextual and out of primary navigation.<br>No backend API, provider, worker, Kanban, Docker, Graphify, or Git authority changes are introduced.<br>`P18.9.12 - Pepper Visual Identity and Design System` remains out of scope. |
| `P18.9.1` | `expected_artifacts` | Frontend shell/navigation and descriptor changes inside the allowed paths.<br>Focused frontend tests proving group order, namespace protection, plugin collision blocking, route compatibility, detail-route contextual behavior, and P18.9.12 boundary preservation.<br>Final report with files inspected, files modified, tests run, preserved boundaries, and rollback posture. |
| `P18.9.1` | `validation_steps` | V1: Human review confirms the generated TicketSpec and WorkPacket are implementation-oriented and carry the P18.9.1 shell/routing/navigation contract => The reviewer can identify implementation objective, scope, IA groups, route/namespace contracts, non-goals, risks, expected artifacts, acceptance criteria, and no execution authority.<br>V2: Focused frontend tests validate route compatibility, plugin collision protection, navigation grouping, contextual detail routes, and P18.9.12 boundary => Test results show the existing shell/navigation primitives satisfy the accepted contract without a second router/sidebar/plugin loader. |
| `P18.9.1` | `completion_verdict` | `p18_9_1_shell_routing_navigation_implementation_ready` |
| `P18.9.1` | `recommended_commit_message` | `P18.9.1 Implement Pepper shell routing and compact navigation` |

P18.9.1 is therefore `Pepper Shell, Routing, and Compact Navigation`. `Pepper Design System` is not the P18.9.1 implementation ticket; visual identity and design-system work resolves as P18.9.12 unless a later accepted authority supersedes this sequence.

## 33. Invariants And Final Verdict

| ID | Invariant |
| --- | --- |
| P70B-001 | P7.0.B is documentation-only roadmap generation and work-breakdown design. |
| P70B-002 | Roadmap generation is not roadmap execution. |
| P70B-003 | Work packet generation is not task execution. |
| P70B-004 | Parallelization groups are not runtime concurrency, workers, queues, or orchestration. |
| P70B-005 | Review objects are not automated review or approval. |
| P70B-006 | Integration summaries are not merge automation. |
| P70B-007 | Commit advice is not Git mutation and must never recommend `git add .`. |
| P70B-008 | User remains final execution authority and final Git authority. |
| P70B-009 | AGENT PLATFORM remains AL-1 metadata skeleton; AL-1.5 is planning vocabulary only. |
| P70B-010 | `activation_level_transition: not_approved` remains active. |
| P70B-011 | `runtime_activation: not_approved` remains active. |
| P70B-012 | Product-bound work remains blocked pending P4. |
| P70B-013 | EXT.* remains required before external adoption. |
| P70B-014 | GBrain remains candidate-only and future-blocked by EXT.GB-HARD. |
| P70B-015 | Graphify remains supporting generated evidence only. |
| P70B-016 | Cognitive Semantic System substrate remains deferred. |
| P70B-017 | No source loading, product source inspection, external source inspection, GBrain source inspection, raw generated output inspection, credential inspection, provider/auth use, API/network/MCP call, or tool execution is approved. |
| P70B-018 | P7.0.B stops before adjacent P7, P7.1, P8, P4, EXT.*, runtime, product, external, substrate, generated-output tracking, source tracking, publication, and Git work. |

Final verdict: P7.0.B creates the canonical manual Roadmap Generation / Work Breakdown Contract for AGENT PLATFORM / Siamese. It defines `UserObjective`, `Roadmap`, `RoadmapPhase`, `Workstream`, `WorkPacket`, `Dependency`, `ParallelizationGroup`, `SequencingRule`, `Blocker`, `CompletionCriterion`, `TicketKind`, review objects, integration objects, and commit-advice objects. It preserves P6.7 accepted planning readiness while keeping AGENT PLATFORM at AL-1 metadata skeleton. It does not activate runtime, execute agents/tasks/handoffs, automate review or integration, inspect source, inspect product/external/GBrain/Graphify/raw generated outputs, use providers/auth/API/MCP, run validation/tests/scripts/builds, select substrate, track generated outputs, expand source tracking, publish, stage, commit, push, or start adjacent tickets.
