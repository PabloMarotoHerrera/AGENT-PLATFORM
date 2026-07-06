# Core Workflow Schema Candidates

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Core Workflow Schema Candidates |
| Ticket | P8.3 |
| Status | Accepted core workflow schema candidates |
| Date | 2026-07-06 |
| Scope | Documentation-only schema candidate design for AGENT PLATFORM / Siamese MVP-0 core workflow objects. |
| Authority | Core Workflow Schema Candidates only, not schema implementation, not code generation, not JSON schema generation, not package creation, not runtime implementation, not MVP skeleton implementation, not CLI/TUI/web UI implementation, not adapter implementation, not OpenCode execution, not Graphify rerun/adoption, not GBrain runtime, not GStack runtime, not Hermes runtime, not Cadence activation, not provider/auth/API/MCP activation, not credential use, not API calls, not MCP activation, not tool execution, not agent execution, not task execution, not handoff execution, not source loading, not source inspection, not product source inspection, not external source inspection, not validation execution, not security enforcement activation, not persistence/database/event stream, not telemetry, not vector DB implementation, not embeddings generation, not graph DB implementation, not generated output tracking approval, not source tracking expansion approval, not publication approval, not Git mutation approval, and not Cognitive Semantic System substrate selection. |
| Related documents | P8.0 Platform MVP Scope / External Integration Boundary; P8.1 External Source Inventory / Classification, if present; P8.2 MVP Interaction Surface Architecture, if present; P8.4 Local Workspace / State Model, if present; P8.5 Security / Activation Gate Model, if present; P7.R Manual Agentic Workflow Planning Closure; P7.0.A Manual Lead Agent / User Gateway Contract; P7.0.B Roadmap Generation / Work Breakdown Contract; P7.0.C Parallel Agent Lane / Work Packet Taxonomy; P7.0.D Manual Context / Memory Manifest Strategy; P7.0.E Manual Harness Strategy / OpenCode-Hermes Boundary; P7.0.F Reviewer Mesh / Immune Safeguards Contract; P7.0.G Integrator / Commit Advisory Protocol; P7.0.H First Manual Agentic Workflow Pilot Playbook; P6.7 Operational Readiness Audit; P5.R Minimal Active Agent Platform Audit; P3.BR Activation Decision Reconciliation Closure; P2.KR Knowledge / Retrieval Architecture Reconciliation Closure; P2.R Cross-Lane Integration Reconciliation Closure; P2.1 Shared Metadata Vocabulary Alignment; P2.2 Cross-Lane Evidence Reference Contract; P2.3 Audit / Retention / Rollback Baseline; P1.1 Context Runtime Contract Hardening; P1.2 Provider Adapter Metadata Contract Hardening; P1.3 Tool Execution Boundary Contract Hardening; P1.4 Agent Runtime Boundary Contract Hardening; P1.5 Cognitive Semantic System Prototype Hardening; P0.1 Activation Gate Enforcement Map; P0.2 Validation Execution Gate Design; P0.3 Security Enforcement Hardening Plan; Activation Gate Charter; Tool / Shell / Network / MCP Execution Policy; Local-Only / Secrets / Credentials Policy; Cognitive Semantic System ADR / audit; README.md; `.gitignore`; `.graphifyignore`. |
| Output | core workflow schema candidates |

Schema is not runtime.

Schema candidate is not implementation.

Schema reference is not permission.

SourceRef is not source loading.

FileRef is not file inspection.

EvidenceRef is not authority.

ReviewVerdictPackage is not approval.

IntegrationSummary is not automatic merge.

CommitCandidate is not Git mutation.

CommitCommandBlock is advisory only.

The user performs Git manually.

Never recommend git add .

## 2. Purpose

P8 turns the P7 manual workflow into a local Platform MVP / Interaction Layer.

P8.3 extracts the stable workflow objects from P7 and defines them as schema candidates.

P8.3 enables later MVP-0 architecture synthesis and implementation planning.

P8.3 defines the data contracts needed for:

```text
user objective capture
work packet generation
HarnessInputPackage generation
manual external harness output intake
HarnessOutputPackage structuring
review checklist flow
review verdict capture
integration summary capture
drift register capture
accepted/rejected output registers
CommitCandidate rendering
CommitCommandBlock rendering
```

P8.3 does not implement the schema package.

P8.3 does not implement the interaction surface.

P8.3 does not implement local state.

P8.3 does not implement adapters.

P8.3 does not execute OpenCode.

P8.3 does not activate runtime.

P8.3 does not mutate Git.

## 3. Current Posture

| Area | P8.3 posture |
| --- | --- |
| AGENT PLATFORM | AGENT PLATFORM remains AL-1 metadata skeleton unless a future explicit gate changes it. |
| P8 | P8 is Platform MVP / Interaction Layer. |
| P8.3 | P8.3 is architecture/design only. |
| Schema | Schema is not runtime. |
| Schema candidate | Schema candidate is not implementation. |
| P7 workflow | P7 workflow remains manual. |
| MVP-0 | P8 MVP-0 remains manual interactive assistant, not autonomous runtime. |
| OpenCode | OpenCode remains H0 user-operated harness unless later gates approve otherwise. |
| Graphify | Graphify remains read-only evidence candidate, not authority. |
| GBrain | GBrain remains memory architecture candidate, not runtime. |
| GStack | GStack remains GBrain-compatible skill stack candidate, not adopted. |
| Hermes | Hermes remains interface/runtime/orchestration candidate, not activated. |
| Provider/auth/API/MCP | No provider/auth/API/MCP activation is approved. |
| Tools | No tool execution is approved. |
| Agents | No agent execution is approved. |
| Product/Siamese | No product/Siamese source inspection is approved. |
| Git | No Git mutation by agent is approved. The user remains final Git authority. |

## 4. Inputs Reviewed

Inputs were consumed as posture and metadata only. No source content, product/Siamese source, external source content, GBrain/GStack/Hermes source, raw Graphify output, secrets, credentials, `.env`, provider config, token store, browser auth, local credential store, API keys, generated outputs, or `3_platform` contents were inspected.

| input | status | role in P8.3 | limitations |
| --- | --- | --- | --- |
| `0_architecture/governance/agent_platform_core_workflow_schema_candidates.md` | Absent before this ticket | Target document. | Created only by P8.3. |
| `0_architecture/governance/agent_platform_p8_platform_mvp_scope_external_integration_boundary.md` | Present by path check | P8.0 required MVP scope boundary. | Consumed as boundary input; not modified. |
| `0_architecture/governance/agent_platform_external_source_inventory_graphify_gbrain_gstack_hermes_opencode.md` | Present by path check | P8.1 external candidate inventory alignment. | Consumed as present sibling posture; not modified. |
| `0_architecture/governance/agent_platform_mvp_interaction_surface_architecture.md` | Present by path check | P8.2 interaction surface alignment. | Consumed as present sibling posture; not modified. |
| `0_architecture/governance/agent_platform_local_workspace_state_model.md` | Present by path check | P8.4 local workspace state alignment. | Consumed as present sibling posture; not modified. |
| `0_architecture/governance/agent_platform_p8_security_activation_gate_model.md` | Present by path check | P8.5 security / activation gate alignment. | Consumed as present sibling posture; not modified. |
| `0_architecture/governance/agent_platform_manual_agentic_workflow_planning_closure.md` | Present by path check | P7.R manual workflow closure source. | Consumed as workflow prerequisite; not modified. |
| `0_architecture/governance/agent_platform_agent_native_organization_research_carry_forward.md` | Present by path check | Agent-native metadata source. | Not runtime topology activation. |
| `0_architecture/governance/agent_platform_manual_lead_agent_user_gateway_contract.md` | Present by path check | UserObjective and user gateway source. | Not modified. |
| `0_architecture/governance/agent_platform_roadmap_generation_work_breakdown_contract.md` | Present by path check | WorkPacket and roadmap/work breakdown source. | Not modified. |
| `0_architecture/governance/agent_platform_parallel_agent_lane_work_packet_taxonomy.md` | Present by path check | Manual lane, manual execution projection, and lane output source. | Not runtime taxonomy. |
| `0_architecture/governance/agent_platform_manual_context_memory_manifest_strategy.md` | Present by path check | Context, memory, evidence, and Context & Memory Fabric source. | Metadata only; no persistence. |
| `0_architecture/governance/agent_platform_manual_harness_opencode_hermes_boundary_strategy.md` | Present by path check | Harness input/output and H0/H1 boundary source. | No harness execution. |
| `0_architecture/governance/agent_platform_reviewer_mesh_immune_safeguards_contract.md` | Present by path check | Corrected P7.0.F reviewer mesh / immune safeguards source. | Reviewer mesh is review metadata only, not automatic reviewer assignment. |
| `0_architecture/governance/agent_platform_manual_integrator_commit_advisory_protocol.md` | Present by path check | IntegrationSummary, registers, CommitCandidate, and CommitCommandBlock source. | Commit advice only; no Git mutation. |
| `0_architecture/governance/agent_platform_first_manual_agentic_workflow_pilot_playbook.md` | Present by path check | Pilot workflow source for repeated manual flow. | Pilot does not imply runtime. |
| `0_architecture/governance/agent_platform_operational_readiness_audit.md` | Required governance input, not rechecked in corrected command set | P6.7 operational planning boundary. | Metadata input only. |
| `0_architecture/governance/agent_platform_minimal_active_agent_platform_audit.md` | Required governance input, not rechecked in corrected command set | P5.R AL-1 skeleton posture. | No skeleton activation. |
| `0_architecture/governance/agent_platform_activation_decision_reconciliation_closure.md` | Required governance input, not rechecked in corrected command set | P3.BR activation decision boundary. | Activation remains gated. |
| `0_architecture/governance/agent_platform_shared_metadata_vocabulary_alignment.md` | Required governance input, not rechecked in corrected command set | P2.1 canonical vocabulary. | No runtime schema. |
| `0_architecture/governance/agent_platform_cross_lane_evidence_reference_contract.md` | Required governance input, not rechecked in corrected command set | P2.2 EvidenceRef semantics. | Evidence supports; it does not decide. |
| `0_architecture/governance/agent_platform_audit_retention_rollback_baseline.md` | Required governance input, not rechecked in corrected command set | P2.3 retention, rollback, and incident posture. | No persistence or rollback automation. |
| `README.md` | Present by path check | Repository orientation. | No runtime effect. |
| `.gitignore` | Present by path check | Ignore hygiene posture. | Not modified. |
| `.graphifyignore` | Present by path check | Graphify boundary posture. | Not modified; not permission to run Graphify. |
| `external/sources` | Absent by path check | External root candidate posture. | Contents not inspected. |
| `external/sources/gbrain-master` | Absent by path check | GBrain candidate path posture. | Contents not inspected. |
| `external/sources/gstack` | Absent by path check | GStack candidate path posture. | Contents not inspected. |
| `external/sources/gstack-master` | Absent by path check | GStack candidate path posture. | Contents not inspected. |
| `external/sources/gstack-main` | Absent by path check | GStack candidate path posture. | If present later: present_path_not_inspected, external_source_candidate, gbrain_compatibility_candidate, skill_stack_candidate, not_adopted, not_executed, not_runtime. |
| `external/sources/hermes` | Absent by path check | Hermes candidate path posture. | Contents not inspected. |
| `external/sources/hermes-master` | Absent by path check | Hermes candidate path posture. | Contents not inspected. |
| `3_platform` | Present by path check | Platform path posture only. | Contents not inspected or modified. |
| `3_platform/_governed_skeleton` | Present by path check | Governed skeleton path posture only. | Contents not inspected or modified. |
| `9_artifacts` | Present by path check | Generated/local-only path posture only. | Contents not inspected or modified. |
| `graphify-out` | Absent by path check | Generated output path posture only. | Contents not inspected. |

## 5. Dependency Posture

P8.3 consumes P8.0 as the MVP scope boundary.

P8.3 consumes P7.R as the manual workflow closure.

P8.3 consumes P7.0.A/B/C/D/E/F/G/H as the manual workflow object source.

P8.3 consumes P7.0.F as Reviewer Mesh / Immune Safeguards Contract. P8.3 does not require, create, or restore the legacy reviewer approval pipeline path.

P8.3 consumes P2.1 vocabulary to preserve canonical names.

P8.3 consumes P2.2 EvidenceRef relationships.

P8.3 consumes P2.3 audit / retention / rollback posture.

P8.3 consumes P3-B decision boundaries.

P8.3 consumes P6 operational planning boundaries.

P8.3 may consume P8.1 external inventory, P8.2 interaction surface, P8.4 local state, and P8.5 security gates because they are present by path check.

P8.3 must not create or supersede sibling P8 documents.

P8.3 may record drift candidates for P8.10 synthesis.

## 6. Schema Candidate Decision Model

Decision questions:

```text
1. Which P7 workflow object does this schema candidate represent?
2. Is it user input, work planning, harness input, harness output, review, integration, or commit advice?
3. Does the schema candidate require context, evidence, validation, security, retention, rollback, incident, or human approval refs?
4. Does it include file paths?
5. Does it include source refs?
6. Does it include external harness output?
7. Does it include generated output?
8. Does it include product-related material?
9. Does it include local-only material?
10. Does it require exact-path Git safety?
11. What is blocked by default?
12. What future implementation level may consume it?
```

Transformation rules:

```text
If schema fields imply execution, convert them into blocked metadata fields.
If schema fields imply source loading, convert them into SourceRef metadata fields with blockers.
If schema fields imply Git mutation, convert them into advisory command fields with human execution required.
If schema fields imply adapter execution, mark them future-gated.
```

## 7. Schema Candidate Registry

| schema candidate | workflow stage | source P7 object | MVP-0 use | future implementation posture | blocked interpretation |
| --- | --- | --- | --- | --- | --- |
| UserObjective | user objective capture | UserObjective / Lead Agent gateway | Capture user intent and scope. | Candidate for future local input model. | Broad approval or execution permission. |
| WorkPacket | work planning | WorkPacket / Roadmap / Lane taxonomy | Represent manual work unit. | Candidate for future work packet view. | Automatic dispatch. |
| HarnessInputPackage | harness input | LaneInputPackage / harness boundary | Prepare manual copy/paste packet. | Candidate for future H0/H1 packet rendering. | Harness execution or adapter activation. |
| HarnessOutputPackage | harness output | LaneOutputPackage / pilot output | Structure user-pasted output. | Candidate for future output intake model. | Trusted execution proof or acceptance. |
| ReviewInputPackage | review | ReviewRoutingRequest / reviewer mesh | Prepare manual review checklist input. | Candidate for future review checklist UI. | Automatic reviewer assignment. |
| ReviewVerdictPackage | review verdict | ReviewerVerdictPackage / reviewer mesh | Capture review metadata. | Candidate for future review result model. | Approval, Git approval, or runtime approval. |
| IntegrationSummary | integration | IntegrationSummary / integrator protocol | Capture manual synthesis. | Candidate for future integration view. | Automatic merge. |
| DriftRegister | integration / drift | DriftRegister | Track drift and resolution posture. | Candidate for future drift panel. | Silent drift waiver. |
| AcceptedOutputRegister | integration / acceptance | AcceptedOutputRegister | Track accepted output metadata. | Candidate for future accepted register. | Git approval. |
| RejectedOutputRegister | integration / rejection | RejectedOutputRegister | Exclude rejected outputs and paths. | Candidate for future rejected register. | Silent integration or staging. |
| CommitCandidate | commit advice | CommitCandidate | Render exact-path commit proposal. | Candidate for future commit advice model. | Git mutation. |
| CommitCommandBlock | commit advice | CommitCommandBlock | Render advice-only Git commands. | Candidate for future command block rendering. | Automatic Git execution. |

## 8. Shared Field Conventions

Common fields:

```text
*_id
*_ref
*_refs
status
scope
objective
summary
limitations
blockers
evidence_refs
validation_refs
security_refs
retention_refs
rollback_refs
incident_refs
human_approval_required
created_files
modified_files
excluded_files
exact_paths
source_refs
context_refs
review_required
stop_rules
```

Path conventions:

```text
path fields are inert strings
path presence is not content inspection permission
exact_paths must be explicit
wildcards are blocked by default
generated output paths require tracking posture
product paths require product boundary posture
local-only paths require retention/security posture
```

## 9. UserObjective Schema Candidate

Required fields:

```text
user_objective_id
objective_text
objective_type
requested_outcome
scope
non_goals
constraints
priority
expected_artifacts
manual_bridge_layer_refs
agent_native_refs
context_refs
evidence_refs
validation_refs
security_refs
retention_refs
human_decision_points
stop_rules
limitations
```

UserObjective is user intent metadata, not broad approval.

UserObjective does not authorize source loading, provider/auth, tool execution, agent execution, product access, live connectors, publication, source tracking, generated output tracking, or Git mutation.

## 10. WorkPacket Schema Candidate

Required fields:

```text
work_packet_id
ticket_id
title
objective
work_packet_type
lane_assignment_refs
agent_native_topology_refs
task_graph_refs
blackboard_refs
capability_cell_refs
reviewer_mesh_refs
routing_decision_refs
scope_allowed
scope_blocked
target_files
mandatory_inputs
optional_inputs
expected_outputs
dependencies
parallelization_group
sequencing_rule
review_requirements
integration_requirements
security_requirements
validation_requirements
context_requirements
harness_requirements
stop_rules
completion_criteria
limitations
```

WorkPacket is manual execution projection, not automatic dispatch.

WorkPacket does not activate agents, tools, providers, harnesses, or runtime.

## 11. HarnessInputPackage Schema Candidate

Required fields:

```text
harness_input_package_id
target_harness
harness_mode
work_packet_ref
objective
instructions
allowed_scope
blocked_scope
mandatory_context_refs
evidence_refs
validation_refs
security_refs
source_refs
file_refs
expected_output_format
stop_rules
non_goals
human_operator_notes
limitations
```

Allowed harness modes:

```text
H0_user_operated_manual
H1_metadata_adapter_design
```

Blocked harness modes:

```text
H2_controlled_execution_adapter
H3_autonomous_orchestration_adapter
```

HarnessInputPackage may be copied manually by the user into OpenCode or another external harness.

HarnessInputPackage does not execute the harness.

HarnessInputPackage does not activate OpenCode, Hermes, MCP, providers, tools, or agents.

## 12. HarnessOutputPackage Schema Candidate

Required fields:

```text
harness_output_package_id
source_harness
harness_mode
work_packet_ref
raw_output_provided_by_user
structured_summary
created_files
modified_files
not_created_register
commands_claimed_run
tests_claimed_run
decisions_made
limitations
blockers
drift_observed
evidence_refs
validation_refs
security_refs
retention_refs
rollback_refs
incident_refs
review_required
human_operator_notes
```

HarnessOutputPackage records user-provided external harness output.

It does not verify execution automatically.

It does not trust claims by default.

It does not accept outputs by default.

It does not commit anything.

If commands/tests are claimed, they are evidence claims, not validation execution by AGENT PLATFORM.

## 13. ReviewInputPackage Schema Candidate

Required fields:

```text
review_input_package_id
review_target_ref
work_packet_ref
harness_output_package_refs
review_scope
review_type
reviewer_role
review_checklist_refs
evidence_refs
validation_refs
security_refs
source_classification_refs
retention_refs
stop_rules
expected_verdicts
limitations
```

Review types:

```text
architecture_review
security_review
validation_readiness_review
consistency_review
memory_context_review
external_boundary_review
product_boundary_review
git_safety_review
```

ReviewInputPackage is not automatic reviewer assignment.

ReviewInputPackage is not approval.

## 14. ReviewVerdictPackage Schema Candidate

Required fields:

```text
review_verdict_package_id
review_input_package_ref
reviewer_role
review_verdict
accepted_items
accepted_with_limitations_items
needs_rework_items
blocked_items
out_of_scope_items
findings
blockers
limitations
evidence_refs
validation_refs
security_refs
retention_refs
rollback_refs
incident_refs
human_escalation_required
recommended_next_action
```

Allowed verdicts:

```text
accepted
accepted_with_limitations
needs_rework
blocked
out_of_scope
```

ReviewVerdictPackage is review metadata.

Reviewer approval is not Git approval.

Reviewer approval is not runtime approval.

Reviewer approval is not human commit authorization.

ReviewVerdictPackage consumes P7.0.F reviewer mesh / immune safeguards metadata only.

Reviewer mesh is not automatic reviewer assignment.

## 15. IntegrationSummary Schema Candidate

Required fields:

```text
integration_summary_id
integrated_work_packet_refs
harness_output_package_refs
review_verdict_package_refs
accepted_output_register_ref
rejected_output_register_ref
drift_register_ref
agent_native_refs
context_refs
evidence_refs
validation_refs
security_refs
retention_refs
rollback_refs
incident_refs
summary
decisions
limitations
blockers
unresolved_drift
recommended_next_ticket
human_decision_required
```

IntegrationSummary is manual synthesis.

IntegrationSummary is not automatic merge.

IntegrationSummary does not approve Git mutation.

## 16. DriftRegister Schema Candidate

Required fields:

```text
drift_register_id
drift_items
affected_work_packets
affected_schema_candidates
affected_files
affected_contracts
affected_agent_native_refs
drift_type
severity
resolution_status
resolution_summary
owner_or_route
review_required
integrator_decision
human_decision_required
limitations
```

Required drift types:

```text
scope_drift
schema_drift
contract_drift
naming_drift
boundary_drift
security_drift
validation_drift
evidence_drift
retention_drift
rollback_drift
agent_native_topology_drift
manual_projection_drift
commit_scope_drift
external_harness_claim_drift
```

## 17. AcceptedOutputRegister Schema Candidate

Required fields:

```text
accepted_output_register_id
accepted_work_packet_refs
accepted_harness_output_refs
accepted_review_verdict_refs
accepted_file_paths
accepted_decisions
accepted_limitations
accepted_integrator_rationale
accepted_agent_native_refs
required_follow_up
commit_candidate_ref
human_decision_required
```

AcceptedOutputRegister is integration metadata.

It is not Git approval.

Accepted output still requires user commit decision.

## 18. RejectedOutputRegister Schema Candidate

Required fields:

```text
rejected_output_register_id
rejected_work_packet_refs
rejected_harness_output_refs
rejected_file_paths
rejection_reasons
blocking_verdict_refs
out_of_scope_items
rework_required
future_ticket_refs
security_or_boundary_reasons
human_decision_required
limitations
```

RejectedOutputRegister prevents accidental inclusion in commit candidates.

Rejected paths must not be staged.

Rejected paths must not be silently integrated.

## 19. CommitCandidate Schema Candidate

Required fields:

```text
commit_candidate_id
commit_scope
included_file_paths
excluded_file_paths
accepted_output_register_ref
rejected_output_register_ref
drift_register_ref
review_verdict_refs
integration_summary_ref
commit_message_candidate
git_add_paths
git_commit_command
git_push_command
rollback_note_ref
human_approval_required
limitations
```

CommitCandidate is advisory only.

CommitCandidate is not Git mutation.

CommitCandidate does not stage files.

CommitCandidate does not commit.

CommitCandidate does not push.

CommitCandidate must never use git add .

## 20. CommitCommandBlock Schema Candidate

Required fields:

```text
commit_command_block_id
status_command
git_add_commands
git_commit_command
git_push_command
excluded_paths
forbidden_commands
human_execution_required
limitations
```

Required command pattern:

```powershell
git status --short

git add <exact_path_1>
git add <exact_path_2>

git commit -m "<exact commit message>"

git push origin main
```

Forbidden command:

```powershell
git add .
```

CommitCommandBlock is advice only.

The user executes commands manually.

## 21. Supporting Reference Schema Candidates

| reference candidate | purpose | required posture | blocked interpretation |
| --- | --- | --- | --- |
| SessionRef | Reference to a local/manual interaction session. | Metadata only. | Persistent runtime session. |
| ContextRef | Reference to context pack or context item. | Metadata lineage. | Source loading permission. |
| EvidenceRefBinding | Binds EvidenceRef to workflow object. | Evidence supports. | Evidence as authority. |
| ValidationRefBinding | Binds validation posture to workflow object. | Validation metadata. | Validation execution. |
| SecurityRefBinding | Binds security posture to workflow object. | Security constraint metadata. | Security activation. |
| RetentionRefBinding | Binds retention posture. | Retention metadata. | Persistence implementation. |
| RollbackRefBinding | Binds rollback posture. | Rollback metadata. | Rollback automation. |
| IncidentRefBinding | Binds incident posture. | Incident metadata. | Monitoring or incident automation. |
| HumanApprovalRef | Records explicit human decision requirement. | Human approval metadata. | Silent approval. |
| SourceRef | Metadata source reference. | SourceRef is metadata only. | Source loading. |
| FileRef | Metadata file reference. | FileRef is not file inspection. | File read/write permission. |
| PathRef | Inert path string with posture. | Path presence is not content inspection permission. | Wildcard or broad staging. |
| ChecklistRef | Metadata checklist reference. | Review checklist lineage. | Automatic review assignment. |
| LimitationRef | Metadata limitation reference. | Preserves limitation. | Waiver by omission. |
| BlockerRef | Metadata blocker reference. | Preserves blocker. | Automatic resolution. |
| ExternalCandidateRef | Metadata external candidate classification. | Path/class metadata only. | Adoption, execution, or source inspection. |

## 22. Schema Relationship Model

Relationships:

```text
UserObjective -> WorkPacket
WorkPacket -> HarnessInputPackage
HarnessInputPackage -> HarnessOutputPackage
HarnessOutputPackage -> ReviewInputPackage
ReviewInputPackage -> ReviewVerdictPackage
ReviewVerdictPackage -> IntegrationSummary
IntegrationSummary -> DriftRegister
IntegrationSummary -> AcceptedOutputRegister
IntegrationSummary -> RejectedOutputRegister
AcceptedOutputRegister -> CommitCandidate
RejectedOutputRegister -> CommitCandidate exclusion rules
CommitCandidate -> CommitCommandBlock
```

Cross-cutting refs:

```text
ContextRef
EvidenceRefBinding
ValidationRefBinding
SecurityRefBinding
RetentionRefBinding
RollbackRefBinding
IncidentRefBinding
HumanApprovalRef
ExternalCandidateRef
```

References preserve lineage.

References do not grant permission.

References do not execute behavior.

## 23. Boundary Model

### Runtime Boundary

Schemas do not activate runtime.

Schemas do not dispatch tasks.

Schemas do not execute agents.

Schemas do not execute tools.

Schemas do not call providers.

Schemas do not execute OpenCode.

### Harness Boundary

HarnessInputPackage is manual copy/paste input.

HarnessOutputPackage is user-pasted output capture.

No internal OpenCode adapter execution is approved.

No Hermes runtime is approved.

No MCP activation is approved.

### Source Boundary

SourceRef is metadata only.

Source classification is not source loading permission.

Path presence is not content inspection permission.

Product/Siamese source remains blocked.

External source content remains blocked unless future exact gate approves.

### Git Boundary

CommitCandidate is not Git mutation.

CommitCommandBlock is advisory.

The agent never stages, commits, pushes, force-adds, cleans, resets, restores, or publishes.

The user performs Git manually.

`git add .` is forbidden.

### External Candidate Boundary

Graphify remains read-only evidence candidate, not authority.

GBrain remains memory architecture candidate, not runtime.

GStack remains GBrain-compatible skill stack candidate, not adopted.

Hermes remains interface/runtime candidate, not activated.

OpenCode remains H0 user-operated harness.

Schema candidates must not imply external runtime adoption.

### Product / Siamese Boundary

Siamese is product vision, not product activation.

P8.3 does not inspect product/Siamese source.

Schema candidates may carry product boundary posture only.

Schema candidates must not imply product source permission, product execution, or product activation.

### Cognitive Semantic System Boundary

Cognitive Semantic System remains the accepted name.

Cognitive Semantic System substrate remains deferred.

Schema candidates must not select graph DB, vector DB, embeddings, ontology runtime, persistence DB, or substrate.

## 24. Interfaces With P8.1 / P8.2 / P8.4 / P8.5

| sibling | path status | P8.3 handling |
| --- | --- | --- |
| P8.1 External Source Inventory / Classification | Present by path check | Consumed as present external inventory alignment. |
| P8.2 MVP Interaction Surface Architecture | Present by path check | Consumed as present interaction surface alignment. |
| P8.4 Local Workspace / State Model | Present by path check | Consumed as present local workspace state alignment. |
| P8.5 Security / Activation Gate Model | Present by path check | Consumed as present security / activation gate alignment. |

P8.3 does not claim unresolved alignment for present P8.1, P8.2, P8.4, or P8.5 sibling files.

## 25. Interfaces With P7 Manual Workflow

P8.3 preserves P7 manual bridge layer.

P8.3 preserves P7 agent-native references as metadata only.

P8.3 preserves manual execution projection.

P8.3 preserves manual harness operation.

P8.3 preserves reviewer/integrator/human Git authority.

P8.3 consumes P7.0.F as reviewer mesh / immune safeguards metadata only.

P8.3 does not convert P7 workflow into autonomous orchestration.

## 26. Evidence / Validation / Security Interfaces

### Evidence Interface

Evidence supports; it does not decide.

Schema candidates may include EvidenceRef bindings.

EvidenceRef bindings do not approve workflow outputs.

EvidenceRef bindings do not approve runtime behavior.

### Validation Interface

Validation evaluates; governance decides.

Schema candidates may include ValidationRef bindings.

ValidationRef bindings do not execute validation.

P8.3 does not run validation.

### Security Interface

Security constrains; it does not activate.

Schema candidates may include SecurityRef bindings.

SecurityRef bindings do not approve source loading, provider/auth, tool execution, agent execution, external adapter execution, product source access, publication, source tracking, or generated output tracking.

## 27. Retention / Rollback / Incident Posture

Schema candidates must preserve limitations and blockers.

Schema candidates should include retention, rollback, and incident refs when outputs, local state, generated artifacts, or commit candidates are involved.

P8.3 does not implement logging.

P8.3 does not implement persistence.

P8.3 does not implement rollback automation.

P8.3 does not implement incident automation.

## 28. Human Approval Requirements

Human user remains final authority for:

```text
submitting objectives
choosing generated work packets
copying HarnessInputPackage into external harnesses
pasting HarnessOutputPackage back into AGENT PLATFORM
accepting review verdicts
accepting integration summaries
choosing whether to commit
executing git add
executing git commit
executing git push
starting any future activation gate
```

Schema candidates must preserve human approval fields where decisions can affect files, Git, scope, external harnesses, source surfaces, or future implementation.

## 29. Stop Rules

STOP if any of the following occur:

```text
schema implementation attempted
JSON schema generation attempted
runtime activation attempted
OpenCode execution attempted
Hermes runtime requested
GBrain runtime requested
GStack runtime requested
Graphify rerun/adoption requested
provider/auth/API/MCP activation requested
tool execution requested
agent execution requested
source loading attempted
source inspection attempted
product source inspection attempted
external source content inspection attempted
secret or credential encountered
.env inspection requested
validation execution requested
security enforcement activation requested
persistence/vector/graph DB requested
generated output tracking requested
source tracking expansion requested
publication requested
Git mutation requested
git add . proposed
Cognitive Semantic System substrate selection requested
scope drift detected
mandatory P8.0 input missing
```

## 30. Schema Candidate Drift Register

| drift_id | source_area | observed_issue | expected_canonical_posture | status | impact | resolution_route |
| --- | --- | --- | --- | --- | --- | --- |
| P8.3-DRIFT-P8.1 | P8.1 | P8.1 external inventory present and consumed by posture. | Present sibling should not emit pending alignment. | resolved | External candidate alignment available for later synthesis. | Carry to P8.10 synthesis. |
| P8.3-DRIFT-P8.2 | P8.2 | P8.2 interaction surface present and consumed by posture. | Present sibling should not emit pending alignment. | resolved | Interaction surface alignment available for later synthesis. | Carry to P8.10 synthesis. |
| P8.3-DRIFT-P8.4 | P8.4 | P8.4 local workspace state present and consumed by posture. | Present sibling should not emit pending alignment. | resolved | Local state alignment available for later synthesis. | Carry to P8.10 synthesis. |
| P8.3-DRIFT-P8.5 | P8.5 | P8.5 security gate model present and consumed by posture. | Present sibling should not emit pending alignment. | resolved | Security gate alignment available for later synthesis. | Carry to P8.10 synthesis. |
| P8.3-DRIFT-LEGACY-P7F | P7.0.F | Legacy reviewer approval pipeline path is absent; accepted P7.0.F is reviewer mesh / immune safeguards contract. | Use corrected P7.0.F reviewer mesh path and do not require legacy path. | resolved_by_corrected_prerequisite | Prevents false blocker. | Consume `agent_platform_reviewer_mesh_immune_safeguards_contract.md`. |
| P8.3-DRIFT-006 | schema semantics | Schema candidate vs implementation ambiguity. | Schema candidate is not implementation. | resolved | Prevents code/schema generation. | SCHEMA-003. |
| P8.3-DRIFT-007 | harness input | HarnessInputPackage vs harness execution ambiguity. | HarnessInputPackage does not execute harnesses. | resolved | Prevents OpenCode/Hermes activation. | SCHEMA-007. |
| P8.3-DRIFT-008 | harness output | HarnessOutputPackage vs trusted output ambiguity. | HarnessOutputPackage records user-pasted output and is not trusted by default. | resolved | Prevents unreviewed acceptance. | SCHEMA-008. |
| P8.3-DRIFT-009 | commit candidate | CommitCandidate vs Git mutation ambiguity. | CommitCandidate is advisory only. | resolved | Preserves user Git authority. | SCHEMA-014. |
| P8.3-DRIFT-010 | command block | CommitCommandBlock vs automatic Git ambiguity. | CommitCommandBlock is advisory only. | resolved | Prevents automatic Git. | SCHEMA-015. |
| P8.3-DRIFT-011 | source refs | SourceRef vs source loading ambiguity. | SourceRef is metadata only. | resolved | Prevents source loading. | SCHEMA-019. |
| P8.3-DRIFT-012 | file refs | FileRef vs file inspection ambiguity. | FileRef is not file inspection. | resolved | Prevents content inspection. | Supporting refs. |
| P8.3-DRIFT-013 | evidence refs | EvidenceRef vs authority ambiguity. | Evidence supports; it does not decide. | resolved | Prevents evidence-as-authority. | SCHEMA-021. |
| P8.3-DRIFT-014 | review verdict | ReviewVerdictPackage vs approval ambiguity. | ReviewVerdictPackage is review metadata, not Git approval. | resolved | Preserves human approval. | SCHEMA-010. |
| P8.3-DRIFT-015 | integration summary | IntegrationSummary vs automatic merge ambiguity. | IntegrationSummary is manual synthesis, not automatic merge. | resolved | Prevents automatic integration. | SCHEMA-011. |

## 31. Schema Candidate Invariants

| invariant | statement |
| --- | --- |
| SCHEMA-001 | P8.3 is core workflow schema candidate design only. |
| SCHEMA-002 | Schema is not runtime. |
| SCHEMA-003 | Schema candidate is not implementation. |
| SCHEMA-004 | Schema reference is not permission. |
| SCHEMA-005 | UserObjective is not broad approval. |
| SCHEMA-006 | WorkPacket is manual execution projection, not automatic dispatch. |
| SCHEMA-007 | HarnessInputPackage does not execute harnesses. |
| SCHEMA-008 | HarnessOutputPackage records user-pasted output and is not trusted by default. |
| SCHEMA-009 | ReviewInputPackage is not automatic reviewer assignment. |
| SCHEMA-010 | ReviewVerdictPackage is review metadata, not Git approval. |
| SCHEMA-011 | IntegrationSummary is manual synthesis, not automatic merge. |
| SCHEMA-012 | AcceptedOutputRegister is not Git approval. |
| SCHEMA-013 | RejectedOutputRegister must exclude rejected paths from commit candidates. |
| SCHEMA-014 | CommitCandidate is advisory only. |
| SCHEMA-015 | CommitCommandBlock is advisory only. |
| SCHEMA-016 | CommitCommandBlock must use exact paths. |
| SCHEMA-017 | CommitCommandBlock must never use git add . |
| SCHEMA-018 | The user commits and pushes manually. |
| SCHEMA-019 | SourceRef is metadata only. |
| SCHEMA-020 | Path presence is not content inspection permission. |
| SCHEMA-021 | Evidence supports; it does not decide. |
| SCHEMA-022 | Validation evaluates; governance decides. |
| SCHEMA-023 | Security constrains; it does not activate. |
| SCHEMA-024 | Provider metadata is not provider activation. |
| SCHEMA-025 | Tool metadata is not tool execution. |
| SCHEMA-026 | Agent metadata is not agent execution. |
| SCHEMA-027 | Graphify evidence is supporting generated evidence only, not authority. |
| SCHEMA-028 | GBrain / GStack / Hermes remain future candidates, not active runtime. |
| SCHEMA-029 | Siamese is product vision, not product activation. |
| SCHEMA-030 | Cognitive Semantic System substrate remains deferred. |

## 32. Future Validation Targets

Future validation targets are proposed only and were not executed:

| target | status |
| --- | --- |
| core workflow schema candidates document exists | future target, not executed. |
| UserObjective required fields completeness | future target, not executed. |
| WorkPacket required fields completeness | future target, not executed. |
| HarnessInputPackage required fields completeness | future target, not executed. |
| HarnessOutputPackage required fields completeness | future target, not executed. |
| ReviewInputPackage required fields completeness | future target, not executed. |
| ReviewVerdictPackage required fields completeness | future target, not executed. |
| IntegrationSummary required fields completeness | future target, not executed. |
| DriftRegister required fields completeness | future target, not executed. |
| AcceptedOutputRegister required fields completeness | future target, not executed. |
| RejectedOutputRegister required fields completeness | future target, not executed. |
| CommitCandidate required fields completeness | future target, not executed. |
| CommitCommandBlock required fields completeness | future target, not executed. |
| schema relationship model completeness | future target, not executed. |
| shared field conventions completeness | future target, not executed. |
| exact path Git safety invariant | future target, not executed. |
| no git add . invariant | future target, not executed. |
| HarnessInputPackage no-execution invariant | future target, not executed. |
| HarnessOutputPackage not-trusted-by-default invariant | future target, not executed. |
| ReviewVerdictPackage not-Git-approval invariant | future target, not executed. |
| IntegrationSummary not-automatic-merge invariant | future target, not executed. |
| CommitCandidate not-Git-mutation invariant | future target, not executed. |
| SourceRef metadata-only invariant | future target, not executed. |
| no schema implementation invariant | future target, not executed. |
| no JSON schema generation invariant | future target, not executed. |
| no runtime activation invariant | future target, not executed. |
| no provider/auth/API/MCP invariant | future target, not executed. |
| no tool execution invariant | future target, not executed. |
| no agent execution invariant | future target, not executed. |
| no product source inspection invariant | future target, not executed. |
| no external runtime activation invariant | future target, not executed. |

## 33. Future Hardening Candidates

Future tickets are proposed only and not started:

| candidate | purpose |
| --- | --- |
| SCHEMA-HARD-01 - UserObjective Schema Candidate Alignment | Harden user objective candidate shape. |
| SCHEMA-HARD-02 - WorkPacket / HarnessInputPackage Schema Alignment | Harden work packet and harness input relationship. |
| SCHEMA-HARD-03 - HarnessOutputPackage Intake Schema Alignment | Harden user-pasted output capture. |
| SCHEMA-HARD-04 - ReviewInputPackage / ReviewVerdictPackage Schema Alignment | Harden review input and verdict candidates. |
| SCHEMA-HARD-05 - IntegrationSummary / DriftRegister Schema Alignment | Harden integration and drift candidates. |
| SCHEMA-HARD-06 - Accepted / Rejected Output Register Schema Alignment | Harden acceptance and rejection registers. |
| SCHEMA-HARD-07 - CommitCandidate / CommitCommandBlock Schema Alignment | Harden exact-path commit advice. |
| SCHEMA-HARD-08 - Exact-Path Git Safety Schema Validation Design | Define future Git safety checks without executing Git. |
| SCHEMA-HARD-09 - P8 Schema Candidate Drift Validation Design | Define schema drift validation checklist. |
| SCHEMA-HARD-10 - MVP-0 Schema Implementation Readiness Review | Future readiness review before implementation planning. |

## 34. Created / Modified / Not Created Register

Created:

| item |
| --- |
| `0_architecture/governance/agent_platform_core_workflow_schema_candidates.md` |

Modified:

| item |
| --- |
| none |

Not created / not approved:

| item | status |
| --- | --- |
| no schema implementation | Preserved. |
| no JSON schema files | Preserved. |
| no code files | Preserved. |
| no package | Preserved. |
| no MVP skeleton package | Preserved. |
| no CLI/TUI/web UI | Preserved. |
| no adapters | Preserved. |
| no OpenCode execution | Preserved. |
| no Hermes runtime | Preserved. |
| no GBrain runtime | Preserved. |
| no GStack runtime | Preserved. |
| no Graphify rerun | Preserved. |
| no Graphify adoption | Preserved. |
| no provider/auth/API/MCP activation | Preserved. |
| no credential use | Preserved. |
| no API calls | Preserved. |
| no MCP activation | Preserved. |
| no tool execution | Preserved. |
| no shell/subprocess execution beyond allowed posture checks | Preserved. |
| no package-manager execution | Preserved. |
| no build/test/CI execution | Preserved. |
| no validation execution | Preserved. |
| no security enforcement activation | Preserved. |
| no agent execution | Preserved. |
| no task execution | Preserved. |
| no live connector activation | Preserved. |
| no Cadence | Preserved. |
| no always-on behavior | Preserved. |
| no source loading | Preserved. |
| no source inspection | Preserved. |
| no product source inspection | Preserved. |
| no external source inspection | Preserved. |
| no GBrain source inspection | Preserved. |
| no GStack source inspection | Preserved. |
| no Hermes source inspection | Preserved. |
| no raw Graphify output inspection | Preserved. |
| no Codegraph execution | Preserved. |
| no vector DB | Preserved. |
| no embeddings | Preserved. |
| no graph DB | Preserved. |
| no ontology runtime | Preserved. |
| no persistence DB | Preserved. |
| no event stream | Preserved. |
| no telemetry | Preserved. |
| no generated outputs modified/tracked | Preserved. |
| no source tracking expansion | Preserved. |
| no publication | Preserved. |
| no Cognitive Semantic System substrate selected | Preserved. |
| no Git mutation by the agent | Preserved. |
| no .graphifyignore modified | Preserved. |
| no .gitignore modified | Preserved. |
| no P8.0 created or modified | Preserved. |
| no P8.1 created or modified | Preserved. |
| no P8.2 created or modified | Preserved. |
| no P8.4 created or modified | Preserved. |
| no P8.5 created or modified | Preserved. |
| no P8.6-P8.R created or modified | Preserved. |
| no P9 started | Preserved. |
| no P4 started | Preserved. |
| no EXT.* started | Preserved. |

## 35. Recommended Next Tickets

P8.1, P8.2, P8.4, and P8.5 are present by path check. Recommended Round 2:

```text
P8.6 - Graphify Read-Only Evidence Boundary
P8.7 - GBrain / GStack Memory Compatibility Boundary
P8.8 - Hermes Interface / Runtime Candidate Boundary
P8.9 - OpenCode Harness Upgrade Boundary
```

Do not recommend P8.10 until P8.1-P8.9 are complete.

Do not recommend implementation tickets P8.12-P8.16 until P8.10/P8.11 authorize them.

Do not recommend runtime activation, autonomous orchestration, provider/auth activation, tool execution, agent execution, product activation, Graphify adoption, GBrain/GStack/Hermes/Cadence activation, source tracking expansion, vector DB implementation, graph DB implementation, or Cognitive Semantic System substrate selection.

## 36. Final Verdict

| Question | Answer |
| --- | --- |
| What did P8.3 create? | `0_architecture/governance/agent_platform_core_workflow_schema_candidates.md`. |
| What UserObjective schema candidate was defined? | User intent metadata with scope, constraints, refs, decision points, stop rules, and limitations; not broad approval. |
| What WorkPacket schema candidate was defined? | Manual execution projection with lane/native refs, scope, inputs, dependencies, review/integration/security/validation/context/harness requirements, stop rules, and completion criteria. |
| What HarnessInputPackage schema candidate was defined? | Manual copy/paste harness input for H0/H1 posture with allowed/blocked scope, context, refs, expected output, stop rules, and limitations. |
| What HarnessOutputPackage schema candidate was defined? | User-provided external harness output capture with structured summary, claimed files/commands/tests, decisions, blockers, drift, refs, and review requirement; not trusted by default. |
| What ReviewInputPackage schema candidate was defined? | Review target, scope, type, role, checklist refs, evidence/validation/security/source/retention refs, stop rules, expected verdicts, and limitations. |
| What ReviewVerdictPackage schema candidate was defined? | Review metadata with verdict, accepted/limited/rework/blocked/out-of-scope items, findings, blockers, refs, escalation, and next action. |
| What IntegrationSummary schema candidate was defined? | Manual synthesis over work packets, harness outputs, review verdicts, registers, drift, native/context/evidence refs, decisions, blockers, unresolved drift, next ticket, and human decision requirement. |
| What DriftRegister schema candidate was defined? | Drift item model across schema, contract, naming, boundary, security, validation, evidence, retention, rollback, topology, projection, commit scope, and external harness claim drift. |
| What AcceptedOutputRegister schema candidate was defined? | Accepted work packet/output/verdict/file/decision/limitation/rationale/native-ref register with commit candidate ref and human decision requirement. |
| What RejectedOutputRegister schema candidate was defined? | Rejected work packet/output/path/reason/blocking verdict/out-of-scope/rework/future ticket/security-boundary register. |
| What CommitCandidate schema candidate was defined? | Advisory commit proposal with included/excluded paths, registers, drift, verdicts, summary, message, Git command strings, rollback note, approval, and limitations. |
| What CommitCommandBlock schema candidate was defined? | Advice-only command block with status command, exact git add commands, commit command, push command, excluded paths, forbidden commands, human execution, and limitations. |
| What shared field conventions were defined? | ID/ref/status/scope/summary/limitation/blocker/evidence/validation/security/retention/rollback/incident/human approval/file/path/source/context/review/stop-rule conventions. |
| What schema relationship model was defined? | UserObjective -> WorkPacket -> HarnessInputPackage -> HarnessOutputPackage -> ReviewInputPackage -> ReviewVerdictPackage -> IntegrationSummary -> DriftRegister/AcceptedOutputRegister/RejectedOutputRegister -> CommitCandidate -> CommitCommandBlock. |
| How does P8.3 prevent schema candidates from becoming runtime? | It states schema is not runtime, schema candidate is not implementation, and execution-like fields become blocked metadata. |
| How does P8.3 preserve OpenCode as H0 manual harness? | HarnessInputPackage may be copied manually by the user, while OpenCode execution and adapters remain blocked. |
| How does P8.3 prevent HarnessOutputPackage from being trusted by default? | HarnessOutputPackage records user-pasted output, does not verify execution, does not trust claims by default, and does not accept outputs by default. |
| How does P8.3 preserve exact-path Git safety? | CommitCandidate and CommitCommandBlock require exact paths, human execution, and forbid `git add .`. |
| Does P8.3 ever recommend git add .? | No. Never recommend git add . |
| Was schema implementation created? | No. |
| Were JSON schema files created? | No. |
| Was code created? | No. |
| Was a package created? | No. |
| Was MVP UI implemented? | No. |
| Were adapters implemented? | No. |
| Was OpenCode executed? | No. |
| Were Graphify/GBrain/GStack/Hermes activated? | No. |
| Was provider/auth/API/MCP activated? | No. |
| Were tools executed? | No. |
| Were agents executed? | No. |
| Was product/Siamese source inspected? | No. |
| Was validation executed? | No. |
| Was security enforcement activated? | No. |
| Was persistence/vector/graph DB implemented? | No. |
| Was generated output tracking approved? | No. |
| Was source tracking expansion approved? | No. |
| Was Cognitive Semantic System substrate selected? | No. |
| What pending P8 alignments remain? | None for P8.1, P8.2, P8.4, or P8.5 because all four sibling files are present by path check and consumed as present posture. |
| What is the next ticket? | Round 2: P8.6, P8.7, P8.8, or P8.9. |

Stop after P8.3. Do not start P8.6, P8.7, P8.8, P8.9, P8.10, P8.11, P8.12+, P8.R, P9, P4, EXT.*, schema implementation, JSON schema generation, package creation, MVP UI, adapters, OpenCode execution, Graphify/GBrain/GStack/Hermes/Cadence activation, provider/auth/API/MCP activation, tool execution, agent execution, product activation, source tracking expansion, generated output tracking, publication, Git mutation, or Cognitive Semantic System substrate selection.
