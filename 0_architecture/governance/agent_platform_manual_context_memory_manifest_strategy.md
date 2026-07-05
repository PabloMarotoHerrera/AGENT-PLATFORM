# P7.0.D - Manual Context / Memory Manifest Strategy

## Document Header
| Field | Value |
|---|---|
| Title | Manual Context / Memory Manifest Strategy |
| Ticket | P7.0.D |
| Status | Accepted manual context / memory manifest strategy |
| Date | 2026-07-05 |
| Scope | Documentation-only manual context / memory manifest strategy for AGENT PLATFORM / Siamese AL-1.5 manual controlled agentic workflow planning. |
| Authority | Manual context / memory manifest design only, not agent runtime activation, autonomous orchestration, automatic dispatch, automatic handoff, automatic reviewer assignment, automatic context retrieval, persistent memory, live retrieval, GBrain runtime, Hermes runtime, Cadence, provider/auth/API/MCP activation, tool execution, agent execution, reviewer execution, integrator execution, source loading, source inspection, product source inspection, external source inspection, Graphify adoption/rerun, Codegraph execution, vector DB, embeddings, graph DB, ontology runtime, generated output tracking, source tracking expansion, publication, Git mutation, or Cognitive Semantic System substrate selection. |
| Related documents | P7 roadmap, P7.0.A, P7.0.B, P7.0.C, P7.0.E, P7.0.F, P7.0.G, P6.7, P6.1, P6.2, P6.3, P6.4, P6.5, P6.6 if created/deferred, P5.R, P3.BR, P3.3, P3.4, P3.5, P3.R, P3.0, P3.1, P3.2, P2.KR, P2.1, P2.2, P2.3, P1.1, P1.2, P1.3, P1.4, P1.5, P0.1, P0.2, P0.3, S-03, S-04, CSS ADR/audit, Graphify Repo Map Summary, README, `.gitignore`, `.graphifyignore`. |
| Output | Manual context / memory manifest strategy. |

This ticket is manual workflow design only.

## Purpose
P7 converts the current manual agentic workflow into a repeatable operating architecture.

P7.0.D defines how memory and context are packaged manually for lead agents, lane agents, reviewer agents, integrators, and external harnesses.

P7.0.D defines a manual MemoryManifest interface so future GBrain / Graphify evidence / Cognitive Semantic System / harness capabilities can be integrated later without changing the workflow shape.

P7 designs the manual operating model for a future agentic platform.

P7 does not execute the future platform.

P7.0.D allows M0 — canonical markdown + metadata refs.

P7.0.D allows M1 — curated Graphify evidence references only if already approved as evidence.

P7.0.D allows M2 — GBrain-style candidate references as candidate notation only.

P7.0.D blocks M3 active GBrain runtime / substrate.

P7.0.D blocks graph DB, vector DB, embeddings, persistent memory, live retrieval, and Cadence.

P7.0.D does not activate runtime.

P7.0.D does not automate context assembly.

P7.0.D does not execute agents, tools, providers, MCP, GBrain, Hermes, Cadence, Graphify evidence, Codegraph candidate, or product behavior.

P7.0.D does not mutate Git.

## Current Posture
| Posture | Statement |
|---|---|
| Activation level | P7 is AL-1.5 manual controlled agentic workflow planning. |
| AL-2 boundary | P7 is not AL-2. |
| Runtime boundary | Manual workflow design is not runtime activation. |
| Context packs | Manual context packs are not automatic memory. |
| Memory manifests | Manual memory manifests are not persistent memory. |
| Harness usage | Manual harness usage is not internal harness adoption. |
| ContextPack | ContextPack is not source loading. |
| EvidencePack | EvidencePack is not authority. |
| SourceRef | SourceRef is not content inspection permission. |
| FileRef | FileRef is not file reading permission. |
| DecisionRef | DecisionRef is not approval. |
| GraphifyRef | GraphifyRef is not Graphify authority. |
| GBrainCandidateRef | GBrainCandidateRef is not GBrain adoption. |
| Freshness | Context freshness is not validation. |
| Stale context | Stale context blocks trust until reviewed. |
| Missing context | Missing context blocks execution or acceptance until supplied or explicitly waived. |
| Git authority | The user remains final commit authority. |
| Git mutation | The agent never mutates Git. |

Manual operating model preserved by P7.0.D:

| Step | Manual workflow stage |
|---|---|
| 1 | User objective. |
| 2 | Lead agent / main planning chat. |
| 3 | Roadmap generation. |
| 4 | Work packet decomposition. |
| 5 | Parallel manual agents. |
| 6 | Reviewer agents. |
| 7 | Integrator / lead agent. |
| 8 | Final verdict. |
| 9 | Exact git add / commit / push commands. |
| 10 | User performs Git manually. |

## Inputs Reviewed
| Input | Expected role | Present / missing | Memory-manifest use | Blocking consequence if missing |
|---|---|---|---|---|
| P7.0.A Manual Lead Agent / User Gateway Contract | Lead/user gateway alignment. | Missing. | Would define lead chat context intake and user authority. | pending_P7.0.A_lead_gateway_alignment. |
| P7.0.B Roadmap Generation / Work Breakdown Contract | Roadmap/work packet alignment. | Missing. | Would define context by roadmap phase and work packet. | pending_P7.0.B_roadmap_breakdown_alignment. |
| P7.0.C Parallel Agent Lane / Work Packet Taxonomy | Lane taxonomy alignment. | Missing. | Would define lane-specific context requirements. | pending_P7.0.C_agent_lane_taxonomy_alignment. |
| P7.0.E Manual Harness Strategy / OpenCode-Hermes Boundary | Harness boundary alignment. | Missing. | Would define harness-specific context consumption. | pending_P7.0.E_harness_boundary_alignment. |
| P7.0.F Reviewer Agent / Approval Pipeline Contract | Reviewer pipeline alignment. | Missing. | Would define review context and approval refs. | pending_P7.0.F_reviewer_pipeline_alignment. |
| P7.0.G Integrator / Reconciliation / Commit Advisory Protocol | Integrator and commit advisory alignment. | Missing. | Would define final integration context and exact Git command advice. | pending_P7.0.G_integrator_commit_advisory_alignment. |
| P6.7 Operational Readiness Audit | P6 closure baseline. | Present. | Supplies operational readiness posture for P7 planning. | Block P7 reconciliation if absent. |
| P6.1 Agent Registry / Capability Registry Operational Contract | Capability registry boundary. | Present. | Registry refs may inform ManifestConsumerRef and agent lane refs. | Registry alignment incomplete if absent. |
| P6.2 Agent-to-Agent Communication Protocol | Communication protocol boundary. | Present. | Manual routing and handoff metadata semantics. | Protocol alignment incomplete if absent. |
| P6.3 Shared Context / Evidence Bus Operational Contract | Context/evidence bus boundary. | Present. | EvidencePack and ContextPack ref semantics. | Context/evidence alignment incomplete if absent. |
| P6.4 Human Approval / Review Loop Operational Contract | Approval boundary. | Present. | HumanDecisionPoint and approval boundary semantics. | Approval alignment incomplete if absent. |
| P6.5 Runtime Monitoring / Incident Handling Operational Contract | Monitoring/incident boundary. | Present. | ManifestIncidentRef and stop-rule posture. | Incident alignment incomplete if absent. |
| P6.6 Cognitive Semantic System Substrate Decision, if created or deferred | Substrate posture. | Present. | Cognitive Semantic System substrate posture and GBrainCandidateRef boundary. | Substrate alignment incomplete if absent/deferred marker needed. |
| P5.R Minimal Active Agent Platform Audit | P5 skeleton baseline. | Present. | Confirms manual planning does not activate runtime skeleton. | Baseline incomplete if absent. |
| P3.BR Activation Decision Reconciliation Closure | Activation decision reconciliation. | Present. | Prevents decisions becoming execution. | Activation-decision drift if absent. |
| P3.3 Tool Execution Activation Decision | Tool execution decision boundary. | Present. | Tool execution blockers in manifests. | Tool boundary incomplete if absent. |
| P3.4 Provider/Auth/API/MCP Activation Decision | Provider/auth/API/MCP boundary. | Present. | Provider/auth blockers in manifests. | Provider boundary incomplete if absent. |
| P3.5 Agent Runtime Activation Decision | Agent runtime decision boundary. | Present. | Agent execution blockers in manifests. | Agent boundary incomplete if absent. |
| P3.R Activation Readiness Reconciliation Closure | Readiness reconciliation. | Present. | Readiness is not activation. | Readiness alignment incomplete if absent. |
| P3.0 Controlled Source Classification Readiness | Source classification posture. | Present. | SourceRef and FileRef classification. | Source classification incomplete if absent. |
| P3.1 Validation Execution Readiness | Validation readiness posture. | Present. | Validation refs and freshness boundary. | Validation posture incomplete if absent. |
| P3.2 Security Enforcement Readiness | Security readiness posture. | Present. | Security blockers and secret/credential exclusions. | Security posture incomplete if absent. |
| P2.KR Knowledge / Retrieval Architecture Reconciliation Closure | Knowledge/retrieval posture. | Present. | Memory mode boundaries and future retrieval candidate posture. | Retrieval alignment incomplete if absent. |
| P2.1 Shared Metadata Vocabulary Alignment | Vocabulary baseline. | Present. | Ref and marker naming. | Vocabulary alignment incomplete if absent. |
| P2.2 EvidenceRef Contract | Evidence ref semantics. | Present. | EvidencePack and EvidenceRef conformance. | Evidence semantics incomplete if absent. |
| P2.3 Audit / Retention / Rollback Baseline | Retention/rollback baseline. | Present. | ManifestRetentionRef and ManifestRollbackRef posture. | Lifecycle posture incomplete if absent. |
| P1.1 Context Runtime Contract Hardening | Context boundary. | Present. | ContextPack is not source loading. | Context boundary incomplete if absent. |
| P1.2 Provider Adapter Metadata Contract Hardening | Provider metadata boundary. | Present. | Provider metadata is not activation. | Provider boundary incomplete if absent. |
| P1.3 Tool Execution Boundary Contract Hardening | Tool execution boundary. | Present. | Tool metadata is not tool execution. | Tool boundary incomplete if absent. |
| P1.4 Agent Runtime Boundary Contract Hardening | Agent runtime boundary. | Present. | Agent metadata is not agent execution. | Agent boundary incomplete if absent. |
| P1.5 Cognitive Semantic System Prototype Hardening | Cognitive Semantic System boundary. | Present. | Substrate remains governed and deferred unless future decision says otherwise. | CSS boundary incomplete if absent. |
| P0.1 Activation Gate Enforcement Map | Gate baseline. | Present. | Manual manifests cannot satisfy activation gates. | Gate posture incomplete if absent. |
| P0.2 Validation Execution Gate Design | Validation gate baseline. | Present. | Validation evaluates; governance decides. | Validation gate posture incomplete if absent. |
| P0.3 Security Enforcement Hardening Plan | Security hardening baseline. | Present. | Security constrains; it does not activate. | Security hardening posture incomplete if absent. |
| S-03 Tool / Shell / Network / MCP Execution Policy | Tool/network/MCP security policy. | Present. | Blocks tool, network, MCP, and shell execution through manifests. | Policy boundary incomplete if absent. |
| S-04 Local-Only Secrets / Credentials Policy | Secrets/credentials policy. | Present. | Secrets and credentials are never manifest content. | Secret/credential boundary incomplete if absent. |
| CSS ADR/audit | Accepted Cognitive Semantic System naming and audit. | Present. | Preserves accepted name and substrate boundary. | CSS naming/audit incomplete if absent. |
| Graphify Repo Map Summary | Curated Graphify evidence summary. | Present. | M1 curated Graphify evidence references only. | Graphify evidence boundary incomplete if absent. |
| README | Repository boundary context. | Present. | High-level repo posture only. | Repo posture incomplete if absent. |
| `.gitignore` | Ignore boundary. | Present. | Boundary posture only; not modified. | Ignore posture incomplete if absent. |
| `.graphifyignore` | Graphify ignore boundary. | Present. | Boundary posture only; not modified. | Graphify ignore posture incomplete if absent. |
| `external/sources/gbrain-master` | Optional external path metadata only. | Missing. | GBrainCandidateRef remains path/class metadata only. | No content inspection; candidate path remains absent. |

## Dependency Posture
P7.0.A is missing, so P7.0.D records `pending_P7.0.A_lead_gateway_alignment`.

P7.0.B is missing, so P7.0.D records `pending_P7.0.B_roadmap_breakdown_alignment`.

P7.0.C is missing, so P7.0.D records `pending_P7.0.C_agent_lane_taxonomy_alignment`.

P7.0.E is missing, so P7.0.D records `pending_P7.0.E_harness_boundary_alignment`.

P7.0.F is missing, so P7.0.D records `pending_P7.0.F_reviewer_pipeline_alignment`.

P7.0.G is missing, so P7.0.D records `pending_P7.0.G_integrator_commit_advisory_alignment`.

P7.0.D may proceed in parallel with pending markers.

P7.0.D must not synthesize sibling P7.0.A-P7.0.G documents.

P7.0.D must not start P7.0.H.

P7.0.D must not start P7.0.R.

P7.0.D must be reconciled later by P7.0.R.

## Manual Memory Mode Model
| Mode | Meaning | Allowed in P7.0.D | Blocked behavior | Required future gate | Retention posture | Limitations |
|---|---|---|---|---|---|---|
| M0 — canonical markdown + metadata refs | Manual use of canonical governance markdown and metadata refs. | Yes. | Source loading, automatic retrieval, approval, execution. | None for metadata-only manual use; future gate for any activation. | Metadata-only retention posture. | Manual curation required. |
| M1 — curated Graphify evidence references | Manual references to curated Graphify evidence already approved as evidence. | Yes, only when already approved as evidence. | Raw Graphify output, Graphify authority, substrate selection, source tracking expansion. | Future exact gate for any generated output tracking or source expansion. | Evidence-reference retention posture. | Supporting evidence only. |
| M2 — GBrain-style candidate references | Candidate notation for future memory/substrate review. | Yes, candidate notation only. | GBrain adoption, runtime, source inspection, dependency approval, substrate selection. | P6.6 or future exact substrate/source/security/persistence gate. | Metadata-only candidate posture. | `external/sources/gbrain-master` remains path/class metadata only. |
| M3 — active GBrain runtime / substrate | Active GBrain runtime, substrate, live retrieval, persistence, or memory service. | No. | M3 active GBrain runtime is blocked. | Future exact gate; not P7.0.D. | Not applicable. | Blocked in P7.0.D. |

Required mode decisions:

| Decision | P7.0.D posture |
|---|---|
| M0 | Allowed. |
| M1 | Allowed only for curated Graphify evidence references already approved as evidence. |
| M2 | Allowed as candidate notation only. |
| M3 | M3 active GBrain runtime is blocked. |
| Vector DB | No vector DB; blocked. |
| Graph DB | No graph DB; blocked. |
| Embeddings | Blocked. |
| Persistent memory | No persistent memory; blocked. |
| Live retrieval | No live retrieval; blocked. |
| Cadence | No Cadence; blocked. |
| Automatic ingestion | Blocked. |

## MemoryManifest Operational Model
MemoryManifest is a manual routing artifact that lists context, evidence, source refs, file refs, decision refs, Graphify refs, GBrain candidate refs, freshness markers, stale-context markers, missing-context markers, blockers, limitations, retention posture, rollback posture, and stop rules for a manual work packet or review pass.

MemoryManifest is not persistent memory.

MemoryManifest is not runtime context assembly.

MemoryManifest is not source loading.

MemoryManifest is not connector activation.

MemoryManifest is not GBrain runtime.

MemoryManifest is not vector search.

MemoryManifest is not graph traversal.

MemoryManifest is not automatic retrieval.

MemoryManifest is not approval.

## MemoryManifest Object Model
| Object | Meaning | Required fields | Forbidden fields | Security posture | Validation posture | Activation posture |
|---|---|---|---|---|---|---|
| MemoryManifest | Manual routing artifact for context, evidence, refs, freshness, blockers, and stop rules. | ID, scope, owner, consumers, packs, refs, markers, blockers, posture, stop rules. | Secrets, credentials, raw source, raw external source, raw product source, raw Graphify output, live payloads. | Must preserve blockers and sensitivity. | Freshness is not validation. | Not runtime context assembly. |
| ContextPack | Curated context or metadata refs for a manual task. | ID, scope, owner, items, refs, classification, freshness, allowed/forbidden use. | Unknown-sensitivity content, secrets, credentials, raw blocked source. | Must exclude blocked content. | Completeness is not validation execution. | Not source loading. |
| EvidencePack | Evidence refs and supporting documents for manual review. | ID, scope, EvidenceRefs, source/file/decision refs, validation/security refs, limitations. | Evidence as authority, approval, raw blocked content. | Must preserve exclusions and blocked material. | Evidence supports; it does not decide. | Not approval and not validation execution. |
| SourceRef | Metadata reference to a source or source-like surface. | ID, type, path/identifier, classification, sensitivity, allowed/forbidden use, posture. | Content body unless future exact gate permits. | SourceRef is not content inspection permission. | May reference validation refs only. | Not source loading. |
| FileRef | Metadata reference to a file or file-like artifact. | ID, path/identifier, role, classification, sensitivity, allowed/forbidden use, permission posture. | File content, write permission, Git tracking permission. | FileRef is not file reading permission. | May support checks later. | Not file read/write/Git permission. |
| DecisionRef | Metadata reference to a governance decision. | ID, document, scope, status, authority scope, allowed/blocked consequence. | Execution permission unless explicitly governed. | Must preserve blockers. | Decision refs may include validation/security refs. | DecisionRef is not approval by default. |
| GraphifyRef | Metadata reference to curated Graphify evidence. | ID, artifact type, curation/evidence status, local-only flag, authority posture. | Raw Graphify output, authority posture, substrate approval. | Must remain generated evidence only. | Supporting evidence only. | Not Graphify authority. |
| GBrainCandidateRef | Candidate notation for GBrain-style future memory/substrate review. | ID, candidate path/identifier, role, status, mode, posture, future review, blockers. | Adoption, runtime activation, source content, substrate selection. | External source candidate blockers preserved. | Future review only. | Not GBrain adoption. |
| ContextFreshnessMarker | Marker for whether context is current enough for manual task use. | Marker value, scope, timestamp/ref if applicable, limitations. | Validation result. | Unknown freshness can block use. | Freshness is not validation. | Not automatic refresh permission. |
| StaleContextMarker | Marker that context may be outdated. | Stale reason, affected scope, limitation, required review. | Permission to refresh automatically. | Stale sensitive context blocks trust. | Requires review or limitation. | Not automatic retrieval. |
| MissingContextMarker | Marker that required or optional context is unavailable. | Missing item, required/optional class, blocker/waiver posture. | Permission to inspect source automatically. | Missing sensitive context blocks use. | Missing required context blocks acceptance or needs waiver. | Not source inspection permission. |
| ContextBoundary | Boundary definition for allowed/forbidden context contents. | Classification, sensitivity, exclusions, allowed use, forbidden use. | Broad permission. | Preserves secret/product/external blockers. | Not validation. | Not activation. |
| MemoryRoute | Manual route from producer to consumer. | Producer, consumer, route purpose, memory mode, restrictions. | Automatic dispatch. | Route cannot bypass blockers. | Route cannot validate. | Not orchestration. |
| ManifestConsumerRef | Metadata ref for manifest consumer. | Consumer type, role, allowed use, forbidden use. | Agent activation. | Consumer gets only allowed context. | Not validation execution. | Not agent execution. |
| ManifestProducerRef | Metadata ref for manifest producer. | Producer type, role, scope, limitations. | Automatic context retrieval. | Producer cannot include blocked content. | Not validation execution. | Not runtime. |
| ManifestReviewRef | Metadata ref for manual review pass. | Reviewer, scope, findings, limitations. | Approval by default. | Review cannot bypass blockers. | Review is not validation execution. | Not Git approval. |
| ManifestRetentionRef | Metadata ref for retention posture. | Retention class, duration/posture, limitations. | Persistence implementation. | Sensitive refs need incident posture. | Not validation. | Not database. |
| ManifestRollbackRef | Metadata ref for rollback posture. | Rollback scope, affected outputs, route, limitations. | Rollback automation. | Rollback route preserves blockers. | Not validation. | Not automation. |
| ManifestIncidentRef | Metadata ref for incident posture. | Incident trigger, route, owner/ref, limitations. | Incident automation. | Required for sensitive/product/external/live material. | Not validation. | Not runtime monitoring. |
| ManifestStopRule | Stop rule for unsafe or incomplete manual context use. | Condition, blocked consequence, required action. | Auto-waiver. | Stops on security blockers. | Stops on validation posture gaps. | Blocks activation. |

## MemoryManifest Contract
MemoryManifest fields:

| Field | Requirement |
|---|---|
| memory_manifest_id | Stable identifier. |
| manifest_title | Human-readable title. |
| manifest_owner | Accountable owner. |
| manifest_scope | Exact manual workflow scope. |
| manifest_consumer_refs | Manual consumers. |
| manifest_producer_ref | Manual producer. |
| work_packet_refs | Work packet refs. |
| agent_lane_refs | Agent lane refs. |
| reviewer_refs | Reviewer refs. |
| integrator_refs | Integrator refs. |
| context_packs | ContextPack refs. |
| evidence_packs | EvidencePack refs. |
| source_refs | SourceRef refs. |
| file_refs | FileRef refs. |
| decision_refs | DecisionRef refs. |
| graphify_refs | GraphifyRef refs. |
| gbrain_candidate_refs | GBrainCandidateRef refs. |
| freshness_markers | ContextFreshnessMarker refs. |
| stale_context_markers | StaleContextMarker refs. |
| missing_context_markers | MissingContextMarker refs. |
| source_classification_refs | Source classification refs. |
| sensitivity | Sensitivity posture. |
| local_only_flags | Local-only posture. |
| product_boundary_flags | Product/Siamese blockers. |
| external_boundary_flags | External source blockers. |
| generated_output_flags | Generated output blockers. |
| secret_credential_blockers | Secret/credential blockers. |
| provider_auth_blockers | Provider/auth blockers. |
| tool_execution_blockers | Tool execution blockers. |
| agent_execution_blockers | Agent execution blockers. |
| live_connector_blockers | Live connector blockers. |
| cadence_blockers | Cadence blockers. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| review_required | Review requirement. |
| human_decision_points | Explicit human decision points. |
| allowed_use | Exact allowed use. |
| forbidden_use | Exact forbidden use. |
| stop_rules | ManifestStopRule refs. |
| limitations | Known limitations. |

MemoryManifest must be manually provided, updated, or reviewed.

MemoryManifest cannot activate retrieval.

MemoryManifest cannot inspect files.

MemoryManifest cannot execute tools.

MemoryManifest cannot call providers.

MemoryManifest cannot wake agents.

MemoryManifest cannot mutate Git.

## ContextPack Contract
ContextPack fields:

| Field | Requirement |
|---|---|
| context_pack_id | Stable identifier. |
| context_scope | Exact context scope. |
| context_owner | Accountable context owner. |
| context_items | Curated context items or metadata refs only. |
| source_refs | SourceRef refs. |
| file_refs | FileRef refs. |
| decision_refs | DecisionRef refs. |
| evidence_refs | EvidenceRef-compatible refs. |
| source_classification | Source classification posture. |
| sensitivity | Sensitivity posture. |
| freshness_marker | ContextFreshnessMarker. |
| stale_marker | StaleContextMarker, if applicable. |
| missing_context_marker | MissingContextMarker, if applicable. |
| allowed_use | Exact allowed use. |
| forbidden_use | Exact forbidden use. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| blockers | Blockers. |
| limitations | Limitations. |

ContextPack is not source loading.

ContextPack must contain curated context or metadata refs only.

ContextPack must not contain secrets, credentials, raw product source, raw external source, raw Graphify output, raw live connector payloads, or unknown-sensitivity material.

## EvidencePack Contract
EvidencePack fields:

| Field | Requirement |
|---|---|
| evidence_pack_id | Stable identifier. |
| evidence_scope | Exact evidence scope. |
| evidence_refs | EvidenceRef-compatible refs. |
| supporting_documents | Supporting document refs. |
| source_refs | SourceRef refs. |
| file_refs | FileRef refs. |
| decision_refs | DecisionRef refs. |
| graphify_refs | GraphifyRef refs. |
| validation_refs | Validation refs. |
| security_refs | Security refs. |
| retention_refs | Retention refs. |
| rollback_refs | Rollback refs. |
| incident_refs | Incident refs. |
| limitations | Limitations. |
| excluded_material | Excluded material. |
| blocked_material | Blocked material. |

EvidencePack supports; it does not decide.

EvidencePack is not approval.

EvidencePack is not validation execution.

EvidencePack is not security enforcement.

EvidencePack is not source loading.

## SourceRef Contract
SourceRef fields:

| Field | Requirement |
|---|---|
| source_ref_id | Stable identifier. |
| source_type | Source type. |
| source_path_or_identifier | Path or identifier. |
| source_owner | Owner/ref. |
| source_classification | Classification. |
| sensitivity | Sensitivity. |
| local_only | Local-only posture. |
| product_related | Product relation flag. |
| external_related | External relation flag. |
| generated_output_related | Generated output relation flag. |
| credential_related | Credential relation flag. |
| secret_related | Secret relation flag. |
| allowed_use | Exact allowed use. |
| forbidden_use | Exact forbidden use. |
| inspection_posture | Inspection posture. |
| content_loading_posture | Content loading posture. |
| evidence_refs | Evidence refs. |
| validation_refs | Validation refs. |
| security_refs | Security refs. |
| tracking_posture | Tracking posture. |
| retention_posture | Retention posture. |
| rollback_posture | Rollback posture. |
| incident_posture | Incident posture. |
| review_required | Review requirement. |
| blockers | Blockers. |
| limitations | Limitations. |

SourceRef is not content inspection permission.

SourceRef is not source loading permission.

Path presence is not content inspection permission.

## FileRef Contract
FileRef fields:

| Field | Requirement |
|---|---|
| file_ref_id | Stable identifier. |
| path_or_identifier | Path or identifier. |
| file_role | File role. |
| source_classification | Source classification. |
| sensitivity | Sensitivity. |
| allowed_use | Exact allowed use. |
| forbidden_use | Exact forbidden use. |
| read_permission_posture | Read permission posture. |
| write_permission_posture | Write permission posture. |
| tracking_posture | Tracking posture. |
| retention_posture | Retention posture. |
| blockers | Blockers. |
| limitations | Limitations. |

FileRef is not file reading permission.

FileRef is not file writing permission.

FileRef is not Git tracking permission.

## DecisionRef Contract
DecisionRef fields:

| Field | Requirement |
|---|---|
| decision_ref_id | Stable identifier. |
| decision_document | Referenced decision document. |
| decision_scope | Decision scope. |
| decision_status | Decision status. |
| authority_scope | Authority scope. |
| allowed_consequence | Allowed consequence. |
| blocked_consequence | Blocked consequence. |
| evidence_refs | Evidence refs. |
| validation_refs | Validation refs. |
| security_refs | Security refs. |
| retention_refs | Retention refs. |
| rollback_refs | Rollback refs. |
| incident_refs | Incident refs. |
| limitations | Limitations. |

DecisionRef is not approval unless exact accepted governance says so.

DecisionRef is not execution permission.

DecisionRef is not Git permission.

## GraphifyRef Contract
GraphifyRef fields:

| Field | Requirement |
|---|---|
| graphify_ref_id | Stable identifier. |
| graphify_artifact_type | Curated artifact type. |
| curation_status | Curation status. |
| evidence_status | Evidence status. |
| source_path_or_identifier | Source path or identifier metadata. |
| generated_output_related | Generated output relation flag. |
| local_only | Local-only posture. |
| allowed_use | Exact allowed use. |
| forbidden_use | Exact forbidden use. |
| authority_posture | Not authority. |
| retention_posture | Retention posture. |
| blockers | Blockers. |
| limitations | Limitations. |

GraphifyRef is not Graphify authority.

GraphifyRef may refer only to curated Graphify evidence already approved as evidence.

Raw Graphify output remains local-only and blocked by default.

GraphifyRef cannot approve source loading, source tracking, runtime activation, substrate selection, or Git mutation.

## GBrainCandidateRef Contract
GBrainCandidateRef fields:

| Field | Requirement |
|---|---|
| gbrain_candidate_ref_id | Stable identifier. |
| candidate_path_or_identifier | Candidate path or identifier. |
| candidate_role | Candidate role. |
| candidate_status | Candidate status. |
| memory_mode | M2 only in P7.0.D. |
| source_classification | external_source_candidate if path-based. |
| inspection_posture | No source inspection in P7.0.D. |
| adoption_posture | not adopted. |
| runtime_posture | not executed. |
| cadence_posture | not Cadence-active. |
| substrate_posture | not substrate. |
| allowed_use | Candidate notation only. |
| forbidden_use | Adoption, runtime, source inspection, substrate selection. |
| required_future_review | Future exact review. |
| blockers | Source/security/provider/auth/persistence/substrate blockers. |
| limitations | Limitations. |

GBrainCandidateRef is candidate notation only.

GBrainCandidateRef is not GBrain adoption.

GBrainCandidateRef is not runtime activation.

GBrainCandidateRef is not substrate selection.

GBrainCandidateRef is not source inspection permission.

`external/sources/gbrain-master` remains path/class metadata only.

## Context Freshness Model
ContextFreshnessMarker marks whether a context pack or manifest is current enough for a manual task.

StaleContextMarker marks context that may be outdated.

MissingContextMarker marks required context that was not available.

| Marker | Meaning | Allowed consequence | Blocked consequence | Required human action |
|---|---|---|---|---|
| current_context | Context is considered current for exact manual scope. | Use with limitations recorded. | Treating freshness as validation. | Confirm scope. |
| recent_but_unverified_context | Context appears recent but was not validated. | Use as limitation. | Treating as validated. | Human review or limitation. |
| stale_context | Context may be outdated. | Block acceptance or record limitation. | Automatic refresh. | Review, update manually, or waive explicitly. |
| missing_required_context | Required context unavailable. | Block execution or acceptance. | Permission to inspect source automatically. | Supply context or waive explicitly. |
| missing_optional_context | Optional context unavailable. | Record limitation. | Silent omission if material. | Decide whether omission is acceptable. |
| unknown_freshness | Freshness unknown. | Treat as blocker or limitation. | Treating as current. | Review freshness or waive explicitly. |
| superseded_context | Context has newer replacement. | Use replacement if supplied. | Using superseded context without limitation. | Confirm replacement or limitation. |
| conflicting_context | Context conflicts with another ref. | Block acceptance or require review. | Silent conflict resolution. | Human review and decision. |

Freshness markers are not validation.

Stale context blocks acceptance or requires explicit limitation.

Missing required context blocks acceptance or requires explicit human waiver.

Unknown freshness must be treated as blocker or limitation.

## Manual Context Routing Model
Manual context routing is determined by user objective, roadmap phase, work packet, agent lane, reviewer role, integrator role, harness type, source classification, sensitivity, memory mode, freshness status, required evidence, required decisions, and required stop rules.

| Consumer | Context required | Evidence required | Blocked context | Freshness requirement | Review requirement |
|---|---|---|---|---|---|
| Lead / Orchestrator Agent | User objective, roadmap refs, work packet refs, decision refs, manifest limitations. | EvidencePack summary and decision refs. | Secrets, credentials, raw product/external source, raw Graphify output. | Current or explicit limitation. | Lead human review and final user confirmation. |
| Architecture Agent | Architecture docs, decision refs, source classification refs, memory mode posture. | EvidenceRefs, GraphifyRef only if curated. | Runtime activation instructions, source contents, credentials. | Current or recent with limitation. | Architecture review. |
| Implementation Planning Agent | Implementation records and boundary docs, not runtime code. | Decision and evidence refs. | Source loading, product source, scripts/tests/build commands. | Current or limitation. | Planning review. |
| Security Agent | S-03, S-04, P3.2, blockers, sensitivity refs. | Security refs and evidence refs. | Secrets, credential values, token stores, `.env`. | Current or limitation. | Security review. |
| Validation Agent | P3.1, P0.2, validation posture refs. | Validation refs and evidence refs. | Test execution instructions unless future gate approves. | Current or limitation. | Validation review. |
| Memory / Context Agent | ContextPack, MemoryManifest, freshness/missing/stale markers. | EvidencePack and source classification refs. | Persistent memory, live retrieval, source loading. | Explicit marker required. | Context review. |
| Harness / Tooling Agent | Manual harness packet and allowed/forbidden use. | Evidence and decision refs. | Harness activation, tool execution, provider calls, MCP. | Current or limitation. | Harness boundary review. |
| Reviewer Agent | Work output, MemoryManifest, EvidencePack, decision refs, stop rules. | EvidencePack and review refs. | Reviewer auto-approval, Git approval, broad approval. | Current or limitation. | Reviewer pass. |
| Integrator Agent | Accepted/rejected outputs, drift, manifests, reviews, exact file refs. | Evidence, review, and decision refs. | Git mutation, git add dot, generated output tracking. | Current or explicit limitation. | Integrator reconciliation. |
| Product Boundary Agent | Product metadata boundary only. | Product gate refs and decision refs. | Product/Siamese source content and product data. | Current or limitation. | Product readiness review. |
| External Source Review Agent | External source path/class metadata and approved safe docs only. | Evidence refs and source classification refs. | External source contents without exact review approval. | Current or limitation. | External source review. |

## Manual Harness Consumption Model
Manual harness consumption means the user manually copies or supplies a ticket, context pack, evidence pack, or manifest to an external harness.

| Mode | Meaning | P7.0.D posture |
|---|---|---|
| H0 | Manual copy/supply by user. | Allowed. |
| H1 | Metadata-only harness adapter design. | Allowed as design only. |
| H2 | Controlled tool execution adapter. | Blocked. |
| H3 | Autonomous orchestration adapter. | Blocked. |

Manual OpenCode usage is not internal runtime adoption.

Manual Codex usage is not internal runtime adoption.

Manual Claude usage is not internal runtime adoption.

Manual Cursor usage is not internal runtime adoption.

Hermes boundary design is not Hermes runtime activation.

No harness may activate blocked behavior through a manifest.

No harness output is accepted until reviewer/integrator pass.

## Reviewer / Integrator Interface
Reviewer agents may consume MemoryManifest, ContextPack, and EvidencePack manually.

Reviewer approval is not Git approval.

Reviewer approval is not human final commit approval.

Integrator agents may reconcile manifests, outputs, reviews, drift, accepted outputs, and rejected outputs.

Integrator recommendations are not Git mutation.

Lead agent may provide exact git add / commit / push command blocks after approval.

The user performs Git manually.

Never recommend git add ..

## Memory / Approval Interface
ApprovalRef is not approval.

DecisionRef is not approval by default.

HumanDecisionPoint must be explicit.

Manual context delivery does not approve action.

Manual memory manifest inclusion does not approve execution.

Manual evidence pack inclusion does not approve execution.

Manual reviewer acceptance does not approve Git mutation.

User remains final commit authority.

## Security Boundary
Secrets and credentials are never memory content.

API keys, tokens, passwords, private keys, OAuth sessions, browser auth, provider configs, token stores, local credential stores, `.env`, and credential values are never manifest content.

Unknown sensitivity blocks inclusion.

Product/Siamese source is blocked.

External source contents are blocked unless future exact review approves.

Raw generated Graphify output is blocked.

Raw live connector payloads are blocked.

Customer-sensitive data is blocked unless future exact review approves.

Security constrains; it does not activate.

## Validation Boundary
Validation evaluates; governance decides.

Freshness is not validation.

Manifest completeness is not validation execution.

EvidencePack is not validation execution.

Reviewer checklist is not validation execution.

No tests, scripts, CI, build, lint, typecheck, or validation commands are approved by P7.0.D.

## Source Classification Boundary
Source classification is not source loading permission.

Path presence is not content inspection permission.

FileRef is not file read permission.

SourceRef is not source read permission.

Manual context packs must preserve P3.0 source classification posture.

Manual memory manifests must preserve local-only, product, external, generated-output, secret, credential, provider-auth, live-connector, and unknown-sensitivity blockers.

## Graphify / GBrain / Cognitive Semantic System Boundary
Graphify evidence is supporting generated evidence only, not authority.

GraphifyRef may reference curated Graphify evidence only when already approved as evidence.

Raw Graphify output remains blocked.

GBrainCandidateRef is candidate notation only.

GBrain runtime remains blocked.

GBrain substrate remains blocked.

Hermes runtime remains blocked.

Cadence remains blocked.

Cognitive Semantic System substrate remains deferred unless a governed future decision changes it.

P7.0.D does not select substrate.

## Product / Siamese Boundary
Siamese is product vision, not product activation.

P7.0.D must not inspect product source.

P7.0.D must not load product source into context.

P7.0.D must not create product-bound manifests from product source.

Product/Siamese context remains blocked until future product-bound readiness and exact source gate.

Product Boundary Agent may receive product-bound metadata only, not product source content.

## Retention / Rollback / Incident Posture
| Manifest object or route | Required posture |
|---|---|
| MemoryManifest | Retention posture required; rollback and incident posture required when downstream decisions or sensitive surfaces are implicated. |
| ContextPack | Retention posture required; rollback/incident posture required for decision-affecting or sensitive context. |
| EvidencePack | Retention posture and evidence limitations required. |
| SourceRef | Source classification, tracking posture, retention posture, and incident posture required for sensitive surfaces. |
| FileRef | Read/write/tracking posture and retention posture required. |
| DecisionRef | Decision authority scope, retention, rollback, and incident refs required where applicable. |
| GraphifyRef | Curated evidence posture, local-only/generated-output posture, and retention posture required. |
| GBrainCandidateRef | Candidate-only posture, external_source_candidate posture, and future review blockers required. |
| Freshness markers | Retention of marker status and limitations required. |
| Stale markers | Limitation/blocker and review route required. |
| Missing context markers | Blocker/waiver posture required. |
| Reviewer-consumed manifests | Review result, limitations, and incident posture required where applicable. |
| Integrator-consumed manifests | Reconciliation posture and exact file refs required where applicable. |
| Harness-supplied manifests | Manual harness boundary, allowed/forbidden use, and review requirement required. |
| Manual git command advice | Exact file paths only, no generated outputs without approval, no product source without product gate, no Git mutation by agent. |

Every MemoryManifest must include retention posture.

Every MemoryManifest must include rollback posture when downstream decisions may depend on it.

Every MemoryManifest must include incident posture when sensitive, product, external, provider, live connector, generated output, or unknown-sensitivity material is implicated.

Accidental inclusion of secrets, credentials, product source, raw external source, raw Graphify output, or raw live connector payloads requires STOP, quarantine/removal route, and safe reporting.

## Manual Git Advisory Boundary
The agent never mutates Git.

The user commits and pushes manually.

The lead agent or integrator may provide exact git add paths after ticket approval.

Never recommend git add ..

Commit advice must include only exact files created or modified.

Commit advice must not include generated outputs unless future exact tracking approval exists.

Commit advice must not include product source unless future product gate approves.

## Stop Rules
STOP if MemoryManifest scope is missing.

STOP if source classification is missing.

STOP if sensitivity is unknown.

STOP if required context is missing and not explicitly waived.

STOP if context is stale and no limitation is recorded.

STOP if secrets or credentials appear in context.

STOP if product source appears in context.

STOP if raw external source appears without exact review approval.

STOP if raw Graphify output appears.

STOP if live connector payload appears.

STOP if GraphifyRef is treated as authority.

STOP if GBrainCandidateRef is treated as adoption.

STOP if manifest implies GBrain runtime, Hermes runtime, Cadence, vector DB, graph DB, embeddings, persistent memory, live retrieval, or automatic ingestion.

STOP if FileRef is treated as file read permission.

STOP if SourceRef is treated as source loading permission.

STOP if DecisionRef is treated as approval without exact governance basis.

STOP if reviewer approval is treated as Git approval.

STOP if agent attempts Git mutation.

STOP if git add . is recommended.

STOP if P7.0.D attempts to start P7.0.H, P7.0.R, P7.1, P8, P4, or implementation.

## Required P7.0.D Invariants
| Invariant | Statement |
|---|---|
| MEM-001 | P7.0.D is manual workflow design only. |
| MEM-002 | P7 designs the manual operating model for a future agentic platform. |
| MEM-003 | P7 does not execute the future platform. |
| MEM-004 | Manual workflow design is not runtime activation. |
| MEM-005 | MemoryManifest is not persistent memory. |
| MEM-006 | ContextPack is not source loading. |
| MEM-007 | EvidencePack supports; it does not decide. |
| MEM-008 | SourceRef is not content inspection permission. |
| MEM-009 | FileRef is not file reading permission. |
| MEM-010 | DecisionRef is not approval by default. |
| MEM-011 | GraphifyRef is not Graphify authority. |
| MEM-012 | GBrainCandidateRef is not GBrain adoption. |
| MEM-013 | M0 canonical markdown + metadata refs is allowed. |
| MEM-014 | M1 curated Graphify evidence references are allowed only when already approved as evidence. |
| MEM-015 | M2 GBrain-style candidate references are candidate notation only. |
| MEM-016 | M3 active GBrain runtime is blocked. |
| MEM-017 | No persistent memory. |
| MEM-018 | No vector DB. |
| MEM-019 | No embeddings. |
| MEM-020 | No graph DB. |
| MEM-021 | No live retrieval. |
| MEM-022 | No Cadence. |
| MEM-023 | No automatic context ingestion. |
| MEM-024 | No product/Siamese source. |
| MEM-025 | No secrets or credentials in memory manifests. |
| MEM-026 | Context freshness is not validation. |
| MEM-027 | Missing context is a blocker, not permission. |
| MEM-028 | Stale context is a blocker or limitation, not permission to refresh automatically. |
| MEM-029 | Manual harness use is not internal harness adoption. |
| MEM-030 | Reviewer approval is not Git approval. |
| MEM-031 | The user remains final commit authority. |
| MEM-032 | The agent never mutates Git. |
| MEM-033 | Never recommend git add .. |

## Future Validation Targets
Future validation targets are proposed only and were not executed:

| Target | Purpose |
|---|---|
| MemoryManifest required fields completeness | Check required manifest metadata. |
| ContextPack required fields completeness | Check required context metadata. |
| EvidencePack EvidenceRef conformance | Check P2.2 evidence semantics. |
| SourceRef no-content-permission invariant | Check SourceRef is not content inspection permission. |
| FileRef no-read-permission invariant | Check FileRef is not file reading permission. |
| DecisionRef no-approval-by-default invariant | Check DecisionRef is not approval by default. |
| GraphifyRef evidence-only invariant | Check curated evidence-only posture. |
| GBrainCandidateRef candidate-only invariant | Check candidate notation only. |
| ContextFreshnessMarker completeness | Check freshness markers. |
| StaleContextMarker blocker/limitation preservation | Check stale context remains blocker/limitation. |
| MissingContextMarker blocker preservation | Check missing context remains blocker unless waived. |
| M0/M1/M2/M3 mode compliance | Check mode rules. |
| no-persistent-memory invariant | Check no persistent memory. |
| no-vector-DB invariant | Check no vector DB. |
| no-graph-DB invariant | Check no graph DB. |
| no-embeddings invariant | Check no embeddings. |
| no-live-retrieval invariant | Check no live retrieval. |
| no-Cadence invariant | Check no Cadence. |
| no-secret/no-credential manifest invariant | Check blocked sensitive content. |
| no-product-source manifest invariant | Check product source remains blocked. |
| no-raw-Graphify-output invariant | Check raw generated output remains blocked. |
| manual-harness-use-not-adoption invariant | Check harness use remains manual. |
| reviewer-approval-not-Git-approval invariant | Check reviewer approval is not Git approval. |
| never-recommend-git-add-dot invariant | Check exact Git safety posture. |
| P7 sibling alignment checks | Check P7.0.A-P7.0.G alignment. |
| P7.0.R reconciliation readiness check | Check readiness for later P7.0.R closure. |

## Future Hardening Candidates
Future tickets are proposed only and not started:

| Candidate | Purpose |
|---|---|
| MEM-HARD-01 - MemoryManifest Schema Alignment | Align manifest schema with P7 sibling contracts. |
| MEM-HARD-02 - ContextPack / EvidencePack Manual Assembly Contract | Harden manual context/evidence assembly. |
| MEM-HARD-03 - SourceRef / FileRef Permission Boundary Contract | Harden no-read/no-load boundary. |
| MEM-HARD-04 - Context Freshness / Staleness / Missing Context Contract | Harden marker semantics. |
| MEM-HARD-05 - Manual Harness Context Intake Contract | Harden external harness context intake. |
| MEM-HARD-06 - GraphifyRef / GBrainCandidateRef Boundary Contract | Harden Graphify and GBrain candidate refs. |
| MEM-HARD-07 - Manual Git Advisory Context Safety Contract | Harden exact Git advisory safety. |
| MEM-HARD-08 - Memory Manifest Validation Checklist | Define future validation checklist without executing validation. |

## Created / Modified / Not Created Register
| Item | Status |
|---|---|
| Manual context / memory manifest strategy document | Created. |
| MemoryManifest model | Created. |
| ContextPack model | Created. |
| EvidencePack model | Created. |
| SourceRef model | Created. |
| FileRef model | Created. |
| DecisionRef model | Created. |
| GraphifyRef model | Created. |
| GBrainCandidateRef model | Created. |
| ContextFreshnessMarker model | Created. |
| StaleContextMarker model | Created. |
| MissingContextMarker model | Created. |
| MemoryRoute model | Created. |
| Manual harness consumption model | Created. |
| Runtime activation | Not created. |
| Autonomous orchestration | Not created. |
| Automatic dispatch | Not created. |
| Automatic handoff | Not created. |
| Automatic reviewer assignment | Not created. |
| Automatic context retrieval | Not created. |
| Live retrieval | Not created. |
| Persistent memory | Not created. |
| GBrain runtime | Not created. |
| Hermes runtime | Not created. |
| Cadence | Not created. |
| Agent execution | Not created. |
| Reviewer execution | Not created. |
| Integrator execution | Not created. |
| Tool execution | Not created. |
| Provider/auth/API/MCP activation | Not created. |
| Credential use | Not created. |
| API calls | Not created. |
| MCP activation | Not created. |
| Live connector activation | Not created. |
| Source loading | Not created. |
| Source inspection | Not created. |
| Product source inspection | Not created. |
| External source inspection | Not created. |
| `external/sources/gbrain-master` content inspection | Not created. |
| Graphify rerun/adoption | Not created. |
| Codegraph execution/adoption | Not created. |
| Validation execution | Not created. |
| Tests / CI / scripts / builds | Not created. |
| Security enforcement activation | Not created. |
| Persistence/database/event stream | Not created. |
| Telemetry | Not created. |
| Vector DB / embeddings | Not created. |
| Graph DB / substrate implementation | Not created. |
| Generated output tracking | Not created. |
| Source tracking expansion | Not created. |
| Publication | Not created. |
| Git mutation | Not created. |
| Auto-commit | Not created. |
| Auto-push | Not created. |
| `.gitignore` modified | Not created. |
| `.graphifyignore` modified | Not created. |
| Generated outputs modified/tracked | Not created. |
| Cognitive Semantic System substrate selected | Not created. |
| P7.0.H started | Not created. |
| P7.0.R started | Not created. |
| P7.1 started | Not created. |
| P8 started | Not created. |
| P4/product-bound files started | Not created. |

## Recommended Next Tickets
P7.0.D is one Round 1 parallel P7 ticket.

Round 1 parallel tickets:

| Ticket | Name | Current P7.0.D posture |
|---|---|---|
| P7.0.A | Manual Lead Agent / User Gateway Contract | Missing; continue remaining Round 1 parallel planning tickets. |
| P7.0.B | Roadmap Generation / Work Breakdown Contract | Missing; continue remaining Round 1 parallel planning tickets. |
| P7.0.C | Parallel Agent Lane / Work Packet Taxonomy | Missing; continue remaining Round 1 parallel planning tickets. |
| P7.0.D | Manual Context / Memory Manifest Strategy | Complete by this document. |
| P7.0.E | Manual Harness Strategy / OpenCode-Hermes Boundary | Missing; continue remaining Round 1 parallel planning tickets. |
| P7.0.F | Reviewer Agent / Approval Pipeline Contract | Missing; continue remaining Round 1 parallel planning tickets. |
| P7.0.G | Integrator / Reconciliation / Commit Advisory Protocol | Missing; continue remaining Round 1 parallel planning tickets. |

After P7.0.A-P7.0.G:

| Ticket | Name | Boundary |
|---|---|---|
| P7.0.H | First Manual Pilot Playbook | Do not start P7.0.H inside P7.0.D. |

After P7.0.H:

| Ticket | Name | Boundary |
|---|---|---|
| P7.0.R | Manual Agentic Workflow Planning Closure | Do not start P7.0.R inside P7.0.D. |

Recommended actual: Continue remaining P7.0.A-P7.0.G parallel planning tickets until Round 1 is complete.

Do not start P7.0.H inside P7.0.D.

Do not start P7.0.R inside P7.0.D.

## Final Verdict
| Question | Answer |
|---|---|
| What did P7.0.D create? | `0_architecture/governance/agent_platform_manual_context_memory_manifest_strategy.md`. |
| What manual context / memory manifest strategy was defined? | A manual AL-1.5 strategy for MemoryManifest, ContextPack, EvidencePack, refs, freshness/stale/missing markers, manual routing, harness consumption, reviewer/integrator consumption, and Git advisory boundaries. |
| What is MemoryManifest? | A manual routing artifact listing context, evidence, refs, freshness, blockers, limitations, retention, rollback, incident posture, and stop rules; it is not persistent memory. |
| What is ContextPack? | Curated manual context or metadata refs for a task; ContextPack is not source loading. |
| What is EvidencePack? | EvidenceRef-compatible support package; EvidencePack supports, it does not decide. |
| What is SourceRef? | Source metadata reference; SourceRef is not content inspection permission or source loading permission. |
| What is FileRef? | File metadata reference; FileRef is not file reading permission, file writing permission, or Git tracking permission. |
| What is DecisionRef? | Governance decision metadata ref; DecisionRef is not approval by default and not execution permission. |
| What is GraphifyRef? | Curated Graphify evidence ref; GraphifyRef is not Graphify authority. |
| What is GBrainCandidateRef? | Candidate notation for future GBrain-style memory/substrate review; GBrainCandidateRef is not GBrain adoption. |
| What are ContextFreshnessMarker, StaleContextMarker, and MissingContextMarker? | Manual markers for currentness, staleness, and unavailable context; they are not validation and do not authorize automatic refresh or source inspection. |
| Which memory modes are allowed? | M0 and constrained M1 are allowed; M2 is allowed as candidate notation only. |
| Which memory modes are blocked? | M3 active GBrain runtime / substrate is blocked. |
| Is M0 allowed? | Yes. M0 — canonical markdown + metadata refs is allowed. |
| Is M1 allowed? | Yes, only for M1 — curated Graphify evidence references already approved as evidence. |
| Is M2 allowed? | Yes, only as M2 — GBrain-style candidate references. |
| Is M3 active GBrain runtime allowed? | No. M3 active GBrain runtime is blocked. |
| Did P7.0.D activate GBrain? | No. |
| Did P7.0.D activate Hermes? | No. |
| Did P7.0.D activate Cadence? | No. No Cadence. |
| Did P7.0.D implement persistent memory? | No. No persistent memory. |
| Did P7.0.D implement vector DB, embeddings, graph DB, or ontology runtime? | No. No vector DB, no embeddings, no graph DB, and no ontology runtime. |
| Did P7.0.D activate live retrieval? | No. No live retrieval. |
| Did P7.0.D rerun or adopt Graphify? | No. |
| Did P7.0.D inspect `external/sources/gbrain-master` contents? | No. The path was checked only as path/class metadata and was absent. |
| Did P7.0.D load or inspect source? | No. |
| Did P7.0.D inspect product/Siamese source? | No. |
| Did P7.0.D execute agents, reviewers, integrators, tools, providers, MCP, or product behavior? | No. |
| Did P7.0.D mutate Git? | No. |
| Can the agent recommend git add .? | No. Never recommend git add .. |
| Who remains final commit authority? | The user remains final commit authority. |
| What is the next ticket? | Continue remaining P7.0.A-P7.0.G parallel planning tickets; do not start P7.0.H or P7.0.R inside P7.0.D. |

Final verdict: P7.0.D is accepted as manual context / memory manifest strategy for AL-1.5 manual controlled agentic workflow planning. It creates no runtime behavior, no persistent memory, no live retrieval, no GBrain/Hermes/Cadence activation, no Graphify adoption, and no Git mutation.
