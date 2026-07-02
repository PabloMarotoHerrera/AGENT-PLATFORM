# I-06 - Tool Execution Boundary

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Tool Execution Boundary |
| Ticket | I-06 |
| Status | Accepted minimal tool execution boundary implementation |
| Date | 2026-07-02 |
| Scope | Create the first minimal governed tool execution boundary metadata layer for AGENT PLATFORM / Siamese. |
| Authority | Minimal tool execution boundary metadata layer only, not tool execution or runtime activation. |
| Related documents | I-00, I-01, I-02, I-03, I-04, I-05, IR-A, IR-05, IR-06, S-series, V-series, H-series, W-series agent operating rules, P-A, `.gitignore`, README.md, Siamese Product Vision |
| Implementation target | Exact tool execution boundary files under `3_platform/_governed_skeleton/tools/execution_boundary/` |

## 2. Purpose
I-00 created only the governed skeleton. I-01 added a metadata-only validation registry. I-02 added a metadata-only security/access evaluator. I-03 added a metadata-only context pack runtime. I-04 added a metadata-only provider/adapter layer. I-05 added a metadata-only agent runtime boundary. I-06 adds the first minimal tool execution boundary metadata layer. I-06 does not activate tools. I-06 does not execute tools. I-06 does not execute shell/subprocess commands. I-06 does not start I-07.

## 3. Tool Execution Boundary Definition
A Tool Execution Boundary is a minimal in-memory metadata layer for tool descriptors, tool capabilities, execution requests, execution decisions, blockers, limitations, evidence references, and review posture.

Tool registration is not tool activation. Tool capability metadata is not tool permission. Execution request creation is not execution approval. Execution decision metadata is not execution authorization. Shell availability is not command approval. Tool availability is not permission. Provider/adapter refs are not provider/adapter activation. MCP refs are not MCP activation. Metadata boundary is not runtime executor.

## 4. Decision Summary
Create exact tool execution boundary implementation files only. Create one pure Python module. Create no package manifests. Create no tests. Create no runtime service. Create no scheduler. Create no persistence. Create no dependencies. Preserve source tracking boundaries. Preserve tool/shell/filesystem/network/provider/API/MCP activation blockers. Preserve existing `3_platform` sibling quarantine. I-07 may proceed only after explicit instruction.

## 5. Authority Boundary
| actor | authority |
| --- | --- |
| Governance | Decides tool execution, runtime expansion, publication, source tracking, dependency adoption, product activation, and lifecycle. |
| Security | Constrains credentials, local-only content, shell/filesystem/network/tool execution, providers, MCP, and data exposure. |
| Validation | Evaluates evidence. |
| Tool execution boundary | Records metadata only. |
| Git | Records artifacts but does not approve tool status or execution. |
| Agent | Cannot stage, commit, push, execute, install, publish, authenticate, call providers, execute tools, run shell commands, or start I-07. |

## 6. Source Boundary
I-00 skeleton is the implementation base. I-01 registry remains metadata-only. I-02 evaluator remains metadata-only. I-03 context runtime remains metadata-only. I-04 provider/adapter layer remains metadata-only. I-05 agent runtime boundary remains metadata-only. IR-A blockers remain inherited. IR-05 provides runtime/agent/context boundaries. IR-06 provides provider/adapter/MCP activation boundaries. H-series provides harness/provider/tool/MCP boundaries. W-series agent operating rules provide tool approval boundaries. S-series provides local-only/security/access/tool/shell/network boundaries. V-series provides evidence/proof boundaries. Raw `3_platform` siblings are not inspected. Product source remains local-only. Secrets and credentials are not inspected.

## 7. Exact Target Scope
Files created: `0_architecture/implementation/agent_platform_tool_execution_boundary.md`, `3_platform/_governed_skeleton/tools/execution_boundary/README.md`, `3_platform/_governed_skeleton/tools/execution_boundary/TOOL_EXECUTION_BOUNDARY.md`, `3_platform/_governed_skeleton/tools/execution_boundary/TOOL_EXECUTION_CONTRACT.md`, and `3_platform/_governed_skeleton/tools/execution_boundary/tool_execution_boundary.py`.

Directory created only as needed: `3_platform/_governed_skeleton/tools/execution_boundary/`. No sibling paths are in scope.

## 8. Implementation File Contract
`tool_execution_boundary.py` contains one minimal import-side-effect-free Python standard-library module. It may define tool kinds, activation statuses, risk levels, request statuses, decision statuses, tool descriptors, capability descriptors, execution requests, execution decisions, and an in-memory boundary. It must not persist files, read files, write files, access process variables, call network, spawn processes, import external packages, approve governance decisions, activate tools, execute tools, execute shell, activate providers/APIs/MCP, execute validation, enforce security, or inspect credentials.

## 9. Tool Descriptor Contract
Required fields are `tool_id`, `name`, `tool_kind`, `description`, `activation_status`, `allowed_scope`, `forbidden_scope`, `side_effects`, `filesystem_required`, `shell_required`, `network_required`, `credential_required`, `provider_refs`, `adapter_refs`, `mcp_refs`, `evidence_refs`, `limitations`, `blockers`, `created_at`, and `review_required`. Tool kinds include metadata, validation, security, context, agent metadata, provider/adapter metadata, shell, filesystem, Git, package manager, build, test runner, network, provider API, MCP, product, simulation, and unknown tools. Risky flags and side effects require review and blockers.

## 10. Tool Capability Contract
Required fields are `capability_id`, `tool_id`, `name`, `description`, `activation_status`, `input_classes`, `output_classes`, `side_effects`, `filesystem_behavior`, `shell_behavior`, `network_behavior`, `credential_behavior`, `provider_behavior`, `mcp_behavior`, `evidence_refs`, `limitations`, `blockers`, `created_at`, and `review_required`. Capability registration is metadata only and not tool permission. Non-metadata behavior or side effects require review and blockers.

## 11. Tool Execution Request Contract
Required fields are `request_id`, `tool_id`, `capability_id`, `requested_by`, `target_id`, `intent`, `input_summary`, `risk_level`, `status`, `context_pack_refs`, `validation_refs`, `security_decision_refs`, `agent_task_refs`, `provider_adapter_refs`, `evidence_refs`, `limitations`, `blockers`, `created_at`, and `review_required`. Request statuses are draft, proposed for review, blocked, needs review, rejected for scope, and recorded metadata only. Input summaries are summaries only, not raw payloads, secrets, credentials, or source contents. Execution request creation is not execution approval.

## 12. Tool Execution Decision Contract
Required fields are `decision_id`, `request_id`, `status`, `reasons`, `risk_level`, `limitations`, `blockers`, `evidence_refs`, `created_by`, `created_at`, and `review_required`. Decision statuses are metadata recorded only, execution not approved, blocked, needs review, and rejected for scope. `execution_not_approved` is the safe default. Decision metadata is not execution authorization.

## 13. Documentation File Contract
`README.md` describes purpose, current status, representable metadata, non-approval boundaries, IR-06 relationship, agent operating rules relationship, validation registry relationship, security/access evaluator relationship, context pack runtime relationship, provider/adapter layer relationship, agent runtime boundary relationship, product relationship, Git/source tracking relationship, future route, and stop rules. `TOOL_EXECUTION_BOUNDARY.md` describes allowed and forbidden implementation. `TOOL_EXECUTION_CONTRACT.md` describes tool, capability, request, and decision contracts.

## 14. Source Tracking / Git Boundary
Only exact I-06-created files may be considered for exact-path staging after human review. No broad source tracking is approved. Existing `3_platform` sibling contents remain not trackable. `.gitignore` is unchanged. No force-add is authorized. No `git add .`.

## 15. Dependency Boundary
No dependencies are adopted. No package manifests are created. No lockfiles are created. No package managers are run. Pure Python standard library only. Tool frameworks, automation frameworks, package managers, build systems, test runners, shell wrappers, and SDKs are not adopted.

## 16. Security / Credential Boundary
No credential reading occurs. No auth flow occurs. No provider config is created. No tool credential is used. Credential, provider, and tool refs are metadata IDs only. Tools requiring credentials, filesystem, shell, network, providers, MCP, Git mutation, package managers, builds, tests, products, or side effects require review and blockers.

## 17. Runtime / Execution Boundary
No runtime service, scheduler, worker loop, queue, orchestration engine, tool execution, shell execution, subprocess execution, filesystem action, network action, Git mutation, package manager execution, build execution, or test execution is created.

## 18. Network / Provider / API / MCP Boundary
No network is used. No API calls occur. No provider activation occurs. No adapter activation occurs. No MCP activation occurs. No MCP tool execution occurs. Provider, adapter, and MCP refs are metadata only.

## 19. Validation Boundary
No validation execution occurs. No validation/security enforcement runtime is created. Tool metadata, requests, and decisions may be represented later in the validation registry as metadata only.

## 20. Agent Boundary
Agent task refs are metadata only. Agent registration is not agent activation. Tool refs in agent metadata are not tool execution approval. No agent task execution occurs.

## 21. Context Boundary
Context pack refs are metadata only. Context inclusion is not permission. No context source loading occurs. No local-only, raw source, secrets, or credentials are included.

## 22. Cognitive Semantic System Boundary
Cognitive Semantic System name remains accepted. Substrate remains deferred. Graph remains candidate only. Graphify remains evidence only, not authority. The tool execution boundary does not decide substrate.

## 23. Product Boundary
Products remain inactive. Product source remains local-only. Product tool metadata may be represented later as metadata only. Product tools are not executed or activated. EnergyPlus, OpenStudio, Omniverse, Nucleus, Web, Desktop, and CLI product tools are not activated.

## 24. Created Files Register
| file | type | purpose | contains code? | executable? | dependency impact? | future owner |
| --- | --- | --- | --- | --- | --- | --- |
| `0_architecture/implementation/agent_platform_tool_execution_boundary.md` | Markdown | I-06 record | no | no | none | governance/tools |
| `3_platform/_governed_skeleton/tools/execution_boundary/README.md` | Markdown | boundary overview | no | no | none | tools |
| `3_platform/_governed_skeleton/tools/execution_boundary/TOOL_EXECUTION_BOUNDARY.md` | Markdown | boundary rules | no | no | none | tools/security |
| `3_platform/_governed_skeleton/tools/execution_boundary/TOOL_EXECUTION_CONTRACT.md` | Markdown | record contract | no | no | none | tools |
| `3_platform/_governed_skeleton/tools/execution_boundary/tool_execution_boundary.py` | Python | in-memory tool boundary metadata layer | yes | no runtime service | stdlib only | tools |

## 25. Non-created Artifacts Register
| artifact | status | future route |
| --- | --- | --- |
| tool executor | not created | future execution gate |
| shell runner | not created | shell approval gate |
| filesystem guard | not created | filesystem/security gate |
| network client | not created | network/API gate |
| provider client | not created | activation/dependency gate |
| API client | not created | activation gate |
| MCP server/config | not created | MCP gate |
| credential store | not created | security gate |
| package manager wrapper | not created | dependency gate |
| build runner | not created | build gate |
| test runner | not created | test gate |
| Git mutation wrapper | not created | Git gate |
| runtime service | not created | runtime gate |
| tests | not created | future test gate |
| scripts/tools | not created | future tool gate |
| CI | not created | future CI gate |
| package manifests | not created | dependency gate |
| product source | not copied | product governance |
| CSS prototype | not created | CSS governance and I-07 |

## 26. I-06 Gate Checklist
| gate | pass condition | current result | blocker if failed |
| --- | --- | --- | --- |
| I-00 exists | skeleton record exists | pass | stop |
| I-01 exists | registry record exists | pass | stop |
| I-02 exists | security/access record exists | pass | stop |
| I-03 exists | context runtime record exists | pass | stop |
| I-04 exists | provider/adapter record exists | pass | stop |
| I-05 exists | agent boundary record exists | pass | stop |
| exact target files absent before creation | no overwrite | pass | stop |
| exact tool execution boundary path under governed skeleton | path is scoped | pass | stop |
| Python stdlib only | module imports stdlib only | pass | stop |
| no package manifests | none created | pass | stop |
| no tests | none created | pass | stop |
| no execution | no module/tool/shell/test execution | pass | stop |
| no dependencies adopted | none adopted | pass | stop |
| no credentials inspected | none inspected | pass | stop |
| no tool or shell execution | none performed | pass | stop |
| no filesystem read/write | none performed | pass | stop |
| no network/API call | none performed | pass | stop |
| no provider/API/MCP activation | none activated | pass | stop |
| no existing `3_platform` sibling approval | siblings uninspected/unapproved | pass | stop |
| I-07 not started | no I-07 artifact | pass | stop |

## 27. Residual Risk Register
| risk | severity | mitigation | route |
| --- | --- | --- | --- |
| no tool executor | blocker | keep metadata-only scope explicit | future execution gate |
| no shell runner | blocker | shell approval gate | future |
| no filesystem guard | blocker | security gate | future |
| no network client | blocker | network gate | future |
| no provider/API/MCP integration | blocker | activation gate | future |
| no credential store | blocker | security gate | future |
| no tests | major_gap | future test gate | future |
| no persistence | major_gap | keep in-memory scope explicit | future persistence gate |
| no dependency review for future expansion | blocker | dependency gate | future |
| no source tracking broad approval | blocker | exact-path review only | governance |
| existing `3_platform` siblings unknown | blocker | keep quarantine | future classification |
| product tools inactive | blocker | product governance | future |
| CSS substrate deferred | blocker | CSS governance | I-07 |

## 28. Blocker Register
| blocker | stop behavior | required future action | blocks broad implementation? |
| --- | --- | --- | --- |
| need tool execution | stop | execution gate | yes |
| need shell/subprocess execution | stop | shell approval | yes |
| need filesystem access | stop | filesystem/security gate | yes |
| need network/API call | stop | network/API approval | yes |
| need provider/API/MCP activation | stop | activation gate | yes |
| need credential access | stop | security approval | yes |
| need Git mutation | stop | Git approval | yes |
| need package manager/build/test execution | stop | execution approval | yes |
| need tests | stop | test gate | yes |
| need persistence | stop | persistence gate | yes |
| need dependency | stop | dependency review | yes |
| need source tracking beyond exact files | stop | tracking gate | yes |
| need product tool execution | stop | product governance | yes |
| need CSS substrate | stop | CSS governance | yes |
| I-07 scope pressure | stop | finish I-06 only | yes |

## 29. Incident Handling
Incidents include target overwrite, dependency import, file/network/process-variable access, credential inspection, auth flow, API/network call, provider activation, adapter activation, MCP activation, tool execution, shell/subprocess execution, filesystem read/write, Git mutation, package manager execution, build/test execution, package manifest creation, test execution, product source inspection, existing `3_platform` inspection, Git mutation, or I-07 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 30. I-06 Invariants
| id | invariant |
| --- | --- |
| I06-001 | Tool execution boundary is metadata-only. |
| I06-002 | Tool registration is not tool activation. |
| I06-003 | Capability registration is not tool permission. |
| I06-004 | Execution request creation is not execution approval. |
| I06-005 | Execution decision metadata is not execution authorization. |
| I06-006 | Shell availability is not command approval. |
| I06-007 | Tool availability is not permission. |
| I06-008 | Provider/adapter/MCP refs are metadata only. |
| I06-009 | No external dependencies are adopted. |
| I06-010 | No package manifests or lockfiles are created. |
| I06-011 | No tests/scripts/tools/CI are created. |
| I06-012 | No provider/API/MCP activation occurs. |
| I06-013 | No tool/shell/subprocess execution occurs. |
| I06-014 | Existing 3_platform contents remain uninspected and unapproved. |
| I06-015 | Product source remains local-only. |
| I06-016 | Cognitive Semantic System substrate remains deferred. |
| I06-017 | Validation evaluates; governance decides. |
| I06-018 | I-06 stops before I-07. |

## 31. Anti-patterns
Anti-patterns: tool metadata as tool activation; capability metadata as tool permission; execution request as execution approval; decision metadata as execution authorization; shell availability as command approval; tool availability as permission; provider/adapter ref as provider activation; MCP ref as MCP activation; package manager metadata as dependency adoption; product tool metadata as product activation; package manifest as harmless; existing `3_platform` as approved source; starting I-07 inside I-06; `git add .`.

## 32. Readiness For I-07
I-07 - Cognitive Semantic System Prototype is ready after explicit instruction if I-06 tool execution boundary exists; only exact I-06 files were created; layer is metadata-only and in-memory; no tool, shell, subprocess, filesystem, or network execution occurred; no provider/API/MCP activation occurred; no network/auth/credential use occurred; no dependencies were adopted; no source tracking was broadly approved; existing `3_platform` contents remain uninspected and unapproved; and no product activation, CSS substrate decision, publication, Git mutation, or broad implementation is implied.

Do not create I-07.

## 33. Final Verdict
I-06 created the exact architecture record, tool execution boundary documentation, tool execution contract, and one minimal pure-stdlib in-memory tool execution boundary metadata layer. I-06 did not activate tools. I-06 did not execute tools. I-06 did not run shell/subprocess commands. I-06 did not read or write files. I-06 did not call APIs or network. I-06 did not authenticate or inspect credentials. I-06 did not activate providers/adapters/MCP. I-06 did not create package manifests or lockfiles. I-06 did not adopt dependencies. I-06 did not create tests, scripts, tools, or CI. I-06 did not approve source tracking broadly. I-06 did not inspect or approve existing `3_platform` contents. I-06 did not decide CSS substrate.

Blocked items remain: tool execution, shell/subprocess execution, filesystem access, network/API calls, provider/API/MCP activation, credential access, Git mutation, package manager/build/test execution, tests, persistence, dependency adoption, package manifests, source tracking beyond exact files, product tool execution, product activation, existing `3_platform` approval, CSS substrate decision, publication, staging, commit, push, and I-07. I-07 is ready after explicit instruction only.
