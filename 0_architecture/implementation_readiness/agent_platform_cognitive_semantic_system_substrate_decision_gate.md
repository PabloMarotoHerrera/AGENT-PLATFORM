# IR-07 - Cognitive Semantic System Substrate Decision Gate
## 1. Document Header
| Field | Value |
| --- | --- |
| Title | Cognitive Semantic System Substrate Decision Gate |
| Ticket | IR-07 |
| Status | Accepted Cognitive Semantic System substrate decision gate |
| Date | 2026-07-02 |
| Scope | Decision-gate assessment for the future Cognitive Semantic System substrate after IR-06 for AGENT PLATFORM / Siamese. |
| Authority | Decision-gate assessment only, not substrate implementation. |
| Related documents | IR-00 through IR-06, CSS-series, P-A, P-00 through P-10, M-A, M-03, M-05, M-06, W-series, V-series, S-series, H-series, `.gitignore`, `README.md`, Siamese Product Vision |
| Gate target | Future Cognitive Semantic System substrate decision |

## 2. Purpose
IR-00 found the platform not ready for implementation but ready for planning tickets. IR-01 reserved `3_platform` conceptually only. IR-02 blocked source tracking and source tree creation. IR-03 blocked scripts/tools/tests creation and execution. IR-04 blocked dependency adoption and package manager execution. IR-05 blocked runtime/agent/context implementation. IR-06 blocked provider/adapter/MCP/API/network/auth activation.

IR-07 assesses the Cognitive Semantic System substrate decision gate. IR-07 does not implement or prototype any substrate. IR-07 prepares IR-08 after explicit instruction and does not start IR-08.

## 3. Cognitive Semantic System Substrate Decision Gate Definition
The gate is a governance assessment that determines whether enough evidence exists to select, defer, or reject substrate classes for the Cognitive Semantic System before any implementation, source tracking, dependency adoption, runtime activation, provider activation, or prototype work.

Decision gate is not implementation, prototype creation, final substrate selection unless evidence is sufficient, graph adoption, vector-store adoption, database adoption, ontology adoption, dependency adoption, provider/API/MCP activation, or product activation.

## 4. Decision Summary
Cognitive Semantic System is the accepted name. Final substrate remains undecided. Default verdict: substrate decision deferred. Existing governance does not provide sufficient evidence to select a final substrate now.

Graph remains a candidate only. Graphify remains evidence/historical/external/prohibited/candidate-evidence only, not authority. No graph/vector/database/ontology/event/context runtime is created. No substrate dependency is adopted. No substrate source tracking is approved. No provider/API/MCP activation occurs. Governance docs under `0_architecture/implementation_readiness/` remain trackable as docs only by exact path and human instruction. IR-08 may assess validation / security enforcement readiness after explicit instruction.

## 5. Authority Boundary
| Layer | IR-07 boundary |
| --- | --- |
| Governance | Decides final substrate selection, implementation, exceptions, source tracking, dependency adoption, publication, and lifecycle. |
| Validation | Evaluates substrate evidence. |
| Security | Constrains local-only data, sensitive context, generated outputs, runtime, provider/API/MCP/network/auth, secrets, credentials, and publication. |
| IR-07 | Assesses substrate decision readiness only. |
| Products | May provide requirements but cannot decide substrate. |
| Graphify/external sources | Evidence only. |
| Agents | May prepare safe decision-gate metadata but cannot implement, execute, activate, adopt, stage, commit, push, publish, or start IR-08. |

## 6. Source Boundary
CSS-series controls accepted name and substrate-neutral decisions. M-03 controls conflicted semantic material normalization. M-05/M-06 control research/external evidence posture. IR-06 controls provider/API/MCP activation blockers. IR-05 controls runtime/agent/context blockers. IR-04 controls dependency blockers. IR-02 controls source tracking blockers. W-series controls cognitive workspace/context/governance. V-series controls proof/evidence. S-series controls security/local-only.

Raw Graphify/external source contents are not adopted. Raw `3_platform`, `2_products`, and `4_external/sources` are not inspected. Safe metadata only.

## 7. Current CSS Posture
| area | current posture | decision status | blocked action | future route |
| --- | --- | --- | --- | --- |
| system name | Cognitive Semantic System. | name accepted | Rename to old/external names. | Preserve. |
| substrate | No final substrate. | substrate undecided | Select without evidence. | Decision gate. |
| graph | Relationship candidate. | graph candidate only | Treat as truth. | Compare via criteria. |
| Graphify material | Historical/external evidence. | evidence only | Authority/name adoption. | Normalize/review. |
| vector store | Candidate retrieval layer. | candidate only | Embeddings/index. | Evidence/security review. |
| relational/document store | Candidate records. | candidate only | DB/schema/files as truth. | Schema/governance review. |
| ontology/knowledge graph | Candidate formal semantics. | candidate only | Ontology/reasoner. | Criteria/review. |
| event log | Candidate audit trail. | candidate only | Event runtime. | Audit model review. |
| context pack layer | Selected exposure. | not substrate by default | Treat context as permission. | Context gate. |
| evidence registry | Needed conceptually. | not implemented | Registry runtime. | IR-08. |
| product requirements | Inform criteria. | non-authorizing | Decide substrate. | Product governance. |
| provider/API/MCP | Blocked. | blocked | Activation. | IR-06 gates. |
| runtime/prototype | None. | blocked | Prototype/runtime. | Prototype gate. |
| source tracking | Docs only. | blocked | Track schemas/indexes. | IR-02 future gate. |
| dependencies | Candidate only. | blocked | Adopt tools/stores. | IR-04 gates. |

## 8. Candidate Substrate Class Catalog
| class | meaning | possible future use | current status | key risks | required future evidence | blocked now |
| --- | --- | --- | --- | --- | --- | --- |
| graph_database_or_property_graph | Nodes/edges store. | lineage, relations. | candidate_keep | graph-as-truth. | schema/query/security. | adoption/runtime. |
| knowledge_graph_or_ontology | Formal types/rules. | constraints/inference. | candidate_keep | inference as approval. | ontology/version/reasoner review. | schema/reasoner. |
| relational_store | Tables/constraints. | registries/audit. | candidate_keep | rigid model. | schema/migration/validation. | DB creation. |
| document_store | Documents/records. | flexible records. | candidate_keep | drift/path authority. | version/query/security. | store creation. |
| vector_store_or_embedding_index | Similarity retrieval. | context discovery. | candidate_keep_with_caution | leakage/weak truth. | sensitivity/model/provenance. | embeddings/index. |
| event_log_or_append_only_ledger | Append-only events. | provenance/replay. | candidate_keep | retention risk. | retention/redaction/replay. | event store. |
| file_based_evidence_registry | Human-readable files. | evidence records. | candidate_keep | weak querying. | registry schema/governance. | registry. |
| context_pack_registry | Pack metadata. | selected exposure. | candidate_keep | permission confusion. | source/sensitivity/freshness. | runtime packs. |
| hybrid_multi_substrate | Multiple bounded stores. | practical composition. | candidate_keep_with_caution | sync complexity. | authority hierarchy/rollback. | design/adoption. |
| semantic_projection_layer | Derived views. | graph/views/search. | candidate_keep | projection as truth. | lineage/staleness policy. | runtime. |
| in_memory_runtime_index | transient runtime index. | fast selection. | defer | state leakage. | retention/cache policy. | runtime. |
| external_provider_backed_substrate | hosted store/service. | managed infra. | blocked_now | data/provider/cost. | IR-06 + terms/security. | activation. |
| unknown_future_substrate | later option. | future evidence. | defer | unknown. | classification/criteria. | use. |

## 9. Evaluation Criteria
Criteria: governance authority preservation; source traceability; evidence binding; context sensitivity handling; local-only enforcement; reversibility; auditability; explainability; schema/version governance; conflict handling; freshness/staleness handling; security/access control; dependency/runtime risk; provider/network risk; implementation complexity; validation feasibility; product interoperability; migration path; generated-output handling; human approval integration; failure/rollback behavior.

## 10. Candidate Evaluation Matrix
| candidate | current fit | evidence maturity | security risk | dependency risk | validation risk | implementation readiness | current verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| graph/property graph | Strong relation fit. | Criteria only. | Medium. | Medium/high. | Medium. | Not ready. | candidate_keep |
| knowledge graph/ontology | Strong constraint fit. | Criteria only. | Medium. | Medium/high. | High. | Not ready. | candidate_keep_with_caution |
| relational/document | Good audit fit. | Criteria only. | Medium. | Medium. | Medium. | Not ready. | candidate_keep |
| vector/embedding | Good retrieval fit. | Criteria only. | High. | High. | High. | Not ready. | candidate_keep_with_caution |
| event log | Good audit fit. | Criteria only. | Medium/high. | Medium. | Medium. | Not ready. | candidate_keep |
| file/evidence registry | Good governance fit. | Criteria only. | Low/medium. | Low. | Medium. | Not ready. | candidate_keep |
| context-pack registry | Good context fit. | Criteria only. | Medium. | Low/medium. | Medium. | Not ready. | candidate_keep |
| hybrid | Broad fit. | Criteria only. | Medium/high. | High. | High. | Not ready. | defer |
| external provider-backed | Possible infra fit. | Insufficient. | High. | High. | High. | Blocked. | blocked_now |

## 11. Graph Candidate Posture
Graph remains a candidate only. Graph can model relationships, provenance, dependencies, entities, evidence links, and semantic projections. Graph does not automatically become truth authority. Graph structure does not decide governance.

Graph implementation requires schema, query model, storage, validation, security, migration, versioning, dependency review, and rollback. No graph database, graph schema, graph runtime, graph library, or graph source is adopted by IR-07.

## 12. Graphify Posture
Graphify is evidence only, not authority. Graphify is not the accepted system name. Graphify does not own truth. Graphify material remains evidence/historical/external/prohibited/candidate-evidence only. Rejected strings such as `Platform Graphify`, `Graphify Authority`, and `Graphify owns truth` are historical/prohibited examples only.

Any Graphify-derived idea must pass normalization, conflict review, source/provenance review, security review, dependency review, and governance. No raw Graphify source or instruction is adopted.

## 13. Vector / Embedding Posture
Vector stores and embeddings are candidates only. Vector similarity is not semantic truth. Embeddings can leak sensitive context and local-only data if mishandled. Vectorization requires source classification, sensitivity controls, retention/deletion, model/provider/dependency review, reproducibility, and auditability. No embeddings, vector index, model, provider, or store is created or adopted.

## 14. Ontology / Knowledge Graph Posture
Ontologies and knowledge graphs are candidates only. Formal semantics may help with types, constraints, inference, and validation. Ontology does not replace governance. Inference output is evidence, not approval. Ontology adoption requires schema governance, reasoning limits, validation rules, conflict handling, versioning, and tool/dependency review. No ontology, reasoner, graph schema, or knowledge base is created.

## 15. Relational / Document / File Registry Posture
Relational, document, and file-based evidence registries are candidates only. Simpler stores may be easier to audit, version, diff, and govern, but may lack rich semantic traversal unless paired with projections. No database, table schema, document DB, file registry, or implementation source is created. Adoption requires schema, source tracking, validation, security, and governance.

## 16. Event Log / Ledger Posture
Event logs or append-only ledgers are candidates only. They may support auditability, provenance, and replay. They do not solve semantic modeling alone and can retain sensitive data indefinitely if not governed. No event store, ledger, or append-only runtime is created.

## 17. Hybrid Substrate Posture
Hybrid substrate remains likely as a future candidate, but not selected by IR-07 because evidence is insufficient. A hybrid may separate evidence storage, semantic projection, vector retrieval, audit log, and context pack registry. Hybrid design increases integration complexity. Adoption requires clear authority hierarchy, ownership, data boundaries, validation, dependency posture, and rollback.

## 18. External Provider-backed Substrate Posture
External provider-backed substrate is blocked now. Provider availability is not provider permission. Provider/API/MCP needs do not decide substrate. External storage or hosted graph/vector/DB services require IR-06 gates, security review, data classification, cost/terms review, and governance. No provider-backed substrate is activated.

## 19. Product Requirement Relationship
Siamese product routes can inform criteria, but product requirements cannot decide CSS substrate. Omniverse visualization does not require graph as truth. EnergyPlus solver needs do not decide CSS substrate. CLI/Desktop/Web needs do not decide CSS substrate. Product integration remains inactive and local-only. Product source remains local-only.

## 20. Context / Evidence Relationship
Context packs are not the substrate by default. Context inclusion is not permission. Evidence binding is required before claims become usable. Evidence supports validation but does not approve action. CSS substrate must preserve source references, sensitivity, exclusion, freshness, blockers, and governance decisions. Local-only raw content remains excluded.

## 21. Validation / Security Relationship
Substrate decision requires validation and security enforcement readiness. IR-07 does not create validation registry or security enforcement. Validation/security enforcement readiness is deferred to IR-08. Future substrate must be testable, auditable, least-privilege, reversible, and sensitive-data aware.

## 22. Runtime / Provider / Dependency Relationship
IR-07 does not activate runtime, provider/API/MCP, or dependencies. Any substrate implementation will require IR-04/IR-05/IR-06/IR-08 gates. Tool availability is not permission. Provider credentials are not provider permission. MCP availability is not MCP activation.

## 23. Source Tracking / Git Relationship
IR-07 does not approve source tracking, change product Git posture, or modify `.gitignore`. CSS substrate source, schemas, graph files, ontologies, embeddings, database files, indexes, generated outputs, and prototypes are not trackable now. Governance docs only are trackable by exact path and human instruction. No force-add is authorized. No `git add .` is authorized.

## 24. Substrate Decision Gate
Before final substrate selection: decision owner, candidate class, authority model, data/source classes, sensitivity model, local-only exclusions, evidence binding model, schema/version model, validation plan, security/access plan, dependency/runtime posture, provider/API/MCP posture, source tracking posture, migration path, rollback/removal path, auditability model, and governance approval must be recorded.

IR-07 does not pass this gate because the evidence remains insufficient for final substrate selection.

## 25. Prototype Gate
Before any CSS prototype: substrate decision or explicit prototype exception, prototype scope, source tracking posture, dependency posture, data/sensitivity policy, generated-output policy, runtime/tool/provider/MCP behavior, validation/security plan, exact paths, rollback/removal path, and governance approval must be recorded.

IR-07 does not pass this gate.

## 26. Decision Status Model
Statuses: name_accepted, substrate_undecided, substrate_decision_deferred, candidate_graph_retained, candidate_vector_retained, candidate_ontology_retained, candidate_relational_document_retained, candidate_event_log_retained, candidate_file_registry_retained, candidate_hybrid_retained, external_provider_backed_blocked, implementation_not_started, prototype_not_approved, source_tracking_not_approved, rejected_for_final_selection_now.

Current status: name_accepted + substrate_decision_deferred + candidate_hybrid_retained + candidate_graph_retained + implementation_not_started + prototype_not_approved.

## 27. Readiness Gate Model
| Gate | pass condition | current posture | blocker if missing |
| --- | --- | --- | --- |
| IR07-G01 IR-06 exists | IR-06 document exists. | Present. | Provider posture unknown. |
| IR07-G02 CSS-series exists | CSS-00/01/02/A exist. | Present. | Name/substrate evidence missing. |
| IR07-G03 accepted name preserved | Cognitive Semantic System retained. | Pass. | Stop. |
| IR07-G04 substrate not selected without sufficient evidence | Selection deferred. | Pass. | Stop/governance. |
| IR07-G05 graph remains candidate only | No graph adoption. | Pass. | Stop. |
| IR07-G06 Graphify remains evidence only | No authority use. | Pass. | Stop. |
| IR07-G07 no runtime/prototype created | No prototype. | Pass. | Stop. |
| IR07-G08 no dependencies adopted | No adoption/install. | Pass. | Stop. |
| IR07-G09 no provider/API/MCP activated | No activation. | Pass. | Stop. |
| IR07-G10 source tracking remains blocked | IR-02 preserved. | Pass. | Stop. |
| IR07-G11 IR-08 next scope declared | Next readiness only. | Ready after instruction. | Do not start. |

## 28. Residual Risk Register
| risk_id | residual risk | source | severity | mitigation | route | blocks implementation? |
| --- | --- | --- | --- | --- | --- | --- |
| R-01 | Final substrate undecided. | CSS/IR-07 | High | Decision gate evidence. | Later governance. | Yes |
| R-02 | Graph authority confusion. | CSS-00/02 | High | Candidate-only wording. | CSS review. | Yes |
| R-03 | Graphify naming/authority confusion. | CSS-02 | High | Normalization. | Migration/CSS. | Yes |
| R-04 | Evidence binding model not implemented. | V/W | High | IR-08. | IR-08. | Yes |
| R-05 | Schema/versioning model absent. | CSS-01 | High | Schema governance. | I00 later. | Yes |
| R-06 | Security enforcement absent. | S-series | High | IR-08. | IR-08. | Yes |
| R-07 | Validation registry absent. | V-series | High | IR-08. | IR-08. | Yes |
| R-08 | Substrate tool dependencies unreviewed. | IR-04 | High | Dependency gates. | Future. | Yes |
| R-09 | Provider-backed substrate blocked. | IR-06 | High | Provider gates. | Future. | Yes |
| R-10 | Source tracking blocked. | IR-02 | High | Tracking gate. | IR-A/I00. | Yes |
| R-11 | Existing `3_platform` contents unknown. | IR-01/02 | High | Classification. | Future. | Yes |
| R-12 | Context sensitivity model not implemented. | W/S | High | IR-08. | IR-08. | Yes |
| R-13 | Migration path absent. | M/CSS | Medium | Migration plan. | Later. | Yes |
| R-14 | Rollback/removal model absent. | CSS-01 | Medium | Gate evidence. | Later. | Yes |
| R-15 | Product needs may pressure premature substrate. | P-series | Medium | Criteria-only use. | Product governance. | Yes |

## 29. Blocker Register
| blocker | stop behavior | required future action | blocks IR-07? | blocks implementation? |
| --- | --- | --- | --- | --- |
| missing IR-06 | Stop. | Complete IR-06. | Yes | Yes |
| missing CSS-series | Stop. | Restore CSS evidence. | Yes | Yes |
| select final substrate now without evidence | Stop. | Gather gate evidence. | No | Yes |
| implement prototype | Stop. | Prototype gate. | No | Yes |
| adopt graph/vector/database dependency | Stop. | IR-04 gate. | No | Yes |
| activate provider/API/MCP | Stop. | IR-06 gate. | No | Yes |
| inspect Graphify raw source | Stop. | External review scope. | No | Yes |
| inspect `3_platform` contents | Stop. | Classification scope. | No | Yes |
| source tracking implied | Stop. | IR-02 future gate. | No | Yes |
| product activation implied | Stop. | Product governance. | No | Yes |
| validation/security enforcement implied | Stop. | IR-08. | No | Yes |
| Git action implied | Stop. | Human Git approval. | No | Yes |
| IR-08 scope pressure detected | Stop. | Finish/report IR-07. | No | No |
| I-00 scope pressure detected | Stop. | Later explicit ticket. | No | Yes |

## 30. Incident Handling
Incidents include: final substrate selected without gate evidence; graph adopted as truth by wording; Graphify treated as authority; prototype created; graph/vector/database/ontology dependency adopted; embeddings or index created; provider/API/MCP activated; raw external source inspected/adopted; `3_platform` contents inspected; source tracking approved; validation/security enforcement implemented; Git staging/commit/push attempted; IR-08 or I-00 started.

Response: STOP, report safe metadata only, do not continue adjacent work, and require human/security/governance decision.

## 31. IR-07 Invariants
| ID | Invariant |
| --- | --- |
| IR07-001 | Cognitive Semantic System is the accepted name. |
| IR07-002 | Substrate decision gate is not substrate implementation. |
| IR07-003 | Final substrate is not selected without sufficient evidence. |
| IR07-004 | Graph remains a candidate only. |
| IR07-005 | Graphify is evidence only, not authority. |
| IR07-006 | No graph/vector/database/ontology/event/context runtime is created. |
| IR07-007 | No prototype is created. |
| IR07-008 | Dependencies remain unadopted. |
| IR07-009 | Provider/API/MCP activation remains blocked. |
| IR07-010 | Source tracking is not approved. |
| IR07-011 | Product source remains local-only. |
| IR07-012 | Product Git posture is not changed. |
| IR07-013 | Validation evaluates; governance decides. |
| IR07-014 | IR-07 stops before IR-08. |

## 32. Anti-patterns
Anti-patterns: decision gate as implementation; candidate as selected substrate; graph as truth by default; vector similarity as semantic truth; ontology inference as governance approval; Graphify as accepted name; `Graphify owns truth`; provider-backed store by convenience; product visualization need as graph requirement; EnergyPlus solver need as CSS substrate requirement; external source as authority; prototype by curiosity; starting IR-08 inside IR-07; starting I-00 inside IR-07; `git add .`.

## 33. Readiness For IR-08
IR-08 - Validation / Security Enforcement Readiness is ready after explicit instruction if IR-07 substrate decision gate exists; Cognitive Semantic System name remains accepted; final substrate is deferred or selected only with sufficient evidence; no prototype was created; no substrate dependencies were adopted; no provider/API/MCP activation occurred; source tracking remains not approved; `3_platform` contents remain uninspected and unapproved; and no product activation, publication, Git mutation, or implementation is implied.

IR-07 does not create IR-08.

## 34. Final Verdict
IR-07 assesses whether AGENT PLATFORM / Siamese has enough evidence to select a Cognitive Semantic System substrate before implementation. Cognitive Semantic System is the accepted name. Final substrate was not selected; substrate decision deferred because existing evidence defines criteria and candidate posture but lacks gate evidence, implementation readiness, validation/security enforcement readiness, dependency posture, source tracking posture, and rollback evidence.

Graph remains a candidate only. Graphify is evidence only, not authority. No graph/vector/database/ontology/runtime/prototype artifacts were created. No dependencies were adopted. No providers/API/MCP were activated. Source tracking was not approved. Existing `3_platform` contents were not inspected or approved. Product source remains local-only.

Blocked items remain: final substrate selection, prototype/runtime, schemas, graph/vector/database/ontology/event/context stores, embeddings/indexes, dependencies, provider/API/MCP activation, validation/security enforcement, source tracking, product activation, and implementation. IR-08 is ready after explicit instruction only.
