# GBrain Adoption / Graphify Semantic Replacement Decision

## Summary

Ticket: P12.5

Status: Accepted adoption decision / semantic replacement boundary / no-runtime

Result marker: `gbrain_adoption_graphify_semantic_replacement_decision_ready`

Decision outcome: Outcome A - Adopt GBrain as semantic/retrieval replacement for Graphify.

Decision markers:

- `gbrain_adopted_as_local_semantic_retrieval_candidate`
- `gbrain_not_adopted_as_authority`
- `gbrain_not_adopted_as_graph_traversal_authority`
- `graphify_semantic_replacement_confirmed`
- `graphify_visualization_reporting_role_deferred`
- `graphify_not_memory_authority`
- `gbrain_mode_b_ollama_deferred`
- `p12_7_memory_store_integration_ready_after_gbrain_adoption`

P12.5 decides only GBrain's adoption status relative to Graphify for semantic retrieval and local memory indexing. It does not decide GStack adoption, Hermes adoption, Paperclip adoption, or any runtime/provider/tool execution authority.

## Files Inspected

Inspection was limited to allowed governance marker checks and path-existence checks. No generated sandbox internals, external source contents, product/Siamese source, secrets, credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, DB internals, or generated output contents were inspected.

Marker-checked governance files:

Historical P12.0A-P12.0E and Graphify evidence conclusions are retained as decision lineage in this record.

Marker-checked governance file by final recheck:

- `0_architecture/governance/agent_platform_memory_authority_model.md`

## P12.0E-GRAPH-REVIEW Dependency Status

P12.0E-GRAPH-REVIEW conclusions are retained as historical decision lineage in this record.

Required marker confirmed:

- `gbrain_empty_graph_query_output_review_ready`

Branch-closure markers confirmed:

- `gbrain_mode_a_keyword_memory_validated`
- `gbrain_mode_a_graph_edges_not_validated`
- `gbrain_p12_0e_branch_closed`
- `gbrain_project_12_main_roadmap_resume_ready`

Decision basis:

- The empty graph-query result is not a runtime failure.
- No more P12.0E debugging is required now.
- Project 12 main roadmap may resume.

## GBrain Validated Evidence

P12.5 records the following validated Mode A evidence from the P12.0A-P12.0E branch:

- local installation successful
- dependency install successful
- sandboxed GBRAIN_HOME successful
- PGLite local init successful
- governance markdown import successful
- 119 pages imported
- 1644 chunks created
- keyword search successful
- 119 pages exported
- graph-query command executed successfully

Specific confirmed markers and evidence:

- `gbrain_direct_governance_import_rerun_success`
- `119 pages imported`
- `1644 chunks created`
- `Exported 119 pages`
- `gbrain_graph_query_exact_slug_execution_success`
- `gbrain_graph_query_empty_result`
- `No edges found`

## GBrain Limitation Classification

P12.5 records the following limitations:

- graph-query returned empty edges for selected slug
- graph traversal usefulness not validated
- semantic embeddings not validated
- Ollama Mode B not validated
- provider-free semantic embedding path not validated
- production memory store integration not designed yet
- cleanup/reindex policy not designed yet
- GStack not validated

Classification:

- The empty graph-query result does not reject GBrain for local memory/retrieval.
- The empty graph-query result blocks treating GBrain as graph traversal authority.
- Keyword retrieval and local markdown import are validated enough for semantic/retrieval candidate adoption.
- Embedding, Mode B/Ollama, graph traversal, and production integration remain future-gated.

## Graphify Evidence and Limitation Classification

P12.5 records the following Graphify posture:

- Graphify can remain a visualization/report/evidence-map candidate.
- Graphify outputs were classified as generated evidence, not authority.
- Graphify provider/API path was blocked by API key/cost boundary.
- Graphify local/free provider feasibility exists but was not selected as primary semantic path.

Confirmed Graphify evidence markers and phrases:

- `raw_generated_evidence`
- `Graphify output is not authority`
- `Graphify output is not source of truth`
- `Graphify output is not approval`
- `graphify_ollama_provider_feasible`
- `graphify_claude_code_provider_feasible`
- `OpenAI`
- `local`
- `provider`

Cost / provider posture:

- Avoid OpenAI API cost for Graphify semantic extraction.
- Avoid Claude Code dependency unless separately justified.
- Prefer local/free GBrain path for memory/retrieval.
- Do not make hosted provider availability a prerequisite for Project 12.

## Adoption Decision

Outcome A applies.

GBrain is adopted as:

- local memory/retrieval candidate
- governance markdown indexer
- context assembly support
- keyword retrieval baseline
- future optional embedding substrate
- future optional graph substrate only after additional validation

Decision markers:

- `gbrain_adopted_as_local_semantic_retrieval_candidate`
- `graphify_semantic_replacement_confirmed`
- `graphify_visualization_reporting_role_deferred`

Rationale:

- GBrain has validated local installation, local dependency setup, sandboxed local state, governance markdown import, chunking, keyword search, export, and graph-query command execution.
- Graphify semantic extraction remains entangled with provider/API/backend cost and availability considerations.
- Existing GBrain evidence is sufficient to choose GBrain as Project 12's preferred local memory/retrieval substrate candidate.
- Existing GBrain evidence is not sufficient to treat GBrain as graph traversal authority, runtime authority, or final memory authority.

Graphify semantic replacement decision:

- GBrain should replace Graphify for semantic retrieval / local memory indexing.
- GBrain should not replace Graphify for graph visualization / evidence maps.
- Graphify may remain in the architecture as a deferred visualization/report/evidence-map candidate.

## GBrain Authority Boundary

GBrain adoption is adoption of infrastructure, not adoption of authority.

GBrain is not adopted as:

- source of truth
- approval authority
- runtime execution authority
- policy authority
- graph traversal authority
- skill execution authority
- replacement for GStack
- replacement for Hermes
- replacement for Paperclip
- replacement for Graphify visualization/reporting

Authority markers:

- `gbrain_not_adopted_as_authority`
- `gbrain_not_adopted_as_graph_traversal_authority`

Canonical rule:

- Governance markdown and accepted architecture records remain the source of record.
- GBrain may index, retrieve, and support context assembly.
- GBrain must not decide, approve, execute, mutate, or override governance.

## Graphify Remaining Role

Graphify remains in the architecture only as:

- deferred visualization/report/evidence-map candidate
- possible future frontend/report reuse review candidate
- possible future evidence map visualization adapter candidate
- possible future local Ollama test candidate only if later justified

Graphify is not:

- primary semantic extraction path
- memory authority
- approval authority
- source of truth
- required for P12 memory store integration

Expected marker:

- `graphify_not_memory_authority`

Graphify visualization/reporting role:

- `graphify_visualization_reporting_role_deferred`

Graphify remains evidence-map-only unless a later exact governance gate changes that posture.

## Mode B / Ollama Boundary

P12.5 records:

- `gbrain_mode_b_ollama_deferred`

Mode B / Ollama remains deferred because:

- semantic embeddings are not validated
- Ollama Mode B is not validated
- provider-free semantic embedding path is not validated
- local model availability, quality, resource posture, and cleanup/reindex policy remain unresolved

P12.5 does not run Ollama.

P12.5 does not run embeddings.

P12.5 does not call any provider/API.

## P12.3 Relationship

`0_architecture/governance/agent_platform_memory_authority_model.md` is present by final path-only recheck.

Marker search confirms:

- `memory_authority_model_ready`
- `canonical_memory_sources_defined`
- `gbrain_memory_authority_boundary_defined`
- `graphify_evidence_map_authority_boundary_defined`
- `p12_7_memory_store_integration_ready_after_authority_model`

P12.5 conforms to P12.3.

P12.3 classifies GBrain as derived retrieval/index infrastructure, not source of truth, approval, runtime, or policy authority.

P12.3 classifies Graphify as generated evidence map/report/visualization candidate, not memory authority or approval authority.

Rule:

- P12.5 adopts GBrain as local memory/retrieval infrastructure candidate.
- P12.5 does not define final memory authority beyond P12.3.
- P12.5 preserves canonical governance and accepted source records as the source of record.
- If future conflicts appear, P12.R or a later reconciliation ticket must resolve them.

Expected rule:

- GBrain adoption is adoption of infrastructure, not adoption of authority.

## P12.7 Handoff Decision

P12.5 enables handoff to:

- P12.7 - Memory Store Integration Design

Handoff marker:

- `p12_7_memory_store_integration_ready_after_gbrain_adoption`

P12.7 should require:

- P12.3 accepted
- P12.5 accepted

P12.7 should design:

- how GBrain-derived local memory/retrieval is integrated
- what stays canonical outside GBrain
- how imported markdown pages and chunks are refreshed
- cleanup/reindex policy
- retention/rollback/incident posture
- no authority promotion

P12.5 may also inform:

- P12.11 - Retention / Rollback / Incident Hardening
- CLEAN - Knowledge Base Cleanup / Memory Operational Readiness

P12.5 does not block P12.2/P12.4/P12.6 GStack work.

## Non-Adoption / Deferred Areas

P12.5 does not adopt:

- GStack
- Hermes
- Paperclip
- Graphify visualization/reporting replacement
- GBrain graph traversal authority
- GBrain Mode B / Ollama
- semantic embeddings
- provider/API-backed semantic extraction
- production memory store integration
- cleanup/reindex policy
- Cognitive Semantic System substrate

## Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_gbrain_adoption_graphify_semantic_replacement_decision.md`

Not created / not approved:

- No GBrain execution
- No Graphify execution
- No GStack execution
- No Ollama command
- No embeddings
- No provider/API call
- No graph-query rerun
- No markdown cleanup
- No file deletion
- No archive move
- No sandbox output modification
- No DB/internal inspection
- No credential inspection
- No PATH mutation
- No Git mutation
- No git add .

## Limitations

P12.5 is based on already-recorded governance evidence and marker checks only.

P12.5 did not inspect generated sandbox internals.

P12.5 did not inspect external source content.

P12.5 did not inspect product/Siamese source.

P12.5 did not validate semantic embeddings, graph traversal usefulness, GStack, Ollama Mode B, or production memory store integration.

P12.5 does not supersede the future P12.3 Memory Authority Model.

## Recommended Next Ticket

Recommended next ticket:

- P12.7 - Memory Store Integration Design.

Because P12.3 is present by final path-only recheck and P12.5 is now created, the next Project 12 handoff is:

- P12.7 - Memory Store Integration Design

## Final Verdict

Should GBrain replace Graphify for semantic retrieval / local memory indexing? Yes. `graphify_semantic_replacement_confirmed`.

Should GBrain replace Graphify for graph visualization / evidence maps? No. `graphify_visualization_reporting_role_deferred`.

Should GBrain become authority? No. `gbrain_not_adopted_as_authority`.

Should Graphify remain in the architecture? Yes, as deferred visualization/report/evidence-map candidate only.

Which claims are validated by the P12.0A-P12.0E branch? Local install, dependency install, sandboxed GBRAIN_HOME, PGLite local init, governance import, 119 imported pages, 1644 chunks, keyword search, 119 exported pages, and graph-query command execution.

Which claims remain unvalidated? Graph edge extraction, graph traversal usefulness, semantic embeddings, Ollama Mode B, provider-free embedding path, production memory integration, cleanup/reindex policy, and GStack.

What is the next Project 12 handoff? P12.7 Memory Store Integration Design after P12.3 and P12.5 are accepted.
