# I-05 - Agent Runtime Boundary

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Agent Runtime Boundary |
| Ticket | I-05 |
| Status | Accepted minimal agent runtime boundary implementation |
| Date | 2026-07-02 |
| Scope | Create the first minimal governed agent runtime boundary metadata layer for AGENT PLATFORM / Siamese. |
| Authority | Minimal agent runtime boundary metadata layer only, not agent execution or runtime activation. |
| Related documents | I-00, I-01, I-02, I-03, I-04, IR-A, IR-05, IR-06, S-series, V-series, H-series, W-series agent operating rules, P-A, `.gitignore`, README.md, Siamese Product Vision |
| Implementation target | Exact agent runtime boundary files under `3_platform/_governed_skeleton/agents/runtime_boundary/` |

## 2. Purpose
I-00 created only the governed skeleton. I-01 added a metadata-only validation registry. I-02 added a metadata-only security/access evaluator. I-03 added a metadata-only context pack runtime. I-04 added a metadata-only provider/adapter layer. I-05 adds the first minimal agent runtime boundary metadata layer. I-05 does not activate agents, execute tasks, execute handoffs, execute tools, or start I-06.

## 3. Agent Runtime Boundary Definition
An Agent Runtime Boundary is a minimal in-memory metadata layer for agent descriptors, agent capabilities, task envelopes, handoff records, activation blockers, limitations, evidence references, and review posture.

Agent registration is not agent activation. Task envelope creation is not task execution. Handoff record creation is not handoff execution. Capability metadata is not tool permission. Agent metadata is not runtime readiness. Provider/adapter refs are not provider/adapter activation. Tool refs are not tool execution approval. Orchestration metadata is not orchestration runtime.

## 4. Decision Summary
Create exact agent runtime boundary implementation files only. Create one pure Python module. Create no package manifests. Create no tests. Create no runtime service. Create no scheduler. Create no persistence. Create no dependencies. Preserve source tracking boundaries. Preserve agent/tool/provider/API/MCP activation blockers. Preserve existing `3_platform` sibling quarantine. I-06 may proceed only after explicit instruction.

## 5. Authority Boundary
| actor | authority |
| --- | --- |
| Governance | Decides agent activation, tool execution, runtime expansion, publication, source tracking, product activation, and lifecycle. |
| Security | Constrains credentials, local-only content, tool execution, network, providers, MCP, and data exposure. |
| Validation | Evaluates evidence. |
| Agent runtime boundary | Records metadata only. |
| Git | Records artifacts but does not approve agent status. |
| Agent | Cannot stage, commit, push, execute, install, publish, authenticate, call providers, execute tools, or start I-06. |

## 6. Source Boundary
I-00 skeleton is the implementation base. I-01 registry remains metadata-only. I-02 evaluator remains metadata-only. I-03 context runtime remains metadata-only. I-04 provider/adapter layer remains metadata-only. IR-A blockers remain inherited. IR-05 provides runtime/agent/context boundaries. IR-06 provides provider/adapter/MCP activation boundaries. H-series provides harness/provider/tool/MCP boundaries. W-series agent operating rules provide agent behavior boundaries. S-series provides local-only/security/access boundaries. V-series provides evidence/proof boundaries. Raw `3_platform` siblings are not inspected. Product source remains local-only. Secrets and credentials are not inspected.

## 7. Exact Target Scope
Files created: `0_architecture/implementation/agent_platform_agent_runtime_boundary.md`, `3_platform/_governed_skeleton/agents/runtime_boundary/README.md`, `3_platform/_governed_skeleton/agents/runtime_boundary/AGENT_RUNTIME_BOUNDARY.md`, `3_platform/_governed_skeleton/agents/runtime_boundary/AGENT_RUNTIME_CONTRACT.md`, and `3_platform/_governed_skeleton/agents/runtime_boundary/agent_runtime_boundary.py`.

Directory created only as needed: `3_platform/_governed_skeleton/agents/runtime_boundary/`. No sibling paths are in scope.

## 8. Implementation File Contract
`agent_runtime_boundary.py` contains one minimal import-side-effect-free Python standard-library module. It may define agent kinds, activation statuses, task statuses, handoff statuses, agent descriptors, capability descriptors, task envelopes, handoff records, and an in-memory boundary. It must not persist files, read files, write files, access process variables, call network, spawn processes, import external packages, approve governance decisions, activate agents, execute tasks, execute handoffs, execute tools, activate providers/APIs/MCP, execute validation, enforce security, or inspect credentials.

## 9. Agent Descriptor Contract
Required fields are `agent_id`, `name`, `agent_kind`, `description`, `activation_status`, `allowed_scope`, `forbidden_scope`, `provider_refs`, `adapter_refs`, `tool_refs`, `context_pack_refs`, `evidence_refs`, `limitations`, `blockers`, `created_at`, and `review_required`. Agent kinds include governance, validation, security, context, provider adapter, tool boundary, product, implementation, review, orchestration, and unknown agents. Provider, adapter, tool, and context refs are metadata references only. Agents with provider refs, adapter refs, tool refs, or orchestration scope require review and blockers.

## 10. Agent Capability Contract
Required fields are `capability_id`, `agent_id`, `name`, `description`, `activation_status`, `input_classes`, `output_classes`, `side_effects`, `tool_required`, `provider_required`, `context_required`, `evidence_refs`, `limitations`, `blockers`, `created_at`, and `review_required`. Capability registration is metadata only and not tool permission. Side effects, tools, providers, or context requirements require review and blockers.

## 11. Agent Task Envelope Contract
Required fields are `task_id`, `agent_id`, `target_id`, `intent`, `status`, `context_pack_refs`, `validation_refs`, `security_decision_refs`, `provider_adapter_refs`, `tool_refs`, `blockers`, `limitations`, `created_by`, `created_at`, and `review_required`. Task statuses are draft, proposed for review, blocked, needs review, rejected for scope, and recorded metadata only. Task envelope creation is not task execution.

## 12. Agent Handoff Record Contract
Required fields are `handoff_id`, `from_agent_id`, `to_agent_id`, `task_id`, `reason`, `status`, `context_pack_refs`, `evidence_refs`, `blockers`, `limitations`, `created_at`, and `review_required`. Handoff statuses are draft, proposed for review, blocked, needs review, rejected for scope, and recorded metadata only. Handoff record creation is not handoff execution.

## 13. Documentation File Contract
`README.md` describes purpose, current status, representable metadata, non-approval boundaries, IR-05 relationship, agent operating rules relationship, validation registry relationship, security/access evaluator relationship, context pack runtime relationship, provider/adapter layer relationship, product relationship, Git/source tracking relationship, future route, and stop rules. `AGENT_RUNTIME_BOUNDARY.md` describes allowed and forbidden implementation. `AGENT_RUNTIME_CONTRACT.md` describes records, statuses, reference rules, evidence rules, blocker rules, limitation rules, review rule, and non-activation/non-execution semantics.

## 14. Source Tracking / Git Boundary
Only exact I-05-created files may be considered for exact-path staging after human review. No broad source tracking is approved. Existing `3_platform` sibling contents remain not trackable. `.gitignore` is unchanged. No force-add is authorized. No `git add .`.

## 15. Dependency Boundary
No dependencies are adopted. No package manifests are created. No lockfiles are created. No package managers are run. Pure Python standard library only. Agent frameworks, orchestration frameworks, workflow engines, queues, and schedulers are not adopted.

## 16. Security / Credential Boundary
No credential reading occurs. No auth flow occurs. No provider config is created. No tool credential is used. Credential, provider, and tool refs are metadata IDs only. Agents requiring credentials, tools, providers, network, or side effects require review and blockers.

## 17. Runtime / Execution Boundary
No runtime service, scheduler, worker loop, queue, orchestration engine, agent execution, task execution, handoff execution, or tool execution is created.

## 18. Network / Provider / API / MCP Boundary
No network is used. No API calls occur. No provider activation occurs. No adapter activation occurs. No MCP activation occurs. No tool execution occurs. Provider, adapter, and MCP refs are metadata only.

## 19. Validation Boundary
No validation execution occurs. No validation/security enforcement runtime is created. Agent, task, and handoff metadata may be represented later in the validation registry as metadata only.

## 20. Context Boundary
Context pack refs are metadata only. Context inclusion is not permission. No context source loading occurs. No local-only, raw source, secrets, or credentials are included.

## 21. Cognitive Semantic System Boundary
Cognitive Semantic System name remains accepted. Substrate remains deferred. Graph remains candidate only. Graphify remains evidence only, not authority. The agent runtime boundary does not decide substrate.

## 22. Product Boundary
Products remain inactive. Product source remains local-only. Product agent metadata may be represented later as metadata only. Product agents are not executed or activated. EnergyPlus, OpenStudio, Omniverse, Nucleus, Web, Desktop, and CLI product agents are not activated.

## 23. Created Files Register
| file | type | purpose | contains code? | executable? | dependency impact? | future owner |
| --- | --- | --- | --- | --- | --- | --- |
| `0_architecture/implementation/agent_platform_agent_runtime_boundary.md` | Markdown | I-05 record | no | no | none | governance/agents |
| `3_platform/_governed_skeleton/agents/runtime_boundary/README.md` | Markdown | boundary overview | no | no | none | agents |
| `3_platform/_governed_skeleton/agents/runtime_boundary/AGENT_RUNTIME_BOUNDARY.md` | Markdown | boundary rules | no | no | none | agents/security |
| `3_platform/_governed_skeleton/agents/runtime_boundary/AGENT_RUNTIME_CONTRACT.md` | Markdown | record contract | no | no | none | agents |
| `3_platform/_governed_skeleton/agents/runtime_boundary/agent_runtime_boundary.py` | Python | in-memory agent boundary metadata layer | yes | no runtime service | stdlib only | agents |

## 24. Non-created Artifacts Register
| artifact | status | future route |
| --- | --- | --- |
| agent runtime | not created | runtime gate |
| scheduler | not created | scheduler gate |
| worker loop | not created | runtime gate |
| queue | not created | runtime gate |
| orchestration engine | not created | orchestration gate |
| tool executor | not created | I-06 after instruction |
| provider client | not created | activation/dependency gate |
| API client | not created | activation gate |
| MCP server/config | not created | MCP gate |
| credential store | not created | security gate |
| tests | not created | future test gate |
| scripts/tools | not created | future tool gate |
| CI | not created | future CI gate |
| package manifests | not created | dependency gate |
| product source | not copied | product governance |
| CSS prototype | not created | CSS governance and I-07 |

## 25. I-05 Gate Checklist
| gate | pass condition | current result | blocker if failed |
| --- | --- | --- | --- |
| I-00 exists | skeleton record exists | pass | stop |
| I-01 exists | registry record exists | pass | stop |
| I-02 exists | security/access record exists | pass | stop |
| I-03 exists | context runtime record exists | pass | stop |
| I-04 exists | provider/adapter record exists | pass | stop |
| exact target files absent before creation | no overwrite | pass | stop |
| exact agent runtime boundary path under governed skeleton | path is scoped | pass | stop |
| Python stdlib only | module imports stdlib only | pass | stop |
| no package manifests | none created | pass | stop |
| no tests | none created | pass | stop |
| no execution | no module/agent/tool/test execution | pass | stop |
| no dependencies adopted | none adopted | pass | stop |
| no credentials inspected | none inspected | pass | stop |
| no agent/task/handoff/tool execution | none performed | pass | stop |
| no provider/API/MCP activation | none activated | pass | stop |
| no existing `3_platform` sibling approval | siblings uninspected/unapproved | pass | stop |
| I-06 not started | no I-06 artifact | pass | stop |

## 26. Residual Risk Register
| risk | severity | mitigation | route |
| --- | --- | --- | --- |
| no agent runtime | blocker | keep metadata-only scope explicit | runtime gate |
| no scheduler | blocker | scheduler gate | future |
| no orchestration engine | blocker | orchestration gate | future |
| no tool execution | blocker | route to I-06 | I-06 |
| no provider/API/MCP integration | blocker | activation gate | future |
| no credential store | blocker | security gate | future |
| no tests | major_gap | future test gate | future |
| no persistence | major_gap | keep in-memory scope explicit | future persistence gate |
| no dependency review for future expansion | blocker | dependency gate | future |
| no source tracking broad approval | blocker | exact-path review only | governance |
| existing `3_platform` siblings unknown | blocker | keep quarantine | future classification |
| product agents inactive | blocker | product governance | future |
| CSS substrate deferred | blocker | CSS governance | I-07 |

## 27. Blocker Register
| blocker | stop behavior | required future action | blocks broad implementation? |
| --- | --- | --- | --- |
| need agent activation | stop | activation gate | yes |
| need task execution | stop | runtime gate | yes |
| need handoff execution | stop | handoff gate | yes |
| need tool execution | stop | I-06 instruction | yes |
| need provider/API/MCP activation | stop | activation gate | yes |
| need credential access | stop | security approval | yes |
| need network/API call | stop | activation approval | yes |
| need tests | stop | test gate | yes |
| need persistence | stop | persistence gate | yes |
| need dependency | stop | dependency review | yes |
| need source tracking beyond exact files | stop | tracking gate | yes |
| need product agent execution | stop | product governance | yes |
| need CSS substrate | stop | CSS governance | yes |
| I-06 scope pressure | stop | finish I-05 only | yes |

## 28. Incident Handling
Incidents include target overwrite, dependency import, file/network/process-variable access, credential inspection, auth flow, API/network call, provider activation, adapter activation, MCP activation, tool execution, agent execution, task execution, handoff execution, package manifest creation, test execution, product source inspection, existing `3_platform` inspection, Git mutation, or I-06 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 29. I-05 Invariants
| id | invariant |
| --- | --- |
| I05-001 | Agent runtime boundary is metadata-only. |
| I05-002 | Agent registration is not agent activation. |
| I05-003 | Task envelope creation is not task execution. |
| I05-004 | Handoff record creation is not handoff execution. |
| I05-005 | Capability registration is not tool permission. |
| I05-006 | Provider/adapter refs are metadata only. |
| I05-007 | Tool refs are metadata only. |
| I05-008 | No external dependencies are adopted. |
| I05-009 | No package manifests or lockfiles are created. |
| I05-010 | No tests/scripts/tools/CI are created. |
| I05-011 | No provider/API/MCP activation occurs. |
| I05-012 | No tool execution occurs. |
| I05-013 | Existing 3_platform contents remain uninspected and unapproved. |
| I05-014 | Product source remains local-only. |
| I05-015 | Cognitive Semantic System substrate remains deferred. |
| I05-016 | Validation evaluates; governance decides. |
| I05-017 | I-05 stops before I-06. |

## 30. Anti-patterns
Anti-patterns: agent metadata as agent activation; task envelope as task execution; handoff record as handoff execution; capability metadata as tool permission; tool ref as tool execution approval; provider/adapter ref as provider activation; orchestration metadata as orchestration runtime; agent need as dependency adoption; product agent metadata as product activation; package manifest as harmless; existing `3_platform` as approved source; starting I-06 inside I-05; `git add .`.

## 31. Readiness For I-06
I-06 - Tool Execution Boundary is ready after explicit instruction if I-05 agent runtime boundary exists; only exact I-05 files were created; layer is metadata-only and in-memory; no agent, task, handoff, or tool execution occurred; no provider/API/MCP activation occurred; no network/auth/credential use occurred; no dependencies were adopted; no source tracking was broadly approved; existing `3_platform` contents remain uninspected and unapproved; and no product activation, CSS substrate decision, publication, Git mutation, or broad implementation is implied.

Do not create I-06.

## 32. Final Verdict
I-05 created the exact architecture record, agent runtime boundary documentation, agent runtime contract, and one minimal pure-stdlib in-memory agent runtime boundary metadata layer. I-05 did not activate agents. I-05 did not execute tasks. I-05 did not execute handoffs. I-05 did not execute tools. I-05 did not call APIs or network. I-05 did not authenticate or inspect credentials. I-05 did not activate providers/adapters/MCP. I-05 did not create package manifests or lockfiles. I-05 did not adopt dependencies. I-05 did not create tests, scripts, tools, or CI. I-05 did not approve source tracking broadly. I-05 did not inspect or approve existing `3_platform` contents. I-05 did not decide CSS substrate.

Blocked items remain: agent activation, task execution, handoff execution, tool execution, provider/API/MCP activation, credential access, network/API calls, tests, persistence, dependency adoption, package manifests, source tracking beyond exact files, product agent execution, product activation, existing `3_platform` approval, CSS substrate decision, publication, staging, commit, push, and I-06. I-06 is ready after explicit instruction only.
