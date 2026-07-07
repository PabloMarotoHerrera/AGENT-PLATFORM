# External Source Inspection Permission Gate

## Document Header

Title: External Source Inspection Permission Gate

Ticket: P9.3

Status: Accepted external source inspection permission gate

Date: 2026-07-07

Scope: Governance permission gate for controlled external source inspection under exact future scope within the post-P8 External Tool Integration Program.

Authority: External Source Inspection Permission Gate only, not external source inspection, directory listing, source traversal, dependency adoption, tool adoption, source modification, external tool execution, adapter implementation, runtime implementation, provider/auth/API/MCP activation, credential use, API calls, MCP calls, Graphify rerun, Hermes runtime activation, Hermes Cadence activation, GBrain/GStack runtime activation, ECC-main runtime activation, OpenCode execution from AGENT PLATFORM, product/Siamese source inspection, product integration, validation execution, security enforcement activation, persistence/database/event stream, telemetry, vector DB implementation, embeddings generation, graph DB implementation, generated output tracking approval, source tracking expansion approval, publication approval, Git mutation approval, or Cognitive Semantic System substrate selection.

Related documents:

- P8.R Platform MVP Readiness Closure
- P9.0 External Tool Integration Charter / Adopt-Not-Rebuild Boundary
- P8.0 Platform MVP Scope / External Integration Boundary
- P8.1 External Source Inventory / Classification
- P8.5 Security / Activation Gate Model
- P7.R Manual Agentic Workflow Planning Closure
- P7.0.F Reviewer Mesh / Immune Safeguards Contract
- P7.0.G Integrator / Commit Advisory Protocol
- P6.7 Operational Readiness Audit
- P5.R Minimal Active Agent Platform Audit
- P3.BR Activation Decision Reconciliation Closure
- P2.KR Knowledge / Retrieval Architecture Reconciliation Closure
- P2.R Cross-Lane Integration Reconciliation Closure
- P2.1 Shared Metadata Vocabulary Alignment
- P2.2 Cross-Lane Evidence Reference Contract
- P2.3 Audit / Retention / Rollback Baseline
- P1.1 Context Runtime Contract Hardening
- P1.2 Provider Adapter Metadata Contract Hardening
- P1.3 Tool Execution Boundary Contract Hardening
- P1.4 Agent Runtime Boundary Contract Hardening
- P1.5 Cognitive Semantic System Prototype Hardening
- P0.1 Activation Gate Enforcement Map
- P0.2 Validation Execution Gate Design
- P0.3 Security Enforcement Hardening Plan
- Activation Gate Charter
- Tool / Shell / Network / MCP Execution Policy
- Local-Only / Secrets / Credentials Policy
- Cognitive Semantic System ADR / audit
- README.md
- .gitignore
- .graphifyignore
- Optional P9.1 if present
- Optional P9.2 if present
- Optional P9.4 if present
- Optional P9.5 if present
- Optional P9.6 if present

Output: external source inspection permission gate

Result:

- `external_source_inspection_permission_gate_ready`
- `controlled_external_source_inspection_allowed_under_exact_future_gate`
- `no_external_source_inspection_performed_by_P9_3`

## Purpose

P9 opens the post-P8 External Tool Integration Program.

P9.3 defines the permission gate for controlled source inspection of external tools. P9.3 turns external source review from ad hoc/manual risk into governed permission.

P9.3 enables future exact-scope inspection tickets such as Graphify, Hermes, GBrain/GStack, ECC-main, OpenCode-related external harness candidates, or future MIT tools.

P9.3 does not inspect source itself.

P9.3 does not approve adoption.

P9.3 does not approve execution.

P9.3 does not approve runtime.

P9.3 does not approve adapters.

P9.3 does not approve product integration.

## Current Posture

P8 closed MVP-0 manual/non-executing.

P9 is the External Integration Foundation.

P9 default policy is adopt/adapt/wrap validated MIT tools when they fit.

Rebuild from scratch is not the default.

External source inspection is now permitted only through explicit gates.

External source inspection is not external tool adoption.

External source inspection is not dependency adoption.

External source inspection is not execution permission.

External source inspection is not runtime activation.

External source inspection is not provider/auth/API/MCP activation.

External source inspection is not product integration.

Canonical external source root is `4_external/sources`.

Legacy `external/sources` is not canonical.

## Core Rule

- Source inspection permission is not source adoption.
- Source inspection permission is not dependency adoption.
- Source inspection permission is not execution permission.
- Source inspection permission is not runtime activation.
- Source inspection permission is not product integration.

## Path / Root Normalization

Accepted P8.R path used by P9.3:

- `0_architecture/governance/agent_platform_p8_platform_mvp_readiness_closure.md`

Accepted P9.0 path used by P9.3:

- `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md`

Canonical external source root:

- `4_external/sources`

Legacy external source root:

- `external/sources` is legacy only and is not the current canonical root.

Known GStack candidate path:

- `4_external/sources/gstack-main`

GStack posture in P9.3:

- Path/class metadata only.
- No inspection.
- No listing.
- No import.
- No execution.
- No configuration.
- No adoption.

## Inputs Reviewed

| input | status | role in P9.3 | limitations |
| --- | --- | --- | --- |
| `0_architecture/governance/agent_platform_p8_platform_mvp_readiness_closure.md` | present | Required post-P8 closure input | Corrected P8.R path; path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_p9_external_tool_integration_charter_adopt_not_rebuild_boundary.md` | present | Required P9.0 policy authority | Corrected P9.0 path; path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_p8_platform_mvp_scope_external_integration_boundary.md` | present | P8.0 external integration boundary | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_external_source_inventory_graphify_gbrain_gstack_hermes_opencode.md` | present | P8.1 external source classification | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_p8_security_activation_gate_model.md` | present | P8.5 security / activation gate model | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_manual_agentic_workflow_planning_closure.md` | present | P7.R manual workflow closure | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_agent_native_organization_research_carry_forward.md` | present | P7 native carry-forward context | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_manual_harness_opencode_hermes_boundary_strategy.md` | present | P7 harness/OpenCode/Hermes boundary | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_reviewer_mesh_immune_safeguards_contract.md` | present | P7.0.F reviewer mesh / immune safeguards | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_manual_integrator_commit_advisory_protocol.md` | present | P7.0.G integration protocol | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_operational_readiness_audit.md` | present | P6.7 operational readiness | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_minimal_active_agent_platform_audit.md` | present | P5.R minimal active platform audit | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_activation_decision_reconciliation_closure.md` | present | P3.BR activation decision reconciliation | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_tool_execution_activation_decision.md` | mandatory input | Tool execution activation decision | Listed as mandatory input; not rechecked by the restricted P9.3 command set. |
| `0_architecture/governance/agent_platform_provider_auth_api_mcp_activation_decision.md` | mandatory input | Provider/auth/API/MCP activation decision | Listed as mandatory input; not rechecked by the restricted P9.3 command set. |
| `0_architecture/governance/agent_platform_agent_runtime_activation_decision.md` | mandatory input | Agent runtime activation decision | Listed as mandatory input; not rechecked by the restricted P9.3 command set. |
| `0_architecture/governance/agent_platform_activation_readiness_reconciliation_closure.md` | mandatory input | Activation readiness reconciliation | Listed as mandatory input; not rechecked by the restricted P9.3 command set. |
| `0_architecture/governance/agent_platform_controlled_source_classification_readiness.md` | mandatory input | Source classification readiness | Listed as mandatory input; not rechecked by the restricted P9.3 command set. |
| `0_architecture/governance/agent_platform_validation_execution_readiness.md` | mandatory input | Validation execution readiness | Listed as mandatory input; not rechecked by the restricted P9.3 command set. |
| `0_architecture/governance/agent_platform_security_enforcement_readiness.md` | mandatory input | Security enforcement readiness | Listed as mandatory input; not rechecked by the restricted P9.3 command set. |
| `0_architecture/governance/agent_platform_knowledge_retrieval_architecture_reconciliation_closure.md` | present | P2.KR knowledge / retrieval reconciliation | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_cross_lane_integration_reconciliation_closure.md` | present | P2.R cross-lane integration reconciliation | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_shared_metadata_vocabulary_alignment.md` | present | P2.1 shared metadata vocabulary | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_cross_lane_evidence_reference_contract.md` | present | P2.2 evidence reference contract | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_audit_retention_rollback_baseline.md` | present | P2.3 audit / retention / rollback baseline | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_context_runtime_contract_hardening.md` | present | P1.1 context runtime hardening | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_provider_adapter_metadata_contract_hardening.md` | present | P1.2 provider adapter metadata hardening | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_tool_execution_boundary_contract_hardening.md` | present | P1.3 tool execution boundary hardening | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_agent_runtime_boundary_contract_hardening.md` | present | P1.4 agent runtime boundary hardening | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_cognitive_semantic_system_prototype_hardening.md` | present | P1.5 Cognitive Semantic System hardening | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_activation_gate_enforcement_map.md` | present | P0.1 activation gate enforcement map | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_validation_execution_gate_design.md` | present | P0.2 validation execution gate design | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_security_enforcement_hardening_plan.md` | present | P0.3 security enforcement hardening plan | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_activation_gate_charter.md` | present | Activation Gate Charter | Path-only posture; content not inspected. |
| `0_architecture/security/agent_platform_tool_shell_network_mcp_execution_policy.md` | present | Tool / shell / network / MCP execution policy | Path-only posture; content not inspected. |
| `0_architecture/security/agent_platform_local_only_secrets_credentials_policy.md` | present | Local-only / secrets / credentials policy | Path-only posture; content not inspected. |
| `0_architecture/cognitive_semantic_system/agent_platform_cognitive_semantic_system_naming_substrate_adr.md` | present | Cognitive Semantic System ADR | Path-only posture; content not inspected. |
| `0_architecture/cognitive_semantic_system/agent_platform_cognitive_semantic_system_decision_audit.md` | present | Cognitive Semantic System audit | Path-only posture; content not inspected. |
| `README.md` | present | Repository boundary input | Path-only posture; content not inspected. |
| `.gitignore` | present | Git boundary input | Path-only posture; content not inspected or modified. |
| `.graphifyignore` | present | Graphify boundary input | Path-only posture; content not inspected or modified. |
| `0_architecture/governance/agent_platform_external_source_root_normalization.md` | present | Optional P9.1 root normalization | Path-only posture; content not inspected. |
| `0_architecture/governance/agent_platform_external_source_license_trust_intake_model.md` | present | Optional P9.2 license/trust intake | Path-only posture by recheck; content not inspected. |
| `0_architecture/governance/agent_platform_external_tool_execution_gate_model.md` | present | Optional P9.4 execution gate | Path-only posture; P9.3 still does not approve execution. |
| `0_architecture/governance/agent_platform_external_vendor_fork_wrapper_submodule_decision_model.md` | absent | Optional P9.5 adoption mode decision | `pending_P9.5_adoption_mode_decision_alignment`. |
| `0_architecture/governance/agent_platform_external_integration_rollback_incident_protocol.md` | absent | Optional P9.6 rollback/incident protocol | `pending_P9.6_rollback_incident_protocol_alignment`. |
| `4_external/sources` | present | Canonical external source root | Path-only posture; no listing, traversal, or content inspection. |
| `4_external/sources/graphify` | present | Graphify candidate path | Path/class metadata only; not inspected by P9.3. |
| `4_external/sources/Graphify` | present | Graphify candidate path | Path/class metadata only; not inspected by P9.3. |
| `4_external/sources/gbrain-master` | present | GBrain candidate path | Path/class metadata only; not inspected by P9.3. |
| `4_external/sources/gstack-main` | present | GStack candidate path | Path/class metadata only; not inspected, listed, imported, executed, configured, or adopted. |
| `4_external/sources/hermes` | absent | Hermes candidate path | Path-only posture; not inspected by P9.3. |
| `4_external/sources/Hermes` | absent | Hermes candidate path | Path-only posture; not inspected by P9.3. |
| `4_external/sources/ecc-main` | present | ECC-main candidate path | Path/class metadata only; not inspected by P9.3. |
| `4_external/sources/ECC-main` | present | ECC-main candidate path | Path/class metadata only; not inspected by P9.3. |
| `3_platform` | present | Local platform boundary | Path-only posture; content not inspected. |
| `3_platform/_governed_skeleton` | present | Governed skeleton boundary | Path-only posture; content not inspected. |
| `9_artifacts` | present | Generated/local artifact boundary | Path-only posture; content not inspected or modified. |
| `graphify-out` | absent | Graphify output boundary | Path-only posture; content not inspected or modified. |

## Dependency Posture

P9.3 consumes P9.0 as the policy authority for external tool integration.

P9.3 may consume P9.1 root normalization if present. P9.1 is present by path-only check.

P9.3 may consume P9.2 license/trust intake if present. P9.2 is present by path-only recheck.

P9.3 may consume P9.4 execution gate if present, but P9.3 does not approve execution. P9.4 is present by path-only check.

P9.3 may consume P9.5 adoption mode model if present, but P9.3 does not approve adoption. P9.5 is absent, so `pending_P9.5_adoption_mode_decision_alignment` is recorded.

P9.3 may consume P9.6 rollback/incident protocol if present. P9.6 is absent, so `pending_P9.6_rollback_incident_protocol_alignment` is recorded.

P9.3 must not create, modify, or supersede sibling P9 documents.

P9.3 may record drift candidates for P9.R.

## Inspection Permission Level Model

| level | name | meaning | P9.3 posture |
| --- | --- | --- | --- |
| P9-SI0 | path-existence-only | `Test-Path` only. | Allowed by P9.3 posture checks. |
| P9-SI1 | path-and-class-metadata-only | Path/class metadata from existing approved inventory only. | Allowed as metadata; no source reading. |
| P9-SI2 | license-readme-manifest-read-only | License/readme/manifest file inspection if exact file paths are approved. | Requestable by future exact gate; not performed by P9.3. |
| P9-SI3 | bounded-documentation-inspection | Bounded documentation inspection under exact file list or exact glob. | Requestable by future exact gate; not performed by P9.3. |
| P9-SI4 | bounded-source-file-inspection | Bounded source-file inspection under exact file list or exact glob. | Requestable by future exact gate; not performed by P9.3. |
| P9-SI5 | dependency-entrypoint-static-inspection | Static dependency/entrypoint inspection under exact file list, no execution. | Requestable by future exact gate; not performed by P9.3. |
| P9-SI6 | controlled-execution-required-but-not-approved-by-P9.3 | Execution is required to answer the question. | Blocked by P9.3; route to P9.4 or tool-specific execution gate. |
| P9-SI7 | adoption-required-but-not-approved-by-P9.3 | Adoption is required to answer or proceed. | Blocked by P9.3; route to P9.5 and tool-specific adoption decision. |

P9.3 may define when P9-SI2 through P9-SI5 can be requested. P9.3 must not itself perform P9-SI2 through P9-SI5 inspection.

## Inspection Permission Decision Model

Allowed decision statuses:

- `approved_for_exact_scope_read_only_inspection`
- `approved_for_metadata_only`
- `approved_for_license_manifest_only`
- `deferred_pending_license_trust_intake`
- `deferred_pending_root_normalization`
- `deferred_pending_security_review`
- `deferred_pending_human_approval`
- `blocked_sensitive_surface`
- `blocked_missing_scope`
- `blocked_requires_execution_gate`
- `blocked_requires_adoption_decision`
- `blocked_product_boundary`
- `blocked_secret_or_credential_risk`
- `rejected_out_of_scope`

Approval must be exact-scope.

Broad source inspection is blocked.

Wildcard inspection is blocked unless explicitly narrowed and justified.

Recursive inspection is blocked unless explicitly approved and bounded.

Execution remains blocked.

## ExternalSourceInspectionRequest Contract

`ExternalSourceInspectionRequest` required fields:

- `inspection_request_id`
- `requesting_ticket`
- `external_tool_name`
- `external_tool_family`
- `canonical_root`
- `target_path_refs`
- `requested_permission_level`
- `requested_inspection_purpose`
- `inspection_question`
- `expected_outputs`
- `allowed_files`
- `blocked_files`
- `allowed_patterns`
- `blocked_patterns`
- `license_trust_refs`
- `security_refs`
- `validation_refs`
- `retention_refs`
- `rollback_refs`
- `incident_refs`
- `human_approval_ref`
- `sensitivity_assessment`
- `secret_credential_risk`
- `product_boundary_risk`
- `execution_requirement_assessment`
- `adoption_requirement_assessment`
- `stop_rules`
- `limitations`

ExternalSourceInspectionRequest is a request.

It is not permission by itself.

## InspectionScope Contract

`InspectionScope` required fields:

- `inspection_scope_id`
- `inspection_request_ref`
- `canonical_root`
- `allowed_root`
- `allowed_paths`
- `allowed_file_types`
- `allowed_patterns`
- `blocked_paths`
- `blocked_file_types`
- `blocked_patterns`
- `max_depth`
- `recursive_allowed`
- `binary_file_posture`
- `large_file_posture`
- `generated_file_posture`
- `secret_sensitive_file_posture`
- `product_source_posture`
- `external_dependency_posture`
- `limitations`

Default blocked paths/patterns:

- `.env`
- `.env.*`
- `**/.env`
- `**/.env.*`
- `credentials/**`
- `secrets/**`
- `**/credentials/**`
- `**/secrets/**`
- `**/*secret*`
- `**/*credential*`
- `**/*token*`
- `**/*key*`
- provider configs
- token stores
- browser auth
- local credential stores
- product/Siamese source
- `9_artifacts/**`
- `graphify-out/**`
- generated outputs unless explicitly approved

## ApprovedInspectionSurface Contract

`ApprovedInspectionSurface` required fields:

- `approved_surface_id`
- `inspection_scope_ref`
- `approved_paths`
- `approved_patterns`
- `approved_file_types`
- `approved_permission_level`
- `allowed_operations`
- `blocked_operations`
- `rationale`
- `review_required`
- `human_approval_required`
- `limitations`

Allowed operations for P9.3-approved inspection gates:

- `read_text_only`
- `quote_limited`
- `summarize`
- `map_structure_from_approved_files`
- `record_dependency_metadata_from_approved_manifest`
- `record_entrypoint_metadata_from_approved_manifest`

Blocked operations:

- `execute`
- `import`
- `install`
- `build`
- `test`
- `run`
- `configure`
- `write`
- `patch`
- `delete`
- `move`
- `copy_into_runtime`
- `create_adapter`
- `adopt_dependency`
- `activate_runtime`
- `call_network`
- `call_provider`
- `call_MCP`
- `read_secrets`
- `read_credentials`
- `read_product_source`

## BlockedInspectionSurface Contract

`BlockedInspectionSurface` required fields:

- `blocked_surface_id`
- `inspection_scope_ref`
- `blocked_path_or_pattern`
- `blocker_reason`
- `sensitivity`
- `required_future_gate`
- `safe_reporting_format`
- `review_required`
- `limitations`

## InspectionPermissionDecision Contract

`InspectionPermissionDecision` required fields:

- `inspection_permission_decision_id`
- `inspection_request_ref`
- `decision_status`
- `approved_permission_level`
- `approved_surface_refs`
- `blocked_surface_refs`
- `required_future_gates`
- `license_trust_posture`
- `security_posture`
- `validation_posture`
- `retention_posture`
- `rollback_posture`
- `incident_posture`
- `human_approval_required`
- `expiration_or_revalidation_rule`
- `decision_rationale`
- `limitations`

## SensitiveContentHandling Contract

`SensitiveContentHandling` required fields:

- `sensitive_content_handling_id`
- `inspection_scope_ref`
- `sensitive_content_types`
- `detection_posture`
- `allowed_response`
- `blocked_response`
- `redaction_required`
- `stop_required`
- `escalation_route`
- `retention_posture`
- `limitations`

Required sensitive content types:

- `secret`
- `credential`
- `API_key`
- `token`
- `private_key`
- `.env_content`
- `provider_config`
- `auth_cookie`
- `browser_auth`
- `local_credential_store`
- `personal_data`
- `product_confidential_source`
- `unknown_sensitive_content`

If suspected sensitive content is encountered, stop inspection and report safe metadata only.

## RedactionRequirement Contract

`RedactionRequirement` required fields:

- `redaction_requirement_id`
- `sensitive_content_handling_ref`
- `redaction_scope`
- `redaction_method`
- `verbatim_quote_limits`
- `safe_summary_format`
- `blocked_disclosure`
- `review_required`
- `limitations`

## InspectionOutputPackage Contract

`InspectionOutputPackage` required fields:

- `inspection_output_package_id`
- `inspection_request_ref`
- `inspection_permission_decision_ref`
- `inspected_paths`
- `not_inspected_paths`
- `summary`
- `architecture_findings`
- `license_findings`
- `dependency_findings`
- `entrypoint_findings`
- `risk_findings`
- `blocked_findings`
- `sensitive_content_encountered`
- `redaction_applied`
- `evidence_refs`
- `validation_refs`
- `security_refs`
- `retention_refs`
- `rollback_refs`
- `incident_refs`
- `adoption_recommendation_allowed`
- `execution_recommendation_allowed`
- `limitations`
- `next_gate_recommendations`

InspectionOutputPackage may summarize inspected source.

InspectionOutputPackage may not approve execution.

InspectionOutputPackage may not approve adoption.

InspectionOutputPackage may not approve runtime.

InspectionOutputPackage may not approve product integration.

## InspectionStopRule Contract

`InspectionStopRule` required fields:

- `inspection_stop_rule_id`
- `trigger`
- `reason`
- `required_action`
- `safe_reporting_format`
- `escalation_route`
- `blocked_follow_up`
- `limitations`

Required triggers:

- attempt to inspect outside approved scope
- attempt to recursively inspect without approval
- secret or credential encountered
- `.env` encountered
- provider/auth material encountered
- API key or token encountered
- product source encountered
- binary or large file outside approved scope
- execution required to continue
- install/build/test/run required to continue
- network/provider/MCP required to continue
- source modification required to continue
- dependency adoption required to continue
- runtime activation required to continue
- adapter implementation required to continue
- Git mutation requested

## External Tool Family Gate Mapping

| tool family | canonical path candidate | default allowed P9.3 level | possible future level | blocked by default | future project |
| --- | --- | --- | --- | --- | --- |
| Graphify | `4_external/sources/graphify`, `4_external/sources/Graphify` | P9-SI0/P9-SI1 | P9-SI2-P9-SI5 only through P10/P9.3-approved exact source inspection if needed | execution, rerun, authority, adoption | P10 |
| Hermes | `4_external/sources/hermes`, `4_external/sources/Hermes` | P9-SI0/P9-SI1 | P9-SI2-P9-SI5 through P11.0/P11.1 | runtime, orchestration, Cadence, provider/MCP | P11 |
| GBrain | `4_external/sources/gbrain-master` | P9-SI0/P9-SI1 | P9-SI2-P9-SI5 through P12.0/P12.1 | runtime, persistent memory, substrate | P12 |
| GStack | `4_external/sources/gstack-main` | P9-SI0/P9-SI1 | P9-SI2-P9-SI5 through P12.0/P12.2 | execution, runtime, adoption | P12 |
| ECC-main | `4_external/sources/ecc-main`, `4_external/sources/ECC-main` | P9-SI0/P9-SI1 | P9-SI2-P9-SI5 through P13.0/P13.1 | Agent OS runtime, orchestration, adoption | P13 |
| OpenCode-related harnesses | external harness path if later normalized | P9-SI0/P9-SI1 | deeper inspection requires exact future gate | execution from AGENT PLATFORM, provider/auth/API/MCP | Future exact gate |
| future MIT tool | exact future `4_external/sources/<tool>` path | P9-SI0/P9-SI1 | P9-SI2-P9-SI5 after exact intake and trust model exist | execution, adoption, dependency use | Future exact gate |

## Candidate Classifications

Graphify:

- `external_source_candidate`
- `repo_evidence_tool_candidate`
- `MIT_candidate_if_license_confirms`
- `not_inspected_by_P9_3`
- `not_executed`
- `not_rerun`
- `not_authority`

Hermes:

- `external_source_candidate`
- `interface_candidate`
- `runtime_candidate`
- `orchestration_candidate`
- `cadence_candidate`
- `MIT_candidate_if_license_confirms`
- `not_inspected_by_P9_3`
- `not_executed`
- `not_runtime`

GBrain:

- `external_source_candidate`
- `memory_architecture_candidate`
- `persistent_knowledge_candidate`
- `MIT_candidate_if_license_confirms`
- `not_inspected_by_P9_3`
- `not_runtime`
- `not_substrate`

GStack:

- `external_source_candidate`
- `gbrain_compatibility_candidate`
- `skill_stack_candidate`
- `path: 4_external/sources/gstack-main`
- `MIT_candidate_if_license_confirms`
- `not_inspected_by_P9_3`
- `not_executed`
- `not_runtime`

ECC-main:

- `external_source_candidate`
- `agent_os_candidate`
- `orchestration_candidate`
- `runtime_candidate`
- `MIT_candidate_if_license_confirms`
- `not_inspected_by_P9_3`
- `not_executed`
- `not_runtime`

OpenCode:

- `external_harness_candidate`
- `H0_user_operated_harness`
- `not_executed_by_AGENT_PLATFORM`

## Interface With P9.1 - External Source Root Normalization

If P9.1 is present, use it as root authority.

P9.1 is present by path-only check.

P9.3 uses `4_external/sources`.

P9.3 must not use `external/sources` as canonical root.

## Interface With P9.2 - License / Trust Intake

If P9.2 is present, use it as license/trust authority.

P9.2 is present by path-only recheck.

If license/trust status is unknown, limit permission to P9-SI0/P9-SI1 unless a specific human/governance decision allows license/readme/manifest inspection.

## Interface With P9.4 - External Tool Execution Gate

P9.3 never approves execution.

P9.4 is present by path-only check, but P9.3 does not consume it as execution approval.

If inspection requires install/build/test/run/import, route to P9.4 or a future tool-specific execution gate.

## Interface With P9.5 - Vendor / Fork / Wrapper / Submodule Decision Model

P9.3 never approves adoption mode.

If inspection output suggests adoption, route to P9.5 or tool-specific adoption decision.

P9.5 is absent by path-only check, so `pending_P9.5_adoption_mode_decision_alignment` is recorded.

## Interface With P9.6 - Rollback / Incident Protocol

P9.3 must require rollback/incident posture for any future deeper inspection that may affect repository state, generated outputs, local cache, dependency files, or runtime.

P9.3 itself does not create such effects.

P9.6 is absent by path-only check, so `pending_P9.6_rollback_incident_protocol_alignment` is recorded.

## Interface With P10-P13

P10 Graphify source/evidence integration must use P9.3 before deeper source inspection.

P11 Hermes source review must use P9.3 before inspecting Hermes source.

P12 GBrain/GStack source review must use P9.3 before inspecting GBrain/GStack source.

P13 ECC-main source review must use P9.3 before inspecting ECC-main source.

P14 synthesis may consume inspection outputs, but P14 does not retroactively authorize inspection.

## Evidence / Validation / Security Interfaces

### Evidence Interface

Evidence supports; it does not decide.

P9.3 may define EvidenceRefs for inspection permission decisions.

EvidenceRefs do not approve inspection by themselves.

### Validation Interface

Validation evaluates; governance decides.

P9.3 does not run validation.

ValidationRefs may describe future validation requirements.

### Security Interface

Security constrains; it does not activate.

SecurityRefs are required for inspection decisions.

SecurityRefs do not approve execution, adoption, runtime, provider/auth/API/MCP, or Git mutation.

## Retention / Rollback / Incident Posture

Inspection outputs must minimize retained sensitive material.

Inspection outputs must not include secrets, credentials, tokens, `.env` values, private keys, provider configs, or personal data.

Inspection outputs should include redacted safe summaries only when sensitive material is encountered.

Any future source inspection must define rollback and incident routes before it can proceed.

P9.3 does not implement logging.

P9.3 does not implement persistence.

P9.3 does not implement rollback automation.

P9.3 does not implement incident automation.

## Human Approval Requirements

Human/governance approval is required for:

- any inspection beyond P9-SI1 metadata
- any recursive inspection
- any source-file inspection
- any dependency/entrypoint inspection
- any inspection of unknown sensitivity
- any inspection of large files
- any inspection that may encounter secrets or credentials
- any inspection that may imply runtime/adoption decisions

Human approval is not broad approval.

Human approval must be exact-scope.

## Stop Rules

Stop if any of the following occur:

- P9.0 missing
- P8.R missing
- external source inspection attempted by P9.3
- external source directory listing attempted by P9.3
- external source traversal attempted by P9.3
- external source execution attempted
- external source import attempted
- external source modification attempted
- inspection outside approved future scope attempted
- secret or credential encountered
- `.env` encountered
- provider/auth material encountered
- API key or token encountered
- product/Siamese source encountered
- Graphify rerun requested
- Hermes runtime activation requested
- GBrain/GStack runtime activation requested
- ECC-main runtime activation requested
- OpenCode execution requested from AGENT PLATFORM
- provider/auth/API/MCP activation requested
- network call requested
- tool execution requested
- agent execution requested
- autonomous orchestration requested
- validation execution requested
- security enforcement activation requested
- persistence/vector/graph DB requested
- generated output tracking requested
- source tracking expansion requested
- publication requested
- Git mutation requested
- Cognitive Semantic System substrate selection requested

## Drift Register

| drift_id | source_area | observed_issue | expected_canonical_posture | status | impact | resolution_route |
| --- | --- | --- | --- | --- | --- | --- |
| P9.3-DRIFT-001 | external source root | legacy external/sources root used as canonical | `4_external/sources` is canonical; `external/sources` is legacy only. | resolved | Prevents wrong-root inspection. | P9.3 root rule and P9.1 alignment. |
| P9.3-DRIFT-002 | external source root | 4_external/sources root missing | `4_external/sources` must exist for path-based candidate posture. | not_observed | No blocker; path present. | P9.1/P9.R reconciliation. |
| P9.3-DRIFT-003 | GStack path | GStack path drift | GStack path is `4_external/sources/gstack-main`. | resolved | Prevents GStack inspection/listing/adoption drift. | P9.3 path normalization. |
| P9.3-DRIFT-004 | source/adoption boundary | source inspection vs source adoption ambiguity | Source inspection permission is not source adoption. | resolved | Prevents adoption-by-review. | INSPECT invariants. |
| P9.3-DRIFT-005 | source/execution boundary | source inspection vs execution permission ambiguity | Source inspection permission is not execution permission. | resolved | Prevents run/build/test drift. | Route execution-required findings to P9.4. |
| P9.3-DRIFT-006 | dependency boundary | source inspection vs dependency adoption ambiguity | Source inspection permission is not dependency adoption. | resolved | Prevents dependency adoption. | Route adoption-required findings to P9.5. |
| P9.3-DRIFT-007 | adapter boundary | source inspection vs adapter implementation ambiguity | Source inspection permission is not adapter implementation. | resolved | Prevents wrapper/adapter creation. | P9.5/tool-specific decision. |
| P9.3-DRIFT-008 | metadata boundary | path existence vs content inspection ambiguity | Path existence is not content inspection permission. | resolved | Prevents overreading. | P9-SI0/P9-SI1 model. |
| P9.3-DRIFT-009 | license/trust | license/trust unknown but deeper inspection requested | Deeper inspection needs P9.2 or exact human/governance decision. | not_observed | P9.2 is present by path-only recheck; content not inspected. | P9.R reconciliation. |
| P9.3-DRIFT-010 | recursive scope | recursive inspection ambiguity | Broad recursive inspection is blocked by default. | resolved | Prevents uncontrolled source review. | InspectionScope max depth and recursive flag. |
| P9.3-DRIFT-011 | wildcard scope | wildcard inspection ambiguity | Wildcard inspection blocked unless narrowed and justified. | resolved | Prevents uncontrolled source review. | ApprovedInspectionSurface contract. |
| P9.3-DRIFT-012 | sensitive content | secret/credential risk unresolved | Secrets and credentials stop inspection. | resolved | Prevents sensitive disclosure. | SensitiveContentHandling and stop rules. |
| P9.3-DRIFT-013 | product boundary | product/Siamese source boundary ambiguity | Product/Siamese source remains blocked. | resolved | Prevents product source inspection. | InspectionScope blocked paths. |
| P9.3-DRIFT-014 | Graphify boundary | Graphify evidence inspection vs Graphify authority ambiguity | Graphify inspection does not make Graphify authority. | resolved | Prevents authority drift. | Tool family mapping. |
| P9.3-DRIFT-015 | Hermes boundary | Hermes source inspection vs Hermes runtime ambiguity | Hermes inspection does not activate Hermes runtime. | resolved | Prevents runtime activation. | Tool family mapping. |
| P9.3-DRIFT-016 | GBrain/GStack boundary | GBrain/GStack inspection vs memory runtime ambiguity | GBrain/GStack inspection does not activate memory/skill runtime. | resolved | Prevents runtime/substrate drift. | Tool family mapping. |
| P9.3-DRIFT-017 | ECC-main boundary | ECC-main inspection vs agent OS adoption ambiguity | ECC-main inspection does not adopt Agent OS runtime. | resolved | Prevents runtime/adoption drift. | Tool family mapping. |
| P9.3-DRIFT-018 | P9.1 | P9.1 root normalization pending | P9.1 should be available as root authority. | not_observed | No pending marker; P9.1 present. | P9.R reconciliation. |
| P9.3-DRIFT-019 | P9.2 | P9.2 license/trust intake pending | P9.2 should define license/trust authority. | not_observed | No pending marker; P9.2 present by path-only recheck, but P9.3 still does not inspect its contents. | P9.R reconciliation. |
| P9.3-DRIFT-020 | P9.4 | P9.4 execution gate pending | P9.4 should route execution-required findings. | not_observed | No pending marker; P9.4 present, but P9.3 still does not approve execution. | P9.R reconciliation. |
| P9.3-DRIFT-021 | P9.5 | P9.5 adoption mode pending | P9.5 should route adoption-required findings. | pending_P9.5_alignment | Adoption mode unresolved. | P9.5. |
| P9.3-DRIFT-022 | P9.6 | P9.6 rollback/incident protocol pending | P9.6 should define rollback/incident protocol. | pending_P9.6_alignment | Incident/rollback route incomplete. | P9.6. |

## Inspection Permission Invariants

- INSPECT-001 P9.3 is an external source inspection permission gate only.
- INSPECT-002 P9.3 does not inspect external source content.
- INSPECT-003 Source inspection permission is not source adoption.
- INSPECT-004 Source inspection permission is not dependency adoption.
- INSPECT-005 Source inspection permission is not execution permission.
- INSPECT-006 Source inspection permission is not runtime activation.
- INSPECT-007 Source inspection permission is not adapter implementation.
- INSPECT-008 Source inspection permission is not product integration.
- INSPECT-009 Canonical external source root is 4_external/sources.
- INSPECT-010 external/sources is legacy only.
- INSPECT-011 GStack canonical candidate path is 4_external/sources/gstack-main.
- INSPECT-012 Path existence is not content inspection permission.
- INSPECT-013 Exact scope is required for inspection beyond metadata.
- INSPECT-014 Broad recursive inspection is blocked by default.
- INSPECT-015 Wildcard inspection is blocked unless explicitly narrowed.
- INSPECT-016 Secrets and credentials stop inspection.
- INSPECT-017 Product/Siamese source remains blocked.
- INSPECT-018 Execution-required findings route to P9.4.
- INSPECT-019 Adoption-required findings route to P9.5.
- INSPECT-020 Rollback/incident posture routes to P9.6.
- INSPECT-021 Graphify inspection does not make Graphify authority.
- INSPECT-022 Hermes inspection does not activate Hermes runtime.
- INSPECT-023 GBrain/GStack inspection does not activate memory/skill runtime.
- INSPECT-024 ECC-main inspection does not adopt Agent OS runtime.
- INSPECT-025 Evidence supports; it does not decide.
- INSPECT-026 Validation evaluates; governance decides.
- INSPECT-027 Security constrains; it does not activate.
- INSPECT-028 Git mutation remains blocked.

## Future Validation Targets

Future validation targets, not executed:

- external source inspection permission gate document exists
- canonical root is 4_external/sources
- legacy external/sources not used as canonical
- ExternalSourceInspectionRequest completeness
- InspectionScope completeness
- ApprovedInspectionSurface completeness
- BlockedInspectionSurface completeness
- InspectionPermissionDecision completeness
- SensitiveContentHandling completeness
- RedactionRequirement completeness
- InspectionOutputPackage completeness
- InspectionStopRule completeness
- inspection permission levels completeness
- Graphify gate mapping completeness
- Hermes gate mapping completeness
- GBrain gate mapping completeness
- GStack gate mapping completeness
- ECC-main gate mapping completeness
- OpenCode harness gate mapping completeness
- no source inspection by P9.3 invariant
- no external source listing by P9.3 invariant
- no execution permission invariant
- no adoption permission invariant
- no product source inspection invariant
- secret/credential stop rule invariant
- P10 handoff readiness
- P11 handoff readiness
- P12 handoff readiness
- P13 handoff readiness

## Future Hardening Candidates

Future tickets, not started:

- INSPECT-HARD-01 - ExternalSourceInspectionRequest Schema Alignment
- INSPECT-HARD-02 - InspectionScope Exact-Path Validation Design
- INSPECT-HARD-03 - Sensitive Content Stop Rule Hardening
- INSPECT-HARD-04 - License / Trust Intake Coupling Review
- INSPECT-HARD-05 - Execution Gate Coupling Review
- INSPECT-HARD-06 - Vendor/Fork/Wrapper Coupling Review
- INSPECT-HARD-07 - Rollback/Incident Coupling Review
- INSPECT-HARD-08 - Tool-Specific Inspection Template Design
- INSPECT-HARD-09 - P10 Graphify Source Inspection Template
- INSPECT-HARD-10 - P11/P12/P13 Source Review Template

## Created / Not Created Register

- external source inspection permission gate document created
- controlled external source inspection permission model defined
- inspection levels P9-SI0 through P9-SI7 defined
- ExternalSourceInspectionRequest contract defined
- InspectionScope contract defined
- ApprovedInspectionSurface contract defined
- BlockedInspectionSurface contract defined
- InspectionPermissionDecision contract defined
- SensitiveContentHandling contract defined
- RedactionRequirement contract defined
- InspectionOutputPackage contract defined
- InspectionStopRule contract defined
- canonical external source root recorded as 4_external/sources
- legacy external/sources not used as canonical
- GStack path recorded as 4_external/sources/gstack-main path/class metadata only
- no external source inspection performed
- no external source directory listing performed
- no external source traversal performed
- no Graphify source inspected
- no Hermes source inspected
- no GBrain source inspected
- no GStack source inspected
- no ECC-main source inspected
- no OpenCode source inspected
- no external source modified
- no dependency adopted
- no vendor/fork/wrapper/submodule decision made
- no adapter implemented
- no runtime implemented
- no Graphify rerun
- no Graphify adoption approved
- no Hermes runtime activated
- no Hermes Cadence activated
- no GBrain runtime activated
- no GStack runtime activated
- no ECC-main runtime activated
- no OpenCode execution from AGENT PLATFORM approved
- no provider/auth/API/MCP activation approved
- no credential use approved
- no API calls executed
- no MCP calls executed
- no network calls executed
- no tool execution approved
- no shell/subprocess execution approved
- no package-manager execution approved
- no build/test/CI execution approved
- no validation execution approved
- no security enforcement activation approved
- no agent execution approved
- no task execution approved
- no live connector activation approved
- no product/Siamese source inspected
- no product integration approved
- no vector DB implemented
- no embeddings generated
- no graph DB implemented
- no ontology runtime implemented
- no persistence DB implemented
- no event stream implemented
- no telemetry implemented
- no generated outputs modified/tracked
- no source tracking expansion approved
- no publication approved
- no Cognitive Semantic System substrate selected
- no Git mutation by the agent
- no `.graphifyignore` modified
- no `.gitignore` modified
- no P9.0 created or modified
- no P9.1 created or modified
- no P9.2 created or modified
- no P9.4 created or modified
- no P9.5 created or modified
- no P9.6 created or modified
- no P9.R started
- no P10 started
- no P11 started
- no P12 started
- no P13 started
- no P14 started
- no P4 started
- no EXT.* started

## Recommended Next Tickets

After P9.3:

- P9.1 - External Source Root Normalization, if not already completed
- P9.2 - External Source License / Trust Intake Model, if not already completed
- P9.4 - External Tool Execution Gate Model, if not already completed
- P9.5 - Vendor / Fork / Wrapper / Submodule Decision Model, if not already completed
- P9.6 - External Integration Rollback / Incident Protocol, if not already completed
- P9.R - External Integration Foundation Closure, after P9.1-P9.6 are complete

Recommended actual if any of P9.1-P9.6 remain incomplete:

- Complete remaining P9 foundation tickets before P9.R.

Recommended actual after P9.1-P9.6 are complete:

- P9.R - External Integration Foundation Closure

After P9.R, recommended sequence:

- P10.0 - Graphify Integration Scope / Markdown Authorization

Do not recommend P10/P11/P12/P13 execution before P9.R unless the user explicitly chooses a gated early branch.

Do not recommend external source execution, Graphify rerun, Hermes runtime, GBrain/GStack runtime, ECC-main runtime, provider/auth/API/MCP activation, product/Siamese integration, Git automation, vector DB, graph DB, or Cognitive Semantic System substrate selection.

## Final Verdict

What did P9.3 create? P9.3 created the External Source Inspection Permission Gate.

What canonical external source root was recorded? `4_external/sources`.

Was external/sources avoided as canonical root? Yes, `external/sources` is legacy only.

Was GStack recorded as `4_external/sources/gstack-main`? Yes.

Did P9.3 inspect any external source content? No.

Did P9.3 list or traverse external source directories? No.

What inspection permission levels were defined? P9-SI0 through P9-SI7.

What ExternalSourceInspectionRequest contract was defined? A request contract with ticket, tool family, canonical root, target refs, scope, purpose, expected outputs, allowed/blocked files and patterns, refs, risk assessments, stop rules, and limitations.

What InspectionScope contract was defined? A scope contract with allowed root, allowed paths/patterns/types, blocked paths/patterns/types, max depth, recursion posture, binary/large/generated/sensitive/product/dependency postures, and limitations.

What ApprovedInspectionSurface contract was defined? An approved surface contract with approved paths/patterns/types, permission level, allowed operations, blocked operations, rationale, review requirements, and limitations.

What BlockedInspectionSurface contract was defined? A blocked surface contract with blocked path or pattern, blocker reason, sensitivity, future gate, safe reporting format, review requirement, and limitations.

What InspectionPermissionDecision contract was defined? A decision contract with decision status, approved level, approved and blocked surfaces, required future gates, license/trust, security, validation, retention, rollback, incident posture, human approval requirement, revalidation rule, rationale, and limitations.

What SensitiveContentHandling contract was defined? A sensitive content contract that requires stop-and-safe-metadata reporting for secrets, credentials, API keys, tokens, private keys, `.env` content, provider config, auth material, personal data, product confidential source, and unknown sensitive content.

What RedactionRequirement contract was defined? A redaction contract defining redaction scope, method, quote limits, safe summary format, blocked disclosure, review requirement, and limitations.

What InspectionOutputPackage contract was defined? A controlled output contract for summaries/findings/refs/limitations that may not approve execution, adoption, runtime, or product integration.

What InspectionStopRule contract was defined? A stop-rule contract for out-of-scope inspection, recursive inspection without approval, sensitive content, product source, execution/install/build/test/run requirements, network/provider/MCP needs, source modification, dependency adoption, runtime activation, adapter implementation, and Git mutation.

How does P9.3 prevent source inspection from becoming adoption? It states source inspection permission is not adoption and routes adoption-required findings to P9.5.

How does P9.3 prevent source inspection from becoming execution permission? It states source inspection permission is not execution permission and routes execution-required findings to P9.4.

How does P9.3 prevent source inspection from becoming runtime activation? It blocks runtime activation and maps runtime-required findings to future gates.

How does P9.3 handle secrets/credentials? Suspected sensitive content stops inspection and permits safe metadata reporting only.

How does P9.3 handle product/Siamese source boundaries? Product/Siamese source is blocked by default and remains outside external source inspection permission.

How does P9.3 route execution-required findings? To P9.4 or a tool-specific execution gate.

How does P9.3 route adoption-required findings? To P9.5 or a tool-specific adoption decision.

How does P9.3 hand off to P10/P11/P12/P13? P10, P11, P12, and P13 must use P9.3 before deeper Graphify, Hermes, GBrain/GStack, or ECC-main source inspection.

Was Graphify source inspected? No.

Was Hermes source inspected? No.

Was GBrain source inspected? No.

Was GStack source inspected? No.

Was ECC-main source inspected? No.

Was any external tool executed? No.

Was any dependency adopted? No.

Was any adapter implemented? No.

Was provider/auth/API/MCP activated? No.

Was product/Siamese source inspected? No.

Was Git mutated? No.

What pending P9 alignments remain? `pending_P9.5_adoption_mode_decision_alignment` and `pending_P9.6_rollback_incident_protocol_alignment`.

What is the next ticket? Complete remaining P9 foundation tickets before P9.R, starting with P9.2 if it is still absent.
