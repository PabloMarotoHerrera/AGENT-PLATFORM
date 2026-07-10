# Agent Platform Memory Store Integration Design

## 1. Document Header

| Field | Value |
| --- | --- |
| Ticket | P12.7 |
| Title | Memory Store Integration Design |
| Type | Architecture / memory-store-design / retrieval-integration-boundary / no-runtime |
| Status | Drafted for acceptance |
| Target file | `0_architecture/governance/agent_platform_memory_store_integration_design.md` |
| Authority | Design only. This document is not memory store implementation, memory reindex, GBrain execution, GStack execution, Graphify execution, graph-query execution, Ollama execution, embedding generation, provider/API/MCP activation, markdown cleanup, DB/internal inspection, sandbox output inspection, source tracking expansion, generated output tracking, Git mutation, or production agent taxonomy execution. |
| Result marker | `memory_store_integration_design_ready` |

## 2. Purpose

P12.7 designs the future memory store integration for the agent platform.

The design answers what the memory store is, which sources feed it, which sources must not feed it, how GBrain fits as derived retrieval/index infrastructure, what remains canonical outside GBrain, how memory references are represented, how debug records are downranked, how refresh/reindex is governed, how CLEAN affects production operational memory, and how P12.9 should run a canonical local memory sandbox spike later.

P12.7 does not build, run, reindex, clean, inspect sandbox internals, or mutate Git.

## 3. Dependency Status

| Dependency | Required posture | P12.7 status | Decision impact |
| --- | --- | --- | --- |
| P12.3 Memory Authority Model | Present with `memory_authority_model_ready` | Confirmed | P12.7 must preserve canonical authority and derived/generated evidence boundaries. |
| P12.5 GBrain adoption / Graphify semantic replacement decision | Present with `gbrain_adoption_graphify_semantic_replacement_decision_ready` | Confirmed | GBrain may be designed as semantic retrieval/local memory indexing candidate, not authority. |
| P12.2 GStack license/dependency/skill audit | Present with `gstack_license_dependency_skill_audit_ready` | Confirmed | GStack remains pending; setup/runtime/skills/browser/providers/hooks/Git remain blocked. |
| P12.0E GBrain graph review closure | Present with `gbrain_empty_graph_query_output_review_ready` and `p12_0e_branch_closed` posture | Confirmed | Mode A keyword memory is validated; graph edges/traversal are not validated authority. |
| P12.4 Skill Authority / Execution Boundary | Optional peer | Present with `skill_authority_execution_boundary_ready`; inspected read-only after it appeared in the working tree | P12.7 records skill-memory alignment only and must not decide skill execution. |

Confirmed P12.3 decisions consumed by P12.7:

| P12.3 decision | P12.7 use |
| --- | --- |
| Canonical governance / architecture / adoption / closure records remain source of truth. | Memory store records references to canonical files, not authority replacements. |
| GBrain pages, chunks, search results, exports, graph-query output, and sandbox outputs are derived/generated evidence. | GBrain integration is Tier B/Tier C only. |
| Derived memory is useful for retrieval and context assembly, but not authority. | Search output must cite canonical refs and cannot decide. |
| Generated outputs are not source of truth by default. | Generated exports and graph outputs are excluded by default. |
| Audit/debug history must not dominate operational memory. | Operational profiles downrank debug records. |
| Production agent taxonomy execution remains blocked until CLEAN. | OM-2 remains blocked. |

Confirmed P12.5 decisions consumed by P12.7:

| P12.5 decision | P12.7 use |
| --- | --- |
| GBrain replaces Graphify for semantic retrieval / local memory indexing. | GBrain is the designed derived retrieval index provider. |
| GBrain does not replace Graphify for visualization/reporting/evidence maps. | Graphify remains outside semantic memory store authority. |
| GBrain is not source of truth. | Canonical files remain outside and above GBrain. |
| GBrain is not approval authority. | Memory hits cannot approve actions. |
| GBrain is not graph traversal authority. | Graph-query/edges stay generated evidence until future validation. |
| Mode B / Ollama remains deferred. | P12.7 default design is keyword-only / no-provider baseline. |

Confirmed P12.2 / GStack boundary consumed by P12.7:

| P12.2 decision | P12.7 use |
| --- | --- |
| GStack is license-permissible for further evaluation. | GStack may be referenced as future skill-stack candidate. |
| GStack setup/runtime/skills/browser/providers/hooks/Git remain blocked. | No skill/runtime memory integration is designed here. |
| GStack is not adopted yet. | P12.7 cannot depend on GStack. |
| GStack must not be treated as memory authority. | Skills cannot write memory without future gates. |

## 4. Memory Store Concept

The memory store is a governed retrieval and context assembly layer that references canonical sources and derived indexes without becoming authority.

The memory store is not:

| Not a | Reason |
| --- | --- |
| Source of truth | Canonical files and accepted records remain source of truth. |
| Approval system | Human/governance approval records decide. |
| Runtime execution system | It does not run tools, agents, skills, providers, scripts, or commands. |
| Skill runner | Skill execution remains P12.4/P12.8/P12.6 territory. |
| Graph authority | GBrain graph usefulness is not validated; Graphify graphs are generated evidence. |
| Provider interface | Ollama/hosted providers remain deferred/gated. |
| Cleanup system | CLEAN owns cleanup, compaction, and historical classification. |
| Git mutation system | It cannot stage, commit, push, delete, move, or rewrite files. |

The memory store may contain:

| Memory record type | Purpose |
| --- | --- |
| Source references | Stable refs to canonical repo files and approved source metadata. |
| Document metadata | Path, class, accepted status, freshness, supersession, sensitivity, limitations. |
| Accepted status | Whether a record is accepted, draft, superseded, rejected, or unknown. |
| Supersession metadata | Explicit relationships between active, superseded, and closure records. |
| Classification metadata | Canonical, derived, generated, audit/debug, external, operational, or skill candidate. |
| Retrieval index references | Pointers to GBrain index/sandbox/store records. |
| GBrain page/chunk references | Derived refs back to canonical source refs. |
| EvidenceRef links | Supporting evidence references with authority posture. |
| Operational memory profiles | OM-0, OM-1, OM-2 and future profile definitions. |
| Refresh manifests | Planned/approved/indexed/stale state records for refreshes. |
| Exclusion/downranking rules | Filters that prevent noisy or unsafe records from dominating context. |

Decision marker:

`memory_store_integration_architecture_defined`

## 5. Canonical Source Reference Model

The canonical source remains the file or accepted record. The memory store stores references and metadata only.

Required reference model:

```yaml
CanonicalSourceRef:
  id: "<stable ID>"
  path: "<repo-relative path>"
  source_class: "governance | architecture | source | adoption | closure | execution_record | audit_record"
  authority_tier: "Tier A"
  accepted_status: "accepted | draft | superseded | rejected | unknown"
  supersedes: []
  superseded_by: []
  sensitivity: "public | internal | restricted | blocked"
  allowed_for_operational_memory: true_or_false
  cleanup_action: "keep | compact | downrank | archive_candidate | exclude"
  canonical_summary: "<optional future generated summary, not authority>"
  citation_required: true
```

CanonicalSourceRef rules:

| Rule | Requirement |
| --- | --- |
| File remains authority | The repo file or accepted governance record remains canonical, not the memory row. |
| Citation required | Operational memory must cite canonical paths or accepted refs. |
| Accepted status controls inclusion | Draft/unknown records cannot outrank accepted records. |
| Supersession explicit | Newer files do not supersede older files unless accepted records say so. |
| Summary is generated | `canonical_summary` is optional future generated support and not authority. |
| Debug records downranked | Debug/audit records may be preserved but not fed into normal context by default. |
| Sensitivity blocks content | Restricted/blocked records may expose only safe metadata. |

Canonical source class handling:

| Source class | Operational posture |
| --- | --- |
| `governance` | Include if accepted/current; downrank if historical/debug-only. |
| `architecture` | Include if accepted/current and within active platform scope. |
| `source` | Include metadata for approved source scopes; source body inclusion requires later gate. |
| `adoption` | Include accepted adoption decisions and blockers. |
| `closure` | Include latest accepted closure records as compact authority. |
| `execution_record` | Include only in audit profile unless still active evidence. |
| `audit_record` | Preserve for traceability; downrank outside audit profile. |

Decision marker:

`canonical_source_reference_model_defined`

## 6. GBrain Derived Index Integration Model

GBrain is the derived index provider for local semantic retrieval / local memory indexing under P12.5, subject to P12.3 authority boundaries.

GBrain roles:

| Role | P12.7 design posture |
| --- | --- |
| Derived index provider | Approved design role. |
| Keyword retrieval baseline | Default future baseline because Mode A keyword search is validated and no provider is required. |
| Local memory sandbox candidate | P12.9 may run a fresh canonical sandbox after acceptance. |
| Future optional embedding substrate | Deferred; requires Mode B/Ollama or provider gate. |
| Future optional graph substrate | Deferred; graph edges/traversal usefulness not validated. |

GBrain artifacts and authority posture:

| Artifact | Tier | Rule |
| --- | --- | --- |
| Imported pages | Tier B | Derived from approved inputs; must cite canonical refs. |
| Chunks | Tier B | Retrieval units only; not authority. |
| Keyword index | Tier B | Retrieval index only; rebuildable/disposable. |
| Search results | Tier B evidence view | Must return source refs; cannot decide. |
| Exports | Tier C | Generated evidence; not canonical even if mirroring source. |
| Graph-query output | Tier C | Generated evidence; not graph authority. |
| Future embeddings | Tier B candidate | Blocked until provider/storage gate. |
| Future graph edges | Tier B/C candidate | Blocked until graph validation gate. |

Required future design fields:

```yaml
GBrainIndexRef:
  sandbox_or_store_id: "<id>"
  gbrain_home_path: "<approved path>"
  db_path: "<approved path>"
  input_scope_manifest: "<path/ref>"
  imported_page_count: "<count>"
  chunk_count: "<count>"
  mode: "keyword_only | embedding | hybrid"
  provider: "none | ollama | hosted | unknown"
  authority_tier: "Tier B"
  rebuild_policy: "manual_gate | scheduled_gate | blocked"
  cleanup_policy: "retain | rebuild | discard | archive"
```

GBrain integration rules:

| Rule | Requirement |
| --- | --- |
| Approved sources only | Input scope must come from an accepted source manifest. |
| Derived refs only | Pages/chunks must carry CanonicalSourceRef IDs. |
| Search result citations | Search results must identify source path/slug/ref and limitations. |
| Exports non-canonical | Exports remain generated evidence until promoted by exact governance review. |
| Graph-query non-authority | Graph-query output remains generated evidence. |
| No decisions | GBrain cannot approve, reject, promote, mutate, execute, or decide. |
| Rebuildable/disposable | Index state can be discarded and rebuilt from canonical inputs. |
| Provider blocked by default | `provider: none` / `mode: keyword_only` is the default future sandbox posture. |

Decision marker:

`gbrain_derived_index_integration_defined`

## 7. Representation Model

The memory store separates references from payloads.

| Record | Contents allowed | Contents blocked |
| --- | --- | --- |
| `CanonicalSourceRef` | Path, class, status, supersession, sensitivity, cleanup action | Full blocked source bodies, secrets, credentials. |
| `DerivedPageRef` | GBrain page ID/slug, canonical source ref, import timestamp, limitations | Authority claim, approval claim. |
| `DerivedChunkRef` | Chunk ID, page ref, source span metadata, retrieval score metadata | Decision claim, unbounded source content. |
| `SearchResultRef` | Query ID, matched refs, score, source citation, freshness | Approval, mutation, runtime trigger. |
| `EvidenceRefLink` | Evidence ref, target ref, generated/audit posture, limitations | Raw generated payload, raw Graphify output, secret payload. |
| `GeneratedOutputRef` | Output class, local path/ref metadata, sensitivity, retention posture | Generated output body by default. |
| `RefreshManifestRef` | Input manifest, gate status, index state, reviewer, rollback route | Automatic execution command. |
| `OperationalMemoryProfileRef` | Profile ID, include/downrank/exclude rules, status | Raw source/materialized context by default. |

Context assembly must request refs first and only materialize content under the exact future gate applicable to that source class.

## 8. Operational Memory Profiles

### OM-0 - Audit / Full Trace Profile

Purpose: maximum traceability for governance debugging and incident review.

Includes:

| Included class | Rule |
| --- | --- |
| Canonical docs | Include accepted and historical canonical refs. |
| Debug records | Include for traceability with low decision weight. |
| Safe blocks | Include as incident/audit evidence. |
| Reruns | Include with run status and closure refs. |
| Execution records | Include accepted execution records and blockers. |
| Generated evidence metadata | Include metadata only, not raw generated payloads. |

Not for: normal agent production context or production agent taxonomy execution.

### OM-1 - Active Governance Profile

Purpose: day-to-day agent planning and governance-aware task execution.

Includes:

| Included class | Rule |
| --- | --- |
| Current accepted governance | Include active policy/design decisions. |
| Current adoption decisions | Include accepted adoption and non-adoption boundaries. |
| Current active boundary contracts | Include tool, memory, skill, approval, source, retention, rollback, incident contracts. |
| Latest closure records | Include latest explicit closures as compact authority. |
| Current roadmap | Include current roadmap refs only. |
| Selected audit records | Include only when active dependency or incident relevance exists. |

Downranks:

| Downranked class | Rule |
| --- | --- |
| Old failed runs | Keep as audit refs, not context drivers. |
| Intermediate command-prep tickets | Exclude unless active. |
| Obsolete provider branches | Exclude/downrank after supersession. |
| Duplicate rerun records | Collapse behind latest closure plus citations. |
| Sandbox outputs | Exclude raw outputs; keep safe metadata only if needed. |

### OM-2 - Production Operational Profile

Purpose: future production agent taxonomy execution on real projects.

Requires:

| Requirement | Status |
| --- | --- |
| CLEAN.R or equivalent cleanup closure | Required; not present in P12.7. |
| Compacted canonical docs | Required. |
| Debug history downranked/excluded | Required. |
| Source authority model | Required and must be current. |
| Retention/rollback policy | Required. |
| Incident handling | Required. |
| Fresh memory reindex | Required under explicit future gate. |

OM-2 is blocked now.

Decision marker:

`operational_memory_profile_defined`

## 9. Source Scope Filters

Include by default after acceptance:

| Source category | Rule |
| --- | --- |
| Accepted governance docs | Include in OM-1 and OM-2 after cleanup. |
| Accepted architecture docs | Include in OM-1 and OM-2 after cleanup. |
| Accepted adoption decisions | Include current decisions. |
| Accepted closure records | Include latest closures and supersession refs. |
| Active boundary contracts | Include as active constraints. |
| Active implementation contracts | Include current implementation boundaries. |
| Current roadmap docs | Include only if current and accepted. |
| Approved source metadata | Include metadata only unless future source-content gate allows more. |

Include only in audit profile:

| Source category | Rule |
| --- | --- |
| Safe blocks | OM-0 default; OM-1 only if active incident relevance. |
| Failed install attempts | OM-0 only unless latest accepted decision cites them. |
| Debugging reruns | OM-0 only unless active. |
| Intermediate command-prep tickets | OM-0 only unless future gate consumes them. |
| Risk records | OM-0 or OM-1 only if current boundary depends on them. |
| Tool failure records | OM-0; OM-1 only if active failure boundary. |

Exclude by default:

| Excluded category | Rule |
| --- | --- |
| `9_artifacts/**` | Generated/local-only; metadata only unless future gate. |
| `graphify-out/**` | Raw Graphify outputs; generated evidence only. |
| `node_modules/**` | Dependency material; excluded. |
| Normal user tool state | `.gbrain`, `.gstack`, provider state excluded. |
| Credentials/secrets/.env | Always excluded except explicit safe placeholder policy. |
| Provider configs | Excluded. |
| Product/Siamese source | Excluded from P12.7 memory scope. |
| Raw external source bodies | Excluded unless exact source review gate. |
| Generated exports | Excluded by default; not canonical. |
| Sandbox DBs | Excluded; no DB internals inspection. |

Filter precedence:

| Rank | Rule |
| --- | --- |
| 1 | Secrets/credentials/provider configs are blocked regardless of profile. |
| 2 | Product/Siamese source is blocked unless future product gate. |
| 3 | Generated artifacts are excluded unless exact promotion/tracking gate. |
| 4 | External source bodies are blocked unless exact source review gate. |
| 5 | Accepted canonical docs are included only under accepted/current profile rules. |
| 6 | Debug/audit history is downranked by default outside OM-0. |

Decision marker:

`memory_scope_filtering_rules_defined`

## 10. Debug History Downranking Rules

Debug history is preserved for audit but constrained in operational context.

| Rule | Requirement |
| --- | --- |
| Keep debug records for audit | Do not delete, rewrite, archive, or move records in P12.7. |
| Do not feed all debug records into operational context | OM-1 includes only active/select audit refs. |
| Preserve latest closure/adoption decision as compact authority | Closure/adoption records summarize branch outcomes. |
| Retain safe blocks as incident/audit evidence | Safe blocks explain boundaries but should not dominate planning. |
| Collapse repeated reruns | Use latest accepted closure plus references to rerun records. |
| Downrank obsolete branches | Old provider/tool branches should not appear in default agent context unless cited. |
| Preserve conflict visibility | Downranking must not hide unresolved conflicts; unresolved conflicts require reconciliation. |

Recommended future cleanup actions:

| Debug class | Cleanup action candidate |
| --- | --- |
| Safe failure records | `downrank` or `archive_candidate` after closure. |
| Empty graph-query branch records | `compact` behind P12.0E closure. |
| Intermediate command plans | `exclude` from OM-1/OM-2 unless active. |
| Duplicate rerun records | `compact` into latest closure with citations. |
| Risk reviews still active | `keep` if boundary depends on them. |

Decision marker:

`debug_history_downranking_rules_defined`

## 11. Generated Evidence Exclusion Rules

Generated evidence is excluded from operational memory by default.

| Generated class | Default rule |
| --- | --- |
| Sandbox outputs | Local/untracked generated evidence; exclude raw content. |
| GBrain exports | Not canonical even if mirroring canonical files. |
| Graph-query output | Evidence only; not graph authority. |
| Graphify outputs | Generated evidence, not source of truth, approval, or memory authority. |
| Runtime logs | Audit/debug evidence; metadata only by default. |
| Reports | Supporting evidence with citations; not authority. |
| Generated summaries | Optional convenience only; canonical source remains file. |

Promotion requirements:

| Step | Requirement |
| --- | --- |
| Exact evidence ref | Identify exact output or report. |
| Sensitivity review | Confirm no secrets/credentials/product/raw blocked content. |
| Conflict review | Compare against accepted governance and source refs. |
| Human/governance review | Required for promotion. |
| Tracking decision | Generated output tracking remains blocked unless exact gate approves. |
| Rollback/incident route | Required for promoted generated evidence. |

Decision marker:

`generated_evidence_exclusion_rules_defined`

## 12. Refresh / Reindex Lifecycle

Lifecycle states:

| State | Meaning |
| --- | --- |
| `planned` | Refresh/reindex design or manifest drafted; no execution. |
| `approved` | Exact future gate approved the refresh/reindex. |
| `indexed` | Index produced by approved run. |
| `reviewed` | Index/output reviewed for scope and safety. |
| `stale` | Source changes or policy changes make index outdated. |
| `superseded` | New accepted index/manifest replaces it. |
| `archived` | Retained as audit only. |
| `discarded` | Removed from operational consideration. |
| `blocked` | Must not run or be used. |

Allowed refresh triggers:

| Trigger | Requirement |
| --- | --- |
| Accepted governance/adoption change | Exact memory refresh gate required. |
| Accepted cleanup change | CLEAN output may trigger fresh canonical reindex. |
| Source scope change | Manifest update and human review required. |
| Memory authority model change | Re-evaluate index profile and filters. |
| Tool adoption decision | Update derived index/tool references. |
| Incident/rollback | Revoke, quarantine, or rebuild affected refs. |
| Manual human approval | Exact-scope approval only; no broad approval. |

Blocked automatic triggers:

| Trigger | Rule |
| --- | --- |
| Chat request alone | Cannot cause operational reindex. |
| New generated output alone | Cannot cause operational reindex or promotion. |
| Sandbox run alone | Cannot update operational memory. |
| External source update alone | Cannot feed memory without source/adoption gate. |
| Tool suggestion alone | Cannot trigger indexing. |

Reindex rule:

No automatic operational reindex before explicit memory integration gate.

Decision marker:

`memory_refresh_reindex_boundary_defined`

## 13. Memory Store Conflict Resolution

P12.7 reuses the P12.3 hierarchy and applies it inside memory store behavior.

Conflict hierarchy:

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

Conflict behavior:

| Conflict | Resolution |
| --- | --- |
| Derived result conflicts with canonical source | Canonical source wins. |
| Generated evidence conflicts with accepted governance | Governance wins. |
| Debug record conflicts with explicit closure | Closure wins when explicit. |
| Two canonical records conflict | Stop and request reconciliation. |
| Source metadata conflicts with governance scope | Governance scope wins. |
| GBrain graph result conflicts with keyword/canonical evidence | Canonical/accepted evidence wins; graph result remains non-authority. |
| Graphify map conflicts with GBrain retrieval | Canonical source refs decide; both outputs are supporting evidence. |

Decision marker:

`memory_store_conflict_resolution_defined`

## 14. Sandbox and Output Boundaries

P12.7 does not inspect sandbox DB internals, generated home internals, generated exports, raw Graphify outputs, or artifact contents.

Future memory sandboxes must follow these boundaries:

| Boundary | Requirement |
| --- | --- |
| Fresh sandbox | P12.9 should create/use a fresh canonical sandbox, not the noisy P12.0D sandbox as production memory. |
| Approved root | `gbrain_home_path` and `db_path` must be under an approved generated-local sandbox root. |
| Reduced manifest | Input scope manifest must be reduced to accepted canonical source refs. |
| Keyword-only default | Default future mode is `keyword_only` with `provider: none`. |
| Generated outputs local | Exports/logs/run outputs remain local/untracked unless future gate approves tracking. |
| No DB internals as context | DB files are implementation/storage, not memory authority. |
| No raw generated content import | Operational memory imports refs/metadata first, not raw outputs. |
| Rollback route | Any future indexed sandbox requires rollback and incident posture. |

## 15. CLEAN Dependency

CLEAN is required before production agent taxonomy execution on real projects.

CLEAN should later define:

| CLEAN work item | Purpose |
| --- | --- |
| Markdown inventory | Identify canonical, historical, debug, duplicate, and obsolete records. |
| Redundancy map | Find duplicate/repeated branch records. |
| Canonical vs historical classification | Separate current authority from history. |
| Debug archive/downranking | Decide what remains OM-0 only. |
| Canonical governance consolidation | Compact active authority into current refs. |
| Clean GBrain reindex | Fresh canonical index after cleanup. |
| Hermes/Paperclip/GStack memory refresh | Refresh only if future adoption decisions exist. |
| Operational readiness gate | Decide whether OM-2 can become usable. |

P12.7 does not clean anything.

Decision marker:

`cleanup_project_dependency_confirmed`

## 16. P12.9 Handoff Decision

P12.7 hands off to:

`P12.9 - Canonical Local Memory Sandbox Spike`

P12.9 prerequisites:

| Prerequisite | Requirement |
| --- | --- |
| P12.3 accepted | Memory authority model must be accepted. |
| P12.5 accepted | GBrain semantic retrieval/local memory indexing decision must be accepted. |
| P12.7 accepted | Memory store integration design must be accepted. |
| P12.11 retention/rollback | May be pending, but P12.9 must reference current retention/rollback/incident posture and not bypass it. |

P12.9 design constraints:

| Constraint | Rule |
| --- | --- |
| Fresh canonical sandbox | Do not reuse noisy P12.0D sandbox as production memory. |
| Reduced scope manifest | Use accepted canonical governance/adoption/closure/boundary refs only. |
| Keyword-only default | No embeddings/Ollama/provider unless separate gate. |
| No graph authority | Graph-query is not required for first canonical memory sandbox. |
| Metadata-first review | Review refs/counts/scope before any generated output import. |
| Generated output blocked | Exports/logs remain generated evidence. |

Decision marker:

`p12_9_canonical_memory_sandbox_ready_after_design`

## 17. GStack / Skill Relation

P12.7 does not design skill execution.

Skill memory must follow P12.4. `agent_platform_skill_authority_execution_boundary.md` is present as a read-only boundary input with `skill_authority_execution_boundary_ready`, and P12.7 consumes only its non-authority and execution-gate posture. P12.7 still avoids skill execution decisions.

GStack remains pending P12.6. P12.8 may design skill stack bootstrap, but skills cannot write memory unless a future memory write gate allows it.

| Surface | P12.7 position |
| --- | --- |
| Skill memory | Future candidate only; must follow P12.4. |
| Skill execution | Not designed or approved by P12.7. |
| GStack setup/runtime | Still blocked by P12.2. |
| GStack adoption | Deferred to P12.6. |
| Skill writes to memory | Blocked unless future exact memory write gate approves. |
| Skill reads from memory | Future design must preserve source refs, authority posture, and profile scope. |

## 18. Acceptance Criteria Mapping

| Criterion | Status |
| --- | --- |
| Creates exactly one memory store integration design file | Satisfied by this file only. |
| Uses P12.3 and P12.5 as dependencies | Satisfied. |
| Does not overrule memory authority model | Satisfied. |
| Defines canonical source reference model | Satisfied. |
| Defines GBrain derived index integration | Satisfied. |
| Defines operational memory profiles | Satisfied. |
| Defines source scope filters | Satisfied. |
| Defines debug history downranking | Satisfied. |
| Defines generated evidence exclusion | Satisfied. |
| Defines refresh/reindex lifecycle | Satisfied. |
| Defines conflict resolution | Satisfied. |
| Confirms cleanup dependency | Satisfied. |
| Hands off to P12.9 | Satisfied. |
| Does not run runtime tools | Satisfied: no GBrain/GStack/Graphify/Ollama/runtime execution. |
| Does not reindex memory | Satisfied. |
| Does not clean files | Satisfied. |
| Does not mutate Git | Satisfied. |

## 19. Created / Not Created Register

Created:

| Item | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_memory_store_integration_design.md` | Created as P12.7 memory store integration design. |

Not created / not approved:

| Item | Status |
| --- | --- |
| Memory store implementation | Not created. |
| Memory reindex | Not run. |
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

## 20. Decision Markers

memory_store_integration_design_ready

memory_store_integration_architecture_defined

canonical_source_reference_model_defined

gbrain_derived_index_integration_defined

operational_memory_profile_defined

memory_refresh_reindex_boundary_defined

memory_scope_filtering_rules_defined

debug_history_downranking_rules_defined

generated_evidence_exclusion_rules_defined

memory_store_conflict_resolution_defined

cleanup_project_dependency_confirmed

p12_9_canonical_memory_sandbox_ready_after_design

## 21. Final Verdict

P12.7 defines the memory store as a governed retrieval and context assembly layer that references canonical sources and derived indexes without becoming authority.

Canonical governance, architecture, adoption, closure, and approved source records remain outside and above the memory store as source of truth. GBrain is integrated as a derived, rebuildable, keyword-first index provider. Graphify remains generated evidence for visualization/reporting/evidence maps. GStack remains pending and non-authoritative.

Generated evidence, sandbox outputs, exports, graph-query output, raw logs, and artifact contents are excluded from operational memory by default. Debug history is retained for audit but downranked outside OM-0.

P12.9 may proceed after P12.7 acceptance to plan a fresh canonical local memory sandbox spike using a reduced scope manifest. Production operational memory remains blocked until CLEAN or equivalent cleanup closure.
