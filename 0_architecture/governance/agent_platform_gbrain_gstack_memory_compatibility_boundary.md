# GBrain / GStack Memory Compatibility Boundary

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | GBrain / GStack Memory Compatibility Boundary |
| Ticket | P8.7 |
| Status | Accepted GBrain / GStack memory compatibility boundary |
| Date | 2026-07-06 |
| Scope | Canonical GBrain / GStack memory compatibility boundary for AGENT PLATFORM / Siamese P8 MVP planning. |
| Authority | Memory compatibility boundary only, not GBrain adoption, GStack adoption, runtime activation, memory runtime activation, persistent memory activation, automatic retrieval, source indexing, graph/vector DB implementation, embedding generation, database/persistence, Cadence, provider/auth/API/MCP activation, source content inspection, product/Siamese source inspection, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Required prerequisites | P8.0, P8.1, and P8.5 present. |
| Related documents | P8.0, P8.1, P8.5, P8.2, P8.3, P8.4, P8.6, P8.8, P8.9, P7.R, P7.0.D, P7.0.0, P6.6, P6.7, P5.R, P3.BR, P2.KR, P2.2, P2.3, P1.5, CSS ADR/audit, S-03, S-04, README.md, `.gitignore`, `.graphifyignore`. |
| Output | GBrain / GStack memory compatibility boundary ready. |
| Output markers | `gbrain_gstack_memory_compatibility_boundary_ready`; `gbrain_registered_as_memory_architecture_candidate`; `gstack_registered_as_gbrain_compatible_skill_stack_candidate`; `future_memory_mvp_candidate_defined`; `no_memory_runtime_adoption`; `no_persistent_memory_activation`; `no_graph_vector_db_activation`; `no_cadence_activation` |

P8.7 proceeds because P8.0, P8.1, and P8.5 are present. The stop markers `p8_0_missing_boundary`, `p8_1_missing_external_inventory`, and `p8_5_missing_security_activation_gate_model` were not triggered.

## 2. Purpose

P8.7 defines the compatibility boundary between GBrain and GStack.

P8.7 classifies GBrain as memory architecture / persistent knowledge / second-brain / future Cognitive Semantic System substrate candidate.

P8.7 classifies GStack as GBrain-compatible skill stack / bootstrap layer / agent workflow support candidate.

P8.7 maps what each candidate may inform, what can be inspected now, what remains blocked, and what future gates are required before deeper inspection, adoption, runtime, dependency approval, memory persistence, retrieval, graph/vector DB, provider/auth/MCP, or Cadence.

P8.7 proposes a future memory MVP candidate as design posture only. P8.7 does not activate GBrain, GStack, memory runtime, retrieval, persistence, adapters, or substrate.

## 3. Current Posture

| Area | Current posture | P8.7 interpretation | Blocked interpretation |
| --- | --- | --- | --- |
| AGENT PLATFORM | P8 Platform MVP / Interaction Layer. | Boundary/design only. | Runtime platform. |
| P8.0 | Present. | Defines scope and external integration boundary. | Runtime approval. |
| P8.1 | Present. | Inventories external candidates and records GStack as GBrain-compatible candidate. | Source review or adoption. |
| P8.5 | Present. | Defines security / activation gates and blocked surfaces. | Enforcement or execution. |
| P8.7 | Boundary/design only. | Consumes P8.1 and P8.5. | Implementation or runtime. |
| MVP-0 | Local interactive manual workflow assistant. | Does not require GBrain/GStack runtime. | Autonomous assistant. |
| Persistent memory | Not approved. | Future candidate only. | Active memory store. |
| Graph/vector DB | Not approved. | Future candidate only. | Active substrate. |
| Automatic retrieval | Not approved. | Manual ContextPack / MemoryManifest only. | Automatic context injection. |
| P6.6 substrate posture | Cognitive Semantic System substrate deferred. | Preserved. | Substrate selection. |
| GBrain | Candidate only. | Memory architecture candidate. | Runtime or selected substrate. |
| GStack | Candidate only. | GBrain-compatible skill stack candidate. | Runtime, dependency approval, or compatibility proof. |
| Compatibility | Inventory-supported candidate relationship. | Unverified unless future exact external reviews exist. | Approval, adoption, dependency trust, or runtime readiness. |
| Product/Siamese | Product vision deferred. | Product/Siamese source remains blocked. | Product source memory. |
| External runtime adoption | Not approved. | `no_memory_runtime_adoption`. | Adoption by path presence. |

## 4. Inputs Reviewed

Inputs are consumed as governance/path/class metadata only. P8.7 does not inspect GBrain/GStack source contents, product source, raw generated outputs, secrets, credentials, configs, token stores, browser auth, local credential stores, API keys, or runtime state.

| Input | Present | Consumed_as | Memory_boundary_relevance | Limitations | Pending_alignment |
| --- | --- | --- | --- | --- | --- |
| P8.0 Platform MVP Scope / External Integration Boundary | Yes | Required P8 boundary | Defines P8 MVP scope, external candidates, MVP-0, and no-runtime posture. | Not modified. | None. |
| P8.1 External Source Inventory / Classification | Yes | Required external inventory | Classifies GBrain and GStack and records path/class metadata. | Inventory only, not source review. | None. |
| P8.5 Security / Activation Gate Model | Yes | Required security/activation gate posture | Defines P8-L0 through P8-L5, external inspection gates, blocked surfaces, and activation blockers. | Gate model is not enforcement. | None. |
| P8.2 MVP Interaction Surface Architecture | Yes | Optional peer metadata | Confirms MVP-0 interaction is manual and no automatic retrieval/UI execution is approved. | Not modified. | None. |
| P8.3 Core Workflow Schema Candidates | Yes | Optional peer metadata | Supplies schema-candidate posture for refs and packages; schema is not runtime. | Not modified. | None. |
| P8.4 Local Workspace / State Model | Yes | Optional peer metadata | Confirms no persistent memory, no automatic retrieval, and local-only state posture. | Historical sibling-presence notes may be stale; P8.7 uses current checks. | None. |
| P8.6 Graphify Read-Only Evidence Boundary | Yes | Optional P8 peer metadata | Aligns GraphifyRef evidence-only boundary and no Graphify runtime/rerun posture. | Not modified. | None. |
| P8.8 Hermes Interface / Runtime Candidate Boundary | Yes | Optional P8 peer metadata | Aligns Hermes interface/runtime/Cadence candidate boundary. | Historical P8.7-absent note exists in P8.8 because P8.7 was created later; not modified. | None. |
| P8.9 OpenCode Harness Upgrade Boundary | Yes | Optional P8 peer metadata | Aligns OpenCode H0/H1/H2 harness boundary and manual harness posture. | Historical P8.7/P8.8/P8.6 absence notes exist in P8.9 because these peers were created later; not modified. | None. |
| EXT.GB-01 exact P8.7 optional path | No | Optional external review | Would support source-verified GBrain capability review. | Exact optional review path absent; source claims remain candidate-level. | `pending_EXT.GB_01_gbrain_external_source_review` |
| EXT.GSTACK-01 exact P8.7 optional path | No | Optional external review | Would support source-verified GStack compatibility review. | Exact optional review path absent; source claims remain candidate-level. | `pending_EXT.GSTACK_01_gstack_external_source_review` |
| P7.R Manual Agentic Workflow Planning Closure | Yes | Manual workflow closure | Confirms manual workflow maturity and no runtime activation. | No P7 work started. | None. |
| P7.0.D Manual Context / Memory Manifest Strategy | Yes | Memory manifest baseline | Defines MemoryManifest, ContextPack, EvidencePack, refs, freshness/stale/missing markers, and GBrainCandidateRef as candidate notation only. | No active retrieval or persistent memory. | None. |
| P7.0.0 Agent-Native Organization Research Carry-Forward | Yes | Conceptual pattern set | Supplies task graph, blackboard, cells, routing, and memory fabric as conceptual inputs. | Conceptual only. | None. |
| P7.0.F Reviewer Mesh / Immune Safeguards Contract | Yes | Review boundary metadata | Supplies contradiction and evidence-conflict handling concepts. | No automatic review/runtime. | None. |
| P7.0.G Manual Integrator / Commit Advisory Protocol | Yes | Integration/Git advisory metadata | Preserves exact-path Git advisory and no mutation. | No Git mutation. | None. |
| P6.7 Operational Readiness Audit | Yes | Operational readiness baseline | Confirms AGENT PLATFORM remains non-runtime and substrate not selected. | Historical EXT.GB language is not P8.7 exact optional review presence. | None. |
| P6.6 Cognitive Semantic System Substrate Decision / Defer Record | Yes | Substrate defer baseline | Keeps Cognitive Semantic System substrate deferred and GBrain not adopted. | No substrate selection. | None. |
| P5.R Minimal Active Agent Platform Audit | Yes | AL-1 skeleton audit | Confirms implementation skeletons are not activation. | No skeleton activation. | None. |
| P3.BR Activation Decision Reconciliation Closure | Yes | Activation decision baseline | Preserves provider/tool/agent and GBrain/Hermes/Cadence blockers. | Decision is not execution. | None. |
| P2.KR Knowledge / Retrieval Architecture Reconciliation Closure | Yes | Knowledge/retrieval baseline | Confirms markdown canonical governance memory, graph/vector candidates only, and Level 5 GBrain/Hermes/Cadence blocked. | No retrieval runtime. | None. |
| P2.1 Shared Metadata Vocabulary Alignment | Yes | Vocabulary baseline | Supplies status/posture/ref vocabulary. | Vocabulary is not permission. | None. |
| P2.2 EvidenceRef Contract | Yes | Evidence vocabulary | Evidence supports; it does not decide. | No evidence promotion. | None. |
| P2.3 Audit / Retention / Rollback Baseline | Yes | Lifecycle baseline | Supplies retention, rollback, local-only, generated-output, publication, and tracking blockers. | No persistence or tracking. | None. |
| P1.5 Cognitive Semantic System Prototype Hardening | Yes | Semantic metadata baseline | Confirms semantic records are metadata only and no graph/vector/database/ontology runtime is approved. | No semantic runtime. | None. |
| CSS ADR / audit | Yes | Naming/substrate posture | Confirms Cognitive Semantic System name and substrate neutrality. | No substrate decision. | None. |
| S-03 Local-only / Secrets / Credentials Policy | Yes | Local-only/secrets policy | Secrets/credentials/local-only/external/product/generated outputs remain excluded from memory. | No secrets or credentials inspected. | None. |
| S-04 Tool / Shell / Network / MCP Execution Policy | Yes | Execution policy | Blocks tools, shell, network, APIs, MCP, databases, package managers, tests, builds, and external execution by default. | No execution run. | None. |
| README.md | Yes | Repository orientation | Confirms AGENT PLATFORM workspace purpose. | No runtime effect. | None. |
| `.gitignore` | Yes | Ignore posture metadata | Confirms ignored local-only/product/external/artifact/secret/provider-auth patterns. | Not modified; ignore is not security. | None. |
| `.graphifyignore` | Yes | Graphify boundary metadata | Confirms default-deny Graphify input boundary and excludes `4_external/`, `9_artifacts/`, `graphify-out/`, secrets, and docs. | Not modified; not permission to run Graphify. | None. |
| GBrain path metadata | No | Path presence metadata | `external/sources/gbrain-master` checked as path/class metadata only. | Path absent; no content inspected. | `not_present` |
| GStack path metadata | No | Path presence metadata | `external/sources/gstack` and `external/sources/gstack-master` checked as path/class metadata only. | Paths absent; no content inspected. | `not_present`; future multiple paths require `exact_path_requires_followup_classification` |

## 5. Dependency Posture

| Dependency | Required_for_P8.7 | Consumed_posture | Boundary_implication | Blocker_if_absent |
| --- | --- | --- | --- | --- |
| P8.0 | Yes | Present required scope boundary. | Allows P8.7 as P8 boundary/design only. | STOP with `p8_0_missing_boundary`. |
| P8.1 | Yes | Present required external inventory. | Supplies GBrain/GStack candidate records and path/class posture. | STOP with `p8_1_missing_external_inventory`. |
| P8.5 | Yes | Present required security/activation gate model. | Supplies P8-L0 design ceiling and activation blockers. | STOP with `p8_5_missing_security_activation_gate_model`. |
| P8.2 | No | Present optional peer. | Memory candidate posture may inform manual memory UX. | If absent: `pending_P8.2_interaction_surface_alignment`. |
| P8.3 | No | Present optional peer. | P8.7 objects may become schema candidates. | If absent: `pending_P8.3_schema_candidates_alignment`. |
| P8.4 | No | Present optional peer. | Memory MVP-0 aligns with local workspace/state model. | If absent: `pending_P8.4_local_workspace_state_alignment`. |
| P8.6 | No | Present optional peer. | Graphify evidence boundary alignment available. | If absent: `pending_P8.6_graphify_boundary_alignment`. |
| P8.8 | No | Present optional peer. | Hermes/Cadence boundary alignment available. | If absent: `pending_P8.8_hermes_boundary_alignment`. |
| P8.9 | No | Present optional peer. | OpenCode harness upgrade boundary alignment available. | If absent: `pending_P8.9_opencode_boundary_alignment`. |
| EXT.GB-01 | No | Exact optional P8.7 path absent. | GBrain source-verified capability remains unavailable. | `pending_EXT.GB_01_gbrain_external_source_review`; blocks source-verified compatibility, adoption, dependency approval, and runtime/substrate selection. |
| EXT.GSTACK-01 | No | Exact optional P8.7 path absent. | GStack source-verified compatibility remains unavailable. | `pending_EXT.GSTACK_01_gstack_external_source_review`; blocks source-verified compatibility, adoption, dependency approval, and runtime/skill activation. |
| P6.6 | Yes as baseline | Present substrate-defer posture. | Cognitive Semantic System substrate remains deferred. | Substrate posture would be unresolved. |
| P7.0.D | Yes as baseline | Present manual memory manifest posture. | MemoryManifest remains manual and metadata-only. | Manual memory baseline would be incomplete. |
| P2.KR | Yes as baseline | Present knowledge/retrieval closure. | Markdown full-read remains canonical; vector/graph/retrieval remain candidates. | Retrieval boundary would be unresolved. |
| S-03/S-04 | Yes as baseline | Present local-only/secrets and execution policies. | Secrets, credentials, tool/network/MCP/database/package execution remain blocked. | Security/execution posture would be unresolved. |

Missing P8.2/P8.3/P8.4/P8.6/P8.8/P8.9 does not block P8.7, but must be reconciled by P8.10 where applicable. In current checks P8.2, P8.3, P8.4, P8.6, P8.8, and P8.9 are present.

## 6. GBrain Candidate Classification

`GBrainCandidateRecord` is the canonical GBrain candidate object.

| Field | Meaning |
| --- | --- |
| `candidate_id` | Stable candidate identifier. |
| `candidate_name` | Human-readable candidate name. |
| `observed_paths` | Exact path candidates checked as metadata only. |
| `inventory_status` | Path/class metadata status. |
| `candidate_classes` | GBrain candidate classes. |
| `memory_architecture_posture` | MemoryArchitectureCandidate posture. |
| `persistent_knowledge_posture` | Persistent knowledge candidate posture. |
| `second_brain_posture` | Second-brain candidate posture. |
| `cognitive_semantic_system_posture` | Future Cognitive Semantic System substrate candidate posture. |
| `substrate_posture` | Substrate posture; current value `not_substrate`. |
| `runtime_posture` | Runtime posture; current value `not_runtime`. |
| `execution_posture` | Execution posture; current value `not_executed`. |
| `import_posture` | Import posture; current value `not_imported`. |
| `configuration_posture` | Configuration posture; current value `not_configured`. |
| `dependency_posture` | Dependency posture; current value `not_dependency_approved`. |
| `provider_auth_posture` | Provider/auth posture; current value `not_provider_auth_approved`. |
| `mcp_posture` | MCP posture; current value `not_mcp_active`. |
| `cadence_posture` | Cadence posture; current value `not_cadence_active`. |
| `persistence_posture` | Persistence posture; current value `no_persistent_memory_activation`. |
| `retrieval_posture` | Retrieval posture; current value no automatic retrieval. |
| `source_inspection_posture` | SourceInspectionPosture; current value source inspection blocked. |
| `security_posture` | Security posture and policy constraints. |
| `retention_posture` | Future retention posture only. |
| `rollback_posture` | Future rollback posture only. |
| `incident_posture` | Future incident posture only. |
| `allowed_p8_use` | Allowed P8.7 candidate-level use. |
| `blocked_p8_use` | Blocked uses. |
| `required_future_gates` | Gates required before expansion. |
| `adoption_blockers` | AdoptionBlocker values. |
| `limitations` | Known limitations. |

Current `GBrainCandidateRecord`:

| Field | Value |
| --- | --- |
| `candidate_id` | `gbrain_candidate` |
| `candidate_name` | GBrain |
| `observed_paths` | `external/sources/gbrain-master` |
| `inventory_status` | `not_present` |
| `candidate_classes` | `memory_architecture_candidate`; `persistent_knowledge_candidate`; `second_brain_substrate_candidate`; `cognitive_semantic_system_substrate_candidate`; `possible_cadence_reference_candidate`; `external_source_candidate`; `candidate_only` |
| `memory_architecture_posture` | `MemoryArchitectureCandidate`; `gbrain_registered_as_memory_architecture_candidate` |
| `persistent_knowledge_posture` | Candidate only; not persistent memory. |
| `second_brain_posture` | Candidate only; not adopted second brain. |
| `cognitive_semantic_system_posture` | Future candidate only; P6.6 substrate remains deferred. |
| `substrate_posture` | `not_substrate` |
| `runtime_posture` | `not_runtime` |
| `execution_posture` | `not_executed` |
| `import_posture` | `not_imported` |
| `configuration_posture` | `not_configured` |
| `dependency_posture` | `not_dependency_approved` |
| `provider_auth_posture` | `not_provider_auth_approved` |
| `mcp_posture` | `not_mcp_active` |
| `cadence_posture` | `not_cadence_active` |
| `persistence_posture` | `no_persistent_memory_activation` |
| `retrieval_posture` | No automatic context retrieval, automatic memory retrieval, or live retrieval. |
| `source_inspection_posture` | Source content inspection blocked until future exact external review gate. |
| `allowed_p8_use` | Classify candidate; map conceptual memory compatibility; define future gate requirements; define future memory MVP candidate posture; consume EXT.GB-01 only if exact optional path is present. |
| `blocked_p8_use` | Source content inspection; execution/import/configuration; dependency approval; runtime adoption; persistent memory activation; automatic retrieval; graph/vector DB; embeddings; Cadence; provider/auth/MCP; product/source ingestion. |
| `required_future_gates` | EXT.GB-01 exact source intake review; P8.5 activation alignment; security/secrets review; dependency/license review; retention/rollback/incident review; human approval; P8.10/P8.11 synthesis before implementation. |
| `adoption_blockers` | `AdoptionBlocker: source_review_missing`; `AdoptionBlocker: dependency_review_missing`; `AdoptionBlocker: security_review_missing`; `AdoptionBlocker: persistence_review_missing`; `AdoptionBlocker: activation_gate_missing`; `AdoptionBlocker: substrate_deferred`. |
| `limitations` | Path absent; exact optional EXT.GB-01 P8.7 review absent; compatibility claims are candidate-level only. |

Required GBrain posture: `not_adopted`, `not_executed`, `not_imported`, `not_configured`, `not_runtime`, `not_dependency_approved`, `not_provider_auth_approved`, `not_mcp_active`, `not_cadence_active`, and `not_substrate`.

Do not use as current accepted names: GBrain runtime, GBrain adopted memory, GBrain selected substrate, GBrain dependency approved, GBrain provider/auth approved, GBrain MCP active, or GBrain Cadence active.

## 7. GStack Candidate Classification

`GStackCandidateRecord` is the canonical GStack candidate object.

| Field | Meaning |
| --- | --- |
| `candidate_id` | Stable candidate identifier. |
| `candidate_name` | Human-readable candidate name. |
| `observed_paths` | Exact path candidates checked as metadata only. |
| `inventory_status` | Path/class metadata status. |
| `candidate_classes` | GStack candidate classes. |
| `gbrain_compatibility_posture` | GBrain compatibility candidate posture. |
| `skill_stack_posture` | SkillStackCandidate posture. |
| `bootstrap_layer_posture` | Bootstrap layer candidate posture. |
| `agent_workflow_support_posture` | Agent workflow support candidate posture. |
| `runtime_posture` | Runtime posture; current value `not_runtime`. |
| `execution_posture` | Execution posture; current value `not_executed`. |
| `import_posture` | Import posture; current value `not_imported`. |
| `configuration_posture` | Configuration posture; current value `not_configured`. |
| `dependency_posture` | Dependency posture; current value `not_dependency_approved`. |
| `provider_auth_posture` | Provider/auth posture; current value `not_provider_auth_approved`. |
| `mcp_posture` | MCP posture; current value `not_mcp_active`. |
| `cadence_posture` | Cadence posture; current value `not_cadence_active`. |
| `persistence_posture` | Persistence posture; current value no persistent memory. |
| `source_inspection_posture` | SourceInspectionPosture; current value source inspection blocked. |
| `security_posture` | Security posture and policy constraints. |
| `retention_posture` | Future retention posture only. |
| `rollback_posture` | Future rollback posture only. |
| `incident_posture` | Future incident posture only. |
| `allowed_p8_use` | Allowed P8.7 candidate-level use. |
| `blocked_p8_use` | Blocked uses. |
| `required_future_gates` | Gates required before expansion. |
| `adoption_blockers` | AdoptionBlocker values. |
| `limitations` | Known limitations. |

Current `GStackCandidateRecord`:

| Field | Value |
| --- | --- |
| `candidate_id` | `gstack_candidate` |
| `candidate_name` | GStack |
| `observed_paths` | `external/sources/gstack`; `external/sources/gstack-master` |
| `inventory_status` | `not_present`; future multiple present paths require `exact_path_requires_followup_classification` |
| `candidate_classes` | `external_source_candidate`; `gbrain_compatibility_candidate`; `skill_stack_candidate`; `bootstrap_layer_candidate`; `agent_workflow_support_candidate`; `candidate_only` |
| `gbrain_compatibility_posture` | `GBrainCompatibilityRef`; candidate relationship only. |
| `skill_stack_posture` | `SkillStackCandidate`; `gstack_registered_as_gbrain_compatible_skill_stack_candidate` |
| `bootstrap_layer_posture` | Candidate only; no bootstrap runtime. |
| `agent_workflow_support_posture` | Candidate only; no automatic workflow support activation. |
| `runtime_posture` | `not_runtime` |
| `execution_posture` | `not_executed` |
| `import_posture` | `not_imported` |
| `configuration_posture` | `not_configured` |
| `dependency_posture` | `not_dependency_approved` |
| `provider_auth_posture` | `not_provider_auth_approved` |
| `mcp_posture` | `not_mcp_active` |
| `cadence_posture` | `not_cadence_active` |
| `persistence_posture` | No persistence or memory store activation. |
| `source_inspection_posture` | Source content inspection blocked until future exact external review gate. |
| `allowed_p8_use` | Classify candidate; register as GBrain-compatible skill stack candidate; define future compatibility review requirements; consume EXT.GSTACK-01 only if exact optional path is present. |
| `blocked_p8_use` | Source content inspection; execution/import/configuration; dependency approval; runtime adoption; skill runtime activation; automatic workflow support activation; provider/auth/MCP; Cadence; persistence; source/product ingestion. |
| `required_future_gates` | EXT.GSTACK-01 exact source intake / compatibility review; P8.5 activation alignment; security/secrets review; dependency/license review; retention/rollback/incident review; human approval; P8.10/P8.11 synthesis before implementation. |
| `adoption_blockers` | `AdoptionBlocker: source_review_missing`; `AdoptionBlocker: dependency_review_missing`; `AdoptionBlocker: security_review_missing`; `AdoptionBlocker: activation_gate_missing`; `AdoptionBlocker: runtime_blocked`. |
| `limitations` | Paths absent; exact optional EXT.GSTACK-01 P8.7 review absent; compatibility claims are candidate-level only. |

Required GStack posture: `not_adopted`, `not_executed`, `not_imported`, `not_configured`, `not_runtime`, `not_dependency_approved`, `not_provider_auth_approved`, `not_mcp_active`, `not_cadence_active`, and `not_substrate`.

Required outcome: `gstack_registered_as_gbrain_compatible_skill_stack_candidate`.

Do not use as current accepted names: GStack adopted runtime, GStack dependency approved, GStack skill runtime active, GStack validates GBrain, or GStack proves GBrain compatibility.

## 8. GBrain / GStack Compatibility Boundary

`MemoryCompatibilityBoundary` is the canonical boundary object. `MemoryCompatibilityClaim` is the canonical compatibility claim object.

| Field | Meaning |
| --- | --- |
| `boundary_id` | Stable boundary identifier. |
| `gbrain_candidate_ref` | `GBrainCandidateRef` for GBrain. |
| `gstack_candidate_ref` | `GStackCandidateRef` for GStack. |
| `compatibility_status` | Current compatibility status. |
| `compatibility_claims` | MemoryCompatibilityClaim list. |
| `verified_evidence_refs` | EvidenceRef-compatible governance/path metadata only. |
| `unverified_claims` | Claims awaiting future source review. |
| `allowed_interpretations` | Interpretations allowed now. |
| `blocked_interpretations` | Interpretations blocked now. |
| `future_review_requirements` | Required future gates. |
| `security_requirements` | Security prerequisites before expansion. |
| `activation_gate_requirements` | P8.5/P8.R/future gate requirements. |
| `adoption_blockers` | AdoptionBlocker values. |
| `limitations` | Known limitations. |

Current `MemoryCompatibilityBoundary`:

| Field | Value |
| --- | --- |
| `boundary_id` | `memory_compatibility_boundary_gbrain_gstack_p8_7` |
| `gbrain_candidate_ref` | `GBrainCandidateRef:gbrain_candidate` |
| `gstack_candidate_ref` | `GStackCandidateRef:gstack_candidate` |
| `compatibility_status` | `compatibility_supported_by_inventory_only` |
| `compatibility_claims` | GStack may be evaluated later as a GBrain-compatible skill stack / bootstrap layer / agent workflow support candidate; GBrain may inform memory architecture candidate posture. |
| `verified_evidence_refs` | P8.1 external inventory, P8.5 security/activation gate model, P6.6 substrate defer record, P7.0.D memory manifest strategy, path presence checks. |
| `unverified_claims` | Source-level compatibility, dependency-level compatibility, runtime compatibility, MCP/provider compatibility, persistence compatibility, Cadence compatibility. |
| `allowed_interpretations` | Compatibility candidate relationship; inventory-level classification; future review routing. |
| `blocked_interpretations` | Adoption, dependency approval, runtime approval, source review, security approval, substrate selection, proof of compatibility. |
| `future_review_requirements` | EXT.GB-01, EXT.GSTACK-01, P8.5 activation alignment, security/secrets review, dependency/license review, retention/rollback/incident review, human approval. |
| `security_requirements` | S-03/S-04 remain binding; no secrets/credentials/source contents/product source generated into memory. |
| `activation_gate_requirements` | P8-L3 or higher requires future explicit implementation approval; P8-L4 execution remains future-only; P8-L5 blocked. |
| `adoption_blockers` | Source review missing, GStack review missing, dependency review missing, security review missing, runtime gate missing, persistence/retrieval/Cadence gates missing. |
| `limitations` | No local GBrain/GStack candidate paths present; exact optional external review docs absent. |

Compatibility status values:

| Value | Meaning |
| --- | --- |
| `compatibility_candidate_only` | Candidate relationship only. |
| `compatibility_claim_unverified` | Claim exists but is not source-verified. |
| `compatibility_supported_by_inventory_only` | Current P8.7 status; supported by P8.1 inventory/path/class metadata only. |
| `compatibility_supported_by_external_review` | Future status only if exact EXT.GB-01 and EXT.GSTACK-01 exist and are consumed as governance evidence. |
| `compatibility_blocked_until_EXT_review` | Deep compatibility remains blocked until external reviews. |
| `compatibility_rejected_for_scope` | Rejected in a future review. |
| `unknown_compatibility_status` | Unknown; treat as blocked or needs review. |

GStack compatibility with GBrain is a candidate relationship. Compatibility is not adoption, dependency approval, runtime approval, source review, security approval, or substrate selection.

## 9. Memory Capability Claim Matrix

`MemoryCapabilityClaim` is the canonical memory capability claim object. `MemoryCapabilityClaim` and `SkillStackCapabilityClaim` are claims, not approvals.

| capability_area | GBrain_candidate_relevance | GStack_candidate_relevance | current_evidence | P8_allowed_use | blocked_use | required_future_gate |
| --- | --- | --- | --- | --- | --- | --- |
| markdown-first memory | Memory architecture candidate may inform markdown-first memory. | Skill stack may later support markdown workflows. | P7.0.D, P2.KR, P8.1. | Conceptual alignment. | Automated ingestion or runtime memory. | P8.10/P8.11 plus future memory gate. |
| MemoryManifest compatibility | May inform MemoryManifest future shape. | May inform helper skill candidates. | P7.0.D. | Boundary design. | Live manifest ingestion. | P8.3/P8.10 schema synthesis. |
| ContextPack compatibility | May inform explicit manual context packs. | May inform packaging helpers. | P7.0.D, P8.3. | Manual refs only. | Automatic context assembly/retrieval. | Future retrieval/security gate. |
| EvidencePack compatibility | May inform evidence-linked memory. | May inform evidence packaging skills. | P2.2, P7.0.D. | EvidenceRef-compatible metadata. | Evidence as authority. | Evidence/security/review gate. |
| SourceRef / EvidenceRef linkage | May inform source/evidence relation model. | May support relation helpers later. | P2.1, P2.2. | Metadata refs. | Source loading or content review. | Source inspection gate. |
| TaskMemorySlice | May inform task-scoped memory slices. | May support task helper skill candidates. | P7.0.0, P8.3. | Candidate schema term. | Persistent task memory. | P8.10/P8.11. |
| CellMemorySlice | May inform cell-scoped memory slices. | May support cell bootstrap patterns. | P7.0.0. | Conceptual only. | Runtime cell memory. | Future memory architecture gate. |
| BlackboardMemoryRef | May inform blackboard memory refs. | May support blackboard helpers. | P7.0.0. | Metadata ref candidate. | Runtime blackboard store. | Future state/security gate. |
| TopologyContextPack | May inform topology-aware context packs. | May support topology bootstrap. | P7.0.0, P8.3. | Candidate object only. | Automatic topology retrieval. | P8.10/P8.11. |
| FreshnessMarker | May inform stale/fresh memory semantics. | May support freshness helper skills. | P7.0.D. | Marker vocabulary. | Automatic stale refresh. | Future validation/retrieval gate. |
| StaleContextMarker | May inform stale blockers. | May support stale-context prompts. | P7.0.D. | Manual warning metadata. | Scheduled refresh. | Future Cadence gate. |
| MissingContextMarker | May inform missing-context blockers. | May support manual checklist helpers. | P7.0.D. | Manual blocker metadata. | Automatic context fetch. | Future retrieval/source gate. |
| ContradictionMarker | May inform contradiction memory posture. | May support contradiction checklist helpers. | P7.0.F, P7.0.D. | Manual review marker. | Contradiction detection runtime. | Future validation/Cadence gate. |
| EvidenceConflictMarker | May inform evidence conflict posture. | May support evidence-conflict helper prompts. | P7.0.F, P2.2. | Manual review marker. | Automatic citation fixing. | Future validation/evidence gate. |
| retrieval strategy | May inform future retrieval architecture. | May support retrieval workflow helper candidates. | P2.KR. | Candidate planning only. | Automatic retrieval/live retrieval. | Future retrieval/security/retention gate. |
| hybrid retrieval | May inform hybrid graph/vector/markdown candidate evaluation. | May support helper skills later. | P2.KR. | Candidate comparison only. | Vector/graph DB or embeddings. | Future CSS/storage gate. |
| typed graph / entity-relation memory | May inform entity-relation memory ideas. | May support relationship helpers. | P1.5, P2.KR. | Metadata relation concepts. | Graph DB or ontology runtime. | Future graph/storage/security gate. |
| persistent knowledge store | Persistent knowledge candidate only. | May support bootstrap patterns later. | P6.6, P8.1. | Candidate posture. | Persistent memory activation. | Storage/security/retention gate. |
| skill stack / bootstrap helpers | May be target architecture for helper stack. | Core candidate area for GStack. | P8.1. | Classify as skill stack candidate. | Skill runtime activation. | EXT.GSTACK-01 and activation gate. |
| agent workflow support | May inform memory workflow shape. | May support agent workflow helpers later. | P7.0.0, P8.1. | Manual workflow support concepts. | Automatic task/handoff execution. | Future agent/runtime gate. |
| synthesis / gap analysis | May inform future synthesis posture. | May support helper prompts later. | P7.0.F, P8.3. | Manual checklist candidate. | Automatic synthesis/gap analysis. | Future validation/Cadence gate. |
| stale fact refresh | May inform freshness posture. | May support manual stale review helper. | P7.0.D. | Manual marker only. | Scheduled stale fact refresh. | Future Cadence gate. |
| contradiction handling | May inform contradiction posture. | May support manual contradiction checklist. | P7.0.F. | Manual review marker. | Contradiction detection runtime. | Future validation/Cadence gate. |
| Cadence / dream-cycle | Possible cadence reference candidate only. | No active cadence role. | P2.KR, P8.5. | Blocked future concept only. | Dream cycle, always-on behavior. | Future exact Cadence gate. |
| provider/auth/MCP integration | Not approved. | Not approved. | P8.5, S-04. | Boundary metadata only. | Provider/API/MCP activation. | Provider/auth/API/MCP gate. |
| product-bound memory | Product vision only. | Product vision only. | P8.0, P8.5, S-03. | Blocked marker only. | Product source/data memory. | P4 / GT-09 or equivalent. |

## 10. Future Memory MVP Candidate

`FutureMemoryMVPCandidate` is the canonical future memory MVP object.

| Field | Meaning |
| --- | --- |
| `memory_mvp_candidate_id` | Stable memory MVP candidate identifier. |
| `candidate_name` | Human-readable candidate name. |
| `candidate_level` | Memory MVP level. |
| `purpose` | Candidate purpose. |
| `allowed_inputs` | Inputs allowed for the candidate. |
| `blocked_inputs` | Inputs blocked for the candidate. |
| `storage_posture` | Storage posture. |
| `retrieval_posture` | Retrieval posture. |
| `persistence_posture` | Persistence posture. |
| `source_inspection_posture` | SourceInspectionPosture. |
| `security_posture` | Security posture. |
| `context_posture` | Context posture. |
| `evidence_posture` | Evidence posture. |
| `GBrain_influence` | GBrain candidate influence. |
| `GStack_influence` | GStack candidate influence. |
| `Graphify_influence` | Graphify candidate influence. |
| `activation_requirements` | Future activation prerequisites. |
| `human_approval_requirements` | Required human approvals. |
| `stop_rules` | Stop conditions. |
| `limitations` | Known limitations. |

Candidate levels:

| Level | Current posture |
| --- | --- |
| `Memory_MVP_0_markdown_json_refs_only` | Required current recommendation. |
| `Memory_MVP_1_read_only_local_metadata_memory` | Future candidate only after future gate and P8.10/P8.11 synthesis. |
| `Memory_MVP_2_controlled_index_candidate` | Future controlled index candidate only. |
| `Memory_MVP_3_controlled_persistent_memory_candidate` | Future controlled persistent memory candidate only. |
| `Memory_MVP_4_active_retrieval_candidate` | Future active retrieval candidate only. |
| `Memory_MVP_5_cadence_always_on_candidate_blocked` | Blocked. |

Current recommended `FutureMemoryMVPCandidate`:

| Field | Value |
| --- | --- |
| `memory_mvp_candidate_id` | `future_memory_mvp_candidate_0` |
| `candidate_name` | Memory MVP-0 markdown/json refs only. |
| `candidate_level` | `Memory_MVP_0_markdown_json_refs_only` |
| `purpose` | Preserve manual memory/context/evidence refs for MVP-0 without runtime memory. |
| `allowed_inputs` | Canonical markdown by manual full-read/reference only; future local JSON/markdown metadata refs if later authorized by P8.12+; MemoryManifest; ContextPack; EvidencePack; SourceRef; FileRef; DecisionRef; GraphifyRef as supporting evidence only; GBrainCandidateRef; GStackCandidateRef; freshness/stale/missing markers; contradiction/evidence-conflict markers. |
| `blocked_inputs` | Secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, product/Siamese source, external source contents, raw generated outputs, raw Graphify outputs, runtime logs, unclassified local-only material, GBrain/GStack source contents. |
| `storage_posture` | Markdown/json refs only if later implemented; no database. |
| `retrieval_posture` | Manual context assembly only; no automatic retrieval. |
| `persistence_posture` | `no_persistent_memory_activation`. |
| `source_inspection_posture` | SourceRef/FileRef are not source loading or file reading permission. |
| `security_posture` | S-03/S-04 binding; secrets/credentials excluded. |
| `context_posture` | User controls what context enters HarnessInputPackage. |
| `evidence_posture` | EvidenceRef/GraphifyRef support only; evidence does not decide. |
| `GBrain_influence` | Memory architecture candidate only; no runtime. |
| `GStack_influence` | Skill stack / bootstrap helper candidate only; no runtime. |
| `Graphify_influence` | Supporting evidence only; not authority. |
| `activation_requirements` | P8.10/P8.11 synthesis plus explicit future implementation gate before any implementation; additional storage/retrieval/security gates before any escalation. |
| `human_approval_requirements` | Exact approval required before any source inspection, implementation, persistence, retrieval, execution, provider/API/MCP, product work, or Git action. |
| `stop_rules` | Stop on runtime memory, automatic retrieval, persistence DB, vector DB, graph DB, source indexing, Cadence, provider/auth/API/MCP, secrets/credentials, external/product source, raw generated outputs, validation execution, tests/builds/scripts, or Git mutation. |
| `limitations` | Design posture only; no memory store and no runtime state. |

Required output marker: `future_memory_mvp_candidate_defined`.

Future candidate `Memory_MVP_1_read_only_local_metadata_memory` is allowed only after future gate, P8.10/P8.11 synthesis, security review, retention/rollback/incident posture, explicit implementation approval, and human approval.

## 11. Source Inspection Boundary

| Candidate | Allowed_now | Blocked_now | Required_gate_for_deep_inspection | Notes |
| --- | --- | --- | --- | --- |
| GBrain | P8.1 inventory metadata; P6.6 substrate-defer posture; P7.0.D memory manifest posture; path presence checks; candidate classification; compatibility boundary design. | File content inspection; source code inspection; dependency analysis by reading manifests; license analysis by reading files; import/execution; runtime probing; package installation; provider/auth/MCP probing; source indexing; content summarization from source files. | EXT.GB-01 for GBrain source intake / read-only capability review; P8.5 activation gate alignment; security/secrets review; dependency/license review; retention/rollback/incident review; human approval. | Exact optional P8.7 EXT.GB-01 path absent, so GBrain claims remain candidate-level. |
| GStack | P8.1 inventory metadata; P6.6 substrate-defer posture; P7.0.D memory manifest posture; path presence checks; candidate classification; compatibility boundary design. | File content inspection; source code inspection; dependency analysis by reading manifests; license analysis by reading files; import/execution; runtime probing; package installation; provider/auth/MCP probing; source indexing; content summarization from source files. | EXT.GSTACK-01 for GStack source intake / compatibility review; P8.5 activation gate alignment; security/secrets review; dependency/license review; retention/rollback/incident review; human approval. | Exact optional P8.7 EXT.GSTACK-01 path absent, so GStack claims remain candidate-level. |

Path presence is not content review. Path presence is not dependency approval. Path presence is not adoption. Path presence is not runtime approval.

## 12. Persistence / Storage Boundary

No storage implementation or persistent memory activation is approved.

Blocked explicitly:

| Blocked storage / persistence surface | P8.7 posture |
| --- | --- |
| Postgres | Not approved. |
| pgvector | Not approved. |
| PGLite | Not approved. |
| SQLite | Not approved. |
| embedded DB | Not approved. |
| vector DB | Not approved. |
| graph DB | Not approved. |
| ontology runtime | Not approved. |
| embeddings | Not approved. |
| persistent memory | `no_persistent_memory_activation`. |
| AGENT PLATFORM markdown ingestion | Not approved. |
| source indexing | Not approved. |
| product data ingestion | Not approved. |
| event store | Not approved. |
| telemetry store | Not approved. |
| live connector sync store | Not approved. |

If storage is mentioned, classify it only as `future_persistence_candidate_only` and `blocked_until_storage_security_retention_review`.

Required marker: `no_graph_vector_db_activation`.

## 13. Retrieval / Context Injection Boundary

No automatic context retrieval is approved.

| Retrieval / injection surface | P8.7 posture |
| --- | --- |
| automatic GBrain retrieval | Not approved. |
| automatic GStack-assisted context assembly | Not approved. |
| live retrieval | Not approved. |
| context injection into prompts | Not approved. |
| provider-bound context transmission | Not approved. |
| source indexing | Not approved. |
| embeddings | Not approved. |
| MVP-0 context | Manually assembled ContextPack / MemoryManifest only. |
| user control | User controls what context enters HarnessInputPackage. |

Future retrieval requires explicit gate, security review, retention model, rollback model, incident route, and human approval.

## 14. Cadence / Always-On Boundary

GBrain/GStack may suggest future memory workflow patterns, but P8.7 does not approve always-on behavior.

| Cadence / always-on surface | Classification |
| --- | --- |
| dream cycle | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| scheduled memory refresh | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| background ingestion | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| automatic synthesis | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| automatic gap analysis | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| stale fact refresh | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| contradiction detection runtime | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| automatic citation fixing | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| live connector sync | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| notification / alerting | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| Hermes integration | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |
| Cadence activation | `blocked_until_future_exact_gate`; `not_active`; `not_implemented`; `requires_P8.5_P8.10_P8.11_future_Cadence_gate` |

Required marker: `no_cadence_activation`.

## 15. Provider/Auth/API/MCP Boundary

No provider/auth/API/MCP activation is approved.

| Surface | Current posture |
| --- | --- |
| GBrain provider/auth | `not_provider_auth_approved` |
| GStack provider/auth | `not_provider_auth_approved` |
| GBrain MCP | `not_mcp_active` |
| GStack MCP | `not_mcp_active` |
| MCP metadata | Not MCP activation. |
| Provider metadata | Not provider activation. |
| CredentialRef | Not credential approval. |
| API key availability | Not API key approval. |

Any future memory candidate requiring API/MCP/provider behavior requires P8.5 gate alignment, security review, validation readiness, retention/rollback/incident posture, and human approval.

## 16. Security / Secrets / Credentials Boundary

Secrets and credentials are never memory content.

| Rule | P8.7 posture |
| --- | --- |
| GBrain/GStack secret ingestion | Blocked. |
| GBrain/GStack credential ingestion | Blocked. |
| `.env` ingestion | Blocked. |
| provider config ingestion | Blocked. |
| token store ingestion | Blocked. |
| browser auth ingestion | Blocked. |
| local credential store ingestion | Blocked. |
| API key ingestion | Blocked. |
| secret-adjacent indexing | Blocked. |
| secret summarization | Blocked. |
| credential transformation/hash/fingerprint/partial exposure | Blocked. |
| unknown sensitivity | Blocks memory candidacy. |

Future memory review requires security/secrets boundary proof. S-03 and S-04 remain binding.

## 17. Product / Siamese Boundary

Siamese is product vision, not product activation.

| Product / Siamese surface | P8.7 posture |
| --- | --- |
| Product/Siamese source | Blocked. |
| Product-bound semantic storage | Blocked. |
| Product data ingestion | Blocked. |
| Product source indexing | Blocked. |
| Product-derived graph/vector/persistent memory | Blocked. |
| Product-bound memory path | Requires P4 / product readiness gate / security / validation / retention / rollback / incident posture / human approval. |

P8.7 does not start P4 and does not inspect product source.

## 18. Graphify Boundary

Graphify remains read-only generated supporting evidence candidate.

| Graphify relation | P8.7 posture |
| --- | --- |
| Graphify as memory runtime | No. |
| Graphify as GBrain | No. |
| Graphify as GStack | No. |
| Graphify as substrate | No. |
| Graphify as authority | No. |
| Graphify deciding GBrain/GStack compatibility | No. |
| GraphifyRef | May support evidence only under P8.6 or previous governance. P8.6 is present and still does not approve Graphify runtime/rerun/adoption. |
| P8.7 Graphify action | Does not run Graphify and does not inspect raw Graphify outputs. |

Graphify evidence supports; it does not decide.

## 19. Interface With P8.2 / P8.3 / P8.4 / P8.5 / P8.10

| Interface | P8.7 relationship | Current alignment |
| --- | --- | --- |
| P8.2 | GBrain/GStack memory candidate posture may inform future memory UX. MVP-0 interaction surface must remain manual. No automatic retrieval in UI. | P8.2 present; no `pending_P8.2_interaction_surface_alignment`. |
| P8.3 | GBrainCandidateRef, GStackCandidateRef, MemoryCompatibilityBoundary, FutureMemoryMVPCandidate, and MemoryCapabilityClaim may become schema candidates. | P8.3 present; no `pending_P8.3_schema_candidates_alignment`. |
| P8.4 | Memory MVP-0 should align with local workspace/state model. No external source content persistence by default. | P8.4 present; no `pending_P8.4_local_workspace_state_alignment`. |
| P8.5 | All future memory activation levels must map to P8-L0 through P8-L5. P8.7 must not redefine activation gates independently. | P8.5 required and present. |
| P8.10 | P8.10 must reconcile whether Memory_MVP_0 remains sufficient for MVP-0 and whether any future Memory_MVP_1 work is eligible. | P8.7 does not start synthesis. |

P8.6, P8.8, and P8.9 are present by current P8.7 path checks and were consumed as optional peer metadata only. P8.7 does not modify those peer files.

## 20. Interface With P7 / P6 / P2

| Baseline | P8.7 interface |
| --- | --- |
| P7.0.D | MemoryManifest remains manual. ContextPack and EvidencePack remain explicit. GBrainCandidateRef and GStackCandidateRef remain candidate notation only. No live retrieval. |
| P7.0.0 | MemoryFabric pattern may inform future design. Mycelial memory network remains conceptual. Federated cell memory remains conceptual. No memory substrate activation. |
| P6.6 | Cognitive Semantic System substrate remains deferred. GBrain-style architecture may remain strongest external candidate. GStack may support future GBrain-compatible skill-stack evaluation. No substrate selection. |
| P2.KR | Markdown + metadata refs remain baseline. Vector/graph/hybrid retrieval candidates remain future candidates. Evidence traceability and blocker propagation remain required. |

## 21. Evidence / Validation / Security Interfaces

Evidence interface:

| Rule | P8.7 posture |
| --- | --- |
| Candidate compatibility must cite EvidenceRef-compatible governance/path metadata. | Required. |
| GBrainCandidateRef | Candidate notation only. |
| GStackCandidateRef | Candidate notation only. |
| Evidence supports. | Preserved. |
| Evidence decides. | Rejected. |
| Missing EXT reviews | Explicit pending markers required. |

Validation interface:

| Rule | P8.7 posture |
| --- | --- |
| Validation execution | Not run. |
| Future validation | May check candidate records, boundary invariants, and no-adoption invariants. |
| Validation evaluates | Preserved. |
| Governance decides | Preserved. |

Security interface:

| Rule | P8.7 posture |
| --- | --- |
| GBrain/GStack are security-sensitive until reviewed. | Preserved. |
| Source inspection | Blocked. |
| Secrets and credentials in memory candidate records | Prohibited. |
| Security constrains | Preserved. |
| Security activates | Rejected. |

## 22. Retention / Rollback / Incident Posture

Required future memory retention posture fields:

| Field | Required future meaning |
| --- | --- |
| `retention_owner` | Human/governance owner for memory retention. |
| `retention_scope` | Exact memory scope. |
| `retention_duration` | Explicit duration or deletion rule. |
| `redaction_policy` | How sensitive content is excluded/redacted. |
| `local_only_policy` | Local-only handling. |
| `source_indexing_policy` | Source indexing allowed/blocked status. |
| `generated_output_policy` | Generated output retention/handling. |
| `product_bound_policy` | Product-bound data/source handling. |
| `publication_policy` | Publication blocker posture. |
| `source_tracking_policy` | Source tracking posture. |

Required future rollback posture fields:

| Field | Required future meaning |
| --- | --- |
| `rollback_owner` | Human/governance owner for rollback. |
| `rollback_trigger` | Trigger condition. |
| `memory_disable_route` | Route to disable memory behavior. |
| `data_removal_route` | Route to remove retained data. |
| `index_removal_route` | Route to remove indexes. |
| `embedding_removal_route` | Route to remove embeddings. |
| `graph_edge_removal_route` | Route to remove graph edges. |
| `persistence_cleanup_route` | Route to clean persistence. |
| `source_tracking_reversal_route` | Route to reverse source tracking. |
| `publication_reversal_route` | Route to reverse publication. |

Incident triggers:

| Incident trigger | P8.7 response posture |
| --- | --- |
| `secret_exposure` | Stop, escalate, do not retain. |
| `credential_exposure` | Stop, escalate, do not retain. |
| `API_key_exposure` | Stop, escalate, do not retain. |
| `provider_config_exposure` | Stop, escalate, do not retain. |
| `token_store_exposure` | Stop, escalate, do not retain. |
| `browser_auth_exposure` | Stop, escalate, do not retain. |
| `local_credential_store_exposure` | Stop, escalate, do not retain. |
| `product_source_exposure` | Stop and require product/security gate. |
| `local_only_source_exposure` | Stop and require sensitivity review. |
| `raw_generated_output_exposure` | Stop and require generated-output review. |
| `unauthorized_persistence` | Stop and require cleanup/rollback. |
| `unauthorized_embedding` | Stop and require embedding removal route. |
| `unauthorized_graph_write` | Stop and require graph rollback route. |
| `unauthorized_source_indexing` | Stop and require index/source tracking reversal. |
| `unauthorized_GBrain_execution` | Stop and incident escalation. |
| `unauthorized_GStack_execution` | Stop and incident escalation. |
| `unauthorized_Cadence_activation` | Stop and incident escalation. |
| `unauthorized_live_connector_sync` | Stop and incident escalation. |
| `generated_output_tracking_violation` | Stop and generated-output policy review. |
| `source_tracking_violation` | Stop and source tracking reversal review. |
| `publication_violation` | Stop and publication reversal route. |

P8.7 creates no runtime state and no memory store. It records future posture only.

## 23. Human Approval Requirements

Human approval is required before:

| Action | P8.7 approval posture |
| --- | --- |
| Deep GBrain source inspection | Required; not granted. |
| Deep GStack source inspection | Required; not granted. |
| Adopting GBrain | Required; not granted. |
| Adopting GStack | Required; not granted. |
| Executing either candidate | Required; not granted. |
| Dependency approval | Required; not granted. |
| Memory persistence | Required; not granted. |
| Automatic retrieval | Required; not granted. |
| Provider/auth/API/MCP activation | Required; not granted. |
| Product/Siamese source work | Required; not granted. |

P8.7 itself does not approve these actions.

## 24. Stop Rules

STOP if any condition applies:

| Stop condition | Required response |
| --- | --- |
| P8.0 is missing | STOP and report `p8_0_missing_boundary`. |
| P8.1 is missing | STOP and report `p8_1_missing_external_inventory`. |
| P8.5 is missing | STOP and report `p8_5_missing_security_activation_gate_model`. |
| Boundary work requires reading GBrain source contents | STOP. |
| Boundary work requires reading GStack source contents | STOP. |
| Boundary work requires recursive external source inspection | STOP. |
| Boundary work requires importing or executing GBrain or GStack | STOP. |
| Boundary work requires dependency installation or package-manager commands | STOP. |
| Boundary work requires provider/auth/API/MCP | STOP. |
| Boundary work requires credential use | STOP. |
| Boundary work requires API/MCP calls | STOP. |
| Boundary work requires tool execution | STOP. |
| Boundary work requires agent execution | STOP. |
| Boundary work requires memory runtime activation | STOP. |
| Boundary work requires persistent memory activation | STOP. |
| Boundary work requires automatic retrieval | STOP. |
| Boundary work requires source indexing | STOP. |
| Boundary work requires graph/vector DB, embeddings, database, or substrate selection | STOP. |
| Boundary work requires Cadence / always-on behavior | STOP. |
| Boundary work requires product/Siamese source inspection | STOP. |
| Boundary work requires raw generated output inspection | STOP. |
| Boundary work requires secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, or API keys | STOP. |
| Boundary work requires validation execution, tests, CI, scripts, or builds | STOP. |
| Boundary work requires generated output tracking, source tracking expansion, publication, or Git mutation | STOP. |
| Boundary work exceeds compatibility boundary scope | STOP. |

## 25. Future Validation Targets

Future validation targets, not executed:

| Target | Purpose |
| --- | --- |
| GBrainCandidateRecord required fields completeness | Check record completeness. |
| GStackCandidateRecord required fields completeness | Check record completeness. |
| MemoryCompatibilityBoundary required fields completeness | Check boundary completeness. |
| MemoryCapabilityClaim matrix completeness | Check capability matrix coverage. |
| FutureMemoryMVPCandidate required fields completeness | Check future memory MVP candidate completeness. |
| GBrain candidate-only invariant | Preserve candidate-only posture. |
| GStack candidate-only invariant | Preserve candidate-only posture. |
| GStack registered as GBrain-compatible skill stack candidate invariant | Check required marker. |
| no GBrain/GStack execution invariant | Preserve not-executed posture. |
| no GBrain/GStack import/configuration invariant | Preserve not-imported/not-configured posture. |
| no dependency approval invariant | Preserve not-dependency-approved posture. |
| no source content inspection invariant | Preserve source-inspection blocker. |
| no memory runtime adoption invariant | Check `no_memory_runtime_adoption`. |
| no persistent memory activation invariant | Check `no_persistent_memory_activation`. |
| no automatic retrieval invariant | Preserve no automatic retrieval. |
| no source indexing invariant | Preserve no source indexing. |
| no vector DB invariant | Preserve no vector DB. |
| no graph DB invariant | Preserve no graph DB. |
| no embeddings invariant | Preserve no embeddings. |
| no Cadence invariant | Check `no_cadence_activation`. |
| no provider/auth/MCP invariant | Preserve provider/auth/MCP blockers. |
| no secrets/credentials memory invariant | Preserve secret/credential exclusion. |
| product/Siamese boundary invariant | Preserve product source blocker. |
| EXT.GB-01 pending marker invariant when absent | Check `pending_EXT.GB_01_gbrain_external_source_review`. |
| EXT.GSTACK-01 pending marker invariant when absent | Check `pending_EXT.GSTACK_01_gstack_external_source_review`. |
| P8.10 synthesis readiness check | Prepare future synthesis, not execution. |

## 26. Future Hardening Candidates

Future tickets, not started:

| Candidate | Purpose |
| --- | --- |
| MEMCOMP-HARD-01 - GBrainCandidateRecord Schema Alignment | Harden GBrain candidate schema. |
| MEMCOMP-HARD-02 - GStackCandidateRecord Schema Alignment | Harden GStack candidate schema. |
| MEMCOMP-HARD-03 - MemoryCompatibilityBoundary Schema Hardening | Harden compatibility boundary schema. |
| MEMCOMP-HARD-04 - MemoryCapabilityClaim Matrix Hardening | Harden capability matrix. |
| MEMCOMP-HARD-05 - FutureMemoryMVPCandidate Contract | Harden future memory MVP contract. |
| MEMCOMP-HARD-06 - No Automatic Retrieval Boundary Contract | Harden retrieval blocker. |
| MEMCOMP-HARD-07 - No Persistence / No Graph / No Vector Boundary Contract | Harden storage blocker. |
| MEMCOMP-HARD-08 - GBrain / GStack Source Inspection Gate Contract | Harden source inspection gates. |
| MEMCOMP-HARD-09 - Memory Retention / Rollback / Incident Contract | Harden lifecycle posture. |
| MEMCOMP-HARD-10 - P8.10 Memory Compatibility Reconciliation Inputs | Prepare synthesis inputs. |

Optional future external review candidates, not started:

| Candidate | Purpose |
| --- | --- |
| EXT.GB-01 - GBrain External Source Intake / Read-Only Capability Review | Future GBrain review. |
| EXT.GSTACK-01 - GStack External Source Intake / Compatibility Review | Future GStack review. |

## 27. Created / Modified / Not Created Register

Created:

| Path | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_gbrain_gstack_memory_compatibility_boundary.md` | Created as P8.7 GBrain / GStack memory compatibility boundary. |

Modified:

| Area | Status |
| --- | --- |
| Other files | None modified by P8.7. |

Not created / not approved:

| Area | Status |
| --- | --- |
| P8.0 file | Not created. |
| P8.1 file | Not created. |
| P8.2 file | Not created. |
| P8.3 file | Not created. |
| P8.4 file | Not created. |
| P8.5 file | Not created. |
| P8.6 file | Not created. |
| P8.8 file | Not created. |
| P8.9 file | Not created. |
| P8.10 file | Not created. |
| P8.11 file | Not created. |
| P8.12+ file | Not created. |
| P8.R file | Not created. |
| P9/P4/EXT.* file | Not created. |
| runtime implementation | Not created. |
| memory runtime implementation | Not created. |
| adapter implementation | Not created. |
| executable adapter | Not created. |
| GBrain adoption | Not approved. |
| GBrain execution | Not performed. |
| GBrain import | Not performed. |
| GBrain configuration | Not performed. |
| GBrain dependency approval | Not granted. |
| GBrain provider/auth approval | Not granted. |
| GBrain MCP activation | Not active. |
| GBrain Cadence activation | Not active. |
| GBrain substrate selection | Not selected. |
| GStack adoption | Not approved. |
| GStack execution | Not performed. |
| GStack import | Not performed. |
| GStack configuration | Not performed. |
| GStack dependency approval | Not granted. |
| GStack runtime | Not active. |
| persistent memory activation | Not active. |
| automatic context retrieval | Not active. |
| automatic memory retrieval | Not active. |
| live retrieval | Not active. |
| source indexing | Not approved. |
| AGENT PLATFORM markdown ingestion | Not approved. |
| product data ingestion | Not approved. |
| provider/auth/API/MCP activation | Not active. |
| credential use | Not performed. |
| API calls | Not performed. |
| MCP calls | Not performed. |
| tool execution | Not performed beyond allowed path/status/target checks. |
| agent execution | Not performed. |
| live connector activation | Not active. |
| source loading | Not approved. |
| source inspection | Not approved. |
| GBrain source content inspection | Not performed. |
| GStack source content inspection | Not performed. |
| product/Siamese source inspection | Not performed. |
| raw generated output inspection | Not performed. |
| secrets inspected | Not performed. |
| credentials inspected | Not performed. |
| `.env` inspected | Not performed. |
| provider configs inspected | Not performed. |
| token stores inspected | Not performed. |
| browser auth inspected | Not performed. |
| local credential stores inspected | Not performed. |
| API keys inspected | Not performed. |
| validation execution | Not performed. |
| tests / CI / scripts / builds executed | Not performed. |
| security enforcement activation | Not performed. |
| persistence DB | Not created. |
| Postgres | Not created. |
| pgvector | Not created. |
| PGLite | Not created. |
| SQLite | Not created. |
| vector DB / embeddings | Not created. |
| graph DB / substrate selection | Not created or selected. |
| ontology runtime | Not created. |
| telemetry | Not created. |
| event streaming | Not created. |
| Cadence / dream-cycle / always-on behavior | Not active. |
| Graphify execution/rerun/adoption | Not performed. |
| Codegraph execution/adoption | Not performed. |
| Hermes runtime | Not active. |
| OpenCode execution | Not performed. |
| generated output tracking | Not approved. |
| source tracking expansion | Not approved. |
| publication | Not performed. |
| Git mutation | Not performed. |

## 28. Recommended Next Ticket

After P8.7, if P8.6, P8.8, or P8.9 are still missing, continue Round 2:

| Ticket | Current status | Recommendation |
| --- | --- | --- |
| P8.6 - Graphify Read-Only Evidence Boundary | Present. | Do not modify from P8.7. |
| P8.8 - Hermes Interface / Runtime Candidate Boundary | Present. | Do not modify from P8.7. |
| P8.9 - OpenCode Harness Upgrade Boundary | Present. | Do not modify from P8.7. |

Recommended actual: P8.10 - MVP-0 Architecture Synthesis, because P8.6, P8.7, P8.8, and P8.9 are present by current checks.

After P8.6-P8.9 are complete: P8.10 - MVP-0 Architecture Synthesis.

Do not start P8.8, P8.9, P8.10, or implementation tickets from this ticket.

## 29. Final Verdict

| Question | Answer |
| --- | --- |
| What did P8.7 create? | `0_architecture/governance/agent_platform_gbrain_gstack_memory_compatibility_boundary.md`. |
| What GBrain / GStack memory compatibility boundary was defined? | A MemoryCompatibilityBoundary between GBrainCandidateRecord and GStackCandidateRecord with inventory-only compatibility posture. |
| How is GBrain classified? | Memory architecture / persistent knowledge / second-brain / future Cognitive Semantic System substrate candidate; candidate only. |
| How is GStack classified? | GBrain-compatible skill stack / bootstrap layer / agent workflow support candidate; candidate only. |
| Is GStack registered as GBrain-compatible skill stack candidate? | Yes: `gstack_registered_as_gbrain_compatible_skill_stack_candidate`. |
| What compatibility status was assigned? | `compatibility_supported_by_inventory_only`. |
| What compatibility claims were mapped? | GBrain may inform future memory architecture; GStack may inform future GBrain-compatible skill stack / bootstrap / workflow support candidates. |
| What source inspection posture was defined? | Path/class metadata only; deep source inspection blocked until EXT.GB-01 / EXT.GSTACK-01 and security/approval gates. |
| Were EXT.GB-01 / EXT.GSTACK-01 present? | No exact P8.7 optional paths were present. |
| What pending external review markers were recorded? | `pending_EXT.GB_01_gbrain_external_source_review`; `pending_EXT.GSTACK_01_gstack_external_source_review`. |
| What future memory MVP candidate was defined? | `FutureMemoryMVPCandidate` with required current recommendation `Memory_MVP_0_markdown_json_refs_only`. |
| Is Memory_MVP_0 still markdown/json refs only? | Yes. Manual refs only; no runtime memory, automatic retrieval, persistence DB, vector DB, graph DB, source indexing, or Cadence. |
| Was any memory runtime adopted? | No: `no_memory_runtime_adoption`. |
| Was GBrain adopted? | No. |
| Was GStack adopted? | No. |
| Was GBrain or GStack executed? | No. Both remain `not_executed`. |
| Was GBrain or GStack imported/configured? | No. |
| Was dependency approval granted? | No. |
| Was provider/auth/API/MCP activated? | No. |
| Was MCP activated? | No. |
| Was persistent memory activated? | No: `no_persistent_memory_activation`. |
| Was automatic retrieval activated? | No. |
| Was source indexing approved? | No. |
| Was graph DB implemented? | No. |
| Was vector DB implemented? | No. |
| Were embeddings generated? | No. |
| Was database/persistence implemented? | No. |
| Was Cadence / dream-cycle / always-on activated? | No: `no_cadence_activation`. |
| Was product/Siamese source inspected? | No. |
| Was external source content inspected? | No. |
| Were secrets or credentials inspected? | No. |
| Was Cognitive Semantic System substrate selected? | No. GBrain remains `not_substrate`; GStack remains `not_substrate`. |
| What gates are required before future deep inspection or adoption? | EXT.GB-01, EXT.GSTACK-01, P8.5 activation alignment, security/secrets review, dependency/license review, retention/rollback/incident review, P8.10/P8.11 synthesis where applicable, and explicit human approval. |
| What P8 peer alignments are pending? | None for P8.2, P8.3, P8.4, P8.6, P8.8, or P8.9 by current P8.7 path checks. P8.10 synthesis remains future. |
| What is the recommended next ticket? | P8.10 - MVP-0 Architecture Synthesis. |

Final markers:

```text
gbrain_gstack_memory_compatibility_boundary_ready
gbrain_registered_as_memory_architecture_candidate
gstack_registered_as_gbrain_compatible_skill_stack_candidate
future_memory_mvp_candidate_defined
no_memory_runtime_adoption
no_persistent_memory_activation
no_graph_vector_db_activation
no_cadence_activation
```

Stop after P8.7. Do not start P8.0, P8.1, P8.2, P8.3, P8.4, P8.5, P8.6, P8.8, P8.9, P8.10, P8.11, P8.12+, P8.R, P9, P4, EXT.*, implementation, memory runtime, adapters, executable adapters, runtime activation, source inspection, source indexing, provider/auth/API/MCP, persistent memory, automatic retrieval, graph/vector DB, embeddings, database, Cadence, product source, raw generated output inspection, validation, tests, builds, scripts, generated output tracking, source tracking expansion, publication, or Git mutation from this ticket.
