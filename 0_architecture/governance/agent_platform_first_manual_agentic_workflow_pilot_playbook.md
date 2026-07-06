# First Manual Agent-Native Pilot Playbook

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | First Manual Agent-Native Pilot Playbook |
| Ticket | P7.0.H |
| Status | Accepted pilot playbook design; pilot not executed |
| Date | 2026-07-06 |
| Scope | Documentation-only playbook for the first later manual agent-native pilot for AGENT PLATFORM / Siamese. |
| Target result | first_manual_agent_native_pilot_playbook_ready |
| Authority | Pilot procedure design only; not pilot execution, not P7.1 start, not P7.0.R start, not runtime activation, not agents/tools/providers/MCP activation, not GBrain/Hermes/Cadence activation, not Graphify/Codegraph adoption, not live connectors, not product/Siamese source access, not persistence, not vector DB, not graph DB, not generated-output tracking, not source tracking expansion, not publication, and not Git mutation. |
| Required inputs | P7.0.0, P7.0.A, P7.0.B, P7.0.C, P7.0.D, P7.0.E, P7.0.F, P7.0.G, and operational readiness audit. |
| Output | Manual playbook for running a later first safe agent-native manual workflow pilot. |

## 2. Purpose

P7.0.H defines how AGENT PLATFORM will later run the first manual agent-native pilot without executing it now.

The playbook consumes the current `manual_bridge_layer`:

| Manual bridge component | P7.0.H use |
| --- | --- |
| User Gateway | Captures objective, authority, scope, and stop rules. |
| Roadmap / Work Breakdown | Produces manual roadmap, work packets, and sequence. |
| Manual Lane Projection | Maps work to human-operated lanes and external H0 harnesses. |
| Context / Memory Manifest | Builds manual context packs and memory metadata. |
| Manual Harness Boundary | Governs H0/H1/H2/H3 harness posture. |
| Reviewer Mesh | Routes outputs to manual reviewer mesh / immune safeguards. |
| Integrator / Commit Advisory | Produces manual synthesis and exact-path commit advice candidate. |

The playbook also consumes the `agent_native_internal_organization_layer`:

| Agent-native concept | P7.0.H use |
| --- | --- |
| topology selection | Select a safe conceptual topology for the pilot. |
| recursive task graph | Represent pilot work as manual task graph metadata. |
| blackboard / shared evidence space | Track claims, evidence, blockers, contradictions, and questions. |
| capability cells | Map work needs to manual capability projections. |
| reviewer mesh / immune safeguards | Review outputs and detect drift, unsafe scope, and boundary breaches. |
| routing decision | Record why a manual lane or H0 harness is selected. |
| context & memory fabric | Assemble context packs and memory slices as metadata only. |
| manual execution projection | Project internal concepts into manual tickets, harness prompts, reviews, integration, and user-owned Git advice. |

P7.0.H recommends a first safe pilot but does not execute it.

## 3. Current Posture

| Area | Current posture | P7.0.H interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM | Governed manual platform design. | P7 remains a manual controlled workflow. | Runtime platform execution. |
| Siamese | Living energy twin product vision. | Product vision context only. | Product/Siamese source inspection or product activation. |
| P7.0.A-G | Present peer governance inputs. | Consumed as manual bridge and safety boundaries. | Modification or rework by P7.0.H. |
| P7.1 | Future pilot execution ticket. | Recommended but not started. | Pilot execution now. |
| P7.0.R | Future closure ticket. | Future closure after pilot-readiness design. | Closure now. |
| External harnesses | H0 user-operated surfaces, H1 design-only metadata. | Manual harness prompts may be prepared later. | Internal harness activation or automatic dispatch. |
| Reviewer mesh | Manual metadata and immune safeguards. | Review route designed for later pilot. | Automatic reviewer assignment or auto-review. |
| Integrator | Manual synthesis and commit advisory. | Exact-path command advice candidate only. | Agent staging, commit, push, or `git add .`. |

## 4. Inputs Reviewed

| Input | Presence posture | P7.0.H consumption | Boundary preserved |
| --- | --- | --- | --- |
| `agent_platform_agent_native_organization_research_carry_forward.md` | Present by safe path check. | Agent-native organization patterns. | Conceptual only; no runtime. |
| `agent_platform_manual_lead_agent_user_gateway_contract.md` | Present by safe path check. | User gateway and manual control plane. | User remains final authority. |
| `agent_platform_roadmap_generation_work_breakdown_contract.md` | Present by safe path check; `TaskGraphRef` and `BlackboardRef` markers found. | Work breakdown, topology, task graph, blackboard projection. | Planning only; no scheduling. |
| `agent_platform_parallel_agent_lane_work_packet_taxonomy.md` | Present by safe path check; `ManualExecutionProjection` marker found. | Manual lane projection and capability/routing references. | Lanes are not runtime agents. |
| `agent_platform_manual_context_memory_manifest_strategy.md` | Present by safe path check. | Context & Memory Fabric procedure. | No live retrieval or persistence. |
| `agent_platform_manual_harness_opencode_hermes_boundary_strategy.md` | Present by safe path check; `H0` marker found. | H0/H1/H2/H3 manual harness semantics. | No internal harness activation. |
| `agent_platform_reviewer_mesh_immune_safeguards_contract.md` | Present by safe path check; `ReviewerMesh` marker found. | Reviewer mesh and immune safeguard procedure. | No automatic review. |
| `agent_platform_manual_integrator_commit_advisory_protocol.md` | Present by safe path check; `CommitCandidate` marker found. | Integration summary, drift register, commit candidate, command block. | No Git mutation. |
| `agent_platform_operational_readiness_audit.md` | Present by safe path check. | Operational readiness boundaries. | Audit posture does not activate runtime. |
| P6.1-P6.6 | Inherited governance inputs. | Capability, communication, evidence, approval, monitoring, and incident boundaries. | Operational metadata only. |
| P5.R / P5.1-P5.7 | Inherited skeleton baseline. | Inert skeleton and non-activation posture. | No implementation. |
| P3.BR / P3.3 / P3.4 / P3.5 | Inherited activation decisions. | Provider/tool/agent activation blocks. | No activation. |
| P2.KR / P2.1-P2.3 | Inherited knowledge architecture. | Evidence, metadata, retention, and rollback refs. | No live retrieval. |
| P1.1-P1.5 | Inherited metadata contracts. | Context/provider/tool/agent/CSS metadata vocabulary. | Metadata is not execution. |
| P0.1-P0.3 | Inherited gates. | Activation gate, validation gate, and security posture. | Gate mapping is not approval. |
| S-03 / S-04 | Inherited security policies. | Shell/network/MCP and secrets boundaries. | No secret, credential, network, or MCP use. |
| CSS ADR/audit | Inherited naming and audit posture. | Cognitive Semantic System naming and deferral. | No substrate selection. |
| README.md / `.gitignore` / `.graphifyignore` | Inherited repository governance posture. | Boundary continuity. | No tracking expansion. |

## 5. Non-Action Statement

P7.0.H is not the pilot. P7.0.H is not P7.1. P7.0.H is not P7.0.R.

P7.0.H does not activate runtime, agents, tools, providers, MCP, GBrain, Hermes, Cadence, Graphify, Codegraph, live connectors, product/Siamese source, persistence, vector DB, graph DB, generated-output tracking, source tracking, publication, validation execution, security enforcement, or Git mutation.

P7.0.H creates only the playbook for a later manual pilot.

## 6. Pilot Selection Decision

Recommended pilot:

```text
P7.1-FIRST-PILOT - Manual Agent-Native Workflow Pilot For A Small AGENT PLATFORM Documentation Task
```

Recommended pilot class:

```text
documentation_only_governance_workflow
```

Recommended pilot scope:

```text
Use the manual P7 workflow to generate, run, review, integrate, and commit a small AGENT PLATFORM governance/documentation ticket.
```

The recommended pilot is safe because it is documentation-only, non-product-bound, small enough for manual review, and useful for validating the P7 workflow without requiring runtime, source inspection, provider access, external source review, Graphify rerun, Codegraph execution, persistence, or agent Git mutation.

The pilot must avoid product/Siamese source, runtime implementation, tool execution, provider/auth/API/MCP, GBrain runtime, Hermes runtime, Cadence, Graphify rerun/adoption, Codegraph execution, persistence, vector DB, graph DB, generated output tracking, source tracking expansion, publication, and Git mutation by agent.

## 7. Pilot Candidate Matrix

| Candidate | Safety fit | Usefulness | Boundary risk | Verdict | Rationale |
| --- | --- | --- | --- | --- | --- |
| small AGENT PLATFORM governance/documentation workflow | High | High | Low | `recommended_first_pilot` | Validates the P7 workflow using documentation-only governance work. |
| external source review planning workflow | Medium | Medium | Medium | `valid_later` | May be useful later, but external source content requires stricter EXT scope. |
| barbería website roadmap workflow | Medium | Medium | Low to medium | `valid_later_non_product_pilot_candidate` | Non-product roadmap planning can be safe later if source/runtime are excluded. |
| simple non-product implementation planning workflow | Medium | Medium | Medium | `valid_later_if_no_runtime` | Planning can be safe, but implementation pressure must not trigger runtime/tool execution. |
| P4/Siamese product workflow | Low for first pilot | High later | High | `blocked_until_P4` | Product/Siamese source and product-bound work require future product readiness. |
| GBrain/Hermes/Graphify adoption workflow | Low for first pilot | High later | High | `blocked_until_EXT_or_future_exact_gate` | Adoption requires EXT/future activation gates and must not be first manual pilot. |

## 8. Recommended First Pilot

The first pilot should be P7.1-FIRST-PILOT, a small documentation-only AGENT PLATFORM governance/manual workflow task.

Recommended constraints:

- Use only governance/documentation scope.
- Use the user gateway to capture exact objective and exclusions.
- Use topology selection, task graph, blackboard, capability cells, routing, context/memory fabric, and manual execution projection as metadata only.
- Use one H0 external harness only if the user manually runs it outside AGENT PLATFORM.
- Return output as `HarnessOutputPackage`.
- Review through `ReviewerMesh` and `ImmuneSafeguard` metadata.
- Integrate through `IntegrationSummary`, `DriftRegister`, `AcceptedOutputRegister`, `RejectedOutputRegister`, `CommitCandidate`, and `CommitCommandBlock` metadata.
- User performs Git manually if they choose to do so.

## 9. Manual Agent-Native Pilot Lifecycle

Each lifecycle stage is manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation.

| Stage | Name | Later pilot action | Boundary |
| --- | --- | --- | --- |
| 1 | UserObjective intake | Capture objective, scope, non-goals, constraints, authority, and stop rules. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 2 | Lead/User Gateway session | Lead agent frames the manual control-plane session and confirms user authority. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 3 | AgentNativeTopologySelection | Select conceptual topology for the pilot. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 4 | TaskGraphRef / TaskGraphProjection | Define task nodes, dependencies, blockers, review edges, and integration edge metadata. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 5 | BlackboardRef / shared evidence and blocker space | Record evidence, claims, blockers, contradictions, and questions. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 6 | CapabilityCellProjection | Map task needs to conceptual capability cells and manual lanes. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 7 | RoutingDecisionRef | Record manual routing rationale for human/harness lane choice. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 8 | ManualWorkPacketProjection | Convert metadata into exact manual work packets. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 9 | HarnessInputPackage generation | Prepare exact prompt/context package for an H0 harness. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 10 | User manually runs H0 external harness | User may manually use OpenCode, Codex, Claude, Cursor, or equivalent outside AGENT PLATFORM. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 11 | HarnessOutputPackage returned by user | User manually returns output summary, files, commands, decisions, blockers, and limitations. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 12 | ReviewInputPackage assembled | Build reviewer input from output, scope, evidence, boundaries, and risk markers. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 13 | ReviewerMesh / ImmuneSafeguard review | Manual reviewer mesh checks correctness, drift, scope, unsafe output, contradictions, and evidence conflicts. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 14 | ReviewVerdictPackage produced | Reviewer produces accept/rework/reject/escalate metadata. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 15 | IntegrationSummary and DriftRegister | Integrator manually synthesizes accepted output and records drift. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 16 | AcceptedOutputRegister / RejectedOutputRegister | Separate accepted and rejected paths and decisions. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 17 | CommitCandidate and CommitCommandBlock | Produce exact-path commit advice candidate only. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |
| 18 | User performs Git manually | User decides whether to run exact commands. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation by agent. |
| 19 | Pilot audit and P7.0.R closure | Later closure summarizes pilot readiness/outcome and unresolved issues. | Manual only; metadata only unless explicitly human-run outside AGENT PLATFORM; not runtime; not dispatch; not automatic review; not automatic integration; not Git mutation. |

## 10. Agent-Native Topology For The Pilot

Recommended pilot topology:

```text
UserObjective -> AgentNativeTopologySelection -> recursive TaskGraphRef -> BlackboardRef -> CapabilityCellProjection -> ReviewerMesh / ImmuneSafeguard -> RoutingDecisionRef -> Context & Memory Fabric -> ManualExecutionProjection
```

| Topology element | Pilot use | Boundary |
| --- | --- | --- |
| AgentNativeTopologySelection | Choose a small documentation-only manual topology. | Not topology activation. |
| recursive task graph | Break work into bounded metadata nodes and dependencies. | Not scheduler graph or runnable queue. |
| blackboard / shared evidence space | Record claims, blockers, questions, contradictions, and findings. | Not persistence, event stream, vector DB, graph DB, or live retrieval. |
| capability cells | Map work needs to manual lanes/harness choices. | Not active agents or runtime workers. |
| reviewer mesh / immune safeguards | Plan manual review coverage and risk checks. | Not automatic reviewer assignment or auto-review. |
| routing decision | Record why a human or H0 harness path is selected. | Not automatic routing. |
| context & memory fabric | Assemble context packs and memory slices as markdown metadata. | Not GBrain runtime or persistent memory. |
| manual execution projection | Create manual tickets, harness prompts, review packets, integration packets, and Git advice candidates. | Not autonomous orchestration or Git mutation. |

## 11. Manual Execution Projection

`ManualExecutionProjection` is the bridge from conceptual agent-native organization into human-operable work.

| Internal concept | Manual projection | Later pilot artifact |
| --- | --- | --- |
| topology selection | Lead/user gateway planning choice. | `PilotTopologySelection` |
| recursive task graph | Work packet decomposition. | `PilotTaskGraph` |
| blackboard | Evidence/blocker/context register. | `PilotBlackboard` |
| capability cells | Manual lane and H0 harness mapping. | `PilotCapabilityCellMap` |
| reviewer mesh | Manual review route. | `PilotReviewerMesh` |
| routing decision | Manual route rationale. | `PilotRoutingDecision` |
| context & memory fabric | Context packs and memory manifest. | `PilotMemoryManifest` |
| integration | Manual accepted/rejected output and drift handling. | `PilotIntegrationSummary` and registers |
| Git advice | Exact-path advisory only. | `PilotCommitCandidate` and `PilotCommandBlock` |

## 12. Pilot Object Model

| Object | Meaning | Required fields | Forbidden fields | Boundary |
| --- | --- | --- | --- | --- |
| `PilotObjective` | Captured user objective for the pilot. | objective id, user statement, scope, non-goals, authority, stop rules. | runtime permission, source-loading permission, broad approval. | Manual objective metadata only. |
| `PilotScope` | Inclusion/exclusion boundaries. | included docs, excluded surfaces, allowed actions, blocked actions, review needs. | product source grant, external source grant, credentials. | Scope is not permission to execute. |
| `PilotTopologySelection` | Conceptual topology choice. | topology id, pattern, rationale, constraints, blocked interpretations. | runtime topology config, scheduler config. | Metadata only. |
| `PilotTaskGraph` | Manual task graph projection. | task nodes, dependency edges, blocker edges, review edges, integration edges. | runnable tasks, queue ids, dispatch flags. | Not runtime. |
| `PilotBlackboard` | Shared evidence and blocker space. | claims, evidence refs, blockers, questions, contradictions, conflict markers. | persistence handles, vector DB, graph DB, event stream. | Manual evidence metadata. |
| `PilotCapabilityCellMap` | Capability-to-lane/harness mapping. | capability needs, candidate lanes, candidate H0 harnesses, risk notes. | active agents, provider routes, tool grants. | Manual mapping only. |
| `PilotRoutingDecision` | Manual route rationale. | decision id, selected lane/harness, reason, alternatives, constraints, human authority. | automatic router config, model routing, provider routing. | Manual decision record. |
| `PilotMemoryManifest` | Context & Memory Fabric package. | context refs, memory slices, blackboard refs, topology context, limitations. | persistent memory, retrieval endpoint, embeddings. | Markdown/context metadata only. |
| `PilotHarnessInputPackage` | Package the user may copy to an H0 harness. | ticket text, context refs, allowed files, blocked files, expected output, stop rules. | secrets, credentials, blocked source, dispatch hook. | Manual copy only. |
| `PilotHarnessOutputPackage` | User-returned harness output. | summary, files created/modified, commands run, decisions, limitations, blockers. | accepted-by-default flag, commit hook, approval token. | Proposed output only. |
| `PilotReviewInputPackage` | Input to reviewer mesh. | output refs, scope, evidence, risk markers, boundary checklist, reviewer needs. | automatic assignment trigger, auto-review flag. | Manual review input only. |
| `PilotReviewerMesh` | Manual review coverage topology. | reviewer cells, immune safeguards, checks, escalation path, containment recommendations. | live mesh, automatic reviewer assignment. | Metadata only. |
| `PilotReviewVerdict` | Reviewer result metadata. | verdict, findings, required rework, blockers, escalation, limitations. | Git approval, automatic acceptance. | ReviewVerdict is not approval. |
| `PilotIntegrationSummary` | Manual synthesis of reviewed outputs. | accepted changes, rejected changes, drift, risks, evidence, open questions. | automatic integration, broad staging permission. | Manual synthesis only. |
| `PilotDriftRegister` | Records scope/content/process drift. | drift id, source, severity, disposition, rework need, reviewer/integrator refs. | auto-remediation, hidden scope expansion. | Required before commit advice. |
| `PilotAcceptedOutputRegister` | Accepted output list. | exact accepted paths, rationale, review refs, limitations. | Git approval flag. | Acceptance metadata only. |
| `PilotRejectedOutputRegister` | Rejected output list. | rejected paths, reason, required action, exclusion from commit advice. | staging permission. | Rejected paths must not be staged. |
| `PilotCommitCandidate` | Advisory commit proposal. | exact paths, message, summary, accepted refs, rejected refs, rollback note. | actual staging flag, commit token, `git add .`. | Advisory only. |
| `PilotCommandBlock` | Exact command advice candidate. | status command, exact add commands, commit message, push command, human warning. | wildcard staging, force push, auto-run flag. | User manual Git only. |
| `PilotHumanFinalDecision` | Human final decision on acceptance and Git. | decision, rationale, accepted risk, commands run by user if any. | delegated final approval to agent/harness. | Human user remains final authority. |
| `PilotAuditNote` | Pilot audit and closure note. | outcome, deviations, blockers, lessons, future ticket refs. | publication approval, runtime approval. | Feeds future P7.0.R closure. |

## 13. User Gateway Procedure

The later pilot starts with the User Gateway.

Procedure:

- Capture `PilotObjective` in the user's words.
- Confirm documentation-only governance scope.
- Name all excluded surfaces: product/Siamese source, external source, runtime, tools, providers, MCP, GBrain, Hermes, Cadence, Graphify rerun/adoption, Codegraph execution, persistence, vector DB, graph DB, publication, and Git mutation by agent.
- Confirm that the pilot is manual only.
- Confirm that the user remains final authority.
- Stop if the user objective requires blocked scope.

## 14. Roadmap / Work Breakdown Procedure

The later pilot uses the roadmap/work breakdown contract to convert the objective into manual work packets.

Procedure:

- Create a small documentation-only roadmap.
- Identify `TaskGraphRef` / `TaskGraphProjection` metadata.
- Identify `BlackboardRef` metadata for claims, blockers, evidence, and unresolved questions.
- Create `ManualWorkPacketProjection` records with exact scope and exclusions.
- Preserve all blocked boundaries.
- Do not create runnable tasks, dispatch work, or execute handoffs.

## 15. Task Graph / Blackboard Procedure

`PilotTaskGraph` and `PilotBlackboard` are metadata only.

Procedure:

- Define task nodes for objective intake, context preparation, manual harness input, manual output return, review, integration, and commit advice.
- Define dependency, blocker, review, and integration edges.
- Define blackboard entries for evidence, constraints, unresolved questions, contradictions, drift, and blockers.
- Use blackboard evidence to support review, not to decide automatically.
- Do not create live shared state, persistence, event streaming, vector DB, graph DB, or live retrieval.

## 16. Capability Cell / Routing Procedure

Capability cells and routing decisions are manual metadata.

Procedure:

- Map the pilot to documentation/governance capability needs.
- Select manual lanes or H0 harness candidates based on risk, scope, and user preference.
- Record `PilotRoutingDecision` with selected route and rejected alternatives.
- Prefer one small H0 harness route for the first pilot if the user elects to use a harness.
- Do not activate agents, tools, providers, or automatic routing.

## 17. Context & Memory Fabric Procedure

Context & Memory Fabric is manual context packaging only.

Procedure:

- Assemble `PilotMemoryManifest` from approved governance docs and exact context refs.
- Include only required snippets or references needed for the later pilot.
- Track task memory, cell memory, blackboard memory, topology context, contradictions, and evidence conflicts as metadata.
- Exclude secrets, credentials, `.env`, provider configs, token stores, browser auth, API keys, local credential stores, product/Siamese source, external source, raw Graphify output, and GBrain source.
- Do not create persistent memory, vector DB, graph DB, embeddings, semantic search, ontology runtime, or live retrieval.

## 18. Manual Harness Procedure

P7.0.H uses P7.0.E semantics.

Required harness decisions:

- H0 manual harness use is allowed.
- H1 metadata-only design is allowed.
- H2 controlled tool execution adapter is blocked.
- H3 autonomous orchestration adapter is blocked.
- OpenCode may be used manually by the user.
- Codex / Claude / Cursor may be used manually by the user.
- Hermes remains candidate-only; no runtime.
- GBrain remains candidate-only; no runtime.
- Graphify remains evidence-only; no rerun/adoption.
- MCP/provider/auth/API/live connectors are blocked.
- `HarnessOutputPackage` is not accepted by default.

Procedure:

- Generate `PilotHarnessInputPackage` for a documentation-only governance task.
- The user manually copies the package into OpenCode, Codex, Claude, Cursor, or equivalent H0 surface if they choose.
- The user manually returns the result as `PilotHarnessOutputPackage`.
- The lead agent may summarize returned output but cannot automatically dispatch, accept, integrate, or commit it.

## 19. Reviewer Mesh / Immune Safeguard Procedure

P7.0.H uses P7.0.F semantics.

Required review decisions:

- `ReviewerMesh` is metadata only.
- `ImmuneSafeguard` is metadata only.
- `ReviewRequest` is not automatic assignment.
- `ReviewVerdict` is not approval.
- Reviewer approval is not Git approval.
- `ContainmentAction` is recommendation only.
- `ReworkRequest` is not automatic dispatch.
- `HumanFinalDecision` is required for final acceptance and Git.

Procedure:

- Build `PilotReviewInputPackage` from the harness output and blackboard/context refs.
- Map reviewer cells for scope, governance, security boundary, harness boundary, integration, and Git advisory checks.
- Mark drift, contradictions, evidence conflicts, unsafe output, and scope violations.
- Produce `PilotReviewVerdict` as accept/rework/reject/escalate metadata.
- Escalate to user when final authority is needed.

## 20. Integrator / Commit Advisory Procedure

P7.0.H uses P7.0.G semantics.

Required integration decisions:

- `IntegrationSummary` is manual synthesis only.
- `DriftRegister` is required before commit advice.
- `AcceptedOutputRegister` is not Git approval.
- `RejectedOutputRegister` paths must not be staged.
- `CommitCandidate` is advisory only.
- `CommitCommandBlock` must use exact paths.
- Never recommend git add .
- User performs Git manually.

Procedure:

- Create `PilotIntegrationSummary` only after review.
- Create `PilotDriftRegister` before commit advice.
- Separate accepted and rejected outputs.
- Create `PilotCommitCandidate` only for accepted exact paths.
- Create `PilotCommandBlock` as exact-path advice only.

Required command pattern:

```powershell
git status --short

git add <exact_path_1>
git add <exact_path_2>

git commit -m "<exact commit message>"

git push origin main
```

## 21. Drift And Rework Procedure

Drift and rework are manual controls.

Procedure:

- Record all scope, content, evidence, security, validation, harness, reviewer, integration, and Git advisory drift in `PilotDriftRegister`.
- If drift is minor and within scope, reviewer/integrator may recommend rework.
- If drift touches blocked surfaces, stop and escalate to user.
- If rework is needed, create `ReworkRequest` metadata only.
- Do not automatically dispatch rework.
- Do not automatically assign reviewers.
- Do not automatically integrate revised output.

## 22. Git Advisory Procedure

Git remains user-owned.

Procedure:

- Produce `PilotCommitCandidate` only after accepted output and drift review.
- Include exact paths only.
- Exclude rejected output paths.
- Include rollback note and limitations.
- Include `PilotCommandBlock` as advice only.
- User manually decides whether to stage, commit, and push.
- Agent and harnesses must not stage, commit, push, force-add, publish, or recommend `git add .`.

## 23. Success Criteria

The later pilot is successful if:

- user objective is captured with exact scope
- topology selection is recorded
- task graph is defined
- blackboard / evidence / blocker space is defined
- capability cells are mapped
- manual execution projection creates exact work packets
- H0 harness input package is generated
- user can manually run the harness
- output can be returned as HarnessOutputPackage
- reviewer mesh can review it
- immune safeguards can mark drift/blockers
- integrator can reconcile outputs
- commit advice can be exact-path only
- no blocked runtime/source/provider/product/Git behavior is introduced

## 24. Failure Criteria

The later pilot fails or must stop if:

- source scope is unclear
- product/Siamese source is required
- external source content is required without EXT gate
- runtime activation is implied
- autonomous orchestration is implied
- tool execution by AGENT PLATFORM is required
- provider/auth/API/MCP is required
- GBrain runtime is required
- Hermes runtime or Cadence is required
- Graphify rerun/adoption is required
- validation execution/tests/scripts/builds are required
- security enforcement/scanners are required
- persistent memory/vector DB/graph DB is required
- generated output tracking is required
- source tracking expansion is required
- publication is required
- Git mutation by the agent is required
- `git add .` is recommended

## 25. Stop Rules

STOP if P7.0.H attempts to execute the pilot, start P7.1, start P7.0.R, modify P7.0.A/B/C/D/E/F/G, activate runtime, execute agents/tasks/handoffs, dispatch work automatically, assign reviewers automatically, activate tools, activate providers/auth/API/MCP, use credentials, call APIs/network/MCP, activate live connectors, activate OpenCode internally, activate Hermes runtime, activate GBrain runtime, activate Cadence, rerun or adopt Graphify, execute or adopt Codegraph, inspect product/Siamese source, inspect external source, inspect GBrain source, inspect raw Graphify output, load source, run validation/tests/CI/scripts/builds, activate security enforcement, create persistence/database/event stream/telemetry, create vector DB/embeddings/graph DB/ontology runtime, track generated outputs, expand source tracking, publish, stage/commit/push, mutate Git, recommend `git add .`, or select Cognitive Semantic System substrate.

## 26. P7 Peer Alignment Register

| Peer | Status | P7.0.H disposition | Drift handling |
| --- | --- | --- | --- |
| P7.0.E harness boundary | present | consumed_by_P7.0.H | resolved_for_playbook_by_current_presence_check |
| P7.0.F reviewer mesh | present | consumed_by_P7.0.H | resolved_for_playbook_by_current_presence_check |
| P7.0.G integrator commit protocol | present | consumed_by_P7.0.H | resolved_for_playbook_by_current_presence_check |
| P7.0.R closure | not_started_expected | future_closure_required | P7.0.R will perform final closure. |

P7.0.H does not modify P7.0.E/F/G to clean stale peer markers. P7.0.R will perform final closure.

## 27. Pilot Readiness Register

| Readiness item | Status | Evidence posture | Required later action |
| --- | --- | --- | --- |
| Agent-native research carry-forward | ready | P7.0.0 present. | Use conceptual pattern set only. |
| User Gateway | ready | P7.0.A present. | Capture objective manually. |
| Roadmap / Work Breakdown | ready | P7.0.B present and marker checks pass. | Build manual roadmap and work packets. |
| Manual Lane Projection | ready | P7.0.C present and marker checks pass. | Map lanes/harnesses manually. |
| Context / Memory Manifest | ready | P7.0.D present. | Build context packages only. |
| Manual Harness Boundary | ready | P7.0.E present and H0 marker check passes. | Use H0 only unless H1 design-only is explicitly scoped. |
| Reviewer Mesh | ready | P7.0.F present and ReviewerMesh marker check passes. | Review manually. |
| Integrator / Commit Advisory | ready | P7.0.G present and CommitCandidate marker check passes. | Produce exact-path advice only. |
| Operational readiness audit | ready | Required input present. | Preserve operational boundaries. |
| P7.1 execution | not started | Future recommended pilot. | Start only by explicit future ticket. |
| P7.0.R closure | not started | Future closure. | Start only after P7.0.H and any pilot evidence are ready. |

## 28. Future Validation Targets

Future validation targets, not executed by P7.0.H:

| Target | Purpose |
| --- | --- |
| Required P7.0.0 and P7.0.A-G presence | Confirm playbook prerequisites. |
| TaskGraphRef marker presence | Confirm P7.0.B alignment. |
| BlackboardRef marker presence | Confirm P7.0.B alignment. |
| ManualExecutionProjection marker presence | Confirm P7.0.C alignment. |
| H0 harness marker presence | Confirm P7.0.E readiness. |
| ReviewerMesh marker presence | Confirm P7.0.F readiness. |
| CommitCandidate marker presence | Confirm P7.0.G readiness. |
| Lifecycle stage completeness | Confirm all 19 lifecycle stages are represented. |
| Object model completeness | Confirm all pilot objects are defined. |
| Manual-only invariant | Confirm no runtime/dispatch/review/integration/Git automation. |
| H0-only first pilot invariant | Confirm first pilot does not require H2/H3. |
| HarnessOutputPackage review invariant | Confirm harness outputs are not accepted by default. |
| DriftRegister before commit advice invariant | Confirm drift is handled before command advice. |
| Exact-path Git command invariant | Confirm no broad staging and no `git add .`. |
| Product/Siamese block invariant | Confirm no product source or product activation. |
| Provider/API/MCP block invariant | Confirm no provider/auth/API/MCP activation. |
| GBrain/Hermes/Cadence block invariant | Confirm candidate-only posture. |
| Graphify/Codegraph block invariant | Confirm no rerun/execution/adoption. |
| P7.0.R closure readiness | Confirm closure can consume pilot-readiness register. |

## 29. Future Hardening Candidates

Future candidates, not started:

| Candidate | Purpose |
| --- | --- |
| P7-PILOT-HARD-01 - PilotObjective Template | Create a reusable objective capture template. |
| P7-PILOT-HARD-02 - PilotTaskGraph Checklist | Harden task graph metadata completeness. |
| P7-PILOT-HARD-03 - PilotBlackboard Checklist | Harden evidence/blocker/contradiction capture. |
| P7-PILOT-HARD-04 - H0 HarnessInputPackage Template | Create safe H0 prompt/context package template. |
| P7-PILOT-HARD-05 - HarnessOutputPackage Review Checklist | Harden returned output review. |
| P7-PILOT-HARD-06 - PilotReviewerMesh Checklist | Harden reviewer mesh coverage. |
| P7-PILOT-HARD-07 - PilotDriftRegister Checklist | Harden drift capture before integration. |
| P7-PILOT-HARD-08 - PilotCommitCandidate Checklist | Harden exact-path commit advice. |
| P7-PILOT-HARD-09 - P7.1 First Pilot Execution Ticket Template | Prepare future P7.1 ticket form without starting it. |
| P7-PILOT-HARD-10 - P7.0.R Closure Evidence Checklist | Prepare future closure checklist without starting it. |

## 30. Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_first_manual_agentic_workflow_pilot_playbook.md`

Modified:

- none

Not created / not approved:

- no pilot execution
- no P7.1
- no P7.0.R
- no runtime activation
- no autonomous orchestration
- no automatic dispatch
- no automatic reviewer assignment
- no automatic integration
- no OpenCode integration
- no Hermes runtime
- no GBrain runtime
- no Cadence
- no MCP
- no provider/auth/API
- no tool execution
- no agent execution
- no source loading
- no product/Siamese source inspection
- no external source inspection
- no Graphify rerun/adoption
- no Codegraph execution/adoption
- no validation execution
- no security enforcement activation
- no persistence/vector DB/graph DB
- no generated output tracking
- no source tracking expansion
- no publication
- no Git mutation
- no Cognitive Semantic System substrate selection

## 31. Final Verdict

P7.0.H creates the First Manual Agent-Native Pilot Playbook.

The playbook recommends P7.1-FIRST-PILOT as a documentation-only AGENT PLATFORM governance/manual workflow pilot.

P7.0.H consumes P7.0.0 and P7.0.A-G.

P7.0.H resolves E/F/G peer presence for playbook readiness by current presence check.

P7.0.H does not execute the pilot.

P7.0.H does not start P7.1.

P7.0.H does not start P7.0.R.

P7.0.H does not activate runtime, autonomous orchestration, tool execution, provider/auth/API/MCP, GBrain, Hermes, Cadence, product source, Graphify, Codegraph, persistence, vector DB, graph DB, generated/source tracking, publication, Git mutation, or Cognitive Semantic System substrate selection.

Recommended next ticket:

P7.0.R - Manual Agent-Native Workflow Closure.
