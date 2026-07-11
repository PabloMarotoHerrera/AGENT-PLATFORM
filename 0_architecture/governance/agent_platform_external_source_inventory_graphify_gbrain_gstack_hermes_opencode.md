# External Source Inventory / Classification

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | External Source Inventory / Classification |
| Ticket | P8.1 |
| Status | Accepted external source inventory / classification |
| Date | 2026-07-06 |
| Scope | Canonical external / adjacent platform candidate inventory and classification for AGENT PLATFORM / Siamese covering Graphify, GBrain, GStack, Hermes, and OpenCode. |
| Authority | External candidate inventory and classification only, not external source adoption, runtime activation, adapter execution, provider/auth/API/MCP activation, credential use, API calls, MCP calls, tool execution, agent execution, live connector activation, Graphify execution/rerun/adoption, GBrain runtime/adoption/import/configuration, GStack runtime/adoption/import/configuration, Hermes runtime/adoption/import/configuration, OpenCode execution/integration, source content inspection, product/Siamese source inspection, vector DB implementation, embedding generation, graph DB implementation, persistence, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P8.0, P7.R, P6.7, P6.6, P5.R, P3.BR, P2.KR, P2.2, P2.3, Graphify Repo Map Summary, S-03, S-04, README.md, `.gitignore`, `.graphifyignore`, P8.2, P8.4, and P8.5. P8.3 was absent during P8.1 checks. |
| Output | `external_source_inventory_ready` |
| Additional output markers | `gstack_registered_as_gbrain_compatible_candidate`; `no_external_runtime_adoption` |

P8.0 was present during P8.1 posture checks. P8.1 is not blocked by `p8_0_missing_boundary`.

## 2. Purpose

P8 converts the validated P7 manual workflow into a local interactive MVP path. P8.1 inventories external and adjacent candidates before design or integration.

P8.1 covers Graphify, GBrain, GStack, Hermes, and OpenCode. It verifies paths only as path/class metadata, distinguishes source candidate, runtime candidate, memory candidate, UI candidate, harness candidate, evidence candidate, GBrain compatibility candidate, and skill stack candidate, and records what is present, absent, uninspected, and gated.

P8.1 does not execute or inspect external candidate contents. P8.1 does not adopt any external runtime. P8.1 does not start P8.6, P8.7, P8.8, or P8.9.

## 3. Current Posture

| Area | Current posture | P8.1 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM | Entering P8 Platform MVP / Interaction Layer. | P8.1 can inventory candidates after P8.0. | Autonomous platform runtime. |
| P8.0 | Present boundary posture. | Defines MVP scope and external integration boundary. | Runtime approval. |
| MVP-0 | Local interactive manual workflow assistant. | Manual workflow support only. | Product generator or autonomous runtime. |
| P8.1 | Inventory/classification only. | Path/class metadata and gate mapping. | Integration or runtime activation. |
| Graphify | Generated evidence / repo map candidate. | Repository graph / evidence graph / architecture map candidate. | Authority, source of truth, automatic rerun, architecture decider, repo-state writer. |
| GBrain | Memory architecture candidate. | Candidate only; not adopted. | Runtime, persistent memory, graph/vector DB, automatic retrieval. |
| GStack | GBrain-compatible skill stack candidate. | Candidate only; not adopted. | Runtime, dependency approval, bootstrap activation. |
| Hermes | UI/runtime/orchestration/Cadence candidate. | Future UI/runtime boundary candidate only. | Active Hermes runtime, Cadence, automatic dispatch. |
| OpenCode | H0 user-operated harness. | Manual harness candidate only. | Integrated runtime or automatic execution. |
| Product/Siamese | Product vision deferred. | Product source remains blocked. | Product behavior or source inspection. |
| External adoption | Blocked. | `no_external_runtime_adoption`. | Adoption by path presence. |

## 4. Inputs Reviewed

Inputs were consumed as governance/path/class metadata only. P8.1 did not inspect external candidate source contents, product source, raw generated outputs, secrets, credentials, configs, token stores, browser auth, local credential stores, API keys, or runtime state.

| Input | Present | Consumed as | Inventory relevance | Limitations | Pending alignment |
| --- | --- | --- | --- | --- | --- |
| P8.0 Platform MVP Scope / External Integration Boundary | Yes | Required P8 boundary | Defines P8 MVP scope, external candidate classes, and no-runtime posture. | Not modified. | None. |
| P7.R Manual Agentic Workflow Planning Closure | Yes | Manual workflow closure | Confirms H0/manual workflow lineage. | No P7 work started. | None. |
| P6.7 Operational Readiness Audit | Yes | Operational baseline | Confirms no runtime activation and no external adoption. | No operational activation. | None. |
| P6.6 Cognitive Semantic System Substrate Decision / Defer Record | Yes | Substrate defer baseline | Confirms Graphify evidence-only and GBrain candidate-only posture. | No substrate selection. | None. |
| P5.R Minimal Active Agent Platform Audit | Yes | AL-1 skeleton audit | Confirms metadata skeleton and non-activation posture. | No skeleton execution. | None. |
| P3.BR Activation Decision Reconciliation Closure | Yes | Activation decision baseline | Preserves provider/tool/agent blockers. | No activation decision changed. | None. |
| P2.KR Knowledge / Retrieval Architecture Reconciliation Closure | Yes | Knowledge/retrieval baseline | Confirms markdown canonical memory, no live retrieval, Graphify support-only. | No retrieval runtime. | None. |
| P2.2 EvidenceRef Contract | Yes | Evidence vocabulary | Evidence supports; it does not decide. | No evidence promotion. | None. |
| P2.3 Audit / Retention / Rollback Baseline | Yes | Retention/rollback baseline | Confirms generated/raw output and tracking blockers. | No persistence or tracking. | None. |
| Graphify Repo Map Summary | Yes | Curated generated evidence metadata | Supports Graphify classification as generated evidence only. | Raw Graphify output not inspected. | None. |
| S-03 Local-only / Secrets / Credentials Policy | Yes | Security/local-only baseline | Preserves local-only, artifact, secret, credential, product, external blockers. | No secret/credential inspection. | None. |
| S-04 Tool / Shell / Network / MCP Execution Policy | Yes | Execution policy baseline | Preserves no tool/shell/network/MCP execution posture. | No execution. | None. |
| README.md | Yes | Root orientation | Confirms AGENT PLATFORM workspace purpose. | No runtime effect. | None. |
| `.gitignore` | Yes | Ignore posture metadata | Confirms local-only/generated/secrets/provider-auth hygiene. | Not modified; not enforcement. | None. |
| `.graphifyignore` | Yes | Graphify input boundary metadata | Confirms default-deny Graphify boundary. | Not modified; not permission to run Graphify. | None. |
| P8.2 MVP Interaction Surface Architecture | Yes | Optional P8 peer metadata | Aligns interaction surface, Hermes UI candidate posture, and OpenCode H0 manual harness loop. | Not modified. | None. |
| P8.3 Core Workflow Schema Candidates | No | Optional P8 peer | Would align schema objects if present. | Not created. | `pending_P8.3_schema_candidates_alignment` |
| P8.4 Local Workspace / State Model | Yes | Optional P8 peer metadata | Confirms local-only/no-persistence state boundary. | Not modified. | None. |
| P8.5 Security / Activation Gate Model | Yes | Optional P8 peer metadata | Confirms P8 activation levels and external candidate gates. | Not modified. | None. |
| `external/sources/` path metadata | No | Path presence metadata | External source parent path. | Absent; directory-name listing not run. | `not_present` |
| `external/sources/gbrain-master` path metadata | No | Path presence metadata | GBrain candidate path. | No content available or inspected. | `not_present` |
| GStack candidate path metadata | No | Path presence metadata | `external/sources/gstack` and `external/sources/gstack-master`. | No content available or inspected. | `not_present` |
| Hermes candidate path metadata | No | Path presence metadata | `external/sources/hermes` and `external/sources/hermes-master`. | No content available or inspected. | `not_present` |
| OpenCode candidate path metadata | No | Path presence metadata | `external/sources/opencode` and `external/sources/opencode-master`. | No content available or inspected. | `not_present` |
| `graphify-out/` path metadata | No | Raw Graphify output path candidate | Raw Graphify output path check. | Absent; no raw output inspected. | `not_present` |
| `9_artifacts/` path metadata | Yes | Local-only generated artifact path | Confirms generated artifact surface exists. | Contents not inspected. | `present_path_not_inspected` |

## 5. Inventory Method

Allowed inventory method:

| Method | P8.1 use | Boundary |
| --- | --- | --- |
| Path presence checks | Used for exact candidate paths and generated artifact path. | Path presence is not adoption, content review, dependency approval, or runtime approval. |
| Non-recursive external directory-name listing | Allowed only if `external/sources/` exists. | Not run because `external/sources/` was absent. |
| Approved governance document review | Used for mandatory governance, security, and CSS inputs. | Governance metadata only. |
| Graphify Repo Map Summary review | Used as curated generated evidence metadata. | Raw Graphify output not inspected. |
| External candidate file-content inspection | Not used. | Blocked until future explicit gate. |
| Raw output inspection | Not used. | Blocked. |
| Execution/import/dependency install/network/runtime probing | Not used. | Blocked. |

Inventory status values:

| Status | Meaning |
| --- | --- |
| `present_path_not_inspected` | Path exists, but contents were not inspected. |
| `present_metadata_document_only` | Governed metadata document exists and was read as metadata only. |
| `not_present` | Path was checked and absent. |
| `path_candidate_ambiguous` | Multiple plausible paths exist or exact path is unresolved. |
| `installed_claim_unverified` | A candidate may be claimed elsewhere but installation was not verified. |
| `installed_path_verified` | A candidate install path was verified as a path only. No candidate reached this status in P8.1. |
| `exact_path_requires_followup_classification` | Multiple or ambiguous path candidates require later classification. |
| `inspection_blocked_until_gate` | Content inspection requires a future explicit gate. |
| `adoption_blocked` | Adoption is blocked. |
| `unknown_inventory_status` | Status is unknown and must be treated as blocked or needs review. |

## 6. ExternalCandidateRecord Object Model

`ExternalCandidateInventory` is the canonical inventory object. `ExternalCandidateRecord` is the canonical candidate record object. Both are metadata only.

| Field | Meaning |
| --- | --- |
| `candidate_id` | Stable candidate identifier. |
| `candidate_name` | Human-readable candidate name. |
| `candidate_family` | Candidate family, such as evidence, memory, skill stack, runtime/UI, or harness. |
| `candidate_kind` | `ExternalCandidateKind` values. |
| `candidate_status` | `ExternalCandidateStatus` values. |
| `observed_paths` | Path candidates checked as metadata only. |
| `path_verification_status` | Path presence result. |
| `source_inspection_posture` | `SourceInspectionPosture` value. |
| `execution_posture` | Whether the candidate was executed; P8.1 value is `not_executed`. |
| `adoption_posture` | Whether the candidate was adopted; P8.1 value is `not_adopted`. |
| `runtime_posture` | Whether runtime is active; P8.1 value is `not_runtime`. |
| `dependency_posture` | Dependency approval posture. |
| `provider_auth_posture` | Provider/auth posture. |
| `mcp_posture` | MCP posture. |
| `memory_posture` | Memory/persistent knowledge posture. |
| `persistence_posture` | Persistence/database posture. |
| `ui_posture` | UI/interface posture. |
| `harness_posture` | Harness posture. |
| `evidence_posture` | Evidence posture. |
| `product_posture` | Product/Siamese boundary posture. |
| `security_posture` | Security blocker posture. |
| `validation_posture` | Validation posture. |
| `retention_posture` | Retention posture. |
| `rollback_posture` | Rollback posture. |
| `incident_posture` | Incident posture. |
| `required_future_gates` | Gate or ticket required before expansion. |
| `adoption_blockers` | Active `AdoptionBlocker` values. |
| `allowed_p8_use` | Allowed P8.1 metadata use. |
| `blocked_p8_use` | Blocked uses. |
| `evidence_refs` | EvidenceRef-compatible metadata refs. |
| `source_refs` | SourceRef-compatible path metadata refs. |
| `validation_refs` | ValidationRef-compatible future validation refs. |
| `security_refs` | SecurityRef-compatible blocker refs. |
| `limitations` | Known limitations. |
| `pending_alignment_refs` | Pending P8 peer or future gate alignments. |

ExternalCandidateRecord is not adoption, import, execution, integration, dependency approval, source inspection approval, provider/auth approval, MCP approval, memory substrate selection, or runtime activation.

Related vocabulary refs may include EvidenceRef, SourceRef, ValidationRef, SecurityRef, ApprovalRef, RetentionRef, RollbackRef, IncidentRef, GraphifyRef, ProductRef, and GBrainCandidateRef.

## 7. Candidate Kind / Classification Vocabulary

`ExternalCandidateKind` values:

| ExternalCandidateKind | Meaning |
| --- | --- |
| `external_source_candidate` | External source candidate, not adopted by presence. |
| `repository_graph_candidate` | Repository graph candidate. |
| `evidence_graph_candidate` | Evidence graph candidate. |
| `architecture_map_candidate` | Architecture map candidate. |
| `generated_evidence_tool_candidate` | Generated evidence tool candidate. |
| `memory_architecture_candidate` | Memory architecture candidate. |
| `persistent_knowledge_candidate` | Persistent knowledge candidate. |
| `second_brain_substrate_candidate` | Second-brain substrate candidate. |
| `gbrain_compatibility_candidate` | GBrain compatibility candidate. |
| `skill_stack_candidate` | Skill stack candidate. |
| `bootstrap_layer_candidate` | Bootstrap layer candidate. |
| `agent_workflow_support_candidate` | Agent workflow support candidate. |
| `agent_runtime_candidate` | Agent runtime candidate. |
| `orchestration_candidate` | Orchestration candidate. |
| `cadence_candidate` | Cadence candidate. |
| `ui_candidate` | UI/interface candidate. |
| `manual_harness_candidate` | Manual harness candidate. |
| `coding_harness_candidate` | Coding harness candidate. |
| `review_harness_candidate` | Review harness candidate. |
| `future_adapter_candidate` | Future adapter candidate. |
| `live_connector_candidate` | Live connector candidate. |
| `unknown_candidate` | Unknown candidate; blocked until classified. |

`ExternalCandidateStatus` values:

| ExternalCandidateStatus | Meaning |
| --- | --- |
| `candidate_only` | Candidate metadata only. |
| `not_adopted` | Not adopted. |
| `not_executed` | Not executed. |
| `not_imported` | Not imported. |
| `not_configured` | Not configured. |
| `not_runtime` | Not runtime. |
| `not_dependency_approved` | No dependency approval. |
| `not_provider_auth_approved` | No provider/auth approval. |
| `not_mcp_active` | MCP not active. |
| `not_cadence_active` | Cadence not active. |
| `not_substrate` | Not Cognitive Semantic System substrate. |
| `read_only_metadata_candidate` | Candidate for read-only metadata use only. |
| `requires_external_review` | Requires future external review. |
| `requires_security_review` | Requires future security review. |
| `requires_activation_gate` | Requires future activation gate. |
| `blocked` | Blocked. |
| `unknown` | Unknown and blocked until reviewed. |

## 8. Candidate Inventory Matrix

| Candidate | Observed path or metadata | Inventory status | Candidate kinds | Current status | Allowed P8 use | Blocked P8 use | Required future gate | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Graphify | `0_architecture/governance/agent_platform_graphify_reduced_scope_collision_provenance_remediation_plan.md`; `graphify-out/`; `9_artifacts/` | `present_metadata_document_only`; `graphify-out/` `not_present`; `9_artifacts/` `present_path_not_inspected` | `repository_graph_candidate`; `evidence_graph_candidate`; `architecture_map_candidate`; `generated_evidence_tool_candidate` | `candidate_only`; `not_adopted`; `not_executed`; `not_runtime` | Metadata classification and current Graphify governance citation. | Source of truth, authority, automatic rerun, repo writer, raw output inspection, substrate selection. | Future exact gate for rerun remains blocked. | Generated supporting evidence only. |
| GBrain | `external/sources/gbrain-master` | `not_present` | `memory_architecture_candidate`; `persistent_knowledge_candidate`; `second_brain_substrate_candidate` | `candidate_only`; `not_adopted`; `not_executed`; `not_dependency_approved`; `not_provider_auth_approved`; `not_mcp_active`; `not_cadence_active`; `not_substrate`; `not_runtime` | Path/class metadata and candidate classification. | Execution, import, configuration, runtime, persistent memory, graph/vector DB, automatic retrieval, source content inspection. | P8.7 and future EXT.GB review/hardening gate. | Candidate only. |
| GStack | `external/sources/gstack`; `external/sources/gstack-master` | `not_present`; `exact_path_requires_followup_classification` if future multiple paths appear | `external_source_candidate`; `gbrain_compatibility_candidate`; `skill_stack_candidate`; `bootstrap_layer_candidate`; `agent_workflow_support_candidate` | `candidate_only`; `not_adopted`; `not_executed`; `not_imported`; `not_configured`; `not_dependency_approved`; `not_runtime` | Path/class metadata, GBrain compatibility candidate registration, skill stack candidate registration. | Execution, import, configuration, adoption, dependency approval, runtime, source content inspection. | P8.7 and future EXT.GSTACK review if needed. | `gstack_registered_as_gbrain_compatible_candidate`. |
| Hermes | `external/sources/hermes`; `external/sources/hermes-master` | `not_present`; `exact_path_requires_followup_classification` if future multiple paths appear | `agent_runtime_candidate`; `orchestration_candidate`; `cadence_candidate`; `ui_candidate` | `candidate_only`; `not_adopted`; `not_executed`; `not_runtime`; `not_cadence_active` | Path/class metadata and future UI feasibility classification. | Execution, import, configuration, adoption, runtime, Cadence, automatic dispatch, autonomous orchestration, source content inspection. | P8.8. | UI candidate and runtime candidate must be separated later. |
| OpenCode | `external/sources/opencode`; `external/sources/opencode-master` | `not_present`; `exact_path_requires_followup_classification` if future multiple paths appear | `manual_harness_candidate`; `coding_harness_candidate`; `review_harness_candidate`; `future_adapter_candidate` | H0 user-operated harness; `candidate_only`; `not_adopted`; `not_executed`; `not_runtime` | H0 manual harness classification and future P8.9 boundary requirement. | OpenCode execution from AGENT PLATFORM, adapter execution, automatic task routing, automatic output ingestion, tool execution, MCP/provider/auth automation. | P8.9 for H1 metadata adapter design; future exact gate for H2 controlled execution. | Manual user operation only. |

## 9. Graphify Classification

Graphify candidate use:

| Use | P8.1 classification |
| --- | --- |
| Repository graph | `repository_graph_candidate` |
| Evidence graph | `evidence_graph_candidate` |
| Architecture map | `architecture_map_candidate` |
| Generated evidence reference | GraphifyRef-compatible generated evidence metadata. |
| Read-only evidence provider candidate | Future P8.6 boundary only. |
| Imported evidence candidate | Future evidence boundary only. |

Allowed P8.1 posture: inventory, metadata classification, Graphify Repo Map Summary citation, path presence of generated-output folders, and read-only evidence boundary planning for future P8.6.

Blocked P8.1 posture: Graphify as source of truth, Graphify as authority, Graphify automatic rerun, Graphify deciding architecture, Graphify writing repo state, Graphify raw output inspection, Graphify adoption, and Graphify substrate selection.

Graphify remains generated supporting evidence only, not authority.

## 10. GBrain Classification

GBrain candidate use:

| Use | P8.1 classification |
| --- | --- |
| Memory architecture candidate | `memory_architecture_candidate` |
| Persistent knowledge candidate | `persistent_knowledge_candidate` |
| Second-brain substrate candidate | `second_brain_substrate_candidate` |
| Future Cognitive Semantic System substrate candidate | Candidate only; `not_substrate`. |
| Possible cadence reference candidate | Candidate only; `not_cadence_active`. |

Allowed P8.1 posture: inventory, path/class metadata, candidate classification, link to P6.6 substrate defer posture, and future P8.7 / EXT.GB review requirement.

Blocked P8.1 posture: GBrain runtime adoption, GBrain execution, GBrain import, GBrain configuration, GBrain dependency approval, persistent memory activation, graph/vector DB activation, automatic retrieval into agent context, Cadence activation, and source content inspection without future gate.

GBrain remains candidate only.

## 11. GStack Classification

GStack candidate use:

| Use | P8.1 classification |
| --- | --- |
| External source candidate | `external_source_candidate` |
| GBrain compatibility candidate | `gbrain_compatibility_candidate` |
| Skill stack candidate | `skill_stack_candidate` |
| Bootstrap layer candidate | `bootstrap_layer_candidate` |
| Agent workflow support candidate | `agent_workflow_support_candidate` |

Allowed P8.1 posture: inventory, path/class metadata, GBrain compatibility candidate registration, skill stack candidate registration, and future P8.7 compatibility boundary requirement.

Blocked P8.1 posture: GStack execution, GStack import, GStack configuration, GStack adoption, GStack dependency approval, GStack runtime, GStack source content inspection, and treating GStack as validated because a path exists.

Required outcome: `gstack_registered_as_gbrain_compatible_candidate`.

## 12. Hermes Classification

Hermes candidate use:

| Use | P8.1 classification |
| --- | --- |
| Agent runtime candidate | `agent_runtime_candidate` |
| Orchestration candidate | `orchestration_candidate` |
| Cadence candidate | `cadence_candidate`; `not_cadence_active` |
| Possible interface/UI candidate | `ui_candidate` |

Allowed P8.1 posture: inventory, path/class metadata, future Hermes UI feasibility classification, and future P8.8 boundary requirement.

Blocked P8.1 posture: Hermes runtime activation, Hermes execution, Hermes import, Hermes configuration, Hermes adoption, Cadence activation, automatic dispatch, autonomous orchestration, and source content inspection without future gate.

Hermes UI candidate and Hermes runtime candidate must be separated in later P8.8.

## 13. OpenCode Classification

OpenCode current use: H0 user-operated harness.

OpenCode candidate use:

| Use | P8.1 classification |
| --- | --- |
| Manual external development harness | `manual_harness_candidate` |
| Coding harness candidate | `coding_harness_candidate` |
| Review harness candidate | `review_harness_candidate` |
| Future H1 metadata adapter candidate | `future_adapter_candidate`; design only later. |
| Future H2 controlled execution adapter candidate | Future exact gate only; currently blocked. |

Allowed P8.1 posture: inventory, classification as H0 current manual harness, future P8.9 boundary requirement, and no AGENT PLATFORM execution.

Blocked P8.1 posture: OpenCode execution from AGENT PLATFORM, OpenCode adapter execution, automatic task routing to OpenCode, automatic output ingestion, automatic tool execution, MCP activation, and provider/auth automation.

P8 MVP-0 may generate prompts/packages for OpenCode later, but OpenCode remains manually operated by the user until later gates.

## 14. Source Inspection Rules

| Candidate | Allowed now | Blocked now | Required gate for deep inspection |
| --- | --- | --- | --- |
| Graphify | Governance metadata and curated Graphify Repo Map Summary citation; path checks for generated-output surfaces. | Raw Graphify output inspection, Graphify execution, Graphify rerun, source-of-truth use. | P8.6 and future exact evidence/output gate. |
| GBrain | Path checks and candidate classification. | Source contents, imports, execution, dependency review, runtime probing. | EXT.GB-01 or P8.7-defined external review gate. |
| GStack | Path checks and candidate classification. | Source contents, imports, execution, dependency review, runtime probing. | EXT.GSTACK-01 or P8.7-defined external review gate. |
| Hermes | Path checks and candidate classification. | Source contents, imports, execution, runtime probing, UI activation, Cadence. | P8.8-defined external/interface/runtime review gate. |
| OpenCode | Path checks and H0 harness classification. | Source contents, OpenCode execution, adapter execution, automation. | P8.9-defined harness/adapter review gate. |

Path checks are allowed. Directory names under `external/sources/` are allowed as path/class metadata only when the directory exists. File contents are blocked. Runtime probing, imports, and execution are blocked. Source inspection requires explicit external-source review or later P8 boundary ticket. Product/Siamese source remains blocked. Raw generated outputs remain blocked.

## 15. Installation / Presence Register

| Candidate | Expected path candidates | Observed present paths | Observed absent paths | Exact path decision | Inspection status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Graphify | `graphify-out/`; `9_artifacts/`; current Graphify governance | `9_artifacts/`; `0_architecture/governance/agent_platform_graphify_reduced_scope_collision_provenance_remediation_plan.md` | `graphify-out/` | Curated governance record present; raw output path absent; artifact root present. | Governance metadata inspected; `9_artifacts/` contents not inspected. | Presence does not imply Graphify adoption. |
| GBrain | `external/sources/gbrain-master` | None | `external/sources/gbrain-master` | `not_present` | No source inspected. | Absence does not reject future candidate review. |
| GStack | `external/sources/gstack`; `external/sources/gstack-master` | None | Both paths absent. | `not_present`; future multiple paths would require `exact_path_requires_followup_classification`. | No source inspected. | Registered as GBrain-compatible candidate by classification only. |
| Hermes | `external/sources/hermes`; `external/sources/hermes-master` | None | Both paths absent. | `not_present`; future multiple paths would require `exact_path_requires_followup_classification`. | No source inspected. | UI/runtime separation deferred to P8.8. |
| OpenCode | `external/sources/opencode`; `external/sources/opencode-master` | None | Both paths absent. | `not_present`; future multiple paths would require `exact_path_requires_followup_classification`. | No source inspected. | H0 user-operated harness posture remains. |

Presence does not imply adoption. Absence does not imply rejection. Ambiguous path requires follow-up classification.

## 16. Gate Requirement Matrix

| Candidate | Future action | Required gate or ticket | Current status |
| --- | --- | --- | --- |
| Graphify | Read-only evidence boundary | P8.6 | Future only. |
| Graphify | Rerun | Future exact gate | Currently blocked. |
| Graphify | Authority/adoption | Rejected / blocked | Not allowed. |
| GBrain | Source review | EXT.GB-01 or P8.7-defined gate | Currently blocked. |
| GBrain/GStack | Compatibility evaluation | P8.7 | Future only. |
| GBrain | Runtime / persistent memory | Future substrate / security / storage gates | Currently blocked. |
| GStack | Source review | EXT.GSTACK-01 or P8.7-defined gate | Currently blocked. |
| Hermes | UI feasibility review | P8.8 | Future only. |
| Hermes | Runtime / Cadence | Future exact gate | Currently blocked. |
| OpenCode | H1 metadata adapter design | P8.9 | Future only. |
| OpenCode | H2 controlled execution adapter | Future exact gate after P8.9/P8.5 | Currently blocked. |
| Provider/auth/API/MCP | Activation | P8.5 plus future exact activation gate | Currently blocked. |
| Product/Siamese | Product-bound work | P4 / GT-09 equivalent product readiness path | Currently blocked. |

## 17. Interface With P8.2 / P8.3 / P8.4 / P8.5

| Peer | Interface | Current P8.1 status |
| --- | --- | --- |
| P8.2 | Candidate inventory informs MVP interaction surface options; Hermes UI feasibility remains candidate only; OpenCode H0 manual harness informs interaction loop. | P8.2 present and consumed as optional metadata. |
| P8.3 | Candidate inventory informs schema needs for HarnessInputPackage, HarnessOutputPackage, ExternalCandidateRecord, EvidenceRef, SourceRef, and candidate refs. | P8.3 absent; `pending_P8.3_schema_candidates_alignment`. |
| P8.4 | Candidate inventory informs local workspace state model; external source state remains metadata-only; no external source content is persisted by default. | P8.4 present and consumed as optional metadata. |
| P8.5 | Candidate inventory informs activation gate model; P8.1 does not define activation levels alone; external candidates map to P8-L0 through P8-L5 after P8.5. | P8.5 present and consumed as optional metadata. |

P8.1 may proceed after P8.0 even when P8.3 is absent because P8.1-P8.5 may run in parallel.

## 18. Evidence / Validation / Security Interfaces

Evidence interface:

| Rule | P8.1 posture |
| --- | --- |
| Candidate classification cites EvidenceRef-compatible governance/path metadata. | Preserved. |
| GraphifyRef is supporting generated evidence only. | Preserved. |
| GBrainCandidateRef and GStackCandidateRef are candidate notation only. | Preserved. |
| Evidence supports; it does not decide. | Preserved. |

Validation interface:

| Rule | P8.1 posture |
| --- | --- |
| P8.1 does not run validation. | Preserved. |
| Future validation may check candidate records, path classifications, and no-adoption invariants. | Future only. |
| Validation evaluates; governance decides. | Preserved. |

Security interface:

| Rule | P8.1 posture |
| --- | --- |
| External candidates remain security-sensitive until classified. | Preserved. |
| No secrets or credentials may enter candidate records. | Preserved. |
| Source inspection remains blocked. | Preserved. |
| Security constrains; it does not activate. | Preserved. |

## 19. Retention / Rollback / Incident Posture

P8.1 creates only governance metadata. No runtime state is created. No external source content is retained. No raw generated output is retained. No provider output is retained. No local connector payload is retained.

If forbidden content is encountered, stop and record safe metadata only. Candidate records must include retention and incident posture for future review.

| Posture | P8.1 result |
| --- | --- |
| Retention | Governance metadata only. |
| Rollback | Exact target document can be reviewed/reverted by the user if needed; no rollback automation. |
| Incident | Safe metadata only if a blocked surface is encountered. |
| Generated outputs | Raw generated outputs not inspected or retained. |
| External source contents | Not inspected or retained. |
| Secrets/credentials | Not inspected or retained. |

## 20. Human Approval Requirements

Human approval is required before deep source inspection, adopting any external candidate, executing any external candidate, creating adapters, provider/auth/API/MCP activation, product/Siamese source work, and Git mutation.

P8.1 itself does not approve these actions. ApprovalRef is not approval. Candidate status is not approval. Path presence is not approval.

## 21. Stop Rules

STOP if P8.0 boundary document is missing and report `p8_0_missing_boundary`.

STOP if inventory requires reading external source contents, recursive external source inspection, importing or executing Graphify, GBrain, GStack, Hermes, or OpenCode, provider/auth/API/MCP, credential use, API/MCP calls, tool execution, agent execution, OpenCode execution from AGENT PLATFORM, Graphify rerun/adoption, GBrain/GStack/Hermes runtime activation, Cadence, product/Siamese source inspection, source loading, raw generated output inspection, secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, validation execution, tests, CI, scripts, builds, persistence, vector DB, graph DB, embeddings, substrate selection, generated output tracking, source tracking expansion, publication, Git mutation, or any work beyond path/class metadata scope.

## 22. Future Validation Targets

Future validation targets, not executed:

| Target | Purpose |
| --- | --- |
| ExternalCandidateRecord required fields completeness | Check candidate record shape. |
| Candidate kind vocabulary conformance | Check kind values. |
| Candidate status vocabulary conformance | Check status values. |
| Graphify classification completeness | Check Graphify inventory and blockers. |
| GBrain classification completeness | Check GBrain inventory and blockers. |
| GStack classification completeness | Check GStack inventory and blockers. |
| Hermes classification completeness | Check Hermes inventory and blockers. |
| OpenCode classification completeness | Check OpenCode inventory and blockers. |
| GStack registered as GBrain-compatible candidate invariant | Check `gstack_registered_as_gbrain_compatible_candidate`. |
| no external runtime adoption invariant | Check `no_external_runtime_adoption`. |
| no external source content inspection invariant | Check contents were not inspected. |
| path presence is not adoption invariant | Check no adoption inference. |
| path presence is not content review invariant | Check no review inference. |
| Graphify support-only invariant | Check Graphify remains generated evidence only. |
| GBrain candidate-only invariant | Check GBrain remains candidate only. |
| GStack candidate-only invariant | Check GStack remains candidate only. |
| Hermes runtime blocked invariant | Check Hermes runtime remains blocked. |
| OpenCode H0 manual harness invariant | Check OpenCode remains H0 manual. |
| required future gates completeness | Check P8.6-P8.9 and other gates. |
| P8.2/P8.3/P8.4/P8.5 alignment checks | Check peer alignment state. |
| P8.6/P8.7/P8.8/P8.9 readiness checks | Future boundary readiness only. |

## 23. Future Hardening Candidates

Future tickets, not started:

| Candidate | Purpose |
| --- | --- |
| EXTINV-HARD-01 - ExternalCandidateRecord Schema Alignment | Harden record shape. |
| EXTINV-HARD-02 - External Source Path Verification Contract | Harden path-only verification rules. |
| EXTINV-HARD-03 - External Candidate Gate Matrix Hardening | Harden gate routing. |
| EXTINV-HARD-04 - Graphify Evidence Candidate Classification Hardening | Harden Graphify support-only classification. |
| EXTINV-HARD-05 - GBrain / GStack Compatibility Classification Hardening | Harden memory/compatibility candidate classification. |
| EXTINV-HARD-06 - Hermes UI / Runtime Candidate Classification Hardening | Harden Hermes UI/runtime separation. |
| EXTINV-HARD-07 - OpenCode H0/H1/H2 Harness Classification Hardening | Harden OpenCode harness levels. |
| EXTINV-HARD-08 - No External Runtime Adoption Invariant Design | Harden no-adoption invariant. |
| EXTINV-HARD-09 - External Source Inspection Stop Rules Hardening | Harden inspection stop rules. |
| EXTINV-HARD-10 - P8.6-P8.9 Boundary Preparation Contract | Harden boundary handoff package. |

Optional future external review candidates, not started:

| Candidate | Purpose |
| --- | --- |
| EXT.GB-01 - GBrain External Source Intake / Read-Only Capability Review | Future GBrain review. |
| EXT.GSTACK-01 - GStack External Source Intake / Compatibility Review | Future GStack review. |
| EXT.HERMES-01 - Hermes Interface / Runtime External Review | Future Hermes review. |
| EXT.OPENCODE-01 - OpenCode Harness / Adapter External Review | Future OpenCode review. |

## 24. Created / Modified / Not Created Register

Created:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_external_source_inventory_graphify_gbrain_gstack_hermes_opencode.md` | Created as P8.1 inventory/classification. |

Modified:

| Area | Status |
| --- | --- |
| Other files | None modified by P8.1. |

Not created / not approved:

| Area | Status |
| --- | --- |
| P8.0, P8.2, P8.3, P8.4, P8.5, P8.6, P8.7, P8.8, P8.9, P8.10, P8.11, P8.12+, P8.R, P9, P4, EXT.* files | Not created by this ticket. |
| Runtime implementation | Not created. |
| Adapter implementation / executable adapter | Not created. |
| External source adoption/content inspection | Not approved or performed. |
| Graphify execution/rerun/adoption/authority/repo-state writing | Not approved or performed. |
| GBrain execution/import/configuration/adoption/runtime/persistent memory | Not approved or performed. |
| GStack execution/import/configuration/adoption/runtime | Not approved or performed. |
| Hermes execution/import/configuration/adoption/runtime/UI activation/Cadence | Not approved or performed. |
| OpenCode execution from AGENT PLATFORM / adapter execution | Not approved or performed. |
| Provider/auth/API/MCP activation, credential use, API calls, MCP calls | Not approved or performed. |
| Tool execution, agent execution, live connector activation | Not approved or performed. |
| Source loading/source inspection/product or Siamese source inspection | Not approved or performed. |
| Raw generated output inspection | Not performed. |
| Secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys | Not inspected. |
| Validation execution, tests, CI, scripts, builds | Not run. |
| Security enforcement activation | Not created. |
| Persistence DB, vector DB, embeddings, graph DB, substrate selection | Not created or selected. |
| Telemetry, event streaming, generated output tracking, source tracking expansion | Not created or approved. |
| Publication / Git mutation | Not performed. |

## 25. Recommended Next Ticket

After P8.1, if P8.2-P8.5 are not complete, continue Round 1:

| Ticket | Current status | Recommendation |
| --- | --- | --- |
| P8.2 - MVP Interaction Surface Architecture | Present. | Do not modify from P8.1. |
| P8.3 - Core Workflow Schema Candidates | Absent. | Continue Round 1 after P8.2 or in parallel if explicitly assigned. |
| P8.4 - Local Workspace / State Model | Present. | Do not modify from P8.1. |
| P8.5 - Security / Activation Gate Model | Present. | Do not modify from P8.1. |

Recommended actual: P8.3 - Core Workflow Schema Candidates, because P8.2, P8.4, and P8.5 are already present.

After P8.1 and P8.5 are complete, Round 2 may later proceed only by explicit instruction:

| Ticket | Purpose |
| --- | --- |
| P8.6 | Graphify Read-Only Evidence Boundary. |
| P8.7 | GBrain / GStack Memory Compatibility Boundary. |
| P8.8 | Hermes Interface / Runtime Candidate Boundary. |
| P8.9 | OpenCode Harness Upgrade Boundary. |

Do not start P8.6-P8.9 from this ticket. Do not start P8.10 or implementation tickets from this ticket.

## 26. Final Verdict

| Question | Answer |
| --- | --- |
| What did P8.1 create? | `0_architecture/governance/agent_platform_external_source_inventory_graphify_gbrain_gstack_hermes_opencode.md`. |
| What external candidates were inventoried? | Graphify, GBrain, GStack, Hermes, and OpenCode. |
| What paths were checked? | `external/sources/`, `external/sources/gbrain-master`, `external/sources/gstack`, `external/sources/gstack-master`, `external/sources/hermes`, `external/sources/hermes-master`, `external/sources/opencode`, `external/sources/opencode-master`, `graphify-out/`, `9_artifacts/`, and Graphify Repo Map Summary. |
| Which candidates were present? | Graphify curated metadata document was present; `9_artifacts/` was present as generated/local-only path. No external candidate source path was present. |
| Which candidates were absent? | GBrain, GStack, Hermes, and OpenCode candidate paths were absent; `external/sources/` and `graphify-out/` were absent. |
| Which candidates have ambiguous paths? | GStack, Hermes, and OpenCode have multiple plausible future path candidates; all are absent now, and future presence would require `exact_path_requires_followup_classification`. |
| What was inspected? | Governance documents, security/CSS documents, README, `.gitignore`, `.graphifyignore`, path presence metadata, and curated Graphify Repo Map Summary. |
| What was not inspected? | External source contents, product/Siamese source, raw generated outputs, raw Graphify outputs, secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, runtime state. |
| How is Graphify classified? | Repository graph / evidence graph / architecture map / generated evidence tool candidate; generated supporting evidence only, not authority. |
| How is GBrain classified? | Memory architecture / persistent knowledge / second-brain substrate candidate; candidate only, not adopted and not runtime. |
| How is GStack classified? | External source / GBrain compatibility / skill stack / bootstrap layer / agent workflow support candidate. |
| Is GStack registered as GBrain-compatible candidate? | Yes: `gstack_registered_as_gbrain_compatible_candidate`. |
| How is Hermes classified? | Agent runtime / orchestration / Cadence / UI candidate; candidate only, not runtime and not Cadence-active. |
| How is OpenCode classified? | H0 user-operated manual/coding/review harness candidate and future adapter candidate; not integrated runtime. |
| Was any external source adopted? | No: `no_external_runtime_adoption`. |
| Was any external source executed? | No. All candidates are `not_executed`. |
| Was any external source imported or configured? | No. |
| Was Graphify rerun or adopted? | No. |
| Was GBrain runtime activated? | No. |
| Was GStack runtime activated? | No. |
| Was Hermes runtime activated? | No. |
| Was OpenCode executed by AGENT PLATFORM? | No. |
| Was provider/auth/API/MCP activated? | No. |
| Was product/Siamese source inspected? | No. |
| Was any external source content inspected? | No. |
| Was any source loading approved? | No. |
| Were secrets or credentials inspected? | No. |
| Was vector DB, graph DB, persistence, or substrate selected? | No. |
| What gates are required before future deep inspection? | P8.6 for Graphify boundary, P8.7 for GBrain/GStack compatibility, P8.8 for Hermes, P8.9 for OpenCode, EXT.* review gates where applicable, P8.5/activation gates for any execution/provider/MCP/runtime, and P4/GT-09 for product/Siamese work. |
| What P8 peer alignments are pending? | `pending_P8.3_schema_candidates_alignment`. |
| What is the recommended next ticket? | P8.3 - Core Workflow Schema Candidates. |

Final markers:

```text
external_source_inventory_ready
gstack_registered_as_gbrain_compatible_candidate
no_external_runtime_adoption
```

Stop after P8.1. Do not start P8.2, P8.3, P8.4, P8.5, P8.6, P8.7, P8.8, P8.9, P8.10, P8.11, P8.12+, P8.R, P9, P4, EXT.*, implementation, activation, runtime integration, source inspection, or publication from this ticket.
