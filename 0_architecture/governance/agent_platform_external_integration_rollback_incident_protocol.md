# External Integration Rollback / Incident Protocol

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | External Integration Rollback / Incident Protocol |
| Ticket | P9.6 |
| Status | Accepted external integration rollback / incident protocol |
| Date | 2026-07-07 |
| Scope | Governance and security protocol for rollback planning, containment decisioning, incident routing, recovery, evidence retraction, source-tracking reversal planning, generated artifact cleanup planning, dependency removal planning, adapter disabling planning, vendor/fork/submodule/wrapper reversal planning, and human escalation for external integration risk. |
| Authority | Rollback/incident governance protocol only, not automatic rollback, not automatic quarantine, not automatic deletion, not Git mutation, not external tool execution, not external source inspection, not dependency removal, not source tracking mutation, not generated artifact cleanup execution, not adapter disabling execution, not provider/auth/API/MCP activation, not credential use, not tool execution, not agent execution, not live connector activation, not Graphify execution/rerun/adoption, not Hermes execution/adoption/runtime, not GBrain/GStack execution/adoption/runtime, not ECC-main execution/adoption/runtime, not OpenCode execution/integration, not product/Siamese source inspection, not source loading, not vector DB implementation, not embedding generation, not graph DB implementation, not persistence, not generated output tracking activation, not source tracking expansion activation, not publication, and not Cognitive Semantic System substrate selection. |
| Related documents | P9.0 at `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`; P9.1 if present; P9.2 if present; P9.3 if present; P9.4 if present; P9.5 if present; P8.R; P8.1; P8.5; P7.R; P6.6; S-03; S-04; README.md; `.gitignore`; `.graphifyignore`. |
| Output | rollback / incident protocol ready |
| Target file | `0_architecture/governance/agent_platform_external_integration_rollback_incident_protocol.md` |
| Result markers | `external_integration_rollback_incident_protocol_ready`; `rollback_incident_model_defined`; `external_tool_containment_model_defined`; `repo_contamination_response_model_defined`; `human_escalation_required_for_remediation`; `no_automatic_rollback`; `no_git_mutation`; `no_external_execution` |

## 2. Purpose

P9 opens the External Integration Foundation phase. P9 changes external tool posture from candidate-only to integrable-under-gate.

P9.6 defines rollback and incident posture before real integrations proceed. It defines how external integration failures are classified, how contamination is identified as metadata, how containment decisions are recorded, how rollback plans are specified, and how human escalation is required.

P9.6 does not execute rollback or remediation. P9.6 does not mutate Git. P9.6 does not delete files. P9.6 does not quarantine files. P9.6 does not inspect external source contents, license files, dependency manifests, lockfiles, package metadata, product/Siamese source, raw generated outputs, secrets, credentials, provider configs, token stores, browser auth, local credential stores, API keys, or runtime state.

## 3. Current Posture

AGENT PLATFORM is post-P8. P8 closed MVP-0 as manual, local, non-executing workflow support. P9.0 is required before P9.6 and is present at the corrected path `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`.

External tools are integrable under gate, not automatically adopted. Rollback and incident posture is required before P10-P13 integrations. P9.6 is a governance/security protocol. P9.6 does not inspect source. P9.6 does not approve execution. P9.6 does not perform rollback.

Human approval is required for remediation. Git remains manual and under user authority. P9.6 may describe remediation records and future manual routes, but it may not perform remediation.

## 4. Inputs Reviewed

Inputs are consumed as governance/path/class metadata only. P9.6 does not inspect external source contents, license files, dependency manifests, lockfiles, package metadata, product source, raw generated outputs, secrets, credentials, configs, token stores, browser auth, local credential stores, API keys, or runtime state.

| input | present | consumed_as | rollback_incident_relevance | limitations | pending_alignment |
| --- | --- | --- | --- | --- | --- |
| P9.0 External Tool Integration Charter / Adopt-Not-Rebuild Boundary | Yes, corrected path | Required governance charter | Establishes integrable-under-gate posture, canonical external root, no execution/source inspection, and P9.6 route. | Prompt-listed legacy P9.0 path without `p9_` prefix is absent; corrected path is used. | None. |
| P9.1 External Source Root Normalization | Yes | Optional P9 peer | Confirms `4_external/sources` canonical root and `external/sources` legacy drift. | P9.6 does not modify P9.1. | None. |
| P9.2 External Source License / Trust Intake Model | Yes | Optional P9 peer | Supplies license/trust/dependency/supply-chain incident trigger context. | P9.6 does not approve license, trust, or dependencies. | None. |
| P9.3 External Source Inspection Permission Gate | Yes | Optional P9 peer | Supplies unauthorized source inspection incident context. | P9.6 does not inspect source. | None. |
| P9.4 External Tool Execution Gate Model | Yes | Optional P9 peer | Supplies unauthorized execution incident context and exact-scope execution boundary. | P9.6 does not approve execution. | None. |
| P9.5 Vendor / Fork / Wrapper / Submodule Decision Model | No at prompt-listed path | Optional P9 peer | Would supply concrete adoption-mode rollback routes. | A similarly named untracked peer file was not consumed because it is outside the prompt-listed P9.5 input. | `pending_P9.5_vendor_fork_wrapper_submodule_decision_alignment` |
| P8.R Platform MVP Readiness Closure | Yes at accepted path | Post-P8 closure baseline | Confirms MVP-0 manual/non-executing closure and no runtime/external adoption/Git readiness. | Prompt-listed shorter alias is absent; accepted path is `agent_platform_p8_platform_mvp_readiness_closure.md`. | Alias drift to reconcile in P9.R if needed. |
| P8.1 External Source Inventory / Classification | Yes | Candidate inventory metadata | Supplies Graphify, GBrain, GStack, Hermes, OpenCode candidate classes and blocked postures. | Earlier legacy path assumptions are superseded by P9.1/P9.0. | None. |
| P8.5 Security / Activation Gate Model | Yes | Gate metadata | Supplies activation levels, external inspection gates, human approval, and Git boundary. | No enforcement activated. | None. |
| P6.6 Cognitive Semantic System Substrate Decision / Defer Record | Yes | Substrate defer baseline | Keeps graph/vector/GBrain/Graphify substrate decisions deferred. | No substrate selected. | None. |
| P7.R Manual Agentic Workflow Planning Closure | Yes | Manual workflow closure | Preserves manual bridge, review, integration, no runtime, no Git mutation. | No P7 work started. | None. |
| S-03 Local-only / Secrets / Credentials Policy | Yes | Security policy | Supplies secret/credential/local-only incident handling and safe metadata rules. | No secret/credential inspection. | None. |
| S-04 Tool / Shell / Network / MCP Execution Policy | Yes | Security policy | Supplies execution, package manager, provider/API/MCP, network, external execution, and Git risk rules. | No execution performed. | None. |
| README.md | Yes | Repository orientation | Confirms AGENT PLATFORM workspace. | No runtime effect. | None. |
| `.gitignore` | Yes | Ignore posture metadata | Confirms `4_external/sources`, generated outputs, products, datasets, models, secrets, credentials, and provider/auth patterns are local-only/ignored. | Not modified; ignore is not security. | None. |
| `.graphifyignore` | Yes | Graphify boundary metadata | Confirms default-deny Graphify boundary and explicit `4_external/` exclusion. | Not modified; not permission to run Graphify. | None. |
| `4_external/sources` path metadata | Yes | Path metadata only | Canonical external root exists. | No listing, traversal, or content inspection. | None. |
| `external/sources` legacy path metadata | No | Legacy/path-drift metadata | Legacy root is absent and non-canonical. | Absence is not a blocker. | None. |
| `4_external/sources/gstack-main` path metadata | Yes | Path/class metadata only | Known GStack path exists. | No listing, source inspection, import, execution, configuration, adoption, or dependency approval. | None. |

## 5. Dependency Posture

| dependency | required_for_P9.6 | consumed_posture | rollback_incident_implication | blocker_if_absent |
| --- | --- | --- | --- | --- |
| P9.0 | Yes | Present at corrected path. | Defines P9.6 authority and no-execution/no-inspection baseline. | STOP with `p9_0_missing_external_tool_integration_charter`. |
| P9.1 | No, parallel peer | Present. | Canonical root and legacy path drift incidents can be classified precisely. | If absent, mark `pending_P9.1_external_source_root_normalization_alignment`. |
| P9.2 | No, parallel peer | Present. | License/trust/dependency rollback triggers are available as model concepts. | If absent, mark `pending_P9.2_license_trust_intake_alignment`; triggers remain conservative. |
| P9.3 | No, parallel peer | Present. | Source inspection incident triggers align with source permission gate. | If absent, mark `pending_P9.3_external_source_inspection_permission_gate_alignment`; triggers remain conservative. |
| P9.4 | No, parallel peer | Present. | Execution incident triggers align with external execution gate. | If absent, mark `pending_P9.4_external_tool_execution_gate_alignment`; triggers remain conservative. |
| P9.5 | No, parallel peer | Absent at expected path. | Vendor/fork/wrapper/submodule rollback routes remain generic templates. | Mark `pending_P9.5_vendor_fork_wrapper_submodule_decision_alignment`. |
| P8.R | Baseline | Present at accepted path. | Confirms post-P8 non-executing manual baseline. | If absent, record limitation; P9.0 remains P9.6 hard prerequisite. |
| P8.1 | Baseline | Present. | Supplies candidate families and candidate-only posture. | If absent, candidate-specific matrix becomes limited. |
| P8.5 | Baseline | Present. | Supplies activation gate and human approval vocabulary. | If absent, security/activation alignment limitation. |
| S-03 | Baseline | Present. | Governs secret/credential/local-only incidents. | If absent, secure incident handling limitation. |
| S-04 | Baseline | Present. | Governs execution, package, network, MCP, provider, Git, external execution incidents. | If absent, execution incident handling limitation. |

P9.R must reconcile all pending alignments before P10+ external integration work proceeds.

## 6. ExternalIntegrationRollbackIncidentProtocol Object Model

`ExternalIntegrationRollbackIncidentProtocol` is the canonical protocol object for external integration rollback and incident posture.

| Field | Meaning |
| --- | --- |
| `protocol_id` | Stable identifier for this rollback/incident protocol. |
| `protocol_scope` | Scope of governed external integration remediation planning. |
| `governed_external_root` | Canonical external root: `4_external/sources`. |
| `legacy_root_refs` | Legacy/path-drift references, including `external/sources`. |
| `covered_tool_families` | Graphify, Hermes, GBrain, GStack, ECC-main, OpenCode, Codegraph, provider/API/MCP, and future external tools. |
| `covered_adoption_modes` | reference, source review, vendor, fork, wrapper, adapter, submodule, dependency, runtime, reject, defer. |
| `covered_integration_surfaces` | Source, license, dependencies, execution, adapters, generated outputs, source tracking, Git, product/Siamese, provider/API/MCP, credentials, runtime, persistence, telemetry. |
| `rollback_triggers` | `RollbackTrigger` records. |
| `incident_triggers` | Trigger records that route to `ExternalToolIncidentRecord`. |
| `contamination_surfaces` | `RepoContaminationSurface` records. |
| `containment_decisions` | `ContainmentDecision` records. |
| `quarantine_decisions` | `QuarantineDecision` records. |
| `rollback_plan_templates` | `RollbackPlan` and adoption-mode-specific route templates. |
| `recovery_decisions` | `RecoveryDecision` records. |
| `human_escalation_requirements` | `HumanEscalationRequirement` records. |
| `retention_requirements` | `RetentionRef`-compatible retention posture. |
| `evidence_requirements` | `EvidenceRef` and `EvidenceRetractionRecord` requirements. |
| `validation_requirements` | `ValidationRef` requirements for future validation, not execution. |
| `security_requirements` | `SecurityRef` requirements and S-03/S-04 constraints. |
| `approval_requirements` | `ApprovalRef` requirements; ApprovalRef is not approval. |
| `limitations` | Known absences, pending alignments, and blocked assumptions. |

The protocol is a governance model. It is not an executable rollback engine.

## 7. ExternalIntegrationChangeRecord

`ExternalIntegrationChangeRecord` records what a future external integration changed or proposed to change.

| Field | Meaning |
| --- | --- |
| `change_record_id` | Stable change record id. |
| `candidate_ref` | Candidate ref, such as GraphifyRef, GBrainCandidateRef, GStackCandidateRef, HermesCandidateRef, ECCCandidateRef, or OpenCodeHarnessCandidateRef. |
| `integration_project_ref` | P10-P13 or later integration project reference. |
| `ticket_ref` | Ticket that proposed or approved the change. |
| `adoption_mode` | Vendor, fork, wrapper, submodule, dependency, adapter, runtime, reference-only, reject, or defer. |
| `changed_paths` | Safe path metadata for changed internal files. |
| `generated_paths` | Generated artifact path metadata only. |
| `external_paths` | External path metadata only; no source contents. |
| `dependency_changes` | Dependency change metadata; no manifest/lockfile content in P9.6. |
| `config_changes` | Config change metadata; no secret/credential values. |
| `adapter_changes` | Adapter path/ref metadata only. |
| `runtime_changes` | Runtime change metadata; runtime activation remains blocked. |
| `source_tracking_changes` | Source tracking metadata only; no tracking mutation. |
| `generated_output_changes` | Generated output metadata only; no raw output inspection. |
| `git_state_metadata` | Git status/diff refs as safe metadata, not Git approval. |
| `human_approval_refs` | ApprovalRef metadata required for remediation. |
| `evidence_refs` | EvidenceRef metadata. |
| `validation_refs` | ValidationRef metadata; no validation execution by P9.6. |
| `security_refs` | SecurityRef metadata. |
| `rollback_refs` | RollbackRef metadata. |
| `incident_refs` | IncidentRef metadata. |
| `limitations` | Known unknowns and blocked content. |

ChangeRecord is metadata only. It does not mutate paths and does not inspect content.

## 8. RepoContaminationSurface

`RepoContaminationSurface` is the canonical repo contamination surface object.

Surface types:

| surface_type | Meaning |
| --- | --- |
| `external_source_contamination` | External source content enters an unauthorized surface. |
| `vendored_code_contamination` | Vendored external code appears without approval. |
| `submodule_contamination` | Submodule state/config appears without approval. |
| `wrapper_contamination` | Wrapper code/config appears without gate. |
| `adapter_contamination` | Adapter code/config appears without gate. |
| `dependency_contamination` | Dependency references appear without approval. |
| `package_manager_contamination` | Package-manager output, cache, lock, or script effects appear without gate. |
| `generated_artifact_contamination` | Generated artifacts are unsafe, unclassified, or mis-promoted. |
| `Graphify_output_contamination` | Graphify output is raw, stale, unsafe, or treated as authority. |
| `source_tracking_contamination` | Source tracking expands or misclassifies without approval. |
| `Git_state_contamination` | Git index/history/status indicates unsafe mutation or staging risk. |
| `provider_config_contamination` | Provider/auth config appears in unauthorized surface. |
| `credential_secret_contamination` | Secret/credential material is exposed or staged. |
| `product_source_contamination` | Product/Siamese source crosses boundary without product gate. |
| `runtime_state_contamination` | Runtime state, logs, processes, caches, or state files appear without gate. |
| `persistence_contamination` | Database, vector, graph, ontology, or storage artifacts appear without gate. |
| `telemetry_event_contamination` | Telemetry, event stream, or network traces appear without gate. |
| `unknown_contamination` | Unknown side effects or unexplained artifacts. |

Fields:

| Field | Meaning |
| --- | --- |
| `surface_id` | Stable contamination surface id. |
| `surface_type` | One of the surface types above. |
| `affected_paths_metadata` | Safe path metadata only. |
| `affected_artifacts_metadata` | Safe generated/artifact metadata only. |
| `detected_by` | Human, reviewer, validation ref, security ref, Git metadata, or governance review. |
| `detection_evidence_refs` | EvidenceRef-compatible metadata. |
| `severity` | `IncidentSeverity`. |
| `containment_required` | Whether containment decision is required. |
| `rollback_required` | Whether rollback planning is required. |
| `incident_required` | Whether incident record is required. |
| `human_escalation_required` | Whether human escalation is required. |
| `limitations` | Unknowns and blocked content. |

## 9. Incident Severity Model

`IncidentSeverity` is the canonical severity vocabulary.

| IncidentSeverity | Meaning |
| --- | --- |
| `informational` | Low-risk metadata-only issue; no contamination or side effect known. |
| `low` | Bounded issue with no sensitive exposure, no execution, no Git mutation, no product/external boundary breach. |
| `medium` | Review-required issue with potential license, generated-output, source-tracking, or dependency drift. |
| `high` | Significant contamination, unauthorized dependency state, source tracking violation, Git mutation risk, product exposure risk, or unknown side effects. |
| `critical` | Unauthorized execution, provider/API/MCP/auth activation, credential/secret exposure, product source exposure, network/telemetry surprise, or runtime activation. |
| `emergency_stop` | Immediate stop condition with active credential/secret exposure, uncontrolled execution, live connector/provider/MCP activation, autonomous/Cadence behavior, or broad unknown side effects. |

Severity rules:

| Rule | Severity |
| --- | --- |
| Secret/credential exposure | `critical` or `emergency_stop`. |
| Unexpected Git mutation | `high` or `critical`. |
| Product/Siamese source exposure | `high` or `critical`. |
| Provider/auth/API/MCP activation without gate | `critical`. |
| External tool execution without gate | `critical`. |
| Dependency installation without gate | `high` or `critical`. |
| License mismatch | `medium` or `high` depending on scope. |
| Generated output contamination | `medium` or `high`. |
| Source tracking violation | `high`. |
| Telemetry/network discovery | `high` or `critical`. |
| Cadence/autonomous behavior activation | `critical`. |
| Unknown side effects | `high` until reviewed. |

## 10. RollbackTrigger Model

`RollbackTrigger` is the canonical rollback trigger object.

| Field | Meaning |
| --- | --- |
| `trigger_id` | Stable trigger id. |
| `trigger_type` | Trigger type vocabulary value. |
| `trigger_source` | Evidence, review, Git metadata, security report, human report, validation ref, or incident ref. |
| `affected_candidate_ref` | Candidate or tool family affected. |
| `affected_change_record_ref` | Related `ExternalIntegrationChangeRecord`. |
| `severity` | `IncidentSeverity`. |
| `required_containment` | Required containment decision reference. |
| `required_rollback_plan` | Required rollback plan reference. |
| `required_incident_route` | Required incident route reference. |
| `required_human_approval` | Required `HumanEscalationRequirement` / ApprovalRef. |
| `stop_required` | Whether work must stop immediately. |
| `limitations` | Unknowns and blocked content. |

Trigger types:

| trigger_type | Meaning |
| --- | --- |
| `unauthorized_external_source_inspection` | Source contents inspected without gate. |
| `unauthorized_external_tool_execution` | External tool executed without gate. |
| `unauthorized_dependency_installation` | Dependency installed without gate. |
| `unauthorized_package_manager_use` | Package manager used without gate. |
| `license_mismatch` | License incompatible, unverified, or changed. |
| `dependency_license_conflict` | Dependency license conflicts with intended use. |
| `malicious_dependency` | Dependency suspected malicious or compromised. |
| `postinstall_side_effect` | Package lifecycle hook caused side effects. |
| `unexpected_network_call` | Network behavior occurred or is detected unexpectedly. |
| `unexpected_provider_auth` | Provider/auth state used or exposed unexpectedly. |
| `unexpected_MCP_transport` | MCP transport started/connected unexpectedly. |
| `telemetry_discovery` | Telemetry/event behavior discovered without gate. |
| `unexpected_persistence` | Persistence, DB, vector, graph, cache, or runtime state appeared without gate. |
| `generated_artifact_contamination` | Generated output is unsafe, unreviewed, or promoted incorrectly. |
| `source_tracking_violation` | Source tracking expanded or changed without gate. |
| `Git_mutation_violation` | Git staging/history/branch/stash/mutation occurred without user authority. |
| `secret_exposure` | Secret value exposed or potentially exposed. |
| `credential_exposure` | Credential material exposed or potentially exposed. |
| `provider_config_exposure` | Provider configuration exposed or copied. |
| `product_source_exposure` | Product/Siamese source crossed boundary. |
| `Graphify_authority_drift` | Graphify treated as authority or source of truth. |
| `Hermes_runtime_drift` | Hermes runtime/Cadence/orchestration boundary drift. |
| `GBrain_runtime_drift` | GBrain runtime, persistence, retrieval, or memory boundary drift. |
| `GStack_runtime_drift` | GStack execution, bootstrap, dependency, or runtime boundary drift. |
| `ECC_autonomy_drift` | ECC-main agent OS/autonomy boundary drift. |
| `OpenCode_execution_drift` | OpenCode executed by AGENT PLATFORM or adapter execution drift. |
| `Cadence_activation_drift` | Scheduler/always-on/Cadence behavior activated. |
| `unknown_side_effect` | Unknown side effect requires high-severity review. |

## 11. ExternalToolIncidentRecord

`ExternalToolIncidentRecord` is the canonical incident record object.

| Field | Meaning |
| --- | --- |
| `incident_id` | Stable incident id. |
| `incident_title` | Human-readable incident title. |
| `incident_type` | Incident type vocabulary value. |
| `incident_severity` | `IncidentSeverity`. |
| `candidate_ref` | Candidate/tool reference. |
| `affected_scope` | Exact affected governance/project/surface scope. |
| `affected_paths_metadata` | Safe path metadata only. |
| `affected_records` | Change, evidence, validation, security, approval, retention, rollback, and incident records. |
| `trigger_refs` | Related `RollbackTrigger` refs. |
| `contamination_surface_refs` | Related `RepoContaminationSurface` refs. |
| `immediate_stop_required` | Whether work must stop immediately. |
| `unsafe_content_repetition_blocked` | Whether unsafe content must not be repeated in records. |
| `containment_decision_ref` | Related `ContainmentDecision`. |
| `rollback_plan_ref` | Related `RollbackPlan`. |
| `incident_route_ref` | Related `IncidentRoute`. |
| `recovery_decision_ref` | Related `RecoveryDecision`. |
| `human_escalation_required` | Whether human escalation is required. |
| `evidence_refs` | EvidenceRef metadata. |
| `validation_refs` | ValidationRef metadata. |
| `security_refs` | SecurityRef metadata. |
| `approval_refs` | ApprovalRef metadata. |
| `retention_refs` | RetentionRef metadata. |
| `rollback_refs` | RollbackRef metadata. |
| `limitations` | Unknowns and blocked content. |

Incident types:

| incident_type | Meaning |
| --- | --- |
| `license_incident` | License mismatch, unclear license, or obligation conflict. |
| `dependency_incident` | Dependency, package manager, lockfile, package script, or supply-chain issue. |
| `execution_incident` | Unauthorized tool/external execution or side effect. |
| `source_boundary_incident` | Unauthorized source inspection/loading/copying. |
| `security_incident` | Security posture or exposure issue. |
| `credential_secret_incident` | Secret, credential, `.env`, provider config, token, browser auth, local credential store, or API key issue. |
| `product_boundary_incident` | Product/Siamese source or behavior boundary issue. |
| `generated_output_incident` | Generated/raw output contamination or misclassification. |
| `source_tracking_incident` | Source tracking expansion or reversal issue. |
| `Git_boundary_incident` | Git staging/history/branch/stash/mutation issue. |
| `runtime_activation_incident` | Runtime, persistence, scheduler, Cadence, or autonomous behavior issue. |
| `provider_auth_api_mcp_incident` | Provider/auth/API/MCP/network/transport issue. |
| `persistence_incident` | Database, vector, graph, cache, or storage issue. |
| `telemetry_network_incident` | Telemetry, event stream, network, or remote call issue. |
| `autonomy_cadence_incident` | Automatic orchestration, scheduler, Cadence, task/handoff, or reviewer assignment issue. |
| `unknown_incident` | Unknown issue requiring review. |

## 12. ContainmentDecision Model

`ContainmentDecision` is the canonical containment decision object.

| Field | Meaning |
| --- | --- |
| `containment_decision_id` | Stable containment decision id. |
| `incident_ref` | Related incident. |
| `containment_status` | Containment status value. |
| `containment_reason` | Reason for containment decision. |
| `allowed_manual_actions` | Manual actions that may be considered after approval. |
| `blocked_actions` | Actions blocked until explicit approval. |
| `quarantine_required` | Whether quarantine planning is required. |
| `rollback_required` | Whether rollback planning is required. |
| `human_approval_required` | Human approval requirement. |
| `security_review_required` | Security review requirement. |
| `governance_review_required` | Governance review requirement. |
| `validation_review_required` | Validation review requirement. |
| `limitations` | Unknowns and blocked content. |

Containment status values:

| containment_status | Meaning |
| --- | --- |
| `contain_metadata_only` | Record containment posture only. |
| `stop_and_hold` | Stop work and hold further actions pending review. |
| `quarantine_plan_required` | A quarantine plan is required before manual steps. |
| `rollback_plan_required` | A rollback plan is required before manual steps. |
| `human_escalation_required` | Human owner must decide next action. |
| `security_review_required` | Security review is required. |
| `governance_review_required` | Governance review is required. |
| `validation_review_required` | Validation review is required. |
| `blocked_until_review` | No remediation may proceed until review. |
| `no_action_required` | No containment required after review. |
| `unknown` | Unknown; block until reviewed. |

ContainmentDecision is a decision record. It does not execute containment.

## 13. QuarantineDecision Model

`QuarantineDecision` is the canonical quarantine decision object.

| Field | Meaning |
| --- | --- |
| `quarantine_decision_id` | Stable quarantine decision id. |
| `affected_candidate_ref` | Candidate/tool reference. |
| `affected_paths_metadata` | Safe affected path metadata. |
| `quarantine_reason` | Reason quarantine may be needed. |
| `quarantine_mode` | Quarantine mode vocabulary value. |
| `allowed_manual_steps` | Manual steps that may be proposed after approval. |
| `forbidden_automatic_steps` | Automatic steps that remain blocked. |
| `human_approval_required` | Human approval requirement. |
| `rollback_dependency` | Rollback plan dependency. |
| `incident_dependency` | Incident route dependency. |
| `limitations` | Unknowns and blocked content. |

Quarantine modes:

| quarantine_mode | Meaning |
| --- | --- |
| `no_quarantine_needed` | No quarantine needed after review. |
| `logical_quarantine_metadata_only` | Mark as quarantined in metadata only. |
| `manual_quarantine_recommended` | Manual quarantine may be recommended after approval. |
| `branch_isolation_recommended` | Manual branch isolation may be considered by the user. |
| `generated_output_hold_recommended` | Generated outputs should be held pending classification. |
| `dependency_hold_recommended` | Dependency changes should be held pending review. |
| `external_tool_hold_recommended` | External tool work should be held pending review. |
| `blocked_until_human_decision` | No action until human decision. |

P9.6 does not move files or quarantine automatically.

## 14. RollbackPlan Model

`RollbackPlan` is the canonical rollback plan object.

| Field | Meaning |
| --- | --- |
| `rollback_plan_id` | Stable rollback plan id. |
| `incident_ref` | Related incident. |
| `rollback_scope` | Exact scope of proposed rollback. |
| `rollback_mode` | Rollback mode vocabulary value. |
| `affected_change_records` | Related `ExternalIntegrationChangeRecord` refs. |
| `candidate_ref` | Candidate/tool reference. |
| `affected_paths_metadata` | Safe affected path metadata. |
| `manual_steps` | Manual steps for future approval; not executed by P9.6. |
| `forbidden_automatic_steps` | Steps P9.6 must not execute. |
| `required_preconditions` | Evidence, security, validation, backup/snapshot, and human approval preconditions. |
| `required_human_approval` | Human approval requirement. |
| `required_backup_or_snapshot_review` | Backup/snapshot review requirement before destructive remediation. |
| `required_security_review` | Security review requirement. |
| `required_validation_review` | Validation review requirement. |
| `expected_result` | Intended result after future manual remediation. |
| `rollback_risks` | Risks introduced by rollback. |
| `rollback_limitations` | Known limitations. |
| `verification_targets` | Future validation targets; not executed by P9.6. |

Rollback modes:

| rollback_mode | Meaning |
| --- | --- |
| `no_rollback_needed` | No rollback required after review. |
| `metadata_retraction_only` | Retract or supersede metadata/evidence only. |
| `manual_path_reversal_plan` | Future manual path reversal plan. |
| `manual_dependency_removal_plan` | Future manual dependency removal plan. |
| `manual_vendor_removal_plan` | Future manual vendor removal plan. |
| `manual_submodule_removal_plan` | Future manual submodule removal plan. |
| `manual_wrapper_disable_plan` | Future manual wrapper disable plan. |
| `manual_adapter_disable_plan` | Future manual adapter disable plan. |
| `manual_generated_artifact_cleanup_plan` | Future manual generated artifact cleanup plan. |
| `manual_source_tracking_reversal_plan` | Future manual source tracking reversal plan. |
| `manual_Git_revert_plan` | Future user-owned Git history/worktree remediation plan. |
| `blocked_until_human_decision` | No rollback action until human decision. |

RollbackPlan is not rollback execution. It may describe manual Git remediation conceptually but must not execute or recommend immediate mutation in P9.6.

## 15. Adoption-Mode-Specific Rollback Routes

These route models are templates only. P9.6 does not edit vendor, submodule, wrapper, adapter, dependency, fork, or source state.

| Route model | Required fields |
| --- | --- |
| `VendorRemovalPlan` | `vendored_paths_metadata`, `removal_reason`, `notice_retention_requirement`, `dependency_cleanup_requirement`, `manual_removal_steps`, `human_approval_required`. |
| `SubmoduleRemovalPlan` | `submodule_path_metadata`, `submodule_config_metadata`, `removal_reason`, `manual_removal_steps`, `human_approval_required`. |
| `ForkReversalPlan` | `fork_ref_metadata`, `divergence_summary`, `reversal_reason`, `manual_reversal_steps`, `human_approval_required`. |
| `WrapperDisableRoute` | `wrapper_paths_metadata`, `adapter_refs`, `disable_reason`, `manual_disable_steps`, `human_approval_required`. |
| `AdapterDisableRoute` | `adapter_paths_metadata`, `execution_gate_refs`, `disable_reason`, `manual_disable_steps`, `human_approval_required`. |
| `DependencyRemovalPlan` | `dependency_refs`, `dependency_manifest_refs`, `lockfile_refs`, `removal_reason`, `manual_removal_steps`, `human_approval_required`. |

P9.5 is absent at the expected path, so these routes remain generic until P9.5 or P9.R reconciles adoption-mode decisions.

## 16. GeneratedArtifactCleanupPlan

`GeneratedArtifactCleanupPlan` is the canonical generated artifact cleanup plan object.

| Field | Meaning |
| --- | --- |
| `cleanup_plan_id` | Stable cleanup plan id. |
| `generated_artifact_refs` | Generated artifact refs. |
| `generated_artifact_paths_metadata` | Safe generated path metadata only. |
| `generation_source` | Tool/process/source that produced artifact, if known. |
| `classification_status` | Classified, unclassified, unsafe, unknown, or hold status. |
| `cleanup_reason` | Reason cleanup may be needed. |
| `retention_required` | Whether retention is required before cleanup. |
| `deletion_required` | Whether deletion may be required after approval. |
| `hold_required` | Whether artifact hold is required. |
| `manual_cleanup_steps` | Future manual cleanup steps; not executed by P9.6. |
| `human_approval_required` | Human approval requirement. |
| `limitations` | Unknowns and blocked content. |

P9.6 does not delete generated artifacts. Generated outputs must be classified before cleanup. Raw generated outputs must not be inspected unless a future gate allows. Unsafe content must not be repeated.

## 17. SourceTrackingReversalPlan

`SourceTrackingReversalPlan` is the canonical source tracking reversal plan object.

| Field | Meaning |
| --- | --- |
| `reversal_plan_id` | Stable reversal plan id. |
| `source_tracking_refs` | Source tracking refs involved. |
| `affected_tracking_records` | Affected tracking records. |
| `reversal_reason` | Reason reversal is needed. |
| `manual_reversal_steps` | Future manual steps; not executed by P9.6. |
| `required_evidence_refs` | EvidenceRefs required before reversal. |
| `required_human_approval` | Human approval requirement. |
| `publication_dependency` | Publication impact and blocker status. |
| `limitations` | Unknowns and blocked content. |

P9.6 does not modify source tracking. Source tracking expansion remains blocked unless later gates approve. Reversal planning is metadata only.

## 18. EvidenceRetractionRecord

`EvidenceRetractionRecord` is the canonical evidence retraction object.

| Field | Meaning |
| --- | --- |
| `retraction_id` | Stable retraction id. |
| `evidence_ref` | EvidenceRef being retracted or superseded. |
| `retraction_reason` | Reason evidence must be retracted. |
| `affected_decisions` | Decisions affected by retraction. |
| `affected_documents` | Documents affected by retraction. |
| `replacement_evidence_refs` | Replacement evidence refs if available. |
| `human_review_required` | Human review requirement. |
| `downstream_reconciliation_required` | Whether downstream reconciliation is required. |
| `limitations` | Unknowns and blocked content. |

Use when Graphify evidence is contaminated, external source review evidence is invalidated, license evidence is invalidated, dependency evidence is invalidated, generated output evidence is unsafe, or source tracking evidence is wrong.

EvidenceRetractionRecord is metadata only. Evidence supports; it does not decide.

## 19. RecoveryDecision Model

`RecoveryDecision` is the canonical recovery decision object.

| Field | Meaning |
| --- | --- |
| `recovery_decision_id` | Stable recovery decision id. |
| `incident_ref` | Related incident. |
| `recovery_status` | Recovery status vocabulary value. |
| `required_reviews` | Security, governance, validation, product, external boundary, integration, memory/context, or Git advisory reviews. |
| `required_rework` | Required future rework. |
| `required_ticket_reopen` | Tickets that must be reopened. |
| `required_gate_reopen` | Gates that must be reopened. |
| `allowed_resume_conditions` | Conditions for resuming work. |
| `blocked_resume_conditions` | Conditions that block resume. |
| `human_approval_required` | Human approval requirement. |
| `limitations` | Unknowns and blocked content. |

Recovery statuses:

| recovery_status | Meaning |
| --- | --- |
| `recovery_not_started` | Recovery not started. |
| `recovery_blocked` | Recovery blocked. |
| `recovery_requires_security_review` | Security review required. |
| `recovery_requires_governance_review` | Governance review required. |
| `recovery_requires_validation_review` | Validation review required. |
| `recovery_requires_human_decision` | Human decision required. |
| `recovery_ready_after_manual_remediation` | Resume may be considered after manual remediation and review. |
| `recovered_metadata_only` | Metadata was corrected/retracted only. |
| `rejected_for_scope` | Recovery rejected because scope is invalid or unsafe. |
| `unknown` | Unknown; block until reviewed. |

## 20. IncidentRoute / Escalation Model

`IncidentRoute` is the canonical incident route object. `HumanEscalationRequirement` is the canonical human escalation object.

| IncidentRoute field | Meaning |
| --- | --- |
| `route_id` | Stable route id. |
| `incident_type` | Incident type routed. |
| `severity_threshold` | Minimum severity for the route. |
| `required_reviewer_cells` | Reviewer cells required. |
| `required_human_owner` | Human owner required. |
| `required_documents_to_update` | Documents that may need future update. |
| `required_downstream_notifications` | Manual notification requirements. |
| `unsafe_content_handling` | Safe metadata and no-repeat handling for unsafe content. |
| `evidence_handling` | Evidence retention, retraction, and replacement handling. |
| `rollback_dependency` | Rollback plan dependency. |
| `recovery_dependency` | Recovery decision dependency. |
| `limitations` | Unknowns and blocked content. |

Required reviewer cells:

| reviewer_cell | Focus |
| --- | --- |
| `security_reviewer_cell` | Security, secrets, credentials, provider/auth/API/MCP, network, package, execution, local-only risk. |
| `governance_reviewer_cell` | Policy, authority, gate, P9/P10+ sequencing, adoption boundary. |
| `validation_reviewer_cell` | Future validation completeness; no validation execution by P9.6. |
| `product_boundary_reviewer_cell` | Product/Siamese exposure and product readiness gate. |
| `external_boundary_reviewer_cell` | External source, license, dependency, trust, source inspection, execution, adoption boundaries. |
| `integration_reviewer_cell` | Adapter/wrapper/vendor/fork/submodule/dependency integration boundaries. |
| `memory_context_reviewer_cell` | GBrain, Graphify, context, evidence, source tracking, generated output, Cognitive Semantic System boundaries. |
| `Git_advisory_reviewer_cell` | User-owned Git advisory and no mutation posture. |

Routing is manual. P9.6 does not send notifications.

## 21. Tool-Specific Incident Considerations

| tool | likely_incident_surfaces | rollback_focus | escalation_focus | blocked_automatic_actions |
| --- | --- | --- | --- | --- |
| Graphify | Generated evidence contamination, authority drift, repo map drift, raw output mishandling, rerun outside scope. | EvidenceRetractionRecord, GeneratedArtifactCleanupPlan, source tracking reversal planning. | Governance, validation, memory/context, external boundary. | No Graphify execution, rerun, adoption, authority promotion, `.graphifyignore` mutation, raw output deletion. |
| Hermes | Runtime activation, Cadence activation, orchestration side effects, UI/runtime boundary drift. | AdapterDisableRoute, WrapperDisableRoute, runtime hold metadata. | Security, governance, integration, product boundary. | No Hermes execution, import, configuration, adoption, runtime, Cadence, orchestration, provider/API/MCP. |
| GBrain | Persistence, memory ingestion, automatic retrieval, source indexing, secret/product exposure. | SourceTrackingReversalPlan, GeneratedArtifactCleanupPlan, persistence hold metadata. | Security, memory/context, product boundary, external boundary. | No GBrain execution, import, configuration, adoption, runtime, persistent memory, retrieval, graph/vector DB. |
| GStack | Skill execution, bootstrap side effects, dependency/install side effects, provider/API/MCP drift. | DependencyRemovalPlan, AdapterDisableRoute, WrapperDisableRoute, external tool hold metadata. | Security, external boundary, integration, provider/API/MCP. | No GStack execution, import, configuration, adoption, runtime, dependency install, provider/API/MCP. |
| ECC-main | Agent OS autonomy, scheduler/orchestration, tool/memory overlap, runtime side effects. | Runtime hold metadata, AdapterDisableRoute, RecoveryDecision gate reopen. | Security, governance, integration, memory/context. | No ECC-main execution, import, configuration, adoption, agent OS, scheduler, autonomy. |
| OpenCode | Harness output trust drift, automatic execution drift, adapter execution drift, Git mutation drift. | EvidenceRetractionRecord, AdapterDisableRoute, Git advisory review route. | Governance, Git advisory, validation, integration. | No OpenCode execution from AGENT PLATFORM, adapter execution, automatic task routing, automatic Git mutation. |

## 22. Gate Interaction Matrix

| gate | rollback_incident_relevance | required_before_remediation | current_status |
| --- | --- | --- | --- |
| `source_review_permission_gate` | Source boundary incident routing. | Required before any source inspection remediation. | P9.3 present; no inspection by P9.6. |
| `license_file_inspection_gate` | License incident evidence. | Required before reading license files. | Future exact gate; not opened by P9.6. |
| `dependency_manifest_inspection_gate` | Dependency incident evidence. | Required before manifest/lockfile review. | Future exact gate; not opened by P9.6. |
| `dependency_install_gate` | Dependency install incident. | Required before install/removal execution. | Blocked. |
| `external_tool_execution_gate` | Execution incident routing. | Required before any tool execution or resume. | P9.4 present; no execution by P9.6. |
| `provider_auth_api_mcp_gate` | Provider/auth/API/MCP incident routing. | Required before provider/API/MCP remediation or resume. | Blocked. |
| `telemetry_network_gate` | Network/telemetry incident routing. | Required before network/telemetry action. | Blocked. |
| `persistence_storage_gate` | Persistence incident routing. | Required before DB/vector/graph/storage action. | Blocked. |
| `adapter_design_gate` | Adapter contamination planning. | Required before adapter design changes. | Future gate. |
| `adapter_execution_gate` | Adapter execution incident. | Required before adapter execution/resume. | Blocked. |
| `vendor_fork_wrapper_submodule_decision_gate` | Adoption-mode rollback route specificity. | Required before concrete adoption-mode remediation. | P9.5 absent at expected path; pending. |
| `rollback_incident_gate` | This protocol. | Required before external integration remediation planning. | Defined by P9.6. |
| `human_approval_gate` | All risky remediation. | Required before quarantine, deletion, dependency removal, adapter disable, Git actions, resume, closure. | Manual only. |
| `Git_mutation_gate` | Git boundary incident. | Required before any Git mutation by user; not agent-owned. | User authority only; P9.6 no mutation. |
| `product_source_gate` | Product/Siamese exposure incident. | Required before product/Siamese source work. | Blocked. |
| `generated_output_tracking_gate` | Generated output contamination. | Required before tracking or promotion. | Blocked. |
| `source_tracking_gate` | Source tracking reversal/expansion. | Required before source tracking changes. | Blocked. |

## 23. Evidence / Validation / Security Interfaces

Evidence interface:

| Rule | P9.6 posture |
| --- | --- |
| Incident records must cite EvidenceRef-compatible metadata. | Required. |
| Evidence supports; it does not decide. | Preserved. |
| Unsafe content must not be repeated. | Required. |
| Evidence retraction must preserve downstream decision impact. | Required. |

Validation interface:

| Rule | P9.6 posture |
| --- | --- |
| P9.6 does not run validation. | Preserved. |
| Future validation may check rollback plan completeness and incident route completeness. | Future only. |
| Validation evaluates; governance decides. | Preserved. |

Security interface:

| Rule | P9.6 posture |
| --- | --- |
| External integration incidents are security-sensitive. | Preserved. |
| Secrets and credentials must never enter incident records. | Preserved. |
| Security constrains; it does not activate. | Preserved. |
| S-03 and S-04 remain binding. | Preserved. |

## 24. Retention / Rollback / Incident Posture

P9.6 defines rollback and incident posture. It does not execute rollback. It does not retain raw unsafe content. It does not delete generated outputs. It does not mutate source tracking. It does not mutate Git.

P9.6 requires human approval for remediation. P9.6 requires security, governance, and validation review for high-risk incidents.

| Posture | P9.6 result |
| --- | --- |
| Retention | Governance metadata only; unsafe content is not retained in the protocol. |
| Rollback | Plans and templates only; no rollback execution. |
| Incident | Records and routes only; no incident automation. |
| Generated artifacts | Cleanup planning only; no deletion or raw output inspection. |
| Source tracking | Reversal planning only; no mutation or expansion. |
| Git | Advisory/manual only; no mutation. |

## 25. Human Approval Requirements

Human approval is required before quarantine, deletion, dependency removal, vendor removal, submodule removal, wrapper disabling, adapter disabling, generated artifact cleanup, source tracking reversal, Git revert/reset/cleanup, external tool resume, execution gate reopening, provider/auth/API/MCP activation after incident, product/Siamese source work after incident, publication after incident, or closing a high/critical incident.

P9.6 itself does not approve these actions.

`HumanEscalationRequirement` fields:

| Field | Meaning |
| --- | --- |
| `escalation_id` | Stable escalation id. |
| `incident_ref` | Incident requiring escalation. |
| `severity_threshold` | Minimum severity that triggers escalation. |
| `required_human_owner` | Human owner required. |
| `required_review_cells` | Reviewer cells required before action. |
| `allowed_decision_scope` | Exact decisions the human may approve. |
| `blocked_decision_scope` | Actions still blocked unless separately approved. |
| `required_evidence_refs` | Evidence required before decision. |
| `required_security_refs` | Security refs required before decision. |
| `required_approval_refs` | ApprovalRefs required; ApprovalRef is not approval by itself. |
| `expiration_or_revisit` | When approval expires or must be revisited. |

## 26. Stop Rules

STOP if P9.0 is missing and report `p9_0_missing_external_tool_integration_charter`.

STOP if protocol work requires executing rollback, deleting files, quarantining files, mutating Git, running `git reset`, `git revert`, `git checkout`, `git clean`, or `git stash`, inspecting external source contents, opening LICENSE files under external sources, reading dependency manifests or lockfiles, package-manager commands, installing dependencies, importing or executing external tools, source loading, Graphify rerun/adoption, Hermes/GBrain/GStack/ECC/OpenCode execution or adoption, provider/auth/API/MCP activation, credential use, API/MCP calls, tool execution, agent execution, product/Siamese source inspection, raw generated output inspection, secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, validation execution, tests, CI, scripts, builds, persistence, vector DB, graph DB, embeddings, substrate selection, generated output tracking activation, source tracking expansion activation, publication, Git mutation, or work beyond rollback/incident governance model scope.

## 27. Future Validation Targets

Future validation targets, not executed:

| Target | Purpose |
| --- | --- |
| ExternalIntegrationRollbackIncidentProtocol required fields completeness | Check protocol object completeness. |
| ExternalIntegrationChangeRecord required fields completeness | Check change record shape. |
| RepoContaminationSurface vocabulary conformance | Check surface type vocabulary. |
| IncidentSeverity vocabulary conformance | Check severity values. |
| RollbackTrigger vocabulary conformance | Check trigger type values. |
| ExternalToolIncidentRecord completeness | Check incident record fields. |
| ContainmentDecision completeness | Check containment fields/statuses. |
| QuarantineDecision completeness | Check quarantine fields/modes. |
| RollbackPlan completeness | Check rollback fields/modes. |
| adoption-mode-specific rollback route completeness | Check VendorRemovalPlan, SubmoduleRemovalPlan, ForkReversalPlan, WrapperDisableRoute, AdapterDisableRoute, DependencyRemovalPlan. |
| GeneratedArtifactCleanupPlan completeness | Check generated artifact cleanup planning fields. |
| SourceTrackingReversalPlan completeness | Check source tracking reversal fields. |
| EvidenceRetractionRecord completeness | Check evidence retraction fields. |
| RecoveryDecision completeness | Check recovery statuses and fields. |
| IncidentRoute completeness | Check route fields and reviewer cells. |
| tool-specific incident matrix completeness | Check Graphify, Hermes, GBrain, GStack, ECC-main, OpenCode rows. |
| no automatic rollback invariant | Check no rollback execution is authorized. |
| no Git mutation invariant | Check no Git mutation is authorized. |
| no deletion/quarantine execution invariant | Check no deletion/quarantine is authorized. |
| no source inspection invariant | Check no source inspection is authorized. |
| human approval required invariant | Check remediation requires human approval. |
| P9.1/P9.2/P9.3/P9.4/P9.5 alignment checks | Check peer alignment. |
| P9.R reconciliation readiness check | Check closure readiness. |

## 28. Future Hardening Candidates

Future tickets, not started:

| Ticket | Purpose |
| --- | --- |
| RBINC-HARD-01 - RollbackIncidentProtocol Schema Alignment | Harden protocol schema. |
| RBINC-HARD-02 - ExternalIntegrationChangeRecord Contract | Harden integration change record. |
| RBINC-HARD-03 - RepoContaminationSurface Vocabulary Hardening | Harden contamination surface vocabulary. |
| RBINC-HARD-04 - RollbackTrigger / IncidentSeverity Contract | Harden triggers and severity. |
| RBINC-HARD-05 - Containment / Quarantine Decision Contract | Harden containment/quarantine records. |
| RBINC-HARD-06 - Adoption-Mode Rollback Route Templates | Harden vendor/fork/wrapper/submodule/dependency templates. |
| RBINC-HARD-07 - Generated Artifact Cleanup Plan Contract | Harden generated artifact cleanup planning. |
| RBINC-HARD-08 - SourceTrackingReversal / EvidenceRetraction Contract | Harden source tracking and evidence retraction. |
| RBINC-HARD-09 - Human Escalation / Recovery Decision Contract | Harden escalation and recovery. |
| RBINC-HARD-10 - P10-P13 Tool-Specific Incident Playbooks | Create future tool-specific incident playbooks after P9.R. |

## 29. Created / Modified / Not Created Register

Created:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_external_integration_rollback_incident_protocol.md` | Created as P9.6 rollback/incident governance protocol. |

Modified:

| Area | Status |
| --- | --- |
| Other files | None modified by P9.6. |

Not created / not approved:

| Area | Status |
| --- | --- |
| P9.0, P9.1, P9.2, P9.3, P9.4, P9.5, P9.R, P10+, P11+, P12+, P13+, P14+, EXT.* files | Not created by P9.6. |
| Rollback, quarantine, deletion | Not executed. |
| Git mutation, Git revert/reset/checkout/clean/stash | Not performed or approved. |
| External source adoption/content/license/dependency/lockfile/package metadata inspection | Not approved or performed. |
| Dependency approval, license approval, trust approval, execution approval | Not granted. |
| Dependency installation, package-manager command, vendor/fork/submodule/wrapper action | Not performed. |
| Adapter implementation or executable adapter | Not created. |
| Graphify execution/rerun/adoption | Not performed or approved. |
| Hermes execution/import/configuration/adoption/runtime | Not performed or approved. |
| GBrain execution/import/configuration/adoption/runtime | Not performed or approved. |
| GStack execution/import/configuration/adoption/runtime | Not performed or approved. |
| ECC-main execution/import/configuration/adoption/runtime | Not performed or approved. |
| OpenCode execution from AGENT PLATFORM | Not performed or approved. |
| Provider/auth/API/MCP activation, credential use, API calls, MCP calls | Not performed or approved. |
| Tool execution, agent execution, live connector activation | Not performed or approved. |
| Source loading, product/Siamese source inspection, raw generated output inspection | Not performed or approved. |
| Secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys | Not inspected. |
| Validation execution, tests, CI, scripts, builds | Not executed. |
| Security enforcement activation | Not created. |
| Persistence DB, vector DB, embeddings, graph DB, substrate selection | Not created or selected. |
| Telemetry, event streaming, generated output tracking activation, source tracking expansion activation, publication | Not created or approved. |

## 30. Recommended Next Ticket

After P9.6, if P9.1/P9.2/P9.3/P9.4/P9.5 are not complete, continue the foundation parallel round:

| Ticket | Status in P9.6 | Recommendation |
| --- | --- | --- |
| P9.1 - External Source Root Normalization | Present. | Do not modify from P9.6. |
| P9.2 - External Source License / Trust Intake Model | Present. | Do not modify from P9.6. |
| P9.3 - External Source Inspection Permission Gate | Present. | Do not modify from P9.6. |
| P9.4 - External Tool Execution Gate Model | Present. | Do not modify from P9.6. |
| P9.5 - Vendor / Fork / Wrapper / Submodule Decision Model | Absent at expected path. | Complete P9.5 before P9.R unless already resolved under an accepted alternate path. |

Recommended actual: P9.R - External Integration Foundation Closure, only if P9.1-P9.6 are complete and P9.5 path alignment is resolved.

Otherwise: P9.5 - Vendor / Fork / Wrapper / Submodule Decision Model, because P9.5 is absent at the expected path.

Do not start P9.R, P10+, P11+, P12+, P13+, or P14 from this ticket.

## 31. Final Verdict

| Question | Answer |
| --- | --- |
| What did P9.6 create? | `0_architecture/governance/agent_platform_external_integration_rollback_incident_protocol.md`. |
| What rollback/incident protocol was defined? | `ExternalIntegrationRollbackIncidentProtocol`, a governance/security protocol for rollback planning, containment decisions, incident routes, recovery, evidence retraction, source-tracking reversal planning, generated artifact cleanup planning, dependency removal planning, adapter disabling planning, and human escalation. |
| What rollback triggers were defined? | `RollbackTrigger` fields and trigger types including unauthorized source inspection, unauthorized execution, dependency install, package manager use, license mismatch, dependency conflict, malicious dependency, postinstall side effects, network/provider/MCP surprises, telemetry, persistence, generated artifact contamination, source tracking violation, Git mutation violation, secret/credential exposure, product source exposure, Graphify/Hermes/GBrain/GStack/ECC/OpenCode/Cadence drift, and unknown side effects. |
| What incident severities were defined? | `informational`, `low`, `medium`, `high`, `critical`, and `emergency_stop`. |
| What contamination surfaces were defined? | `RepoContaminationSurface` types for external source, vendored code, submodule, wrapper, adapter, dependency, package manager, generated artifact, Graphify output, source tracking, Git state, provider config, credential/secret, product source, runtime state, persistence, telemetry/event, and unknown contamination. |
| What containment decisions were defined? | `ContainmentDecision` with statuses including metadata-only containment, stop-and-hold, quarantine plan required, rollback plan required, human escalation required, review required, blocked until review, no action required, and unknown. |
| What quarantine decisions were defined? | `QuarantineDecision` with metadata-only, manual quarantine recommended, branch isolation recommended, generated output hold, dependency hold, external tool hold, and blocked-until-human-decision modes. |
| What rollback plan model was defined? | `RollbackPlan` with manual planning modes for metadata retraction, path reversal, dependency removal, vendor removal, submodule removal, wrapper disable, adapter disable, generated artifact cleanup, source tracking reversal, and user-owned Git remediation planning. |
| What adoption-mode-specific rollback routes were defined? | `VendorRemovalPlan`, `SubmoduleRemovalPlan`, `ForkReversalPlan`, `WrapperDisableRoute`, `AdapterDisableRoute`, and `DependencyRemovalPlan`. |
| What generated artifact cleanup plan was defined? | `GeneratedArtifactCleanupPlan` for safe metadata-only cleanup planning without deletion or raw output inspection. |
| What source tracking reversal plan was defined? | `SourceTrackingReversalPlan` for metadata-only reversal planning without source tracking mutation. |
| What evidence retraction record was defined? | `EvidenceRetractionRecord` for retracting/superseding contaminated or invalidated evidence without treating evidence as authority. |
| What recovery decision model was defined? | `RecoveryDecision` with recovery statuses from not started/blocked through review-required, ready after manual remediation, metadata-only recovery, rejected for scope, and unknown. |
| What incident routes were defined? | `IncidentRoute` and `HumanEscalationRequirement` with required security, governance, validation, product boundary, external boundary, integration, memory/context, and Git advisory reviewer cells. |
| How are Graphify incidents handled? | As generated evidence contamination, authority drift, repo map drift, raw output mishandling, or rerun scope incidents; handled through evidence retraction, generated artifact cleanup planning, source tracking reversal planning, and manual review. |
| How are Hermes incidents handled? | As runtime/Cadence/orchestration/UI-runtime boundary drift; handled through adapter/wrapper disable planning, runtime hold metadata, and security/governance/integration escalation. |
| How are GBrain incidents handled? | As persistence, memory ingestion, retrieval, source indexing, or secret/product exposure drift; handled through source tracking reversal planning, generated artifact planning, persistence hold metadata, and memory/context escalation. |
| How are GStack incidents handled? | As skill execution, bootstrap, dependency/install, or provider/API/MCP drift; handled through dependency removal planning, adapter/wrapper disable planning, and external boundary/security escalation. |
| How are ECC-main incidents handled? | As agent OS autonomy, scheduler/orchestration, tool/memory overlap, or runtime side effects; handled through runtime hold metadata, adapter disable planning, and gate reopening decisions. |
| How are OpenCode incidents handled? | As harness output trust drift, automatic execution drift, adapter execution drift, or Git mutation drift; handled through evidence retraction, adapter disable planning, and Git advisory review. |
| Was rollback executed? | No. |
| Was quarantine executed? | No. |
| Were files deleted? | No. |
| Was Git mutated? | No. |
| Was any external source inspected? | No. |
| Was any external tool executed? | No. |
| Was any dependency installed or removed? | No. |
| Was any adapter disabled? | No. |
| Was any generated output cleaned up? | No. |
| Was any source tracking modified? | No. |
| What pending alignments were recorded? | `pending_P9.5_vendor_fork_wrapper_submodule_decision_alignment`; P8.R alias drift for the prompt-listed shorter path; P9.R reconciliation requirement. |
| What is the recommended next ticket? | P9.R only if P9.1-P9.6 are complete and P9.5 path alignment is resolved; otherwise P9.5. |

Final markers:

```text
external_integration_rollback_incident_protocol_ready
rollback_incident_model_defined
external_tool_containment_model_defined
repo_contamination_response_model_defined
human_escalation_required_for_remediation
no_automatic_rollback
no_git_mutation
no_external_execution
```

Stop after P9.6. Do not start P9.0, P9.1, P9.2, P9.3, P9.4, P9.5, P9.R, P10, P11, P12, P13, P14, or EXT.* files from this ticket.
