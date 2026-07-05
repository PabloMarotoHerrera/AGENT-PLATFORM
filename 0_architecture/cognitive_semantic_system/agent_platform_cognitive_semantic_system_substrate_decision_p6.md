# Cognitive Semantic System Substrate Decision (P6.6)

## 1. Record Status

- Record: Cognitive Semantic System Substrate Decision
- Phase: P6.6
- Status: decision deferred
- Date: 2026-07-05
- Authority level: documentation-only governance record

## 2. Decision Statement

The decision is `cognitive_semantic_system_substrate_deferred`.

No runtime substrate is required yet. The AGENT PLATFORM Cognitive Semantic System remains substrate-neutral while the P6 operational contracts continue to rely on canonical markdown records and metadata references.

## 3. Non-Activation Boundary

This record does not activate a runtime, storage layer, agent loop, scheduler, semantic memory, graph engine, vector index, ontology runtime, ingestion pipeline, event stream, telemetry path, provider integration, MCP server, Cadence worker, or product feature.

## 4. Scope of This Record

This record only defines the substrate decision posture for the Cognitive Semantic System after P6.1 through P6.5.

It does not select, install, configure, import, execute, validate, benchmark, publish, or operationalize any substrate.

## 5. Inputs Considered

- P6.1 agent capability registry operational contract.
- P6.2 agent-to-agent communication protocol.
- P6.3 shared context evidence bus operational contract.
- P6.4 human approval and review loop operational contract.
- P6.5 runtime monitoring and incident handling operational contract.
- EXT.GB-01 GBrain external source intake / read-only capability review.
- P5.R minimal active agent platform audit.
- P2.KR knowledge retrieval architecture reconciliation closure.
- P1.5 Cognitive Semantic System prototype hardening record.
- Cognitive Semantic System naming and substrate ADR.
- Cognitive Semantic System decision audit.
- Graphify repository map summary.
- Shared metadata vocabulary alignment baseline.
- Audit retention and rollback baseline.

## 6. Inputs Not Available

No GBrain source contents, implementation files, dependency manifests, provider/auth configuration, MCP configuration, Cadence configuration, token stores, credentials, or external source contents were inspected for this decision.

EXT.GB-01 is present and reviewed as a read-only external source intake / capability review.

EXT.GB-01 confirms GBrain as a strong external architecture candidate for future Cognitive Semantic System memory/substrate review, while keeping GBrain not adopted, not executed, not imported, not configured, not dependency-approved, not provider/auth-approved, not MCP-active, not Cadence-active, and not substrate.

EXT.GB-01 also records an accepted limitation: `external/sources/gbrain-master` was absent during review, so no local GBrain documentation, source, dependency, persistence, MCP, Cadence, eval, or license claims were validated.

Therefore `pending_EXT.GB_01_gbrain_external_source_review` is closed. The replacement review posture is `EXT.GB_01_present_limited_review`, and `future_EXT.GB_HARD_reviews_required_before_selection` remains required before any GBrain selection, adoption, dependency approval, provider/auth approval, MCP activation, Cadence activation, persistence, or substrate decision.

## 7. Current P6 Contract Posture

The P6.1 through P6.5 contracts are metadata-only governance records. They define registries, message envelopes, evidence/context references, approval references, monitoring references, incident references, and Cadence boundary language without enabling runtime behavior.

P6.5 is present and reviewed as the metadata-only Runtime Monitoring / Incident Handling operational contract. P6.5 confirms that monitoring model is not monitoring runtime, incident route is not incident automation, and Cadence / always-on behavior remains blocked.

Those contracts do not require a semantic substrate to be selected in P6.6.

## 8. Candidate Set

- `markdown_canonical_docs_plus_metadata_refs`: current baseline candidate.
- `gbrain_style_markdown_first_self_wiring_graph_memory`: strongest current external candidate class by posture, reviewed through `EXT.GB_01_present_limited_review` and still requiring future EXT.GB-HARD reviews before selection.
- `graphify_generated_evidence_only`: generated repository-map evidence, not a substrate candidate for adoption.
- `graph_db_runtime_substrate`: deferred and blocked.
- `vector_db_runtime_substrate`: deferred and blocked.
- `hybrid_graph_vector_runtime_substrate`: deferred and blocked.
- `ontology_runtime_substrate`: deferred and blocked.

## 9. Candidate Evaluation Summary

The current baseline is sufficient for P6 governance because the active platform state is still an AL-1 metadata skeleton.

The GBrain-style candidate is directionally aligned with markdown-first, self-wiring graph memory ideas and is reviewed through EXT.GB-01 as present but limited. It is not approved because EXT.GB-01 did not validate local GBrain documentation, source, dependency, persistence, MCP, Cadence, eval, or license claims, and future EXT.GB-HARD reviews remain required before any selection or adoption.

Runtime graph, vector, hybrid, ontology, database, ingestion, and indexing substrates are premature because the platform has not crossed the documented activation gates.

## 10. GBrain Candidate Posture

`gbrain_style_markdown_first_self_wiring_graph_memory` is recorded only as the strongest current external candidate class.

It is reviewed through EXT.GB-01 as a read-only external source intake with limitations.

It is not adopted, imported, executed, configured, dependency-approved, provider/auth-approved, MCP-active, Cadence-active, or selected as the Cognitive Semantic System substrate.

## 11. Graphify Boundary

Graphify remains generated supporting evidence only.

Graphify output can inform repository understanding, but it is not source authority, not canonical truth, not an operational database, not semantic memory, not a runtime substrate, and not a replacement for explicit architecture records.

## 12. Graphify And GBrain Relationship

Graphify and GBrain are complementary.

Graphify is generated evidence about this repository. GBrain-style memory is an external candidate class for a possible future markdown-first semantic memory posture. They are not equivalent and neither is selected as the current substrate.

## 13. Current Baseline Candidate

`markdown_canonical_docs_plus_metadata_refs` remains the working baseline.

Canonical markdown records remain the durable architecture source. Metadata references remain the allowed linkage pattern between governance records until a later decision approves a runtime substrate.

## 14. Runtime Substrate Requirement

No runtime substrate is required yet.

The P6 operational contracts can continue without dispatch, persistence, indexing, embeddings, graph traversal, model calls, live connectors, provider auth, or autonomous execution.

## 15. Storage Boundary

The current decision authorizes no database, no storage service, no object store integration, no cache, no durable runtime state, no product-bound semantic storage, and no generated-output tracking expansion.

## 16. Persistence Boundary

The current decision authorizes no persistence.

Canonical markdown files remain records, but this decision does not introduce runtime persistence, state hydration, retention automation, rollback automation, audit database storage, or semantic-memory writes.

## 17. Vector And Embedding Boundary

The current decision authorizes no vector DB.

It also authorizes no embeddings, embedding provider integration, vector indexing, nearest-neighbor search service, semantic cache, or retrieval augmentation runtime.

## 18. Graph Database Boundary

The current decision authorizes no graph DB.

It also authorizes no graph database schema, graph database dependency, graph query runtime, graph ingestion, graph synchronization, live graph traversal, or graph-backed agent memory.

## 19. Ontology Runtime Boundary

The current decision authorizes no ontology runtime.

Shared metadata vocabulary records may continue as governance documents, but they are not promoted to a live ontology service, reasoner, validator, or runtime policy engine.

## 20. Cadence / Always-On Boundary

Cadence and always-on behavior remain blocked.

This decision does not start workers, schedules, workflows, autonomous loops, monitoring daemons, incident automation, wake-up paths, or long-running semantic maintenance processes.

EXT.GB-01 records GBrain as a cadence_reference_candidate only. Because local GBrain docs/source were unavailable, any future dream-cycle, always-on, background refresh, memory consolidation, or Cadence claim requires `gbrain_cadence_dream_cycle_review_required`, human approval, and a future exact gate before use.

## 21. MCP Provider And Auth Boundary

This decision authorizes no MCP activation, provider authorization, API call, external connector, credential lookup, browser-auth usage, token-store access, or local credential-store access.

Any future substrate that requires provider auth, MCP access, or external execution requires an explicit later approval record.

## 22. Source And Generated Evidence Boundary

This decision does not expand source tracking and does not inspect external source contents.

Generated evidence remains supporting evidence. Canonical architecture records remain the only authority for current platform decisions.

## 23. Product Boundary

Siamese remains a product vision and is not activated by this decision.

This decision does not create product-bound features, product-bound memory, product ingestion, product retrieval, product telemetry, or product persistence.

## 24. Dependency And Import Boundary

This decision approves no dependency, package, import, plugin, framework, runtime service, repository import, submodule, external source checkout, or local source loading.

EXT.GB-01 is present but limited. GBrain-style work cannot proceed beyond candidate-class notation until future EXT.GB-HARD documentation/source/dependency/storage/MCP/Cadence/eval/license reviews are complete and an exact future gate approves a narrower scope.

## 25. Risks Accepted

- Deferring the substrate may slow future semantic-memory implementation.
- Keeping markdown plus metadata references may require manual governance discipline.
- EXT.GB-01 reviewed GBrain as a strong candidate only with accepted limitations because local GBrain documentation/source was unavailable.
- Not selecting graph or vector infrastructure preserves reversibility but postpones performance and retrieval tradeoff analysis.

## 26. Deferred Work And Blockers

- `EXT.GB_01_present_limited_review` closes the prior EXT.GB-01 absence blocker for P6.6 alignment.
- `future_EXT.GB_HARD_reviews_required_before_selection` remains required before any GBrain adoption, dependency approval, provider/auth approval, MCP activation, Cadence activation, persistence, substrate selection, or implementation planning.
- Required future blockers: `gbrain_documentation_capability_map_required`, `gbrain_source_dependency_boundary_review_required`, `gbrain_persistence_storage_review_required`, `gbrain_mcp_provider_auth_review_required`, `gbrain_cadence_dream_cycle_review_required`, `gbrain_brainbench_eval_review_required`, `gbrain_license_provenance_supply_chain_review_required`, `human_approval_required`, and `future_exact_substrate_gate_required`.
- Keep graph DB, vector DB, hybrid graph/vector storage, ontology runtime, persistence, ingestion, indexing, embeddings, and product-bound semantic storage blocked until a later explicit decision.
- Keep AGENT PLATFORM at AL-1 metadata skeleton until activation gates are explicitly satisfied.

## 27. Decision Outputs

- Primary output: `cognitive_semantic_system_substrate_deferred`.
- Current baseline: `markdown_canonical_docs_plus_metadata_refs`.
- Strongest current external candidate class: `gbrain_style_markdown_first_self_wiring_graph_memory`.
- GBrain external review posture: `EXT.GB_01_present_limited_review`.
- Generated evidence posture: `graphify_generated_evidence_only`.
- Required future blocker: `future_EXT.GB_HARD_reviews_required_before_selection`.

## 28. Closure

P6.6 closes with no substrate selected and no runtime authorized.

P6.6-ALIGN-01 corrected P6.6 so EXT.GB-01 is consumed as present but limited. `pending_EXT.GB_01_gbrain_external_source_review` is no longer an active blocker.

GBrain remains the strongest current external candidate class, but is not adopted, not executed, not dependency-approved, not provider/auth-approved, not MCP-active, not Cadence-active, and not substrate.

The Cognitive Semantic System remains documentation-led, metadata-only, and substrate-neutral until a future governance record explicitly changes that posture.
