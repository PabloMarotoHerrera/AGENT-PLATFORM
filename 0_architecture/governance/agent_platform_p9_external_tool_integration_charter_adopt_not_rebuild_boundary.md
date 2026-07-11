# External Tool Integration Charter / Adopt-Not-Rebuild Boundary

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | External Tool Integration Charter / Adopt-Not-Rebuild Boundary |
| Ticket | P9.0 |
| Status | Accepted external tool integration charter |
| Date | 2026-07-07 |
| Scope | Documentation-only charter for governed post-P8 external tool integration. |
| Authority | Charter only, not external source content inspection, not external source adoption, not external tool execution, not runtime activation, not autonomous orchestration, not OpenCode execution, not Graphify execution/rerun/adoption, not Hermes runtime, not GBrain runtime, not GStack execution, not ECC-main execution, not Codegraph execution, not provider/auth/API/MCP activation, not credential use, not API calls, not MCP activation, not live connector activation, not tool execution, not agent execution, not task execution, not handoff execution, not source loading, not source inspection, not product/Siamese source inspection, not validation execution, not test execution, not package-manager execution, not dependency installation, not persistence/database/event stream, not telemetry, not vector DB implementation, not embeddings generation, not graph DB implementation, not generated output tracking approval, not source tracking expansion approval, not publication approval, not Git mutation approval, and not Cognitive Semantic System substrate selection. |
| Required inputs | P8.R, P8.0, P8.5, P8.6, P8.7, P8.8, P8.9, S-03, S-04 |
| Output | External integration charter |
| Target file | `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md` |
| Result markers | `external_tool_integration_charter_ready`; `adopt_not_rebuild_boundary_accepted`; `validated_external_tools_may_be_adopted_under_gate`; `external_source_root_normalized_to_4_external_sources`; `external_source_inspection_requires_explicit_gate`; `external_tool_execution_requires_explicit_gate`; `runtime_activation_requires_explicit_gate`; `no_external_source_content_inspection`; `no_external_tool_execution`; `no_runtime_activation`; `no_git_mutation` |

## 2. Purpose

P9.0 opens the external integration foundation phase after P8.R.

P9.0 accepts that external MIT tools are not merely inspiration candidates. P9.0 establishes that AGENT PLATFORM should evaluate reuse, adoption, adaptation, wrapping, forking, or vendoring before rebuilding from scratch.

P9.0 does not inspect external source contents. P9.0 does not execute external tools. P9.0 does not modify external tools. P9.0 does not activate runtime. P9.0 does not modify `.graphifyignore`. P9.0 prepares P9.1-P9.6 and later P10-P14.

## 3. Current Posture

P8.R closed MVP-0 as local non-executing manual workflow readiness. P8.R did not establish runtime readiness, external runtime adoption readiness, product/Siamese readiness, provider/API/MCP readiness, or Git automation readiness.

Graphify remains read-only evidence candidate until future gate. Hermes remains interface/runtime candidate until future gate. GBrain remains memory architecture candidate until future gate. GStack remains skill-stack candidate with `4_external/sources/gstack-main` path/class metadata only until future gate. ECC-main is a new candidate for later evaluation and does not become agent OS by P9.0.

| Area | P9.0 posture | Blocked interpretation |
| --- | --- | --- |
| P8.R closure | Accepted closure with runtime/external adoption not established. | Runtime readiness. |
| External tools | Integrable under future gates. | Immediate adoption or execution. |
| Graphify | Future controlled evidence refresh candidate. | Graphify run, rerun, authority, or `.graphifyignore` change. |
| Hermes | Future real interface/runtime candidate. | Hermes source inspection or runtime. |
| GBrain | Future memory architecture candidate. | GBrain runtime or source inspection. |
| GStack | `4_external/sources/gstack-main` path/class metadata only. | Source inspection, execution, adoption, dependency approval. |
| ECC-main | Future agent OS candidate. | Agent OS activation or orchestration. |
| OpenCode | H0 user-operated harness. | AGENT PLATFORM execution. |
| Provider/API/MCP | Future integration class, blocked by default. | Auth, credentials, API calls, MCP activation. |
| Git | User-owned. | Agent Git mutation or `git add .`. |

## 4. Inputs Reviewed

Inputs were consumed through allowed posture, path, and marker checks only. No external source contents, product/Siamese source, raw generated outputs, secrets, credentials, provider configs, token stores, browser auth, local credential stores, API keys, scripts, tests, package managers, tools, agents, or runtimes were inspected or executed.

| Input | Review mode | P9.0 use | Limitation |
| --- | --- | --- | --- |
| `agent_platform_mvp0_implementation_plan_authorization_boundary.md` | path posture check | Confirms P8.11 authorization boundary context. | No implementation scope changed. |
| `agent_platform_p8_platform_mvp_scope_external_integration_boundary.md` | path posture check | Carries P8 external boundary. | No P8.0 modification. |
| `agent_platform_p8_security_activation_gate_model.md` | path posture check | Carries activation/security gate model. | No P8.5 modification. |
| `agent_platform_gbrain_gstack_memory_compatibility_boundary.md` | path posture check | Carries GBrain/GStack candidate boundary. | No source inspection. |
| `agent_platform_hermes_interface_runtime_candidate_boundary.md` | path posture check | Carries Hermes candidate boundary. | No Hermes runtime. |
| `agent_platform_opencode_harness_upgrade_boundary.md` | path posture check | Carries OpenCode H0/manual boundary. | No OpenCode execution. |
| S-03 / S-04 security policies | path posture check | Carries secret, credential, tool, shell, network, MCP blockers. | No enforcement activated. |
| README, `.gitignore`, `.graphifyignore` | path posture check | Confirms repository and boundary files exist. | Not modified. |
| `4_external/sources` and candidate paths | path metadata only | Confirms canonical external root and candidate path presence/absence. | No listing, traversal, or content inspection. |

## 5. Adopt-Not-Rebuild Principle

Conceptual inspiration is insufficient when a validated external tool can be safely reused.

Validated external tools should be reused when they fit the architecture and safety boundaries. MIT/license-compatible tools may be candidates for adoption, adaptation, wrapping, forking, vendoring, or dependency use after license and trust review.

Rebuilding from scratch is not the default. Scratch rebuild is allowed only after an explicit reuse rejection record. A reuse rejection record must identify why adoption, wrapping, forking, or vendor use is not suitable.

Architecture purity is not a sufficient reason by itself to reject a validated external tool. Security, dependency risk, runtime mismatch, authority mismatch, or maintenance risk may be sufficient reasons.

Policy shift:

```text
If an external MIT tool already solves a relevant problem, AGENT PLATFORM should first evaluate adoption/adaptation/wrapping before rebuilding from scratch.
```

Core decision:

```yaml
ExternalToolIntegrationCharter:
  phase: P9_external_integration_foundation
  default_strategy: adopt_adapt_wrap_before_rebuild
  rebuild_from_scratch: allowed_only_after_reuse_rejection_record
  external_tools_are_integrable: true_under_future_gate
  mit_tools_may_be_used_modified_or_wrapped: true_after_license_verification
  license_verification_ticket: P9.2
  source_inspection_ticket: P9.3
  execution_gate_ticket: P9.4
  adoption_mode_ticket: P9.5
  rollback_incident_ticket: P9.6
  closure_ticket: P9.R
  current_ticket_authority: charter_only
  source_inspection_authorized_by_P9_0: false
  execution_authorized_by_P9_0: false
  runtime_authorized_by_P9_0: false
  git_mutation_authorized_by_P9_0: false
```

Reimplementation from scratch requires a documented reason:

- license mismatch
- dependency risk
- security risk
- architecture mismatch
- runtime incompatibility
- maintenance risk
- excessive coupling
- unclear provenance
- unacceptable side effects
- user decision to rebuild despite available external tool

## 6. External Integration Level Model

P9.0 may authorize only `EXT-L0` path metadata checks and future planning. P9.0 does not authorize `EXT-L1` through `EXT-L7`.

| Level | Name | Meaning | P9.0 authorization |
| --- | --- | --- | --- |
| EXT-L0 | named_candidate_path_metadata | Tool is named and path may be checked. | Allowed by P9.0. |
| EXT-L1 | source_inspection_authorized | Source contents may be inspected under exact scope. | Not authorized by P9.0; delegated to P9.3. |
| EXT-L2 | license_dependency_audit | License/dependencies/entrypoints may be audited. | Planned by P9.0; delegated to P9.2/P9.3. |
| EXT-L3 | adoption_design | Adoption mode may be designed. | Planned by P9.0; delegated to P9.5 and tool-specific projects. |
| EXT-L4 | non_executing_adapter_or_wrapper | Local non-executing adapter/wrapper may be created. | Not authorized by P9.0. |
| EXT-L5 | controlled_local_execution | Tool may be executed under exact command/scope. | Not authorized by P9.0; delegated to P9.4 and tool-specific gates. |
| EXT-L6 | runtime_integration | Tool participates in AGENT PLATFORM runtime. | Not authorized by P9.0. |
| EXT-L7 | autonomous_or_always_on_integration | Tool participates in autonomous/always-on orchestration. | Blocked by default. |

## 7. Canonical External Source Root

Canonical external source root: `4_external/sources`.

Do not use `external/sources` as canonical.

Known path/class metadata carried forward:

```yaml
4_external/sources:
  posture: canonical_external_source_root
  content_inspection_by_P9_0: not_authorized

4_external/sources/gstack-main:
  posture: present_path_not_inspected
  candidate_classes:
    - external_source_candidate
    - gbrain_compatibility_candidate
    - skill_stack_candidate
    - bootstrap_layer_candidate
    - agent_workflow_support_candidate
  adoption_posture: not_adopted_by_P9_0
  execution_posture: not_executed_by_P9_0
  runtime_posture: not_runtime_by_P9_0
  source_inspection_posture: content_not_inspected_by_P9_0
```

Optional path checks completed as path metadata only: `4_external/sources`, `4_external/sources/gstack-main`, `4_external/sources/gbrain-master`, `4_external/sources/hermes`, `4_external/sources/Hermes`, `4_external/sources/ECC-main`, and `4_external/sources/ecc-main`.

P9.0 did not list, inspect, summarize, import, execute, configure, install, adopt, or traverse those paths.

## 8. Candidate Tool Tracks

| Tool | P9.0 posture | Future project | P9.0 allowed action | P9.0 blocked action |
| --- | --- | --- | --- | --- |
| Graphify | Evidence/repo graph candidate for controlled refresh. | P10 | Define future Markdown evidence integration track. | No `.graphifyignore` change, no Graphify run. |
| Hermes | Real interface/runtime candidate for possible adoption. | P11 | Define future source review and adoption track. | No Hermes source inspection or runtime. |
| GBrain | Memory architecture candidate for possible adoption. | P12 | Define future memory/source review track. | No memory runtime or source inspection. |
| GStack | Skill stack/bootstrap candidate. | P12 | Carry corrected path/class metadata. | No source inspection, execution, adoption, dependency approval. |
| ECC-main | Agent OS candidate, optional later evaluation. | P13 | Define future evaluation track. | No agent OS activation or orchestration. |
| OpenCode | H0 user-operated harness; possible future adapter. | Later gate | Preserve manual boundary. | No AGENT PLATFORM execution. |
| Provider/API/MCP | Candidate future integration class. | Later gate | Define blocked-by-default posture. | No auth, credentials, calls, MCP activation. |

## 9. Allowed / Blocked P9.0 Behavior

| Behavior | P9.0 posture |
| --- | --- |
| Name external candidates | Allowed. |
| Check exact candidate path existence | Allowed as `EXT-L0`. |
| Define adopt-not-rebuild policy | Allowed. |
| Define future P9/P10-P14 queue | Allowed. |
| Inspect external source contents | Blocked. |
| List external source trees | Blocked. |
| Execute external tools | Blocked. |
| Modify external tools or generated outputs | Blocked. |
| Activate runtime or autonomous orchestration | Blocked. |
| Mutate Git | Blocked. |

## 10. License / Trust Posture

P9.0 recognizes that validated external MIT tools may be used, modified, wrapped, forked, vendored, or integrated only after license verification and trust review.

P9.0 does not verify licenses, inspect dependency files, inspect source, install dependencies, or approve dependency use. License and trust intake is delegated to P9.2.

## 11. Source Inspection Posture

`external_source_inspection_requires_explicit_gate`.

P9.0 does not authorize external source content inspection. P9.0 does not inspect Graphify, Hermes, GBrain, GStack, ECC-main, Codegraph, OpenCode, provider/MCP, product/Siamese, generated output, secret, credential, or dataset/model contents.

Source inspection is delegated to P9.3 and later tool-specific gates.

## 12. Execution / Runtime Posture

`external_tool_execution_requires_explicit_gate`.

`runtime_activation_requires_explicit_gate`.

P9.0 does not authorize external tool execution, controlled local execution, runtime integration, autonomous orchestration, always-on integration, provider/API/MCP activation, OpenCode execution, Graphify execution/rerun, Hermes runtime, GBrain runtime, GStack execution, ECC-main execution, Codegraph execution, tests, validation, scripts, package managers, dependency installation, or Git mutation.

## 13. Adoption Mode Taxonomy

| Mode | Meaning | Allowed by P9.0? |
| --- | --- | --- |
| reference_only | Use as design/context reference only. | Yes. |
| path_metadata_only | Record path/class metadata only. | Yes. |
| source_review_candidate | Future exact source inspection. | Future P9.3 only. |
| wrap_existing_source | Use external source through local wrapper. | Future gate only. |
| fork_and_patch | Fork and modify external code. | Future gate only. |
| vendor_snapshot | Copy/vendor selected external code with license preservation. | Future gate only. |
| submodule_or_dependency | Use as submodule/dependency. | Future gate only. |
| direct_runtime_integration | Runtime integration. | Future runtime gate only. |
| reject_after_review | Reject with reason. | Future review result. |
| defer_after_review | Defer with reason. | Future review result. |

## 14. Scratch-Rebuild Rejection Rule

No AGENT PLATFORM component should be rebuilt from scratch when an external validated tool provides the needed capability unless a `ReuseRejectionRecord` exists.

```yaml
ReuseRejectionRecord:
  external_tool:
  capability_needed:
  evaluated_modes:
    - wrap_existing_source
    - fork_and_patch
    - vendor_snapshot
    - submodule_or_dependency
  rejection_reason:
  evidence_refs:
  security_refs:
  dependency_refs:
  maintenance_refs:
  user_decision:
  accepted_rebuild_scope:
  expiration_or_revisit_condition:
```

## 15. Tool-Specific Future Project Map

| Tool | First future ticket | Later project | P9.0 status |
| --- | --- | --- | --- |
| Graphify | P10.0 Graphify Integration Scope / Markdown Authorization | P10 | Future controlled evidence refresh; not started. |
| Hermes | P11.0 Hermes Source Review Authorization | P11 | Future real integration review; not started. |
| GBrain | P12.0 GBrain / GStack Source Review Authorization | P12 | Future memory architecture review; not started. |
| GStack | P12.0 GBrain / GStack Source Review Authorization | P12 | Future skill stack/bootstrap review; not started. |
| ECC-main | P13.0 ECC-main Source Review Authorization | P13 | Future agent OS evaluation; not started. |
| Integrated stack | P14.0 External Integration State Synthesis | P14 | Future synthesis; not started. |

Future project queue, defined but not started: P10 Graphify Markdown Evidence Integration, P11 Hermes Real Integration, P12 GBrain / GStack Memory + Skill Stack Integration, P13 ECC-main Agent OS Evaluation / Possible Integration, and P14 Integrated External Runtime Synthesis.

## 16. Security / Secrets / Credentials Boundary

P9.0 does not inspect secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, auth state, or provider/API/MCP settings.

Credential use, provider/auth/API/MCP activation, API calls, MCP activation, live connectors, dependency installation, and external tool execution remain blocked until explicit future gates.

## 17. Product / Siamese Boundary

Siamese is the living energy twin product vision, not product activation. P9.0 does not inspect product/Siamese source, does not authorize product/Siamese integration, and does not use external tools as a product source inspection path.

Product-bound external integration requires P4 / GT-09 or equivalent product readiness plus the relevant P9/P10+ gates.

## 18. Cognitive Semantic System Boundary

The Cognitive Semantic System substrate remains deferred. P9.0 does not select graph, vector search, Graphify, GBrain, GStack, ECC-main, Hermes, or any external tool as Cognitive Semantic System substrate.

Graph DB, vector DB, embeddings, semantic search, ontology runtime, and relationship persistence are not authorized by P9.0.

## 19. Git Boundary

P9.0 does not authorize Git mutation, staging, commit, push, force-add, publication, generated output tracking approval, or source tracking expansion approval.

Never recommend `git add .`.

## 20. P9 Ticket Queue

| Ticket | Name | Purpose | P9.0 posture |
| --- | --- | --- | --- |
| P9.1 | External Source Root Normalization | Normalize `4_external/sources` and legacy path drift. | Future ticket; not started. |
| P9.2 | External Source License / Trust Intake Model | Verify license, provenance, trust, dependency posture. | Future ticket; not started. |
| P9.3 | External Source Inspection Permission Gate | Authorize exact external source inspection scopes. | Future ticket; not started. |
| P9.4 | External Tool Execution Gate Model | Define when controlled execution may occur. | Future ticket; not started. |
| P9.5 | Vendor / Fork / Wrapper / Submodule Decision Model | Define adoption modes. | Future ticket; not started. |
| P9.6 | External Integration Rollback / Incident Protocol | Define rollback/incident handling for external integrations. | Future ticket; not started. |
| P9.R | External Integration Foundation Closure | Close P9 foundation and unlock P10+. | Future ticket; not started. |

## 21. Future Gate Requirements

| Gate | Purpose | First ticket |
| --- | --- | --- |
| source_root_normalization_gate | Normalize external path assumptions. | P9.1 |
| license_trust_gate | Verify license/provenance/dependency trust. | P9.2 |
| source_inspection_gate | Authorize exact source content inspection. | P9.3 |
| execution_gate | Authorize exact controlled execution. | P9.4 |
| adoption_mode_gate | Choose vendor/fork/wrapper/submodule/reject. | P9.5 |
| rollback_incident_gate | Define rollback/incident handling. | P9.6 |
| graphify_markdown_scope_gate | Modify `.graphifyignore` and run Graphify. | P10 |
| hermes_runtime_gate | Integrate Hermes beyond source review. | P11 |
| memory_skill_gate | Integrate GBrain/GStack memory/skills. | P12 |
| agent_os_gate | Evaluate ECC-main as agent OS candidate. | P13 |
| integrated_runtime_synthesis_gate | Decide MVP-1 stack. | P14 |

## 22. Drift / Limitation Register

| Drift ID | Source area | Issue | P9.0 posture | Status | Route |
| --- | --- | --- | --- | --- | --- |
| P9.0-DRIFT-CONCEPTUAL-ONLY-TOOLS | P8 external candidates | External tools were treated as candidate-only. | Corrected to adopt-under-gate. | resolved_in_charter | P9.2-P9.5 |
| P9.0-DRIFT-SCRATCH-BIAS | implementation strategy | Rebuilding from scratch may duplicate external tools. | Adopt-not-rebuild default. | resolved_in_charter | ReuseRejectionRecord |
| P9.0-DRIFT-GSTACK-PATH | external source root | Correct path is `4_external/sources/gstack-main`. | Path metadata only. | carried_forward | P9.1/P12 |
| P9.0-DRIFT-GRAPHIFY-MD-SCOPE | Graphify | Markdown evidence is not yet included/refreshed. | Future gate. | pending_P10 | P10 |
| P9.0-DRIFT-HERMES-REAL-INTEGRATION | Hermes | Hermes is not yet source-reviewed/integrated. | Future gate. | pending_P11 | P11 |
| P9.0-DRIFT-GBRAIN-GSTACK-REAL-INTEGRATION | GBrain/GStack | Memory/skill stack not integrated. | Future gate. | pending_P12 | P12 |
| P9.0-DRIFT-ECC-AGENT-OS | ECC-main | Agent OS candidate not evaluated. | Future gate. | pending_P13 | P13 |
| P9.0-DRIFT-RUNTIME-NOT-AUTHORIZED | runtime | P9.0 is charter only. | Runtime blocked. | blocked_until_future_gate | P14+ |

## 23. Stop Rules

STOP if P9.0 attempts external source content inspection, external source tree listing, Graphify execution, Graphify rerun, `.graphifyignore` modification, Hermes source inspection, Hermes runtime activation, GBrain source inspection, GBrain runtime activation, GStack source inspection, GStack execution, ECC-main source inspection, ECC-main execution, Codegraph execution, OpenCode execution, provider/auth/API/MCP activation, credential use, API calls, MCP activation, live connector activation, tool execution, agent execution, task execution, handoff execution, runtime activation, autonomous orchestration, automatic dispatch, automatic review, automatic integration, source loading, product/Siamese source inspection, secret inspection, `.env` inspection, test execution, Python execution, package-manager execution, dependency installation, validation execution, security enforcement activation, persistence/database/event stream, telemetry, vector DB, embeddings, graph DB, generated output tracking approval, source tracking expansion approval, publication, Git mutation, `git add .`, Cognitive Semantic System substrate selection, P9.1+ file creation, P10+ file creation, P4 file creation, or EXT.* file creation.

## 24. Created / Modified / Not Created Register

Created:

- `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`

Modified:

- none

Not created / not approved:

- no P9.1-P9.R files
- no P10-P14 files
- no P4 files
- no EXT.* files
- no code
- no adapters
- no wrappers
- no runtime files
- no source inspection
- no external source content inspection
- no external source tree listing
- no external source modification
- no `.graphifyignore` modification
- no `.gitignore` modification
- no Graphify execution
- no Hermes execution
- no GBrain runtime
- no GStack execution
- no ECC-main execution
- no OpenCode execution
- no provider/auth/API/MCP activation
- no credentials
- no API calls
- no MCP calls
- no tools
- no agents
- no tasks
- no handoffs
- no runtime activation
- no autonomous orchestration
- no persistence
- no vector DB
- no graph DB
- no telemetry
- no generated output tracking
- no source tracking expansion
- no product/Siamese source inspection
- no publication
- no Git mutation
- no git add .
- no Cognitive Semantic System substrate selection

## 25. Recommended Next Ticket

Recommended next ticket:

```text
P9.1 - External Source Root Normalization
```

After P9.1:

```text
P9.2 - External Source License / Trust Intake Model
P9.3 - External Source Inspection Permission Gate
P9.4 - External Tool Execution Gate Model
P9.5 - Vendor / Fork / Wrapper / Submodule Decision Model
P9.6 - External Integration Rollback / Incident Protocol
```

P10 must not start until P9.0 exists and the relevant P9 gates are accepted.

## 26. Final Verdict

| Question | Answer |
| --- | --- |
| What did P9.0 create? | `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`. |
| What policy did P9.0 establish? | Adopt, adapt, wrap, fork, vendor, or dependency-use validated external MIT tools under future gates before rebuilding. |
| Did P9.0 replace scratch-first behavior? | Yes. Rebuild-from-scratch now requires a `ReuseRejectionRecord`. |
| Did P9.0 authorize source inspection? | No. |
| Did P9.0 authorize external tool execution? | No. |
| Did P9.0 authorize runtime? | No. |
| Did P9.0 authorize Graphify rerun? | No. |
| Did P9.0 authorize Hermes integration? | No. |
| Did P9.0 authorize GBrain/GStack integration? | No. |
| Did P9.0 authorize ECC-main integration? | No. |
| Did P9.0 authorize provider/API/MCP? | No. |
| Did P9.0 authorize product/Siamese source inspection? | No. |
| Did P9.0 authorize Git mutation? | No. |
| What external root was normalized? | `4_external/sources`. |
| What GStack path was carried forward? | `4_external/sources/gstack-main`, path/class metadata only. |
| What adoption modes were defined? | `reference_only`, `path_metadata_only`, `source_review_candidate`, `wrap_existing_source`, `fork_and_patch`, `vendor_snapshot`, `submodule_or_dependency`, `direct_runtime_integration`, `reject_after_review`, `defer_after_review`. |
| What future gates are required? | P9.1 source root normalization, P9.2 license/trust, P9.3 source inspection, P9.4 execution, P9.5 adoption mode, P9.6 rollback/incident, then P10-P14 tool/project gates. |
| What is the next ticket? | P9.1 - External Source Root Normalization. |
