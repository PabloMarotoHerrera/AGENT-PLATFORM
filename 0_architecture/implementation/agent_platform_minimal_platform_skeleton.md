# I-00 - Minimal Platform Skeleton

## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Minimal Platform Skeleton |
| Ticket | I-00 |
| Status | Accepted minimal platform skeleton |
| Date | 2026-07-02 |
| Scope | Create only the exact governed Markdown skeleton for AGENT PLATFORM / Siamese. |
| Authority | Minimal skeleton creation only, not broad implementation approval. |
| Related documents | IR-A, IR-00 through IR-08, P-A, P-00 through P-10, W-series, V-series, S-series, CSS-series, H-series, `.gitignore`, `README.md`, Siamese Product Vision |
| Implementation target | Exact governed skeleton under `3_platform/_governed_skeleton/` |

## 2. Purpose
IR-A closed FASE 5 at documentation/readiness-planning level only. IR-A did not approve broad implementation. I-00 creates only a minimal governed skeleton. I-00 does not approve broad source tracking. I-00 does not approve existing `3_platform` contents. I-00 does not start I-01.

## 3. Minimal Platform Skeleton Definition
A minimal platform skeleton is a bounded, non-executable, Markdown-only initial implementation structure that reserves exact areas for future governed platform implementation while preserving all blockers from IR-A.

The skeleton is not broad implementation approval, runtime implementation, dependency adoption, validation/security enforcement, provider/API/MCP activation, CSS substrate selection, product activation, or approval of existing `3_platform` contents.

## 4. Decision Summary
Create exact governed skeleton files only. Use `3_platform/_governed_skeleton/` to avoid approving unknown existing `3_platform` siblings. Existing `3_platform` contents remain uninspected and unapproved. No code is created. No executable artifact is created. No package manifest or lockfile is created. No dependency is adopted. No validation/security enforcement is implemented. No runtime, agent, context, provider, MCP, or CSS prototype is implemented. I-01 may proceed only after explicit instruction.

## 5. Authority Boundary
| actor | authority |
| --- | --- |
| Governance | Decides implementation expansion, source tracking, dependency adoption, provider activation, product activation, publication, exceptions, and lifecycle. |
| Validation | Evaluates evidence. |
| Security | Constrains local-only content, secrets, credentials, execution, generated outputs, providers, APIs, MCP, network/auth, and publication. |
| I-00 | Creates exact skeleton placeholders only. |
| Git | Records artifacts but does not approve broad implementation. |
| Agents | May create exact approved skeleton files but cannot execute, install, activate, stage, commit, push, publish, or start I-01. |

## 6. Source Boundary
IR-A is the primary input. IR-02 controls source tracking. IR-04 controls dependency blockers. IR-05 controls runtime, agent, and context blockers. IR-06 controls provider, API, and MCP blockers. IR-07 controls CSS substrate deferral. IR-08 controls validation/security enforcement blockers. Raw `3_platform`, `2_products`, `4_external/sources`, secrets, credentials, datasets, models, artifacts, generated outputs, and product source are not inspected. Safe metadata only.

## 7. Exact Target Scope
Directories created only as needed: `0_architecture/implementation/`, `3_platform/_governed_skeleton/`, `3_platform/_governed_skeleton/core/`, `3_platform/_governed_skeleton/validation/`, `3_platform/_governed_skeleton/security/`, `3_platform/_governed_skeleton/context/`, `3_platform/_governed_skeleton/integrations/`, `3_platform/_governed_skeleton/agents/`, `3_platform/_governed_skeleton/tools/`, `3_platform/_governed_skeleton/cognitive_semantic_system/`.

Files created: `0_architecture/implementation/agent_platform_minimal_platform_skeleton.md`, `3_platform/_governed_skeleton/README.md`, `3_platform/_governed_skeleton/SKELETON_BOUNDARY.md`, `3_platform/_governed_skeleton/PLATFORM_MANIFEST.md`, `3_platform/_governed_skeleton/core/README.md`, `3_platform/_governed_skeleton/validation/README.md`, `3_platform/_governed_skeleton/security/README.md`, `3_platform/_governed_skeleton/context/README.md`, `3_platform/_governed_skeleton/integrations/README.md`, `3_platform/_governed_skeleton/agents/README.md`, `3_platform/_governed_skeleton/tools/README.md`, `3_platform/_governed_skeleton/cognitive_semantic_system/README.md`.

No sibling paths are in scope. Existing sibling contents under `3_platform/` are not approved. If any exact target file already exists, stop and report conflict. If exact target directories exist, do not inspect their contents; only create missing exact files if safe. If conflict is detected, do not overwrite.

## 8. Skeleton Area Manifest
| area | exact path | current purpose | current status | future route | explicitly not included |
| --- | --- | --- | --- | --- | --- |
| governed skeleton root | `3_platform/_governed_skeleton/` | isolated governed placeholder root | placeholder only | future implementation tickets | sibling approval, runtime |
| core | `3_platform/_governed_skeleton/core/` | reserve platform core area | placeholder only | future platform core tickets | core implementation |
| validation | `3_platform/_governed_skeleton/validation/` | reserve validation area | placeholder only | I-01 Validation Registry Implementation | registry implementation |
| security | `3_platform/_governed_skeleton/security/` | reserve security area | placeholder only | I-02 Security / Access Enforcement | enforcement implementation |
| context | `3_platform/_governed_skeleton/context/` | reserve context area | placeholder only | I-03 Context Pack Runtime | context runtime |
| integrations | `3_platform/_governed_skeleton/integrations/` | reserve integration area | placeholder only | I-04 Provider / Adapter Layer | providers/adapters/MCP |
| agents | `3_platform/_governed_skeleton/agents/` | reserve agent boundary area | placeholder only | I-05 Agent Runtime Boundary | agents/runtime |
| tools | `3_platform/_governed_skeleton/tools/` | reserve tool boundary area | placeholder only | I-06 Tool Execution Boundary | executable tools |
| cognitive_semantic_system | `3_platform/_governed_skeleton/cognitive_semantic_system/` | reserve CSS area | placeholder only | I-07 Cognitive Semantic System Prototype after CSS governance | substrate/prototype |

## 9. Root Skeleton README Requirements
`3_platform/_governed_skeleton/README.md` must state governed skeleton only, no implementation logic, exact scope, inherited blockers, not broad source tracking, not approval of existing `3_platform`, and future tickets own expansion.

## 10. Skeleton Boundary Requirements
`SKELETON_BOUNDARY.md` must state allowed files, forbidden files, no code, no dependencies, no runtime, no execution, no product source, no local-only leakage, no provider/API/MCP activation, no CSS substrate decision, and no broad implementation approval.

## 11. Platform Manifest Requirements
`PLATFORM_MANIFEST.md` must include skeleton version I-00, governed root `3_platform/_governed_skeleton/`, created areas, current status, source tracking posture, dependency posture, validation/security posture, future roadmap link to I-01 through I-07, and unresolved blockers.

## 12. Area README Requirements
Each area README includes Purpose, Current status: placeholder only, Non-goals, Blocked now, Future ticket route, and Stop rules. Future routes are: core to future platform core tickets, validation to I-01 Validation Registry Implementation, security to I-02 Security / Access Enforcement, context to I-03 Context Pack Runtime, integrations to I-04 Provider / Adapter Layer, agents to I-05 Agent Runtime Boundary, tools to I-06 Tool Execution Boundary, and cognitive_semantic_system to I-07 Cognitive Semantic System Prototype only after CSS governance.

## 13. Existing 3_platform Treatment
Existing `3_platform` contents remain uninspected. Existing `3_platform` contents remain unapproved. I-00 does not classify existing contents. I-00 does not delete, move, archive, copy, normalize, or reuse existing contents. The governed skeleton subroot does not approve any sibling content.

## 14. Source Tracking / Git Boundary
I-00 does not approve broad source tracking. Only exact I-00-created skeleton files may be considered for exact-path staging after human review. Existing `3_platform` content remains not trackable. Product source remains not trackable. `.gitignore` is unchanged. No force-add is authorized. No `git add .`.

## 15. Dependency Boundary
No dependencies are adopted. No package manifests are created. No lockfiles are created. No package managers are run. No SDK, native, tool, or runtime dependency is activated. Future dependency work requires gates.

## 16. Validation / Security Boundary
No validation registry is created. No security enforcement is created. No proof/evidence registry is created. No validation/security scan is executed. No secrets or credentials are inspected. Future enforcement belongs to later exact tickets.

## 17. Runtime / Agent / Context Boundary
No runtime is created. No agents are created or activated. No context engine or context pack runtime is created. No memory/state persistence is approved. No tool execution is approved.

## 18. Provider / Adapter / MCP Boundary
No providers are activated. No adapters are created or activated. No MCP server, tool, or resource is activated. No API, network, or auth call is made. No credentials are inspected or used.

## 19. Cognitive Semantic System Boundary
Cognitive Semantic System remains accepted name. Cognitive Semantic System substrate remains deferred. Graph remains candidate only. Graphify remains evidence only, not authority. No CSS prototype, graph schema, vector index, ontology, database, event store, or semantic runtime is created.

## 20. Product Boundary
Products remain inactive. Product source remains local-only. Product source is not copied into skeleton. EnergyPlus remains solver, not internal model. Omniverse Kit remains interface, not backend. Product activation remains blocked.

## 21. Created Files Register
| file | type | purpose | contains code? | executable? | dependency impact? | source tracking posture | future owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0_architecture/implementation/agent_platform_minimal_platform_skeleton.md` | Markdown | I-00 record | no | no | none | exact-path review only | governance |
| `3_platform/_governed_skeleton/README.md` | Markdown | root placeholder | no | no | none | exact-path review only | governance |
| `3_platform/_governed_skeleton/SKELETON_BOUNDARY.md` | Markdown | boundary placeholder | no | no | none | exact-path review only | governance/security |
| `3_platform/_governed_skeleton/PLATFORM_MANIFEST.md` | Markdown | platform skeleton manifest | no | no | none | exact-path review only | governance |
| `3_platform/_governed_skeleton/core/README.md` | Markdown | core placeholder | no | no | none | exact-path review only | future core ticket |
| `3_platform/_governed_skeleton/validation/README.md` | Markdown | validation placeholder | no | no | none | exact-path review only | I-01 |
| `3_platform/_governed_skeleton/security/README.md` | Markdown | security placeholder | no | no | none | exact-path review only | I-02 |
| `3_platform/_governed_skeleton/context/README.md` | Markdown | context placeholder | no | no | none | exact-path review only | I-03 |
| `3_platform/_governed_skeleton/integrations/README.md` | Markdown | integration placeholder | no | no | none | exact-path review only | I-04 |
| `3_platform/_governed_skeleton/agents/README.md` | Markdown | agent placeholder | no | no | none | exact-path review only | I-05 |
| `3_platform/_governed_skeleton/tools/README.md` | Markdown | tool placeholder | no | no | none | exact-path review only | I-06 |
| `3_platform/_governed_skeleton/cognitive_semantic_system/README.md` | Markdown | CSS placeholder | no | no | none | exact-path review only | I-07 after CSS governance |

## 22. Non-created Artifacts Register
| artifact class | examples | status | future route |
| --- | --- | --- | --- |
| code | Python, JavaScript, TypeScript, shell | not created | future exact tickets |
| package manifests | package files, project files | not created | dependency gate |
| lockfiles | package locks | not created | dependency gate |
| scripts/tools/tests | executable scripts, tests, tools | not created | test/tool gates |
| CI/runners/hooks | workflows, hooks, runners | not created | CI gate |
| validation registry | registry implementation | not created | I-01 after instruction |
| security enforcement | access controls, policy runtime | not created | I-02 after instruction |
| runtime | process/runtime modules | not created | future runtime gates |
| agents | agent implementations | not created | I-05 after instruction |
| context engine | context runtime, memory/state | not created | I-03 after instruction |
| provider/adapters/MCP | providers, adapters, MCP configs | not created | I-04 after instruction |
| CSS prototype | graph, vector, ontology, database | not created | I-07 after CSS governance |
| product source | Siamese product source | not copied | product governance |

## 23. I-00 Gate Checklist
| gate | pass condition | current result | blocker if failed |
| --- | --- | --- | --- |
| IR-A exists | path exists | pass | stop |
| exact scope declared | this record lists targets | pass | stop |
| exact targets declared | all files listed | pass | stop |
| no existing target conflicts | target files absent before creation | pass | stop |
| skeleton root isolated | `_governed_skeleton` used | pass | stop |
| no code created | Markdown only | pass | stop |
| no manifests created | no package manifests; Markdown platform manifest only | pass | stop |
| no dependencies adopted | none adopted | pass | stop |
| no execution occurred | no runtime/tool/test/product execution | pass | stop |
| source tracking bounded | exact-path review only | pass | stop |
| existing 3_platform contents unapproved | no inspection or approval | pass | stop |
| next ticket I-01 not started | no I-01 artifact | pass | stop |

## 24. Residual Risk Register
| risk_id | residual risk | severity | mitigation | route | blocks broad implementation? |
| --- | --- | --- | --- | --- | --- |
| I00-R-01 | existing `3_platform` siblings unknown | blocker | keep isolated | future classification | yes |
| I00-R-02 | skeleton has no runtime | blocker | preserve non-runtime scope | future runtime gates | yes |
| I00-R-03 | no validation registry | blocker | route to I-01 | I-01 | yes |
| I00-R-04 | no security enforcement | blocker | route to I-02 | I-02 | yes |
| I00-R-05 | no dependencies | blocker | dependency gate | future | yes |
| I00-R-06 | no tests | major_gap | test gate | future | yes |
| I00-R-07 | no provider/adapters/MCP | blocker | activation gate | I-04 | yes |
| I00-R-08 | CSS substrate deferred | blocker | CSS governance | I-07 | yes |
| I00-R-09 | product source local-only | blocker | product governance | future | yes |
| I00-R-10 | generated output controls absent | major_gap | enforcement design | future | yes |
| I00-R-11 | source tracking broad approval absent | blocker | exact tracking gate | future | yes |

## 25. Blocker Register
| blocker | stop behavior | required future action | blocks I-00? | blocks broad implementation? |
| --- | --- | --- | --- | --- |
| exact target file exists | stop before overwrite | conflict decision | yes | yes |
| need to inspect existing 3_platform | stop | classification ticket | yes | yes |
| need to create code | stop | future exact ticket | yes | yes |
| need to create package manifest | stop | dependency gate | yes | yes |
| need to adopt dependency | stop | dependency review | yes | yes |
| need to execute tool/test | stop | execution approval | yes | yes |
| need to activate provider/API/MCP | stop | activation gate | yes | yes |
| need to select CSS substrate | stop | CSS governance | yes | yes |
| need to activate product | stop | product governance | yes | yes |
| source tracking implied beyond exact skeleton | stop | source tracking gate | yes | yes |
| Git action implied | stop | human approval | yes | yes |
| I-01 scope pressure detected | stop | finish I-00 only | yes | yes |

## 26. Incident Handling
Incidents include existing `3_platform` content inspected or approved; target file overwritten; code created; package manifest created; dependency adopted; test, script, or tool executed; validation/security enforcement implemented; provider/API/MCP activated; CSS substrate selected; product source copied; `.gitignore` modified; Git staging, commit, or push attempted; or I-01 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 27. I-00 Invariants
| id | invariant |
| --- | --- |
| I00-001 | Minimal platform skeleton is not broad implementation approval. |
| I00-002 | Only exact governed skeleton files are created. |
| I00-003 | Existing 3_platform contents remain uninspected and unapproved. |
| I00-004 | No code is created. |
| I00-005 | No package manifests or lockfiles are created. |
| I00-006 | Dependencies remain unadopted. |
| I00-007 | Source tracking is not broadly approved. |
| I00-008 | Product source remains local-only. |
| I00-009 | Validation/security enforcement is not implemented. |
| I00-010 | Providers/API/MCP remain inactive. |
| I00-011 | Cognitive Semantic System substrate remains deferred. |
| I00-012 | Product activation remains blocked. |
| I00-013 | Validation evaluates; governance decides. |
| I00-014 | I-00 stops before I-01. |

## 28. Anti-patterns
Anti-patterns: skeleton as full implementation; skeleton as source tracking approval; skeleton as dependency adoption; README as runtime; placeholder as implementation; existing `3_platform` as approved source; product source copied into platform skeleton; package manifest as harmless placeholder; validation/security folders as enforcement; CSS folder as substrate decision; graph folder as graph adoption; provider folder as provider activation; `git add .`; starting I-01 inside I-00.

## 29. Readiness For I-01
I-01 - Validation Registry Implementation is ready after explicit instruction if I-00 skeleton exists; only exact skeleton files were created; no code was created; no dependencies were adopted; no validation registry was created; no security enforcement was created; no provider/API/MCP activation occurred; CSS substrate remains deferred; product source remains local-only; existing `3_platform` contents remain uninspected and unapproved; and no Git mutation occurred.

Do not create I-01.

## 30. Final Verdict
I-00 created the exact Markdown architecture record and governed skeleton placeholders only. I-00 did not approve broad implementation. I-00 did not inspect or approve existing `3_platform` contents. I-00 did not create code. I-00 did not create package manifests or lockfiles. I-00 did not adopt dependencies. I-00 did not approve source tracking broadly. I-00 did not create validation/security enforcement. I-00 did not activate providers/API/MCP. I-00 did not decide CSS substrate. I-00 did not activate products.

Blocked items remain: broad implementation, source tracking beyond exact skeleton review, existing `3_platform` approval, product source tracking, dependency adoption, package manager use, validation registry, security enforcement, runtime, agents, context engine, providers, adapters, MCP, CSS prototype/substrate, products, generated-output controls, CI, tests, scripts, tools, publication, staging, commit, push, and I-01. I-01 is ready after explicit instruction only.
