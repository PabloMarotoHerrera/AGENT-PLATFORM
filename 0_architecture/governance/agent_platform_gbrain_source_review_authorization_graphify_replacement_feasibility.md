# GBrain Source Review Authorization Graphify Replacement Feasibility

## Document Header

| Field | Value |
| --- | --- |
| Title | GBrain Source Review Authorization Graphify Replacement Feasibility |
| Ticket | P12.0A |
| Status | Source-review-only partial replacement feasible; runtime adoption and Graphify retry still gated |
| Date | 2026-07-09 |
| Scope | Read-only feasibility review of `4_external/sources/gbrain-master` to determine whether GBrain can replace Graphify's semantic markdown/code search layer before paying for Claude Code or continuing Graphify runtime work. |
| Authority | Feasibility review only; not GBrain execution, Graphify execution, provider activation, provider login, credential inspection, package installation, dependency resolution, embedding generation, database creation, graph/vector store creation, generated output import, frontend reuse, runtime integration, authority promotion, source-of-truth promotion, Git mutation, or Cognitive Semantic System substrate selection. |
| Target file | `0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md` |

Final declaration: `gbrain_partially_replaces_graphify_semantic_layer`.

Supporting markers:

```text
gbrain_local_provider_feasible_candidate
graphify_visualization_only_candidate
graphify_frontend_reuse_requires_separate_gate
graphify_runtime_retry_still_blocked
```

## Summary

P12.0A reviewed GBrain source and documentation only. GBrain is a credible candidate to replace the portion of Graphify we were considering paying an LLM provider for: semantic markdown/code retrieval, hybrid search, typed graph traversal, and code-intelligence lookup.

GBrain does not replace Graphify's graph-report and visualization output layer. Graphify still owns the `GRAPH_REPORT.md`, `graph.json`, `graph.html`, `graph.svg`, Obsidian/wiki, call-flow HTML, and browser-facing project-map export posture.

The decision is therefore partial, not wholesale:

```yaml
P12_0A_Decision:
  gbrain_can_replace_graphify_semantic_markdown_code_search_layer: "partial_candidate"
  gbrain_can_replace_graphify_visual_report_export_layer: false
  graphify_runtime_retry_required_before_this_decision: false
  claude_code_purchase_required_now_for_graphify: false
  graphify_visualization_only_candidate: true
  graphify_frontend_reuse_requires_separate_gate: true
  gbrain_runtime_execution_authorized_now: false
  graphify_runtime_execution_authorized_now: false
  cognitive_semantic_system_substrate_selected: false
  final_marker: "gbrain_partially_replaces_graphify_semantic_layer"
```

## Source Discovery Result

Exact-path candidate checks performed before this review found the expected GBrain root only as:

```text
4_external/sources/gbrain-master
```

Negative exact-path candidates were:

```text
4_external/sources/gbrain
4_external/sources/GBrain
4_external/sources/gbrain-main
4_external/sources/GBrain-main
4_external/sources/gbrain-main-main
```

Filtered discovery returned:

```text
gbrain-master
```

## Prior Graphify State

P10.5 executed exactly once:

```text
graphify . --no-viz
```

The execution stopped safely before semantic extraction because no LLM API key was available.

P10.5 final marker:

```text
graphify_controlled_rerun_execution_recorded_safe_failure_missing_llm_api_key
```

P10.5 observed scan counts:

```yaml
code_files: 46
docs: 227
papers: 0
images: 0
```

P10.5A recorded:

```text
OPENAI_API_KEY_PRESENT=false
```

P10.5A-ALT recorded Graphify provider feasibility markers:

```text
graphify_claude_code_provider_feasible
```

P10.5B remains blocked because P10.3A is OpenAI-only and does not authorize `--backend` or equivalent provider-selection flags.

## Files Inspected

Governance files inspected:

- `0_architecture/governance/agent_platform_graphify_controlled_rerun_execution_record.md`
- `0_architecture/governance/agent_platform_graphify_openai_provider_availability_credential_boundary_resolution.md`
- `0_architecture/governance/agent_platform_graphify_local_free_provider_feasibility_review.md`
- `.graphifyignore`

GBrain source and documentation inspected:

- `4_external/sources/gbrain-master/package.json`
- `4_external/sources/gbrain-master/README.md`
- `4_external/sources/gbrain-master/docs/architecture/RETRIEVAL.md`
- `4_external/sources/gbrain-master/docs/architecture/system-of-record.md`
- `4_external/sources/gbrain-master/docs/architecture/brains-and-sources.md`
- `4_external/sources/gbrain-master/docs/integrations/embedding-providers.md`
- `4_external/sources/gbrain-master/src/core/import-file.ts`
- `4_external/sources/gbrain-master/src/core/chunkers/code.ts`
- `4_external/sources/gbrain-master/src/core/operations.ts`
- `4_external/sources/gbrain-master/src/commands/extract.ts`
- `4_external/sources/gbrain-master/src/commands/graph-query.ts`
- `4_external/sources/gbrain-master/src/commands/export.ts`
- `4_external/sources/gbrain-master/admin/src/pages/Dashboard.tsx`
- `4_external/sources/gbrain-master/admin/DESIGN.md`

Graphify documentation inspected for comparison only:

- `4_external/sources/graphify/README.md`
- `4_external/sources/graphify/ARCHITECTURE.md`

Additional grep-only README hits surfaced inside the allowed GBrain and Graphify source roots:

- `4_external/sources/gbrain-master/evals/functional-area-resolver/README.md`
- `4_external/sources/gbrain-master/recipes/agent-voice/tests/e2e/audio-fixtures/README.md`
- `4_external/sources/gbrain-master/docs/tutorials/README.md`
- `4_external/sources/gbrain-master/docs/integrations/README.md`
- `4_external/sources/graphify/worked/rsl-siege-manager/README.md`
- `4_external/sources/graphify/worked/mixed-corpus/README.md`

These grep-only hits were not used as primary evidence, and no generated artifacts referenced by worked examples were opened.

No generated Graphify output, credential files, provider configuration, product/Siamese source, unrelated external source, package manager state, runtime database, vector store, graph store, or generated artifacts were inspected.

## Files Created

- `0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md`

## Files Modified

- None beyond creating and correcting this P12.0A feasibility review document.

## Commands Run

No GBrain, Graphify, provider, package-manager, test, build, Python, Node, npm, Claude, Ollama, or CI command was run.

Allowed shell command run after document creation:

```text
git status --short
```

Dedicated non-shell marker/status checks were also performed with repository file tools:

```text
Glob: target document path exists
Grep: final and support markers present
```

No forbidden command was run.

## Verification Result

Target document present: true.

Required markers present after correction:

```text
gbrain_partially_replaces_graphify_semantic_layer
gbrain_local_provider_feasible_candidate
graphify_visualization_only_candidate
graphify_frontend_reuse_requires_separate_gate
graphify_runtime_retry_still_blocked
```

Observed `git status --short` after creation:

```text
?? 0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

The implementation file was already observed as untracked before this P12.0A document was created and was not modified by this review.

## GBrain Capability Evidence

`package.json` identifies the package as `gbrain` and describes it as a `Postgres-native personal knowledge brain with hybrid RAG search`. It exposes a `gbrain` binary and exports core modules for operations, import, embedding, config, and hybrid search.

`README.md` describes GBrain as a brain layer for agents with synthesis, graph traversal, gap analysis, hybrid search, and a self-wiring knowledge graph. It explicitly distinguishes raw retrieval from synthesized answers with citations and gap analysis.

`docs/architecture/RETRIEVAL.md` defines the retrieval stack as vector search using HNSW on pgvector, BM25 keyword search, reciprocal-rank fusion, and knowledge graph traversal. The same document says `search` is the cheap-hybrid op and `query` is the full-control variant.

`docs/architecture/RETRIEVAL.md` also documents the full `query` path as intent classification, optional expansion, hybrid vector/keyword/relational retrieval, source-aware re-rank, RRF fusion, graph augment, reranking, token-budget enforcement, deduplication, and final results.

`docs/architecture/system-of-record.md` states that the markdown/frontmatter repo is the system of record and Postgres/PGLite is a derived cache. It states that pages, chunks, embeddings, links, timeline, facts, and tags are derived from or reconciled with markdown.

`docs/architecture/brains-and-sources.md` defines a brain as a database and a source as a named content repo inside a brain. This matters because GBrain is a multi-source retrieval substrate, not a one-shot project-map export.

`docs/integrations/embedding-providers.md` lists 16 embedding-provider recipes and explicitly includes local/free options: `ollama`, `llama-server`, and `litellm` proxy. It also states that explicit `--embedding-model` and `--no-embedding` override environment auto-detection.

`src/core/import-file.ts` parses markdown, chunks content, extracts fenced code blocks from markdown into first-class code chunks, embeds chunks unless `opts.noEmbed` is set, writes pages/tags/chunks transactionally, and extracts code references for doc-to-implementation links.

`src/core/import-file.ts` routes code files through `importCodeFile`. That code path uses tree-sitter chunking, persists language/symbol/line metadata, embeds only new or changed chunks when embedding is enabled, and persists best-effort code call-site edges.

`src/core/chunkers/code.ts` identifies itself as a tree-sitter-based semantic code splitter. It extracts semantic units such as functions, classes, types, and exports as chunks and supports many languages through embedded grammar WASMs.

`src/core/operations.ts` exposes read operations relevant to this replacement question: `search`, `query`, `get_links`, `get_backlinks`, `traverse_graph`, `code_callers`, `code_callees`, `code_def`, and `code_refs`.

`src/commands/graph-query.ts` provides relationship traversal with type and direction filters over `traversePaths` and maps to `traverse_graph` for MCP-style operation use.

`src/commands/extract.ts` states that link and timeline extraction are deterministic regex-based extraction with no LLM cost at the extraction stage. This is materially different from Graphify's non-code semantic extraction path.

`src/commands/export.ts` exports brain pages back to markdown files. It is a markdown export/restore tool, not a Graphify-style project-map visualization export.

`admin/src/pages/Dashboard.tsx` and `admin/DESIGN.md` show an ops/admin dashboard for connected agents, requests, scopes, tokens, and live activity. They do not show an equivalent of Graphify's browser graph map.

## Graphify Capability Evidence

`4_external/sources/graphify/ARCHITECTURE.md` defines the Graphify pipeline:

```text
detect() -> extract() -> build_graph() -> cluster() -> analyze() -> report() -> export()
```

The same architecture document maps `report.py` to `GRAPH_REPORT.md`, `export.py` to Obsidian vault, `graph.json`, `graph.html`, and `graph.svg`, and `callflow_html.py` to Mermaid architecture/call-flow HTML.

`4_external/sources/graphify/README.md` says `/graphify .` produces `graph.html`, `GRAPH_REPORT.md`, and `graph.json` under `graphify-out/`.

Graphify's report layer includes god nodes, surprising connections, why/rationale nodes, suggested questions, and confidence tags.

Graphify's file handling matrix includes code, docs, Office, Google Workspace, PDFs, images, video/audio, YouTube/URLs, manifests, MCP config, Terraform/HCL, and more.

Graphify processes code locally with tree-sitter and says code-only corpora require no API key. It also says docs, PDFs, and images require semantic extraction through the IDE model/API path or a headless backend.

Graphify documents headless provider paths for Gemini, Kimi, Claude API, OpenAI, DeepSeek, Ollama, Bedrock, Claude Code CLI, Azure, and OpenAI-compatible servers.

## Capability Comparison Matrix

| Capability | GBrain source-review result | Graphify source-review result | P12.0A assessment |
| --- | --- | --- | --- |
| Semantic markdown retrieval | Markdown import, chunking, embeddings, hybrid search, deterministic link/timeline extraction, source scoping | Docs are graph nodes/edges; non-code semantic extraction requires an assistant/model/backend | GBrain is a viable replacement candidate for search/retrieval, not for generated project reports |
| Code search and code intelligence | Tree-sitter semantic chunking, code metadata, `code_def`, `code_refs`, `code_callers`, `code_callees`, code edge persistence | Tree-sitter AST extraction and call/import/use edges into a graph | Strong overlap; GBrain better matches ongoing query/retrieval, Graphify better matches static project-map export |
| Hybrid retrieval | Vector + BM25 + RRF + graph traversal + reranker/intent layers | Query over generated `graph.json` and graph path/explain commands | GBrain is stronger as a retrieval substrate; Graphify is stronger as graph artifact output |
| Typed graph traversal | `traverse_graph`, `graph-query`, typed links, direction/depth filters, source scoping | NetworkX graph build, clustering, path/query/explain over generated graph | Overlap exists, but models differ: GBrain is live brain DB/cache; Graphify is generated evidence graph |
| Local/free provider path | Ollama and llama-server embedding options require no key; LiteLLM proxy supported; `--no-embedding` exists | Ollama, Claude Code CLI, Bedrock, and compatible servers documented; P10.3B still required for retry | GBrain is a credible no-new-paid-API candidate, but provider/runtime validation is not performed here |
| Generated report | No equivalent observed to `GRAPH_REPORT.md` project analysis report | First-class `GRAPH_REPORT.md` report with god nodes, surprises, questions, confidence labels | Graphify remains superior for report generation |
| Visualization | Admin dashboard is an operator dashboard, not a graph map | `graph.html`, `graph.svg`, GraphML, Neo4j/FalkorDB exports, Obsidian/wiki/callflow outputs | GBrain does not replace Graphify visualization/export layer |
| Source-of-truth posture | Markdown/frontmatter repo is source of record; DB is derived cache | Generated `graphify-out/` is intended to be used and even committed in Graphify team workflow | For Agent Platform, both remain evidence/derived only unless future governance changes that explicitly |
| Runtime footprint | Requires GBrain init/config, PGLite/Postgres, provider selection, embeddings or no-embedding mode | Requires Graphify CLI/runtime and provider/backend for non-code docs | Neither runtime path is authorized by P12.0A |

## Replacement Decision

GBrain partially replaces the Graphify layer that motivated the paid-provider question.

GBrain can replace, at feasibility level only:

- Semantic markdown retrieval over governed markdown.
- Code-aware search and symbol lookup.
- Hybrid keyword/vector search, if a future gate authorizes embeddings or local embedding configuration.
- Typed link traversal and relationship lookup.
- Ongoing agent retrieval against a derived cache.

GBrain does not replace:

- Graphify's `GRAPH_REPORT.md` architecture report.
- Graphify's browser graph visualization.
- Graphify's graph artifact exports.
- Graphify's Obsidian/wiki/callflow export posture.
- Graphify's project-map UX without separate frontend reuse or visualization work.

Graphify should therefore be treated as a `visualization/report/export candidate`, not as the necessary semantic search substrate, until a future gate says otherwise.

## Cost And Provider Decision

No paid Claude Code subscription or paid OpenAI API spend is justified by P12.0A solely to continue Graphify semantic extraction.

Reason:

- GBrain source shows a credible semantic retrieval path with local/free embedding candidates.
- Graphify already has documented no-paid-API candidates, but P10.3B is still required before any `--backend` retry.
- The missing OpenAI key safe stop remains unresolved.
- Runtime provider quality has not been validated for either tool.

The next cost-safe posture is to evaluate GBrain runtime feasibility under a separate gate before purchasing or activating Claude Code only for Graphify.

## Authority Boundary

Graphify remains evidence map only.

GBrain, if later adopted, must also remain derived/evidence infrastructure only unless a separate governance record explicitly grants more authority.

Neither Graphify nor GBrain is approved here as:

- Authority.
- Source of truth for Agent Platform decisions.
- Approval engine.
- Runtime control plane.
- Cognitive Semantic System substrate.
- Product/Siamese source interpreter.
- Credential manager.
- Provider activation mechanism.

GBrain's own documentation says its markdown/frontmatter repo is its system of record and its database is a derived cache. That contract is compatible with Agent Platform governance only if future adoption keeps GBrain output/cache derived and non-authoritative.

## Runtime Boundary

P12.0A did not run:

- `gbrain`
- `graphify`
- `/graphify`
- `claude`
- `ollama`
- `python`
- `node`
- `npm`
- package managers
- tests
- builds
- CI

P12.0A did not perform:

- GBrain init.
- Graphify retry.
- Provider login.
- Provider availability test.
- Credential inspection.
- `.env` inspection.
- Provider config inspection.
- Embedding generation.
- Vector DB creation.
- Graph DB creation.
- Runtime adapter creation.
- Memory store creation.
- Generated output import.
- Generated output tracking approval.
- Git staging, commit, amend, push, or reset.

## Stop Conditions Preserved

This review stops before any conclusion that would require:

- Executing GBrain or Graphify.
- Installing dependencies.
- Reading credentials or `.env`.
- Reading provider configs or token stores.
- Generating embeddings.
- Creating PGLite/Postgres/vector/graph stores.
- Inspecting `graphify-out/**`.
- Inspecting product/Siamese source.
- Copying or reusing Graphify frontend code.
- Mutating Git.

## Future Gates

Recommended next governance gates, if the user wants to proceed:

1. P12.0B: GBrain runtime feasibility plan with explicit no-paid-provider posture, explicit `--no-embedding` versus local embedding decision, and credential-boundary rules.
2. P12.0C: GBrain controlled dry-run or init/import plan only if P12.0B authorizes exact commands and runtime side effects.
3. P10.3B: Graphify backend amendment only if continuing Graphify retry with `claude-cli`, `ollama`, Gemini, Bedrock, or another non-OpenAI backend.
4. Separate Graphify frontend reuse gate before copying, adapting, or depending on Graphify visualization/UI/export code.
5. Separate Cognitive Semantic System substrate gate before selecting any persistent semantic substrate.

## Final Decision Record

```yaml
GBrainReplacementFeasibility:
  ticket: P12.0A
  date: "2026-07-09"
  source_root_reviewed: "4_external/sources/gbrain-master"
  graphify_docs_reviewed_for_comparison: true
  generated_graphify_output_inspected: false
  credentials_inspected: false
  provider_config_inspected: false
  product_source_inspected: false
  gbrain_executed: false
  graphify_executed: false
  package_install_performed: false
  embedding_generation_performed: false
  database_created: false
  vector_store_created: false
  graph_store_created: false
  git_mutation_performed: false
  semantic_layer_replacement: "partial_candidate"
  replacement_limit: "does_not_replace_graphify_report_visualization_export_layer"
  graphify_runtime_retry_allowed_now: false
  gbrain_runtime_allowed_now: false
  claude_code_purchase_required_now: false
  result_marker: "gbrain_partially_replaces_graphify_semantic_layer"
```

Final marker:

```text
gbrain_partially_replaces_graphify_semantic_layer
```
