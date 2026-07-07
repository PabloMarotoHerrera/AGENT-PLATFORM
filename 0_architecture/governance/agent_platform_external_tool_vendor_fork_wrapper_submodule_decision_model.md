# Vendor / Fork / Wrapper / Submodule Decision Model

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Vendor / Fork / Wrapper / Submodule Decision Model |
| Ticket | P9.5 |
| Status | Accepted Vendor / Fork / Wrapper / Submodule Decision Model |
| Date | 2026-07-07 |
| Scope | Documentation-only governance model for choosing future external tool adoption modes in AGENT PLATFORM / Siamese under the External Tool Integration Program. |
| Authority | Adoption mode decision model only, not source inspection, not dependency approval, not license approval, not external tool adoption, not vendoring, not forking, not wrapping, not submodule creation, not execution, not adapter implementation, not runtime activation, not provider/API/MCP activation, not product/Siamese source inspection, not Git automation, and not publication. |
| Prerequisite | P9.0 accepted at `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`. |
| Canonical root | `4_external/sources` |
| Legacy root | `external/sources` |
| Known GStack path/class metadata | `4_external/sources/gstack-main` as path/class metadata only. |
| Related documents | P9.0, P9.1-P9.4 if present, P9.6 if present, P8.R, P8.0-P8.R, P7.R, P6.R/P6.7, P5.R, P3.BR, P2.2/P2.3, P1 boundaries, P0 gates, S-03/S-04. |
| Output | External Tool Vendor / Fork / Wrapper / Submodule Decision Model |
| Result marker | `external_tool_adoption_mode_decision_model_ready` |

## 2. Purpose

P9.5 defines how AGENT PLATFORM chooses between external adoption modes. P9.5 operationalizes the post-P8 principle: Adopt / adapt / wrap validated MIT tools when they fit, and do not rebuild from scratch by default.

P9.5 prevents ad-hoc external tool integration. It defines decision criteria for vendor, fork, wrapper, submodule, import/reference-only, defer, and reject outcomes. It defines prerequisites before any mode can be selected as implementation-ready.

P9.5 prepares P10-P13 adoption decisions and P14 synthesis. P9.5 does not adopt any external tool. P9.5 does not inspect external source. P9.5 does not execute external tools. P9.5 does not mutate Git.

## 3. Current Posture

| Area | Current state | P9.5 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| P8.R closure | MVP-0 closed as manual/non-executing readiness. | No runtime, external adoption, provider/API/MCP, product/Siamese, or Git automation readiness is inherited. | Runtime activation or external tool adoption. |
| P9.0 charter | External integration charter accepted. | Adoption mode decisions must follow adopt/adapt/wrap before rebuild. | P9.5 as direct adoption authority. |
| Adopt/adapt/wrap principle | Validated external tools should be reused when safe. | Rebuild requires a rejection rationale. | Rebuild by default without external-tool evaluation. |
| Canonical external root | `4_external/sources`. | Use for ExternalSourcePathRef normalization. | `external/sources` as canonical root. |
| Source inspection | Gated by P9.3 and candidate-specific tickets. | Required before implementation-ready selection. | external source inspected by this ticket. |
| Dependency review | Gated by P9.2/P9.3 and candidate-specific review. | Required before adoption implementation. | dependency approved by this ticket. |
| License/trust intake | P9.2 alignment is available if present. | Required evidence before implementation. | license approved by this ticket or trust intake as trust approval. |
| Execution gates | P9.4 alignment is available if present. | Required before executable integration. | execution approved by this ticket. |
| Rollback/incident posture | P9.6 is pending if absent. | Required before implementation-ready decision. | rollback automation by P9.5. |
| Vendor mode | Candidate adoption mode. | Requires strong justification and explicit approval. | vendored by default. |
| Fork mode | Candidate adoption mode. | Requires patch necessity and ownership plan. | forked by default. |
| Wrapper mode | Candidate adoption mode. | Often preferred when isolation and boundary are strong. | wrapper implemented by this ticket. |
| Submodule mode | Candidate adoption mode. | Requires upstream-tracking justification. | submodule by default or submodule creation. |
| Import/reference-only mode | Candidate non-runtime mode. | Appropriate for architecture/evidence use. | Import/reference as dependency approval. |
| Defer mode | Legitimate outcome after insufficient evidence or pending gates. | DeferAfterAudit preserves future revisit. | Deferral as silent approval. |
| Reject mode | Legitimate outcome for boundary mismatch. | RejectForBoundaryMismatch blocks unsafe adoption. | Rejection without rationale. |
| Graphify | Evidence tooling candidate. | Future P10 decision must use P9.5. | Graphify adopted as runtime by P9.5. |
| Hermes | Runtime/UI/orchestration candidate. | Future P11 decision must use P9.5. | Hermes adopted or runtime active by P9.5. |
| GBrain/GStack | Memory/skill stack candidates. | Future P12 decisions must use P9.5; GStack path remains `4_external/sources/gstack-main` PathOnlyMetadata. | GBrain/GStack adopted, inspected, or executed by P9.5. |
| ECC-main | Agent OS candidate. | Future P13 decision must use P9.5. | ECC-main adopted as runtime by P9.5. |
| OpenCode | H0 manual harness candidate. | Future wrapper only after explicit gate. | OpenCode integrated runtime by P9.5. |
| Provider/API/MCP | Blocked by security/local policies. | Must pass provider/auth/API/MCP gates. | provider/API/MCP active. |
| Product/Siamese | Siamese is product vision. | Product-bound adoption needs product readiness. | product/Siamese source readable by default. |
| Git automation | User-owned. | Exact commit advice only. | Git automation active or `git add .` advice. |

## 4. Inputs Reviewed

Inputs were reviewed through allowed governance checks and path-only metadata checks only. External roots and GStack were checked with `Test-Path` only; no source tree was listed, enumerated, imported, executed, configured, adopted, or inspected.

| Input group | Document/path | Review mode | P9.5 use | Limitation |
| --- | --- | --- | --- | --- |
| P9.0 charter | `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md` | charter_review | Confirms P9.0 prerequisite and adopt/adapt/wrap posture. | No P9.0 modification. |
| P9.1 root normalization, if present | `0_architecture/governance/agent_platform_external_source_root_normalization.md` | root_normalization_review | Confirms `4_external/sources` canonical root and `external/sources` legacy root. | No P9.1 modification. |
| P9.2 license/trust intake, if present | `0_architecture/governance/agent_platform_external_source_license_trust_intake_model.md` | license_trust_alignment_review | Aligns required license/trust evidence. | License candidate is not license clearance. |
| P9.3 source inspection permission gate, if present | `0_architecture/governance/agent_platform_external_source_inspection_permission_gate.md` | inspection_gate_alignment_review | Aligns source inspection prerequisite. | Source inspection gate is not source inspection. |
| P9.4 external tool execution gate, if present | `0_architecture/governance/agent_platform_external_tool_execution_gate_model.md` | execution_gate_alignment_review | Aligns execution prerequisite. | Execution gate is not execution. |
| P9.6 rollback/incident protocol, if present | `0_architecture/governance/agent_platform_external_integration_rollback_incident_protocol.md` | rollback_incident_alignment_review | Not present; record `pending_P9.6_rollback_incident_alignment`. | Do not create or modify P9.6. |
| P8.R closure | `0_architecture/governance/agent_platform_p8_platform_mvp_readiness_closure.md` | p8_closure_review | Confirms accepted post-P8 baseline in this repo. | Prompt-listed shorter P8.R alias was absent and not used as blocker. |
| P8 external boundary docs | P8.0 external boundary, external inventory, security activation gate, Graphify boundary, GBrain/GStack boundary, Hermes boundary, OpenCode boundary, MVP-0 synthesis, MVP-0 implementation authorization, MVP-0 skeleton package | governance_markdown_review | Provides inherited boundaries. | No P8 document modified. |
| P7/P6/P5/P3/P2/P1/P0 baseline docs | Manual workflow closure, reviewer mesh, harness strategy, audits, reconciliation closures, metadata/evidence contracts, rollback baseline, runtime/provider/tool/agent hardening, Cognitive Semantic System hardening, activation/validation/security hardening | governance_markdown_review | Provides inherited governance posture. | No baseline document modified. |
| S-03/S-04 policies | Local-only secrets policy and tool/shell/network/MCP execution policy | security_policy_review | Confirms secrets, credentials, tools, network, and MCP remain gated. | No security enforcement activated. |
| Canonical external root path | `4_external/sources` | path_only_metadata_check | Confirms canonical root path reference only. | Source root is not dependency approval. |
| Legacy external root path | `external/sources` | legacy_path_reference_check | Classifies as legacy/superseded reference only. | Not canonical; absence is not a blocker. |
| GStack path | `4_external/sources/gstack-main` | path_only_metadata_check | Records known GStack path/class metadata only. | No GStack inspection, listing, import, execution, configuration, vendoring, forking, wrapping, submodule, patching, or adoption. |
| External source contents | Any external source contents | not_reviewed_blocked | Not reviewed by P9.5. | Requires future gated source review. |

Pending alignments:

- `pending_P9.6_rollback_incident_alignment`

## 5. Decision Model Overview

`ExternalToolAdoptionModeDecisionModel` is the governance model that compares external tool adoption modes after required evidence exists. It produces an `AdoptionModeDecision` record, not implementation.

| Decision stage | Purpose | Required evidence | Blocked shortcut | Future owner |
| --- | --- | --- | --- | --- |
| 1. candidate identification | Identify external candidate and purpose. | Candidate name, capability need, owner. | Automatic source ingestion. | P10-P13 owner. |
| 2. root/path normalization | Bind path to canonical root. | ExternalSourcePathRef under `4_external/sources`. | `external/sources` as canonical root. | P9.1 / candidate owner. |
| 3. license/trust intake | Determine license/trust candidate posture. | ExternalLicenseReviewRef and trust intake. | License metadata as adoption approval. | P9.2 / candidate owner. |
| 4. source inspection authorization | Authorize exact source review scope. | Source inspection gate. | Source path is source permission. | P9.3 / candidate owner. |
| 5. source/dependency/runtime audit | Understand code, dependency, entrypoint, and side effects. | Source, dependency, runtime/entrypoint summaries. | Dependency approval by path presence. | Candidate owner. |
| 6. execution gate review | Decide whether execution may be tested. | ExternalExecutionGateRef. | Execution gate is execution. | P9.4 / candidate owner. |
| 7. adapter boundary review | Define adapter or isolation boundary. | ExternalAdapterBoundaryRef. | Adapter boundary is adapter implementation. | Candidate owner. |
| 8. rollback/incident posture review | Define rollback and incident handling. | ExternalRollbackIncidentRef. | Rollback/incident posture as rollback automation. | P9.6 / candidate owner. |
| 9. adoption mode comparison | Compare vendor/fork/wrapper/submodule/reference/defer/reject. | AdoptionModeEvidencePackage. | Selecting mode without complete evidence. | P9.5 / candidate decision ticket. |
| 10. human approval | Obtain explicit scope-bound approval. | ExternalHumanApprovalRef. | Silent or implied approval. | User / governance owner. |
| 11. implementation authorization | Create future implementation ticket. | Approved AdoptionModeDecision. | Implementation inside P9.5. | Candidate implementation ticket. |
| 12. closure/audit | Close decision and audit constraints. | Closure record and limitations. | Skipping audit. | Candidate closure / P14. |

No adoption mode can be selected as implementation-ready until all required stages are satisfied.

## 6. Adoption Mode Vocabulary

`AdoptionModeCandidate` is any candidate mode under evaluation. Required modes:

| Mode | Meaning | When appropriate | Required prerequisites | Blocked shortcuts | Expected future implementation ticket type |
| --- | --- | --- | --- | --- | --- |
| `AdoptAsVendorCode` | Copy approved external code into governed repo scope with license preservation. | Stable source, low update need, strong auditability, acceptable repo impact. | License clearance, source review, dependency review, security review, rollback posture, human approval. | Vendoring by default or path presence. | Vendor implementation ticket. |
| `AdoptAsSubmodule` | Track external repository as a submodule. | Upstream tracking is essential and workflow burden is acceptable. | License/trust, source/dependency review, submodule workflow review, rollback posture, human approval. | Submodule by default or submodule creation in P9.5. | Submodule implementation ticket. |
| `WrapExistingSource` | Keep external source isolated and call via approved boundary. | Stable API/CLI, strong isolation, minimal patch need. | Source/dependency/runtime review, execution gate, adapter boundary, rollback posture, human approval. | wrapper implemented by this ticket. | Wrapper/adapter implementation ticket. |
| `ForkAndPatch` | Fork external source and maintain patches. | Necessary patches cannot be upstreamed or wrapped. | License clearance, source review, patch plan, ownership plan, rollback posture, human approval. | forked by default or patching in P9.5. | Fork maintenance implementation ticket. |
| `ImportReferenceOnly` | Use as documentation, architecture, or evidence reference without runtime/dependency adoption. | Tool informs design but does not need runtime integration. | Root/path normalization and boundary note; source review only if details are needed. | Import/reference as dependency approval. | Documentation/evidence ticket. |
| `DeferAfterAudit` | Defer decision after incomplete or mixed audit results. | Value exists but gates/evidence are incomplete or risk is unresolved. | Audit summary and revisit condition. | Deferral as approval. | Follow-up review ticket. |
| `RejectForBoundaryMismatch` | Reject adoption because boundaries or risks do not fit. | License, dependency, runtime, security, product, autonomy, or maintenance mismatch. | Evidence-backed rejection rationale. | Rejection without rationale. | Rejection/closure ticket. |

## 7. AdoptionModeDecision Contract

`AdoptionModeDecision` fields:

```yaml
AdoptionModeDecision:
  decision_id:
  candidate_tool_ref:
  candidate_path_ref:
  candidate_license_ref:
  candidate_dependency_review_ref:
  candidate_source_review_ref:
  candidate_execution_gate_ref:
  candidate_adapter_boundary_ref:
  candidate_rollback_incident_ref:
  candidate_security_review_ref:
  candidate_product_boundary_ref:
  candidate_git_boundary_ref:
  decision_options:
  selected_mode:
  rejected_modes:
  decision_status:
  decision_rationale:
  required_human_approval:
  required_follow_up_tickets:
  blocked_actions:
  limitations:
  stop_rules:
```

AdoptionModeDecision is a governance record, not an adoption action.

Reference fields may use `ExternalSourcePathRef`, `ExternalDependencyReviewRef`, `ExternalLicenseReviewRef`, `ExternalExecutionGateRef`, `ExternalAdapterBoundaryRef`, `ExternalRollbackIncidentRef`, and `ExternalHumanApprovalRef`.

## 8. AdoptionModeStatus Vocabulary

`AdoptionModeStatus` values:

| Status | Meaning |
| --- | --- |
| `not_started` | No decision work started. |
| `path_only_metadata` | Only path/class metadata exists. |
| `pending_license_trust` | License/trust intake is required. |
| `pending_source_inspection_gate` | Source inspection permission is required. |
| `pending_dependency_review` | Dependency review is required. |
| `pending_execution_gate` | Execution gate is required. |
| `pending_adapter_boundary` | Adapter boundary is required. |
| `pending_rollback_incident` | Rollback/incident posture is required. |
| `candidate_for_decision` | Required evidence is sufficient for decision comparison. |
| `selected_for_future_implementation` | Mode selected for later implementation ticket. |
| `deferred` | Decision deferred with revisit condition. |
| `rejected` | Candidate or mode rejected with rationale. |
| `blocked` | Candidate blocked by missing gate or stop rule. |
| `out_of_scope` | Candidate outside ticket/program scope. |

No status value executes adoption or mutates repo.

## 9. Evidence Package Requirements

`AdoptionModeEvidencePackage` is the minimum evidence bundle needed to compare modes and later authorize implementation.

| Evidence item | Required before decision? | Required before implementation? | Source ticket | Blocker if missing |
| --- | --- | --- | --- | --- |
| External source root normalization | yes | yes | P9.1 | Cannot bind path safely. |
| Source path ref | yes | yes | P9.1 / candidate owner | Candidate path unknown. |
| License review | yes | yes | P9.2 | No adoption implementation. |
| Trust intake | yes | yes | P9.2 | No adoption implementation. |
| Source inspection authorization | yes | yes | P9.3 | No source review or implementation-ready selection. |
| Source review summary | yes, except pure reference-only if no details are used | yes for adoption modes | Candidate source review | No vendor/fork/wrapper/submodule implementation. |
| Dependency review summary | yes for adoption modes | yes | Candidate dependency review | path presence is not dependency approval. |
| Runtime/entrypoint review summary | yes for executable modes | yes | Candidate runtime review | No execution or wrapper/submodule/fork runtime use. |
| Side-effect review | yes for executable modes | yes | Candidate runtime/security review | No execution-ready mode. |
| Security review | yes | yes | S-03/S-04 plus candidate review | No adoption implementation. |
| Execution gate review | yes for executable modes | yes for executable modes | P9.4 | No execution. |
| Adapter boundary review | yes for wrapper/runtime modes | yes | Candidate adapter boundary ticket | No adapter implementation. |
| Rollback/incident posture | yes | yes | P9.6 | No implementation-ready mode. |
| Product boundary review, if applicable | conditional | yes when product-bound | P4 / GT-09 or equivalent | No product/Siamese integration. |
| Git boundary review | yes | yes | P9/P0 governance | No agent Git mutation. |
| Human approval ref | yes for selected implementation-ready mode | yes | User/governance owner | No implementation authorization. |

## 10. Vendor Code Candidate Model

`VendorCodeCandidate` evaluates whether copied external code should become governed repository content after gates and approval.

| Decision criterion | Favorable condition | Unfavorable condition | Required gate | Risk |
| --- | --- | --- | --- | --- |
| License compatibility | Clear permissive license and preserved notices. | Ambiguous, incompatible, or missing license. | P9.2 | Legal/reuse risk. |
| Dependency footprint | Small, audited, stable dependencies. | Large, dynamic, or risky dependency tree. | Dependency review | Supply-chain risk. |
| Source stability | Stable code with low churn. | Frequent breaking changes. | Source review | Update burden. |
| Patch volume | Minimal or no local changes. | Heavy patch set required. | Adapter/adoption review | Maintenance burden. |
| Update cadence | Infrequent critical updates. | Rapid upstream security churn. | P9.6 | Stale vendor risk. |
| Security exposure | Low privilege, no credentials. | Handles secrets or network execution. | S-03/S-04 | Credential/security risk. |
| Repo contamination risk | Clearly isolated subtree with license metadata. | Mixed generated/source/secrets boundaries. | Repo impact review | Governance contamination. |
| Rollback complexity | Easy removal or replacement. | Deep coupling across repo. | P9.6 | Rollback risk. |
| Maintenance burden | Owned by named maintainer. | No ownership or update process. | Human approval | Abandonment risk. |
| Auditability | Small, readable, traceable snapshot. | Opaque or generated source. | Source review | Audit failure. |
| Testability | Can be validated under future gates. | Requires unavailable services/runtime. | Execution/validation gate | Validation gap. |
| Isolation feasibility | Can remain isolated from runtime. | Spreads across core runtime. | Adapter boundary | Runtime coupling. |

Vendoring is not default and requires explicit approval. P9.5 does not vendor code.

## 11. Submodule Candidate Model

`SubmoduleCandidate` evaluates whether upstream tracking is worth the operational burden.

| Decision criterion | Favorable condition | Unfavorable condition | Required gate | Risk |
| --- | --- | --- | --- | --- |
| Upstream tracking need | Frequent upstream updates are valuable. | Snapshot is sufficient. | Adoption review | Unnecessary complexity. |
| Repo cleanliness | External code stays outside main tree. | Submodule introduces ambiguous ownership. | Repo impact review | Governance drift. |
| Reproducibility | Commit pinning is stable. | Floating refs or unavailable upstream. | Git/repro review | Build drift. |
| Dependency isolation | Dependencies remain contained. | Dependencies leak into core runtime. | Dependency review | Supply-chain risk. |
| CI/build impact | No automatic build/test activation. | CI requires external tool execution. | Execution gate | Unapproved execution. |
| Developer workflow impact | Team accepts submodule workflow. | Workflow confusion likely. | Human approval | Operational burden. |
| Security review | Upstream trust is reviewed. | Unknown provenance or unsafe maintainer practices. | P9.2/security review | Trust risk. |
| Submodule operational burden | Update/rollback process is documented. | No owner or update plan. | P9.6 | Maintenance risk. |
| Rollback complexity | Pin can be reverted cleanly. | Deep runtime coupling. | P9.6 | Rollback risk. |

Submodule creation is not authorized by P9.5.

## 12. Wrapper Candidate Model

`WrapperCandidate` evaluates whether external source can remain isolated behind a governed boundary.

| Decision criterion | Favorable condition | Unfavorable condition | Required gate | Risk |
| --- | --- | --- | --- | --- |
| Stable external API/CLI | Interface is versioned and predictable. | Interface is unstable or undocumented. | Source/runtime review | Breakage risk. |
| Minimal patch need | No local patching required. | Requires deep source changes. | Adoption review | Maintenance burden. |
| Isolation feasibility | Can run in controlled boundary. | Requires privileged runtime access. | Adapter boundary | Runtime risk. |
| Execution boundary | Exact commands/scopes can be gated. | Tool has broad side effects. | P9.4 | Execution risk. |
| Input/output contract clarity | Inputs/outputs are explicit and testable. | Ambiguous or stateful behavior. | Adapter boundary | Data integrity risk. |
| Rollback simplicity | Wrapper can be disabled without data loss. | Runtime depends on wrapper state. | P9.6 | Rollback risk. |
| Provider/API/MCP risk | No provider/API/MCP activation needed. | Requires credentials or remote calls. | Provider/MCP gate | Credential/network risk. |
| Credential risk | No secret handling. | Reads `.env`, tokens, API keys, auth stores. | S-03 | Secret exposure. |
| Runtime side effects | Side effects are bounded and reversible. | Writes uncontrolled files or services. | P9.4/P9.6 | State contamination. |
| Observability | Logs and outcomes can be audited later. | Opaque behavior. | Validation/audit gate | Audit gap. |
| Adapter boundary | Clear non-invasive adapter possible. | Requires invasive integration. | Adapter boundary | Coupling risk. |

Wrapping existing source is often preferred when safe, but P9.5 does not implement wrappers.

## 13. ForkAndPatch Candidate Model

`ForkAndPatchCandidate` evaluates whether a maintained fork is justified.

| Decision criterion | Favorable condition | Unfavorable condition | Required gate | Risk |
| --- | --- | --- | --- | --- |
| Upstream mismatch | Upstream cannot support required boundary. | Upstream already supports needed mode. | Source/adoption review | Unnecessary fork. |
| Patch necessity | Patches are small, scoped, and justified. | Large or speculative patch plan. | Human approval | Maintenance burden. |
| License compatibility | Forking and modification permitted. | License ambiguity. | P9.2 | Legal risk. |
| Maintenance burden | Named owner and update policy. | No maintainer or update plan. | P9.6/human approval | Abandonment risk. |
| Divergence risk | Divergence is acceptable and tracked. | Rapidly diverging upstream. | Rollback/update plan | Security drift. |
| Security review | Patched code can be audited. | Patches obscure unsafe behavior. | Security review | Vulnerability risk. |
| Rollback complexity | Fork can be disabled or replaced. | Core runtime depends on fork internals. | P9.6 | Rollback risk. |
| Contribution-back possibility | Patches may upstream later. | Private divergence is permanent. | Adoption review | Long-term ownership risk. |
| Long-term ownership | Cost is explicitly accepted. | Ownership unclear. | Human approval | Sustainability risk. |

Forking is high-burden and requires explicit approval. P9.5 does not fork or patch code.

## 14. ImportReferenceOnly Candidate Model

`ImportReferenceCandidate` evaluates documentation/reference-only use without runtime or dependency adoption.

| Decision criterion | Favorable condition | Unfavorable condition | Required gate | Risk |
| --- | --- | --- | --- | --- |
| Architecture reference value | Tool informs design patterns or evidence. | No concrete learning value. | Governance review | Noise. |
| No runtime need | Runtime integration is unnecessary. | Capability is needed live. | Adoption review | Under-integration. |
| Documentation-only use | Summary can cite boundaries without source ingestion. | Requires detailed source extraction. | P9.3 if source details are needed | Accidental source review. |
| Evidence-only use | Evidence supports but does not decide. | Evidence is treated as authority. | Governance review | Authority drift. |
| Unsupported execution risk | Execution is explicitly blocked. | Users may infer execution readiness. | P9.4 if execution is needed | Unsafe execution. |
| Dependency avoidance | Avoids dependency approval and runtime coupling. | Hidden dependency import. | Dependency review if dependency use is proposed | Dependency drift. |
| Integration deferral | Revisit condition is clear. | Indefinite ambiguity. | Follow-up ticket | Decision drift. |

Import/reference-only is appropriate when the tool informs architecture but should not enter runtime.

## 15. Defer / Reject Candidate Model

`DeferAfterAuditCandidate` and `RejectForBoundaryMismatchCandidate` are valid outcomes, not failures.

| Mode | When to use | Required evidence | Required explanation | Future revisit rule |
| --- | --- | --- | --- | --- |
| `DeferAfterAudit` | Evidence is incomplete, gates are pending, or risks are unresolved but candidate remains plausible. | Current audit status, missing evidence list, owner. | Why decision cannot be made now. | Revisit only when missing gates/evidence are complete. |
| `RejectForBoundaryMismatch` | Candidate conflicts with license, dependency, runtime, security, product, repo, autonomy, or maintenance boundaries. | Boundary mismatch evidence and rejected modes. | Why adoption does not fit. | Revisit only if mismatch is resolved or user explicitly reopens. |

Reject reasons must include one or more of:

- license mismatch
- dependency risk
- runtime side effects
- security risk
- credential risk
- provider/API/MCP risk
- product boundary conflict
- repo contamination risk
- maintenance burden
- overlap/conflict with existing adopted tool
- autonomy/orchestration risk
- insufficient value over local implementation

## 16. Mode Comparison Matrix

| Candidate mode | Repo impact | Maintenance burden | Update burden | Security exposure | Rollback complexity | Runtime risk | Auditability | Isolation feasibility | Best suited for | Default posture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `WrapExistingSource` | Low to medium | Medium | Medium | Bounded if isolated | Low to medium | Medium | High if interface logged | High when API/CLI stable | Executable external tools with clear boundary | Often preferred when isolation is strong. |
| `ImportReferenceOnly` | Low | Low | Low | Low | Low | Low | Medium | High | Architecture inspiration/evidence-only tools | Preferred for reference/evidence-only tools. |
| `AdoptAsVendorCode` | High | Medium to high | Medium | Medium to high | Medium to high | Medium | High if snapshot small | Medium | Stable code needing local control | Requires strong justification. |
| `AdoptAsSubmodule` | Medium | Medium | Medium to high | Medium | Medium | Medium | Medium | Medium | Tools needing upstream tracking | Requires strong upstream-tracking justification. |
| `ForkAndPatch` | High | High | High | Medium to high | High | Medium to high | Medium | Medium to low | Necessary patch ownership | Requires strong patch necessity. |
| `DeferAfterAudit` | None | Low | None | None | None | None | High | N/A | Incomplete evidence or pending gates | Legitimate outcome. |
| `RejectForBoundaryMismatch` | None | Low | None | None | None | None | High | N/A | Boundary mismatch or insufficient value | Legitimate outcome. |

Wrapper is often preferred for executable external tools when isolation is strong. Import/reference-only is preferred for architecture inspiration/evidence-only tools. Vendoring requires strong justification. Submodule requires strong upstream-tracking justification. Forking requires strong patch necessity. Defer/reject must remain legitimate outcomes.

## 17. Tool-Class Default Guidance

| Tool class | Default candidate mode | Alternative modes | Blocked modes without gate | Future project owner |
| --- | --- | --- | --- | --- |
| Graphify evidence tooling | `WrapExistingSource` or `ImportReferenceOnly`, depending on P10. | `AdoptAsVendorCode` only with strong justification. | Execution, runtime, `.graphifyignore` changes, generated output tracking. | P10 |
| Hermes runtime/UI/orchestration candidate | `WrapExistingSource` or `AdoptAsSubmodule` only after P11 audit. | `ImportReferenceOnly`, `DeferAfterAudit`, `RejectForBoundaryMismatch`. | Runtime active, execution, source inspection before gate. | P11 |
| GBrain memory candidate | `WrapExistingSource`, `AdoptAsSubmodule`, or `AdoptAsVendorCode` only after P12 audit. | `ImportReferenceOnly`, `DeferAfterAudit`, `RejectForBoundaryMismatch`. | Persistent memory, execution, source inspection before gate. | P12 |
| GStack skill stack candidate | `WrapExistingSource`, `AdoptAsSubmodule`, or `AdoptAsVendorCode` only after P12 audit. | `ImportReferenceOnly`, `DeferAfterAudit`, `RejectForBoundaryMismatch`. | Skill execution, GStack inspection/list/import/execution/configuration/adoption. | P12 |
| ECC-main agent OS candidate | Reference/component adoption candidate only after P13. | `ImportReferenceOnly`, limited wrapper candidate, `RejectForBoundaryMismatch`. | Full runtime by default, agent OS activation. | P13 |
| OpenCode harness candidate | H0 manual harness / future wrapper only after explicit gate. | `ImportReferenceOnly`, `DeferAfterAudit`. | AGENT PLATFORM runtime integration. | Later OpenCode gate |
| Codegraph analysis candidate | Reference or wrapper candidate only after EXT review. | `ImportReferenceOnly`, `DeferAfterAudit`, `RejectForBoundaryMismatch`. | Execution/source inspection without gate. | EXT/P10/P14 later gate |
| Provider/model APIs | Blocked until provider/auth/API gates. | `DeferAfterAudit`, `RejectForBoundaryMismatch`. | Active credentials, API calls, model calls. | Provider/API gate |
| MCP servers/tools/resources | Blocked until MCP gates. | `DeferAfterAudit`, `RejectForBoundaryMismatch`. | MCP activation, tools/resources calls. | MCP gate |
| Product/Siamese-specific tools | Deferred to P4/GT-09 or equivalent. | `ImportReferenceOnly` for governance context. | Product/Siamese source inspection or product runtime. | P4 / GT-09 plus P9/P10+ gates |
| Git tools | User manual Git only; automation blocked. | Documentation-only guidance. | Git automation, staging, commit, push, force-add. | User / Git governance |

## 18. Required Gate Chain Before Implementation

Required chain: candidate path normalized -> license/trust intake -> source inspection gate -> source/dependency/runtime audit -> execution gate -> adapter boundary -> rollback/incident posture -> adoption mode decision -> human approval -> implementation authorization.

| Gate | Required evidence | Owner ticket | Stop rule if missing |
| --- | --- | --- | --- |
| Candidate path normalized | ExternalSourcePathRef under `4_external/sources`. | P9.1 / candidate owner | Stop if path uses `external/sources` as canonical or path is unknown without inventory. |
| License/trust intake | ExternalLicenseReviewRef and trust intake. | P9.2 | Stop if license/trust evidence is missing. |
| Source inspection gate | Source inspection permission. | P9.3 | Stop on source review without gate. |
| Source/dependency/runtime audit | Source, dependency, runtime, entrypoint, side-effect summaries. | Candidate owner | Stop if audit is incomplete for adoption mode. |
| Execution gate | ExternalExecutionGateRef. | P9.4 | Stop on execution without gate. |
| Adapter boundary | ExternalAdapterBoundaryRef. | Candidate owner | Stop on adapter implementation without boundary. |
| Rollback/incident posture | ExternalRollbackIncidentRef. | P9.6 | Stop if rollback/incident posture is missing. |
| Adoption mode decision | AdoptionModeDecision. | P9.5 / candidate decision ticket | Stop if decision is implied or ad hoc. |
| Human approval | ExternalHumanApprovalRef. | User/governance owner | Stop if approval is not explicit and scope-bound. |
| Implementation authorization | Future implementation ticket. | Candidate implementation owner | Stop if implementation begins in P9.5. |

## 19. Decision Outcomes For Future Projects

| Project | Decision owner ticket | Must use P9.5 to decide | Allowed outcomes | Blocked shortcut |
| --- | --- | --- | --- | --- |
| P10 Graphify | P10 adoption decision ticket | Yes | `WrapExistingSource`, `ImportReferenceOnly`, `AdoptAsVendorCode`, `DeferAfterAudit`, `RejectForBoundaryMismatch` | Graphify execution or runtime adoption from P9.5. |
| P11 Hermes | P11.4 Hermes Adoption Mode Decision | Yes | `WrapExistingSource`, `AdoptAsSubmodule`, `ImportReferenceOnly`, `DeferAfterAudit`, `RejectForBoundaryMismatch` | Hermes runtime/source adoption without P11 gates. |
| P12 GBrain | P12.5 GBrain Adoption Decision | Yes | `WrapExistingSource`, `AdoptAsSubmodule`, `AdoptAsVendorCode`, `ImportReferenceOnly`, `DeferAfterAudit`, `RejectForBoundaryMismatch` | GBrain memory runtime before gates. |
| P12 GStack | P12.6 GStack Adoption Decision | Yes | `WrapExistingSource`, `AdoptAsSubmodule`, `AdoptAsVendorCode`, `ForkAndPatch`, `ImportReferenceOnly`, `DeferAfterAudit`, `RejectForBoundaryMismatch` | GStack adopted by path presence. |
| P13 ECC-main | P13.5 ECC-main Adoption Decision | Yes | `ImportReferenceOnly`, limited component `WrapExistingSource`, `DeferAfterAudit`, `RejectForBoundaryMismatch` | ECC-main adopted as runtime by default. |
| P14 Integrated External Runtime Synthesis | P14.5 External Stack MVP-1 Architecture | Yes | Reconcile P9.5-derived decisions only after P10-P13 closures. | Runtime synthesis without P10-P13 closures. |

P11.4 Hermes Adoption Mode Decision, P12.5 GBrain Adoption Decision, P12.6 GStack Adoption Decision, P13.5 ECC-main Adoption Decision, and P14.5 External Stack MVP-1 Architecture must consume P9.5.

## 20. Source Inspection Boundary

P9.5 does not authorize source inspection. P9.5 does not authorize source tree listing. P9.5 does not authorize source review. P9.3 defines source inspection permission gates. Candidate adoption mode cannot be selected as implementation-ready without source inspection authorization and source review.

| Source surface | P9.5 status | Future gate | Stop rule |
| --- | --- | --- | --- |
| `4_external/sources` | canonical root only | P9.3 | Stop on inspect/list/enumerate request. |
| `4_external/sources/gstack-main` | PathOnlyMetadata only | P12/P9.3 | Stop on GStack inspect/list/import request. |
| `external/sources` | legacy reference only | P9.1 / future migration if needed | Stop if used as canonical root. |
| Graphify source | not inspected | P10/P9.3 | Stop on source review without gate. |
| Hermes source | not inspected | P11/P9.3 | Stop on source review without gate. |
| GBrain source | not inspected | P12/P9.3 | Stop on source review without gate. |
| GStack source | not inspected | P12/P9.3 | Stop on source review without gate. |
| ECC-main source | not inspected | P13/P9.3 | Stop on source review without gate. |
| OpenCode source | not inspected | Later OpenCode/P9.3 gate | Stop on source review without gate. |
| Codegraph source | not inspected | EXT/P9.3 gate | Stop on source review without gate. |
| Provider SDK / MCP server/tool/resource source | not inspected | Provider/MCP gate | Stop on provider/MCP source or activation request. |
| Product/Siamese source | not inspected | P4 / GT-09 or equivalent | Stop on product/Siamese source request. |

## 21. Execution Boundary

P9.5 does not authorize execution. P9.5 does not authorize local tool execution. P9.5 does not authorize external tool execution. P9.5 does not authorize provider/API/MCP execution. P9.5 does not authorize runtime adoption. P9.4 defines External Tool Execution Gate Model.

| Execution scenario | P9.5 status | Future gate | Stop rule |
| --- | --- | --- | --- |
| Graphify or `/graphify` | not authorized | P10/P9.4 | Stop on execution request. |
| Hermes execution/runtime | not authorized | P11/P9.4 | Stop on execution/runtime request. |
| GBrain execution/runtime | not authorized | P12/P9.4 | Stop on execution/runtime request. |
| GStack execution/configuration | not authorized | P12/P9.4 | Stop on execution/configuration request. |
| ECC-main execution/agent OS | not authorized | P13/P9.4 | Stop on execution/runtime request. |
| OpenCode execution by AGENT PLATFORM | not authorized | Later OpenCode gate | Stop on execution request. |
| Codegraph execution | not authorized | EXT/P9.4 gate | Stop on execution request. |
| Provider/API/model calls | not authorized | Provider/API gate | Stop on call request. |
| MCP resources/tools | not authorized | MCP gate | Stop on MCP activation request. |
| Tests, CI, scripts, Python, package managers, builds, validation | not authorized by P9.5 | Appropriate validation/build gate | Stop on execution request. |

## 22. Repository Impact Boundary

P9.5 does not authorize repository mutation. P9.5 does not authorize vendoring. P9.5 does not authorize forking. P9.5 does not authorize submodule creation. P9.5 does not authorize wrapping implementation. P9.5 does not authorize path migration. P9.5 does not authorize generated output tracking. P9.5 does not authorize source tracking expansion.

| Repo-impact scenario | P9.5 status | Future gate | Stop rule |
| --- | --- | --- | --- |
| Vendor external code | not authorized | P9.5-derived implementation ticket plus human approval | Stop on vendor request. |
| Fork external code | not authorized | Fork implementation ticket plus human approval | Stop on fork request. |
| Wrap external code | not authorized | Wrapper/adapter implementation ticket plus gate | Stop on wrapper implementation request. |
| Patch external code | not authorized | Fork/patch implementation ticket | Stop on patch request. |
| Create submodule | not authorized | Submodule implementation ticket plus Git approval | Stop on submodule request. |
| Create symlink | not authorized | Future explicit filesystem migration gate | Stop on symlink request. |
| Move/rename directories | not authorized | Future path migration gate | Stop on move/rename request. |
| Modify `4_external/sources` or `external/sources` | not authorized | Candidate implementation/migration gate | Stop on external directory modification request. |
| Modify `.gitignore` or `.graphifyignore` | not authorized | Relevant future gate | Stop on ignore file modification request. |
| Generated output tracking | not authorized | Future source/output tracking gate | Stop on tracking approval request. |
| Source tracking expansion | not authorized | Future tracking gate | Stop on expansion request. |

## 23. Security / Secret Boundary

P9.5 does not inspect secrets. P9.5 does not scan secrets. P9.5 does not authorize external code handling of secrets. `.env`, credentials, provider configs, token stores, browser auth, local credential stores, and API keys remain blocked. Any adoption mode requiring credentials must go through provider/auth/API/MCP gates.

| Sensitive surface | P9.5 status | Future gate | Incident posture |
| --- | --- | --- | --- |
| `.env` | not inspected | S-03 / P9.6 | Stop and route to incident posture if discovered later. |
| Credentials / token stores / browser auth / local credential stores | not inspected | S-03 / P9.6 | Stop and escalate under security policy. |
| API keys / provider configs | not inspected | Provider/auth/API gate / P9.6 | Stop and route to credential handling policy. |
| MCP server/tool/resource secrets | not inspected | S-04 / MCP gate / P9.6 | Stop and route to MCP/security incident posture. |
| External code handling secrets | not authorized | Provider/auth/API/MCP gates plus security review | Block adoption implementation until reviewed. |

## 24. Product / Siamese Boundary

Siamese is product vision, not product activation. Product/Siamese source is not in scope for P9.5. Product-bound integration requires P4 / GT-09 or equivalent product readiness gate. Adoption modes cannot target product/Siamese source without product readiness.

| Product-bound scenario | P9.5 decision | Blocked shortcut | Future gate |
| --- | --- | --- | --- |
| Product/Siamese source inspection | not authorized | Reading product/Siamese source by default. | P4 / GT-09 or equivalent plus source gate. |
| Product adapter | not authorized | Adapter implementation in P9.5. | Product readiness plus adapter implementation gate. |
| External tool to product runtime | not authorized | Product runtime activation from adoption-mode model. | Product readiness plus P9.4/P9.5/P14 gates. |
| Product provider/API/MCP integration | not authorized | Credentials/API/MCP activation. | Product readiness plus provider/API/MCP gates. |

## 25. Rollback / Incident Boundary

Adoption mode cannot become implementation-ready without rollback/incident posture. P9.6 defines rollback/incident protocol. P9.5 may define rollback/incident requirements but does not implement rollback automation. No quarantine/deletion automation. No publication. No source tracking expansion.

| Adoption mode | Rollback requirement | Incident requirement | Blocker if missing |
| --- | --- | --- | --- |
| `AdoptAsVendorCode` | Snapshot removal/revert plan and license notice handling. | Secret/license/security incident routing. | Cannot become implementation-ready. |
| `AdoptAsSubmodule` | Pin revert/remove plan and upstream availability plan. | Upstream compromise and pin rollback handling. | Cannot become implementation-ready. |
| `WrapExistingSource` | Disable wrapper and isolate outputs/state. | Execution side-effect and credential incident handling. | Cannot become implementation-ready. |
| `ForkAndPatch` | Patch rollback and upstream rebase/replacement plan. | Divergence/security incident handling. | Cannot become implementation-ready. |
| `ImportReferenceOnly` | Remove/deprecate reference if invalid. | Misinformation/provenance correction. | Cannot be closure-ready if provenance unclear. |
| `DeferAfterAudit` | Revisit/close deferral condition. | Escalate discovered blockers. | Cannot be silently treated as approval. |
| `RejectForBoundaryMismatch` | Record rejected modes and rationale. | Reopen only with explicit new evidence. | Cannot be reopened implicitly. |

## 26. Git Boundary

P9.5 may provide exact commit advice only. P9.5 must not mutate Git. User performs Git manually. Never recommend git add .

No submodule commands are authorized. No vendor/fork/wrapper implementation commands are authorized. No path migration commands are authorized.

Required command pattern:

```powershell
git status --short

git add <exact_path_1>

git commit -m "<exact ticket message>"

git push origin main
```

## 27. Stop Rules

- Stop on missing P9.0 request.
- Stop on request to adopt a tool in this ticket.
- Stop on request to vendor code in this ticket.
- Stop on request to fork code in this ticket.
- Stop on request to wrap code in this ticket.
- Stop on request to patch code in this ticket.
- Stop on request to create submodule in this ticket.
- Stop on request to create symlink in this ticket.
- Stop on request to move/rename directories in this ticket.
- Stop on request to use `external/sources` as canonical root.
- Stop on request to require `external/sources` as mandatory current root.
- Stop on request to inspect `4_external/sources`.
- Stop on request to list `4_external/sources`.
- Stop on request to enumerate `4_external/sources`.
- Stop on request to inspect `4_external/sources/gstack-main`.
- Stop on request to list `4_external/sources/gstack-main`.
- Stop on request to import GStack.
- Stop on request to execute GStack.
- Stop on request to configure GStack.
- Stop on request to adopt GStack.
- Stop on external source content inspection request.
- Stop on external source tree listing request.
- Stop on external source adoption request.
- Stop on external tool execution request.
- Stop on source review request without P9.3.
- Stop on execution request without P9.4.
- Stop on adoption implementation request without P9.5 closure plus candidate-specific adoption decision.
- Stop on rollback/incident implementation request.
- Stop on Graphify execution request.
- Stop on Hermes execution request.
- Stop on GBrain execution request.
- Stop on ECC-main execution request.
- Stop on OpenCode execution request.
- Stop on provider/API/MCP request.
- Stop on credential request.
- Stop on `.env` request.
- Stop on product/Siamese source request.
- Stop on runtime activation request.
- Stop on adapter implementation request.
- Stop on persistence DB request.
- Stop on vector DB request.
- Stop on graph DB request.
- Stop on telemetry/event streaming request.
- Stop on generated output tracking request.
- Stop on source tracking expansion request.
- Stop on publication request.
- Stop on Git mutation by agent request.
- Stop on `git add .` recommendation request.
- Stop on request to create P9.6+ files in this ticket.

## 28. Future Validation Targets

Future validation targets are proposed only and were not executed:

- P9.0 prerequisite invariant.
- Adoption mode vocabulary completeness.
- AdoptionModeDecision required field completeness.
- AdoptionModeStatus vocabulary completeness.
- AdoptionModeEvidencePackage completeness.
- VendorCodeCandidate criteria completeness.
- SubmoduleCandidate criteria completeness.
- WrapperCandidate criteria completeness.
- ForkAndPatchCandidate criteria completeness.
- ImportReferenceOnly criteria completeness.
- Defer/Reject criteria completeness.
- Tool-class default guidance completeness.
- Required gate chain completeness.
- P11.4 consumption readiness.
- P12.5 consumption readiness.
- P12.6 consumption readiness.
- P13.5 consumption readiness.
- P14 synthesis readiness.
- No external source inspection invariant.
- No external source listing invariant.
- No adoption implementation invariant.
- No vendoring/forking/wrapping/submodule invariant.
- No path-presence-as-dependency-approval invariant.
- No execution invariant.
- No Git mutation invariant.
- No `git add .` invariant.

## 29. Future Hardening Candidates

Future hardening candidates are proposed only and were not started:

- P9-ADOPT-HARD-01 - AdoptionModeDecision Schema Candidate.
- P9-ADOPT-HARD-02 - AdoptionModeEvidencePackage Checklist.
- P9-ADOPT-HARD-03 - VendorCodeCandidate Risk Matrix.
- P9-ADOPT-HARD-04 - WrapperCandidate Isolation Checklist.
- P9-ADOPT-HARD-05 - SubmoduleCandidate Operational Checklist.
- P9-ADOPT-HARD-06 - ForkAndPatch Maintenance Checklist.
- P9-ADOPT-HARD-07 - ImportReferenceOnly Boundary Checklist.
- P9-ADOPT-HARD-08 - Defer/Reject Rationale Checklist.
- P9-ADOPT-HARD-09 - Tool-Class Default Guidance Review.
- P9-ADOPT-HARD-10 - P9.R Adoption Model Audit Input.

## 30. Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_external_tool_vendor_fork_wrapper_submodule_decision_model.md`

Modified:

- none

Not created / not approved:

- no P9.6-P9.R files
- no P10-P14 files
- no external source directory creation
- no external source directory movement
- no external source directory rename
- no symlinks
- no submodules
- no vendor code
- no forked code
- no wrapped code
- no patched external code
- no external source inspection
- no external source listing
- no external source enumeration
- no GStack inspection
- no GStack listing
- no GStack import
- no GStack execution
- no GStack configuration
- no GStack adoption
- no Graphify execution
- no Hermes execution
- no GBrain execution
- no ECC-main execution
- no OpenCode execution
- no provider/API/MCP activation
- no credentials
- no API calls
- no MCP calls
- no live connectors
- no product/Siamese source inspection
- no source loading
- no tool execution
- no agent execution
- no automatic dispatch
- no runtime activation
- no persistence DB
- no vector DB
- no graph DB
- no telemetry
- no event streaming
- no generated output tracking
- no source tracking expansion
- no publication
- no Git mutation by the agent

## 31. Recommended Next Ticket

After P9.5, continue the P9 foundation parallel queue if not already complete:

- P9.2 - External Source License / Trust Intake Model.
- P9.3 - External Source Inspection Permission Gate.
- P9.4 - External Tool Execution Gate Model.
- P9.6 - External Integration Rollback / Incident Protocol.

If P9.1-P9.6 are complete, the next ticket is:

- P9.R - External Integration Foundation Closure.

Recommended actual next ticket:

```text
P9.6 - External Integration Rollback / Incident Protocol, unless P9.2-P9.4 are still missing.
```

Do not start P9.6. Do not start P9.R. Do not start P10. Do not start P11. Do not start P12. Do not start P13. Do not start P14.

## 32. Final Verdict

| Question | Answer |
| --- | --- |
| What did P9.5 create? | `0_architecture/governance/agent_platform_external_tool_vendor_fork_wrapper_submodule_decision_model.md`. |
| Was P9.0 present? | Yes, at `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`. |
| Which adoption modes were defined? | `AdoptAsVendorCode`, `AdoptAsSubmodule`, `WrapExistingSource`, `ForkAndPatch`, `ImportReferenceOnly`, `DeferAfterAudit`, and `RejectForBoundaryMismatch`. |
| What ExternalToolAdoptionModeDecisionModel was defined? | A gated governance model from candidate identification through implementation authorization. |
| What AdoptionModeDecision contract was defined? | A record with candidate, path, license, dependency, source, execution, adapter, rollback, security, product, Git, options, selected/rejected modes, rationale, approval, follow-up, blocked action, limitation, and stop-rule fields. |
| What AdoptionModeStatus vocabulary was defined? | `not_started`, `path_only_metadata`, `pending_license_trust`, `pending_source_inspection_gate`, `pending_dependency_review`, `pending_execution_gate`, `pending_adapter_boundary`, `pending_rollback_incident`, `candidate_for_decision`, `selected_for_future_implementation`, `deferred`, `rejected`, `blocked`, `out_of_scope`. |
| What evidence package requirements were defined? | Root/path, license/trust, source inspection authorization, source/dependency/runtime/side-effect/security reviews, execution gate, adapter boundary, rollback/incident, product/Git boundary, and human approval refs. |
| What VendorCodeCandidate model was defined? | Vendoring requires license compatibility, low dependency risk, stable source, low patch volume, auditability, rollback plan, and explicit approval. |
| What SubmoduleCandidate model was defined? | Submodule use requires upstream-tracking need, reproducibility, isolation, workflow acceptance, security review, and rollback plan. |
| What WrapperCandidate model was defined? | Wrapping is often preferred when interface stability, isolation, execution boundary, I/O clarity, rollback simplicity, and adapter boundary are strong. |
| What ForkAndPatchCandidate model was defined? | Forking requires patch necessity, compatible license, ownership, divergence plan, security review, and explicit approval. |
| What ImportReferenceOnly model was defined? | Reference-only use is for architecture/evidence value without runtime or dependency adoption. |
| What DeferAfterAudit model was defined? | Defer when gates/evidence are incomplete or risks remain unresolved. |
| What RejectForBoundaryMismatch model was defined? | Reject when license, dependency, runtime, security, credential, product, repo, maintenance, autonomy, or value boundaries do not fit. |
| What tool-class default guidance was defined for Graphify? | Wrapper or import/reference-only depending on P10; execution requires P10 gates. |
| What tool-class default guidance was defined for Hermes? | Wrapper or submodule candidate only after P11 audit; runtime deferred until gate. |
| What tool-class default guidance was defined for GBrain/GStack? | Wrapper/submodule/vendor candidates only after P12 audit; memory/skill execution gated. |
| What tool-class default guidance was defined for ECC-main? | Reference/component candidate only after P13; full runtime unlikely by default. |
| What tool-class default guidance was defined for OpenCode? | H0 manual harness / future wrapper only after explicit gate. |
| What gate chain is required before implementation? | Path normalization -> license/trust intake -> source inspection gate -> source/dependency/runtime audit -> execution gate -> adapter boundary -> rollback/incident posture -> adoption mode decision -> human approval -> implementation authorization. |
| Which future tickets must consume P9.5? | P10, P11.4, P12.5, P12.6, P13.5, and P14.5. |
| Did P9.5 inspect `4_external/sources`? | No. |
| Did P9.5 list `4_external/sources`? | No. |
| Did P9.5 inspect/list/import/execute/configure/adopt GStack? | No. |
| Did P9.5 inspect external source contents? | No. |
| Did P9.5 approve source review? | No. |
| Did P9.5 approve dependency review? | No. |
| Did P9.5 approve execution? | No. |
| Did P9.5 adopt, vendor, fork, wrap, submodule, patch, move, or rename external code? | No. |
| Did P9.5 create symlinks or submodules? | No. |
| Did P9.5 modify `.gitignore` or `.graphifyignore`? | No. |
| Did P9.5 activate providers/API/MCP? | No. |
| Did P9.5 inspect product/Siamese source? | No. |
| Did P9.5 mutate Git? | No. |
| What is the next recommended ticket? | P9.6 - External Integration Rollback / Incident Protocol, unless P9.2-P9.4 are still missing. |
