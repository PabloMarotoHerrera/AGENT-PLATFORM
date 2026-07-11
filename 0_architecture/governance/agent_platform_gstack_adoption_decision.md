# GStack Adoption Decision

## 1. Document Header

| Field | Value |
| --- | --- |
| Ticket | P12.6 |
| Title | GStack Adoption Decision |
| Type | Governance / adoption-decision / skill-stack-boundary / no-runtime |
| Status | Drafted for acceptance |
| Target file | `0_architecture/governance/agent_platform_gstack_adoption_decision.md` |
| Authority | Adoption decision only. This document is not GStack setup, GStack install, GStack runtime, skill execution, tool execution, hook registration, browser daemon launch, cookie import, ngrok, MCP registration, provider/API use, GBrain sync, memory write, settings mutation, PATH mutation, source modification, Git mutation, or dependency installation. |
| Result marker | `gstack_adoption_decision_ready` |

## 2. Purpose

P12.6 decides the GStack adoption posture for Project 12.

The decision answers whether GStack is adopted, what it is adopted as, what it is not adopted as, what remains blocked, how GStack relates to GBrain and the memory store, and what handoff unlocks P12.8.

P12.6 does not install, execute, register, launch, configure, sync, mutate, or write anything.

## 3. Inputs Reviewed

Governance inputs used by P12.6:

| Input | Status | P12.6 use |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_skill_authority_execution_boundary.md` | Present; marker-searched | P12.4 skill non-authority and execution gate boundary. |
| `0_architecture/governance/agent_platform_memory_store_integration_design.md` | Present; marker-searched | P12.7 memory-store relation and skill-memory boundary. |
| `0_architecture/governance/agent_platform_memory_authority_model.md` | Present; marker-searched | P12.3 memory authority and GStack non-memory-authority posture. |
| `0_architecture/governance/agent_platform_gbrain_adoption_graphify_semantic_replacement_decision.md` | Present by path check | P12.5 GBrain retrieval role and non-authority boundary from accepted context. |
| `0_architecture/governance/agent_platform_external_tool_execution_gate_model.md` | Not separately inspected in P12.6 | P12.2/P12.4 evidence was sufficient for tool execution blockers. |
| `0_architecture/governance/agent_platform_human_approval_review_loop_operational_contract.md` | Not separately inspected in P12.6 | P12.4 evidence was sufficient for skill approval/execution boundary. |
| `0_architecture/governance/agent_platform_audit_retention_rollback_baseline.md` | Not separately inspected in P12.6 | Retention/rollback design is not changed by this adoption decision. |
| `.graphifyignore` | Not inspected in P12.6 | Not modified. |
| `.gitignore` | Not inspected in P12.6 | Not modified. |

GStack metadata inspected read-only:

| Input | Status | P12.6 use |
| --- | --- | --- |
| `4_external/sources/gstack-main` | Present | External source root exists as candidate evidence only. |
| `4_external/sources/gstack-main/package.json` | Present | Confirms package name/version/license/script/dependency surfaces by marker search. |
| `4_external/sources/gstack-main/LICENSE` | Present | License file presence confirmed. |
| `4_external/sources/gstack-main/AGENTS.md` | Present | Confirms skill taxonomy and broad browser/GBrain/Git/deploy/codex surfaces by marker search. |
| `4_external/sources/gstack-main/BROWSER.md` | Present | Browser surface path presence confirmed; not executed. |
| `4_external/sources/gstack-main/setup` | Present | Setup surface path presence confirmed; not executed. |

P12.6 did not inspect credentials, generated state, caches, `node_modules`, normal user state, product source, generated artifacts, DB internals, browser cookie stores, or raw provider/auth material.

## 4. P12.2 Dependency Status

P12.2 conclusions are retained as historical decision lineage in this adoption record.

Required marker confirmed:

`gstack_license_dependency_skill_audit_ready`

Supporting markers confirmed:

| Marker | P12.6 implication |
| --- | --- |
| `gstack_mit_license_confirmed` | License posture is permissive enough for further evaluation. |
| `gstack_dependency_surface_classified` | Dependency surface is known enough for adoption boundary decision. |
| `gstack_skill_surface_classified` | Skill surface is known enough for read-only skill-source adoption. |
| `gstack_install_runtime_still_blocked` | Setup/runtime must remain blocked. |
| `gstack_controlled_setup_plan_required` | Any future setup requires a controlled plan. |
| `runtime_allowed_now: false` | P12.6 cannot authorize runtime. |

P12.2 classified GStack as license-permissible for further evaluation and not approved for setup, runtime, skill execution, browser daemon, provider/API usage, MCP registration, cookie import, hooks, memory writes, or Git mutation.

## 5. P12.4 Dependency Status

P12.4 exists as:

`0_architecture/governance/agent_platform_skill_authority_execution_boundary.md`

Required marker confirmed:

`skill_authority_execution_boundary_ready`

Supporting markers confirmed:

| Marker | P12.6 implication |
| --- | --- |
| `skills_not_authority` | GStack skills cannot become policy, approval, or decision authority. |
| `skills_not_memory_authority` | GStack skills cannot define or write authoritative memory. |
| `skills_require_explicit_execution_gate` | Skill execution remains blocked until exact future gate. |
| `gstack_skill_surface_governed` | GStack skill surface can be governed as read-only evidence. |
| `browser_skill_runtime_blocked_by_default` | Browser skill runtime remains blocked. |
| `provider_skill_runtime_blocked_by_default` | Provider/API skill runtime remains blocked. |
| `git_mutation_by_skill_blocked_by_default` | Git mutation by skill remains blocked. |
| `p12_8_skill_stack_bootstrap_design_ready_after_skill_boundary` | P12.8 may consume P12.4 and P12.6 after acceptance. |

P12.4 states: a skill can recommend; governance approves; execution gates execute.

## 6. P12.7 Relationship Status

P12.7 exists as:

`0_architecture/governance/agent_platform_memory_store_integration_design.md`

Required marker confirmed:

`memory_store_integration_design_ready`

P12.7 states that GBrain is the derived retrieval/index provider, GStack remains pending P12.6, skill memory must follow P12.4, and skills cannot write memory unless a future memory write gate allows it.

P12.6 does not alter P12.3, P12.5, or P12.7.

## 7. GStack Metadata Classification

Read-only metadata confirms GStack has skill-stack value and broad execution-risk surfaces.

| Evidence | Classification | P12.6 implication |
| --- | --- | --- |
| `package.json` name/version/license/bin/scripts/dependencies/devDependencies markers | Package/tool surface metadata | Confirms a package/runtime/dependency surface exists, but not permission to install or run. |
| `AGENTS.md` skill table | Skill taxonomy evidence | Supports read-only skill source candidate adoption. |
| `AGENTS.md` plan/review/spec/codex/design/qa/deploy/context/browser/safety references | Workflow pattern evidence | Supports P12.8 bootstrap design input, not execution. |
| `AGENTS.md` browse/browser/cookie/pair-agent references | Browser/remote pairing risk surface | Browser daemon/cookie/ngrok/remote pairing remain blocked. |
| `AGENTS.md` setup-gbrain/sync-gbrain references | Memory/GBrain sync risk surface | GBrain sync and memory writes remain blocked. |
| `AGENTS.md` ship/land/deploy/git references | Git/deployment risk surface | Git/deploy/release flows remain blocked. |
| `AGENTS.md` guard/freeze references | Hook/settings/edit-control risk surface | Advisory concepts may inform design, but hook/settings mutation remains blocked. |

The metadata is sufficient for Outcome A. No runtime inspection is required for P12.6.

## 8. Adoption Options

| Option | Description | P12.6 decision |
| --- | --- | --- |
| Outcome A - Adopt as read-only skill source candidate | Use GStack as reference corpus for skill taxonomy, workflow patterns, skill bootstrap design, and prompt/skill packaging concepts. | Selected. |
| Outcome B - Defer adoption | Keep GStack pending because P12.2/P12.4 evidence is insufficient. | Not selected; evidence is sufficient for read-only adoption. |
| Outcome C - Reject adoption | Close GStack path because evidence shows it cannot safely inform Project 12. | Not selected; no evidence requires rejection for read-only design input. |

Decision: Outcome A.

## 9. Adoption Decision

GStack is adopted only as a read-only skill source candidate for Project 12.

Adoption is limited to using GStack as evidence for skill taxonomy, workflow design patterns, prompt/skill packaging concepts, bootstrap design inputs, and future controlled setup planning if later needed.

P12.6 does not adopt GStack as runtime, active skill system, execution authority, memory authority, policy authority, approval authority, browser automation runtime, provider interface, MCP runtime, credential manager, Git/deployment automation, GBrain replacement, Graphify replacement, Hermes replacement, or Paperclip replacement.

Decision markers:

`gstack_adopted_as_readonly_skill_source_candidate`

`gstack_not_adopted_as_runtime`

`gstack_not_adopted_as_memory_authority`

`gstack_not_adopted_as_execution_authority`

## 10. Adopted Role

GStack is adopted only as:

| Adopted role | Boundary |
| --- | --- |
| Read-only skill source candidate | May inform skill-stack design without install or execution. |
| Skill taxonomy reference | Skill categories, roles, and naming patterns may inform P12.8. |
| Workflow pattern reference | Plan/review/QA/release/context/safety patterns may inform design. |
| Skill bootstrap design input | P12.8 may use GStack concepts to design local skill bootstrap. |
| Prompt/skill packaging reference | Skill file/template structure may inform a governed format. |
| Future controlled setup candidate | Only if P12.8/P12.10 later proves setup is necessary and P12.2A or equivalent gate exists. |

This adoption is evidence-only and read-only.

## 11. Non-Adopted Roles

GStack is not adopted as:

| Non-adopted role | Decision |
| --- | --- |
| Runtime | Not adopted. |
| Active skill system | Not adopted. |
| Memory authority | Not adopted. |
| Execution authority | Not adopted. |
| Policy authority | Not adopted. |
| Approval authority | Not adopted. |
| Browser automation runtime | Not adopted. |
| MCP runtime | Not adopted. |
| Provider interface | Not adopted. |
| Credential manager | Not adopted. |
| Git automation system | Not adopted. |
| Deployment system | Not adopted. |
| GBrain replacement | Not adopted. |
| Graphify replacement | Not adopted. |
| Hermes replacement | Not adopted. |
| Paperclip replacement | Not adopted. |

## 12. Setup / Runtime Decision

P12.6 decides:

| Surface | Decision |
| --- | --- |
| GStack setup | No setup now. |
| GStack install | No install now. |
| GStack runtime | No runtime now. |
| Skill execution | No skill execution now. |
| Tool execution | No tool execution now. |
| Dependency install | No dependency install now. |
| `node_modules` creation | Not approved. |
| Setup script | Not run and not approved. |

Setup remains deferred until a later controlled plan only if needed:

`P12.2A - GStack Controlled Setup Boundary Plan`

Any future controlled setup must select exactly one host integration, disable team mode, auto-upgrade, telemetry, plan-tune/settings hooks, browser/cookie/daemon/sidebar/pair-agent/ngrok surfaces, and Git/checkpoint behavior by default. `GSTACK_HOME` and every writable state path must be pinned to an approved sandbox. Setup must run without provider keys, Supabase tokens, GBrain bearer tokens, proxy credentials, or writes to normal-user Claude, Codex, OpenCode, or GStack directories. The selected version requires a fresh dependency and transitive-license review before installation.

P12.6 does not require P12.2A immediately. P12.8 should proceed first from read-only evidence and decide later whether setup is necessary for P12.10.

Decision marker:

`gstack_setup_deferred_until_controlled_plan`

## 13. Browser / MCP / Provider / Git Boundary

The following remain blocked until exact future gates:

| Surface | P12.6 decision |
| --- | --- |
| Browser daemon | Blocked. |
| Playwright/Chromium runtime | Blocked. |
| Cookie import | Blocked. |
| Browser cookie stores | Not inspected; blocked. |
| ngrok / remote pair-agent | Blocked. |
| Provider CLIs/APIs/SDKs | Blocked. |
| MCP registration/runtime | Blocked. |
| GBrain sync | Blocked. |
| Memory writes | Blocked. |
| Hooks/settings mutation | Blocked. |
| Git mutation | Blocked. |
| Deployment/release flows | Blocked. |
| Credential/env surfaces | Blocked. |

Decision marker:

`gstack_browser_provider_mcp_surfaces_remain_blocked`

## 14. GBrain / Memory Store Relation

P12.6 preserves P12.3, P12.5, and P12.7.

| Surface | Decision |
| --- | --- |
| GBrain | Remains memory/retrieval infrastructure and derived index provider. |
| GStack | Read-only skill source candidate only. |
| Memory authority | GStack is not memory authority. |
| Memory writes | GStack cannot write memory. |
| GBrain sync | GStack cannot sync GBrain. |
| Operational memory | GStack cannot define operational memory. |
| Skill memory | Must follow P12.4 and P12.7. |
| Skill execution | Requires explicit future execution gate. |

P12.6 does not alter the Memory Authority Model, GBrain adoption decision, or Memory Store Integration Design.

## 15. Skill Bootstrap Implications

Because Outcome A is selected, P12.8 may use GStack as read-only input for skill stack bootstrap design.

P12.8 may consider:

| Design topic | Allowed P12.8 use |
| --- | --- |
| Skill taxonomy | Derive governed categories and names. |
| Skill file conventions | Design project-local skill packaging without copying unsafe runtime behavior. |
| Workflow patterns | Translate review/planning/QA/context/safety ideas into governed agent-platform contracts. |
| Permission classes | Align with P12.4 permission classes and blocked surfaces. |
| Memory interaction | Preserve P12.7 memory write/read boundaries. |
| Runtime need assessment | Decide whether no-runtime bootstrap is sufficient or whether P12.2A is needed later. |

P12.8 must not require GStack setup unless its design explicitly concludes runtime inspection is necessary.

Decision marker:

`gstack_skill_bootstrap_design_ready`

## 16. P12.8 Handoff Decision

P12.6 hands off to:

`P12.8 - Skill Stack Bootstrap Design`

P12.8 should require:

| Dependency | Requirement |
| --- | --- |
| P12.4 accepted | Skill authority/execution boundary must govern design. |
| P12.6 accepted | GStack read-only adoption decision must be accepted. |

P12.8 should not require GStack setup unless the design explicitly concludes runtime inspection is necessary.

Future possible ticket only if needed:

`P12.2A - GStack Controlled Setup Boundary Plan`

Future spike:

`P12.10 - Skill Stack Bootstrap Spike`

P12.10 must require P12.8 accepted and either a no-runtime bootstrap design or a controlled GStack setup plan if runtime becomes necessary.

Decision marker:

`p12_8_skill_stack_bootstrap_design_ready_after_gstack_adoption`

## 17. Stop Rules

STOP if work requires any of the following:

| Stop condition | Required response |
| --- | --- |
| Install or run GStack | Stop and require future controlled setup/runtime gate. |
| Execute skills or tools | Stop and require P12.4-aligned execution gate. |
| Register hooks or mutate settings | Stop and require exact future gate. |
| Launch browser daemon, Playwright, Chromium, ngrok, or pair-agent | Stop and require browser/remote gate. |
| Import cookies or inspect browser auth | Stop and preserve credential boundary. |
| Register MCP or call providers | Stop and require provider/API/MCP gate. |
| Run GBrain sync or write memory | Stop and require memory write/sync gate. |
| Mutate Git | Stop unless exact user request and governance approval exist. |
| Install dependencies or create `node_modules` | Stop and require controlled setup plan. |
| Modify GStack source or existing governance files | Stop; P12.6 may create only its output file. |
| Recommend `git add .` | Stop; exact path only. |

## 18. Acceptance Criteria Mapping

| Criterion | Status |
| --- | --- |
| Creates exactly one GStack adoption decision file | Satisfied by this file only. |
| Confirms P12.2 dependency | Satisfied. |
| Confirms P12.4 dependency | Satisfied. |
| Decides GStack adoption posture | Satisfied: Outcome A. |
| Limits adoption to read-only skill source candidate | Satisfied. |
| States setup/runtime remain blocked | Satisfied. |
| States skills remain blocked for execution | Satisfied. |
| States browser/MCP/provider/Git surfaces remain blocked | Satisfied. |
| States GStack is not memory authority | Satisfied. |
| States GStack is not execution authority | Satisfied. |
| Hands off to P12.8 | Satisfied. |
| Does not run tools | Satisfied. |
| Does not install GStack | Satisfied. |
| Does not mutate Git | Satisfied. |

## 19. Created / Not Created Register

Created:

| Item | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_gstack_adoption_decision.md` | Created as P12.6 GStack adoption decision. |

Not created / not approved:

| Item | Status |
| --- | --- |
| GStack installation | Not performed / not approved. |
| GStack execution | Not performed / not approved. |
| Skill execution | Not performed / not approved. |
| Tool execution | Not performed / not approved. |
| MCP registration | Not performed / not approved. |
| Browser daemon | Not launched / not approved. |
| Cookie import | Not performed / not approved. |
| ngrok | Not started / not approved. |
| Provider/API call | Not performed / not approved. |
| GBrain sync | Not performed / not approved. |
| Memory write | Not performed / not approved. |
| Hook registration | Not performed / not approved. |
| Settings mutation | Not performed / not approved. |
| Git mutation | Not performed / not approved. |
| Dependency install | Not performed / not approved. |
| `node_modules` | Not created / not approved. |
| Sandbox outputs | Not created / not approved. |
| Credential inspection | Not performed. |
| PATH mutation | Not performed. |
| `git add .` | Not recommended. |

## 20. Decision Markers

gstack_adoption_decision_ready

gstack_adopted_as_readonly_skill_source_candidate

gstack_not_adopted_as_runtime

gstack_not_adopted_as_memory_authority

gstack_not_adopted_as_execution_authority

gstack_setup_deferred_until_controlled_plan

gstack_browser_provider_mcp_surfaces_remain_blocked

gstack_skill_bootstrap_design_ready

p12_8_skill_stack_bootstrap_design_ready_after_gstack_adoption

## 21. Final Verdict

P12.6 selects Outcome A: GStack is adopted as a read-only skill source candidate only.

GStack may inform P12.8 skill stack bootstrap design as a skill taxonomy reference, workflow pattern reference, prompt/skill packaging reference, and future controlled setup candidate if later needed.

GStack is not adopted as runtime, active skill system, memory authority, execution authority, policy authority, approval authority, browser automation runtime, MCP runtime, provider interface, credential manager, Git automation system, deployment system, GBrain replacement, Graphify replacement, Hermes replacement, or Paperclip replacement.

No setup, install, runtime, skill execution, browser/provider/MCP/Git/cookie/hook/memory-write surface is approved by P12.6.

P12.8 - Skill Stack Bootstrap Design is ready after P12.6 acceptance.
