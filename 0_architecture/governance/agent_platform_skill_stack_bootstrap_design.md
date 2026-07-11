# Skill Stack Bootstrap Design

## 1. Document Header

| Field | Value |
| --- | --- |
| Ticket | P12.8 |
| Title | Skill Stack Bootstrap Design |
| Type | Governance / architecture / skill-stack-bootstrap / no-runtime |
| Status | Drafted for acceptance |
| Target file | `0_architecture/governance/agent_platform_skill_stack_bootstrap_design.md` |
| Authority | Design only. This document is not GStack setup, GStack install, GStack runtime, skill execution, tool execution, hook registration, browser daemon launch, cookie import, ngrok, MCP registration, provider/API use, GBrain sync, memory write, settings mutation, PATH mutation, source modification, dependency installation, Git mutation, or generated skill registration. |
| Result marker | `skill_stack_bootstrap_design_ready` |

Result marker:

```text
skill_stack_bootstrap_design_ready
```

Decision markers:

```text
skill_stack_bootstrap_architecture_defined
gstack_readonly_skill_source_consumed
no_runtime_skill_bootstrap_path_defined
internal_skill_blueprint_model_defined
skill_registry_bootstrap_model_defined
skill_lifecycle_model_defined
skill_taxonomy_mapping_defined
skill_runtime_profile_mapping_defined
skill_permission_gate_mapping_defined
skill_memory_boundary_preserved
skill_output_boundary_preserved
gstack_setup_not_required_for_initial_bootstrap
p12_10_skill_stack_bootstrap_spike_ready_after_design
```

```yaml
P12_8_Skill_Stack_Bootstrap_Design:
  ticket: "P12.8"
  date: "2026-07-10"
  status: "governance_design_only"
  output_file: "0_architecture/governance/agent_platform_skill_stack_bootstrap_design.md"
  p12_2_dependency_confirmed: true
  p12_4_dependency_confirmed: true
  p12_6_dependency_confirmed: true
  p12_7_dependency_confirmed: true
  gstack_role: "read_only_skill_source_candidate"
  gstack_setup_required_for_initial_bootstrap: false
  initial_bootstrap_runtime_profiles: ["S0", "S1", "S2"]
  s3_plus_runtime_enabled: false
  skill_execution_enabled: false
  tool_execution_enabled: false
  browser_runtime_enabled: false
  mcp_enabled: false
  provider_enabled: false
  memory_write_enabled: false
  git_mutation_enabled: false
  final_marker: "skill_stack_bootstrap_design_ready"
```

## 2. Purpose

P12.8 defines how AGENT PLATFORM can bootstrap a governed skill stack without installing, running, or registering GStack.

The design answers:

| Question | P12.8 answer |
| --- | --- |
| What is the bootstrap architecture? | A project-local, inactive blueprint and registry layer governed by P12.4/P12.6/P12.7. |
| How is GStack consumed? | As read-only external skill source evidence for taxonomy, workflow, packaging, and risk boundaries. |
| Is GStack setup required? | No. Initial bootstrap is no-runtime and does not require `setup`, `bun`, generated skills, browser binaries, or host skill registration. |
| What is the internal skill unit? | A `SkillBlueprint` record with source refs, taxonomy, runtime profile, permission gates, lifecycle state, memory posture, and output posture. |
| What is the registry? | A static catalog of inactive skill blueprints, not a dispatcher, command router, host plugin, or execution runtime. |
| What does P12.10 do next? | Create a governed local skeleton and a small inactive S0/S1/S2 candidate set, if accepted. |

P12.8 does not implement the skill stack. It defines the governed model that P12.10 may spike later.

## 3. Dependency Status

| Dependency | Required marker | Status | P12.8 use |
| --- | --- | --- | --- |
| P12.2 GStack License Dependency Skill Audit | `gstack_license_dependency_skill_audit_ready` | Confirmed | Confirms GStack is license-permissible for evaluation, but setup/runtime remain blocked and controlled setup is required if runtime is later needed. |
| P12.4 Skill Authority / Execution Boundary | `skill_authority_execution_boundary_ready` | Confirmed | Defines S0-S6 profiles, permission classes, output classification, blocked surfaces, and explicit execution gate requirements. |
| P12.6 GStack Adoption Decision | `gstack_adoption_decision_ready` | Confirmed | Adopts GStack only as read-only skill source candidate and hands off to P12.8. |
| P12.7 Memory Store Integration Design | `memory_store_integration_design_ready` | Confirmed | Preserves memory store authority boundaries and blocks skill memory writes unless a future exact gate approves them. |

Dependency implications:

| Rule | P12.8 consequence |
| --- | --- |
| Skills are not authority. | Blueprints can guide work but cannot approve, decide, or override governance. |
| Skills are not execution grants. | Registry entries must not execute commands or tools. |
| Skills are not memory authority. | Skill memory writes, GBrain sync, and operational memory mutation remain blocked. |
| GStack is read-only input only. | GStack concepts can be translated into internal records; GStack setup/runtime are not required. |
| S3+ surfaces are blocked by default. | Initial bootstrap must stay S0/S1/S2. |

## 4. Inputs Reviewed

Governance inputs reviewed read-only:

```text
0_architecture/governance/agent_platform_skill_authority_execution_boundary.md
0_architecture/governance/agent_platform_gstack_adoption_decision.md
0_architecture/governance/agent_platform_memory_store_integration_design.md
```

GStack source evidence reviewed read-only:

```text
4_external/sources/gstack-main/package.json
4_external/sources/gstack-main/AGENTS.md
4_external/sources/gstack-main/BROWSER.md
```

GStack evidence consumed:

| Evidence | P12.8 use |
| --- | --- |
| `package.json` package name/version/license/bin/scripts/dependencies | Confirms package and runtime surfaces exist, including browser, Bun, Playwright, ngrok, provider SDK, build/test, and generated-skill scripts. |
| `AGENTS.md` skill categories and conventions | Provides read-only taxonomy input for planning, review, implementation, release, operational, memory, browser, device QA, and safety skill categories. |
| `BROWSER.md` browser runtime description | Confirms browser/daemon/CDP/cookie/ngrok/pair-agent surfaces remain high-risk and out of initial bootstrap scope. |

Not inspected or used:

```text
.env
.env.*
credentials/**
secrets/**
provider configs
browser auth
browser cookie stores
normal user .gbrain
normal user .gstack
normal user .claude
normal user .codex
node_modules/**
9_artifacts/** contents
product source
Siamese/product paths
generated host skill directories
raw provider output
raw runtime output
```

## 5. Bootstrap Architecture

The skill stack bootstrap is a governed metadata architecture with four layers:

| Layer | Role | Runtime posture |
| --- | --- | --- |
| External Skill Source Evidence | Read-only references to GStack taxonomy, packaging concepts, and workflow patterns. | No execution, no setup, no generated skill import. |
| Internal Skill Blueprint | Project-local record describing one proposed skill concept and its boundaries. | Inactive by default. |
| Skill Registry | Static index of blueprints, lifecycle state, runtime profile, and required gates. | Not a dispatcher, not a command router, not a host plugin. |
| Gate Mapping | Explicit mapping from each blueprint to P12.4 permissions and future gates. | Blocks any surface not approved by exact future gate. |

Architecture decision:

```text
AGENT PLATFORM skill bootstrap starts as static governed design data. It does not start as a GStack install, host skill directory, slash-command runtime, browser runtime, MCP server, provider wrapper, memory writer, Git automation layer, or generated-skill importer.
```

Decision marker:

```text
skill_stack_bootstrap_architecture_defined
```

## 6. GStack Source Consumption Model

GStack is consumed as evidence, not runtime.

Allowed P12.8 consumption:

| GStack input | Allowed use |
| --- | --- |
| Skill category names | Map to AGENT PLATFORM taxonomy. |
| Skill role descriptions | Identify useful planning, review, QA, context, safety, and release concepts. |
| `SKILL.md` / template convention | Inform internal packaging concepts only; no generated import required. |
| Safety skill concepts | Inform advisory guardrail blueprints; not enforcement authority. |
| Browser productivity model | Record future candidate surfaces; initial bootstrap blocks them. |
| Memory/context skill concepts | Record future candidate surfaces; memory writes remain blocked. |
| Release/deploy skill concepts | Record future candidate surfaces; Git/deploy remain blocked. |

Blocked P12.8 consumption:

| Blocked action | Reason |
| --- | --- |
| Run `./setup` or any setup script | P12.2/P12.6 require controlled setup plan before runtime/setup. |
| Run `bun install`, `bun run`, tests, build, or generation scripts | Dependency/runtime side effects are not approved. |
| Invoke GStack slash commands | Skill execution remains blocked. |
| Copy generated host skills into `.claude`, `.codex`, `.opencode`, or user home | Host registration and normal-user-home writes are blocked. |
| Launch browser daemon, Playwright, Chromium, CDP, ngrok, or pair-agent | Browser/remote runtime is blocked by default. |
| Use provider CLIs, SDKs, APIs, credentials, cookies, or MCP | Provider/credential/MCP surfaces are blocked by default. |
| Sync GBrain or write memory | Memory write/sync requires future exact memory authority gate. |
| Stage, commit, push, release, deploy, or mutate Git | Git/release skill surfaces are blocked by default. |

Decision marker:

```text
gstack_readonly_skill_source_consumed
```

## 7. No-Runtime Bootstrap Path

Initial bootstrap does not require GStack setup.

P12.10 may create a project-local skeleton under an explicitly approved path such as:

```text
3_platform/_governed_skeleton/agent_platform_mvp0/skills/
```

Candidate skeleton shape for P12.10:

```text
3_platform/_governed_skeleton/agent_platform_mvp0/skills/
  README.md
  registry/skill_registry.yaml
  blueprints/<skill_id>/skill.blueprint.yaml
  blueprints/<skill_id>/instructions.md
  blueprints/<skill_id>/gate_map.md
```

This path is a future candidate only. P12.8 does not create it.

P12.10 no-runtime bootstrap sequence:

| Step | Action | Boundary |
| --- | --- | --- |
| 1 | Create approved project-local skill skeleton files. | File writes by P12.10 implementation only, not by a skill runtime. |
| 2 | Create static `SkillBlueprint` records for selected S0/S1/S2 candidates. | No generated import from GStack. |
| 3 | Create static registry entries. | Registry is inactive and non-executable. |
| 4 | Attach source refs and P12.4/P12.6/P12.7 governance refs. | Citations required. |
| 5 | Mark S3+ concepts as blocked future candidates. | No runtime bridge. |
| 6 | Verify markers and path scope. | No tests, builds, setup, browser, provider, memory write, or Git staging. |

No-runtime bootstrap means:

```text
manual internal blueprint authoring
static registry only
project-local skeleton only
S0/S1/S2 initial candidates only
no active dispatcher
no slash-command invocation
no GStack setup
no host skill installation
no generated skill import
no provider/browser/MCP/runtime execution
```

Decision marker:

```text
no_runtime_skill_bootstrap_path_defined
```

## 8. Internal Skill Blueprint Model

The internal unit is `SkillBlueprint`.

`SkillBlueprint` is a static design record. It is not executable code, not a prompt injection authority, not a permission grant, not a host skill registration, and not a memory writer.

Required model:

```yaml
SkillBlueprint:
  id: "skill.<domain>.<name>"
  title: "<human-readable name>"
  status: "candidate | reviewed | inactive_registered | blocked | superseded"
  lifecycle_state: "source_evidence | blueprint_candidate | reviewed_blueprint | inactive_registry_entry | gated_future_candidate | retired"
  source_refs:
    - source_system: "gstack | agent_platform | other"
      path: "<repo-relative source path>"
      evidence_kind: "taxonomy | workflow_pattern | packaging_pattern | risk_boundary | governance"
      authority_tier: "evidence_only | governance_authority"
  purpose: "<what the skill helps structure>"
  non_goals:
    - "<explicitly blocked behavior>"
  taxonomy:
    family: "planning | review | debug | docs | release | context | memory | browser | device | safety | packaging"
    tags: []
  runtime_profile: "S0 | S1 | S2 | S3 | S4 | S5 | S6"
  permission_classes:
    allowed_now: []
    candidate_only: []
    blocked: []
  required_future_gates: []
  memory_boundary:
    can_read_memory_refs: false
    can_write_memory: false
    can_sync_gbrain: false
    memory_update_output: "request_only | none"
  output_boundary:
    allowed_output_classes: []
    blocked_output_classes: []
    promotion_required: true
  inputs:
    allowed: []
    blocked: []
  command_candidates:
    allowed_to_propose: false
    exact_command_required: true
    execution_allowed: false
  file_write_boundary:
    allowed_to_write: false
    allowed_paths: []
  runtime_boundary:
    execution_allowed: false
    browser_allowed: false
    mcp_allowed: false
    provider_allowed: false
    git_allowed: false
  audit_refs:
    governance_refs: []
    review_refs: []
  p12_10_bootstrap_action: "create_blueprint | register_inactive | block_future | defer"
```

Blueprint invariants:

| Invariant | Requirement |
| --- | --- |
| One skill, one blueprint | Each skill concept gets one primary blueprint ID. |
| Source refs required | External inspiration must cite source paths or governance refs. |
| Runtime profile required | Every blueprint must declare S0-S6. |
| Permission classes required | Every blueprint must map to P12.4 permission classes. |
| Blocked surfaces explicit | Browser/MCP/provider/memory/Git/hook/settings surfaces must be listed when relevant. |
| Output posture explicit | Outputs must be classified as generated evidence, review support, command candidates, draft docs, or future runtime output. |
| Lifecycle explicit | Registry inclusion does not imply activation. |
| No authority escalation | No blueprint can approve itself, promote outputs, or bypass gates. |

Decision marker:

```text
internal_skill_blueprint_model_defined
```

## 9. Skill Registry Bootstrap Model

The skill registry is a static index over `SkillBlueprint` records.

The registry may contain:

| Field | Purpose |
| --- | --- |
| `id` | Stable blueprint ID. |
| `title` | Human-readable name. |
| `registry_status` | `inactive`, `review_only_candidate`, `command_candidate_only`, `blocked_future`, `superseded`. |
| `blueprint_path` | Project-local path to blueprint record. |
| `source_refs` | Governance and external evidence refs. |
| `runtime_profile` | P12.4 S0-S6 profile. |
| `permission_summary` | Allowed, candidate-only, and blocked permission classes. |
| `required_future_gates` | Exact gates required before activation. |
| `memory_posture` | No memory authority and no writes by default. |
| `output_posture` | Output classes and promotion requirements. |
| `owner_or_review_role` | Future human/governance review role, not runtime owner. |
| `last_review_ref` | Optional future review record. |

Registry non-goals:

```text
no slash command dispatch
no host skill registration
no execution routing
no automatic prompt injection
no file generation
no memory writes
no browser/MCP/provider binding
no Git automation
```

Registry statuses:

| Status | Meaning | Execution posture |
| --- | --- | --- |
| `inactive` | Cataloged for review only. | No execution. |
| `review_only_candidate` | May be used as documentation/planning guidance after review. | S0/S1 only. |
| `command_candidate_only` | May propose exact commands as candidates. | S2 only; no execution. |
| `blocked_future` | Valuable concept but requires S3+ or blocked surface. | No execution. |
| `superseded` | Replaced by a newer blueprint. | No execution. |

Decision marker:

```text
skill_registry_bootstrap_model_defined
```

## 10. Skill Lifecycle Model

Lifecycle states:

| State | Entry condition | Exit condition | Allowed actions |
| --- | --- | --- | --- |
| `source_evidence` | External or governance source identified. | Source reviewed and mapped. | Read-only citation and classification. |
| `blueprint_candidate` | Internal blueprint drafted. | P12.4/P12.6/P12.7 alignment reviewed. | Edit blueprint metadata. |
| `reviewed_blueprint` | Source refs, profile, gates, memory, and output boundaries are complete. | Registry entry accepted. | Static review/planning use only if S0/S1. |
| `inactive_registry_entry` | Added to registry as non-executable catalog item. | Future exact gate approves activation path. | Search/read registry only. |
| `command_candidate_only` | S2 blueprint accepted for exact command proposal. | Separate execution gate approves exact command. | Propose exact commands only. |
| `gated_future_candidate` | Skill needs S3+ or blocked permissions. | Future gate creates exact controlled activation plan. | Keep blocked; cite gate requirements. |
| `retired` | Skill is obsolete or unsafe. | Supersession record accepted. | Preserve audit/source refs only. |

Lifecycle transition rules:

| Rule | Requirement |
| --- | --- |
| Source evidence does not activate skill. | Reading GStack docs or templates cannot create a runnable skill. |
| Registry entry does not activate skill. | Static catalog presence is not execution permission. |
| S0/S1 review use requires source review. | Planning guidance must cite source refs and boundaries. |
| S2 command candidates require exactness. | Commands must include command, cwd, inputs, outputs, risks, and gate reference. |
| S3+ requires future gate. | File writes, tool execution, browser/MCP/provider, memory writes, and Git remain blocked. |
| Memory writes require memory gate. | Skill cannot write memory even if registry entry exists. |
| Output promotion requires governance review. | Skill output cannot become authority by default. |

Decision marker:

```text
skill_lifecycle_model_defined
```

## 11. Skill Taxonomy Mapping

GStack categories map to AGENT PLATFORM taxonomy as design input only.

| GStack category | Example concepts from GStack evidence | AGENT PLATFORM family | Initial P12.10 posture | Blocked surfaces |
| --- | --- | --- | --- | --- |
| Plan-mode reviews | office-hours, CEO review, eng review, design review, devex review, spec | `planning_review` | S1 review/planning candidate; S2 only for exact command/spec candidates | Auto-orchestration, issue filing, remote agent spawn, GitHub actions, tool execution. |
| Implementation + review | review, codex, investigate, design-review, QA, scrape, skillify | `implementation_review_debug` | S1 for review/debug methodology; S2 for command candidates | Codex/provider calls, browser runtime, fixes, file writes, generated browser skills. |
| Release + deploy | ship, land-and-deploy, canary, landing-report, document-release, setup-deploy | `release_docs_deploy` | S1 for release checklist/docs concepts; S2 for command candidates only | Tests, CI, push, PR, merge, deploy, production monitoring, Git mutation. |
| Operational + memory | context-save, context-restore, learn, retro, health, benchmark, cso, setup-gbrain, sync-gbrain | `context_memory_observability` | S1 for context review/checklists; S2 for command candidates only | Memory writes, GBrain sync, tests, benchmarks, provider/model comparisons, security scan execution. |
| Browser + agent integration | browse, open browser, setup cookies, pair-agent | `browser_remote_agent` | Blocked future S5 candidate | Browser daemon, cookies, CDP, ngrok, remote agents, token handling. |
| iOS QA/device automation | ios-qa, ios-fix, ios-design-review, ios-clean, ios-sync | `device_qa_remote` | Blocked future S5/S6 candidate | USB/tunnel runtime, device mutation, release cleanup, generated bridge sync. |
| Safety + scoping | careful, freeze, guard, unfreeze, make-pdf, diagram | `safety_scope_docs` | S1 advisory safety/checklist; S2 command candidates only | Hook enforcement, settings mutation, file locks, PDF/diagram generation, destructive command enforcement. |
| Packaging conventions | generated `SKILL.md`, templates, host skill directories | `skill_packaging` | S0/S1 design reference | Generated import, host install, user home writes, GStack script execution. |

Taxonomy rules:

| Rule | Requirement |
| --- | --- |
| Prefer internal names | AGENT PLATFORM skill IDs must not imply GStack runtime dependency. |
| Preserve source refs | GStack-origin concepts must cite GStack source evidence. |
| Separate concept from execution | A useful workflow pattern can be adopted while its runtime remains blocked. |
| Split risky skills | A GStack skill with review and runtime behavior must become separate AGENT PLATFORM blueprints, such as S1 review and blocked S5 runtime. |
| Mark blocked features explicitly | Browser, provider, memory, deploy, Git, and hook features cannot hide inside S1/S2 blueprints. |

Decision marker:

```text
skill_taxonomy_mapping_defined
```

## 12. Runtime Profile Mapping

P12.8 consumes P12.4 runtime profiles directly.

| P12.4 profile | Bootstrap treatment | P12.10 initial eligibility | Notes |
| --- | --- | --- | --- |
| S0 - Documentation-only skill | Allowed as reviewed documentation/source evidence. | Eligible. | No execution, writes, external calls, memory writes, or Git mutation. |
| S1 - Review/planning skill | Allowed after source/license/trust review and scope acceptance. | Eligible. | Structures review, critique, planning, or checklist output only. |
| S2 - Command-suggesting skill | Allowed only as exact command candidate model. | Eligible with caution. | Commands are never executed by the skill; execution requires separate gate. |
| S3 - Local file-writing skill | Blocked in initial skill bootstrap. | Not eligible. | Future file-write gate required. |
| S4 - Local tool-execution skill | Blocked in initial skill bootstrap. | Not eligible. | Future local tool execution gate required. |
| S5 - Browser/MCP/provider skill | Blocked by default. | Not eligible. | Requires high-risk browser/MCP/provider/credential/network gate. |
| S6 - Git/deploy/production skill | Blocked by default. | Not eligible. | Requires exact human approval, Git/deploy gate, rollback, and production safety policy. |

Initial profile rule:

```text
P12.10 may bootstrap S0, S1, and tightly bounded S2 blueprints only. S3, S4, S5, and S6 concepts may be cataloged as blocked future candidates, but must not be implemented, invoked, registered, or simulated as runtime.
```

Decision marker:

```text
skill_runtime_profile_mapping_defined
```

## 13. Permission Gate Mapping

P12.8 maps P12.4 permission classes into bootstrap posture.

| Permission class | P12.10 initial posture | Required future gate before use |
| --- | --- | --- |
| `SKILL_READ_DOCS` | Allowed after source review. | Source/license/trust review. |
| `SKILL_READ_SOURCE_METADATA` | Allowed after source review. | Source metadata review. |
| `SKILL_READ_SOURCE_BODY` | Gated; use already reviewed evidence unless exact source inspection is approved. | Exact source inspection gate. |
| `SKILL_WRITE_APPROVED_FILES` | Skill cannot use it; P12.10 implementation may write approved skeleton paths only. | File-write gate with allowed path list, diff review, rollback. |
| `SKILL_RUN_LOCAL_COMMANDS` | Blocked. | Local tool execution gate with exact command list. |
| `SKILL_RUN_TESTS` | Blocked. | Test execution gate. |
| `SKILL_USE_BROWSER` | Blocked. | Browser runtime gate. |
| `SKILL_USE_MCP` | Blocked. | MCP execution/registration gate. |
| `SKILL_USE_PROVIDER` | Blocked. | Provider/API gate. |
| `SKILL_USE_CREDENTIALS` | Blocked. | Credential access gate. |
| `SKILL_WRITE_MEMORY` | Blocked. | Memory authority gate. |
| `SKILL_REGISTER_HOOKS` | Blocked. | Hook registration gate. |
| `SKILL_MODIFY_SETTINGS` | Blocked. | Settings mutation gate. |
| `SKILL_MUTATE_GIT` | Blocked. | Git mutation gate plus exact human approval. |
| `SKILL_DEPLOY` | Blocked. | Deployment/production safety gate. |

Gate mapping rule:

```text
The registry records required gates. The registry does not satisfy gates.
```

Decision marker:

```text
skill_permission_gate_mapping_defined
```

## 14. Memory Boundary

P12.8 preserves P12.7 and P12.4 memory boundaries.

Skill memory rules:

| Rule | P12.8 design posture |
| --- | --- |
| Skills are not memory authority. | Required invariant. |
| GStack is not memory authority. | Required invariant from P12.6. |
| GBrain remains derived retrieval/index infrastructure. | Required invariant from P12.7. |
| Skill memory writes are blocked. | `SKILL_WRITE_MEMORY` requires future memory authority gate. |
| GBrain sync is blocked. | `/setup-gbrain` and `/sync-gbrain` concepts are blocked future candidates. |
| Normal user memory/state writes are blocked. | No `.gbrain`, `.gstack`, `.claude`, `.codex`, or user-home writes. |
| Memory suggestions are request-only. | A skill may produce a memory update request candidate, not perform the write. |

Allowed memory-related output for S0/S1/S2:

```yaml
MemoryUpdateRequestCandidate:
  source_skill_id: "<blueprint id>"
  requested_change: "<human-readable request>"
  cited_sources: []
  authority_claim: false
  write_performed: false
  required_future_gate: "memory authority gate"
```

Blocked memory actions:

```text
write operational memory
write GBrain production memory
sync GBrain
register remote GBrain MCP
inspect or write normal user .gbrain
inspect or write normal user .gstack
promote generated evidence into memory
reindex memory
clean memory
```

Decision marker:

```text
skill_memory_boundary_preserved
```

## 15. Output Boundary

P12.8 preserves P12.4 output classification.

Allowed S0/S1/S2 output classes:

| Output class | Bootstrap posture |
| --- | --- |
| `source evidence` | Allowed only with citation and no authority escalation. |
| `review support` | Allowed for S1 planning/review blueprints. |
| `command candidates` | Allowed for S2 only; exact command metadata required; no execution. |
| `draft documentation` | Allowed as draft output; not accepted authority until reviewed. |
| `memory update request` | Allowed as request-only generated evidence; no write. |

Blocked or future-gated output classes:

| Output class | Reason |
| --- | --- |
| `draft implementation` | Requires file-write scope and diff review. |
| `runtime output` | Requires execution gate. |
| `browser/provider/MCP output` | Sensitive generated evidence; requires high-risk gates. |
| `Git/deploy audit evidence` | Requires Git/deploy gate and exact human approval. |
| `accepted governance/source record` | Requires governance review and promotion path. |

Output promotion requirements:

```text
exact source
classification
scope check
sensitive-content check
conflict check
human review
accepted governance/source record
tracking decision
rollback posture
```

Decision marker:

```text
skill_output_boundary_preserved
```

## 16. GStack Setup Decision

Initial bootstrap does not require GStack setup.

Rationale:

| Evidence | Decision |
| --- | --- |
| P12.6 adopts GStack as read-only skill source candidate. | Runtime inspection is not required for taxonomy and blueprint design. |
| `AGENTS.md` provides enough taxonomy evidence. | P12.8 can map categories without generated skill import. |
| `package.json` and `BROWSER.md` expose high-risk runtime surfaces. | Setup/runtime would add risk without solving P12.8 design needs. |
| P12.4 defines internal profiles and gates. | AGENT PLATFORM can define its own governed skill model. |

P12.2A is required only if a future task needs one or more of these:

```text
run GStack setup
install dependencies
run Bun, Node, package manager, build, test, or generation scripts
inspect runtime-generated host skill directories
launch or test GStack browser runtime
invoke GStack skills
validate GStack command behavior
write to user homes or host skill directories
use provider/MCP/browser/cookie/ngrok/token surfaces
sync GBrain through GStack
mutate GStack source or settings
```

P12.8 conclusion:

```text
P12.2A is not required for initial P12.10 no-runtime skill stack bootstrap.
```

Decision marker:

```text
gstack_setup_not_required_for_initial_bootstrap
```

## 17. P12.10 Handoff

P12.8 hands off to:

```text
P12.10 - Skill Stack Bootstrap Spike
```

P12.10 should require:

| Requirement | Rule |
| --- | --- |
| P12.8 accepted | `skill_stack_bootstrap_design_ready` must be present. |
| Exact path scope | Use only approved project-local skeleton paths. |
| Initial profiles | S0/S1/S2 only. |
| Static registry | Registry is inactive and non-executable. |
| Static blueprints | Blueprints cite source refs and gates. |
| No runtime | No GStack setup, skill execution, tool execution, browser, MCP, provider, memory write, or Git mutation. |
| S3+ handling | Catalog as blocked future candidates only. |
| Output posture | Outputs are generated evidence/review support/command candidates/draft docs only. |

Candidate P12.10 seed blueprints:

| Candidate | Family | Initial profile | Notes |
| --- | --- | --- | --- |
| `skill.planning.request_review` | `planning_review` | S1 | Planning/review checklist, no commands. |
| `skill.review.architecture` | `implementation_review_debug` | S1 | Architecture/code-review methodology, no file writes. |
| `skill.debug.investigation` | `implementation_review_debug` | S1/S2 | Investigation steps and optional exact command candidates. |
| `skill.safety.command_review` | `safety_scope_docs` | S1/S2 | Advisory destructive-command review; no enforcement hook. |
| `skill.docs.release_notes_candidate` | `release_docs_deploy` | S1/S2 | Documentation/release checklist; no Git/deploy. |
| `skill.memory.update_request` | `context_memory_observability` | S1 | Memory update request candidate only; no write. |

P12.10 must not create an execution runtime. If P12.10 discovers that runtime behavior is necessary, it must stop and require P12.2A or a more specific future controlled setup/execution gate.

Decision marker:

```text
p12_10_skill_stack_bootstrap_spike_ready_after_design
```

## 18. Stop Rules

Stop if work requires any of the following:

| Stop condition | Required response |
| --- | --- |
| Install or run GStack. | Require P12.2A or equivalent controlled setup/runtime plan. |
| Run `./setup`, `bun install`, `bun run`, tests, builds, or generation scripts. | Stop; dependency/runtime side effects are not approved. |
| Invoke skills or slash commands. | Require P12.4-aligned execution gate. |
| Register hooks, host skills, MCP servers, or settings. | Require exact future gate with rollback. |
| Launch browser daemon, Playwright, Chromium, CDP, ngrok, pair-agent, or device tunnels. | Require high-risk browser/device/remote runtime gate. |
| Inspect or use credentials, cookies, provider configs, token stores, or API keys. | Preserve credential boundary and stop. |
| Call providers, provider CLIs, SDKs, APIs, or model benchmarks. | Require provider/API gate. |
| Sync GBrain, write memory, reindex memory, or write user memory stores. | Require memory authority gate. |
| Write outside approved P12.10 skeleton paths. | Require exact path/file-write approval. |
| Mutate Git, stage, commit, push, deploy, or release. | Require exact human approval and Git/deploy gate; never `git add .`. |
| Treat registry inclusion as activation. | Stop; registry is static and inactive. |
| Treat skill output as authority. | Stop; output requires promotion review. |

## 19. Acceptance Criteria Mapping

| Criterion | Status |
| --- | --- |
| Creates exactly one governance design file. | Satisfied by this file only. |
| Confirms P12.2 dependency. | Satisfied. |
| Confirms P12.4 dependency. | Satisfied. |
| Confirms P12.6 dependency. | Satisfied. |
| Confirms P12.7 dependency. | Satisfied. |
| Consumes GStack only as read-only skill source candidate. | Satisfied. |
| Defines no-runtime bootstrap path. | Satisfied. |
| Defines internal skill blueprint model. | Satisfied. |
| Defines static registry model. | Satisfied. |
| Defines lifecycle model. | Satisfied. |
| Maps GStack taxonomy to AGENT PLATFORM taxonomy. | Satisfied. |
| Maps runtime profiles. | Satisfied. |
| Maps permission gates. | Satisfied. |
| Preserves memory boundary. | Satisfied. |
| Preserves output boundary. | Satisfied. |
| States GStack setup is not required for initial bootstrap. | Satisfied. |
| Hands off to P12.10. | Satisfied. |
| Does not install or run GStack. | Satisfied. |
| Does not execute skills or tools. | Satisfied. |
| Does not register hooks, MCP, browser daemon, provider, host skills, or settings. | Satisfied. |
| Does not write memory. | Satisfied. |
| Does not mutate Git. | Satisfied. |

## 20. Files Created

Created exactly one governance design file:

```text
0_architecture/governance/agent_platform_skill_stack_bootstrap_design.md
```

## 21. Files Modified

No existing file was modified.

## 22. Commands / Runtime Actions

No GStack command, setup script, package manager, runtime binary, skill, provider CLI, MCP command, browser daemon, test, build, install, credential inspection, environment secret inspection, staging command, or Git mutation was run by this design.

Allowed verification after file creation:

```text
git status --short
```

Explicitly not run:

```text
gstack
gstack --help
gstack --version
./setup
setup
browse
make-pdf
bun install
bun run
bun build
bun test
npm
node
npx
python
pip
cargo
go
deno
docker
ollama
/graphify
provider commands
MCP servers
browser daemons
ngrok
tests
builds
scripts
CI
```

## 23. Final Decision

P12.8 defines a no-runtime governed skill stack bootstrap architecture. GStack is consumed only as read-only taxonomy, workflow, packaging, and risk-boundary evidence. AGENT PLATFORM should bootstrap internal project-local `SkillBlueprint` records and an inactive static `SkillRegistry` before any runtime. Initial P12.10 work may create S0/S1/S2 blueprints and registry entries only; S3+ and all browser/MCP/provider/memory/Git/deploy surfaces remain blocked pending future exact gates.

Final marker:

```text
skill_stack_bootstrap_design_ready
```
