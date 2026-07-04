# P2.K2 - Hybrid Retrieval Mode Decision Matrix

## 1. Document Header

| Field | Value |
| --- | --- |
| Title | Hybrid Retrieval Mode Decision Matrix |
| Ticket | P2.K2 |
| Status | Accepted hybrid retrieval mode decision matrix |
| Date | 2026-07-04 |
| Scope | Define the metadata-only decision matrix for how AGENT PLATFORM / Siamese knowledge and data should be stored, routed, retrieved, referenced, or excluded. |
| Authority | Knowledge/retrieval architecture decision matrix only, not runtime activation, validation execution, vector DB implementation, embedding generation, graph DB implementation, Graphify adoption, GBrain implementation, Hermes activation, Cadence activation, provider/auth/API/MCP activation, tool execution, agent execution, product activation, source loading, generated output tracking, source tracking expansion, or Cognitive Semantic System substrate selection. |
| Related documents | P2.R Cross-Lane Integration Reconciliation Closure, P2.1 Shared Metadata Vocabulary Alignment, P2.2 Cross-Lane Evidence Reference Contract, P2.3 Audit / Retention / Rollback Baseline, P1.1 Context Runtime Contract Hardening, P1.2 Provider Adapter Metadata Contract Hardening, P1.3 Tool Execution Boundary Contract Hardening, P1.4 Agent Runtime Boundary Contract Hardening, P1.5 Cognitive Semantic System Prototype Hardening, P0.1 Activation Gate Enforcement Map, P0.2 Validation Execution Gate Design, P0.3 Security Enforcement Hardening Plan, G-19 Hybrid Parallel Work Packet Dependency Map, activation gate charter, Graphify Repo Map Summary, S-03 Local-only / Secrets / Credentials Policy, S-04 Tool / Shell / Network / MCP Execution Policy, CSS ADR/audit, README.md, `.gitignore`, `.graphifyignore`. P2.K1, P2.K3, and P2.K4 peer docs are absent and therefore marked pending alignment. |
| Output | Hybrid retrieval mode decision matrix. |

P2.K2 is architecture alignment only. It creates no retrieval runtime, vector DB, embeddings, graph DB, live connector configuration, generated-output tracking, source tracking expansion, provider/auth configuration, tool activation, agent activation, product activation, GBrain implementation, Hermes activation, Cadence behavior, Graphify adoption, or Cognitive Semantic System substrate selection.

Optional second-brain video transcript, notes, and screenshots were not consumed as primary source files in this ticket. Video-source evidence posture is `source_summary_only` based on the provided project summary and the second-brain / AIOS principle that retrieval mode must match the way the information will be queried.

## 2. Purpose

P2 closed cross-lane integration for AGENT PLATFORM metadata contracts. P2.R confirmed `no_unresolved_p2_drift` after reconciling P2.1, P2.2, and P2.3.

P2.K bridges P2 and P3 by deciding how AGENT PLATFORM knowledge should be stored, routed, retrieved, referenced, or excluded before any activation-readiness ticket tries to use knowledge as operational memory.

P2.K2 defines the `data_type` to storage/retrieval mode decision matrix. It prevents two incorrect extremes:

| Incorrect extreme | P2.K2 correction |
| --- | --- |
| Put everything into vector DB. | Vector search is useful for fuzzy lookup across large or semi-structured corpora, but it is not the canonical mode for governance, contracts, activation gates, decisions, or accountability records. |
| Put everything into graph/relationship storage. | Graph/relationship representation is useful for relationship evidence, dependencies, claims, entities, and traceability, but it is not the default storage mode for every artifact. |

P2.K2 does not implement retrieval runtime. P2.K2 does not activate vector search, graph storage, live connectors, Hermes, GBrain, providers, tools, agents, product work, or generated-output tracking. P2.K2 does not start P2.K3, P2.K4, P2.KR, P3.0, P3.1, or P3.2.

## 3. Current Posture

| Area | Current posture |
| --- | --- |
| Activation | AGENT PLATFORM remains pre-active at AL-1 metadata skeleton. |
| P2.K | Architecture alignment only. |
| P2.1 | Provides canonical vocabulary for status, posture, blockers, sensitivity, source classification, and refs. |
| P2.2 | Provides the cross-lane EvidenceRef contract and SourceRef, ValidationRef, SecurityRef, GraphifyRef, and ProductRef relationships. |
| P2.3 | Provides audit, retention, rollback, generated-output, local-only, incident, publication, and source-tracking baseline posture. |
| P2.R | Reconciled P2 drift and confirmed no unresolved P2 drift. |
| Governance and contracts | Markdown-first for canonical records. |
| Wiki/MOC | Future navigability pattern, not runtime. |
| Vector search | Future optional retrieval mode, not active. |
| Graph/Cognitive Semantic System records | Candidate metadata structures, not selected substrate. |
| Graphify | Graphify evidence is supporting generated evidence only, not authority. |
| Live connectors | Future gate-controlled boundaries only. |
| GBrain/Hermes/Cadence | Future and blocked. |
| Product/Siamese source | Blocked until GT-09. Siamese is product vision, not product activation. |
| Secrets and credentials | Never memory content. |

Current memory/retrieval posture is markdown-first for governance and contracts. Wiki/MOC, semantic search, graph relationship records, live connector retrieval, generated evidence curation, and excluded-memory metadata are decision postures only.

Rejected/prohibited/historical examples only: Platform Graphify, Graphify Authority, Graphify owns truth, Graph as selected substrate, GBrain as active runtime, and Hermes as active cadence.

## 4. Retrieval Mode Decision Model

`RetrievalMode` is a metadata-only classification that determines the appropriate storage/retrieval posture for a `DataClass`.

| RetrievalMode | Meaning | Canonical use | Blocked use | Required gate before implementation |
| --- | --- | --- | --- | --- |
| `markdown_full_read_canonical` | markdown full-read canonical record that must be read as a complete document for authority, sequence, nuance, obligations, and accountability. | Governance docs, contracts, activation gates, ADRs, P2.R, audit baselines, security policies. | Vector-only retrieval, graph-only storage, summarized-only authority. | GT-12 for publication/tracking changes; GT-04 only for future validation checks. |
| `markdown_wiki_moc` | markdown wiki / MOC navigation layer that routes readers to canonical records. | Knowledge maps, MOCs, indexes, curated topic routing, decision indexes. | Authority replacement or source-loading approval. | Future P2.K3/P2.KR routing approval before harness projection. |
| `semantic_search_vector_index_candidate` | semantic search / vector index candidate for fuzzy lookup across large or semi-structured corpora. | Large research corpus, transcript corpus, large rule catalogs, supplementary notes. | Authority replacement, full-read bypass, embedding jobs by default. | Future vector/search gate, GT-04/GT-05/GT-08/GT-12 as applicable. |
| `graph_cognitive_semantic_candidate` | graph / Cognitive Semantic System candidate relationship metadata. | Entities, claims, relations, dependencies, ownership, evidence relationships, blocker propagation. | Graph DB writes, selected substrate, truth engine, default storage for all docs. | GT-10 for substrate decision; GT-13 for persistence/state; GT-04/GT-05 for review. |
| `graphify_generated_evidence_ref` | Curated Graphify generated evidence reference. | Graphify repo map summary and curated generated evidence refs. | Graphify authority, raw Graphify output ingestion, source loading approval. | Future Graphify/output/source-tracking gate if rerun/tracking is requested. |
| `live_connector_on_demand` | Live connector data queried at time of need, not permanent memory by default. | Slack, email, task systems, GitHub issues, customer data, runtime logs, volatile state. | Permanent ingestion, connector activation, provider/auth/API/MCP activation. | GT-08, GT-05, GT-15, retention/rollback/incident gates, and exact connector approval. |
| `curated_summary_evidence_ref` | Reviewed summary captured as EvidenceRef with limitations, retention, and review posture. | Reviewed generated summaries, reviewed live-thread summaries, curated research summaries. | Raw output authority, unreviewed generated output promotion. | GT-04/GT-05/GT-12/GT-15 as applicable before tracking/publication. |
| `excluded_from_permanent_memory` | Material that must not be embedded, indexed, graphed, persisted, transmitted, or published by default. | Secrets, credentials, `.env`, API keys, tokens, raw auth, unknown sensitivity, blocked product source. | Any permanent memory, vector index, graph store, summary, provider transmission. | Secure incident route or exact future safe metadata approval only. |
| `blocked_until_gate` | Material whose retrieval/storage mode cannot be promoted until a named gate exists. | Product/Siamese source until GT-09, external raw source until GT-11, source loading until GT-01. | Treating blocked data as safe memory. | Relevant exact gate such as GT-01, GT-09, GT-11, GT-12, GT-15. |
| `unknown_retrieval_mode` | Classification unknown; promotion blocked. | New or mixed data classes. | Default ingestion, default indexing, default graphing. | Classification/security/governance review. |

RetrievalMode is not implementation. RetrievalMode is not permission. RetrievalMode is not source loading approval. RetrievalMode is not provider/auth approval. RetrievalMode is not tool execution approval. RetrievalMode is not agent execution approval. RetrievalMode is not substrate selection.

RetrievalMode must preserve source classification, sensitivity, evidence posture, retention posture, generated-output posture, local-only posture, product posture, provider/auth posture, blockers, limitations, and required gate blockers.

## 5. DataClass Object Model

`DataClass` is the canonical data classification object name for retrieval decisions.

Required `DataClass` fields:

```text
data_class_id
data_type
canonical_description
source_classification
sensitivity
volatility
query_pattern
required_context_completeness
relationship_density
retention_posture
generated_output_posture
local_only_posture
product_posture
provider_auth_posture
evidence_posture
recommended_retrieval_mode
secondary_retrieval_modes
forbidden_retrieval_modes
required_gates
review_required
blockers
limitations
evidence_refs
validation_refs
security_refs
pending_alignment_refs
```

| Field | Meaning |
| --- | --- |
| `data_class_id` | Stable identifier for the data class metadata record. |
| `data_type` | Canonical type being classified for retrieval/storage posture. |
| `canonical_description` | Safe description that does not embed raw source content. |
| `source_classification` | P2.1-aligned origin/access class. |
| `sensitivity` | Highest inherited sensitivity. |
| `volatility` | Stable, periodically updated, volatile, live, unknown, or blocked. |
| `query_pattern` | Query pattern from section 6. |
| `required_context_completeness` | Whether full-document reading is required for valid use. |
| `relationship_density` | Low, medium, high, or unknown relationship/traversal value. |
| `retention_posture` | P2.1/P2.3-aligned retention posture. |
| `generated_output_posture` | P2.1/P2.2/P2.3-aligned generated-output posture. |
| `local_only_posture` | Local-only posture and blockers. |
| `product_posture` | Product posture and GT-09 blocker if implicated. |
| `provider_auth_posture` | Provider/auth/API/MCP posture if implicated. |
| `evidence_posture` | EvidenceRef posture and limitations. |
| `recommended_retrieval_mode` | Primary RetrievalMode. |
| `secondary_retrieval_modes` | Optional supporting RetrievalMode values. |
| `forbidden_retrieval_modes` | RetrievalMode values that must not be used. |
| `required_gates` | Gates required before implementation or promotion. |
| `review_required` | Governance/security/validation/product/source-tracking review needs. |
| `blockers` | Active blockers that must propagate. |
| `limitations` | Known limitations and blocked inferences. |
| `evidence_refs` | EvidenceRef IDs or safe metadata refs. |
| `validation_refs` | ValidationRef IDs or not-executed/future validation posture refs. |
| `security_refs` | SecurityRef IDs or blockers. |
| `pending_alignment_refs` | Pending P2.K1/P2.K3/P2.K4/P2.KR alignment markers. |

DataClass is metadata only and must never embed raw source content, product source, secrets, credentials, provider outputs, tool outputs, agent outputs, raw Graphify outputs, live connector payloads, raw generated output, or external raw source content.

## 6. Query Pattern Decision Criteria

Retrieval mode must match the way the information will be queried.

| query_pattern | Meaning | Preferred retrieval mode | Unsuitable retrieval modes | Notes |
| --- | --- | --- | --- | --- |
| `exact_policy_lookup` | User needs exact policy wording or gate rule. | `markdown_full_read_canonical` | Vector-only, graph-only, live connector. | Use stable canonical markdown first. |
| `full_decision_read` | User needs complete decision sequence and rationale. | `markdown_full_read_canonical` | Vector-only snippets, generated summary only. | Full document required. |
| `contract_compliance_read` | User needs obligations, blockers, interfaces, and exact terms. | `markdown_full_read_canonical` | Vector-only, graph-only. | Contracts must preserve sequence and exact wording. |
| `fuzzy_lookup_large_corpus` | User does not know exact path/title and needs discovery. | `semantic_search_vector_index_candidate` | Vector as authority, graph as default store. | Search should route to source docs for reading. |
| `navigable_topic_exploration` | User needs orientation across curated topics. | `markdown_wiki_moc` | Authority replacement. | MOC routes to canonical docs. |
| `entity_relationship_traversal` | User needs entities, dependencies, and relationships. | `graph_cognitive_semantic_candidate` | Graph DB implementation by default. | Relationship metadata only. |
| `dependency_trace` | User needs blocker/source/evidence propagation. | `graph_cognitive_semantic_candidate` plus `markdown_full_read_canonical` | Vector-only. | Trace uses refs; decisions remain in markdown. |
| `volatile_state_lookup` | User needs current operational or external state. | `live_connector_on_demand` | Permanent memory by default. | Requires future connector gates. |
| `task_thread_lookup` | User needs current task/email/chat/issue thread status. | `live_connector_on_demand` or `curated_summary_evidence_ref` | Permanent raw ingestion. | Curated summary only after review. |
| `incident_sensitive_lookup` | User needs incident posture without exposing unsafe content. | `excluded_from_permanent_memory` plus safe metadata refs | Vector, graph, raw summary. | Use safe metadata only. |
| `product_source_lookup_blocked` | Product/Siamese source would be needed. | `blocked_until_gate` | Any source loading, indexing, graphing, summarizing. | Product/Siamese source remains blocked until GT-09. |
| `credential_secret_lookup_blocked` | Secret or credential would be needed. | `excluded_from_permanent_memory` | Any memory mode, vector, graph, summary, connector persistence. | Secrets and credentials are never memory content. |
| `unknown_query_pattern` | Query pattern unclear. | `unknown_retrieval_mode` | Automatic ingestion. | Block promotion until classified. |

Documents requiring complete context, ordering, authority, obligations, or precise wording must remain full-read markdown canonical records.

## 7. Canonical Data Type To Retrieval Mode Matrix

| data_type | examples | canonical retrieval mode | optional secondary mode | prohibited modes | rationale | required blockers / gates | evidence posture | retention posture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| governance docs | P0/P1/P2/P2.K docs | `markdown_full_read_canonical` | `markdown_wiki_moc` | Vector-only, graph-only | Exact wording and governance authority matter. | Publication/source tracking gates if changed. | EvidenceRef may cite docs; evidence does not decide. | Metadata/full doc canonical. |
| activation gates | G-01, P0.1, future GT records | `markdown_full_read_canonical` | EvidenceRef refs | Vector-only, live connector | Gate fields and stop rules require full read. | Relevant GT records. | EvidenceRef supports gate posture. | Retain canonical markdown and blockers. |
| P1/P2 contracts | P1.1-P1.5, P2.1-P2.3 | `markdown_full_read_canonical` | canonical refs, MOC | Vector-only, graph-only | Contracts require obligations and exact boundaries. | No activation by contract. | EvidenceRef/ValidationRef/SecurityRef preserved. | Metadata/full canonical. |
| P2.R reconciliation closure | P2.R closure doc | `markdown_full_read_canonical` | EvidenceRef | Vector-only | Drift closure must be read complete. | No P2 drift remaining. | EvidenceRef supports reconciliation. | Retain canonical closure. |
| large research corpus | curated research notes | `markdown_wiki_moc` | `semantic_search_vector_index_candidate` | Permanent raw sensitive ingestion | Large fuzzy discovery benefits from wiki/search. | Source/security review. | Evidence only if curated. | Metadata or curated docs. |
| video transcripts | second-brain architecture transcripts if present | `markdown_full_read_canonical` | `semantic_search_vector_index_candidate` | Generated summary as authority | Transcript sequence may matter; fuzzy search can route. | Source review; video-source evidence `source_summary_only` if only summary exists. | SourceRef/EvidenceRef with limitations. | Retain reviewed transcript or summary posture. |
| meeting transcripts | decisions, discussions, meeting notes | `markdown_full_read_canonical` | Vector for fuzzy lookup only | Vector-only, summary-only authority | Sequence, nuance, and accountability may matter. | Review/sensitivity/retention gates. | Evidence with limitations. | Retain full record if approved; summaries limited. |
| architecture decisions / ADRs | CSS ADR, substrate ADRs | `markdown_full_read_canonical` | `markdown_wiki_moc` | Vector-only, graph-only | Decisions require rationale and consequences. | Governance review. | Evidence supports; governance decides. | Canonical markdown. |
| rule catalogs | policy/rule collections | `markdown_full_read_canonical` if small; vector candidate if large and lookup-like | `semantic_search_vector_index_candidate`, MOC | Vector as authority | Lookup may be fuzzy, but source rule must be read. | Future vector gate. | Evidence routes to source. | Metadata/full docs. |
| entity records | SemanticEntity | `graph_cognitive_semantic_candidate` | markdown summary | Graph DB writes by default | Entity identity and relations matter. | GT-10/GT-13 before substrate/persistence. | EvidenceRefs required. | Metadata only. |
| relationship records | SemanticRelation, dependency edge | `graph_cognitive_semantic_candidate` | markdown summary | Graph as selected substrate | Relationship traversal is primary. | GT-10/GT-13 before implementation. | Evidence/Validation/Security refs required. | Metadata only. |
| dependency maps | G-19, blocker maps | `markdown_full_read_canonical` | `graph_cognitive_semantic_candidate` | Graph-only authority | Human summary plus graph-like traversal candidate. | Substrate gate before graph implementation. | Evidence supports dependency trace. | Retain canonical summary. |
| Graphify repo map summaries | curated repo map summary | `graphify_generated_evidence_ref` | `curated_summary_evidence_ref` | Authority, raw output ingestion | Curated generated evidence only. | GT-11/GT-12 if tracking/rerun. | Graphify evidence is supporting generated evidence only, not authority. | Curated generated evidence metadata. |
| raw Graphify outputs | raw files under `9_artifacts/` | `blocked_until_gate` | `excluded_from_permanent_memory` for unsafe raw output | Context load, vector index, graph store | Raw generated output is local-only by default. | GT-12/GT-15/output review. | Raw-output blocker. | Local-only/quarantine candidate. |
| generated summaries | reviewed generated summaries | `curated_summary_evidence_ref` | markdown canonical only if governed | Raw authority | Can become EvidenceRef only after review. | GT-04/GT-05/GT-12 as needed. | EvidenceRef with limitations. | Curated summary only. |
| generated raw outputs | unreviewed reports, logs, provider/tool/agent output | `blocked_until_gate` | quarantine candidate | Vector, graph, publication, source | Generated outputs are not source by default. | GT-15/output review. | Blocked generated output evidence. | Local-only/quarantine. |
| Slack data | chat history | `live_connector_on_demand` | `curated_summary_evidence_ref` | Permanent raw memory | Volatile, user/customer-sensitive, noisy. | Future connector/auth/retention gates. | Curated summary only after review. | Not permanent by default. |
| email data | inbox/thread data | `live_connector_on_demand` | `curated_summary_evidence_ref` | Permanent raw memory | Volatile and sensitive. | Future connector/auth/security gates. | Safe summary only if reviewed. | Not permanent by default. |
| customer data | customer records, support data | `live_connector_on_demand` | `curated_summary_evidence_ref` | Permanent memory by default | Sensitive and externally/customer-owned. | Security/privacy/retention gates. | Evidence with strict limitations. | Not permanent by default. |
| ClickUp / task threads | tasks, comments | `live_connector_on_demand` | `curated_summary_evidence_ref` | Raw permanent ingestion | Operational and changing. | Connector/auth/retention gates. | Curated task summary only after review. | Not permanent by default. |
| GitHub issues / task systems | issues, PRs, project trackers | `live_connector_on_demand` | `curated_summary_evidence_ref` | Raw permanent ingestion by default | Volatile task state. | Connector/auth/network gates. | Curated summary if reviewed. | Not permanent by default. |
| runtime logs | process logs, traces, telemetry | `live_connector_on_demand` | volatile evidence metadata | Permanent memory, raw indexing | Logs may contain secrets and state. | GT-06/GT-13/GT-15. | Safe metadata only. | Local-only/volatile; no permanent default. |
| provider outputs | model/API responses | `blocked_until_gate` | `curated_summary_evidence_ref` | Source, authority, raw permanent memory | Provider outputs are generated evidence. | GT-08/GT-05/GT-15/output review. | Generated output evidence candidate, blocked by default. | Generated-sensitive/local-only. |
| tool outputs | command/tool outputs | `blocked_until_gate` | `curated_summary_evidence_ref` | Source, authority, raw permanent memory | Tool outputs are generated evidence. | GT-07/GT-04/GT-05/GT-15. | Generated output evidence candidate, blocked by default. | Generated-sensitive/local-only. |
| agent outputs | summaries, plans, drafts | `blocked_until_gate` | `curated_summary_evidence_ref` | Authority, raw permanent memory | Agent outputs are generated evidence. | GT-06/GT-04/GT-05/GT-15. | Generated output evidence candidate, blocked by default. | Generated-sensitive/local-only. |
| product/Siamese source | product code, product data | `blocked_until_gate` | none until GT-09 | Source loading, vector, graph, summary, publication | Product/Siamese source remains blocked until GT-09. | GT-09 plus security/validation/source posture. | ProductRef metadata only. | Blocked/product-restricted. |
| external source corpus | external snapshots, examples | `blocked_until_gate` or `markdown_full_read_canonical` if curated/reviewed | `markdown_wiki_moc` after review | Execution, source copy, raw ingestion | External raw source requires source/security/license review. | GT-11 and security review. | Evidence only, not adoption. | Metadata/curated only. |
| secrets / credentials | secret values, credential material | `excluded_from_permanent_memory` | safe metadata blocker only | Any memory/index/graph/summary | Secrets and credentials are never memory content. | Secure incident route. | Not evidence content. | Never retained as content. |
| API keys / tokens | keys, tokens, refresh tokens | `excluded_from_permanent_memory` | safe metadata blocker only | Any memory/index/graph/summary | Credential material must not be embedded or summarized. | Secure auth/incident route. | Not evidence content. | Never retained as content. |
| `.env` contents | environment file values | `excluded_from_permanent_memory` | safe metadata blocker only | Any memory/index/graph/summary | `.env` contents may contain secrets. | S-03 secure handling. | Not evidence content. | Never retained as content. |
| provider configs | raw provider configs | `excluded_from_permanent_memory` unless future safe metadata ref is approved | `blocked_until_gate` | Raw memory, auth use | Provider configs may contain auth/session material. | GT-08/security review. | Credential/auth blocker refs only. | Never content by default. |
| local credential stores | credential stores | `excluded_from_permanent_memory` | safe metadata blocker only | Any memory/index/graph/summary | Credential stores are never memory content. | Secure incident route. | Not evidence content. | Never retained as content. |
| browser auth/session material | cookies, sessions, browser state | `excluded_from_permanent_memory` | safe metadata blocker only | Any memory/index/graph/summary | Browser auth/session material is credential material. | Secure auth/incident route. | Not evidence content. | Never retained as content. |
| unknown sensitivity data | unclassified/mixed data | `unknown_retrieval_mode` or `blocked_until_gate` | safe metadata blocker | Ingestion, vector, graph, summary | Unknown sensitivity blocks promotion. | Classification/security review. | Evidence blocked. | Blocked until classified. |

## 8. Markdown Full-Read Canonical Criteria

Use `markdown_full_read_canonical` when:

| Criterion | Reason |
| --- | --- |
| Exact wording matters. | Snippets can distort obligations or stop rules. |
| Governance authority matters. | Governance decisions require stable canonical records. |
| Decisions must be auditable. | Full rationale, scope, limitations, and consequences must remain together. |
| Sequence and nuance matter. | Ordering can change interpretation. |
| Obligations and blockers must be preserved. | Retrieval must not strip blockers or limitations. |
| Source must be reviewed as a complete document. | Partial retrieval is insufficient. |
| Downstream agents must cite stable canonical records. | Stable docs prevent authority drift. |
| Retrieval must not fragment context. | Full-document reading preserves accountability. |

Examples: governance docs, activation gate records, P1/P2/P2.K contracts, P2.R reconciliation closure, ADRs, security policies, validation gate designs, and audit/retention/rollback baselines.

Markdown full-read canonical records may be indexed later for discovery, but the index must never replace full-document reading for authoritative use.

## 9. Markdown Wiki / MOC Criteria

Use `markdown_wiki_moc` when:

| Criterion | Reason |
| --- | --- |
| Knowledge is curated and navigable. | Manual structure improves orientation. |
| Topics benefit from manual structure. | Topic pages make routing explicit. |
| Links and maps-of-content improve orientation. | MOCs guide readers before canonical reads. |
| Corpus is stable enough for curated organization. | Stable corpus can support durable links. |
| Users or agents need routing before reading full docs. | MOC reduces path discovery friction. |

Examples: knowledge maps, curated research notes, project indexes, architecture MOCs, topic pages, source routing pages, decision indexes, and vocabulary indexes.

Wiki/MOC is a navigation/routing layer, not an authority replacement. MOC pages must route to canonical markdown documents.

## 10. Semantic Search / Vector Index Candidate Criteria

Use `semantic_search_vector_index_candidate` when:

| Criterion | Reason |
| --- | --- |
| Corpus is large. | Manual lookup may be inefficient. |
| Lookup is fuzzy. | User may not know exact terms or file names. |
| User does not know exact file/path/title. | Semantic discovery can route to source. |
| Corpus contains many similar notes. | Similarity search can find related material. |
| Recall-oriented discovery is more important than exact authority. | Search can surface candidates. |
| Documents are supplementary or exploratory. | Authority risk is lower. |
| Semantic search routes to source documents for full reading. | Search remains discovery, not authority. |

Examples: large research corpus, long video transcript corpus, large rule catalogs, large meeting corpus for fuzzy lookup only, supplementary notes, and non-authoritative research snippets.

Vector search is useful for fuzzy lookup and large corpora, but it is not ideal for documents that must be read completely, such as governance decisions, architecture contracts, activation gates, incident records, and meeting/decision records requiring full sequence and nuance.

Vector index candidates require future gates before implementation. P2.K2 does not implement vector DB or generate embeddings.

## 11. Graph / Cognitive Semantic System Candidate Criteria

Use `graph_cognitive_semantic_candidate` when:

| Criterion | Reason |
| --- | --- |
| Entities and relationships matter. | Entity/relation records can preserve connected context. |
| Dependencies must be traversed. | Blocker and dependency propagation benefits from graph-like traversal. |
| Ownership/lifecycle/state relationships matter. | Relationship metadata can expose impact paths. |
| Evidence relationships must be linked. | EvidenceRef networks support traceability. |
| Claims need supporting evidence. | SemanticClaim records require refs and limitations. |
| Blockers must propagate through relationships. | Dependency edges can carry blockers. |
| Impact analysis requires graph-like traversal. | Traversal can support future readiness analysis. |

Examples: SemanticEntity, SemanticClaim, SemanticRelation, EvidenceRef relationship networks, dependency maps, ownership maps, gate dependency maps, blocker propagation maps, source/ref relationships, and product-readiness relationships.

Graph/Cognitive Semantic System candidate records are relationship metadata only. They do not select substrate. Graph remains candidate only. Cognitive Semantic System substrate remains deferred.

## 12. Graphify Generated Evidence Handling

| Graphify-related data | Retrieval classification | Handling rule |
| --- | --- | --- |
| Graphify repo map summaries | `graphify_generated_evidence_ref` | Generated evidence refs, not authority. |
| Curated Graphify summaries | `curated_summary_evidence_ref` | Use only with limitations, refs, and review posture. |
| Raw Graphify outputs | `blocked_until_gate` | Local-only, blocked by default. |
| Graphify labels | Generated metadata | Not governance labels. |
| Graphify relationship evidence | Supporting generated evidence | Can support discussion, not decide. |

Graphify evidence is supporting generated evidence only, not authority.

Graphify evidence cannot approve source loading, provider/auth, tool execution, agent execution, product activation, generated output tracking, source tracking expansion, or Cognitive Semantic System substrate selection.

P2.K2 does not rerun Graphify. P2.K2 does not adopt Graphify. P2.K2 does not modify Graphify outputs.

## 13. Live Connector / On-Demand Criteria

Use `live_connector_on_demand` when data is:

| Data trait | Reason |
| --- | --- |
| Volatile | Permanent memory can go stale quickly. |
| Externally owned | Ownership and retention stay with the external system. |
| User-specific | Privacy and access context matter. |
| Customer-specific | Sensitivity and retention are high risk. |
| Frequently changing | Snapshot memory can mislead. |
| Operational rather than evergreen | Query-at-need is safer. |
| Too noisy for permanent memory | Raw ingestion increases risk and cost. |
| Sensitive by default | Security/retention review required. |
| Better queried at time of need | Current-state lookup beats stale storage. |

Examples: Slack, email, ClickUp / task threads, GitHub issues, task systems, customer data, provider outputs, runtime logs, temporary task state, product state, and incident state.

Live connector data should not become permanent memory by default. It may produce curated summaries only after future security, retention, evidence, and governance review.

## 14. Excluded From Permanent Memory Criteria

Use `excluded_from_permanent_memory` for:

| Excluded class | Rule |
| --- | --- |
| Secrets | Never memory content. |
| Credentials | Never memory content. |
| API keys | Never memory content. |
| Tokens | Never memory content. |
| Passwords | Never memory content. |
| Private keys | Never memory content. |
| Browser auth/session material | Never memory content. |
| Local credential-store contents | Never memory content. |
| `.env` contents | Never memory content. |
| Raw provider configs | Never memory content unless future safe metadata ref is approved. |
| Raw customer-sensitive data | Not permanent memory by default. |
| Raw product source before GT-09 | Blocked. |
| Raw local-only source without approval | Blocked. |
| Raw generated output with unknown sensitivity | Blocked/quarantine candidate. |
| Unknown sensitivity data | Blocked until classified. |

Secrets and credentials are never memory content.

Exclusion is not loss of governance; safe metadata refs may record that excluded material exists as a blocker. Excluded material must not be embedded, summarized, indexed, graphed, persisted, transmitted, or published by default.

## 15. Generated Output And Curated Summary Policy

| Policy item | Rule |
| --- | --- |
| Generated summaries | May become EvidenceRef only after review. |
| Generated raw outputs | Blocked by default. |
| Generated output tracking | Not approved by P2.K2. |
| Generated outputs as source | Generated outputs are not source by default. |
| Raw generated output | May require quarantine/removal review. |
| Curated summaries | Must include limitations, EvidenceRef, retention posture, and review status. |

Generated-output classes:

| Class | Meaning | Retrieval posture |
| --- | --- | --- |
| `generated_summary_unreviewed` | Summary exists but is not reviewed. | Blocked until review. |
| `generated_summary_curated` | Summary reviewed for safe metadata use. | `curated_summary_evidence_ref`. |
| `generated_raw_output_blocked` | Raw generated output exists but is blocked. | `blocked_until_gate`. |
| `generated_sensitive_local_only` | Generated output remains local-only/generated-sensitive. | Blocked/local-only. |
| `generated_output_quarantine_required` | Output may require quarantine/removal review. | Incident/quarantine route. |
| `generated_output_tracking_not_approved` | Tracking is not approved. | No source tracking or publication. |

## 16. Decision Algorithm

Deterministic P2.K2 retrieval-mode decision algorithm:

1. Classify `data_type`.
2. Identify `source_classification` and `sensitivity`.
3. If secret/credential/auth material, choose `excluded_from_permanent_memory`.
4. If product source and GT-09 is absent, choose `blocked_until_gate`.
5. If volatile/live/customer/task/email/Slack/runtime state, choose `live_connector_on_demand`.
6. If exact governance/contract/decision record, choose `markdown_full_read_canonical`.
7. If curated navigation improves discovery, add `markdown_wiki_moc`.
8. If large fuzzy corpus and no exact full-read authority requirement, mark `semantic_search_vector_index_candidate`.
9. If entity/relationship/dependency/evidence traversal is primary, mark `graph_cognitive_semantic_candidate`.
10. If generated output, apply generated-output posture and EvidenceRef rules.
11. Preserve blockers, limitations, retention posture, and pending peer alignment.
12. If uncertain, choose `unknown_retrieval_mode` and block promotion.

When in doubt, prefer safe markdown metadata and blockers over automatic ingestion.

## 17. Interfaces With P2.1 / P2.2 / P2.3

### P2.1 Interface

P2.K2 consumes P2.1 canonical vocabulary for statuses, blockers, sensitivity classes, source classifications, posture fields, and refs. P2.K2 uses canonical status/posture terms where possible, aligns aliases/deprecated terms, and records unresolved vocabulary drift if a future term cannot be mapped.

P2.1 is present, so no P2.K2 vocabulary dependency is marked `pending_P2.1_alignment` except for future retrieval-specific terms that are not yet validated by a later schema.

### P2.2 Interface

Every evidence-bearing retrieval mode must preserve EvidenceRef posture. Generated outputs must preserve EvidenceRef limitations. SourceRef, ValidationRef, SecurityRef, GraphifyRef, and ProductRef relationships must be preserved.

RetrievalMode cannot erase EvidenceRef blockers, limitations, authority posture, generated-output posture, local-only posture, product posture, source classification, sensitivity, retention posture, or review requirements.

### P2.3 Interface

Every retrieval mode must declare retention posture. Live connectors require retention, rollback, incident, security, and audit posture before activation. Excluded memory classes require incident/quarantine posture if breached. Publication/source tracking blockers must propagate.

P2.K2 does not implement runtime logging, persistence, telemetry, rollback automation, incident automation, source tracking, generated output tracking, or publication.

## 18. Interfaces With P2.K1 / P2.K3 / P2.K4

### P2.K1 Interface

P2.K1 is absent, so Four Cs / five-level dependencies are marked `pending_P2.K1_alignment`.

Expected future alignment:

| Retrieval mode | Expected five-level mapping posture |
| --- | --- |
| Markdown full-read canonical | Routing/wiki/governance canonical record level. |
| Markdown wiki / MOC | Routing/wiki level. |
| Vector | Level 3 candidate. |
| Graph | Level 4 candidate. |
| Live/cadence | Level 5 candidate but blocked. |

### P2.K3 Interface

P2.K3 is absent, so harness-routing dependencies are marked `pending_P2.K3_alignment`.

RetrievalMode decisions must be consumable by multiple harnesses as metadata guidance only. A future canonical manifest may reference retrieval mode decisions. AGENTS.md/CLAUDE.md/OpenCode/Codex/Hermes projections must not duplicate or weaken this matrix. Harness routing is future metadata projection only.

### P2.K4 Interface

P2.K4 is absent, so live-connection/cadence dependencies are marked `pending_P2.K4_alignment`.

Volatile data defaults to live connector posture. Cadence/GBrain/Hermes always-on behavior remains blocked. Live connectors require future gates, retention, rollback, incident handling, audit, provider/auth/security review, and exact activation approval.

## 19. Harness Consumption Rules

| Rule | Required behavior |
| --- | --- |
| Harnesses may read this matrix. | Metadata guidance only. |
| Harnesses must not implement retrieval automatically. | No runtime behavior follows from this document. |
| Harnesses must not convert vector candidates into embedding jobs. | Vector implementation remains future-gated. |
| Harnesses must not convert graph candidates into graph DB writes. | Graph implementation and persistence remain future-gated. |
| Harnesses must not convert live connector candidates into connector activation. | Live connector activation remains future-gated. |
| Harnesses must not ingest excluded material. | Secrets, credentials, auth material, blocked product source, and unknown sensitivity remain excluded. |
| Harnesses must preserve gate posture, sensitivity, retention, blockers, and limitations. | P2.1/P2.2/P2.3 propagation rules apply. |
| Harness-specific routing projections are future work. | P2.K3/P2.KR may define projections later. |

## 20. Boundaries And Invariants

| ID | Invariant |
| --- | --- |
| RTM-001 | RetrievalMode is metadata, not implementation. |
| RTM-002 | RetrievalMode is not permission. |
| RTM-003 | Markdown is canonical for governance and contracts. |
| RTM-004 | Wiki/MOC is navigation, not authority. |
| RTM-005 | Vector search is optional and data-type-specific. |
| RTM-006 | Vector search is for fuzzy lookup, not authoritative full-read replacement. |
| RTM-007 | Graph is candidate relationship/evidence structure only. |
| RTM-008 | Cognitive Semantic System substrate remains deferred. |
| RTM-009 | Graphify evidence is supporting generated evidence only, not authority. |
| RTM-010 | Live connectors remain gate-controlled. |
| RTM-011 | Volatile/live data is not permanent memory by default. |
| RTM-012 | Secrets and credentials are never memory content. |
| RTM-013 | Product/Siamese source remains blocked until GT-09. |
| RTM-014 | Generated outputs are not source by default. |
| RTM-015 | Evidence supports; it does not decide. |
| RTM-016 | Validation evaluates; governance decides. |
| RTM-017 | Security constrains; it does not activate. |
| RTM-018 | Provider metadata is not provider activation. |
| RTM-019 | Tool metadata is not tool execution. |
| RTM-020 | Agent metadata is not agent execution. |
| RTM-021 | GBrain/Hermes/Cadence remains future and blocked. |
| RTM-022 | AGENT PLATFORM remains pre-active at AL-1. |

## 21. Future Validation Targets

These are future validation targets only. P2.K2 does not execute validation.

| Future validation target | Purpose |
| --- | --- |
| DataClass required fields completeness | Check all required DataClass fields. |
| RetrievalMode vocabulary conformance | Check RetrievalMode values. |
| data_type to retrieval mode matrix conformance | Check matrix mappings. |
| no-secret/no-credential memory invariant | Check excluded-memory posture without reading values. |
| product source blocked until GT-09 invariant | Check product source remains blocked. |
| vector candidate not implemented invariant | Check vector candidates do not trigger embeddings/index jobs. |
| graph candidate not substrate invariant | Check graph candidates do not imply selected substrate. |
| Graphify supporting evidence only invariant | Check Graphify evidence remains supporting generated evidence only. |
| live connector not permanent memory invariant | Check live connector classes are not ingested by default. |
| generated output not source invariant | Check generated outputs remain generated evidence. |
| markdown canonical governance invariant | Check governance/contract docs remain canonical markdown. |
| full-read required documents not vector-only invariant | Check full-read docs are not reduced to vector-only retrieval. |
| EvidenceRef propagation invariant | Check evidence refs and limitations propagate. |
| retention posture propagation invariant | Check P2.3 retention posture propagates. |
| P2.K1/P2.K3/P2.K4 alignment check | Check peer dependency closure after peer docs exist. |
| P2.KR reconciliation readiness check | Check readiness for future knowledge architecture reconciliation. |

## 22. Future Hardening Candidates

These future tickets are not started by P2.K2.

| Candidate ticket | Purpose | P2.K2 status |
| --- | --- | --- |
| RTM-HARD-01 - RetrievalMode Schema Alignment | Define future schema for retrieval mode records. | Not started. |
| RTM-HARD-02 - DataClass Classification Contract | Harden DataClass fields and blockers. | Not started. |
| RTM-HARD-03 - Markdown Canonical Governance Memory Contract | Harden full-read markdown canonical criteria. | Not started. |
| RTM-HARD-04 - Wiki / MOC Routing Contract | Harden MOC navigation and routing rules. | Not started. |
| RTM-HARD-05 - Semantic Search Candidate Gate Design | Define future vector/index gate. | Not started. |
| RTM-HARD-06 - Graph / Cognitive Semantic System Candidate Boundary Contract | Harden graph relationship metadata boundaries. | Not started. |
| RTM-HARD-07 - Live Connector Retrieval Boundary Contract | Define live connector retrieval gate. | Not started. |
| RTM-HARD-08 - Excluded Memory / No-Permanent-Ingestion Contract | Harden excluded-memory handling. | Not started. |
| RTM-HARD-09 - Generated Output Curated Summary Contract | Harden generated summary promotion to EvidenceRef. | Not started. |
| RTM-HARD-10 - Harness Retrieval Mode Projection Contract | Define future harness projection rules. | Not started. |

## 23. Created / Not Created Register

Created:

| Artifact | Status |
| --- | --- |
| Hybrid retrieval mode decision matrix document | Created. |
| `0_architecture/governance/agent_platform_hybrid_retrieval_mode_decision_matrix.md` | Created. |

Not created / not approved:

| Artifact or action | P2.K2 status |
| --- | --- |
| Runtime code modified | No runtime code modified. |
| Runtime activation | No runtime activation. |
| Validation execution | No validation execution. |
| Tests executed | No tests executed. |
| Vector DB implementation | No vector DB implementation. |
| Embeddings generated | No embeddings generated. |
| Semantic search implementation | No semantic search implementation. |
| Graph DB implementation | No graph DB implementation. |
| Cognitive Semantic System persistence implemented | No Cognitive Semantic System persistence implemented. |
| Cognitive Semantic System substrate selected | No Cognitive Semantic System substrate selected. |
| Graphify rerun | No Graphify rerun. |
| Graphify adoption | No Graphify adoption. |
| Graphify output modified | No Graphify output modified. |
| GBrain implementation | No GBrain implementation. |
| Hermes activation | No Hermes activation. |
| Cadence / always-on behavior activated | No Cadence / always-on behavior activated. |
| Provider/auth/API/MCP configured | No provider/auth/API/MCP configured. |
| Provider/API/network/MCP call executed | No provider/API/network/MCP call executed. |
| Tool execution approved | No tool execution approved. |
| Agent execution approved | No agent execution approved. |
| Product source inspected | No product source inspected. |
| Source loading approved | No source loading approved. |
| Local-only source loaded | No local-only source loaded. |
| External source loaded | No external source loaded. |
| Raw generated output loaded | No raw generated output loaded. |
| Generated output tracking approved | No generated output tracking approved. |
| Source tracking expansion approved | No source tracking expansion approved. |
| Secrets inspected | No secrets inspected. |
| Credentials inspected | No credentials inspected. |
| `.env` inspected | No `.env` inspected. |
| Provider configs inspected | No provider configs inspected. |
| `.graphifyignore` modified | No `.graphifyignore` modified. |
| `.gitignore` modified | No `.gitignore` modified. |
| P2.K1 file created | No P2.K1 file created. |
| P2.K3 file created | No P2.K3 file created. |
| P2.K4 file created | No P2.K4 file created. |
| P2.KR file created | No P2.KR file created. |
| P3.0/P3.1/P3.2 started | No P3.0, P3.1, or P3.2 started. |
| Git staging/commit/push/force-add/publication performed | No Git staging, commit, push, force-add, or publication performed. |

## 24. Recommended Next Tickets

After P2.K2:

| Ticket | Recommendation |
| --- | --- |
| P2.K1 - Four Cs / Five Levels Mapping | Start if not already completed. |
| P2.K3 - Harness-Agnostic Routing / Memory Manifest Strategy | Start if P2.K1 is already running or complete. |
| P2.K4 - Live Connections / Cadence Boundary Strategy | Start after P2.K3 or as governed sequence allows. |
| P2.KR - Knowledge Architecture Reconciliation Closure | Start after P2.K1-P2.K4 are complete. |
| P3.0 - Controlled Source Classification Readiness | Start after P2.KR only. |
| P3.1 - Validation Execution Readiness | Start after P2.KR only. |
| P3.2 - Security Enforcement Readiness | Start after P2.KR only. |

Recommended actual: P2.K3 - Harness-Agnostic Routing / Memory Manifest Strategy, if P2.K1 is already running or complete.

Otherwise: P2.K1 - Four Cs / Five Levels Mapping.

Do not start P2.K3, P2.K4, P2.KR, P3.0, P3.1, or P3.2 from this ticket.

## 25. Final Verdict

| Question | Answer |
| --- | --- |
| What did P2.K2 create? | The canonical Hybrid Retrieval Mode Decision Matrix document. |
| What retrieval decision matrix was defined? | A DataClass-driven matrix that maps data types to full-read markdown, wiki/MOC, vector candidate, graph/Cognitive Semantic System candidate, Graphify generated evidence refs, live connector on-demand, curated summary EvidenceRef, excluded memory, blocked until gate, or unknown retrieval posture. |
| What RetrievalMode values were defined? | `markdown_full_read_canonical`, `markdown_wiki_moc`, `semantic_search_vector_index_candidate`, `graph_cognitive_semantic_candidate`, `graphify_generated_evidence_ref`, `live_connector_on_demand`, `curated_summary_evidence_ref`, `excluded_from_permanent_memory`, `blocked_until_gate`, and `unknown_retrieval_mode`. |
| What DataClass fields are required? | `data_class_id`, `data_type`, `canonical_description`, `source_classification`, `sensitivity`, `volatility`, `query_pattern`, `required_context_completeness`, `relationship_density`, `retention_posture`, `generated_output_posture`, `local_only_posture`, `product_posture`, `provider_auth_posture`, `evidence_posture`, `recommended_retrieval_mode`, `secondary_retrieval_modes`, `forbidden_retrieval_modes`, `required_gates`, `review_required`, `blockers`, `limitations`, `evidence_refs`, `validation_refs`, `security_refs`, and `pending_alignment_refs`. |
| What query patterns were defined? | Exact policy lookup, full decision read, contract compliance read, fuzzy lookup large corpus, navigable topic exploration, entity relationship traversal, dependency trace, volatile state lookup, task thread lookup, incident sensitive lookup, product source lookup blocked, credential secret lookup blocked, and unknown query pattern. |
| What data_type to retrieval mode mappings were defined? | Governance, gates, contracts, P2.R, research, transcripts, meetings, ADRs, rule catalogs, entities, relations, dependency maps, Graphify summaries/raw outputs, generated summaries/raw outputs, Slack, email, customer data, task systems, logs, provider/tool/agent outputs, product/Siamese source, external corpus, secrets, credentials, API keys, tokens, `.env`, provider configs, credential stores, browser auth, and unknown sensitivity data. |
| Which data types remain markdown full-read canonical? | Governance docs, activation gates, P1/P2 contracts, P2.R closure, ADRs, security policies, validation gate designs, audit/retention/rollback baselines, and meeting/decision records requiring sequence and nuance. |
| Which data types may use wiki/MOC? | Knowledge maps, curated research notes, project indexes, architecture MOCs, topic pages, source routing pages, decision indexes, vocabulary indexes, and large curated research corpora. |
| Which data types are vector search candidates? | Large research corpus, long video transcript corpus, large rule catalogs, supplementary notes, non-authoritative snippets, and large meeting corpora for fuzzy lookup only. |
| Which data types are graph / Cognitive Semantic System candidates? | SemanticEntity, SemanticClaim, SemanticRelation, EvidenceRef networks, dependency maps, ownership maps, gate dependency maps, blocker propagation maps, source/ref relationships, and product-readiness relationships. |
| Which data types remain live connector by default? | Slack, email, ClickUp/task threads, GitHub issues/task systems, customer data, provider outputs, runtime logs, temporary task state, product state, and incident state. |
| Which data types are excluded from permanent memory? | Secrets, credentials, API keys, tokens, passwords, private keys, browser auth/session material, local credential stores, `.env` contents, raw provider configs by default, raw customer-sensitive data, raw product source before GT-09, raw local-only source without approval, raw generated output with unknown sensitivity, and unknown sensitivity data. |
| How are Graphify summaries and raw Graphify outputs handled? | Curated Graphify summaries are generated evidence refs or curated summary EvidenceRef; raw Graphify outputs are local-only and blocked by default. |
| How are generated outputs handled? | Generated summaries may become EvidenceRef only after review; raw generated outputs are blocked by default and may require quarantine/removal review. |
| How are secrets and credentials handled? | Secrets and credentials are never memory content and must not be embedded, summarized, indexed, graphed, persisted, transmitted, or published by default. |
| How is product/Siamese source handled? | Product/Siamese source remains blocked until GT-09 and is not inspected, loaded, summarized, indexed, graphed, or activated by P2.K2. |
| How does P2.K2 interface with P2.1, P2.2, and P2.3? | It consumes P2.1 vocabulary, preserves P2.2 EvidenceRef/SourceRef/ValidationRef/SecurityRef/GraphifyRef/ProductRef relationships, and propagates P2.3 retention, rollback, incident, publication, and source-tracking blockers. |
| How does P2.K2 interface with P2.K1, P2.K3, and P2.K4? | P2.K1, P2.K3, and P2.K4 are absent, so peer dependencies are marked `pending_P2.K1_alignment`, `pending_P2.K3_alignment`, and `pending_P2.K4_alignment`. |
| Did P2.K2 implement vector DB? | No. |
| Did P2.K2 generate embeddings? | No. |
| Did P2.K2 implement graph DB? | No. |
| Did P2.K2 adopt Graphify? | No. |
| Did P2.K2 activate Hermes/GBrain/Cadence? | No. |
| Did P2.K2 configure provider/auth/API/MCP? | No. |
| Did P2.K2 execute tools or agents? | No. |
| Did P2.K2 inspect product source? | No. |
| Did P2.K2 approve source loading? | No. |
| Did P2.K2 approve generated output tracking? | No. |
| Did P2.K2 approve source tracking expansion? | No. |
| Was Cognitive Semantic System substrate selected? | No. Cognitive Semantic System substrate remains deferred. |
| What is the next ticket? | P2.K1 - Four Cs / Five Levels Mapping, unless P2.K1 is already running or complete; then P2.K3 - Harness-Agnostic Routing / Memory Manifest Strategy after explicit instruction only. |

Stop rule: After completing P2.K2, STOP. Do not start P2.K1. Do not start P2.K3. Do not start P2.K4. Do not start P2.KR. Do not start P3.0. Do not start P3.1. Do not start P3.2. Do not implement runtime code. Do not run validation. Do not run tests. Do not implement vector DB. Do not generate embeddings. Do not implement semantic search. Do not implement graph DB. Do not implement Cognitive Semantic System persistence. Do not select Cognitive Semantic System substrate. Do not rerun Graphify. Do not adopt Graphify as authority. Do not implement GBrain. Do not activate Hermes. Do not activate Cadence / always-on behavior. Do not configure provider/auth. Do not call provider/API/network/MCP. Do not execute tools. Do not activate agents. Do not inspect product source. Do not load source. Do not approve generated output tracking. Do not approve source tracking expansion. Do not inspect secrets. Do not inspect credentials. Do not modify generated outputs. Do not stage, commit, push, force-add, or publish.
