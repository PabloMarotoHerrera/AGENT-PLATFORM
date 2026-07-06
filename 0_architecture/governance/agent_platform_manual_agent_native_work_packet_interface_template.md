# Manual Agent-Native Work Packet Interface Template

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Manual Agent-Native Work Packet Interface Template |
| Ticket | P7.1-FIRST-PILOT |
| Status | Accepted canonical manual OpenCode work packet interface template |
| Scope | Documentation-only reusable interface template for manual Lead Chat -> OpenCode H0 -> Reviewer -> Integrator -> Git advice workflow. |
| Authority | Interface template only, not runtime activation, not OpenCode integration, not tool execution, not provider/auth/API/MCP activation, not autonomous orchestration, not automatic dispatch, not automatic reviewer assignment, not automatic integration, not Git mutation. |

## 2. Purpose

This document defines the canonical textual interface for manual OpenCode work packets inside the AGENT PLATFORM / Siamese manual agent-native workflow.

It provides reusable templates for `WorkPacket`, `HarnessInputPackage`, `HarnessOutputPackage`, `ReviewInputPackage`, `ReviewVerdictPackage`, `IntegrationSummary`, `DriftRegister`, `AcceptedOutputRegister`, `RejectedOutputRegister`, `CommitCandidate`, and `CommitCommandBlock`.

The interface is designed for H0 user-operated OpenCode use only. It does not integrate OpenCode into AGENT PLATFORM.

## 3. Current Posture

| Area | Current posture | Interface interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM | Manual agent-native workflow is ready for first manual pilot. | Textual work packet interface can be used by the user. | Runtime platform activation. |
| OpenCode | H0 user-operated external harness. | User manually copies bounded work packet text into OpenCode. | OpenCode adapter, internal OpenCode integration, or automatic dispatch. |
| Reviewer Mesh | Manual metadata review layer. | Consumes returned `HarnessOutputPackage`. | Automatic reviewer assignment or auto-review. |
| Integrator | Manual synthesis and commit advisory layer. | Consumes review verdicts and drift register. | Automatic integration or Git mutation. |
| Git | User-owned. | Exact-path advice only. | Agent staging, commit, push, publication, or `git add .`. |

## 4. Interface Boundary

This interface is documentation-only and manual-only.

The interface may be copied by the user into a user-operated H0 harness. It must not be transformed into automatic dispatch, internal tool execution, provider/API/MCP activation, runtime task execution, automatic reviewer assignment, automatic integration, or Git mutation.

Context inclusion is not permission. Provider metadata is not provider activation. Tool metadata is not tool execution. Agent metadata is not agent execution. Review metadata is not approval. Commit advice is not Git mutation.

## 5. Canonical Workflow

```text
Lead Chat / User Gateway
-> WorkPacket / HarnessInputPackage
-> user-operated OpenCode H0 harness
-> HarnessOutputPackage
-> ReviewInputPackage
-> Reviewer Mesh / Immune Safeguards
-> ReviewVerdictPackage
-> IntegrationSummary / DriftRegister
-> AcceptedOutputRegister / RejectedOutputRegister
-> CommitCandidate / CommitCommandBlock
-> user performs Git manually
```

Every stage is manual only, metadata only unless the user manually operates an H0 harness outside AGENT PLATFORM, not runtime, not automatic dispatch, not automatic review, not automatic integration, and not Git mutation.

## P7.2 Simplified Usage Modes

This P7.2 addendum keeps the full canonical interface as reference and adds compact usage modes for repeated manual documentation/governance work.

The full schema remains canonical.

Compact mode is allowed for small documentation-only governance tasks.

Compact mode does not weaken boundaries.

Exact target files remain mandatory.

Blocked actions remain mandatory.

Stop rules remain mandatory.

Review requirement remains mandatory.

Integrator requirement remains mandatory when Git advice is expected.

Exact-path Git advice remains mandatory.

`git add .` remains forbidden.

### Usage Mode Matrix

| Usage mode | When to use | Required posture | Stop condition |
| --- | --- | --- | --- |
| `full_canonical_mode` | Use for complex governance, cross-document, high-risk, external-boundary, product-boundary, or architecture-sensitive work. | Use the full template family and all relevant agent-native refs. | Stop if the task implies blocked runtime/source/provider/tool/Git behavior. |
| `compact_documentation_mode` | Use for small documentation-only governance tickets with exact target files and no product/external/runtime/tool/provider scope. | Use compact WorkPacket, compact HarnessInputPackage, compact HarnessOutputPackage, compact reviewer checklist, and compact integrator checklist. | Stop if exact target files, blocked actions, stop rules, review, integration, or Git boundaries are unclear. |
| `review_only_mode` | Use when only reviewing a returned HarnessOutputPackage. | Use ReviewInputPackage, ReviewVerdictPackage, and compact reviewer boundary drift checklist. | Stop if review requires source loading, automatic assignment, or blocked scope. |
| `integrator_only_mode` | Use when review is complete and only accepted/rejected output plus exact-path Git advice must be reconciled. | Use IntegrationSummary, DriftRegister, AcceptedOutputRegister, RejectedOutputRegister, CommitCandidate, and compact integrator checklist. | Stop if rejected files may be staged or exact Git paths are unclear. |
| `blocked_high_risk_mode` | Use when the task requires product/Siamese source, external source, runtime, provider/auth/API/MCP, tools, GBrain/Hermes/Cadence, Graphify/Codegraph, persistence, generated tracking, publication, or Git mutation by agent. | Stop instead of proceeding. | The task must be routed to a future explicit governance gate. |

### Field Classification Model

Field classifications:

```text
mandatory
conditional
optional
not_applicable_with_reason
blocked
```

A field may be marked `not_applicable_with_reason` only if the reason is explicit and the omission does not hide scope, target files, blocked actions, review requirements, integration requirements, or Git boundaries.

Mandatory fields that must never be optional:

```text
work_packet_id
ticket_title
objective
scope
non_goals
target_files
blocked_files
allowed_actions
blocked_actions
expected_output
review_required
integrator_required
stop_rules
success_criteria
failure_criteria
```

Mandatory Git-related fields when commit advice is expected:

```text
included_file_paths
excluded_file_paths
commit_message_candidate
git_add_paths
git_commit_command
git_push_command
human_approval_required
```

| Template family | Mandatory fields | Conditional fields | Optional fields | `not_applicable_with_reason` allowed for | Blocked fields/content |
| --- | --- | --- | --- | --- | --- |
| WorkPacket | `work_packet_id`, `ticket_title`, `objective`, `scope`, `non_goals`, `target_files`, `blocked_files`, `allowed_actions`, `blocked_actions`, `expected_output`, `review_required`, `integrator_required`, `stop_rules`, `success_criteria`, `failure_criteria` | `memory_manifest_refs`, `agent_native_refs`, `task_graph_refs`, `blackboard_refs`, `capability_cell_refs`, `routing_decision_refs`, `reviewer_mesh_refs` | `ticket_kind`, `context_refs` when already embedded in supplied ticket text | Agent-native refs that do not apply to a small documentation task, with reason. | Secrets, credentials, product/Siamese source, external source, runtime permissions, Git approval. |
| HarnessInputPackage | `target_harness`, `harness_level`, `manual_operator`, `ticket_text`, `allowed_context`, `blocked_context`, `allowed_files`, `expected_response_format`, `stop_rules` | `work_packet_ref`, `forbidden_commands`, `safe_reporting_requirements` | `required_file_register`, `required_decision_register`, `required_not_created_register`, `required_blocker_register` in compact mode if expected response covers them | Commands when no commands are allowed, with reason. | Automatic dispatch, OpenCode integration, H2/H3 adapter behavior, credentials, provider/API/MCP. |
| HarnessOutputPackage | `summary`, `files_created`, `files_modified`, `files_not_created`, `commands_run`, `decisions_made`, `assumptions`, `blockers`, `limitations`, `scope_deviations`, `boundary_deviations` | `evidence_refs`, `validation_refs`, `security_refs`, `recommended_next_ticket`, `commit_advice_candidate` | `source_harness`, `source_work_packet_ref` when obvious from surrounding packet | Empty registers, if explicitly stated as none. | Accepted-by-default status, Git approval, runtime approval. |
| ReviewInputPackage | `target_output_package_ref`, `review_scope`, `excluded_scope`, `reviewer_mesh_ref`, `required_verdict_format`, `human_decision_points`, `stop_rules` | `reviewer_cell_refs`, `immune_safeguard_refs`, `review_checklist_refs`, `context_refs`, `evidence_refs`, marker refs | Extra blackboard refs when not needed | Specific marker groups when no marker exists, with reason. | Source loading permission, automatic reviewer assignment. |
| ReviewVerdictPackage | `review_input_package_ref`, `reviewer_cell_ref`, `verdict_status`, `findings`, `human_final_decision_required`, `limitations` | `accepted_items`, `accepted_with_limitations_items`, `needs_rework_items`, `blocked_items`, `out_of_scope_items`, `markers_emitted`, `containment_recommendations`, `rework_requests` | Empty item categories if explicitly none | Item categories that do not apply, with reason or empty register. | Git approval, runtime approval, final human decision. |
| IntegrationSummary | `integrated_output_package_refs`, `review_verdict_package_refs`, `accepted_output_register_ref`, `rejected_output_register_ref`, `drift_register_ref`, `summary`, `decisions`, `human_decision_required` | `agent_native_refs`, `limitations`, `blockers`, `unresolved_drift`, `recommended_next_ticket` | Extra refs for simple tasks | Agent-native refs not relevant to compact docs, with reason. | Automatic merge, Git approval. |
| DriftRegister | `drift_register_id`, `drift_items`, `drift_type`, `severity`, `resolution_status`, `resolution_summary`, `review_required`, `human_decision_required` | `affected_files`, `affected_contracts`, `affected_agent_native_refs`, `owner_or_route`, `limitations` | Empty drift categories if explicitly none | Affected refs when no drift touches them, with reason. | Hidden scope expansion, auto-remediation. |
| AcceptedOutputRegister | `accepted_output_register_id`, `accepted_output_package_refs`, `accepted_file_paths`, `accepted_decisions`, `accepted_reviewer_verdict_refs`, `accepted_integrator_rationale`, `human_decision_required` | `accepted_limitations`, `required_follow_up`, `commit_candidate_ref` | Follow-up when none | Commit candidate ref when no Git advice is expected, with reason. | Git approval. |
| RejectedOutputRegister | `rejected_output_register_id`, `rejected_output_package_refs`, `rejected_file_paths`, `rejection_reasons`, `human_decision_required` | `blocking_verdict_refs`, `out_of_scope_items`, `rework_required`, `future_ticket_refs`, `limitations` | Empty rejected path list only if no rejected files exist. | Future tickets when not needed, with reason. | Staging permission for rejected paths. |
| CommitCandidate | `commit_candidate_id`, `commit_scope`, `included_file_paths`, `excluded_file_paths`, `accepted_output_register_ref`, `rejected_output_register_ref`, `drift_register_ref`, `reviewer_verdict_refs`, `integration_summary_ref`, `commit_message_candidate`, `git_add_paths`, `git_commit_command`, `git_push_command`, `human_approval_required` | `rollback_note`, `limitations` | None for Git command fields. | Commit candidate may be not applicable only when no Git advice is expected. | `git add .`, staging flags, auto-commit, auto-push. |

## Compact WorkPacket View For Documentation-Only Tasks

Required compact fields:

```text
work_packet_id
ticket_title
objective
target_files
blocked_files
allowed_actions
blocked_actions
required_context
expected_output
review_required
integrator_required
stop_rules
success_criteria
failure_criteria
```

Compact template:

```text
work_packet_id: <id>
ticket_title: <title>
objective: <single bounded objective>
target_files:
- <exact path>
blocked_files:
- product/Siamese source
- external source
- generated artifacts
- secrets/credentials
allowed_actions:
- create or modify documentation-only markdown in exact target files
blocked_actions:
- runtime activation
- source loading
- product/Siamese source inspection
- external source inspection
- provider/auth/API/MCP
- tool execution
- Graphify/Codegraph execution
- GBrain/Hermes/Cadence runtime
- validation/tests/scripts/builds unless explicitly scoped
- security enforcement
- Git mutation by agent
required_context:
- <governance docs or refs supplied by user>
expected_output:
- HarnessOutputPackage compact summary
review_required: true
integrator_required: true
stop_rules:
- stop if blocked action is required
- stop if target file scope is unclear
- stop if secret/credential appears
success_criteria:
- exact target file created/modified
- no blocked behavior introduced
failure_criteria:
- blocked scope required
- `git add .` recommended
```

## Compact HarnessInputPackage View For OpenCode H0

Required compact fields:

```text
target_harness
harness_level
manual_operator
ticket_text
allowed_context
blocked_context
allowed_files
expected_response_format
stop_rules
```

Required statements:

```text
OpenCode remains H0 user-operated only.
The user manually copies this package into OpenCode.
This package is not automatic dispatch.
This package is not OpenCode integration.
```

Compact template:

```text
target_harness: OpenCode
harness_level: H0
manual_operator: user
allowed_context: <provided governance docs or refs only>
blocked_context: product/Siamese source, external source, generated artifacts, secrets, credentials, raw Graphify output, GBrain source
allowed_files: <exact target paths only>
expected_response_format: Compact HarnessOutputPackage summary
stop_rules: stop on blocked context, blocked action, unclear target files, credential exposure, or `git add .`
```

## Compact HarnessOutputPackage View For OpenCode Summaries

Required compact output checklist:

```text
Summary
Files created
Files modified
Files not created
Commands run
Decisions made
Assumptions
Blockers
Limitations
Scope deviations
Boundary deviations
Recommended next ticket
Commit advice candidate
```

Required statements:

```text
HarnessOutputPackage is proposed output only.
HarnessOutputPackage is not accepted by default.
HarnessOutputPackage must be reviewed before integration.
HarnessOutputPackage does not approve Git.
```

## Compact Reviewer Boundary Drift Checklist

Required checks:

```text
scope_boundary_check
target_file_check
blocked_file_check
runtime_activation_check
tool_execution_check
provider_auth_api_mcp_check
product_source_check
external_source_check
gbrain_hermes_cadence_check
graphify_codegraph_check
persistence_vector_graph_db_check
validation_execution_check
security_enforcement_check
git_mutation_check
git_add_dot_check
review_verdict_not_git_approval_check
```

Allowed compact verdicts:

```text
accepted_for_integrator_review
accepted_with_limitations_for_integrator_review
needs_rework
blocked
out_of_scope
```

Compact reviewer result:

```text
reviewer_checklist_id: <id>
target_output_package_ref: <HarnessOutputPackage ref>
checks_passed: <list>
checks_failed: <list>
markers_emitted: <markers or none>
verdict: <allowed compact verdict>
limitations: <limitations>
human_final_decision_required: true | false
```

## Compact Integrator Exact-Path Checklist

Required checks:

```text
accepted_files_exact_paths_present
rejected_files_excluded
drift_register_present
review_verdict_present
commit_scope_matches_accepted_files
commit_message_matches_ticket_scope
git_add_paths_exact
no_git_add_dot
user_final_git_authority_preserved
```

Required compact commit advice pattern:

```powershell
git status --short

git add <exact_path_1>
git add <exact_path_2>

git commit -m "<exact commit message>"

git push origin main
```

Forbidden:

```powershell
git add .
```

Compact integrator result:

```text
integrator_checklist_id: <id>
accepted_files: <exact paths>
rejected_files: <exact paths or none>
drift_register_ref: <ref>
review_verdict_ref: <ref>
commit_candidate: advisory only, exact paths only
human_approval_required: true
```

## P7.2 Examples

### Example 1 - Safe Documentation-Only Governance Task

Compact WorkPacket:

```text
work_packet_id: WP-P72-EXAMPLE-001
ticket_title: Example Governance Note
objective: Create a small AGENT PLATFORM governance documentation note.
target_files:
- 0_architecture/governance/example_safe_doc.md
blocked_files:
- product/Siamese source
- external source
- generated artifacts
- secrets/credentials
allowed_actions:
- create documentation-only markdown in exact target files
blocked_actions:
- runtime activation
- source loading
- product/Siamese source inspection
- external source inspection
- provider/auth/API/MCP
- tool execution
- Graphify/Codegraph execution
- GBrain/Hermes/Cadence runtime
- validation/tests/scripts/builds unless explicitly scoped
- security enforcement
- Git mutation by agent
required_context:
- user-supplied governance docs or refs
expected_output:
- HarnessOutputPackage compact summary
review_required: true
integrator_required: true
stop_rules:
- stop if blocked action is required
- stop if target file scope is unclear
- stop if secret/credential appears
success_criteria:
- 0_architecture/governance/example_safe_doc.md created
- no blocked behavior introduced
failure_criteria:
- blocked scope required
- `git add .` recommended
```

Compact HarnessInputPackage:

```text
target_harness: OpenCode
harness_level: H0
manual_operator: user
allowed_context: user-supplied governance docs only
blocked_context: product/Siamese source, external source, generated artifacts, secrets, credentials
allowed_files: 0_architecture/governance/example_safe_doc.md
expected_response_format: Compact HarnessOutputPackage summary
stop_rules: stop on blocked context, unclear target file, credential exposure, or `git add .`
```

Compact HarnessOutputPackage:

```text
Summary: Created a small governance note.
Files created: 0_architecture/governance/example_safe_doc.md
Files modified: none
Files not created: runtime files, product files, source files, generated artifacts
Commands run: none
Decisions made: kept scope documentation-only
Assumptions: governance refs supplied by user were sufficient
Blockers: none
Limitations: documentation-only output
Scope deviations: none
Boundary deviations: none
Recommended next ticket: none
Commit advice candidate: exact-path only
```

Compact reviewer verdict:

```text
ReviewVerdictPackage: accepted_for_integrator_review
checks_passed: scope_boundary_check, target_file_check, runtime_activation_check, provider_auth_api_mcp_check, product_source_check, external_source_check, git_add_dot_check
checks_failed: none
limitations: documentation-only review
human_final_decision_required: true for Git
```

Compact integrator checklist:

```text
accepted_files_exact_paths_present: pass
rejected_files_excluded: pass
drift_register_present: pass
review_verdict_present: pass
commit_scope_matches_accepted_files: pass
commit_message_matches_ticket_scope: pass
git_add_paths_exact: pass
no_git_add_dot: pass
user_final_git_authority_preserved: pass
```

Exact-path CommitCandidate:

```powershell
git status --short

git add 0_architecture/governance/example_safe_doc.md

git commit -m "Add example governance note"

git push origin main
```

### Example 2 - Rejected Unsafe Output

Unsafe harness output:

```text
Summary: Created a governance note and recommended `git add .`, product/Siamese source inspection, provider/API/MCP activation, runtime activation, Graphify rerun/adoption, and GBrain/Hermes/Cadence runtime exploration.
Files created: 0_architecture/governance/example_safe_doc.md
Boundary deviations: recommended blocked actions
Commit advice candidate: git add .
```

ReviewVerdictPackage:

```text
ReviewVerdictPackage: blocked
blocked_items:
- `git add .`
- product/Siamese source inspection
- provider/API/MCP activation
- runtime activation
- Graphify rerun/adoption
- GBrain/Hermes/Cadence runtime
containment_recommendations:
- reject unsafe output
- request rework with blocked actions removed
human_final_decision_required: true
```

RejectedOutputRegister:

```text
rejected_output_register_id: ROR-P72-EXAMPLE-002
rejected_output_package_refs: unsafe output example
rejected_file_paths: none accepted from unsafe output until rework
rejection_reasons: blocked actions recommended
out_of_scope_items: product/Siamese source, provider/API/MCP, runtime, Graphify, GBrain/Hermes/Cadence, `git add .`
rework_required: true
future_ticket_refs: governance escalation if unsafe scope is intentional
human_decision_required: true
```

CommitCandidate:

```text
not produced
```

Required route:

```text
rework or governance escalation
```

## 6. WorkPacket Template

Required fields:

```text
work_packet_id
ticket_title
ticket_kind
objective
scope
non_goals
target_files
blocked_files
allowed_actions
blocked_actions
required_inputs
context_refs
memory_manifest_refs
agent_native_refs
task_graph_refs
blackboard_refs
capability_cell_refs
routing_decision_refs
reviewer_mesh_refs
harness_boundary
expected_output
review_required
integrator_required
git_advisory_expected
stop_rules
success_criteria
failure_criteria
```

Required statements:

```text
WorkPacket is manual instruction text.
WorkPacket is not a runtime task.
WorkPacket is not automatic dispatch.
WorkPacket is not authority to inspect source beyond exact scope.
WorkPacket is not Git approval.
```

Template body:

```text
work_packet_id: <unique manual id>
ticket_title: <exact title>
ticket_kind: <documentation_only_governance_workflow | other allowed manual kind>
objective: <single bounded objective>
scope: <included work only>
non_goals: <explicit exclusions>
target_files: <exact paths only>
blocked_files: <paths/surfaces not allowed>
allowed_actions: <manual documentation actions only>
blocked_actions: <runtime, source, provider, tool, Git, and publication blocks>
required_inputs: <governance/context refs only>
context_refs: <approved context refs>
memory_manifest_refs: <manual memory/context refs>
agent_native_refs: <topology/task/blackboard/cell/routing/review refs>
task_graph_refs: <TaskGraphRef ids or descriptions>
blackboard_refs: <BlackboardRef ids or descriptions>
capability_cell_refs: <CapabilityCellRef ids or descriptions>
routing_decision_refs: <RoutingDecisionRef ids or descriptions>
reviewer_mesh_refs: <ReviewerMesh refs>
harness_boundary: H0 user-operated only unless H1 design-only is explicitly scoped
expected_output: <required HarnessOutputPackage format>
review_required: true
integrator_required: true
git_advisory_expected: <true | false>
stop_rules: <stop triggers>
success_criteria: <completion criteria>
failure_criteria: <failure/stop criteria>
```

## 7. HarnessInputPackage Template

Required fields:

```text
harness_input_package_id
target_harness
harness_level
manual_operator
work_packet_ref
allowed_context
blocked_context
allowed_files
blocked_files
allowed_commands
forbidden_commands
expected_response_format
required_file_register
required_decision_register
required_not_created_register
required_blocker_register
stop_rules
safe_reporting_requirements
```

Required statements:

```text
HarnessInputPackage is manually copied by the user.
HarnessInputPackage is not automatic dispatch.
OpenCode is H0 user-operated only.
H1 is design-only metadata.
H2 controlled tool execution adapter is blocked.
H3 autonomous orchestration adapter is blocked.
```

Template body:

```text
harness_input_package_id: <unique manual id>
target_harness: OpenCode | Codex | Claude | Cursor | equivalent H0 surface
harness_level: H0
manual_operator: user
work_packet_ref: <WorkPacket id>
ticket_text: <bounded ticket text to copy manually>
allowed_context: <approved context only>
blocked_context: <secrets, credentials, product source, external source, raw generated outputs>
allowed_files: <exact target files>
blocked_files: <blocked files/surfaces>
allowed_commands: none, unless user explicitly supplies safe manual commands outside AGENT PLATFORM
forbidden_commands: tests, scripts, builds, Graphify, Codegraph, GBrain, Hermes, provider/API/MCP, Git mutation by agent, git add .
expected_response_format: HarnessOutputPackage
required_file_register: files_created, files_modified, files_not_created
required_decision_register: decisions_made, assumptions, limitations
required_not_created_register: blocked/not-created surfaces
required_blocker_register: blockers and stop conditions
stop_rules: <stop triggers>
safe_reporting_requirements: do not expose secrets; report limitations and blocked requests
```

## 8. HarnessOutputPackage Template

Required fields:

```text
harness_output_package_id
source_harness
source_work_packet_ref
summary
files_created
files_modified
files_not_created
commands_run
decisions_made
assumptions
blockers
limitations
scope_deviations
boundary_deviations
evidence_refs
validation_refs
security_refs
review_required
integrator_required
recommended_next_ticket
commit_advice_candidate
```

Required statements:

```text
HarnessOutputPackage is proposed output only.
HarnessOutputPackage is not accepted by default.
HarnessOutputPackage does not approve Git.
HarnessOutputPackage must be reviewed before integration.
```

Template body:

```text
harness_output_package_id: <unique manual id>
source_harness: <H0 harness name>
source_work_packet_ref: <WorkPacket id>
summary: <what was produced>
files_created: <exact paths>
files_modified: <exact paths>
files_not_created: <expected but not created>
commands_run: <commands run by the harness/user, or none>
decisions_made: <decisions and rationale>
assumptions: <assumptions>
blockers: <blockers>
limitations: <limitations>
scope_deviations: <scope deviations or none>
boundary_deviations: <boundary deviations or none>
evidence_refs: <evidence refs>
validation_refs: <validation refs, not executed unless explicitly allowed>
security_refs: <security refs, not scanners unless explicitly allowed>
review_required: true
integrator_required: true
recommended_next_ticket: <candidate only>
commit_advice_candidate: <candidate only; not Git approval>
```

## 9. ReviewInputPackage Template

Required fields:

```text
review_input_package_id
target_output_package_ref
review_scope
excluded_scope
reviewer_mesh_ref
reviewer_cell_refs
immune_safeguard_refs
review_checklist_refs
context_refs
evidence_refs
blackboard_refs
contradiction_markers
evidence_conflict_markers
drift_markers
unsafe_output_markers
scope_violation_markers
required_verdict_format
human_decision_points
stop_rules
```

Required statements:

```text
ReviewInputPackage is bounded review context.
ReviewInputPackage is not source loading permission.
ReviewRequest is not automatic reviewer assignment.
ReviewerMesh is metadata only.
```

Template body:

```text
review_input_package_id: <unique manual id>
target_output_package_ref: <HarnessOutputPackage id>
review_scope: <exact review scope>
excluded_scope: <excluded review scope>
reviewer_mesh_ref: <ReviewerMesh ref>
reviewer_cell_refs: <reviewer cells>
immune_safeguard_refs: <immune safeguards>
review_checklist_refs: <checklists>
context_refs: <approved refs>
evidence_refs: <evidence refs>
blackboard_refs: <blackboard refs>
contradiction_markers: <markers>
evidence_conflict_markers: <markers>
drift_markers: <markers>
unsafe_output_markers: <markers>
scope_violation_markers: <markers>
required_verdict_format: ReviewVerdictPackage
human_decision_points: <where user decision is required>
stop_rules: <stop triggers>
```

## 10. ReviewVerdictPackage Template

Required fields:

```text
review_verdict_package_id
review_input_package_ref
reviewer_cell_ref
verdict_status
accepted_items
accepted_with_limitations_items
needs_rework_items
blocked_items
out_of_scope_items
findings
markers_emitted
containment_recommendations
rework_requests
human_final_decision_required
limitations
```

Allowed verdicts:

```text
accepted_for_integrator_review
accepted_with_limitations_for_integrator_review
needs_rework
blocked
out_of_scope
escalated_for_human_final_decision
```

Required statements:

```text
ReviewVerdictPackage is review metadata only.
Reviewer approval is not Git approval.
ReviewVerdict is not runtime approval.
ReviewVerdict is not final human decision.
```

Template body:

```text
review_verdict_package_id: <unique manual id>
review_input_package_ref: <ReviewInputPackage id>
reviewer_cell_ref: <reviewer cell>
verdict_status: <allowed verdict>
accepted_items: <items>
accepted_with_limitations_items: <items>
needs_rework_items: <items>
blocked_items: <items>
out_of_scope_items: <items>
findings: <findings>
markers_emitted: <markers>
containment_recommendations: <recommendations only>
rework_requests: <manual metadata only>
human_final_decision_required: true | false
limitations: <limitations>
```

## 11. IntegrationSummary Template

Required fields:

```text
integration_summary_id
integrated_output_package_refs
review_verdict_package_refs
accepted_output_register_ref
rejected_output_register_ref
drift_register_ref
agent_native_refs
summary
decisions
limitations
blockers
unresolved_drift
recommended_next_ticket
human_decision_required
```

Required statements:

```text
IntegrationSummary is manual synthesis only.
IntegrationSummary is not automatic merge.
IntegrationSummary is not Git approval.
```

Template body:

```text
integration_summary_id: <unique manual id>
integrated_output_package_refs: <HarnessOutputPackage refs>
review_verdict_package_refs: <ReviewVerdictPackage refs>
accepted_output_register_ref: <AcceptedOutputRegister id>
rejected_output_register_ref: <RejectedOutputRegister id>
drift_register_ref: <DriftRegister id>
agent_native_refs: <task graph, blackboard, capability cell, routing, reviewer mesh refs>
summary: <manual synthesis>
decisions: <integration decisions>
limitations: <limitations>
blockers: <blockers>
unresolved_drift: <drift items>
recommended_next_ticket: <candidate only>
human_decision_required: true | false
```

## 12. DriftRegister Template

Required fields:

```text
drift_register_id
drift_items
affected_files
affected_contracts
affected_agent_native_refs
drift_type
severity
resolution_status
resolution_summary
owner_or_route
review_required
human_decision_required
limitations
```

Required drift types:

```text
scope_drift
contract_drift
naming_drift
boundary_drift
security_drift
validation_drift
evidence_drift
agent_native_topology_drift
manual_projection_drift
commit_scope_drift
```

Template body:

```text
drift_register_id: <unique manual id>
drift_items: <list>
affected_files: <exact paths>
affected_contracts: <contract refs>
affected_agent_native_refs: <refs>
drift_type: <required drift type>
severity: low | medium | high | blocking
resolution_status: resolved | accepted_limitation | deferred | blocked
resolution_summary: <summary>
owner_or_route: <reviewer, integrator, user, future ticket>
review_required: true | false
human_decision_required: true | false
limitations: <limitations>
```

## 13. AcceptedOutputRegister Template

Required fields:

```text
accepted_output_register_id
accepted_output_package_refs
accepted_file_paths
accepted_decisions
accepted_limitations
accepted_reviewer_verdict_refs
accepted_integrator_rationale
required_follow_up
commit_candidate_ref
human_decision_required
```

Required statement:

```text
AcceptedOutputRegister is not Git approval.
```

Template body:

```text
accepted_output_register_id: <unique manual id>
accepted_output_package_refs: <HarnessOutputPackage refs>
accepted_file_paths: <exact paths>
accepted_decisions: <decisions>
accepted_limitations: <limitations>
accepted_reviewer_verdict_refs: <ReviewVerdictPackage refs>
accepted_integrator_rationale: <rationale>
required_follow_up: <follow-up or none>
commit_candidate_ref: <CommitCandidate id or none>
human_decision_required: true | false
```

## 14. RejectedOutputRegister Template

Required fields:

```text
rejected_output_register_id
rejected_output_package_refs
rejected_file_paths
rejection_reasons
blocking_verdict_refs
out_of_scope_items
rework_required
future_ticket_refs
human_decision_required
limitations
```

Required statement:

```text
Rejected paths must not be staged.
```

Template body:

```text
rejected_output_register_id: <unique manual id>
rejected_output_package_refs: <HarnessOutputPackage refs>
rejected_file_paths: <exact paths>
rejection_reasons: <reasons>
blocking_verdict_refs: <ReviewVerdictPackage refs>
out_of_scope_items: <items>
rework_required: true | false
future_ticket_refs: <future refs>
human_decision_required: true | false
limitations: <limitations>
```

## 15. CommitCandidate Template

Required fields:

```text
commit_candidate_id
commit_scope
included_file_paths
excluded_file_paths
accepted_output_register_ref
rejected_output_register_ref
drift_register_ref
reviewer_verdict_refs
integration_summary_ref
commit_message_candidate
git_add_paths
git_commit_command
git_push_command
rollback_note
human_approval_required
limitations
```

Required statements:

```text
CommitCandidate is advisory only.
CommitCandidate does not stage files.
CommitCandidate does not commit.
CommitCandidate does not push.
CommitCandidate must never use git add .
```

Template body:

```text
commit_candidate_id: <unique manual id>
commit_scope: <exact accepted scope>
included_file_paths: <exact accepted paths only>
excluded_file_paths: <rejected, blocked, and untouched paths>
accepted_output_register_ref: <AcceptedOutputRegister id>
rejected_output_register_ref: <RejectedOutputRegister id>
drift_register_ref: <DriftRegister id>
reviewer_verdict_refs: <ReviewVerdictPackage refs>
integration_summary_ref: <IntegrationSummary id>
commit_message_candidate: <exact message>
git_add_paths: <exact paths only>
git_commit_command: git commit -m "<exact commit message>"
git_push_command: git push origin main
rollback_note: <manual rollback note>
human_approval_required: true
limitations: <limitations>
```

## 16. CommitCommandBlock Template

Required command pattern:

```powershell
git status --short

git add <exact_path_1>
git add <exact_path_2>

git commit -m "<exact commit message>"

git push origin main
```

Required forbidden command:

```powershell
git add .
```

Required statements:

```text
CommitCommandBlock is advice only.
The user executes commands manually.
The agent never mutates Git.
```

## 17. Required Stop Rules

Stop if the work packet or any output requires runtime activation, autonomous orchestration, automatic dispatch, automatic reviewer assignment, automatic integration, OpenCode integration, tool execution by AGENT PLATFORM, provider/auth/API/MCP, credentials, API/network/MCP calls, live connectors, Hermes runtime, GBrain runtime, Cadence, Graphify rerun/adoption, Codegraph execution/adoption, product/Siamese source, external source, GBrain source, raw Graphify output, source loading, validation/tests/CI/scripts/builds, security enforcement/scanners, persistence, vector DB, graph DB, generated-output tracking, source tracking expansion, publication, Git mutation by agent, `git add .`, or Cognitive Semantic System substrate selection.

## 18. Forbidden Content And Actions

Forbidden content:

- secrets
- credentials
- `.env` values
- provider configs
- token stores
- browser auth
- API keys
- local credential stores
- product/Siamese source
- external source contents
- GBrain source
- raw Graphify output
- generated artifacts unless explicitly in scope

Forbidden actions:

- runtime activation
- automatic dispatch
- automatic reviewer assignment
- automatic integration
- OpenCode internal integration
- provider/auth/API/MCP activation
- tool execution by AGENT PLATFORM
- agent execution
- Graphify rerun/adoption
- Codegraph execution/adoption
- validation/tests/scripts/builds/CI
- Git mutation by agent
- `git add .`

## 19. OpenCode H0 Usage Notes

OpenCode may be used manually by the user as an H0 external harness.

The user copies `HarnessInputPackage` text into OpenCode and returns output as `HarnessOutputPackage`. OpenCode is not integrated into AGENT PLATFORM. OpenCode is not activated as internal runtime. OpenCode output is proposed output only and must be reviewed before integration.

## 20. Reviewer Mesh Consumption Notes

The reviewer mesh consumes `ReviewInputPackage` and emits `ReviewVerdictPackage` metadata.

`ReviewRequest` is not automatic reviewer assignment. `ReviewerMesh` is metadata only. `ReviewVerdictPackage` is not final human approval, not runtime approval, and not Git approval.

## 21. Integrator Consumption Notes

The integrator consumes `HarnessOutputPackage`, `ReviewVerdictPackage`, `DriftRegister`, `AcceptedOutputRegister`, and `RejectedOutputRegister`.

The integrator produces `IntegrationSummary`, `CommitCandidate`, and `CommitCommandBlock` as manual synthesis and advice only. Integration is not automatic merge and not Git approval.

## 22. Git Advisory Rules

Git advice must use exact paths only.

Rejected paths must not be staged. Broad staging is forbidden. The agent never stages, commits, pushes, force-adds, publishes, or mutates Git. The user executes any Git commands manually.

Never recommend `git add .`.

## 23. Template Usage Example

Example pilot task:

```text
Create a small AGENT PLATFORM governance documentation artifact through OpenCode H0.
```

Example `WorkPacket` summary:

```text
work_packet_id: WP-P7-EXAMPLE-001
ticket_title: Small AGENT PLATFORM Governance Documentation Artifact
objective: Create one bounded governance documentation artifact.
scope: AGENT PLATFORM governance documentation only.
non_goals: No runtime, no product/Siamese source, no external source, no provider/API/MCP, no Graphify, no Codegraph, no Git mutation.
target_files: 0_architecture/governance/<exact_documentation_file>.md
blocked_files: product source, external source, generated artifacts, secrets, credentials
allowed_actions: create documentation-only markdown artifact
blocked_actions: runtime activation, source loading, tests, scripts, builds, provider calls, Git mutation
expected_output: HarnessOutputPackage with file register, decision register, blocker register, and limitations
review_required: true
integrator_required: true
git_advisory_expected: true
```

Example `HarnessInputPackage` summary:

```text
harness_input_package_id: HIP-P7-EXAMPLE-001
target_harness: OpenCode
harness_level: H0
manual_operator: user
work_packet_ref: WP-P7-EXAMPLE-001
allowed_context: P7 governance docs explicitly provided by user
blocked_context: product/Siamese source, external source, secrets, credentials
expected_response_format: HarnessOutputPackage
```

Example `CommitCommandBlock` advice pattern:

```powershell
git status --short

git add <exact_path_1>
git add <exact_path_2>

git commit -m "<exact commit message>"

git push origin main
```

The example is not product-bound and includes no product/Siamese source or external source.

## 24. Future Hardening Candidates

| Candidate | Purpose |
| --- | --- |
| P7.1-HARD-01 - WorkPacket Field Checklist | Validate required WorkPacket fields. |
| P7.1-HARD-02 - HarnessInputPackage Checklist | Validate H0 input safety. |
| P7.1-HARD-03 - HarnessOutputPackage Checklist | Validate returned output completeness. |
| P7.1-HARD-04 - ReviewVerdictPackage Checklist | Validate reviewer verdict completeness. |
| P7.1-HARD-05 - DriftRegister Checklist | Validate drift capture before integration. |
| P7.1-HARD-06 - CommitCandidate Checklist | Validate exact-path Git advice. |
| P7.1-HARD-07 - OpenCode H0 Prompt Template | Harden manual OpenCode prompt format. |
| P7.1-HARD-08 - Reviewer Mesh Intake Template | Harden review intake packaging. |
| P7.1-HARD-09 - Integrator Intake Template | Harden integration packaging. |
| P7.1-HARD-10 - P7.1.R Lessons Learned Checklist | Prepare audit checklist without starting P7.1.R. |

## 25. Final Verdict

This document creates the canonical manual OpenCode work packet interface template for P7.1-FIRST-PILOT.

It validates the textual interface for `WorkPacket`, `HarnessInputPackage`, `HarnessOutputPackage`, `ReviewInputPackage`, `ReviewVerdictPackage`, `IntegrationSummary`, `DriftRegister`, `AcceptedOutputRegister`, `RejectedOutputRegister`, `CommitCandidate`, and `CommitCommandBlock`.

It does not activate runtime, integrate OpenCode, execute tools, activate providers/auth/API/MCP, automate orchestration, dispatch automatically, assign reviewers automatically, integrate automatically, or mutate Git.
