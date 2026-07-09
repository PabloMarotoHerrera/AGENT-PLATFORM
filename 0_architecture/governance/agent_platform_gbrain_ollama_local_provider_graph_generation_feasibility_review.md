# GBrain Ollama Local Provider Graph Generation Feasibility Review

## Document Header

| Field | Value |
| --- | --- |
| Title | GBrain Ollama Local Provider Graph Generation Feasibility Review |
| Ticket | P12.0B |
| Status | Source-review-only feasible for future sandbox; runtime execution still gated |
| Date | 2026-07-09 |
| Scope | Determine whether GBrain can proceed toward a local/no-paid-API Ollama sandbox and whether GBrain can support evidence-bound graph data for later visualization. |
| Authority | Governance feasibility review only; not GBrain execution, Graphify execution, Ollama inference, model pull/list/show/run, provider configuration, credential inspection, package installation, dependency resolution, embedding generation, database creation, graph/vector store creation, generated output import, frontend reuse, runtime integration, authority promotion, source-of-truth promotion, Git mutation, or Cognitive Semantic System substrate selection. |
| Target file | `0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md` |

Final declaration: `gbrain_ollama_local_provider_graph_generation_feasibility_review_ready`.

Supporting markers:

```text
gbrain_ollama_provider_feasible_for_future_sandbox
gbrain_graph_generation_candidate
gbrain_graph_generation_requires_runtime_sandbox
gbrain_visualization_feed_candidate
graphify_visualization_reuse_still_separate_gate
```

## Summary

P12.0B reviewed GBrain and Graphify source/documentation only. The review did not execute GBrain, Graphify, Ollama inference, package managers, tests, builds, CI, model APIs, embedding generation, or database creation.

The source-review decision is that GBrain has enough first-party source evidence to justify a future local/no-paid-API sandbox using Ollama as a direct embedding provider candidate. GBrain also has enough first-party source evidence to be treated as a candidate graph-generation substrate for deterministic structural edges, retrieval graph traversal, code edges, and evidence-bound model-assisted relation candidates.

This is not a runtime adoption approval. The installed Ollama command was not discoverable on `PATH` from this shell, and this review intentionally did not run `ollama list`, `ollama show`, `ollama run`, `ollama pull`, `ollama serve`, or any GBrain command. Actual local model availability, embedding compatibility, GBrain init behavior, database schema, and graph/export output shape require a later sandbox gate.

```yaml
P12_0B_Decision:
  ollama_direct_provider_source_review: "feasible_candidate"
  ollama_runtime_validated: false
  ollama_model_inventory_validated: false
  gbrain_keyword_only_local_search_candidate: true
  gbrain_local_embedding_search_candidate: true
  gbrain_graph_generation_candidate: true
  gbrain_graph_export_shape_validated: false
  gbrain_visualization_feed_candidate: true
  graphify_visualization_reuse_still_separate_gate: true
  claude_code_purchase_required_now_for_graphify: false
  graphify_runtime_retry_authorized_now: false
  gbrain_runtime_execution_authorized_now: false
  cognitive_semantic_system_substrate_selected: false
  final_marker: "gbrain_ollama_local_provider_graph_generation_feasibility_review_ready"
```

## Prior Authority

P12.0A is the controlling predecessor for this review. It declared `gbrain_partially_replaces_graphify_semantic_layer` and recorded the support markers `gbrain_local_provider_feasible_candidate`, `graphify_visualization_only_candidate`, `graphify_frontend_reuse_requires_separate_gate`, and `graphify_runtime_retry_still_blocked` in `0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md:15-23`.

P12.0A concluded that GBrain is a credible candidate to replace the semantic markdown/code retrieval portion of Graphify, while Graphify still owns `GRAPH_REPORT.md`, `graph.json`, `graph.html`, `graph.svg`, Obsidian/wiki, call-flow HTML, and browser-facing project-map export posture (`0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md:26-45`).

The local `.graphifyignore` remains a hard boundary. It states that Graphify is an evidence map, not authority, source of truth, approval engine, runtime, or Cognitive Semantic System substrate (`.graphifyignore:76-83`). It also blocks sensitive, generated, external, and product scopes including `.env*`, credentials, tokens, provider configs, `4_external/sources/**`, `graphify-out/**`, and product paths (`.graphifyignore:95-117`).

## Local Metadata Checks

Only presence-only metadata checks were performed.

| Check | Observed Result | Decision Use |
| --- | --- | --- |
| `Test-Path 0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md` | `True` | P12.0A dependency exists. |
| `Test-Path 4_external/sources/gbrain-master` | `True` | GBrain source root exists for source review. |
| `Test-Path .graphifyignore` | `True` | Existing Graphify scope boundary exists. |
| `Get-Command ollama -ErrorAction SilentlyContinue` | No output | `ollama` was not discoverable on `PATH` from this shell. This does not prove Ollama is absent globally. |
| `Test-NetConnection 127.0.0.1 -Port 11434` | `TcpTestSucceeded : True` | Local port metadata is compatible with an Ollama-style listener, but not proof of Ollama models, API behavior, or inference. |
| `git status --short` before this file | `?? 0_architecture/implementation/graphify_command_candidate_confirmation.md` | Pre-existing untracked implementation file observed; not modified by this review. |

No model inventory, model inference, model pull, model show, model run, package-manager command, GBrain command, Graphify command, test, build, CI, provider API, embedding creation, vector DB creation, graph DB creation, generated output inspection, credential inspection, or Git mutation was performed.

## Provider Evidence

GBrain documents a broad provider registry with local options. Its embedding provider guide says it ships 16 embedding-provider recipes including three local options and LiteLLM as a universal escape hatch (`4_external/sources/gbrain-master/docs/integrations/embedding-providers.md:1-5`). It also says explicit flags such as `--embedding-model` and `--no-embedding` win over environment detection (`4_external/sources/gbrain-master/docs/integrations/embedding-providers.md:16-20`).

The provider table lists `ollama` with no env vars, 768 default dimensions, zero cost, and local mode; it also lists `llama-server` with no env vars, user-set dimensions, zero cost, and local mode (`4_external/sources/gbrain-master/docs/integrations/embedding-providers.md:24-36`). The note on local providers says Ollama and llama-server have no required API key and should be picked explicitly with `--embedding-model ollama:<model>` to avoid silently routing to a daemon that may not be running (`4_external/sources/gbrain-master/docs/integrations/embedding-providers.md:43`).

The Ollama recipe is direct and OpenAI-compatible. It declares `id: 'ollama'`, `name: 'Ollama (local)'`, `implementation: 'openai-compatible'`, default base URL `http://localhost:11434/v1`, no required auth env, optional `OLLAMA_BASE_URL` and `OLLAMA_API_KEY`, supported embedding models `nomic-embed-text`, `mxbai-embed-large`, and `all-minilm`, default dims 768, and zero cost per million tokens (`4_external/sources/gbrain-master/src/core/ai/recipes/ollama.ts:3-25`).

The llama-server recipe is another local OpenAI-compatible embedding option. It documents `llama-server --embeddings`, default base URL `http://localhost:8080/v1`, no required auth env, explicit user-provided model/dimension requirements, and zero cost (`4_external/sources/gbrain-master/src/core/ai/recipes/llama-server.ts:4-35`). It also has a probe path for `/v1/models`, but this review did not execute it (`4_external/sources/gbrain-master/src/core/ai/recipes/llama-server.ts:42-66`).

The LiteLLM proxy recipe is an OpenAI-compatible universal proxy, can run at `http://localhost:4000`, has no required auth env, and requires user-provided model/dimensions (`4_external/sources/gbrain-master/src/core/ai/recipes/litellm-proxy.ts:3-28`). This keeps a future escape hatch open without committing to paid hosted APIs.

The static recipe registry imports and registers `ollama`, `litellmProxy`, and `llamaServer` alongside hosted providers (`4_external/sources/gbrain-master/src/core/ai/recipes/index.ts:12-48`). This shows these local paths are first-class registry entries, not ad hoc documentation.

## No-Embedding And Keyword Evidence

GBrain has an explicit deferred-setup state. `GBrainConfig` includes `embedding_disabled?: boolean`, documented as the result of `gbrain init --no-embedding`, mutually exclusive with `embedding_model`, and intended to stop embed/import callsites until a provider is configured (`4_external/sources/gbrain-master/src/core/config.ts:47-55`).

The runtime guard throws `EmbeddingDisabledError` when `embedding_disabled` is true and prints a paste-ready provider/dimension setup hint (`4_external/sources/gbrain-master/src/core/embedding-dim-check.ts:46-76`). The headless install guide states that non-TTY init without a provider key exits 1, while `--no-embedding` is the deferred setup pattern and writes `embedding_disabled: true` (`4_external/sources/gbrain-master/docs/operations/headless-install.md:1-54`).

GBrain's search-mode guide says keyword search is fast, needs no embeddings, and is day-one ready; hybrid search is semantic plus keyword and needs embeddings; direct get also needs no embeddings (`4_external/sources/gbrain-master/docs/guides/search-modes.md:21-52`). It also states keyword search works without embeddings and hybrid search needs embeddings to have been run (`4_external/sources/gbrain-master/docs/guides/search-modes.md:63-67`).

This supports a staged local/no-paid sandbox posture: keyword retrieval can be evaluated separately from local embedding retrieval, and local embedding retrieval can be gated on the explicit Ollama model/dimension path.

## Retrieval And Graph Evidence

GBrain's retrieval architecture layers vector HNSW on pgvector, BM25 keyword search, RRF fusion, and knowledge graph traversal (`4_external/sources/gbrain-master/docs/architecture/RETRIEVAL.md:5-10`). It explicitly says hybrid without graph fails on relationship questions and that graph traversal is the layer for typed relationships (`4_external/sources/gbrain-master/docs/architecture/RETRIEVAL.md:18-20`).

The same architecture document describes zero-LLM auto-link edge extraction through markdown links, wikilinks, and typed-link blockquotes, plus deterministic heuristic link-type inference such as `attended`, `works_at`, `invested_in`, `founded`, and `advises` (`4_external/sources/gbrain-master/docs/architecture/RETRIEVAL.md:35-45`). It also describes the query pipeline as vector, keyword, relational typed-edge recall, source-aware re-rank, RRF, and graph augmentation (`4_external/sources/gbrain-master/docs/architecture/RETRIEVAL.md:90-92`, `4_external/sources/gbrain-master/docs/architecture/RETRIEVAL.md:123-132`).

The source types expose graph-ready structures. `Chunk` carries `embedding`, code language, symbol name/type, line ranges, parent symbol path, doc comments, and qualified symbol identity (`4_external/sources/gbrain-master/src/core/types.ts:563-584`). `CodeEdgeInput` and `CodeEdgeResult` describe code relationship rows with from/to symbols, edge type, metadata, source id, and resolved status (`4_external/sources/gbrain-master/src/core/types.ts:1130-1164`). `Link` includes from slug, to slug, link type, context, and provenance fields (`4_external/sources/gbrain-master/src/core/types.ts:1166-1192`). `GraphNode` and `GraphPath` provide traversal node and edge shapes with type, context, direction, and depth (`4_external/sources/gbrain-master/src/core/types.ts:1194-1214`).

The engine interface exposes `getLinks`, `getBacklinks`, `listLinkSources`, `traverseGraph`, and `traversePaths`, with source-scope protections and typed/directional edge traversal (`4_external/sources/gbrain-master/src/core/engine.ts:1150-1221`). It also exposes code graph APIs for callers, callees, and chunk-edge expansion (`4_external/sources/gbrain-master/src/core/engine.ts:2077-2106`).

The operation layer exposes read operations for `get_links`, `get_backlinks`, and `traverse_graph`; `traverse_graph` returns `GraphPath[]` when link type or direction is set and clamps remote depth (`4_external/sources/gbrain-master/src/core/operations.ts:2028-2115`). It also exposes `code_callers`, `code_callees`, `code_def`, and `code_refs` as read operations (`4_external/sources/gbrain-master/src/core/operations.ts:4098-4212`).

The `graph-query` command wraps `engine.traversePaths()`, supports `--type`, `--depth`, and `--direction in|out|both`, and maps to the `traverse_graph` operation (`4_external/sources/gbrain-master/src/commands/graph-query.ts:1-15`, `4_external/sources/gbrain-master/src/commands/graph-query.ts:130-156`). It renders `GraphPath[]` as a typed edge tree (`4_external/sources/gbrain-master/src/commands/graph-query.ts:191-214`).

The current export command writes pages back to markdown plus raw sidecar JSON, not a Graphify-style `graph.json` or browser visualization feed (`4_external/sources/gbrain-master/src/commands/export.ts:11-149`). Therefore, GBrain graph-generation capability is a candidate, but a visualization-feed/export shape remains a future data-model/runtime gate.

## Graphify Comparison Evidence

Graphify's architecture is an explicit graph-report/export pipeline: `detect() -> extract() -> build_graph() -> cluster() -> analyze() -> report() -> export()` (`4_external/sources/graphify/ARCHITECTURE.md:5-11`). Its module table maps extraction into NetworkX graph building, clustering, analysis, `GRAPH_REPORT.md`, Obsidian vault, `graph.json`, `graph.html`, `graph.svg`, and Mermaid call-flow HTML (`4_external/sources/graphify/ARCHITECTURE.md:13-24`).

Graphify's extraction schema includes nodes with `source_file` and `source_location`, edges with `source`, `target`, `relation`, and confidence labels `EXTRACTED`, `INFERRED`, and `AMBIGUOUS` (`4_external/sources/graphify/ARCHITECTURE.md:33-56`). Its README says a normal run produces `graph.html`, `GRAPH_REPORT.md`, and `graph.json` (`4_external/sources/graphify/README.md:34-40`). It also advertises call-flow HTML, wiki, Obsidian, SVG, GraphML, and Neo4j/FalkorDB exports (`4_external/sources/graphify/README.md:280-286`, `4_external/sources/graphify/README.md:516-527`). The package depends on `networkx>=3.4` (`4_external/sources/graphify/pyproject.toml:13-14`).

This comparison keeps Graphify valuable as a visualization/report/export candidate while avoiding a paid provider path for semantic extraction until a separate visualization gate justifies it.

## Decision Matrix

| Question | Decision | Evidence | Gate Remaining |
| --- | --- | --- | --- |
| Can GBrain use Ollama without a paid API key at source-review level? | Yes, feasible candidate. | Direct Ollama recipe has no required env, localhost OpenAI-compatible base URL, zero cost, and registered embedding models. | Future sandbox must confirm `ollama` command/process, model inventory, model dimensions, and GBrain provider behavior. |
| Does local port availability prove Ollama works? | No. | `127.0.0.1:11434` was reachable, but `Get-Command ollama` returned no output. | Future sandbox may run controlled Ollama metadata/inference only if authorized. |
| Can GBrain be useful before embeddings? | Yes, keyword/direct retrieval candidate. | Search modes document says keyword search and direct get need no embeddings. | Future sandbox must run GBrain if execution becomes authorized. |
| Can GBrain support local semantic retrieval later? | Yes, candidate. | Ollama, llama-server, and LiteLLM local/openai-compatible paths exist. | Future sandbox must configure model/dimensions and generate embeddings. |
| Can GBrain generate graph data? | Candidate, not yet accepted output. | Link, GraphPath, code edge, traversal, and operation APIs exist. | Need runtime sandbox and visualization-feed schema gate. |
| Can GBrain replace Graphify visualization/report/export? | Not yet. | GBrain export currently writes markdown/raw sidecars; Graphify has report, browser graph, SVG, wiki, call-flow, graph DB exports. | Separate visualization reuse/adaptation gate. |
| Is Claude Code purchase justified now for Graphify extraction? | No. | GBrain local/no-paid candidate covers the semantic layer enough for next evaluation. | Reconsider only after local sandbox and visualization gate evidence. |
| Should Graphify runtime retry resume now? | No. | P12.0A left Graphify runtime retry blocked; P12.0B found no reason to unblock it. | Needs provider/command/governance amendment. |

## Evidence-Bound Graph Model

GBrain can be evaluated as a graph-generation candidate only if future graph rows remain evidence-bound and reviewable. Model-assisted relations must not become authority.

Layer 1: deterministic structural graph. Source: parser/code edges, markdown links, wikilinks, frontmatter mappings, and deterministic link-type inference. Authority level: candidate evidence derived from explicit source structure.

Layer 2: retrieval graph. Source: GBrain keyword/vector/RRF results, typed-edge traversal, code callers/callees/defs/refs, and graph-query traversal. Authority level: retrieval aid, not source of truth.

Layer 3: model-assisted relation candidate graph. Source: future local model suggestions over retrieved evidence. Authority level: candidate relation only; every edge requires evidence reference and human-review status.

Layer 4: visualization graph. Source: normalized feed for browser or external visualization. Authority level: presentation layer only; no approval, truth, or runtime control authority.

Required relation fields:

| Field | Purpose |
| --- | --- |
| `relation_id` | Stable row identity for review and stale-edge tracking. |
| `source_node` | Origin node slug/id/symbol. |
| `target_node` | Target node slug/id/symbol. |
| `relation_type` | Typed relation such as `calls`, `imports`, `mentions`, `works_at`, `invested_in`, `depends_on`, or future controlled vocabulary. |
| `evidence_ref` | Exact evidence pointer or source quote handle. |
| `source_path` | File/page path that supports the relation. |
| `line_or_section_ref` | Line number, section heading, or chunk id. |
| `model_used` | `deterministic`, parser name, or local model identifier. |
| `confidence` | Bounded confidence label or numeric score. |
| `review_status` | `unreviewed`, `accepted`, `rejected`, `needs_more_evidence`, or equivalent controlled status. |
| `staleness_marker` | Commit hash, file mtime/hash, source revision, or extraction timestamp used to invalidate old edges. |

Example candidate row shape:

```json
{
  "relation_id": "candidate:sha256:<stable-input-hash>",
  "source_node": "src/core/operations.ts::traverse_graph",
  "target_node": "src/core/engine.ts::traversePaths",
  "relation_type": "calls",
  "evidence_ref": "operations.ts:2114",
  "source_path": "4_external/sources/gbrain-master/src/core/operations.ts",
  "line_or_section_ref": "2114",
  "model_used": "deterministic-source-review",
  "confidence": "EXTRACTED",
  "review_status": "unreviewed",
  "staleness_marker": "source-review-2026-07-09"
}
```

## Boundaries

GBrain remains an external candidate evidence source. It is not authority, source of truth, runtime, approval engine, Cognitive Semantic System substrate, or governance controller.

Ollama remains a local provider candidate. It is not authority, and local port reachability does not prove model inventory, model quality, inference behavior, or GBrain compatibility.

Model-assisted relations remain candidate evidence only. They must cite source evidence, carry confidence and review status, and remain invalidatable through staleness markers.

Graphify remains a visualization/report/export candidate. Its frontend, browser graph, report format, and exports require a separate reuse/adaptation gate before any copying, extraction, runtime retry, or generated-output import.

Product/Siamese source, generated outputs, `graphify-out/**`, credentials, `.env*`, provider configs, token stores, and unrelated external sources remain outside this review.

## Future Sandbox Gate

A later sandbox may be proposed, but this document does not authorize it. A future sandbox must specify exact commands, root, ignore scope, model/provider boundaries, expected outputs, rollback/delete behavior, and whether any files, databases, vector stores, graph stores, or generated artifacts may be created.

Minimum future sandbox questions:

| Question | Required Evidence |
| --- | --- |
| Is Ollama actually installed and callable from the sandbox shell? | Controlled command discovery and version/model metadata, if authorized. |
| Which local embedding model exists? | Authorized model inventory only; no assumptions from port reachability. |
| Does GBrain initialize without paid APIs? | Controlled GBrain init in disposable path, if authorized. |
| Does keyword search work without embeddings? | Controlled GBrain search over disposable non-sensitive corpus, if authorized. |
| Does Ollama embedding work with expected dimensions? | Controlled one-shot embedding against disposable text, if authorized. |
| What graph/export shape is available? | Controlled graph traversal/export inspection over disposable corpus, if authorized. |
| Can graph data feed visualization? | Explicit JSON/feed contract and separate visualization gate. |

Forbidden until a future gate explicitly authorizes otherwise:

```text
gbrain runtime execution
graphify runtime execution
ollama list/show/run/pull/serve/ps
model inference
provider API calls
embedding generation
database/vector/graph store creation
package installation
tests/builds/CI
credential or .env inspection
product/Siamese source inspection
Graphify frontend copying
Git mutation
```

## Commit Commands

If this governance record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md
git commit -m "Add GBrain Ollama graph feasibility review"
```

If `0_architecture/implementation/graphify_command_candidate_confirmation.md` should also be committed, stage it explicitly in a separate decision or include it explicitly after review. This P12.0B document does not authorize staging unrelated untracked files.

## Verification Result

Non-mutating marker verification after creation found all required markers.

Marker search command shape used by this review:

```powershell
rg "gbrain_ollama_local_provider_graph_generation_feasibility_review_ready|gbrain_ollama_provider_feasible_for_future_sandbox|gbrain_graph_generation_candidate|gbrain_graph_generation_requires_runtime_sandbox|gbrain_visualization_feed_candidate|graphify_visualization_reuse_still_separate_gate" 0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md
git status --short
```

Observed `git status --short` after creation:

```text
?? 0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

The implementation file was already observed as untracked before this P12.0B document was created and was not modified by this review.

Final marker:

```text
gbrain_ollama_local_provider_graph_generation_feasibility_review_ready
```

gbrain_ollama_local_provider_graph_generation_feasibility_review_ready
