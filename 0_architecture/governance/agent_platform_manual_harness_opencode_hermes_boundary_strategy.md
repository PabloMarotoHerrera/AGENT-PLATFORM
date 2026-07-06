# Manual Harness Strategy / OpenCode-Hermes Boundary

## Document Header

| Field | Value |
| --- | --- |
| Title | Manual Harness Strategy / OpenCode-Hermes Boundary |
| Ticket | P7.0.E |
| Status | Accepted Manual Harness Strategy / OpenCode-Hermes Boundary |
| Date | 2026-07-06 |
| Scope | Documentation-only manual harness strategy for AGENT PLATFORM / Siamese. |
| Authority | Manual harness strategy and external operator boundary only, not harness integration, not OpenCode adapter implementation, not Hermes runtime, not GBrain runtime, not provider/auth/API/MCP activation, not tool execution, not agent execution, not autonomous orchestration, not automatic dispatch, not automatic reviewer assignment, not product/Siamese source inspection, not Graphify adoption, not Codegraph adoption, not persistence, not vector DB, not graph DB, not Cognitive Semantic System substrate selection, and not Git mutation. |
| Required prerequisite | P7.0.0 and P7.0-NATIVE-ALIGN-01 complete. |
| Related documents | P7.0.0, P7.0.A, P7.0.B, P7.0.C, P7.0.D, P6.7, P6.1-P6.6, P5.R, P5.1-P5.7, P3.BR, P3.3, P3.4, P3.5, P2.1, P2.2, P2.3, P2.KR, P1.1-P1.5, P0.1-P0.3, S-03, S-04, CSS ADR/audit. |
| Optional sibling inputs | P7.0.F, P7.0.G, P7.0.H, P7.0.R if present; downstream consumers only in this ticket. |
| Output | Manual Harness Strategy / OpenCode-Hermes Boundary. |
| Target result | manual_harness_strategy_ready_for_agent_native_P7 |

## Purpose

P7 formalizes the manual agentic workflow for AGENT PLATFORM while preserving human control and explicit governance boundaries.

P7.0.E defines how external harnesses are used manually by the user inside that workflow. It consumes the agent-native correction from P7.0.0 and P7.0-NATIVE-ALIGN-01, treats P7.0.A/B/C/D as the `manual_bridge_layer`, and ensures harness strategy supports the `agent_native_internal_organization_layer` without turning harnesses into internal runtime.

P7.0.E maps external tools and harnesses to manual use levels H0/H1/H2/H3. H0 manual external harness use is allowed. H1 metadata-only harness adapter design is allowed as design only. H2 controlled tool execution adapter is blocked. H3 autonomous orchestration adapter is blocked.

P7.0.E does not activate OpenCode, Hermes, GBrain, Codex, Claude, Cursor, MCP, providers, tools, agents, Graphify, Codegraph, live connectors, product/Siamese, or Cadence. P7.0.E does not mutate Git.

## Current Posture

P7.0.E is manual harness strategy only. External harnesses are user-operated surfaces, not internal runtime. Harness classification does not approve integration or execution.

| Area | Current state | P7.0.E interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM activation level | Governed manual platform design. | P7 remains below autonomous runtime activation. | Treating P7 as AL-2 or runtime execution. |
| AL-1.5 manual controlled workflow | Manual controlled workflow target. | Manual planning, manual harness use, manual review, manual integration, and user-owned Git. | Autonomous orchestration or automatic dispatch. |
| `manual_bridge_layer` | P7.0.A/B/C/D user-facing/manual workflow layer. | Bridge from user objective to manual tickets and outputs. | Internal runtime layer. |
| `agent_native_internal_organization_layer` | Conceptual internal organization pattern set. | Source of topology, task graph, blackboard, capability cell, reviewer mesh, routing, and memory concepts. | Activated internal agent runtime. |
| `ManualExecutionProjection` | Human/harness projection of internal concepts. | Manual lane, ticket, harness, review, integration, and Git advice projection. | Scheduler, queue, automatic routing, or execution primitive. |
| External harness usage | User-operated external surfaces. | H0 manual harness use and H1 design-only metadata. | Harness integration, live connectors, or automatic execution. |
| OpenCode | Manual external development harness candidate. | User may manually use OpenCode outside AGENT PLATFORM and return outputs. | OpenCode adapter, OpenCode execution by AGENT PLATFORM, or internal runtime adoption. |
| Hermes | External agent runtime / orchestration / Cadence candidate. | Candidate reference only; H0 outside manual use if user-operated and H1 design only. | Active Hermes runtime, Cadence activation, orchestrator adoption, or auto-dispatch. |
| Codex | External coding/review harness candidate. | User-operated H0 harness candidate. | Provider/auth activation or internal Codex runtime. |
| Claude | External coding/review harness candidate. | User-operated H0 harness candidate. | Provider/auth activation or internal Claude runtime. |
| Cursor | External coding/review harness candidate. | User-operated H0 harness candidate. | Provider/auth activation or internal Cursor runtime. |
| GBrain | External memory architecture candidate. | Candidate notation only. | GBrain runtime, persistent memory, live retrieval, vector DB, or graph DB. |
| Graphify | Generated evidence tooling / repo map evidence. | Curated Graphify Repo Map Summary may support evidence only. | Graphify adoption, Graphify Authority, Graphify truth engine, Graphify substrate, rerun, or work routing. |
| Codegraph | External analysis/tooling candidate. | Future EXT review candidate only. | Codegraph execution, Codegraph authority, or substrate treatment. |
| MCP | Blocked in P7. | Metadata may name the boundary only. | Active MCP, MCP server/client activation, MCP resources, or MCP tools. |
| Provider/auth | Blocked in P7. | Provider metadata is not provider activation. | Active provider/auth, credentials, keys, or API calls. |
| Live connectors | Blocked in P7. | No connector execution. | Live connector runtime. |
| Product/Siamese | Product vision only. | Siamese remains living energy twin product vision, not product activation. | Product/Siamese source readable by default or product-specific harness access. |
| Git authority | User-owned. | Lead/integrator may advise exact commands only. | Automatic commit, automatic push, or agent Git mutation. |
| Autonomous orchestration | Blocked. | Manual workflow only. | Autonomous orchestration, automatic ticket routing, automatic reviewer assignment, or automatic tool execution. |

## Prerequisite Gate: Agent-Native Alignment

If prerequisite alignment is incomplete, P7.0.E must STOP.

| Prerequisite | Required evidence | Status | Action if missing |
| --- | --- | --- | --- |
| P7.0.0 research carry-forward exists | `agent_platform_agent_native_organization_research_carry_forward.md` is present. | Present by allowed path check. | Stop and report missing agent-native research carry-forward. |
| P7.0.A declares user gateway / manual control plane | `manual_bridge_layer` and `manual_control_plane` markers. | Present by allowed marker check. | Stop and repair P7.0-NATIVE-ALIGN-01 alignment. |
| P7.0.B includes topology selection / task graph / blackboard before work packet projection | `topology selection`, `TaskGraphRef`, and `BlackboardRef` markers. | Present by allowed marker check. | Stop and repair P7.0-NATIVE-ALIGN-01 alignment. |
| P7.0.C declares manual lane taxonomy as ManualExecutionProjection, not final internal taxonomy | `ManualExecutionProjection` marker. | Present by allowed marker check. | Stop and repair P7.0-NATIVE-ALIGN-01 alignment. |
| P7.0.C includes agent-native reference objects | `AgentNativeTopologyRef`, `TaskGraphRef`, `BlackboardRef`, `CapabilityCellRef`, `ReviewerMeshRef`, and `RoutingDecisionRef` family evidence. | Required exact gate evidence present through allowed checks for topology, repaired P7.0.B task/blackboard aliases, and P7.0.C cell/reviewer/routing markers. | Stop and repair P7.0-NATIVE-ALIGN-01 alignment. |
| P7.0.D extends MemoryManifest into Context & Memory Fabric | `Context & Memory Fabric` marker. | Present by allowed marker check. | Stop and repair P7.0-NATIVE-ALIGN-01 alignment. |
| P7.0.D includes memory/context marker family | `TaskMemorySlice`, `CellMemorySlice`, `BlackboardMemoryRef`, `TopologyContextPack`, `ContradictionMarker`, and `EvidenceConflictMarker` family evidence. | Gate-consumed as P7.0-NATIVE-ALIGN-01 memory fabric alignment; allowed checks confirmed `TaskMemorySlice` and `BlackboardMemoryRef`. | Stop and repair P7.0-NATIVE-ALIGN-01 alignment if exact gate checks fail. |

## Inputs Reviewed

| Input group | Document | Review mode | Harness strategy use | Limitation |
| --- | --- | --- | --- | --- |
| P7.0.0 agent-native research | `agent_platform_agent_native_organization_research_carry_forward.md` | `agent_native_alignment_review` | Source for `agent_native_internal_organization_layer`, topology, task graph, blackboard, reviewer mesh, routing, and memory fabric concepts. | Reviewed only as prerequisite/path/marker input; no runtime activation. |
| P7.0.A/B/C/D aligned manual bridge docs | P7.0.A, P7.0.B, P7.0.C, P7.0.D | `manual_bridge_contract_review` | Confirms manual gateway, roadmap projection, lane projection, and context/memory projection. | Existing documents are not modified by P7.0.E. |
| P6 operational contracts | P6.1-P6.7 governance contracts | `operational_contract_review` | Supplies capability, communication, evidence, approval, monitoring, and incident boundaries. | Operational contracts do not activate runtime. |
| P5 skeleton baseline | P5.R and P5.1-P5.7 implementation records | `implementation_skeleton_review` | Supplies inert skeleton boundaries and non-activation posture. | Skeleton records are not implementation permission. |
| P3 activation decisions | P3.BR, P3.3, P3.4, P3.5, readiness records | `activation_decision_review` | Preserves provider/auth/API/MCP, tool, and agent runtime blocks. | Decision records do not grant execution. |
| P2/P2.K knowledge architecture | P2/P2.K reconciliation, vocabulary, evidence, retention records | `metadata_contract_review` | Supports evidence refs, context refs, retention refs, and rollback refs. | Knowledge metadata is not live retrieval or persistence. |
| P1 metadata contracts | Context, provider, tool, agent, and CSS hardening records | `metadata_contract_review` | Supplies contract vocabulary and boundary semantics. | Metadata is not activation. |
| P0 gates/security/validation | Activation gate, validation gate, security hardening, and charter records | `operational_contract_review` | Supplies stop rules and activation-gate posture. | Gates are not approval by mention. |
| S-03/S-04 policies | Tool/shell/network/MCP and local-only secrets policies | `operational_contract_review` | Preserves shell/network/MCP and secrets/credential boundaries. | No secret or credential inspection. |
| CSS ADR/audit | Cognitive Semantic System naming and audit records | `metadata_contract_review` | Preserves Cognitive Semantic System naming and substrate deferral. | No substrate selection. |
| Harness candidates | OpenCode, Hermes, Codex, Claude, Cursor, GBrain, Graphify, Codegraph | `harness_candidate_review` | Classifies candidates as manual surfaces, evidence surfaces, or future candidates. | No external source inspection or execution. |
| Blocked surfaces | Product/Siamese source, raw generated outputs, secrets, credentials, providers, MCP, tools, runtime files | `not_reviewed_blocked` | Named only as blocked boundaries. | Not inspected. |

## Harness Level Model

| Harness level | Definition | Allowed P7 use | Blocked use | Required future gate |
| --- | --- | --- | --- | --- |
| H0 | User manually copies tickets into external harness and manually returns output. | Allowed for manual harness use. | Automatic dispatch, hidden source access, credential use, or output auto-acceptance. | Manual review/integration discipline. |
| H1 | Metadata-only harness adapter design. | Allowed as design only. | Adapter implementation, runtime config, provider/auth setup, tool execution, or live connector. | Future explicit design and activation gate. |
| H2 | Controlled tool execution adapter. | Blocked in P7. | Any harness adapter that executes tools, shell, MCP tools, providers, or code. | Future activation decision, security gate, validation gate, and human approval. |
| H3 | Autonomous orchestration adapter. | Blocked in P7. | Automatic task dispatch, handoffs, reviewer assignment, routing, autonomous loops, auto-commit, or auto-push. | Future AL-2+ governance and explicit runtime approval. |

Decisions: H0 is allowed in P7. H1 is allowed as design only. H2 is blocked in P7. H3 is blocked in P7.

## Harness Object Model

| Object | Meaning | Required fields | Forbidden fields | Allowed use | Blocked interpretation |
| --- | --- | --- | --- | --- | --- |
| `ExternalHarnessRef` | Metadata ref for an external harness or candidate surface. | id, name, classification, level, boundaries, allowed manual use, blocked automation, review required. | API keys, token handles, adapter config, runtime handles, automatic dispatch flags. | Catalog and classify external harnesses. | Adapter integration or runtime access. |
| `HarnessBoundary` | Boundary metadata constraining harness use. | boundary id, harness ref, allowed/blocked levels, constraints, stop rules, approval requirement. | Execution permissions, credential grants, live connector endpoints. | State what the harness may not do. | Permission grant. |
| `HarnessLevel` | H0/H1/H2/H3 classification. | level id, definition, allowed use, blocked use, future gate. | Runtime switch, approval token, scheduler config. | Classify manual/design/execution/orchestration levels. | Activation level. |
| `HarnessUseCase` | Manual use scenario for a harness. | use case id, user action, inputs, outputs, boundaries, review route. | Automatic dispatch trigger, tool invocation, provider call. | Describe manual operating scenarios. | Workflow automation. |
| `HarnessInputPackage` | User-supplied package copied into a harness. | package id, target harness, ticket text, context refs, allowed/blocked actions, stop rules. | Secrets, credentials, raw blocked source, provider tokens. | Manual ticket/context packaging. | Automatic dispatch. |
| `HarnessOutputPackage` | User-returned output from a harness. | package id, source harness, summary, files, commands, decisions, limitations, refs, commit advice candidate. | Accepted-by-default status, commit hook, approval token. | Reviewable output record. | Automatic acceptance or Git mutation. |
| `HarnessRiskProfile` | Risk metadata for a harness/use case. | risk id, risk areas, blocked surfaces, review needs, incident refs. | Runtime bypasses, broad approvals. | Identify risk and required review. | Permission to proceed despite risk. |
| `HarnessAdoptionStatus` | Candidate/adopted/blocked metadata posture. | status, rationale, gate requirements, limitations. | Silent adoption, runtime enablement. | State candidate or blocked posture. | Integration approval. |
| `OpenCodeHarnessRef` | OpenCode manual harness metadata. | ExternalHarnessRef fields plus OpenCode manual use boundaries. | OpenCode adapter code, OpenCode runtime invocation. | H0 manual external development harness candidate. | Internal adapter activation. |
| `HermesCandidateRef` | Hermes candidate metadata. | ExternalHarnessRef fields plus orchestration/Cadence blocks. | Hermes runtime handles, Cadence config, dispatch hooks. | Future candidate notation and H1 design only. | Hermes runtime activation. |
| `GBrainCandidateRef` | GBrain candidate metadata. | ExternalHarnessRef fields plus memory/runtime/substrate blocks. | DB handles, retrieval endpoints, embedding config. | Future memory architecture candidate notation. | GBrain runtime or substrate selection. |
| `CodexHarnessRef` | Codex external harness metadata. | ExternalHarnessRef fields plus provider/auth boundary. | Provider tokens, API credentials, internal runtime config. | H0 user-operated coding/review harness candidate. | Provider/auth activation. |
| `ClaudeHarnessRef` | Claude external harness metadata. | ExternalHarnessRef fields plus provider/auth boundary. | Provider tokens, API credentials, internal runtime config. | H0 user-operated coding/review harness candidate. | Provider/auth activation. |
| `CursorHarnessRef` | Cursor external harness metadata. | ExternalHarnessRef fields plus source and Git boundary. | Source-readable-by-default flags, auto-commit hooks. | H0 user-operated coding/review harness candidate. | Product/source access or Git automation. |
| `GraphifyEvidenceToolRef` | Graphify evidence tooling metadata. | evidence tool id, curated summary ref, evidence limitations, authority block. | Rerun command, raw output grant, authority flag, substrate flag. | Curated evidence support. | Graphify adoption or truth engine. |
| `CodegraphCandidateRef` | Codegraph candidate metadata. | candidate id, analysis boundary, EXT review requirement. | execution command, authority flag, substrate flag. | Future external analysis/tooling candidate. | Codegraph authority or execution. |
| `ExternalOperatorBoundary` | Boundary between user-operated external harnesses and AGENT PLATFORM. | operator, manual action, input/output packages, review route, Git boundary. | automatic bridge, live connector, dispatch hook. | Preserve user-operated separation. | Internal automation boundary. |

## ExternalHarnessRef Contract

Required fields:

```text
harness_ref_id
harness_name
harness_classification
harness_level
manual_operator
allowed_manual_use
blocked_automation
input_package_requirements
output_package_requirements
context_boundary
source_boundary
provider_boundary
tool_boundary
agent_boundary
product_boundary
memory_boundary
security_refs
validation_refs
evidence_refs
retention_refs
rollback_refs
incident_refs
blockers
limitations
review_required
```

`ExternalHarnessRef` is metadata only. It does not create adapter integration or runtime access.

## HarnessBoundary Contract

Required fields:

```text
boundary_id
harness_ref
allowed_harness_level
blocked_harness_levels
manual_use_constraints
input_constraints
output_constraints
source_constraints
secret_credential_constraints
provider_auth_constraints
tool_execution_constraints
agent_execution_constraints
product_constraints
generated_output_constraints
git_constraints
human_approval_required
stop_rules
limitations
```

`HarnessBoundary` constrains use; it does not grant execution permission.

## HarnessInputPackage Contract

Required fields:

```text
input_package_id
target_harness_ref
manual_ticket_text
context_pack_refs
memory_manifest_refs
evidence_refs
source_refs
allowed_files
blocked_files
allowed_actions
blocked_actions
expected_response_format
stop_rules
human_operator_notes
```

`HarnessInputPackage` is manually copied or supplied by the user. It is not automatic dispatch.

## HarnessOutputPackage Contract

Required fields:

```text
output_package_id
source_harness_ref
manual_ticket_ref
summary
files_created
files_modified
commands_run
decisions_made
limitations
blockers
evidence_refs
validation_refs
security_refs
retention_refs
rollback_refs
incident_refs
recommended_next_ticket
commit_advice_candidate
```

`HarnessOutputPackage` is returned manually by the user. It is not automatically accepted, reviewed, integrated, committed, or pushed.

## Harness Classification Matrix

| Harness | Classification | Allowed P7 level | Allowed manual use | Blocked use | Required future review |
| --- | --- | --- | --- | --- | --- |
| OpenCode | Manual external development harness candidate. | H0 allowed; H1 design only. | User manually supplies ticket/context and returns output as `HarnessOutputPackage`. | H2/H3, OpenCode adapter, OpenCode execution by AGENT PLATFORM, automatic dispatch, internal runtime adoption. | Future EXT/H1 review before any adapter design hardening. |
| Hermes | External agent runtime / orchestration / Cadence candidate. | H0 reference only if user manually uses it outside AGENT PLATFORM; H1 design only. | Candidate notation and external manual result reporting. | Runtime activation, orchestrator adoption, Cadence activation, handoffs, automatic dispatch. | Future EXT review and activation gates. |
| Codex | External coding/review harness candidate. | H0 allowed; H1 design only. | User manually uses exact tickets and returns output. | Provider/auth activation, internal integration, automatic dispatch. | Future provider/auth and harness boundary review. |
| Claude | External coding/review harness candidate. | H0 allowed; H1 design only. | User manually uses exact tickets and returns output. | Provider/auth activation, internal integration, automatic dispatch. | Future provider/auth and harness boundary review. |
| Cursor | External coding/review harness candidate. | H0 allowed; H1 design only. | User manually uses exact tickets and returns output. | Provider/auth activation, product source access by default, auto-commit. | Future source/Git/provider boundary review. |
| GBrain | External memory architecture candidate. | Candidate notation only; H1 design only if explicitly scoped later. | Reference candidate concepts as notation. | GBrain runtime, persistent memory, live retrieval, vector DB, graph DB, substrate selection. | Future EXT review and CSS substrate governance. |
| Graphify | Generated evidence tool / repo map evidence. | Curated evidence reference only. | Reference curated Graphify Repo Map Summary as supporting evidence. | Rerun, adoption, authority, truth engine, substrate, automatic routing. | Future evidence tooling boundary review. |
| Codegraph | External analysis/tooling candidate. | Candidate notation only. | Name as future analysis/tooling candidate. | Execution, adoption, authority, substrate. | Future EXT review. |
| MCP servers/tools/resources | Blocked integration surface. | None in P7 except boundary metadata. | State blocked boundary. | MCP activation, MCP calls, MCP tools, MCP resources. | Future P3/P0 activation gates. |
| Live connectors | Blocked integration surface. | None in P7 except boundary metadata. | State blocked boundary. | Live connector runtime or event streaming. | Future runtime/security review. |
| Provider/model APIs | Blocked provider/auth surface. | None in P7 except boundary metadata. | State blocked boundary. | API calls, credentials, auth config, model-provider integration. | Future provider/auth activation decision. |
| Product/Siamese-specific tools | Blocked product surface. | None in P7 except boundary metadata. | State blocked boundary. | Product/Siamese source inspection or product tool activation. | Future P4 / GT-09. |
| Generic shell/subprocess tools | Blocked tool execution surface. | None in P7 except boundary metadata. | State blocked boundary. | Shell, subprocess, scripts, build, test, lint, runtime execution. | Future tool activation gate. |
| Git tools | User-owned manual Git surface. | Advice only with exact paths. | User may manually run exact commands. | Agent staging, commit, push, force-add, or `git add .`. | Future integrator/commit advisory governance. |

## OpenCode Boundary

OpenCode may be used manually by the user as an external development harness candidate. P7.0.E does not integrate OpenCode, does not run OpenCode, does not import OpenCode code, and does not create OpenCode adapter. OpenCode output must return as `HarnessOutputPackage`, must pass reviewer/integrator before acceptance, and must not bypass governance.

| OpenCode use case | Allowed P7 use | Blocked use | Required future gate |
| --- | --- | --- | --- |
| Manual ticket execution outside AGENT PLATFORM | User manually copies ticket/context into OpenCode and returns output. | Automatic dispatch or OpenCode execution by AGENT PLATFORM. | Future H1 checklist before adapter design. |
| Manual review support | User asks OpenCode for review and returns findings. | Auto-review or reviewer replacement. | P7.0.F reviewer mesh alignment. |
| Manual implementation candidate output | Output is reported as `HarnessOutputPackage`. | Accepted-by-default code or Git mutation. | P7.0.G integrator/commit advisory alignment. |
| Manual context packaging | User supplies allowed context only. | Secrets, credentials, blocked source, provider configs. | Context/security review if expanded. |

## Hermes Boundary

Hermes is an external agent runtime / orchestration / Cadence candidate only. Hermes runtime is not active. Hermes is not internal AGENT PLATFORM runtime, is not adopted as orchestrator, is not allowed to auto-dispatch tasks, is not allowed to execute handoffs, and is not allowed to activate Cadence. Any Hermes adoption requires future EXT review and explicit gates. This section means no Hermes runtime.

| Hermes surface | P7 classification | Allowed use | Blocked use | Required future review |
| --- | --- | --- | --- | --- |
| Hermes runtime | External runtime candidate. | Candidate notation only. | Runtime activation or internal runtime adoption. | EXT review and activation gates. |
| Hermes orchestration | External orchestration candidate. | Conceptual comparison only. | Auto-dispatch, automatic routing, handoffs. | Future orchestration governance. |
| Cadence | Always-on/runtime cadence candidate. | Named as blocked future candidate. | Cadence activation or live loop. | Future runtime/cadence gate. |
| Hermes outputs | Manual outside output if user-operated. | Automatic acceptance or integration. | Reviewer/integrator pass. | P7.0.F/P7.0.G. |

## Codex / Claude / Cursor Boundary

Codex, Claude, and Cursor are external coding/review harness candidates. In P7, they may be used manually by the user with exact tickets. They are not internal runtime, do not receive automatic dispatch, do not become provider/auth activation, and their outputs require manual review and integration.

| Harness | Allowed use | Blocked use | Expected output package |
| --- | --- | --- | --- |
| Codex | H0 manual coding/review harness with exact ticket text. | Provider/auth activation, internal runtime, automatic dispatch. | `HarnessOutputPackage` with summary, files, commands, limitations, and review needs. |
| Claude | H0 manual coding/review harness with exact ticket text. | Provider/auth activation, internal runtime, automatic dispatch. | `HarnessOutputPackage` with summary, files, commands, limitations, and review needs. |
| Cursor | H0 manual coding/review harness with exact ticket text and explicit source boundaries. | Product source access by default, auto-commit, provider/auth activation. | `HarnessOutputPackage` with source/Git boundary notes. |

## GBrain Boundary

GBrain is an external memory architecture candidate only. GBrain runtime is blocked. GBrain is not a substrate, not persistent memory for AGENT PLATFORM, and not live retrieval. GBrain candidate refs are allowed as notation only. Any GBrain source review requires separate EXT review. Any GBrain runtime requires future gates. This section means no GBrain runtime.

| GBrain surface | P7 classification | Allowed use | Blocked use | Required future review |
| --- | --- | --- | --- | --- |
| GBrain architecture | External memory architecture candidate. | Candidate notation only. | Runtime activation or memory adoption. | EXT review. |
| Memory fabric comparison | Conceptual reference only. | Compare to `Context & Memory Fabric` as inactive candidate. | Persistent memory, live retrieval, vector DB, graph DB. | CSS substrate governance. |
| GBrain source | External source. | Not inspected in P7.0.E. | Source review without EXT scope. | Future EXT source review. |
| GBrain runtime | Blocked runtime surface. | None in P7. | Runtime, Cadence, database, retrieval, embeddings. | Future runtime gates. |

## Graphify Boundary

Graphify is generated evidence tooling / repo map evidence. Curated Graphify summaries may be referenced only as evidence. Raw Graphify output remains blocked/local-only by default. P7.0.E does not rerun Graphify, does not adopt Graphify as authority, does not treat Graphify as substrate, and does not allow Graphify to route work automatically.

| Graphify surface | Allowed P7 use | Blocked use | Evidence posture |
| --- | --- | --- | --- |
| Graphify Repo Map Summary | Curated generated supporting evidence. | Authority, truth engine, substrate. | Evidence supports; it does not decide. |
| Raw Graphify output | Not used by P7.0.E. | Reading, publication, tracking expansion. | Blocked/local-only by default. |
| Graphify execution | None. | Rerun, `/graphify`, generated output creation. | Not executed. |
| Graphify routing | None. | Automatic work routing or ticket dispatch. | Not a router. |

## Codegraph Boundary

Codegraph, if considered later, is an external analysis/tooling candidate. P7.0.E does not run Codegraph, does not adopt Codegraph as authority, does not treat Codegraph as substrate, and requires future EXT review for any Codegraph use.

| Codegraph surface | Allowed P7 use | Blocked use | Required future review |
| --- | --- | --- | --- |
| Codegraph candidate | Candidate notation only. | Execution or adoption. | EXT review. |
| Codegraph analysis | Not performed in P7.0.E. | Authority or truth engine. | Analysis/tooling boundary review. |
| Codegraph substrate | None. | Treating Codegraph as graph substrate. | CSS substrate governance if ever proposed. |

## MCP / Provider / API Boundary

MCP servers/tools/resources are blocked in P7. Provider/auth/API activation is blocked in P7. Credential use is blocked. API calls are blocked. Model-provider integration is blocked. Harness usage must not silently become provider/auth activation. This section means no MCP activation.

| Surface | P7 classification | Allowed use | Blocked use | Required gate |
| --- | --- | --- | --- | --- |
| MCP servers | Blocked integration surface. | Boundary metadata only. | Server activation, resource access, tool calls. | Future MCP activation decision. |
| MCP tools/resources | Blocked tool/resource surface. | Boundary metadata only. | Tool execution or resource retrieval. | P0/P3 gates. |
| Provider/model APIs | Blocked provider surface. | Boundary metadata only. | API calls, auth config, model integration. | Provider/auth/API activation decision. |
| Credentials/API keys | Blocked secret surface. | No use. | Inspection, config, token stores, API keys. | Secrets policy and explicit gate. |
| Harness provider capabilities | External and user-operated only. | User may manually use external UI outside AGENT PLATFORM. | Silent internal provider/auth activation. | Future provider and harness review. |

## Product / Siamese Boundary

Siamese is product vision, not product activation. Product/Siamese source is blocked. Product-specific harnesses are blocked until product readiness. Harnesses must not inspect product source by default. Product-bound work requires future P4 / GT-09.

| Product-bound harness scenario | P7 status | Blocked use | Future requirement |
| --- | --- | --- | --- |
| Product/Siamese source review | Blocked. | Inspecting product source by default. | Future P4 / GT-09. |
| Product-specific harness execution | Blocked. | Product tool activation or live connector. | Product readiness gate. |
| Product architecture discussion | Allowed as vision/governance context only. | Source loading or implementation. | Future product governance. |
| Siamese-specific automation | Blocked. | Autonomous product workflow. | Future product/runtime gates. |

## Agent-Native Projection Boundary

Harnesses relate to the `agent_native_internal_organization_layer` only through manual projection. Harnesses are manual projections of internal topology, not the internal topology itself.

| Internal agent-native concept | Manual harness projection | Allowed P7 use | Blocked interpretation |
| --- | --- | --- | --- |
| `TaskGraphRef` | User may split task graph nodes into manual tickets or harness prompts. | Manual ticket packaging. | Scheduler graph or runnable task queue. |
| `BlackboardRef` | User may include curated claims, evidence, findings, blockers, and questions in context packages. | Manual shared evidence framing. | Live shared state, persistence, graph DB, vector DB, event stream. |
| `CapabilityCellRef` | User may map capability needs to manual lanes or external harness choices. | Manual lane/harness selection metadata. | Active capability cell runtime. |
| `ReviewerMeshRef` | User may route outputs to manual reviewers. | Manual reviewer mesh planning. | Automatic reviewer assignment or auto-review. |
| `RoutingDecisionRef` | Lead agent may record manual routing rationale. | Manual routing record. | Automatic ticket routing, provider routing, or model routing runtime. |
| `ManualExecutionProjection` | User-facing tickets, external harnesses, manual review, manual integration, and exact Git advice. | Manual workflow projection. | Autonomous dispatch, runtime orchestration, handoff execution, or Git mutation. |
| `Context & Memory Fabric` | User may assemble context packs and memory slices as markdown metadata. | Manual context packaging. | GBrain runtime, live retrieval, persistent memory, vector DB, graph DB. |
| `ExternalOperatorBoundary` | User remains the operator between external harness and AGENT PLATFORM. | Manual input/output transfer. | Live connector or automatic bridge. |

## Review / Integration Boundary

Harness outputs are not accepted by default. Harness outputs require reviewer/integrator pass. Reviewer verdict is not Git approval. Integrator acceptance is not Git mutation. Human user remains final authority.

| Output status | Required review | Required integration | Blocked shortcut |
| --- | --- | --- | --- |
| Raw harness output | Boundary and correctness review. | None until reviewed. | Accepting by default. |
| Reviewed harness output | Reviewer verdict with limitations. | Integrator checks scope, files, boundaries, and commit advice. | Treating reviewer verdict as Git approval. |
| Integration candidate | Integrator summary and exact command advice candidate. | User decides whether to run Git. | Agent staging, commit, push, or publication. |
| Blocked output | Stop and report blocker. | No integration. | Workaround execution or hidden permission escalation. |

## Git Boundary

External harnesses must not be instructed to auto-commit. External harnesses must not auto-push. The lead/integrator may advise exact commands. The user performs Git manually. Never recommend `git add .`.

| Git scenario | Allowed use | Blocked use |
| --- | --- | --- |
| Status review | User may manually run `git status --short`. | Agent Git mutation. |
| Staging | Exact-path advice only. | `git add .`, force-add, broad staging. |
| Commit | Exact ticket message advice only. | Auto-commit or harness commit. |
| Push | User-owned manual push. | Auto-push or publication by agent/harness. |

Required command pattern:

```powershell
git status --short

git add <exact_path_1> `
        <exact_path_2>

git commit -m "<exact ticket message>"

git push origin main
```

## Interfaces With P7.0.F / P7.0.G / P7.0.H / P7.0.R

P7.0.E does not start downstream tickets.

| Downstream ticket | What it consumes from P7.0.E | Required alignment | Blocked shortcut |
| --- | --- | --- | --- |
| P7.0.F Reviewer Mesh / Immune Safeguards | Harness output risk, review requirements, reviewer mesh boundaries. | H0/H1/H2/H3 and `ReviewerMeshRef` must preserve manual review. | Automatic reviewer assignment or auto-review. |
| P7.0.G Integrator / Commit Advisory Protocol | `HarnessOutputPackage`, integration boundary, Git boundary, exact-path command pattern. | Integrator advice remains non-mutating and user-owned. | Auto-commit, auto-push, `git add .`. |
| P7.0.H First Manual Agent-Native Pilot Playbook | Manual harness use cases and input/output package rules. | Pilot must use H0 only unless H1 design-only is explicitly scoped. | Running harnesses automatically. |
| P7.0.R Manual Agent-Native Workflow Closure | Final closure invariants and readiness checks. | Closure must preserve no runtime activation and no Git mutation. | Treating closure as activation approval. |

## Interfaces With Prior Governance

| Upstream document group | P7.0.E consumption | Preserved boundary |
| --- | --- | --- |
| P7.0.0 research carry-forward | Consumes `agent_native_internal_organization_layer` pattern set. | Pattern set is conceptual only. |
| P7.0.A/B/C/D aligned bridge docs | Consumes `manual_bridge_layer`, topology/task/blackboard/lane/context projection markers. | Existing P7.0.A/B/C/D are not modified. |
| P6 operational contracts | Consumes capability, communication, evidence, approval, monitoring, and incident concepts. | Operational concepts do not activate runtime. |
| P5 skeleton baseline | Consumes inert skeleton posture. | Skeleton design is not implementation permission. |
| P3 activation decisions | Consumes provider/tool/agent activation blocks. | Activation remains blocked. |
| P2/P2.K knowledge/retrieval architecture | Consumes metadata/evidence/retention/rollback vocabulary. | No live retrieval, persistence, vector DB, or graph DB. |
| P1 metadata contracts | Consumes context/provider/tool/agent/CSS metadata boundaries. | Metadata is not execution. |
| P0 gates | Consumes gate and validation/security posture. | Gate mapping is not approval. |
| S-03/S-04 | Consumes shell/network/MCP and secrets boundaries. | No shell/network/MCP/secret use. |
| CSS ADR/audit | Consumes accepted naming and substrate deferral. | Cognitive Semantic System substrate remains unselected. |

## Stop Rules

Stop on any missing P7.0.0 request, missing P7.0-NATIVE-ALIGN-01 request, OpenCode integration request, OpenCode execution request, Hermes runtime request, Hermes orchestration request, GBrain runtime request, GBrain memory activation request, Cadence request, MCP activation request, provider/auth/API request, credential request, API call request, live connector request, product/Siamese source request, external source inspection request, Graphify rerun/adoption request, Codegraph execution/adoption request, automatic harness dispatch request, automatic ticket routing request, automatic reviewer assignment request, automatic commit/push request, tool execution request, agent execution request, source loading request, source inspection request, persistence DB request, vector DB request, graph DB request, generated output tracking request, source tracking expansion request, publication request, Cognitive Semantic System substrate selection request, Git mutation by agent request, or `git add .` recommendation request.

## Future Validation Targets

Future validation targets, not executed by P7.0.E:

| Target | Purpose |
| --- | --- |
| P7.0.0 prerequisite presence | Confirm agent-native research carry-forward exists. |
| P7.0-NATIVE-ALIGN-01 marker presence in A/B/C/D | Confirm manual bridge alignment markers. |
| HarnessLevel vocabulary completeness | Confirm H0/H1/H2/H3 definitions and decisions. |
| ExternalHarnessRef required field completeness | Confirm required metadata fields. |
| HarnessBoundary required field completeness | Confirm boundary fields. |
| HarnessInputPackage required field completeness | Confirm manual input package fields. |
| HarnessOutputPackage required field completeness | Confirm returned output package fields. |
| OpenCode boundary completeness | Confirm no adapter/integration/runtime activation. |
| Hermes boundary completeness | Confirm no Hermes runtime. |
| GBrain boundary completeness | Confirm no GBrain runtime. |
| Graphify boundary completeness | Confirm evidence-only posture. |
| Codegraph boundary completeness | Confirm no execution/adoption. |
| MCP/provider/API blocked invariant | Confirm no MCP activation, API calls, or provider/auth activation. |
| H0 allowed / H1 design-only / H2-H3 blocked invariant | Confirm level semantics. |
| No automatic dispatch invariant | Confirm manual external operator strategy. |
| No harness runtime activation invariant | Confirm harnesses are not internal runtime. |
| No Hermes runtime invariant | Confirm Hermes is candidate only. |
| No GBrain runtime invariant | Confirm GBrain is candidate only. |
| No Git mutation invariant | Confirm user-owned Git. |
| No `git add .` invariant | Confirm exact-path command advice only. |
| P7.0.F consumption readiness | Confirm reviewer mesh can consume harness risk/output metadata. |
| P7.0.G consumption readiness | Confirm integrator/commit advisory can consume output/Git boundary metadata. |
| P7.0.R closure readiness | Confirm closure can consume final harness invariants. |

## Future Hardening Candidates

Future tickets, not started:

| Candidate | Purpose |
| --- | --- |
| P7-HARNESS-HARD-01 - ExternalHarnessRef Schema Candidate | Define schema candidate for harness refs. |
| P7-HARNESS-HARD-02 - HarnessBoundary Checklist | Define checklist for harness boundaries. |
| P7-HARNESS-HARD-03 - HarnessInputPackage / HarnessOutputPackage Schema Candidate | Define package schemas. |
| P7-HARNESS-HARD-04 - OpenCode Manual Harness Checklist | Define OpenCode H0 checklist. |
| P7-HARNESS-HARD-05 - Hermes Candidate Boundary Review | Review Hermes candidate boundary. |
| P7-HARNESS-HARD-06 - GBrain Candidate Boundary Review | Review GBrain candidate boundary. |
| P7-HARNESS-HARD-07 - Graphify Evidence Tool Boundary Checklist | Review Graphify evidence boundary. |
| P7-HARNESS-HARD-08 - Codegraph Candidate Boundary Checklist | Review Codegraph candidate boundary. |
| P7-HARNESS-HARD-09 - H0/H1/H2/H3 Harness Level Gate Matrix | Define level gate matrix. |
| P7-HARNESS-HARD-10 - Manual Harness Output Review Checklist | Define output review checklist. |

## Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_manual_harness_opencode_hermes_boundary_strategy.md`

Modified:

- none

Not created / not approved:

- no modification of P7.0.A
- no modification of P7.0.B
- no modification of P7.0.C
- no modification of P7.0.D
- no P7.0-NATIVE-ALIGN-01 started
- no P7.0.F/G/H/R started
- no runtime activation
- no autonomous orchestration
- no internal agent runtime
- no automatic task dispatch
- no automatic handoff
- no automatic reviewer assignment
- no automatic commits
- no automatic pushes
- no OpenCode integration
- no OpenCode execution
- no Hermes runtime
- no GBrain runtime
- no Cadence
- no MCP activation
- no provider/auth/API activation
- no credential use
- no API calls
- no live connectors
- no product/Siamese source inspection
- no source loading
- no source inspection
- no external source inspection
- no persistence DB
- no vector DB
- no graph DB
- no telemetry
- no event streaming
- no Graphify rerun/adoption
- no Codegraph execution/adoption
- no tool execution
- no agent execution
- no validation execution
- no security enforcement activation
- no generated output tracking
- no source tracking expansion
- no publication
- no Git mutation by the agent
- no Cognitive Semantic System substrate selection

## Recommended Next Ticket

After P7.0.E, the recommended next ticket is:

- P7.0.F - Reviewer Mesh / Immune Safeguards

Recommended actual: P7.0.F - Reviewer Mesh / Immune Safeguards.

Do not start P7.0.F. Do not start P7.0.G. Do not start P7.0.H. Do not start P7.0.R.

## Final Verdict

P7.0.E created `0_architecture/governance/agent_platform_manual_harness_opencode_hermes_boundary_strategy.md`.

P7.0.0 was present. P7.0-NATIVE-ALIGN-01 alignment evidence was present by the allowed prerequisite and marker checks.

The Manual Harness Strategy defines external harnesses as user-operated H0 surfaces or H1 design-only metadata candidates, not internal runtime. H2 controlled tool execution adapter and H3 autonomous orchestration adapter are blocked.

OpenCode is a manual external development harness candidate. It may be used manually by the user, returns `HarnessOutputPackage`, and is not integrated or run by AGENT PLATFORM.

Hermes is an external agent runtime / orchestration / Cadence candidate only. Hermes runtime, orchestration adoption, automatic dispatch, handoffs, and Cadence activation are blocked.

Codex, Claude, and Cursor are external coding/review harness candidates. They may be used manually with exact tickets and do not become provider/auth activation or internal runtime.

GBrain is an external memory architecture candidate only. GBrain runtime, persistent memory, live retrieval, vector DB, graph DB, and substrate selection are blocked.

Graphify is generated evidence tooling / repo map evidence. Curated Graphify evidence may support review only; Graphify is not authority, not substrate, not rerun, and not a routing engine.

Codegraph is an external analysis/tooling candidate only. Codegraph execution, authority, adoption, and substrate treatment require future EXT review.

MCP servers/tools/resources, provider/auth/API activation, credentials, API calls, and model-provider integration are blocked in P7.

Siamese remains product vision, not product activation. Product/Siamese source and product-specific harnesses are blocked until future P4 / GT-09 readiness.

The `HarnessLevel` model defines H0 manual use, H1 design-only metadata, H2 blocked controlled tool execution adapter, and H3 blocked autonomous orchestration adapter.

The `ExternalHarnessRef`, `HarnessBoundary`, `HarnessInputPackage`, and `HarnessOutputPackage` objects define metadata-only references, constraints, user-supplied manual input packages, and user-returned manual output packages.

Harnesses manually project the `agent_native_internal_organization_layer` through `TaskGraphRef`, `BlackboardRef`, `CapabilityCellRef`, `ReviewerMeshRef`, `RoutingDecisionRef`, `ManualExecutionProjection`, `Context & Memory Fabric`, and `ExternalOperatorBoundary`. They are not the internal topology itself.

Harness outputs require reviewer/integrator pass and are not accepted, integrated, committed, or pushed automatically. The human user performs Git commits and pushes manually.

P7.0.E did not modify P7.0.A/B/C/D. P7.0.E did not activate OpenCode, Hermes, GBrain, Codex, Claude, Cursor, Graphify, Codegraph, MCP, providers, live connectors, product, tools, or agents. P7.0.E did not mutate Git.

Next recommended ticket: P7.0.F - Reviewer Mesh / Immune Safeguards.
