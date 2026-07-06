# Platform MVP Scope / External Integration Boundary

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Platform MVP Scope / External Integration Boundary |
| Ticket | P8.0 |
| Status | Accepted Platform MVP Scope / External Integration Boundary |
| Date | 2026-07-06 |
| Scope | Documentation-only P8 scope and external integration boundary for AGENT PLATFORM / Siamese. |
| Authority | P8 scope and external integration boundary only, not implementation, not runtime activation, not autonomous orchestration, not automatic dispatch, not automatic reviewer assignment, not automatic integration, not Git mutation, not product/Siamese source inspection, not OpenCode execution, not Graphify execution, not GBrain runtime, not GStack execution, not Hermes runtime, not Cadence, not provider/auth/API/MCP activation, not live connector activation, not persistence, not vector DB, not graph DB, not Cognitive Semantic System substrate selection, and not publication. |
| Serial dependency | P8.0 must complete before P8.1-P8.5. |
| Related documents | P7.R, P7.0.A-P7.0.H, P6.7, P6.1-P6.6, P5.R, P5.1-P5.7, P3.BR, P3.3, P3.4, P3.5, P2.1, P2.2, P2.3, P2.KR, P1.1-P1.5, P0.1-P0.3, S-03, S-04, CSS ADR/audit. |
| External candidates | Graphify, GBrain, GStack, Hermes, OpenCode. |
| Output | Platform MVP Scope / External Integration Boundary. |
| Target result | p8_platform_mvp_scope_external_integration_boundary_ready |

## 2. Purpose

P8 transforms the validated P7 manual workflow into a local interactive MVP, not into autonomous runtime.

P8.0 defines MVP scope and external integration boundaries. It separates external candidate inventory, contracts/adapters design, local minimal interaction surface, and later activation gates.

P8.0 defines what `MVP-0` may become: a local interactive manual workflow assistant that helps the user operate the P7 manual workflow with better structure and less copy/paste overhead.

P8.0 defines what P8.1-P8.5 may analyze after P8.0, how P8.6-P8.9 should be gated after P8.1 and P8.5, and that P8.10/P8.11 must authorize implementation before P8.12+.

P8.0 blocks runtime activation, external runtime adoption, product integration, provider/API/MCP, persistent memory, vector/graph DB, Graphify rerun, OpenCode execution from AGENT PLATFORM, Hermes runtime, GBrain runtime, GStack execution, and Git mutation.

## 3. Current Posture

P7.R allows repeated manual workflow use. P7.R does not approve runtime activation. P8.0 opens controlled MVP planning, not mass activation.

| Area | Current state | P8.0 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| P7.R closure | Manual workflow maturity closure is present. | Manual workflow is mature for repeated governance documentation use. | Runtime readiness. |
| manual workflow maturity | Compact and full canonical workflows are available. | P8 may plan local interaction support. | Autonomous AGENT PLATFORM. |
| runtime readiness | Not established. | runtime activation blocked. | Active agent runtime. |
| product integration readiness | Not established. | product/Siamese deferred. | Product/Siamese source readable by default. |
| OpenCode integration readiness | Not established. | OpenCode remains H0 user-operated. | Active OpenCode adapter. |
| provider/API/MCP readiness | Not established. | Provider/API/MCP remains blocked. | Active provider/auth/API/MCP. |
| GBrain/Hermes/Cadence readiness | Not established. | Candidate-only posture. | Active GBrain runtime, active Hermes runtime, or active Cadence. |
| Graphify candidate | External evidence/architecture map candidate. | `GraphifyReadOnlyEvidenceCandidate`. | Active Graphify runner or Graphify authority. |
| GBrain candidate | Memory architecture candidate. | `GBrainMemoryArchitectureCandidate`. | Active GBrain runtime or persistent memory. |
| GStack candidate | Skill stack / GBrain compatibility candidate. | `GStackSkillStackCandidate`. | Active GStack runtime or GStack execution. |
| Hermes candidate | Interface/runtime/orchestration candidate. | `HermesInterfaceRuntimeCandidate`. | Active Hermes runtime or orchestration. |
| OpenCode candidate | H0 manual harness candidate. | `OpenCodeH0HarnessCandidate`. | OpenCode execution from AGENT PLATFORM. |
| local interaction layer | Not implemented. | Candidate MVP-0 planning scope. | CLI/TUI/web shell implementation in P8.0. |
| schemas | Not created in P8.0. | Future P8.3 schema candidates. | Runtime schemas or execution contracts. |
| local state | Not created in P8.0. | Future P8.4 state model. | Persistent DB, telemetry, vector DB, graph DB. |
| external inventory | Path/class metadata only. | Future P8.1 inventory rules. | External source content inspection. |
| adapter design | Design boundary only. | Future P8.6-P8.9 candidate boundaries. | Adapter execution. |
| adapter execution | Blocked. | adapter execution blocked. | Executable adapters or live connectors. |
| product/Siamese | Product vision. | Deferred to P4 / GT-09. | Product generator or source access. |
| Git authority | User-owned. | no Git mutation by agent. | Automatic commit or push. |

## 4. Inputs Reviewed

| Input group | Document | Review mode | P8.0 use | Limitation |
| --- | --- | --- | --- | --- |
| P7.R closure and P7 workflow docs | P7 maturity closure, P7.0.R, P7.0.A-H, P7.1, P7.1.R, P7.2, P7.3 where present | `manual_workflow_closure_review` | Confirms P7 manual workflow maturity and compact mode readiness. | No P7 document modified. Legacy `agent_platform_manual_reviewer_approval_pipeline_contract.md` path was absent; accepted P7.0.F reviewer mesh contract is present. |
| P7.0.0 / agent-native alignment docs | Agent-native research carry-forward and manual bridge docs | `agent_native_alignment_review` | Confirms conceptual topology, task graph, blackboard, capability, review, routing, and memory projections. | Conceptual only. |
| P7 compact pilot/runbook docs | Compact runbook and P7.3 report | `manual_workflow_closure_review` | Confirms compact workflow works for documentation/governance tasks. | Does not establish runtime readiness. |
| P6 operational contracts | Operational readiness, capability, communication, evidence, approval, monitoring/incident records | `operational_contract_review` | Preserves operational planning boundaries. | No runtime activation. |
| P5 skeleton baseline | Minimal active audit and implementation candidate records | `implementation_skeleton_review` | Provides inert skeleton and deferred activation posture. | No implementation created. |
| P3 activation decisions | Activation closure and tool/provider/agent decisions | `activation_decision_review` | Preserves blocked provider/tool/agent runtime posture. | No activation. |
| P2/P2.K knowledge architecture | Knowledge/retrieval, vocabulary, evidence, retention/rollback records | `metadata_contract_review` | Supports metadata vocabulary and evidence refs. | No live retrieval or persistence. |
| P1 metadata contracts | Context/provider/tool/agent/CSS hardening records | `metadata_contract_review` | Supports object and boundary naming. | Metadata is not execution. |
| P0 gates/security/validation | Activation gates, validation gates, security hardening | `security_policy_review` | Preserves gate and stop-rule posture. | No security enforcement. |
| S-03/S-04 policies | Tool/shell/network/MCP and local-only secrets policies | `security_policy_review` | Preserves shell/network/MCP and secret boundaries. | No credentials inspected. |
| CSS ADR/audit | Cognitive Semantic System naming and audit | `metadata_contract_review` | Preserves Cognitive Semantic System name and substrate deferral. | No substrate selection. |
| external candidates, path/class metadata only | Graphify, GBrain, GStack, Hermes, OpenCode, Codegraph candidates | `external_candidate_path_only_review` | Defines candidate classes and gates. | External source paths checked only; no content inspection or tree enumeration. |
| blocked surfaces | product source, external source content, credentials, generated output contents, runtime files | `not_reviewed_blocked` | Named only as blocked surfaces. | Not inspected. |

## 5. P8 Core Principle

P8 must not integrate Graphify, GBrain, GStack, Hermes, and OpenCode all at once as runtime.

| Track | Allowed in P8.0 | Delegated ticket | Blocked shortcut | Required later gate |
| --- | --- | --- | --- | --- |
| External candidate inventory | Define inventory principles and candidate classes. | P8.1 | Source content inspection or adoption by path presence. | ExternalInspectionPolicy and explicit review gate. |
| Contracts/adapters design | Define design-vs-execution boundary. | P8.3, P8.6-P8.9 | Executable adapters or live connectors. | AdapterDesignBoundary plus activation gate. |
| Local minimal interaction surface | Define MVP-0 interaction scope. | P8.2 | CLI/TUI/web shell implementation in P8.0. | P8.10/P8.11 authorization before implementation. |
| Later activation gates | Define that gates are required. | P8.5 | Runtime activation by planning document. | Security / Activation Gate Model. |

## 6. MVP-0 Definition

`MVP-0` means the MVP-0 local interactive manual workflow assistant.

MVP-0 is a local interactive manual workflow assistant. MVP-0 is not autonomous runtime and not product generator.

| MVP-0 capability | Allowed scope | Blocked automation | Likely future ticket |
| --- | --- | --- | --- |
| capture user objective | Manual objective intake and boundary prompts. | Automatic task dispatch. | P8.2 |
| generate WorkPacket | Render text/object from user input. | Runtime task creation. | P8.3 |
| generate HarnessInputPackage | Prepare copy/paste package for H0 harness. | Automatic harness dispatch. | P8.3 / P8.9 |
| register context metadata | Local metadata refs only. | Source loading or automatic retrieval. | P8.4 |
| register memory metadata | Manual memory refs only. | GBrain runtime or persistent memory. | P8.4 / P8.7 |
| register evidence metadata | Evidence refs and blackboard metadata. | Graphify authority or source of truth. | P8.3 / P8.6 |
| accept pasted OpenCode/other harness output | User-pasted text intake. | OpenCode execution from AGENT PLATFORM. | P8.2 / P8.9 |
| structure HarnessOutputPackage | Parse/structure user-pasted output manually or assisted. | Automatic acceptance. | P8.3 |
| render assisted review checklist | Display/manual checklist. | Automatic reviewer assignment or auto-review. | P8.2 / P8.5 |
| render assisted integration checklist | Display/manual checklist. | Automatic integration. | P8.2 / P8.5 |
| render DriftRegister | Local metadata artifact candidate. | Telemetry/event stream. | P8.3 / P8.4 |
| render AcceptedOutputRegister | Local metadata artifact candidate. | Git staging approval. | P8.3 |
| render RejectedOutputRegister | Local metadata artifact candidate. | Staging rejected paths. | P8.3 |
| render CommitCandidate | Exact-path advisory metadata. | Git mutation. | P8.3 / P8.5 |
| render exact-path CommitCommandBlock | Exact Git command text for user. | Automatic commit/push. | P8.2 / P8.5 |
| preserve user manual Git authority | Human-only Git execution. | Agent Git mutation. | All P8 tickets |

## 7. MVP-0 Non-Goals

MVP-0 non-goals:

- no autonomous orchestration
- no automatic dispatch
- no automatic reviewer assignment
- no automatic integration
- no automatic review
- no automatic Git
- no product/Siamese source by default
- no provider/auth/API/MCP activation
- no credentials
- no OpenCode execution from AGENT PLATFORM
- no Graphify execution
- no GBrain runtime
- no GStack execution
- no Hermes runtime
- no Cadence
- no live connectors
- no persistent DB
- no vector DB
- no graph DB
- no automatic retrieval
- no source-of-truth external candidate
- no publication

## 8. P8 Scope Levels

These are preliminary P8.0 scope levels. P8.5 may later harden them into the full Security / Activation Gate Model.

| Scope level | Meaning | Allowed in P8.0 | Allowed later in P8 | Blocked interpretation | Required gate |
| --- | --- | --- | --- | --- | --- |
| `P8-S0` | Documentation and boundary only. | Yes; P8.0 itself is `P8-S0`. | P8.1-P8.5 design docs. | Implementation. | None beyond P8.0 scope. |
| `P8-S1` | Schemas and static templates only. | No creation in P8.0; design allowed. | P8.3 may propose schema candidates; implementation only after authorization. | Runtime schemas or execution contracts. | P8.10/P8.11 before implementation. |
| `P8-S2` | Local non-executing interaction surface. | Design only. | P8.2 may evaluate; implementation only after authorization. | CLI/TUI/web shell now. | P8.10/P8.11. |
| `P8-S3` | Read-only metadata adapter design. | Design boundary only. | P8.6-P8.9 may define boundaries unless P8.5 gates otherwise. | Adapter execution. | P8.5 and specific candidate gate. |
| `P8-S4` | Human-approved controlled execution candidate, future only. | No. | Future candidate only if explicitly approved. | Silent execution or tool runtime. | Explicit activation gate. |
| `P8-S5` | Autonomous runtime. | No. | Blocked by default. | Autonomous AGENT PLATFORM. | Future activation-level review; currently blocked. |

Decisions: P8.0 itself is `P8-S0`. P8.1-P8.5 are `P8-S0` / design only. P8.6-P8.9 are boundary/design only unless P8.5 later gates otherwise. P8.10/P8.11 may authorize implementation plan. P8.12+ may implement only if P8.10/P8.11 authorize it. P8-S5 remains blocked.

## 9. External Candidate Classification

| Candidate | Candidate class | P8.0 status | Allowed P8.0 treatment | Blocked treatment | Next ticket |
| --- | --- | --- | --- | --- | --- |
| Graphify | `GraphifyReadOnlyEvidenceCandidate` | Candidate only. | Classify as repository graph/evidence graph/architecture map candidate. | Graphify execution, rerun, authority, source of truth, substrate. | P8.6 |
| GBrain | `GBrainMemoryArchitectureCandidate` | Candidate only. | Classify as memory architecture / persistent knowledge candidate. | GBrain runtime, persistent memory, graph/vector DB, automatic retrieval. | P8.7 |
| GStack | `GStackSkillStackCandidate` | Candidate only. | Classify as GBrain compatibility / skill stack candidate. | GStack execution, GStack runtime, adoption. | P8.1 / P8.7 |
| Hermes | `HermesInterfaceRuntimeCandidate` | Candidate only. | Classify as interface/runtime/orchestration candidate. | Hermes runtime, Cadence, automatic dispatch. | P8.8 |
| OpenCode | `OpenCodeH0HarnessCandidate` | H0 user-operated only. | Generate packages and accept pasted output later. | OpenCode execution from AGENT PLATFORM or adapter execution. | P8.9 |
| Codegraph | External analysis/tooling candidate only. | Not adopted. | Name as future candidate if considered. | Codegraph execution/adoption/authority. | Future EXT or P8 candidate review |
| provider/model APIs | Blocked external service surface. | Blocked. | Boundary metadata only. | Provider/auth/API activation. | Future explicit provider/auth/API gate |
| MCP servers/tools/resources | Blocked integration surface. | Blocked. | Boundary metadata only. | MCP activation, calls, tools, resources. | Future explicit MCP gate |
| live connectors | Blocked connector surface. | Blocked. | Boundary metadata only. | Active live connectors. | Future connector gate |
| product/Siamese integrations | Product-bound integration surface. | Deferred. | State P4 / GT-09 dependency. | Product source access by default. | P4 / GT-09 |
| Git tools | User manual Git only. | Advisory rendering candidate. | Render exact commands for user. | Agent Git mutation. | P8.5 / P8.10 |

## 10. Graphify Boundary

Graphify may be considered repository graph / evidence graph / architecture map candidate. Graphify may be considered read-only evidence provider or imported evidence candidate. Graphify is not source of truth. Graphify does not decide architecture. Graphify must not automatically rerun. Graphify must not write repo state. Graphify must not route work automatically. Graphify must not become Cognitive Semantic System substrate. P8.6 will define the detailed Graphify Read-Only Evidence Boundary.

| Graphify surface | P8.0 allowed classification | Blocked use | Future ticket |
| --- | --- | --- | --- |
| repository graph evidence | `GraphifyReadOnlyEvidenceCandidate` | Active Graphify runner, automatic rerun, source of truth. | P8.6 |
| architecture map evidence | Imported/read-only evidence candidate. | Architecture decision authority. | P8.6 |
| generated output | Path/class metadata only if governed. | Reading raw generated output contents in P8.0. | P8.6 / future evidence gate |
| routing | Not allowed. | Automatic work routing or dispatch. | Future activation gate only |

## 11. GBrain Boundary

GBrain may be considered memory architecture / persistent knowledge candidate / second-brain substrate candidate. GBrain is not adopted in P8.0. GBrain runtime is blocked. Persistent memory activation is blocked. Graph/vector DB activation is blocked. Automatic retrieval into agent context is blocked. GBrain source inspection requires later explicit gate. P8.7 will define the detailed GBrain / GStack Memory Compatibility Boundary.

| GBrain surface | P8.0 allowed classification | Blocked use | Future ticket |
| --- | --- | --- | --- |
| memory architecture candidate | `GBrainMemoryArchitectureCandidate` | GBrain runtime. | P8.7 |
| persistent knowledge candidate | Candidate metadata only. | Persistent DB, vector DB, graph DB. | P8.7 / later gate |
| context retrieval | Blocked. | Automatic retrieval into agent context. | Future runtime/retrieval gate |
| source review | Not allowed in P8.0. | GBrain source inspection. | Explicit external review gate |

## 12. GStack Boundary

GStack may be considered GBrain-compatible skill stack / bootstrap layer / agent workflow support candidate. GStack may be registered as external source candidate, GBrain compatibility candidate, and skill stack candidate. GStack is not adopted, not executed, and not runtime. GStack source inspection requires later explicit gate. P8.1 will inventory GStack path/class metadata. P8.7 will define memory compatibility boundary.

| GStack surface | P8.0 allowed classification | Blocked use | Future ticket |
| --- | --- | --- | --- |
| skill stack candidate | `GStackSkillStackCandidate` | GStack execution. | P8.1 / P8.7 |
| GBrain compatibility candidate | Candidate metadata only. | Adoption or runtime compatibility claim. | P8.7 |
| bootstrap layer candidate | Named candidate only. | Bootstrapping AGENT PLATFORM runtime. | Future gate |
| source review | Not allowed in P8.0. | GStack source inspection. | Explicit external review gate |

## 13. Hermes Boundary

Hermes may be considered agent runtime / orchestration candidate / possible interface candidate. Hermes UI feasibility may be studied later. Hermes runtime is blocked. Hermes orchestration is blocked. Cadence activation is blocked. Automatic dispatch is blocked. Autonomous orchestration is blocked. Hermes source inspection requires later explicit gate. P8.8 will define Hermes Interface / Runtime Candidate Boundary.

| Hermes surface | P8.0 allowed classification | Blocked use | Future ticket |
| --- | --- | --- | --- |
| interface candidate | `HermesInterfaceRuntimeCandidate` | Hermes runtime activation. | P8.8 |
| orchestration candidate | Candidate metadata only. | Hermes orchestration or automatic dispatch. | P8.8 / future activation gate |
| Cadence candidate | Named as blocked. | Active Cadence. | Future cadence gate |
| source review | Not allowed in P8.0. | Hermes source inspection. | Explicit external review gate |

## 14. OpenCode Boundary

OpenCode remains H0 user-operated harness initially. P8 may improve interaction with OpenCode manually. AGENT PLATFORM may generate HarnessInputPackage for OpenCode. User manually copies HarnessInputPackage to OpenCode. User manually pastes OpenCode output back into AGENT PLATFORM. AGENT PLATFORM may structure HarnessOutputPackage, assist review/integration, and generate CommitCandidate. OpenCode adapter execution is blocked until later gates. OpenCode execution from AGENT PLATFORM is blocked. P8.9 will define OpenCode Harness Upgrade Boundary.

| OpenCode surface | P8.0 allowed classification | Blocked use | Future ticket |
| --- | --- | --- | --- |
| manual harness | `OpenCodeH0HarnessCandidate` | OpenCode execution from AGENT PLATFORM. | P8.9 |
| HarnessInputPackage generation | Future MVP-0 manual package generation. | Automatic dispatch to OpenCode. | P8.2 / P8.9 |
| pasted HarnessOutputPackage intake | Future user-pasted output structuring. | Automatic acceptance or integration. | P8.2 / P8.9 |
| adapter | Design boundary only later. | Adapter execution. | P8.9 plus gate |

## 15. External Inspection Policy

P8.0 defines `ExternalInspectionPolicy` levels.

| Inspection level | Meaning | Allowed in P8.0 | Allowed later ticket | Blocked shortcut |
| --- | --- | --- | --- | --- |
| `EI-0` | Named candidate only. | Yes. | P8.1 may catalog. | Treating name as adoption. |
| `EI-1` | Path existence only. | Optional path-only checks. | P8.1 may propose rules. | Source tree enumeration. |
| `EI-2` | Shallow top-level metadata inventory. | No. | P8.1 may propose rules. | Content review by inventory. |
| `EI-3` | Controlled documentation/source review. | No. | Explicit external review gate. | Deep inspection without gate. |
| `EI-4` | Adapter design. | No implementation. | Candidate-specific boundary ticket. | Adapter execution. |
| `EI-5` | Adapter execution. | No. | Explicit activation gate only. | Executable adapters by default. |
| `EI-6` | Runtime adoption. | No. | Explicit runtime adoption gate only. | Runtime adoption by path presence. |

Decisions: P8.0 allows EI-0 and optional EI-1 only. P8.1 may propose EI-1/EI-2 rules. EI-3+ require explicit gates. EI-5/EI-6 are blocked by default.

## 16. Adapter Design Boundary

Adapter design may be documented later. Adapter contracts, static metadata refs, and read-only metadata adapter candidates may be designed later. Adapter execution remains blocked unless a later explicit gate authorizes it. Provider/auth/API/MCP adapters remain blocked. OpenCode adapter execution remains blocked. Graphify automatic rerun remains blocked. GBrain runtime adapter remains blocked. Hermes runtime adapter remains blocked. Product/Siamese adapters remain blocked until product readiness.

| Adapter type | P8.0 classification | Design status | Execution status | Future gate |
| --- | --- | --- | --- | --- |
| OpenCode adapter | H0 harness upgrade candidate. | Future design only. | adapter execution blocked. | P8.9 plus activation gate |
| Graphify adapter | Read-only evidence candidate. | Future design only. | Graphify rerun blocked. | P8.6 plus evidence gate |
| GBrain adapter | Memory architecture candidate. | Future design only. | GBrain runtime blocked. | P8.7 plus runtime gate |
| GStack adapter | Skill stack candidate. | Future design only. | GStack execution blocked. | P8.7 plus external gate |
| Hermes adapter | Interface/runtime candidate. | Future design only. | Hermes runtime blocked. | P8.8 plus runtime gate |
| provider/API/MCP adapter | Blocked external service adapter. | Boundary metadata only. | Execution blocked. | Provider/API/MCP activation gate |
| product/Siamese adapter | Product-bound future candidate. | Deferred. | Blocked. | P4 / GT-09 |

## 17. Local Interaction Surface Boundary

P8.2 may evaluate CLI local, TUI local, web local, Hermes-provided interface candidate, and hybrid markdown-first interface. P8.0 does not implement any of them.

MVP-0 interaction functions: user objective input, WorkPacket generator, HarnessInputPackage generator, pasted HarnessOutputPackage intake, review checklist, integrator checklist, CommitCandidate renderer.

| Surface option | P8.0 status | Allowed evaluation | Blocked implementation | Future ticket |
| --- | --- | --- | --- | --- |
| CLI local | Candidate interaction surface. | Compare suitability. | CLI implementation. | P8.2 / P8.10 |
| TUI local | Candidate interaction surface. | Compare suitability. | TUI implementation. | P8.2 / P8.10 |
| web local | Candidate interaction surface. | Compare suitability. | Web shell implementation. | P8.2 / P8.10 |
| Hermes-provided interface candidate | Candidate only. | Feasibility classification. | Hermes runtime. | P8.8 |
| hybrid markdown-first interface | Candidate interaction surface. | Compare low-risk markdown workflow. | State store or generator implementation. | P8.2 / P8.10 |

## 18. Core Workflow Object Boundary

Schema candidate is not runtime.

| Object | P8.0 meaning | Future schema ticket | Blocked interpretation |
| --- | --- | --- | --- |
| UserObjective | User-provided objective metadata. | P8.3 | Automatic task trigger. |
| WorkPacket | Manual work instruction object. | P8.3 | Runtime task. |
| HarnessInputPackage | Manual external harness input package. | P8.3 | Automatic dispatch package. |
| HarnessOutputPackage | User-pasted returned output structure. | P8.3 | Accepted-by-default output. |
| ReviewInputPackage | Bounded review context. | P8.3 | Source loading permission. |
| ReviewVerdictPackage | Review metadata. | P8.3 | Approval or Git approval. |
| IntegrationSummary | Manual synthesis. | P8.3 | Automatic merge. |
| DriftRegister | Drift metadata. | P8.3 | Telemetry/event stream. |
| AcceptedOutputRegister | Accepted output metadata. | P8.3 | Git approval. |
| RejectedOutputRegister | Rejected output metadata. | P8.3 | Staging permission. |
| CommitCandidate | Exact-path advisory metadata. | P8.3 | Commit execution. |
| CommitCommandBlock | Exact Git command rendering. | P8.3 | Git mutation. |

## 19. Local Workspace / State Boundary

P8.4 may later decide session state, draft work packets, returned harness outputs, review records, integration records, commit candidates, audit log, local-only artifacts, and ignored/generated artifacts.

Initial state model preference should be markdown/json local files, no database, no live retrieval, unless later tickets prove otherwise.

Blocked: persistent DB, vector DB, graph DB, GBrain runtime memory, automatic retrieval, telemetry/event stream.

| State surface | P8.0 decision | Blocked shortcut | Future ticket |
| --- | --- | --- | --- |
| session state | Future design only. | Persistent database. | P8.4 |
| draft work packets | Future local markdown/json candidate. | Runtime task queue. | P8.4 |
| returned harness outputs | Future local record candidate. | Automatic acceptance. | P8.4 |
| review records | Future local metadata candidate. | Auto-review. | P8.4 |
| integration records | Future local metadata candidate. | Automatic integration. | P8.4 |
| commit candidates | Future advisory artifact candidate. | Git mutation. | P8.4 / P8.5 |
| audit log | Future local-only artifact candidate. | Telemetry/event stream. | P8.4 |

## 20. Security / Activation Gate Boundary

P8.5 must later harden documentation/design level, schema/static template implementation level, local non-executing UI/CLI level, read-only metadata adapters level, human-approved controlled execution candidate level, and autonomous runtime blocked level.

P8.0 keeps blocked: provider/auth/API/MCP, credentials, tool execution, agent execution, OpenCode adapter execution, GBrain runtime, GStack execution, Hermes runtime, Graphify rerun, and Git mutation.

| Gate surface | P8.0 decision | Future gate |
| --- | --- | --- |
| documentation/design | Allowed in P8.0. | P8.5 hardening. |
| schema/static template implementation | Not implemented in P8.0. | P8.10/P8.11 before implementation. |
| local non-executing UI/CLI | Design only. | P8.2 then P8.10/P8.11. |
| read-only metadata adapters | Boundary/design only. | P8.5 and candidate-specific gates. |
| human-approved controlled execution candidate | Future only. | Explicit activation gate. |
| autonomous runtime | Blocked. | Future activation-level review, not P8.0. |

## 21. Product / Siamese Boundary

Siamese is product vision, not product activation. P8 MVP is AGENT PLATFORM interaction layer, not product generator. P8.0 does not inspect product/Siamese source. Product/Siamese source is blocked by default. Product-bound work requires P4 / GT-09 or equivalent product readiness gate. P8 MVP can be built before product integration.

| Product-bound scenario | P8.0 decision | Blocked shortcut | Future gate |
| --- | --- | --- | --- |
| product/Siamese source review | product/Siamese deferred. | Source readable by default. | P4 / GT-09 |
| product generator | Blocked. | Generating product/Siamese outputs. | P4 / product readiness |
| product-specific adapter | Deferred. | Product adapter creation. | P4 / GT-09 |
| product-bound validation | Deferred. | Running tests/builds/validation. | P4 plus explicit validation gate |

## 22. Git Boundary

AGENT PLATFORM may render CommitCandidate in future MVP. AGENT PLATFORM may render exact CommitCommandBlock. AGENT PLATFORM must not mutate Git. The user performs Git manually. Never recommend git add . CommitCandidate does not imply approval. Reviewer verdict does not imply Git approval. Integrator acceptance does not imply Git mutation.

Required command pattern:

```powershell
git status --short

git add <exact_path_1> `
        <exact_path_2>

git commit -m "<exact ticket message>"

git push origin main
```

| Git surface | Allowed future MVP behavior | Blocked behavior |
| --- | --- | --- |
| status | Render advisory `git status --short`. | Running Git automatically. |
| staging | Render exact-path `git add` commands. | `git add .`, broad staging, force-add. |
| commit | Render commit message candidate. | Automatic commit. |
| push | Render push command candidate. | Automatic push/publication. |
| approval | Require human final decision. | Reviewer/integrator verdict as Git approval. |

## 23. P8 Roadmap And Dependency Model

Dependency graph:

```text
P8.0
-> P8.1 / P8.2 / P8.3 / P8.4 / P8.5
-> P8.6 / P8.7 / P8.8 / P8.9
-> P8.10
-> P8.11
-> P8.12 / P8.13 / P8.14 / P8.15 / P8.16
-> P8.R
```

| Ticket | Purpose | Allowed after | Blocked until | Output |
| --- | --- | --- | --- | --- |
| P8.0 | Serial scope and boundary. | P7.R. | P7.R closure. | This boundary document. |
| P8.1 | External Source Inventory / Classification. | P8.0. | P8.0 completion. | Path/class metadata rules. |
| P8.2 | MVP Interaction Surface Architecture. | P8.0. | P8.0 completion. | Interaction surface decision. |
| P8.3 | Core Workflow Schema Candidates. | P8.0. | P8.0 completion. | Schema candidates only. |
| P8.4 | Local Workspace / State Model. | P8.0. | P8.0 completion. | Local state design. |
| P8.5 | Security / Activation Gate Model. | P8.0. | P8.0 completion. | Gate model. |
| P8.6 | Graphify Read-Only Evidence Boundary. | P8.1 and P8.5. | P8.1/P8.5. | Graphify boundary. |
| P8.7 | GBrain / GStack Memory Compatibility Boundary. | P8.1 and P8.5. | P8.1/P8.5. | Memory candidate boundary. |
| P8.8 | Hermes Interface / Runtime Candidate Boundary. | P8.1 and P8.5. | P8.1/P8.5. | Hermes boundary. |
| P8.9 | OpenCode Harness Upgrade Boundary. | P8.1 and P8.5. | P8.1/P8.5. | OpenCode boundary. |
| P8.10 | MVP Architecture / Implementation Plan. | P8.2-P8.9. | P8.2-P8.9 complete. | Implementation plan candidate. |
| P8.11 | Security / Approval Review For Implementation. | P8.10. | P8.10 complete. | Authorization or block. |
| P8.12-P8.16 | Implementation tickets if authorized. | P8.10/P8.11. | P8.10/P8.11 authorization. | Limited implementation only if approved. |
| P8.R | P8 closure. | P8.12-P8.16 or approved scope. | Prior P8 work complete. | Closure record. |

Decisions: P8.0 is serial. P8.1-P8.5 can run in parallel after P8.0. P8.6-P8.9 depend on P8.1 and P8.5. P8.10 depends on P8.2-P8.9. P8.11 depends on P8.10. P8.12-P8.16 require P8.10/P8.11 authorization. P8.R runs last.

## 24. Agent Work Allocation For P8

Agent allocation is manual planning only, not automatic dispatch.

| Agent | Suitable tickets | Responsibility | Blocked actions |
| --- | --- | --- | --- |
| Agent A - Platform / Architecture | P8.2, P8.10 | Interaction surface and architecture planning. | Implementation before authorization. |
| Agent B - External Sources / Integration Candidates | P8.1, P8.6-P8.9 | Candidate inventory and boundary docs. | Source content inspection, execution, adoption. |
| Agent C - Schemas / State / Data Model | P8.3, P8.4 | Schema candidates and local state model. | Database, vector DB, graph DB implementation. |
| Agent D - Security / Gates / Review | P8.5, P8.11 | Security and activation gate model. | Security enforcement activation or scanners. |
| Agent E - Implementation / Skeleton | P8.12-P8.16 only after P8.10/P8.11 | Limited implementation if authorized. | Runtime activation, adapters, autonomous execution without gate. |

## 25. Stop Rules

Stop on runtime activation request, autonomous orchestration request, automatic dispatch request, automatic reviewer assignment request, automatic integration request, automatic commit/push request, OpenCode execution request, OpenCode adapter implementation request, Graphify execution request, Graphify rerun request, Graphify as source of truth request, GBrain runtime request, GBrain persistent memory activation request, GStack execution request, Hermes runtime request, Hermes orchestration request, Cadence request, provider/auth/API/MCP activation request, credential request, API call request, MCP activation request, live connector request, product/Siamese source request, external source content inspection request, source loading request, source inspection request, tool execution request, agent execution request, persistence DB request, vector DB request, graph DB request, generated output tracking request, source tracking expansion request, publication request, Cognitive Semantic System substrate selection request, Git mutation by agent request, `git add .` recommendation request, request to create P8.1+ files in this ticket, or request to implement MVP package in this ticket.

## 26. Future Validation Targets

Future validation targets, not executed:

- P8.0 serial prerequisite invariant.
- P7.R closure dependency check.
- MVP-0 definition completeness.
- MVP-0 non-goals completeness.
- External candidate classification completeness.
- Graphify boundary completeness.
- GBrain boundary completeness.
- GStack boundary completeness.
- Hermes boundary completeness.
- OpenCode boundary completeness.
- ExternalInspectionPolicy completeness.
- AdapterDesignBoundary completeness.
- Local interaction surface boundary completeness.
- Core workflow object boundary completeness.
- Local workspace/state boundary completeness.
- Security/activation gate boundary completeness.
- Product/Siamese boundary completeness.
- Git boundary completeness.
- No runtime activation invariant.
- No autonomous orchestration invariant.
- No automatic dispatch invariant.
- No provider/API/MCP invariant.
- No external runtime adoption invariant.
- No product/Siamese source invariant.
- No Git mutation invariant.
- No `git add .` invariant.
- P8.1-P8.5 readiness.

## 27. Future Hardening Candidates

Future tickets, not started:

| Candidate | Purpose |
| --- | --- |
| P8-HARD-01 - MVP-0 Scope Matrix Hardening | Harden MVP-0 scope levels. |
| P8-HARD-02 - ExternalInspectionPolicy Checklist | Harden external inspection gates. |
| P8-HARD-03 - ExternalCandidateRef Schema Candidate | Draft candidate metadata schema. |
| P8-HARD-04 - AdapterDesignBoundary Checklist | Harden design-vs-execution boundary. |
| P8-HARD-05 - Interaction Surface Decision Checklist | Harden CLI/TUI/web/markdown decision. |
| P8-HARD-06 - MVP-0 Non-Execution Invariant Checklist | Harden no-execution invariants. |
| P8-HARD-07 - CommitCandidate Git Safety Checklist | Harden exact-path Git advice. |
| P8-HARD-08 - Product/Siamese Deferral Checklist | Harden product deferral. |
| P8-HARD-09 - External Candidate Gate Matrix | Harden candidate gate routing. |
| P8-HARD-10 - P8.R Readiness Audit Input | Prepare closure audit inputs. |

## 28. Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_p8_platform_mvp_scope_external_integration_boundary.md`

Modified:

- none

Not created / not approved:

- no P8.1-P8.R files
- no implementation files
- no MVP package
- no schemas
- no CLI/TUI/web shell
- no state store
- no local workspace artifacts
- no adapters
- no executable adapters
- no OpenCode adapter
- no Graphify adapter
- no GBrain adapter
- no GStack adapter
- no Hermes adapter
- no provider/API/MCP adapter
- no product/Siamese adapter
- no runtime activation
- no autonomous orchestration
- no scheduler
- no Cadence
- no Hermes runtime
- no GBrain runtime
- no GStack execution
- no OpenCode execution from AGENT PLATFORM
- no Graphify execution
- no Codegraph execution
- no provider/auth/API/MCP activation
- no credentials
- no API calls
- no MCP calls
- no live connectors
- no product/Siamese source inspection
- no external source content inspection
- no source loading
- no tool execution
- no agent execution
- no task execution
- no handoff execution
- no automatic dispatch
- no automatic reviewer assignment
- no automatic integration
- no automatic commits
- no automatic pushes
- no persistence DB
- no vector DB
- no graph DB
- no telemetry
- no event streaming
- no generated output tracking
- no source tracking expansion
- no publication
- no Git mutation by the agent
- no Cognitive Semantic System substrate selection

## 29. Recommended Next Ticket

After P8.0, the recommended parallel queue is:

- P8.1 - External Source Inventory / Classification
- P8.2 - MVP Interaction Surface Architecture
- P8.3 - Core Workflow Schema Candidates
- P8.4 - Local Workspace / State Model
- P8.5 - Security / Activation Gate Model

Recommended actual: P8.1 - External Source Inventory / Classification.

Do not start P8.1. Do not start P8.2. Do not start P8.3. Do not start P8.4. Do not start P8.5. Do not start P8.6. Do not start P8.7. Do not start P8.8. Do not start P8.9. Do not start P8.10. Do not start P8.11. Do not start P8.12+. Do not start P8.R.

## 30. Final Verdict

P8.0 created `0_architecture/governance/agent_platform_p8_platform_mvp_scope_external_integration_boundary.md`.

P8.0 defined Platform MVP scope as a governed route from validated P7 manual workflow into MVP-0, a local interactive manual workflow assistant.

P8.0 defined `ExternalIntegrationBoundary`, `ExternalCandidateRef`, `ExternalCandidateClass`, `ExternalInspectionPolicy`, and `AdapterDesignBoundary` as metadata boundaries only.

MVP-0 may capture objectives, generate WorkPacket and HarnessInputPackage, accept pasted HarnessOutputPackage, render review/integration checklists, render DriftRegister, AcceptedOutputRegister, RejectedOutputRegister, CommitCandidate, and exact-path CommitCommandBlock.

MVP-0 must not activate runtime, automate orchestration, automatically dispatch, automatically assign reviewers, automatically integrate, execute OpenCode, execute Graphify, activate GBrain/Hermes/Cadence, use providers/API/MCP, inspect product/Siamese source, inspect external source contents, create persistence/vector DB/graph DB, or mutate Git.

P8.0 defined P8-S0 through P8-S5 scope levels. P8.0 is P8-S0; P8-S5 remains blocked.

P8.0 defined Graphify as `GraphifyReadOnlyEvidenceCandidate`, GBrain as `GBrainMemoryArchitectureCandidate`, GStack as `GStackSkillStackCandidate`, Hermes as `HermesInterfaceRuntimeCandidate`, and OpenCode as `OpenCodeH0HarnessCandidate`.

P8.0 defined that external candidate inspection is EI-0/EI-1 only in P8.0 and that EI-3+ require later explicit gates.

P8.0 defined that adapter design may be documented later, but adapter execution blocked until explicit later gates.

P8.0 defined local interaction surface, core workflow object, local workspace/state, security/activation gate, product/Siamese, and Git boundaries.

P8.0 defined the P8 roadmap/dependency model from P8.0 through P8.R.

P8.0 did not create implementation files, adapters, schemas, CLI/TUI/web shell, state store, MVP package, or runtime files.

P8.0 did not activate runtime, execute OpenCode, Graphify, GBrain, GStack, Hermes, Codegraph, tools, agents, providers, API, MCP, or live connectors.

P8.0 did not inspect external source contents or product/Siamese source.

P8.0 did not create persistence, vector DB, graph DB, telemetry, or event streaming.

P8.0 did not mutate Git.

Next recommended ticket: P8.1 - External Source Inventory / Classification.
