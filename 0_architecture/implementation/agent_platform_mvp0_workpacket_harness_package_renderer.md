# MVP-0 WorkPacket / Harness Package Renderer

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | MVP-0 WorkPacket / Harness Package Renderer |
| Ticket | P8.13 |
| Status | Accepted controlled MVP-0 renderer implementation |
| Date | 2026-07-06 |
| Scope | Controlled local inert WorkPacket / HarnessInputPackage renderer implementation for AGENT PLATFORM / Siamese MVP-0. |
| Authority | Local inert WorkPacket / HarnessInputPackage rendering only, not harness execution, adapter execution, provider/auth/API/MCP activation, credential use, tool execution, agent execution, live connector activation, OpenCode execution, Graphify execution/rerun/adoption, GBrain/GStack/Hermes execution, source loading, product/Siamese source inspection, persistence, vector DB implementation, embedding generation, graph DB implementation, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P8.10, accepted P8.11 authorization-boundary file, P8.12, P8.0, P8.2, P8.3, P8.4, P8.5, P8.9, accepted P7.0.F reviewer mesh file, P7.R, P7.0.B, P7.0.E, P7.0.G, S-03, S-04. |
| Output | WorkPacket / HarnessInputPackage renderer ready. |
| Output markers | `workpacket_harness_package_renderer_ready`; `compact_workpacket_renderer_ready`; `harness_input_package_renderer_ready`; `local_inert_template_rendering_only`; `limited_p8_l1_l2_non_executing_renderer_created`; `no_harness_execution`; `no_external_runtime_activation`; `no_git_mutation` |

## 2. Purpose

P8.13 implements only local package rendering. It supports the MVP-0 manual workflow by rendering Compact WorkPacket and HarnessInputPackage markdown/text from already validated in-memory metadata records.

P8.13 uses the corrected P8.11 path `0_architecture/governance/agent_platform_mvp0_implementation_plan_authorization_boundary.md` and the corrected P7.0.F reviewer path `0_architecture/governance/agent_platform_reviewer_mesh_immune_safeguards_contract.md`.

P8.13 keeps external harness use manual. It does not execute OpenCode, does not ingest harness output, does not render CommitCandidate, and does not mutate Git.

## 3. Current Posture

| Area | P8.13 posture |
| --- | --- |
| MVP-0 | Local interactive manual workflow assistant. |
| Renderer | Inert string renderer. |
| Renderer output | Advice/input text only. |
| Rendered package | Not dispatch. |
| Rendered package execution | Not execution. |
| Rendered package approval | Not approval. |
| Rendered package Git posture | Not Git mutation. |
| P8.11 authorization | Limited P8-L1/P8-L2 non-executing implementation only. |
| P8-L3 | Not authorized. |
| P8-L4 | Not authorized. |
| P8-L5 | Blocked. |

## 4. Prerequisite Path Normalization

| Concern | Accepted path | Legacy / corrected path | P8.13 handling |
| --- | --- | --- | --- |
| P8.11 implementation plan authorization boundary | `0_architecture/governance/agent_platform_mvp0_implementation_plan_authorization_boundary.md` | Legacy `0_architecture/governance/agent_platform_mvp0_implementation_plan.md` | Accepted path used; legacy path not required. |
| P8.11 authorization marker | `limited_p8_l1_l2_non_executing_implementation_plan_authorized` | None | Marker present and consumed. |
| P7.0.F reviewer mesh / immune safeguards | `0_architecture/governance/agent_platform_reviewer_mesh_immune_safeguards_contract.md` | Legacy `0_architecture/governance/agent_platform_manual_reviewer_approval_pipeline_contract.md` | Accepted path used; legacy path not required. |
| External source root | `4_external/sources` | Legacy `external/sources` | Corrected root used as path/class metadata only. |
| Known GStack path | `4_external/sources/gstack-main` | Legacy `external/sources/gstack` / `external/sources/gstack-master` | Path/class metadata only; no inspection, listing, import, execution, configuration, or adoption. |

## 5. Inputs Reviewed

| Input | Present | Consumed_as | Renderer_relevance | Limitations | Pending_alignment |
| --- | --- | --- | --- | --- | --- |
| P8.10 MVP-0 Architecture Synthesis | Yes | Required architecture synthesis | Confirms MVP-0 manual workflow and no runtime posture. | No implementation authorization by itself. | None. |
| Accepted P8.11 authorization-boundary | Yes | Required authorization | Authorizes limited P8-L1/P8-L2 non-executing implementation and blocks P8-L3/P8-L4/P8-L5. | No adapters or execution. | None. |
| P8.12 Skeleton Package doc | Yes | Required skeleton implementation record | Confirms target skeleton path and path normalization. | P8.12 does not implement rendering. | None. |
| P8.12 skeleton package path | Yes | Required package path | Host package for rendering subpackage. | Existing files not modified. | None. |
| P8.0 Platform MVP Scope / External Integration Boundary | Yes | Scope boundary | Defines MVP-0 and external integration blockers. | Not modified. | None. |
| P8.2 MVP Interaction Surface Architecture | Yes | Interaction surface metadata | Confirms manual local interaction surface. | No UI implemented. | None. |
| P8.3 Core Workflow Schema Candidates | Yes | Object naming metadata | Guides CompactWorkPacket and HarnessInputPackage names. | No JSON schema implementation. | None. |
| P8.4 Local Workspace / State Model | Yes | State boundary metadata | Confirms no persistence/state store in P8.13. | No storage created. | None. |
| P8.5 Security / Activation Gate Model | Yes | Security/activation boundary | Confirms P8-L1/P8-L2 limits and blockers. | No enforcement activated. | None. |
| P8.9 OpenCode Harness Upgrade Boundary | Yes | Harness boundary metadata | Preserves OpenCode H0 manual use and H1 design-only posture. | Historical peer absence markers are not changed. | None. |
| Accepted P7.0.F reviewer mesh file | Yes | Reviewer boundary metadata | Used as accepted reviewer path. | No review execution. | None. |
| P7.0.B Roadmap / Work Breakdown | Yes | WorkPacket lineage | Supports WorkPacket rendering. | No task dispatch. | None. |
| P7.0.E Manual Harness Boundary | Yes | Harness level model | Supplies H0/H1/H2/H3 semantics. | No harness execution. | None. |
| P7.0.G Integrator / Commit Advisory | Yes | Git/user authority metadata | Preserves manual Git authority. | No CommitCandidate rendering. | None. |
| S-03 Local-only / Secrets / Credentials Policy | Yes | Security boundary | Blocks secrets/credentials/local-only exposure. | No secrets inspected. | None. |
| S-04 Tool / Shell / Network / MCP Execution Policy | Yes | Execution boundary | Blocks shell, tools, network, provider/API/MCP, package/test/build execution. | No execution. | None. |
| `4_external/sources` | Yes | Path/class metadata only | Corrected external root. | Contents not listed or inspected. | None. |
| `4_external/sources/gbrain-master` | Yes | Path/class metadata only | Corrected GBrain path check. | Contents not inspected. | None. |
| `4_external/sources/gstack-main` | Yes | Path/class metadata only | Known GStack path/class metadata. | Contents not inspected; no import/configuration/adoption. | None. |

## 6. Dependency Posture

P8.10 is required and present.

P8.11 authorization-boundary is required and present. The accepted P8.11 file is `agent_platform_mvp0_implementation_plan_authorization_boundary.md`; the legacy P8.11 filename is not required.

P8.12 skeleton is required and present. P8.3 schema candidates guide object names. P8.4 state model guides future storage but P8.13 creates no persistence. P8.5 gates constrain renderer boundaries. P8.9 refines OpenCode H0 manual harness posture. Missing optional boundaries must be marked as pending, not guessed.

## 7. Implementation Scope

| File | Scope |
| --- | --- |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/__init__.py` | Safe rendering API exports only. |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/contracts.py` | Stdlib-only dataclass/enumeration renderer contracts. |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/markdown_sections.py` | Pure markdown section helpers. |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/workpacket_renderer.py` | CompactWorkPacket renderer returning RenderResult. |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/harness_input_renderer.py` | HarnessInputPackage renderer returning RenderResult. |
| `0_architecture/implementation/agent_platform_mvp0_workpacket_harness_package_renderer.md` | Implementation record. |

## 8. Renderer Object Model

| Object | Purpose | Boundary |
| --- | --- | --- |
| `RenderFormat` | Markdown/text render format enum. | Not execution mode. |
| `RenderSafetyPosture` | Safety posture enum. | Not runtime state. |
| `RendererConfig` | Renderer options and explicit no-runtime booleans. | No side effects. |
| `RenderBoundaryBlock` | Boundary statements. | Does not enforce runtime. |
| `StopRuleBlock` | Stop rules. | Does not execute. |
| `ContextRefBlock` | Context/memory ref metadata. | Refs are not permission. |
| `PathScopeBlock` | Provided allowed/blocked path text. | No path discovery. |
| `ReportingFormatBlock` | Expected response headings. | No review execution. |
| `ManualHarnessInstructionBlock` | Manual harness instructions. | No harness execution. |
| `CompactWorkPacket` | WorkPacket render input. | In-memory metadata only. |
| `HarnessInputPackage` | Harness package render input. | Manual copy/paste only. |
| `RenderedPackage` | Rendered package text object. | Text only. |
| `RenderResult` | Render operation result. | Includes warnings, blockers, not-created register, limitations. |

## 9. Compact WorkPacket Render Contract

The CompactWorkPacket renderer implements `render_compact_workpacket(work_packet: CompactWorkPacket, config: RendererConfig | None = None) -> RenderResult`.

Required sections rendered: Title, Ticket / WorkPacket ID, Objective, Scope, Target artifacts, Allowed scope, Blocked scope, Mandatory inputs, Optional inputs, Context / Memory refs, Evidence / Validation / Security refs, Harness expectations, Acceptance criteria, Stop rules, Expected closing response format, Not created / not approved register, and Limitations.

Default boundary statements include manual execution only, no automatic dispatch, no agent runtime activation, no tools/providers/MCP execution, no Git mutation, and user final execution/Git authority.

## 10. HarnessInputPackage Render Contract

The HarnessInputPackage renderer implements `render_harness_input_package(package: HarnessInputPackage, config: RendererConfig | None = None) -> RenderResult`.

Required sections rendered: Harness target, Harness level, WorkPacket reference, Manual copy/paste instructions, Prompt body, Mandatory context refs, Forbidden context refs, Allowed paths, Blocked paths, Expected outputs, Stop rules, Required reporting format, Boundary statements, Not created / not approved register, and Limitations.

Harness levels: `H0_user_operated_harness`, `H1_metadata_adapter_design`, `H2_controlled_execution_adapter_blocked`, and `H3_autonomous_orchestration_adapter_blocked`.

H0 and H1 may be rendered as allowed/manual/design-only. H2 and H3 render as blocked with warnings. OpenCode is rendered as H0 manual unless a later exact gate authorizes otherwise. Hermes target rendering includes blocked runtime/Cadence warnings. Provider/auth/API/MCP implied targets render blocked warnings.

## 11. Boundary Statements Rendered By Default

| Boundary statement | Render posture |
| --- | --- |
| no runtime activation | Rendered as blocker. |
| no automatic dispatch | Rendered as blocker. |
| no harness execution | Rendered as blocker. |
| no OpenCode execution | Rendered as blocker. |
| no provider/auth/API/MCP | Rendered as blocker. |
| no tool execution | Rendered as blocker. |
| no agent execution | Rendered as blocker. |
| no source loading | Rendered as blocker. |
| no product source inspection | Rendered as blocker. |
| no external source inspection | Rendered as blocker. |
| no Graphify/GBrain/GStack/Hermes execution | Rendered as blocker. |
| no persistence/vector/graph DB | Rendered as blocker. |
| no Git mutation | Rendered as blocker. |
| never `git add .` | Rendered as blocked command warning only, never as allowed command. |

## 12. Path Scope Handling

Allowed paths are rendered exactly as provided by the caller. Unknown paths produce warnings. Missing blockers produce conservative warnings. No path discovery is performed by renderer functions. No file existence checks occur inside renderer functions.

If `allowed_paths` is empty, rendered output states that allowed paths are unknown and must not be invented. If `blocked_paths` is empty, rendered output applies conservative blockers for product/Siamese source, external source contents, `4_external/sources` contents, raw generated outputs, secrets/credentials, `.env`, auth material, local credential stores, API keys, and Git mutation paths.

## 13. Context / Evidence / Security Refs Handling

Refs are rendered as metadata only. Refs are not permission. Context inclusion is not source loading permission. Evidence supports; it does not decide. Security constrains; it does not activate.

## 14. Security / Local-Only / Product Boundary

Renderer packages must not request secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, product/Siamese source, external source contents, raw generated outputs, or generated output tracking. If those surfaces are named, they are named as blocked surfaces only.

## 15. OpenCode H0 Boundary

OpenCode remains H0 user-operated harness. The user manually copies packages into OpenCode and manually pastes output back later. AGENT PLATFORM does not execute OpenCode, dispatch to OpenCode, configure OpenCode, or ingest output in P8.13.

## 16. Hermes / GBrain / GStack / Graphify Boundary

Hermes, GBrain, GStack, and Graphify remain candidate/evidence surfaces only. P8.13 creates no imports, adapters, execution, configuration, adoption, runtime, Cadence, Graphify rerun, GBrain memory runtime, or GStack skill runtime.

The corrected GStack path `4_external/sources/gstack-main` was checked only as path/class metadata. P8.13 did not list, open, inspect, import, execute, configure, or adopt GStack.

## 17. No Git Mutation Boundary

Exact path advice may appear only as ordinary text supplied to a renderer, but P8.13 does not create CommitCandidate rendering and does not mutate Git. The broad command `git add .` is never rendered as an allowed command; if supplied in allowed content, renderer functions remove it from allowed rendered content and return a warning.

## 18. Stop Rules

Stop if renderer work requires harness execution, OpenCode execution, automatic dispatch, provider/auth/API/MCP, tool execution, agent execution, task/handoff execution, source loading, source inspection, product/Siamese source inspection, external source content inspection, secrets/credentials, `.env`, Graphify/GBrain/GStack/Hermes execution/import/configuration/adoption/runtime, Cadence, persistence, vector DB, embeddings, graph DB, telemetry, event streaming, generated output tracking, source tracking expansion, publication, Git mutation, HarnessOutput intake, review checklist execution, integration checklist execution, or CommitCandidate rendering.

## 19. Future Validation Targets

Future validation targets, not executed:

| Target | Purpose |
| --- | --- |
| accepted P8.11 path invariant | Verify accepted authorization-boundary path is used. |
| legacy P8.11 not required invariant | Verify legacy filename is not required. |
| accepted P7.0.F reviewer path invariant | Verify reviewer mesh path is used. |
| legacy reviewer path not required invariant | Verify legacy reviewer path is not required. |
| corrected external source root invariant | Verify `4_external/sources` posture. |
| GStack path/class metadata only invariant | Verify `4_external/sources/gstack-main` is metadata only. |
| renderer contract completeness | Check required contracts. |
| CompactWorkPacket section completeness | Check required sections. |
| HarnessInputPackage section completeness | Check required sections. |
| H0/H1/H2/H3 rendering behavior | Check allowed/blocked level behavior. |
| no file I/O invariant | Check renderer functions do not perform file I/O. |
| no subprocess invariant | Check no subprocess/shell. |
| no network/API/MCP invariant | Check no network/API/MCP/provider calls. |
| no harness execution invariant | Check no harness execution. |
| no Git mutation invariant | Check no Git mutation. |
| no `git add .` invariant | Check broad Git staging command is never allowed. |
| unknown paths warning invariant | Check warnings for empty allowed paths. |
| conservative blocked paths warning invariant | Check default blockers for missing blocked paths. |
| P8.14 integration readiness | Future output intake alignment only. |
| P8.15 integration readiness | Future CommitCandidate alignment only. |

## 20. Future Hardening Candidates

| Candidate | Purpose |
| --- | --- |
| RENDER-HARD-01 - Renderer Contract Schema Alignment | Harden renderer contract schema. |
| RENDER-HARD-02 - Compact WorkPacket Template Hardening | Harden WorkPacket template. |
| RENDER-HARD-03 - HarnessInputPackage Template Hardening | Harden harness package template. |
| RENDER-HARD-04 - Harness Level Boundary Rendering Hardening | Harden H0/H1/H2/H3 behavior. |
| RENDER-HARD-05 - Path Scope Warning Contract | Harden path warnings. |
| RENDER-HARD-06 - Boundary Statement Rendering Contract | Harden boundary statements. |
| RENDER-HARD-07 - No Git Mutation Rendering Invariant | Harden Git blocker. |
| RENDER-HARD-08 - OpenCode H0 Package Template Review | Harden OpenCode H0 template. |
| RENDER-HARD-09 - P8.14 Output Intake Interface Alignment | Future P8.14 alignment. |
| RENDER-HARD-10 - P8.15 CommitCandidate Interface Alignment | Future P8.15 alignment. |

## 21. Created / Modified / Not Created Register

Created:

| File | Status |
| --- | --- |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/__init__.py` | Created. |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/contracts.py` | Created. |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/markdown_sections.py` | Created. |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/workpacket_renderer.py` | Created. |
| `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/harness_input_renderer.py` | Created. |
| `0_architecture/implementation/agent_platform_mvp0_workpacket_harness_package_renderer.md` | Created. |

Modified:

| Area | Status |
| --- | --- |
| Files outside exact target list | None. |

Not created / not approved:

| Surface | Status |
| --- | --- |
| P8.14 HarnessOutput intake | Not created. |
| P8.15 CommitCandidate renderer | Not created. |
| P8.16 pilot | Not created. |
| P8.R closure | Not created. |
| runtime activation | Not approved. |
| harness execution | Not approved. |
| OpenCode execution from AGENT PLATFORM | Not approved. |
| adapter implementation / executable adapter | Not created. |
| automatic dispatch / review / integration | Not approved. |
| Git mutation | Not approved. |
| provider/auth/API/MCP activation | Not approved. |
| credential use / API calls / MCP calls | Not performed. |
| tool execution / agent execution / live connector activation | Not performed. |
| Graphify execution/rerun/adoption | Not performed. |
| GBrain/GStack/Hermes execution/import/configuration/adoption/runtime | Not performed. |
| source loading / source inspection | Not approved. |
| product/Siamese source inspection | Not performed. |
| raw generated output inspection | Not performed. |
| secrets / credentials / `.env` inspection | Not performed. |
| validation execution / tests / CI / scripts / builds | Not performed. |
| security enforcement activation | Not performed. |
| persistence DB | Not created. |
| vector DB / embeddings | Not created. |
| graph DB / substrate selection | Not created or selected. |
| telemetry / event streaming | Not created. |
| generated output tracking / source tracking expansion | Not approved. |
| publication | Not performed. |
| Git mutation | Not performed. |

## 22. Recommended Next Ticket

Recommended next ticket: P8.14 - HarnessOutput Intake / Review Checklist.

After P8.14: P8.15 - Integrator / CommitCandidate Renderer.

After P8.15: P8.16 - MVP-0 Manual Pilot.

Do not start P8.14 from this ticket.

## 23. Final Verdict

| Question | Answer |
| --- | --- |
| What did P8.13 create? | The local inert MVP-0 WorkPacket / Harness Package Renderer. |
| What renderer files were created? | `__init__.py`, `contracts.py`, `markdown_sections.py`, `workpacket_renderer.py`, and `harness_input_renderer.py` under `3_platform/_governed_skeleton/agent_platform_mvp0/rendering/`. |
| What implementation doc was created? | `0_architecture/implementation/agent_platform_mvp0_workpacket_harness_package_renderer.md`. |
| Which P8.11 path was used? | `0_architecture/governance/agent_platform_mvp0_implementation_plan_authorization_boundary.md`. |
| Was the legacy P8.11 path required? | No. `0_architecture/governance/agent_platform_mvp0_implementation_plan.md` was not required. |
| Which P7.0.F reviewer path was used? | `0_architecture/governance/agent_platform_reviewer_mesh_immune_safeguards_contract.md`. |
| Was the legacy reviewer approval pipeline path required? | No. |
| What corrected external source root was recorded? | `4_external/sources`. |
| What GStack path/class metadata was recorded? | `4_external/sources/gstack-main`, path/class metadata only. |
| Did P8.13 inspect GStack? | No. |
| What renderer contracts were defined? | RenderFormat, RenderSafetyPosture, RendererConfig, RenderBoundaryBlock, StopRuleBlock, ContextRefBlock, PathScopeBlock, ReportingFormatBlock, ManualHarnessInstructionBlock, CompactWorkPacket, HarnessInputPackage, RenderedPackage, and RenderResult. |
| What CompactWorkPacket renderer was implemented? | `render_compact_workpacket`. |
| What HarnessInputPackage renderer was implemented? | `render_harness_input_package`. |
| Does renderer execute harnesses? | No: `no_harness_execution`. |
| Does renderer execute OpenCode? | No. |
| Does renderer dispatch tasks? | No. |
| Does renderer perform file I/O? | No renderer function performs file I/O. |
| Does renderer perform network/API/MCP/provider calls? | No. |
| Does renderer mutate Git? | No: `no_git_mutation`. |
| Does renderer ever render `git add .` as allowed? | No. It is rendered only as a blocked warning, and supplied allowed content containing it is removed with a warning. |
| Does renderer implement HarnessOutput intake? | No. |
| Does renderer implement review checklist execution? | No. |
| Does renderer implement CommitCandidate rendering? | No. |
| Does renderer activate Graphify/GBrain/GStack/Hermes? | No. |
| Does renderer inspect product/Siamese source? | No. |
| Does renderer create persistence/vector DB/graph DB? | No. |
| What are the known limitations? | Rendering is string-only and assumes input records were already validated in memory. No validation execution was run. |
| What is the recommended next ticket? | P8.14 - HarnessOutput Intake / Review Checklist. |

Final markers:

```text
workpacket_harness_package_renderer_ready
compact_workpacket_renderer_ready
harness_input_package_renderer_ready
local_inert_template_rendering_only
limited_p8_l1_l2_non_executing_renderer_created
no_harness_execution
no_external_runtime_activation
no_git_mutation
```
