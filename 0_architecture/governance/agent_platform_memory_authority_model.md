# Agent Platform Memory Authority Model

## 1. Document Header

| Field | Value |
| --- | --- |
| Ticket | P12.3 |
| Title | Memory Authority Model |
| Type | Governance / architecture / memory-authority-model / no-runtime |
| Status | Drafted for acceptance |
| Target file | `0_architecture/governance/agent_platform_memory_authority_model.md` |
| Authority | Governance/design only. This document is not GBrain execution, GStack execution, Graphify execution, graph-query execution, embedding generation, memory reindex, provider/API/MCP activation, credential inspection, markdown cleanup, generated output tracking approval, source tracking expansion, runtime activation, Git mutation, or production agent taxonomy execution. |
| Result marker | `memory_authority_model_ready` |

## 2. Purpose

P12.3 defines the authority model for memory used by the agent platform.

The model separates canonical source of truth, derived memory index, retrieval evidence, generated evidence, debug/audit history, external source evidence, operational memory, skill memory, and sandbox outputs.

The core rule is simple: retrieval systems, generated files, search results, summaries, sandbox outputs, debug records, and external source snapshots may support review, but they do not become authority unless a future accepted governance record explicitly promotes exact scoped evidence.

## 3. P12.0E-GRAPH-REVIEW Dependency Status

P12.0E-GRAPH-REVIEW exists as:

`0_architecture/governance/agent_platform_gbrain_empty_graph_query_output_review.md`

Required marker confirmed:

`gbrain_empty_graph_query_output_review_ready`

Confirmed Mode A evidence classification:

| Capability | P12.3 classification | Authority implication |
| --- | --- | --- |
| Local GBrain install | validated | GBrain may be considered local retrieval infrastructure candidate only. |
| Governance markdown import | validated | Imported pages are derived index records, not source of truth. |
| Governance markdown chunking | validated | Chunks are derived retrieval units, not canonical policy. |
| Keyword search | validated | Keyword results may locate source refs, not approve decisions. |
| Export imported pages | validated | Exports are generated evidence unless explicitly promoted. |
| Local sandbox isolation | validated | Sandbox evidence supports feasibility only. |
| Graph edge extraction | not validated | No authority may rely on GBrain graph edges as complete. |
| Graph traversal usefulness | not validated | Graph traversal cannot be operational memory authority. |
| Semantic embeddings | not validated | Embedding/vector memory remains future candidate only. |
| Ollama Mode B | not validated | Local semantic provider behavior remains untested. |
| GStack | not validated | GStack remains pending and not adopted. |

P12.0E closes the P12.0A-P12.0E GBrain technical feasibility branch and allows Project 12 main roadmap work to resume. It does not authorize runtime adoption, production memory, graph memory authority, embeddings, Ollama Mode B, GStack adoption, or cleanup.

## 4. Inputs Reviewed

P12.3 consumed only allowed governance and metadata inputs.

| Input | Role in P12.3 | Inspection posture |
| --- | --- | --- |
| `agent_platform_gbrain_empty_graph_query_output_review.md` | P12.0E dependency and Mode A classification | Marker/content search only. |
| `agent_platform_gbrain_license_dependency_storage_audit.md` | GBrain storage and sandbox boundary | Marker/content search only. |
| `agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md` | GBrain versus Graphify role split | Marker/content search only. |
| `agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md` | Ollama/semantic candidate boundary | Marker/content search only. |
| `agent_platform_graphify_evidence_output_classification.md` | Generated evidence and Graphify output authority boundary | Marker/content search only. |
| `agent_platform_graphify_integration_scope_markdown_authorization.md` | Graphify allowed/blocked scope and authority boundary | Marker/content search only. |
| `agent_platform_graphify_markdown_scope_safety_review.md` | Graphify markdown scope safety posture | Existing governance context only. |
| `agent_platform_external_tool_execution_gate_model.md` | External execution and generated output gate model | Marker/content search only. |
| `agent_platform_human_approval_review_loop_operational_contract.md` | Human approval and review authority boundary | Marker/content search only. |
| `agent_platform_shared_context_evidence_bus_operational_contract.md` | EvidenceRef and context bus boundary | Marker/content search only. |
| `.graphifyignore` | Graphify input scope and blocked scope posture | Read-only; not modified. |
| `.gitignore` | Local-only/generated/external/secret/product hygiene posture | Read-only; not modified. |
| Repository metadata paths | Presence of governance, skeleton, external, and artifact roots | Path metadata only. |

No product/Siamese source, credential file, external source content, generated artifact content, raw Graphify output, normal user GBrain/GStack state, package cache, DB internal, or sandbox output content was inspected.

## 5. Memory Tier Overview

| Tier | Name | Role | Authority posture |
| --- | --- | --- | --- |
| Tier A | Canonical authority | Accepted source of truth | Authoritative within exact scope. |
| Tier B | Derived memory index | Retrieval and context assembly | Useful, rebuildable, non-authoritative. |
| Tier C | Generated evidence | Tool/sandbox/report outputs | Supporting evidence only by default. |
| Tier D | Audit/debug history | Traceability of decisions and runs | Historical evidence; not operating policy by default. |
| Tier E | External source evidence | Candidate third-party evidence | Not adopted and not authority by default. |
| Overlay | Operational memory | Curated subset for agent work | Includes only allowed current canonical and selected supporting refs. |
| Overlay | Skill memory | Future skill/tool packaging metadata | Never authority by itself; gated by skill/execution decisions. |

## 6. Tier A - Canonical Authority

Authoritative memory is the accepted source of truth for platform decisions and operating boundaries.

Canonical authority may include:

| Class | Examples | Conditions |
| --- | --- | --- |
| Accepted governance documents | Accepted records under `0_architecture/governance/` | Must be accepted by the project process and not superseded. |
| Accepted architecture documents | Accepted architecture or design records under approved architecture scope | Must define current policy or design, not just brainstorming. |
| Accepted implementation boundary documents | Runtime, tool, memory, skill, source, and safety boundary contracts | Must define exact allowed/blocked behavior. |
| Committed source files inside approved source scopes | Current governed platform source in approved scopes such as `3_platform/_governed_skeleton/**/*.py` | Source authority is limited to implementation behavior, not governance approval. |
| Explicit human approval records | Accepted approval/rejection records with exact scope | Human approval/rejection outranks lower evidence inside its declared scope. |
| Accepted closure records | Closure or reconciliation records | May supersede earlier planning records only when explicit. |
| Accepted adoption decisions | Tool/source/substrate adoption records | Must state exact adoption mode, limitations, and rollback/incident posture. |

Canonical authority must not include:

| Non-canonical item | Reason |
| --- | --- |
| Search results alone | Retrieval can be stale, partial, or incorrectly scoped. |
| Summaries alone | Summaries can omit conflict, limitations, or source refs. |
| Sandbox outputs alone | Sandbox outputs are generated evidence. |
| Generated exports alone | Exports are derived/generated until reviewed and promoted. |
| Agent guesses | Not evidence. |
| Retrieval snippets without source | Cannot be audited or conflict-checked. |
| Unreviewed external docs | External evidence requires gates before adoption. |
| Debug artifacts unless accepted as audit evidence | Debug history explains events but does not define operating policy by default. |

Decision marker:

`canonical_memory_sources_defined`

## 7. Tier B - Derived Memory Index

Derived memory is rebuildable retrieval infrastructure over canonical and permitted supporting sources.

Derived memory includes:

| Class | Examples | Required boundary |
| --- | --- | --- |
| GBrain imported pages | Imported governance markdown pages | Must cite canonical file/path/slug. |
| GBrain chunks | Chunked markdown/code units | Must remain derived retrieval units. |
| GBrain keyword index | Keyword search over imported pages | Must return source refs and snippets, not decisions. |
| GBrain exports | Exported imported pages | Generated evidence unless promoted. |
| Future embeddings | Vector representations | Future only; requires exact provider/storage gate. |
| Future vector indexes | Vector DB/index | Future only; not authority. |
| Future graph indexes | Graph/edge indexes | Future only; graph edge usefulness currently not validated. |

Derived memory rules:

| Rule | Requirement |
| --- | --- |
| Rebuildable | Derived memory must be reproducible from canonical or permitted source refs. |
| Cited | Every operationally useful hit must cite canonical source path, slug, or accepted evidence ref. |
| Non-authoritative | Derived memory cannot approve actions, mutate state, or override governance docs. |
| Conflict-limited | If derived memory conflicts with canonical docs, canonical docs win. |
| Scope-limited | Derived memory must not include blocked content or expand source visibility. |
| Reviewable | Derived memory should preserve enough metadata to audit freshness and source scope. |

Decision marker:

`derived_memory_index_role_defined`

## 8. Tier C - Generated Evidence

Generated evidence is output produced by tools, sandboxes, exports, graph queries, reports, validators, logs, or agents.

Generated evidence includes:

| Class | Examples | Default posture |
| --- | --- | --- |
| Graphify outputs | `graphify-out/**`, graph maps, reports, visualizations | Raw generated evidence; local-only unless reviewed. |
| GBrain sandbox outputs | GBrain sandbox home, DB, exports, stdout/stderr, run records | Generated evidence; not memory authority. |
| Graph-query stdout | Empty or non-empty graph-query results | Supports review only; not graph truth. |
| Exports under `9_artifacts` | Exported pages/reports | Generated/local-only until exact promotion. |
| Reports | Human/agent/tool reports | Supporting review evidence with citations. |
| Temporary evidence maps | Relationship maps, analysis maps | Evidence only. |
| Runtime logs | Logs from future approved runs | Audit/debug evidence, possibly sensitive. |
| Debug/run records | Execution records, safe failure records, rerun records | Audit evidence unless promoted. |

Generated evidence rules:

| Rule | Requirement |
| --- | --- |
| Not source of truth by default | Generated outputs cannot define policy or approve work. |
| Supports review | Generated outputs may help reviewers locate facts or risks. |
| Requires explicit promotion | To become canonical, exact evidence must be reviewed and accepted into governance or approved source. |
| Local/untracked default | Generated outputs remain local/untracked unless exact tracking approval exists. |
| Sensitive by default | Generated outputs may contain copied source, snippets, paths, or secrets and must be handled conservatively. |

Decision marker:

`generated_outputs_non_authoritative_by_default`

## 9. Tier D - Audit / Debug History

Audit/debug history records what happened, what failed safely, what was blocked, and why a branch closed.

Audit/debug history includes:

| Class | Examples | Default memory role |
| --- | --- | --- |
| Safe block records | Missing key safe failure, blocked runtime, blocked provider | Traceability. |
| Failed runs | Failed install, failed Graphify/GBrain attempt, empty graph result | Evidence of past behavior, not current policy alone. |
| Reruns | Controlled rerun records | Evidence of process and output posture. |
| Temporary command-prep files | Exact command plans or command candidates | Planning/audit only. |
| Installation boundary records | Storage/install/dependency audit records | Policy if accepted; debug detail may be downranked later. |
| Debugging tickets | P12.0A-P12.0E records, P10 run records | Historical branch context. |
| Risk reviews | Safety, output, license, source, execution reviews | Governance evidence when accepted. |

Audit/debug history rules:

| Rule | Requirement |
| --- | --- |
| Useful for traceability | Keep enough history to explain decisions and rollbacks. |
| Do not dominate operational memory | Future memory imports should downrank obsolete failed attempts and intermediate prep unless actively relevant. |
| Cleanup deferred | Classification, retention, archiving, and compaction are deferred to a later CLEAN project. |
| No deletion in P12.3 | P12.3 does not clean, delete, archive, move, or rewrite history. |
| Promotion required for policy | Debug records define policy only when an accepted governance record explicitly says so. |

Decision marker:

`debug_history_retention_policy_deferred_to_cleanup`

## 10. Tier E - External Source Evidence

External source evidence is third-party or candidate tool/source material under external roots.

External source evidence includes:

| Class | Examples | Default posture |
| --- | --- | --- |
| External source trees | `4_external/sources/**` | Candidate evidence only. |
| Vendor source | Third-party repos | Not adopted by default. |
| Third-party docs | External documentation snapshots | Not authority by default. |
| GBrain source | `4_external/sources/gbrain-master/**` | Candidate memory infrastructure evidence. |
| GStack source | `4_external/sources/gstack-main/**` | Candidate skill stack evidence; pending. |
| Hermes source | Future candidate source | Candidate evidence only. |
| Paperclip source | Future candidate source | Candidate evidence only. |
| Graphify source | Graphify candidate source | Candidate visualization/evidence tooling evidence. |

External source evidence rules:

| Rule | Requirement |
| --- | --- |
| Candidate evidence | External source can inform reviews, not define platform policy by itself. |
| Not adopted by default | Adoption requires explicit license/trust, dependency, security, execution, and integration decisions. |
| No authority transfer | External docs or code cannot override accepted Agent Platform governance. |
| License/trust gates required | Source review is separate from license and trust acceptance. |
| Execution gates required | Source availability does not authorize commands, installs, builds, tests, runtime, or providers. |
| Promotion requires adoption | No external source becomes platform authority without accepted adoption decision and exact scope. |

## 11. Operational Memory Scope

Operational memory is the future curated memory subset used by agents for context assembly and decision support.

Operational memory may include:

| Candidate | Inclusion rule |
| --- | --- |
| Canonical architecture docs | Include active accepted architecture docs with source refs. |
| Accepted governance docs | Include accepted, current governance boundaries and decisions. |
| Accepted adoption decisions | Include exact adoption mode, allowed/blocked scope, and constraints. |
| Current roadmap docs | Include active roadmap state only when current and accepted. |
| Active boundary contracts | Include memory, tool, skill, source, approval, retention, rollback, incident, and security contracts. |
| Active implementation contracts | Include current implementation boundaries and source-scope metadata. |
| Active source metadata | Include file/path/class metadata for approved scopes; do not include blocked source bodies. |
| Accepted closure records | Include closure records that supersede earlier branches. |

Operational memory should exclude or downrank:

| Candidate | Default action |
| --- | --- |
| Safe block records | Downrank unless needed for incident/rollback context. |
| Failed install attempts | Downrank after closure or cleanup classification. |
| Intermediate command-prep tickets | Exclude from production operational import unless still active. |
| Old Graphify failure debug | Downrank after accepted closure or replacement boundary. |
| Obsolete OpenAI-provider branches | Exclude/downrank unless current provider decision references them. |
| Duplicate rerun records | Collapse to latest accepted closure plus citations. |
| Generated sandbox exports | Exclude from operational memory unless promoted. |
| Raw run logs | Exclude by default; treat as generated/sensitive audit evidence. |
| Raw Graphify outputs | Exclude by default. |
| Raw external source content | Exclude unless exact gate allows review. |
| Secrets/credentials/provider configs/token stores | Always excluded. |
| Product/Siamese source | Excluded from P12.3 operational memory scope. |

Operational memory must carry source refs, accepted status, freshness, supersession posture, sensitivity, limitations, and blocker metadata.

Decision marker:

`operational_memory_scope_defined`

## 12. Promotion Rules

Promotion is how non-authoritative memory becomes canonical authority or permitted operational memory.

Promotion rules:

| Step | Requirement |
| --- | --- |
| 1. Exact source ref | Identify the exact file, output, record, or source path being promoted. |
| 2. Classification | Classify as canonical, derived, generated, audit/debug, external source, operational, or skill memory candidate. |
| 3. Scope check | Confirm the source is inside an approved scope or has an explicit review/adoption gate. |
| 4. Sensitive-content check | Confirm no secrets, credentials, provider config, token stores, product source, or blocked content is promoted. |
| 5. Conflict check | Compare against existing accepted governance, architecture, human decisions, and source authority. |
| 6. Human review | Obtain exact-scope human approval when required by governance. |
| 7. Accepted governance record | Record promotion in an accepted governance/architecture/adoption/closure document. |
| 8. Tracking decision | Track only exact approved files; generated outputs stay local/untracked unless explicitly approved. |
| 9. Rollback/incident posture | Define rollback and incident route for promoted evidence if applicable. |
| 10. Memory reindex gate | Reindex operational memory only after a future exact memory integration/cleanup gate. |

Promotion cannot be automatic. Search hits, GBrain pages, Graphify outputs, GBrain exports, chat summaries, or sandbox outputs do not promote themselves.

## 13. Exclusion Rules

The following must remain outside operational memory unless a later exact governance gate explicitly narrows the scope and authorizes a safe representation:

| Excluded class | Examples |
| --- | --- |
| Secrets and credentials | `.env`, `.env.*`, `credentials/**`, `secrets/**`, API keys, token stores, browser auth, local credential stores, Claude/OpenAI/Anthropic/Gemini credentials. |
| Provider configs | Provider config files, auth state, local service credentials, API/MCP auth payloads. |
| Product/Siamese source | `2_products/**`, `product/**`, `products/**`, product runtime/data/adapters. |
| Raw external source | `4_external/sources/**`, including GBrain/GStack/Graphify source bodies unless exact review gate allows. |
| Generated artifacts | `9_artifacts/**`, sandbox homes, generated DBs, generated exports, raw logs. |
| Raw Graphify outputs | `graphify-out/**`, graph reports, raw graph JSON/HTML/SVG unless classified and promoted. |
| User home tool state | Normal user `.gbrain`, `.gstack`, provider state, caches, package caches. |
| DB internals | DB files under generated/sandbox roots. |
| Unaccepted summaries | Chat notes, draft summaries, unstaged notes not accepted into governance. |

Operational memory may store safe metadata about excluded classes only when needed: path class, blocked status, reason, and required future gate. It must not store sensitive payloads or raw bodies.

## 14. GBrain Authority Boundary

GBrain is local memory/retrieval infrastructure.

GBrain is not:

| Blocked authority role | Rule |
| --- | --- |
| Source of truth | Canonical governance and accepted source files remain source of truth. |
| Approval authority | GBrain cannot approve tickets, gates, adoption, execution, tracking, or promotion. |
| Runtime authority | GBrain cannot decide runtime activation or tool execution. |
| Policy authority | GBrain cannot override accepted governance documents. |
| Repository mutation authority | GBrain output/search cannot stage, commit, edit, delete, move, or rewrite files. |
| Production memory writer | GBrain cannot write production operational memory without future gate. |

Allowed GBrain role:

| Allowed role | Boundary |
| --- | --- |
| Retrieve governance context | Search/index accepted governance and approved source metadata. |
| Index canonical markdown | Store derived pages/chunks with source refs. |
| Support context assembly | Provide cited retrieval candidates to agents/humans. |
| Support evidence discovery | Locate relevant records for review. |
| Support future memory store integration | Candidate infrastructure for P12.7 only after authority model and P12.5. |

Blocked GBrain role:

| Blocked role | Rule |
| --- | --- |
| Approve tickets | Human/governance records decide. |
| Decide adoption alone | Adoption requires accepted decision. |
| Override governance docs | Canonical docs win. |
| Edit source | No repository mutation authority. |
| Execute skills | Skill execution requires separate P12.4/P12.6 gates. |
| Call providers | Provider/API/MCP gates required. |
| Write production memory without gate | Memory writes require P12.7 or later exact gate. |

Decision marker:

`gbrain_memory_authority_boundary_defined`

## 15. Graphify Authority Boundary

Graphify is an evidence-map, visualization, and report candidate.

Graphify is not:

| Blocked authority role | Rule |
| --- | --- |
| Source of truth | Governance docs and accepted source files remain source of truth. |
| Approval authority | Graphify output cannot approve source, scope, execution, tracking, or adoption. |
| Memory authority | Graphify graphs/reports cannot become operational graph memory by default. |
| Cognitive Semantic System substrate | Substrate selection remains deferred unless later adopted. |
| Scope authority | Graphify cannot read blocked scopes or expand input scope. |
| Promotion authority | Graphify cannot promote generated outputs automatically. |

Allowed Graphify role:

| Allowed role | Boundary |
| --- | --- |
| Visualize relationships | Under exact allowed input/output scope only. |
| Summarize evidence | As generated/supporting evidence only. |
| Support review | Reviewers may use maps/reports as leads, not decisions. |
| Generate maps/reports | Only under future classification and execution gates. |

Blocked Graphify role:

| Blocked role | Rule |
| --- | --- |
| Authoritative graph memory | Not allowed by P12.3. |
| Approve source | Not allowed. |
| Override GBrain/governance | Governance authority wins. |
| Read blocked scopes | Blocked by `.graphifyignore` and governance. |
| Promote generated outputs automatically | Requires exact future promotion. |

Decision marker:

`graphify_evidence_map_authority_boundary_defined`

## 16. GStack Relationship Boundary

P12.3 does not decide GStack adoption.

GStack remains pending and unvalidated. If later adopted, GStack is positioned as a candidate for:

| Candidate role | Boundary |
| --- | --- |
| Skill stack | Candidate packaging/execution layer for skills. |
| Tool execution candidate | Requires exact execution gates. |
| Workflow/skill packaging candidate | Requires skill authority boundary and adoption decision. |

GStack must not become memory authority. It cannot decide canonical truth, promote memory, override governance, approve actions, read blocked scopes, write production memory, or execute skills without future gates.

Future dependencies:

| Ticket | Role |
| --- | --- |
| P12.2 - GStack License / Dependency / Skill Audit | License, dependency, and skill surface evidence. |
| P12.4 - Skill Authority / Execution Boundary | Defines skill execution authority and blocked roles. |
| P12.6 - GStack Adoption Decision | Decides whether and how GStack is adopted. |

## 17. Conflict Resolution Rules

Memory conflict hierarchy, highest to lowest authority:

| Rank | Source class |
| --- | --- |
| 1 | Explicit human approval / rejection in accepted governance record. |
| 2 | Accepted governance / architecture document. |
| 3 | Committed source file in approved scope. |
| 4 | Accepted execution record. |
| 5 | Accepted audit/debug record. |
| 6 | External source evidence under approved review. |
| 7 | Derived GBrain memory / chunks / search result. |
| 8 | Generated Graphify/GBrain evidence output. |
| 9 | Chat memory / unstaged notes / unaccepted summaries. |

Conflict rules:

| Rule | Requirement |
| --- | --- |
| Newer is not automatically more authoritative | Acceptance and scope outrank timestamp. |
| Closure can supersede planning | Latest accepted closure may supersede earlier planning docs when explicit. |
| Debug records explain history | Debug records do not define operating policy unless explicitly promoted. |
| Source code is scoped authority | Source files describe implementation behavior but cannot override governance approval boundaries. |
| Generated evidence supports only | Generated evidence can trigger review but cannot resolve conflicts alone. |
| Derived memory loses to canonical | Search/chunks/exports cannot override accepted documents. |
| External evidence remains candidate | Third-party docs/source cannot override project governance unless adopted. |
| Stop on unresolved conflict | If conflict persists after hierarchy application, stop and require human review. |

Decision marker:

`memory_conflict_resolution_rules_defined`

## 18. Repository and Tool Positioning Matrix

| Surface | P12.3 position | Authority boundary |
| --- | --- | --- |
| Governance markdown | Primary canonical authority when accepted and current | Source of truth for policy/design. |
| Architecture docs | Canonical authority when accepted and current | Source of truth for architecture. |
| Repo source files | Canonical for implementation behavior inside approved scope | Cannot approve governance actions. |
| GBrain | Derived retrieval/index infrastructure | Not source of truth, approval, runtime, or policy authority. |
| Graphify | Generated evidence map/report/visualization candidate | Not memory authority or approval authority. |
| Sandbox outputs | Generated evidence | Not source of truth by default. |
| `9_artifacts/**` | Generated/local-only artifact surface | Excluded from operational memory by default. |
| External sources | Candidate evidence only | Require source/license/trust/execution/adoption gates. |
| GStack | Future skill/tool candidate | Not memory authority; adoption deferred. |
| Skills | Future execution packaging | Requires P12.4 authority boundary and execution gates. |
| Shared context/evidence bus | Metadata reference contract | EvidenceRef binding is not authority. |

## 19. Cleanup Dependency

Before production use of the agent taxonomy on real projects, a knowledge cleanup / memory compaction project is required.

Future project candidate:

`CLEAN - Knowledge Base Cleanup / Memory Operational Readiness`

Blocked before CLEAN.R or equivalent accepted cleanup closure:

| Blocked activity | Reason |
| --- | --- |
| Production agent taxonomy execution on real projects | Current memory contains useful debug history that may dominate operational context. |
| Clean memory reindex as operational source | Classification and compaction rules are not yet applied. |
| Long-lived autonomous context assembly | Requires clean operational memory profile and retention/rollback/incident posture. |

P12.3 does not delete, clean, archive, move, rewrite, or compact existing markdowns or records.

Decision marker:

`cleanup_required_before_agent_taxonomy_production`

## 20. P12.7 Handoff Decision

P12.3 hands off to:

`P12.7 - Memory Store Integration Design`

P12.7 should wait for:

| Dependency | Reason |
| --- | --- |
| P12.3 accepted | Memory authority model must be accepted before integration design. |
| P12.5 accepted | Source/memory/retention details from P12.5 must be integrated before store design. |

P12.7 may design how a memory store uses canonical source refs, derived indexes, generated evidence refs, audit/debug refs, and operational memory profiles. P12.7 must not make derived memory authoritative unless a later accepted governance decision changes this model explicitly.

P12.3 also informs:

| Future item | Influence |
| --- | --- |
| P12.4 - Skill Authority / Execution Boundary | Skill memory and skill execution cannot become memory authority. |
| P12.11 - Retention / Rollback / Incident Hardening | Generated/audit memory retention and incident handling. |
| CLEAN - Knowledge Base Cleanup / Memory Operational Readiness | Operational memory compaction and debug-history downranking. |

Decision marker:

`p12_7_memory_store_integration_ready_after_authority_model`

## 21. Stop Rules

STOP if work requires any of the following:

| Stop condition | Required response |
| --- | --- |
| Run GBrain, GStack, Graphify, graph-query, Ollama, embeddings, providers, package managers, tests, builds, scripts, CI, Docker, Node, Python, npm, or Bun | Stop and require exact future execution gate. |
| Inspect credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, or user home tool state | Stop and preserve secret boundary. |
| Inspect `9_artifacts/**` contents, DB internals, generated home internals, raw Graphify outputs, or sandbox output internals | Stop and require generated-output review gate. |
| Inspect product/Siamese source | Stop and require product/source gate. |
| Inspect external source content outside explicit future gate | Stop and require source review gate. |
| Clean, delete, archive, move, or rewrite markdown/debug history | Stop and route to CLEAN project. |
| Modify `.gitignore` or `.graphifyignore` | Stop and require exact patch ticket. |
| Mutate Git | Stop unless exact user request and governance approval exist. |
| Recommend `git add .` | Stop; use exact path only. |

## 22. Acceptance Criteria Mapping

| Criterion | Status |
| --- | --- |
| Creates exactly one governance architecture file | Satisfied by this file only. |
| Defines canonical authority tiers | Satisfied in Tier A. |
| Defines derived memory role | Satisfied in Tier B. |
| Defines generated evidence role | Satisfied in Tier C. |
| Defines audit/debug history role | Satisfied in Tier D. |
| Defines external source evidence role | Satisfied in Tier E. |
| Defines GBrain authority boundary | Satisfied. |
| Defines Graphify authority boundary | Satisfied. |
| Does not prematurely adopt GStack | Satisfied. |
| Defines conflict resolution hierarchy | Satisfied. |
| Defines operational memory scope | Satisfied. |
| Defines cleanup dependency before production agent taxonomy execution | Satisfied. |
| Keeps runtime blocked | Satisfied. |
| Does not clean files | Satisfied. |
| Does not mutate Git | Satisfied. |

## 23. Created / Not Created Register

Created:

| Item | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_memory_authority_model.md` | Created as P12.3 memory authority model. |

Not created / not approved:

| Item | Status |
| --- | --- |
| Memory reindex | Not created / not run. |
| GBrain execution | Not run. |
| GStack execution | Not run. |
| Graphify execution | Not run. |
| Ollama command | Not run. |
| Embeddings | Not generated. |
| Provider/API call | Not performed. |
| Markdown cleanup | Not performed. |
| File deletion | Not performed. |
| Archive move | Not performed. |
| Sandbox output modification | Not performed. |
| DB/internal inspection | Not performed. |
| Credential inspection | Not performed. |
| PATH mutation | Not performed. |
| Git mutation | Not performed. |
| `git add .` | Not recommended. |

## 24. Decision Markers

memory_authority_model_ready

canonical_memory_sources_defined

derived_memory_index_role_defined

gbrain_memory_authority_boundary_defined

graphify_evidence_map_authority_boundary_defined

generated_outputs_non_authoritative_by_default

debug_history_retention_policy_deferred_to_cleanup

memory_conflict_resolution_rules_defined

operational_memory_scope_defined

cleanup_required_before_agent_taxonomy_production

p12_7_memory_store_integration_ready_after_authority_model

## 25. Final Verdict

P12.3 defines the memory authority model for the agent platform.

Authoritative memory is limited to accepted governance/architecture/boundary/adoption/closure records, explicit human approval or rejection records, and committed source files inside approved source scopes for implementation behavior only.

Derived indexes, GBrain pages/chunks/search/export, Graphify outputs, generated reports, sandbox outputs, debug records, external source snapshots, chat memory, and summaries are not authoritative by default.

GBrain may support retrieval and future memory store integration as derived infrastructure. Graphify may support evidence mapping and visualization as generated evidence. GStack remains a pending skill/tool candidate and is not memory authority.

Production agent taxonomy execution on real projects remains blocked until a CLEAN knowledge cleanup / memory operational readiness project is accepted.
