# P11.4 - Hermes Adoption Mode Decision

## 0. Contexto obligatorio

P11 is **Hermes Real Integration**. P11.4 selects the staged source relationship and runtime integration boundary through which the exact P11.0-locked Hermes candidate may be incorporated into AGENT PLATFORM after accepted P11.1, P11.2, and P11.3 evidence.

P11.4 consumes:

- P11.1 license, dependency, installation, runtime, state, network, and provider audit evidence;
- P11.2 architecture and component-classification evidence;
- P11.3 runtime, Cadence, Kanban, workspace, memory, shutdown, and authority decisions;
- the accepted P9.5 Vendor / Fork / Wrapper / Submodule Decision Model.

P11.4 does not inspect Hermes source directly, list or enumerate the Hermes source tree, install or execute Hermes, create adapters or forks, activate runtime, use credentials, configure providers, modify source, authorize redistribution/publication, or mutate Git. It does not start P11.5 or P11.6.

P10.R may remain concurrent and pending. Its absence does not block this static Hermes adoption decision because P11.1-P11.3 contain sufficient accepted Hermes evidence.

```text
p10r_concurrent_pending_not_blocking_p11_static_hermes_decision
```

Post-cleanup prerequisites are resolved by durable current canonical content, not legacy filename identity. Deleted historical Markdown is not restored or recreated.

P11.0 is complete and fixes this immutable candidate:

```text
repository: https://github.com/NousResearch/hermes-agent
release: 0.18.2
tag: v2026.7.7.2
commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
local source path: 4_external/sources/hermes-agent
working license assumption: MIT, superseded by P11.1's detailed license findings
```

Result marker:

```text
hermes_adoption_mode_decision_ready
```

## 1. Tipo

```text
architecture / governance decision
```

## 2. Objetivo

P11.4:

- selects an explicit staged Hermes adoption strategy across the independent source-relationship and runtime-integration dimensions;
- compares all credible P9.5 adoption modes and practical implementation shapes;
- justifies the selection from P11.1-P11.3 evidence rather than preference alone;
- preserves AGENT PLATFORM authority, policy, permissions, security, integration state, and unified observability;
- preserves Paperclip as the future canonical project/task/work control plane;
- preserves GBrain as the durable knowledge and hybrid retrieval plane;
- preserves Graphify as derived repository evidence and visualization;
- keeps Hermes replaceable, reversible, locally controlled, and upstream-compatible through a stable wrapper boundary;
- supports Hermes as the primary local runtime and UI foundation, including planned deep frontend and backend product customization in a future controlled fork;
- supports direct governed Hermes-GBrain communication through `KnowledgeMemoryPort` and, only if separately gated, an MCP transport adapter;
- prepares P11.5 adapter design and P11.6 local spike without starting either ticket.

## 3. Inputs And Prerequisite Resolution

`HermesAdoptionPostCleanupPrerequisiteResolution` applies the rule that current substantive canonical content is authoritative after accepted Markdown rationalization.

| Prerequisite | Expected current canonical path or content | Exact path found? | Substantive content found? | Status | Action |
| --- | --- | --- | --- | --- | --- |
| P11.0 source review authorization | `agent_platform_hermes_source_review_authorization.md` | Yes | Yes; exact repository/release/tag/SHA/path and no-execution boundary | Accepted | Consume immutable lock. |
| P11.1 audit | `agent_platform_hermes_license_dependency_runtime_audit.md` | Yes | Yes; audit-ready marker and complete footprint/risk findings | Accepted with retained blockers | Carry license, SBOM, lazy-install, state, network, and operations blockers. |
| P11.2 architecture mapping | `agent_platform_hermes_architecture_mapping.md` | Yes | Yes; mapping-ready and P11.3/P11.4 classification markers | Accepted | Consume component seams and wrap/adapt classifications. |
| P11.3 runtime/Cadence decision | `agent_platform_hermes_runtime_cadence_boundary_decision.md` | Yes | Yes; readiness marker and authority/Kanban/memory boundaries | Accepted | Bind selected mode to runtime ownership decision. |
| P9.5 adoption model | `agent_platform_external_tool_vendor_fork_wrapper_submodule_decision_model.md` | Yes | Yes; all canonical modes and P11.4 handoff present | Accepted | Use P9.5 comparison and decision rules. |
| P9 external integration charter | Current corrected `agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md` | Yes | Yes; adopt/adapt/wrap before rebuild under gates | Accepted | Do not require deleted legacy filename. |
| P9 source root normalization | `agent_platform_external_source_root_normalization.md` | Yes | Yes; `4_external/sources` canonical | Accepted | Preserve source isolation. |
| P9 license/trust intake | `agent_platform_external_source_license_trust_intake_model.md` | Yes | Yes; license/trust is not adoption permission | Accepted | Carry P11.1 exceptions. |
| P9 source inspection gate | `agent_platform_external_source_inspection_permission_gate.md` | Yes | Yes; exact-scope inspection distinct from execution | Accepted | P11.4 performs no source read. |
| P9 execution gate | `agent_platform_external_tool_execution_gate_model.md` | Yes | Yes; exact action, side effects, rollback, approval required | Accepted | No execution from this decision. |
| P9 rollback/incident protocol | `agent_platform_external_integration_rollback_incident_protocol.md` | Yes | Yes; STOP, containment, safe evidence, human escalation | Accepted | Require disable/remove/rollback path. |
| P10.R | Graphify closure content if present | No exact required P10.R path consumed | Current Graphify evidence-only posture is sufficient for this decision | Concurrent/pending, non-blocking | Do not inspect outputs or create P10.R. |
| Post-cleanup rule | Durable current content over deleted filename identity | Applicable | Yes | Accepted | No historical-document recreation. |
| `.opencode/` and `AGENTS.md` | No-touch unrelated local paths | Present as unrelated untracked paths in initial status | Not inspected as ticket inputs | Excluded | Do not modify, stage, delete, or include. |

Prerequisite conclusion:

```text
P11.0: accepted
P11.1: accepted for adoption decision, blockers retained
P11.2: accepted
P11.3: accepted
P9.5: accepted by substantive content
P11.4 decision eligibility: satisfied
```

## 4. HermesAdoptionEvidencePackage

`HermesAdoptionEvidencePackage` is the bounded evidence object supporting this decision. It contains references and findings, not source contents or runtime proof.

```yaml
HermesAdoptionEvidencePackage:
  source_lock_ref: P11.0/HERMES-VLOCK-001
  license_review_ref: P11.1/HERMES-LIC-001..002
  dependency_review_ref: P11.1/HERMES-DEP-001..003
  runtime_footprint_ref: P11.1/HERMES-RUN-001
  architecture_mapping_ref: P11.2/hermes_architecture_mapping_ready
  component_classification_ref: P11.2/hermes_adoption_classification_ready_for_P11.3_P11.4
  runtime_cadence_boundary_ref: P11.3/hermes_runtime_cadence_boundary_ready_for_P11_4
  kanban_boundary_ref: P11.3/hermes_kanban_provisional_control_plane
  memory_boundary_ref: P11.3/HERMES-CAD-013..015
  security_boundary_ref: S-03/S-04/P11.1/P11.3
  provider_api_mcp_boundary_ref: P3.4/P11.1/P11.3
  state_storage_boundary_ref: P11.1/HERMES-STATE-001
  rollback_requirement_ref: P9.6/P11.3/ShutdownRollbackPort
  human_approval_requirement_ref: P6.4/P11.3
  git_boundary_ref: P7.0.G/P11.0-P11.3
  limitations:
    - static evidence only
    - runtime behavior and shutdown not validated
    - full dependency SBOM/license clearance incomplete
    - restrictive PowerPoint skill license must be excluded or cleared
    - no implementation or execution authority
  license_constraints:
    - exclude or separately clear skills/productivity/powerpoint
    - preserve the Apache-2.0 license and NOTICE obligations for plugins/security-guidance
    - do not label the complete inherited tree as uniformly MIT
    - do not authorize redistribution or publication in P11.4
```

| Evidence item | Source document | Required before decision? | Present? | Blocker if missing |
| --- | --- | --- | --- | --- |
| Immutable source identity | P11.0 | Yes | Yes | Stop P11.4. |
| License and dependency posture | P11.1 | Yes | Yes | Stop mode selection. |
| Installation/runtime/state/network footprint | P11.1 | Yes | Yes | Stop executable-mode comparison. |
| Architecture and component seams | P11.2 | Yes | Yes | Stop wrapper/submodule/fork comparison. |
| Agent/tool/memory/provider/workspace mapping | P11.2 | Yes | Yes | Stop adapter-shape decision. |
| Kanban/Paperclip overlap | P11.2/P11.3 | Yes | Yes | Stop work-control decision. |
| Runtime/Cadence authority split | P11.3 | Yes | Yes | Stop runtime adoption decision. |
| Memory/GBrain split | P11.3 plus current clarification | Yes | Yes | Stop knowledge integration decision. |
| Security/execution boundaries | S-03/S-04/P11.1/P11.3 | Yes | Yes | No implementation-ready mode. |
| Rollback/incident posture | P9.6/P11.3 | Yes | Yes as requirements; unvalidated operationally | No execution. |
| Human approval requirement | P6.4/P11.3 | Yes | Yes | No implementation/execution. |

## 5. Candidate Adoption Modes

### `wrap_existing_source`

Definition: preserve the exact upstream source as an isolated external runtime and integrate it through stable AGENT PLATFORM adapters.

For Hermes Phase A, this means using the exact P11.0-pinned upstream checkout as an isolated, unmodified local runtime and localhost UI foundation behind ports rather than coupling platform consumers to Hermes internals. The wrapper remains the selected runtime integration shape in Phase B when the runtime source moves to the separately authorized controlled fork.

- Required evidence: source/dependency/runtime review, stable seams, authority boundary, adapter design, execution gate, rollback, human approval.
- Advantages: strongest replaceability, source isolation, upstream update compatibility, selective capability exposure, observable boundary, straightforward disable/bypass route.
- Risks: adapter complexity, process/service lifecycle, version drift, semantic mismatch, need to contain broad default capabilities.
- Current blockers: P11.1 license/SBOM findings, unvalidated runtime/shutdown, no P11.5 design, no P11.6 evidence, no P11.7 safety review, no P11.8 runtime gate.
- Rollback posture: disable adapter and local process/service, preserve or remove isolated state under policy, revert pinned source relationship without platform-source surgery.
- P11.5 effect: design stable runtime, memory, work-control, event, approval, workspace, version-compatibility, source-topology, and rollback contracts.
- P11.6 effect: permits a future separately gated local runtime and dashboard spike against the unmodified P11.0-pinned upstream source.
- Decision status: **selected Phase A setup mode and selected runtime integration shape for both phases**.

### `adopt_as_submodule`

Definition: make the upstream repository a Git submodule pinned to the reviewed commit.

- Meaning: source relationship and update workflow become repository-level Git structure.
- Advantages: explicit upstream provenance and pin, direct update comparison.
- Risks: submodule workflow burden, Git coupling, source-tracking expansion, contributor friction, conflicts with ignored external-source posture, no runtime isolation by itself.
- Blockers: no submodule/Git authorization; it does not solve authority, process, state, provider, or UI isolation.
- Rollback: remove/revert submodule and associated configuration through a separately approved Git change.
- P11.5 effect: adapter still required, so submodule adds workflow cost without replacing interface design.
- P11.6 effect: no material safety advantage over the existing pinned external checkout.
- Decision status: rejected for current incorporation.

### `adopt_as_vendor_code`

Definition: copy a reviewed Hermes snapshot into tracked AGENT PLATFORM source.

- Meaning: AGENT PLATFORM assumes source custody and update integration.
- Advantages: maximum local source control and direct customization.
- Risks: repository contamination, large dependency/runtime surface, notice/license obligations, update burden, merge burden, stronger coupling, harder rollback, accidental monolith formation.
- Blockers: restrictive bundled skill license, incomplete SBOM/license clearance, no source-tracking approval, no vendor ownership plan.
- Rollback: remove vendored tree and dependent code through a high-impact reviewed migration.
- P11.5 effect: encourages internal coupling contrary to stable-port requirement.
- P11.6 effect: broadens source and build scope unnecessarily.
- Decision status: rejected.

### `fork_and_patch`

Definition: maintain a controlled upstream-derived Hermes fork for the known AGENT PLATFORM requirement to deeply customize the Hermes frontend and backend while retaining the stable adapter boundary.

- Meaning: after an exact future creation gate, AGENT PLATFORM takes explicit patch, synchronization/rebase, security, provenance, compatibility, and rollback ownership for its productization source.
- Advantages: enables required deep frontend/backend product customization while preserving upstream provenance and preventing platform consumers from coupling to fork internals.
- Risks: divergence, maintenance and security burden, difficult upstream rebases, fork-specific state and compatibility.
- Blockers: P11.1 license disposition remains open; no exact source-workspace authorization, fork topology, synchronization/rebase policy, patch ownership model, version compatibility contract, or tested rollback exists.
- Rollback: revert product patches or return the stable adapter to a compatible pinned upstream runtime through a tested route without changing AGENT PLATFORM consumer contracts.
- P11.5 effect: must define the immutable-upstream/fork/workspace topology, upstream synchronization policy, version compatibility contract, patch ownership, license disposition, and rollback while keeping interfaces fork-neutral.
- P11.6 effect: may run the unmodified pinned upstream source first; it does not create a fork, patch source, or begin UI customization.
- Decision status: **selected Phase B productization source relationship, planned but not authorized for creation or modification**.

`fork_and_patch is the planned productization mode after the initial wrapped upstream spike, subject to license disposition, exact source workspace authorization, and P11.5 topology design.`

### `import_reference_only`

Definition: use Hermes solely as architecture/reference evidence.

- Meaning: no runtime incorporation.
- Advantages: lowest execution and supply-chain exposure.
- Risks: fails P11's validated goal of a real local runtime and UI foundation; loses useful agent-loop, session, tool, workspace, and UI capabilities.
- Blockers: not unsafe, but strategically insufficient given P11.2 stable seams and P11.3 accepted runtime role.
- Rollback: none needed beyond retaining documentation references.
- P11.5/P11.6 effect: would cancel adapter design and runtime spike.
- Decision status: rejected as insufficient.

### `defer_after_audit`

Definition: make no adoption-mode selection because evidence is insufficient or contradictory.

- Advantages: avoids premature commitment.
- Risks: stalls integration despite enough evidence to select a non-executing architecture mode.
- Blockers to selection: none. P11.1-P11.3 are sufficient for mode selection even though execution remains blocked.
- Rollback: revisit when missing evidence closes.
- P11.5/P11.6 effect: would block both.
- Decision status: rejected for mode selection; implementation and execution remain deferred through later gates.

### `reject_for_boundary_mismatch`

Definition: reject Hermes because its architecture cannot fit AGENT PLATFORM authority, safety, rollback, or replacement goals.

- Advantages: eliminates integration risk.
- Risks: discards a capable runtime whose risky surfaces can be isolated and selectively exposed.
- Blockers to selection: P11.2 found adapter seams; P11.3 established a viable authority split and migration boundaries. No unavoidable mismatch is proven.
- Rollback: close P11 integration.
- P11.5/P11.6 effect: neither proceeds.
- Decision status: rejected; reopen only if later evidence shows the wrapper boundary is infeasible.

## 6. Implementation-Shape Options

| Option | Mapped adoption mode | Evidence support | Risk | Maintenance burden | Isolation quality | Rollback quality | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| External CLI use | `wrap_existing_source` | Entrypoints exist, but structured lifecycle needs more than CLI text | Medium | Medium | Medium/high by process | High | Deferred as possible internal transport, not primary contract. |
| Python package use | `wrap_existing_source` | Agent facade and package seams exist | High in-process coupling/import side effects | Medium/high | Low/medium | Medium | Rejected as primary boundary; P11.5 may evaluate only behind adapter. |
| Separate localhost service/process | `wrap_existing_source` | Dashboard/gateway/runtime surfaces and process boundaries exist | Service/port/state risk | Medium | High if loopback and isolated | High | Selected practical runtime direction, subject to later gates. |
| Adapter over Hermes local source/runtime | `wrap_existing_source` | Strongly supported by P11.2/P11.3 ports and classifications | Adapter complexity | Medium | High | High | **Selected incorporation shape.** |
| Submodule with pinned commit | `adopt_as_submodule` | Reproducible source pin possible | Git/workflow coupling | Medium/high | Medium | Medium | Rejected. |
| Vendored code snapshot | `adopt_as_vendor_code` | Technically possible | License/repo/update burden | High | Low | Low/medium | Rejected. |
| Controlled fork behind the same adapter | `fork_and_patch` | Required future route for known deep frontend/backend product customization | Divergence/security/license burden | High | High at adapter boundary | Medium/high with tested upstream fallback | **Selected future productization source relationship after exact creation gate.** |
| Component extraction | `adopt_as_vendor_code` or bespoke reuse | Components mapped, but extraction copies internals | Hidden coupling/license/update drift | High | Medium | Low/medium | Rejected unless a future evidence-backed component decision supersedes. |
| Compatible interface reimplementation | No direct P9.5 adoption; compatibility rebuild | Interfaces can be designed independently | Rebuild cost and semantic drift | Very high | High | High | Rejected while wrapping remains viable. |
| Reference-only use | `import_reference_only` | Fully supported as fallback | Does not deliver runtime/UI objective | Low | Maximum | Maximum | Rejected as primary outcome. |

Selected staged practical shape:

```text
Phase A - setup and controlled validation
  immutable read-only P11.0-pinned upstream reference
    -> AGENT PLATFORM stable adapter
    -> isolated unmodified local Hermes runtime process/service
    -> localhost-only Hermes UI/dashboard spike under exact P11.6 controls

Phase B - AGENT PLATFORM productization
  immutable read-only upstream reference
    -> separately authorized controlled fork with provenance and synchronization policy
    -> AGENT PLATFORM frontend/backend customization in controlled integration source
    -> same AGENT PLATFORM stable adapter ports; no consumer coupling to fork internals

Both phases
  -> governed KnowledgeMemoryPort to GBrain
  -> governed WorkControlPlanePort to future Paperclip
```

This diagram is architecture direction only. No process, service, dashboard, port, fork, source workspace, source modification, GBrain link, or Paperclip link is created or activated by P11.4. The locked external checkout remains an immutable read-only upstream reference.

## 7. HermesAdoptionModeComparisonMatrix

| Candidate mode | Upstream updates | Customization | Rollback | Isolation | Observability/testability | Portability | Coupling risk | License/dependency risk | Security risk | Polish-future fit | Paperclip/GBrain/Graphify fit | Authority preservation | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `wrap_existing_source` | High through pinned source upgrades | Bounded in Phase A; adapter composition remains flexible | High | High | High at stable boundary | High | Low/medium | Contained but unresolved | Containable through process/ports | Establishes safe initial spike and durable wrapper | Strong through ports; Graphify unchanged | Strong | **Selected Phase A setup and cross-phase runtime boundary** |
| `adopt_as_submodule` | High | Medium | Medium | Medium | Medium | Medium | Medium/high Git coupling | Unchanged | Unchanged | Medium | Neutral | Medium | Rejected |
| `adopt_as_vendor_code` | Low/medium, manual merges | High | Low/medium | Low | Medium | Low | High | High, imported into repo | High | High initially, costly later | Weak due coupling | Weak | Rejected |
| `fork_and_patch` | Medium with required synchronization/rebase policy | Very high | Medium/high through stable-adapter fallback | High at adapter boundary | High at stable boundary | Medium/high | High inside controlled source; low for consumers | High ownership burden; license disposition required | Medium/high | Required for deep product customization | Strong if all integrations remain port-bound | Strong at adapter boundary | **Selected Phase B productization source relationship; creation not authorized** |
| `import_reference_only` | N/A | None | High | Maximum | N/A | N/A | None | Low | Low | None | Does not enable integrations | Strong but insufficient | Rejected |
| `defer_after_audit` | N/A | None | High | N/A | N/A | N/A | None | Risks remain open | Low now | None | Delays all | Preserves but stalls | Rejected as decision |
| `reject_for_boundary_mismatch` | N/A | None | High | N/A | N/A | N/A | None | Avoided | Avoided | None | No integration | Preserves by exclusion | Rejected; mismatch not proven |

Selection rationale:

Source relationship and runtime integration are independent dimensions. `wrap_existing_source` is selected for Phase A because it combines source isolation, the exact upstream pin, stable observability/test seams, and straightforward shutdown/rollback for controlled validation. A stable AGENT PLATFORM adapter over an isolated local Hermes process/service is selected as the runtime integration shape for both phases.

`controlled_fork_with_stable_adapter` is selected as the planned Phase B source relationship because Hermes is the primary runtime and UI foundation and deep AGENT PLATFORM frontend/backend customization is a known product requirement. The controlled fork does not replace the wrapper: product customization occurs inside the governed fork while every AGENT PLATFORM consumer continues to use the same stable adapter ports. Fork creation remains blocked until license disposition, exact source-workspace authorization, and P11.5 topology design are accepted.

## 8. HermesSelectedAdoptionMode

`HermesAdoptionModeDecision` is the governance record that selects a staged P9.5-compatible source strategy and a stable cross-phase runtime integration shape for the locked Hermes candidate. It is not an implementation, source relationship change, installation, fork creation, source modification, or runtime action.

```yaml
HermesSelectedAdoptionMode:
  setup_mode: wrap_existing_source
  runtime_integration_shape: stable AGENT PLATFORM adapter over an isolated local Hermes process/service
  productization_source_mode: controlled_fork_with_stable_adapter
  upstream_reference: 4_external/sources/hermes-agent
  upstream_reference_posture: immutable read-only reference
  fork_creation_authorized: false
  source_modification_authorized: false
  fork_topology_owner: P11.5
  first_runtime_spike_source: exact P11.0-pinned upstream source
  final_ui_customization_source: future controlled fork
  gbrain_integration: direct governed KnowledgeMemoryPort
  paperclip_integration: future WorkControlPlanePort
  graphify_posture: evidence and visualization only
  selected_execution_posture: blocked until P11.5 design, P11.6 exact spike gate, P11.7 safety review, and P11.8 controlled runtime gate
  selected_state_posture: dedicated inventory-tracked runtime state; no canonical platform/task/knowledge authority
  selected_provider_posture: provider-independent adapter; provider/auth/API/OAuth/MCP blocked pending exact future gate
  selected_memory_posture: direct governed KnowledgeMemoryPort integration with GBrain; optional MCP transport only after separate gate; no DB fusion
  selected_kanban_posture: provisional MVP compatibility behind WorkControlPlanePort; never canonical task authority
  selected_paperclip_posture: future canonical project/task/work control plane with mandatory migration and no dual writable authority
  selected_gbrain_posture: canonical durable facts, decisions, documents, entities, provenance, and hybrid retrieval
  selected_graphify_posture: derived repository evidence and visualization only
  required_next_tickets:
    - P11.5 Hermes Interface Adapter Design
    - P11.6 Hermes Local Runtime and Dashboard Spike, separately authorized
    - P11.7 Hermes Adapter Safety / Rollback Review
    - P11.8 Hermes Controlled Runtime Gate
  human_approval_required_before_execution: true
  implementation_not_authorized_by_p11_4: true
```

P11.4 selects the staged strategy but does not authorize implementation, execution, fork creation, source modification, redistribution, or publication. UI customization begins only in the future controlled integration source after its exact creation gate.

```text
no installation
no execution
no Git mutation
```

## 9. Rejected / Deferred Modes

| HermesRejectedAdoptionMode | Reason rejected/deferred | Evidence reference | Reopen condition | Risk if used anyway |
| --- | --- | --- | --- | --- |
| `adopt_as_submodule` | Adds Git/workflow coupling without solving runtime isolation or authority boundaries. | P9.5, P11.1, P11.2 | Reopen only if upstream-tracking workflow becomes essential and separately approved. | Submodule complexity and false sense of isolation. |
| `adopt_as_vendor_code` | Imports a large, mixed-license, high-dependency runtime into platform source. | P11.1 license/dependency findings | Reopen only after full clearance and evidence that wrapping cannot meet needs. | Repo contamination, stale fork-like burden, harder rollback. |
| `import_reference_only` | Cannot deliver the accepted primary runtime/UI goal. | P11.2/P11.3 | Reopen if runtime adoption is later rejected. | Strategic under-delivery. |
| `defer_after_audit` | Evidence is sufficient to choose a non-executing mode. | P11.1-P11.3 readiness markers | Reopen if prerequisite evidence is invalidated. | Unnecessary delay and repeated decision work. |
| `reject_for_boundary_mismatch` | Adapter isolation and authority separation are viable; mismatch is not proven. | P11.2/P11.3 | Reopen if P11.5/P11.6 proves isolation, rollback, or replacement infeasible. | Discards useful runtime/UI foundation. |

`fork_and_patch is the planned productization mode after the initial wrapped upstream spike, subject to license disposition, exact source workspace authorization, and P11.5 topology design.` It is a selected future source relationship, not permission from P11.4 to create a fork, patch or modify source, redistribute inherited content, or publish a derived tree.

## 10. Runtime Authority Boundary

| Authority surface | Owner | Hermes role | P11.4 implication | Future gate |
| --- | --- | --- | --- | --- |
| Ontology/taxonomy | AGENT PLATFORM | Consume projected profiles only | Adapter must not expose Hermes taxonomy as canonical. | Governance change if needed |
| Policy/permissions/security | AGENT PLATFORM | Enforce supplied decisions at runtime | Wrapper is subordinate to platform policy. | P11.5/P11.7/P11.8 |
| Worker/session execution | Hermes behind adapter | Primary local runtime mechanics | Selected runtime role, inactive now. | P11.6-P11.8 |
| Tool/shell authority | AGENT PLATFORM/human | Execute only exact approved invocation | No wholesale toolsets. | Exact tool gate |
| Project/task/work state | Paperclip future plane | Provisional execution projection only | `WorkControlPlanePort` mandatory. | Paperclip integration gate |
| Budget/approval state | AGENT PLATFORM/human; Paperclip future workflow | Runtime evidence only | Hermes counters/statuses are not authority. | Approval/work-control gate |
| Durable knowledge | GBrain | Governed read and write-candidate client | `KnowledgeMemoryPort` is core, not an undesired dependency. | GBrain integration gate |
| Session/procedural context | Hermes under platform policy | Runtime-local memory mechanics | Allowed later only with retention/write controls. | P11.5/P11.7/P11.8 |
| Repository evidence | Graphify | No runtime authority | Evidence/visualization only. | Separate Graphify governance |
| Integration state/observability | AGENT PLATFORM | Emit normalized events | No direct log/DB authority. | `RuntimeEventPort` design/gate |

Hermes must not own canonical project, task, budget, approval, agent taxonomy, or durable world knowledge authority. Hermes must not become AGENT PLATFORM replacement or a mandatory monolith.

## 11. Kanban Adoption Boundary

P11.4 adopts P11.3's posture:

```text
provisional MVP compatibility
```

Hermes Kanban remains inactive and non-canonical.

- Adapter isolation: all use must pass through `WorkControlPlanePort`; no platform consumer may bind directly to Hermes Kanban schema.
- Migration: task IDs, states, dependencies, assignments, heartbeats, events, attempts, approvals, failures, audit, rollback, and archive must map to Paperclip.
- State ownership: Hermes owns only temporary runtime projection/attempt mechanics; Paperclip will own canonical work state.
- Allowed future test scope: single local board/queue, bounded approved work projection, no auto-decompose, no external messaging, no canonical approvals or budgets.
- Stop rules: stop on dual writable authority, unmapped state, autonomous task creation, unbounded dispatcher/retry/reclaim, unexpected persistence, provider exposure, product access, or failed shutdown/cleanup.

Hermes Kanban task state must not permanently compete with Paperclip task state.

## 12. Memory Adoption Boundary

Direct governed Hermes-GBrain communication is a core AGENT PLATFORM capability, not an undesired dependency.

| Memory surface | Hermes role | GBrain role | Selected adoption implication | Future gate |
| --- | --- | --- | --- | --- |
| Session/collaboration context | Runtime owner | None | Hermes retains bounded session context. | P11.5/P11.7/P11.8 |
| Preferences/procedural learning | Candidate runtime owner under policy | May receive reviewed durable promotions | No autonomous persistence or promotion. | Memory write policy gate |
| Scoped durable retrieval | Client through `KnowledgeMemoryPort` | Canonical cited retrieval owner | Hermes may retrieve scoped, cited knowledge. | GBrain/adapter/runtime gate |
| Durable write | Submit `MemoryWriteCandidate` only | Validate provenance, permission, review, retention, rollback, then decide | No direct or uncited write. | Human/memory authority gate |
| Facts/decisions/documents/entities | No authority | Canonical owner | Never stored as Hermes authority. | GBrain governance |
| Hybrid retrieval | Consumer | Canonical owner | Adapter must preserve citations and scope. | GBrain integration gate |
| Physical database | No fusion | Independent store | No raw DB coupling or shared tables. | New explicit architecture decision |
| Dream/maintenance | Blocked | Blocked unless separately governed | No automatic memory maintenance. | Exact Cadence/memory gate |

MCP may be used only as a future transport adapter if separately approved. `KnowledgeMemoryPort` is the canonical semantic contract; transport choice must not leak MCP or GBrain internals into Hermes runtime contracts.

## 13. Provider / API / MCP Boundary

| Surface | P11.4 status | Future gate | Stop rule |
| --- | --- | --- | --- |
| Provider/model routing | Inactive; provider-independent interface direction only | P3.4/P11.7/P11.8 exact route approval | Stop before any model/provider call. |
| API/network | Inactive | Exact endpoint/data/auth/retention/cost gate | Stop before network access. |
| OAuth/authentication | Inactive | Secure human-approved auth gate | Stop before token/login/browser auth. |
| MCP | Inactive; optional future GBrain transport only | Exact server/tools/resources/data/transport gate | Stop before start/connect/list/invoke. |
| Credentials/config/token stores | Prohibited from P11.4 | Secure future credential boundary | Stop without inspecting. |

P11.4 does not approve provider routing, APIs, OAuth, MCP, credentials, or model execution.

## 14. Security And Rollback Boundary

`HermesAdoptionLicenseBoundary`:

| Surface | Required posture |
| --- | --- |
| `skills/productivity/powerpoint` | Exclude from the controlled productization source or separately clear its restrictive license before inclusion or redistribution. |
| `plugins/security-guidance` | Preserve the Apache-2.0 license and all applicable NOTICE obligations. |
| Complete inherited tree | Do not label the tree as uniformly MIT; retain file/subtree-specific license findings and provenance. |
| Redistribution/publication | Not authorized by P11.4; requires separate license disposition and exact approval. |

`HermesAdoptionSecurityBoundary`:

| Surface | Required boundary for later tickets |
| --- | --- |
| Command execution | Exact command/action, cwd, input/output, timeout, side effects, approval, audit, rollback. |
| Dangerous/destructive commands | Deny by default; no implicit escalation. |
| Sudo/global install | Prohibited unless a future explicit exceptional gate exists. |
| Filesystem writes | Dedicated state/workspace roots and write inventory; no broad host access. |
| Workspace isolation | Temporary exact-scope workspace with mount/source restrictions and cleanup. |
| Network listeners | None by default; exact listener inventory and shutdown required. |
| Public ports | Prohibited. Future dashboard candidate is loopback only. |
| Credentials/OAuth/provider config | Excluded from logs, context, workspaces, tools, and adapter payloads unless separately approved. |
| Plugins/skills | Disabled by default; explicit allowlist and lifecycle review required. |
| Browser/computer use | Disabled; separate exact gate required. |
| SQLite/state stores | Dedicated, inventoried, versioned, retention-limited, migratable, and non-authoritative. |
| Observability | Normalized redacted events through platform boundary; no external telemetry by default. |

`HermesAdoptionRollbackBoundary`:

| Surface | Required rollback posture |
| --- | --- |
| Runtime | Adapter-level disable/bypass and deterministic process termination. |
| Dashboard/service | Loopback-only if later approved; close listener and invalidate session state. |
| Installation | Isolated uninstall/removal without platform-source edits. |
| Workspace | Inventory, clean, or quarantine all residuals. |
| State | Export required canonical projections, invalidate checkpoints, remove/archive provisional stores under policy. |
| Kanban | Freeze writes, migrate/rollback, disable route; never retain dual authority. |
| GBrain link | Disable transport without corrupting either memory layer; preserve pending write candidates safely. |
| Provider link | Revoke/disable exact route and credentials if a later ticket ever enables them. |
| Kill switch | AGENT PLATFORM-controlled and independent of Hermes internal task state. |
| Incident | STOP, safe metadata only, containment, human/security/governance route, no automatic destructive remediation. |

P11.4 defines requirements for P11.5/P11.6/P11.7. It implements none of them.

## 15. P11.5 Implications

P11.5 must design the selected stable wrapper boundary and the Phase B controlled-fork/workspace topology. Minimum ports:

```text
AgentRuntimePort
KnowledgeMemoryPort
WorkControlPlanePort
```

P11.5 should also preserve the P11.3 event, approval, workspace, and shutdown boundaries.

Required design properties:

- fork/workspace topology that physically and operationally separates the immutable read-only P11.0 upstream reference from the future controlled integration source;
- upstream synchronization/rebase policy with provenance retention, review cadence, conflict handling, and security-update intake;
- version compatibility contract between the stable adapter and both the P11.0-pinned upstream source and authorized controlled-fork versions;
- patch ownership, review, testing, documentation, and retirement responsibilities for frontend and backend customization;
- rollback from the controlled fork to a compatible pinned upstream runtime or prior approved fork version without changing consumer contracts;
- license disposition that excludes or separately clears `skills/productivity/powerpoint`, preserves Apache-2.0 license and NOTICE obligations for `plugins/security-guidance`, and never represents the inherited tree as uniformly MIT;
- idempotent start/submit/cancel/shutdown operations;
- correlation IDs across session, work packet, attempt, tool call, memory request, and runtime event;
- explicit finite timeouts and cancellation semantics;
- bounded retry semantics with retryability classification;
- structured errors and `FailureEnvelope` mapping;
- normalized audit/runtime events without raw sensitive payloads;
- provider and model independence;
- exact workspace isolation and state-location inventory;
- rollback, bypass, kill, and cleanup hooks;
- version/capability negotiation for upstream updates and controlled-fork revisions;
- no direct Paperclip schema coupling or competing task state;
- direct governed GBrain reads and `MemoryWriteCandidate` proposals through `KnowledgeMemoryPort`;
- no GBrain/Hermes physical DB merge or raw DB coupling;
- no Graphify authority dependency;
- UI/dashboard isolation so the deeply customized frontend/backend remains replaceable behind the stable adapter rather than becoming a direct consumer dependency.

P11.5 must not create the fork, modify source, implement the adapter, redistribute inherited content, or publish a derived tree unless each action is separately authorized by exact scope.

## 16. P11.6 Implications

The practical objective is `P11.6 - Hermes Local Runtime and Dashboard Spike`. The selected Phase A mode makes that spike conceptually eligible against the exact unmodified P11.0-pinned upstream source, but P11.6 remains separate, inactive, and subject to its own exact execution and listener controls.

P11.6 may authorize only under exact controls:

- an isolated local Hermes environment;
- a dedicated temporary `HERMES_HOME`;
- the minimum Hermes backend required by the UI;
- the Hermes dashboard bound only to `127.0.0.1`;
- one exact local port;
- a complete frontend/backend process inventory;
- no public listener;
- no external channels;
- no cron or persistent Cadence;
- no autonomous dispatcher;
- no browser automation or computer use;
- no MCP;
- no GBrain or Paperclip integration yet;
- no provider call unless separately required and exactly authorized;
- deterministic shutdown of every frontend/backend process and listener;
- residual-state inventory covering the temporary home, workspace, logs, caches, state stores, and process artifacts.

P11.6 remains blocked from production/hosted deployment, product-source access, credentials unless separately required by an exact approved provider route, source modification, fork creation, patching, vendoring, submodules, UI customization, or Git mutation. UI customization begins only in the controlled integration source after its exact future creation gate.

P11.4's localhost dashboard direction is design intent, not listener authorization. P11.6 must stop unless its own exact ticket reconciles P11.3's dashboard restriction and defines `127.0.0.1`, the exact port, auth/session posture, frontend/backend process inventory, temporary `HERMES_HOME`, deterministic shutdown, residual cleanup, and incident behavior.

## 17. Human Approval Requirement

```yaml
HermesAdoptionHumanApprovalRequirement:
  selected_strategy_requires_human_review: true
  approval_scope: exact future P11.5 design acceptance and separately exact P11.6/P11.8 execution gates
  p11_4_authorizes_execution: false
  p11_4_authorizes_installation: false
  p11_4_authorizes_provider_api_mcp: false
  p11_4_authorizes_source_modification: false
  p11_4_authorizes_fork_creation: false
  p11_4_authorizes_redistribution: false
  p11_4_authorizes_publication: false
  p11_4_authorizes_git_mutation: false
  approval_ref_is_approval: false
  security_and_validation_are_supporting_inputs_not_final_authority: true
```

Human review is required before any execution-related adapter, install, runtime, dashboard, provider, GBrain transport, Paperclip transport, Kanban, tool, shell, or state action.

## 18. Acceptance Criteria

| Criterion | Status |
| --- | --- |
| Target document created | Met |
| Post-cleanup prerequisite resolution documented | Met |
| P11.0 lock recorded | Met |
| P11.1/P11.2/P11.3 consumed | Met |
| P9.5 model consumed | Met |
| All candidate modes evaluated | Met |
| Practical implementation shapes evaluated | Met |
| Staged source relationship and runtime integration shape declared | Met: Phase A `wrap_existing_source`; stable adapter across phases; Phase B `controlled_fork_with_stable_adapter` |
| Every non-selected mode has rationale/reopen condition | Met |
| Runtime authority boundary preserved | Met |
| Kanban, memory, provider/API/MCP boundaries explicit | Met |
| Security/rollback boundaries explicit | Met |
| P11.5/P11.6 implications defined | Met |
| Human approval explicit | Met |
| No direct Hermes source inspection/list/enumeration | Met |
| No install/execution/runtime/adapters/source modification | Met |
| No product or credential access | Met |
| No Git mutation or extra Markdown | Met |

## 19. Validation Required

No tests, scripts, builds, package managers, CI, Hermes commands, source inspection, or runtime validation are permitted.

P11.4 validation is limited to the explicitly allowed `git status --short`, exact `Test-Path`, and exact `Select-String` posture/marker checks. Read-only Git history is needed only when substantive post-cleanup resolution cannot be established from surviving canonical content; it was not required for the present P11/P9.5 paths.

## 20. Decision Summary

### Summary

P11.4 selects a staged strategy: Phase A uses `wrap_existing_source` for an isolated local runtime/dashboard spike against the exact unmodified P11.0-pinned source; Phase B uses `controlled_fork_with_stable_adapter` for deep frontend/backend productization. The stable AGENT PLATFORM adapter remains the runtime integration shape across both phases.

### Files Inspected

Governance documents only: P11.0-P11.3, P9.5, current P9 charter/foundation records, and required marker-bearing canonical records. No Hermes or other external/product source was inspected.

### Files Created

`0_architecture/governance/agent_platform_hermes_adoption_mode_decision.md`

### Files Modified

The P11.4 document was revised in place before commit. No other file was modified.

### Tests/Commands Run

Only allowed initial `git status --short`, exact `Test-Path`, exact `Select-String` prerequisite/marker checks, and a read-only Graphify query over governance evidence. No tests or Hermes runtime commands.

### Post-Cleanup Prerequisite Resolution

All P11 and P9.5 exact current canonical paths were present. The current corrected P9.0 charter path was used; no legacy filename was required. P10.R remains concurrent/pending and non-blocking.

### Selected Adoption Mode

Phase A setup: `wrap_existing_source`

Cross-phase runtime integration shape: stable AGENT PLATFORM adapter over an isolated local Hermes process/service

Phase B productization source relationship: `controlled_fork_with_stable_adapter`

### Rejected / Deferred Modes

Rejected: `adopt_as_submodule`, `adopt_as_vendor_code`, `import_reference_only`, `defer_after_audit`, `reject_for_boundary_mismatch`. Planned after the wrapped upstream spike but not authorized by P11.4: `fork_and_patch` through `controlled_fork_with_stable_adapter`.

### Limitations

Static evidence only; no runtime proof, complete SBOM/license disposition, shutdown proof, adapter/fork topology design, spike evidence, source-workspace authorization, safety review, or controlled runtime authorization exists. Redistribution and publication remain unauthorized.

### Recommended Next Ticket

`P11.5 - Hermes Interface Adapter Design`

## 21. Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_hermes_adoption_mode_decision.md
```

Modified:

```text
0_architecture/governance/agent_platform_hermes_adoption_mode_decision.md
  revised in place before commit
no other files
```

Not created, inspected, executed, activated, or approved:

```text
no P11.5-P11.R, P12-P15, Paperclip, P4, EXT.*, retry, safe-block,
   marker-alignment, naming-drift, or diagnostic Markdown
no Hermes source inspection, source-tree listing, or enumeration by P11.4
no Hermes installation, execution, runtime, shell, dashboard, Kanban, proxy,
   service, skill/plugin, computer-use, browser, provider/model, or memory activation
no Cadence, cron, scheduler, persistent service, daemon, public port,
   shell-profile modification, workspace, state DB, or lifecycle script
no provider/API/OAuth/MCP activation or credential/API-key/token/.env access
no product/Siamese or GBrain/GStack/Paperclip/ECC/OpenCode/Graphify source inspection
no adapter, runtime code, test code, vendor, fork, patch, wrapper implementation,
   submodule, symlink, directory move, or rename
no persistence, vector DB, graph DB, embeddings, telemetry, or event streaming
no .opencode/, AGENTS.md, .gitignore, or .graphifyignore modification
no generated-output tracking, source-tracking expansion, publication, or Git mutation
```

Never use `git add .`.

## 22. Recommended Next Ticket

Valid future queue after explicit instruction:

- P11.5 - Hermes Interface Adapter Design
- P11.6 - Hermes Local Runtime and Dashboard Spike

Recommended actual next ticket:

```text
P11.5 - Hermes Interface Adapter Design
```

P11.4 does not start P11.5, P11.6, P11.7, P11.8, P11.R, P12, P13, P14, or P15.

## 23. Final Verdict

| Question | Answer |
| --- | --- |
| What did P11.4 create? | This single canonical Hermes adoption-mode governance decision. |
| Which source lock was used? | NousResearch `hermes-agent` 0.18.2, tag `v2026.7.7.2`, commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`, path `4_external/sources/hermes-agent`. |
| Were P11.1, P11.2, and P11.3 present and accepted by substantive content? | Yes. |
| Was P9.5 present by substantive content? | Yes. |
| Was cleanup resolution needed? | The corrected current P9.0 filename was used; no deleted prerequisite was recreated. P10.R remains non-blocking. |
| What modes were evaluated? | All seven canonical P11.4 modes. |
| What implementation shapes were evaluated? | CLI, package, service, adapter, submodule, vendor, fork, extraction, reimplementation, and reference-only. |
| What mode was selected? | Phase A `wrap_existing_source`; Phase B `controlled_fork_with_stable_adapter`. |
| What is the runtime integration shape? | The same stable AGENT PLATFORM adapter over an isolated local Hermes process/service across both phases. |
| What is the source relationship? | The P11.0 checkout remains an immutable read-only upstream reference; a future controlled fork is the planned productization source after its exact creation gate. |
| Why? | Wrapping preserves isolation, validation safety, observability, rollback, and consumer stability; the controlled fork enables the known deep frontend/backend customization requirement without exposing fork internals to consumers. |
| Which modes were rejected? | Submodule, vendor, reference-only, defer, and boundary rejection. |
| Which planned mode remains unauthorized? | `fork_and_patch` through `controlled_fork_with_stable_adapter`; it is planned for productization but blocked on license disposition, source-workspace authorization, and P11.5 topology design. |
| What does P11.5 inherit? | Stable ports plus fork/workspace topology, upstream synchronization, version compatibility, patch ownership, mixed-license disposition, and rollback design. |
| What does P11.6 inherit? | A separately gated local runtime/dashboard spike against unmodified pinned upstream source with temporary `HERMES_HOME`, loopback-only exact port, process inventory, no external integrations, deterministic shutdown, and residual-state inventory. |
| Did P11.4 inspect/list/enumerate Hermes source? | No. |
| Did P11.4 install, execute, or activate Hermes? | No. |
| Did P11.4 use credentials or activate provider/API/MCP? | No. |
| Did P11.4 inspect product/Siamese source? | No. |
| Did P11.4 create adapters or modify source? | No. |
| Did P11.4 modify `.opencode/` or `AGENTS.md`? | No. |
| Did P11.4 mutate Git? | No. |
| What is next? | P11.5 Hermes Interface Adapter Design, not started here. |

```text
hermes_adoption_mode_decision_ready
```

## Commit Commands

If the human accepts this decision, the human may run:

```powershell
git status --short

git add 0_architecture/governance/agent_platform_hermes_adoption_mode_decision.md

git commit -m "P11.4 - Hermes Adoption Mode Decision"

git push origin main
```

Never use `git add .`.
