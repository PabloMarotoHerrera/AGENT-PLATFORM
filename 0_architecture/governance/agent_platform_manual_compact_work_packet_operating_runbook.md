# Manual Compact Work Packet Operating Runbook

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Manual Compact Work Packet Operating Runbook |
| Ticket | P7.3 |
| Status | Accepted manual compact work packet operating runbook |
| Scope | Documentation-only operating runbook for compact WorkPacket -> OpenCode H0 -> review -> integrator -> Git advice workflow. |
| Authority | Runbook only, not runtime activation, not OpenCode integration, not tool execution, not provider/auth/API/MCP activation, not autonomous orchestration, not automatic dispatch, not automatic reviewer assignment, not automatic integration, not Git mutation. |

## 2. Purpose

This runbook gives the user a practical manual procedure for repeated AGENT PLATFORM documentation/governance tickets using `compact_documentation_mode`.

It explains how to move from Lead Chat / User Gateway to a Compact WorkPacket, Compact HarnessInputPackage, user-operated OpenCode H0 run, Compact HarnessOutputPackage, compact reviewer boundary drift review, compact integrator exact-path review, and user-owned Git advice.

This runbook does not activate runtime and does not integrate OpenCode into AGENT PLATFORM.

## 3. Current Posture

| Area | Current posture | Runbook interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM | Manual governance workflow. | Compact documentation tickets can use this runbook. | Runtime platform execution. |
| OpenCode | H0 user-operated harness. | User manually copies compact ticket text into OpenCode. | OpenCode integration, adapter, or internal runtime. |
| Reviewer | Compact boundary drift reviewer. | Manual checklist only. | Automatic reviewer assignment or auto-review. |
| Integrator | Compact exact-path reconciler. | Manual checklist and advisory CommitCandidate only. | Automatic integration or Git mutation. |
| Git | User-owned. | Exact-path command advice only. | Agent staging, commit, push, publication, or `git add .`. |

## 4. Operating Boundary

This runbook is for documentation-only governance work.

Allowed operating pattern:

```text
Lead Chat / User Gateway
-> Compact WorkPacket
-> Compact HarnessInputPackage
-> user manually copies ticket into OpenCode H0
-> OpenCode returns Compact HarnessOutputPackage
-> Compact Reviewer Boundary Drift Checklist
-> Compact Integrator Exact-Path Checklist
-> CommitCandidate / CommitCommandBlock
-> user performs Git manually
```

The workflow is manual-only. The user remains final execution authority and final Git authority.

## 5. When To Use Compact Documentation Mode

Use `compact_documentation_mode` for:

```text
small AGENT PLATFORM governance documentation task
small roadmap/planning documentation task
small review-only documentation task
small integrator-only documentation task
safe non-product planning note
```

Use compact mode only when the ticket has exact target files, no product/Siamese source, no external source inspection, no runtime/tool/provider/API/MCP scope, and no need for internal harness execution.

## 6. When To Stop Instead

Stop instead of proceeding if any of the following appear:

```text
product/Siamese source required
external source inspection required
runtime activation required
OpenCode internal integration required
OpenCode adapter required
provider/auth/API/MCP required
tool execution required
agent execution required
GBrain/Hermes/Cadence runtime required
Graphify/Codegraph execution or adoption required
persistence/vector DB/graph DB required
generated output tracking required
source tracking expansion required
publication required
Git mutation by agent required
`git add .` appears
```

If any stop condition appears, route to rework or governance escalation. Do not proceed through compact mode.

## 7. End-To-End Manual Workflow

| Step | Manual action | Output | Boundary |
| --- | --- | --- | --- |
| 1 | User states objective in Lead Chat / User Gateway. | Bounded objective. | No execution permission. |
| 2 | Lead Chat creates Compact WorkPacket. | Exact target files, allowed actions, blocked actions, stop rules. | WorkPacket is not runtime task. |
| 3 | Lead Chat creates Compact HarnessInputPackage. | Copy/paste ticket for OpenCode H0. | Not automatic dispatch. |
| 4 | User manually copies ticket into OpenCode. | H0 manual harness run. | No OpenCode integration. |
| 5 | User returns OpenCode output. | Compact HarnessOutputPackage. | Proposed output only. |
| 6 | Reviewer checks output. | Compact reviewer verdict. | Review is not Git approval. |
| 7 | Integrator reconciles accepted/rejected output. | Compact integrator checklist and CommitCandidate. | Advisory only. |
| 8 | User decides whether to run Git. | User-performed Git only. | Agent never mutates Git. |

## 8. User / Lead Chat Responsibilities

User responsibilities:

- Provide the objective and exact desired scope.
- Confirm target files.
- Manually operate OpenCode H0 if a harness is used.
- Manually return OpenCode output.
- Make final acceptance and Git decisions.

Lead Chat responsibilities:

- Convert objective into Compact WorkPacket and Compact HarnessInputPackage.
- Preserve blocked boundaries.
- Review returned output at the governance level.
- Produce exact-path Git advice only when appropriate.
- Stop on blocked scope.

## 9. OpenCode H0 Responsibilities

OpenCode H0 is a user-operated external harness.

Expected OpenCode behavior:

- Receive only the compact ticket text manually supplied by the user.
- Produce a Compact HarnessOutputPackage summary.
- Report files created, files modified, commands run, decisions, blockers, limitations, scope deviations, and boundary deviations.
- Avoid blocked actions and stop if blocked scope is required.

OpenCode H0 must not be treated as AGENT PLATFORM runtime, an internal adapter, a provider integration, an automatic dispatcher, a reviewer, an integrator, or a Git actor.

## 10. Compact WorkPacket Procedure

To create a Compact WorkPacket:

1. Write a single bounded objective.
2. List exact target files.
3. List blocked files and surfaces.
4. List allowed documentation-only actions.
5. List blocked actions.
6. Name required context.
7. Require Compact HarnessOutputPackage output.
8. Require review and integration.
9. Include stop, success, and failure criteria.

The Compact WorkPacket is manual instruction text. It is not a runtime task, automatic dispatch, source-inspection authority, or Git approval.

## 11. Compact HarnessInputPackage Procedure

To create a Compact HarnessInputPackage:

1. Set `target_harness` to OpenCode.
2. Set `harness_level` to H0.
3. Set `manual_operator` to user.
4. Include the ticket text.
5. Include allowed and blocked context.
6. Include exact allowed files.
7. Require Compact HarnessOutputPackage format.
8. Include stop rules.

The user manually copies this package into OpenCode. The package is not automatic dispatch and not OpenCode integration.

## 12. Compact HarnessOutputPackage Procedure

The returned output should use this compact checklist:

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

The Compact HarnessOutputPackage is proposed output only. It is not accepted by default, does not approve Git, and must be reviewed before integration.

## 13. Compact Reviewer Boundary Drift Procedure

Reviewer checks must cover:

- scope boundary
- target files
- blocked files
- runtime activation
- tool execution
- provider/auth/API/MCP
- product source
- external source
- GBrain/Hermes/Cadence
- Graphify/Codegraph
- persistence/vector/graph DB
- validation execution
- security enforcement
- Git mutation
- `git add .`
- reviewer verdict not Git approval

Allowed verdicts:

```text
accepted_for_integrator_review
accepted_with_limitations_for_integrator_review
needs_rework
blocked
out_of_scope
```

## 14. Compact Integrator Exact-Path Procedure

Integrator checks must confirm:

- accepted files have exact paths
- rejected files are excluded
- drift register exists
- review verdict exists
- commit scope matches accepted files
- commit message matches ticket scope
- Git add paths are exact
- no `git add .`
- user final Git authority is preserved

The integrator produces advisory output only. The integrator does not stage, commit, push, publish, or mutate Git.

## 15. Git Advisory Procedure

Use only this pattern:

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

Git advice is advisory only. The user executes commands manually.

## 16. Minimal Copy/Paste Ticket Skeleton

```text
# Compact WorkPacket / HarnessInputPackage

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
- tool execution by AGENT PLATFORM
- OpenCode integration or adapter
- Graphify/Codegraph execution or adoption
- GBrain/Hermes/Cadence runtime
- validation/tests/scripts/builds unless explicitly scoped
- security enforcement
- Git mutation by agent
- git add .

required_context:
- <docs or refs supplied by user>

expected_output:
- Summary
- Files created
- Files modified
- Files not created
- Commands run
- Decisions made
- Assumptions
- Blockers
- Limitations
- Scope deviations
- Boundary deviations
- Recommended next ticket
- Commit advice candidate

review_required: true
integrator_required: true

stop_rules:
- stop if blocked action is required
- stop if target file scope is unclear
- stop if secret/credential appears
- stop if git add . is recommended

success_criteria:
- exact target files created/modified
- no blocked behavior introduced

failure_criteria:
- blocked scope required
- git add . recommended
```

## 17. Minimal OpenCode Output Skeleton

```text
Summary:
Files created:
Files modified:
Files not created:
Commands run:
Decisions made:
Assumptions:
Blockers:
Limitations:
Scope deviations:
Boundary deviations:
Recommended next ticket:
Commit advice candidate:
```

## 18. Reviewer Checklist Skeleton

```text
scope_boundary_check:
target_file_check:
blocked_file_check:
runtime_activation_check:
tool_execution_check:
provider_auth_api_mcp_check:
product_source_check:
external_source_check:
gbrain_hermes_cadence_check:
graphify_codegraph_check:
persistence_vector_graph_db_check:
validation_execution_check:
security_enforcement_check:
git_mutation_check:
git_add_dot_check:
review_verdict_not_git_approval_check:

verdict:
accepted_for_integrator_review | accepted_with_limitations_for_integrator_review | needs_rework | blocked | out_of_scope
```

## 19. Integrator Checklist Skeleton

```text
accepted_files_exact_paths_present:
rejected_files_excluded:
drift_register_present:
review_verdict_present:
commit_scope_matches_accepted_files:
commit_message_matches_ticket_scope:
git_add_paths_exact:
no_git_add_dot:
user_final_git_authority_preserved:

commit_candidate:
advisory_only
```

## 20. Unsafe Output Handling

Unsafe output must be rejected or routed to governance escalation.

Unsafe signals include:

- `git add .`
- product/Siamese source inspection
- external source inspection
- provider/auth/API/MCP activation
- runtime activation
- OpenCode integration or adapter
- Graphify/Codegraph execution or adoption
- GBrain/Hermes/Cadence runtime
- persistence/vector DB/graph DB
- publication
- Git mutation by agent

If unsafe output appears, produce `ReviewVerdictPackage: blocked`, exclude rejected paths from CommitCandidate, and require rework or governance escalation.

## 21. Common Failure Modes

| Failure mode | Response |
| --- | --- |
| Target file unclear | Stop and ask user to clarify exact path. |
| OpenCode suggests `git add .` | Block output and require rework. |
| OpenCode asks to inspect product/Siamese source | Block output and require governance escalation. |
| Output modifies files outside target scope | Reject out-of-scope files. |
| Output omits file register | Request compact HarnessOutputPackage completion. |
| Review verdict is treated as Git approval | Stop and restore user Git authority. |
| Commit advice includes rejected paths | Remove rejected paths or block CommitCandidate. |

## 22. Practical Usage Rules

- Use compact mode for small documentation/governance tickets.
- Use full canonical mode for complex or high-risk work.
- Always name exact target files.
- Always name blocked files and blocked actions.
- Always require review and integration.
- Always require exact-path Git advice if Git advice is expected.
- Never treat OpenCode output as accepted by default.
- Never treat reviewer verdict as Git approval.
- Never stage rejected paths.
- Never recommend `git add .`.
- Stop on product/source/runtime/provider/tool/Git boundary drift.

## 23. Future Hardening Candidates

| Candidate | Purpose |
| --- | --- |
| P7.3-HARD-01 - Compact Ticket Timing Audit | Measure time cost of compact workflow. |
| P7.3-HARD-02 - OpenCode Output Compliance Checklist | Track whether OpenCode follows the compact output skeleton. |
| P7.3-HARD-03 - Reviewer Checklist Scoring | Add pass/fail scoring for boundary checks. |
| P7.3-HARD-04 - Integrator Checklist Scoring | Add pass/fail scoring for exact-path advice. |
| P7.3-HARD-05 - Unsafe Output Drill | Test blocked output handling in a future safe audit. |

## 24. Final Verdict

This runbook defines the practical manual operating procedure for compact documentation/governance tickets using OpenCode H0.

It supports repeated use of Compact WorkPacket, Compact HarnessInputPackage, Compact HarnessOutputPackage, Compact Reviewer Boundary Drift Checklist, Compact Integrator Exact-Path Checklist, and exact-path CommitCandidate / CommitCommandBlock.

It does not activate runtime, integrate OpenCode, execute tools, activate providers/auth/API/MCP, automate orchestration, dispatch automatically, assign reviewers automatically, integrate automatically, mutate Git, inspect product/source, or approve publication.
