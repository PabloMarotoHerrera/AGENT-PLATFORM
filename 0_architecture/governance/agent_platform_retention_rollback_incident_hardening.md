# Retention / Rollback / Incident Hardening

## 1. Document Header

| Field | Value |
| --- | --- |
| Ticket | P12.11 |
| Title | Retention / Rollback / Incident Hardening |
| Type | Governance / hardening / retention / rollback / incident-response / no-runtime |
| Status | Drafted for acceptance |
| Target file | `0_architecture/governance/agent_platform_retention_rollback_incident_hardening.md` |
| Authority | Governance/design only. This document is not cleanup execution, rollback execution, file deletion, archive move, markdown rewrite, memory reindex, GBrain execution, GStack execution, Graphify execution, Ollama command, embedding generation, provider/API/MCP activation, skill execution, browser daemon launch, generated output tracking, sandbox output staging, dependency artifact staging, credential inspection, product/Siamese source access, DB/internal inspection, Git mutation, or production operational memory activation. |
| Result marker | `retention_rollback_incident_hardening_ready` |

## 2. Purpose

P12.11 hardens retention, rollback, incident handling, and cleanup boundaries for Project 12 after the successful P12.9 canonical local memory sandbox spike and before P12.R closure.

P12.11 defines what gets retained, what stays local/untracked, what must never be retained, what CLEAN should later downrank, how bad memory indexes are rolled back, how generated-output mistakes are handled, how credential/provider/product-source incidents are handled, how future GStack setup/runtime/skill incidents are handled, how memory contamination is handled, and what must be true before P12.R closure.

P12.11 creates policy only. It does not perform cleanup, rollback, deletion, archive movement, reindexing, staging, or source inspection.

## 3. Inputs And Dependency Status

| Dependency | Required marker/status | P12.11 status | Notes |
| --- | --- | --- | --- |
| P12.9 canonical local memory sandbox spike | `canonical_local_memory_sandbox_spike_ready` | Confirmed | Execution record exists. |
| P12.9 successful execution | `p12_9_canonical_memory_sandbox_execution_success` | Confirmed | Sandbox succeeded under controlled scope. |
| P12.9 generated exports posture | `p12_9_exports_generated_local_untracked` | Confirmed | Generated outputs remain local/untracked. |
| P12.9 no provider/embedding posture | `p12_9_no_embeddings_no_ollama_no_providers` | Confirmed | No embeddings, Ollama, or providers. |
| P12.9 no graph-query posture | `p12_9_no_graph_query` | Confirmed | No graph-query in P12.9. |
| P12.9 handoff | `p12_11_retention_rollback_ready_after_memory_spike` | Confirmed | P12.11 is ready after memory spike. |
| P12.7 memory store integration design | `memory_store_integration_design_ready` | Confirmed | Generated evidence excluded by default; CLEAN required. |
| P12.4 skill authority execution boundary | `skill_authority_execution_boundary_ready` | Confirmed | Skills not authority and require execution gates. |
| P12.6 GStack adoption decision | `gstack_adoption_decision_ready` | Confirmed | GStack read-only skill source candidate only. |
| P12.8 skill stack bootstrap design | `skill_stack_bootstrap_design_ready` | Confirmed after the file appeared in the working tree | P12.8 defines a no-runtime bootstrap path, does not require GStack setup for initial P12.10, and hands off to P12.10. |

P12.9 sandbox path metadata checked only:

| Path | Metadata status | Inspection boundary |
| --- | --- | --- |
| `9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/` | Present | Top-level metadata only. |
| `9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/gbrain_home/` | Present | Generated home internals not inspected. |
| `9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/db/` | Present | DB internals not inspected. |
| `9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/exports/` | Present | Export contents not inspected. |
| `9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/logs/` | Present | Log contents not inspected. |
| `9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/reports/` | Present | Report contents not inspected. |
| `9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/manifest/` | Present | Manifest contents not inspected. |

Top-level names observed under the P12.9 sandbox root: `db`, `exports`, `gbrain_home`, `logs`, `manifest`, `reports`.

## 4. Retention Classes

### R0 - Canonical Tracked Governance

Includes:

| Class | Examples |
| --- | --- |
| Accepted governance records | P12.2, P12.3, P12.4, P12.5, P12.6, P12.7, P12.9, P12.11 records. |
| Accepted architecture records | Architecture and memory-store design records. |
| Accepted adoption decisions | GBrain and GStack adoption decisions. |
| Accepted closure records | Future P12.R and accepted closure records. |
| Accepted boundary contracts | Skill, memory, tool, human approval, evidence bus, and runtime boundary contracts. |

Policy:

| Rule | Requirement |
| --- | --- |
| Tracked in Git | These records may be tracked as canonical governance. |
| Retained indefinitely | Retain unless superseded by accepted governance. |
| Not deleted by cleanup | CLEAN may classify and compact, not silently delete. |
| Supersession only by governance | Compaction requires accepted supersession records and citations. |

### R1 - Tracked Audit / Execution Records

Includes:

| Class | Examples |
| --- | --- |
| Accepted P12.9 execution outcome | Retained historical evidence that the controlled sandbox completed successfully. |
| Safe block records | Missing approval, blocked runtime, blocked provider, blocked setup. |
| Controlled runtime execution records | Future accepted exact execution records. |
| Installation records | Controlled install/setup records if ever approved. |
| Source review records | Accepted external source, license, trust, dependency records. |

Policy:

| Rule | Requirement |
| --- | --- |
| Tracked only if accepted | Audit/execution records are tracked only when accepted as governance evidence. |
| Retained for traceability | Retain enough to explain decisions, rollback, and incidents. |
| Downrank outside OM-0 | Do not let debug history dominate operational memory. |
| CLEAN compaction allowed | CLEAN may compact into latest closure plus citations. |

### R2 - Local Generated Evidence

Includes:

| Class | Examples |
| --- | --- |
| GBrain sandboxes | `9_artifacts/gbrain_sandbox/**`. |
| GBrain exports | Exported pages and generated markdown under sandbox outputs. |
| GBrain DBs | PGLite/DB output under sandbox roots. |
| GBrain generated homes | Generated GBrain home directories under sandbox roots. |
| Runtime logs | Local logs from controlled runs. |
| Reports | Generated reports and content-sanity reports. |
| Sandbox manifests | Generated manifests under sandbox roots. |
| Graphify outputs | `graphify-out/**` and generated graph/report artifacts. |

Policy:

| Rule | Requirement |
| --- | --- |
| Local/untracked by default | Do not stage or track generated outputs by default. |
| Not source of truth | Generated outputs cannot override canonical governance. |
| Not operational memory | Generated outputs do not feed OM-1/OM-2 unless exact future gate approves metadata/ref import. |
| Metadata only by default | Future review may record safe path/class/count metadata only. |
| Promotion requires exact gate | No automatic promotion of exports/logs/reports/DB outputs. |

### R3 - External Source Evidence

Includes:

| Class | Examples |
| --- | --- |
| GBrain source | `4_external/sources/gbrain-master/**`. |
| GStack source | `4_external/sources/gstack-main/**`. |
| Graphify source | `4_external/sources/graphify/**`. |
| Future candidate sources | Hermes, Paperclip, or other future external candidates. |

Policy:

| Rule | Requirement |
| --- | --- |
| Read-only candidate evidence | External source can inform governance under exact source review gates. |
| Not authority | External source cannot override platform governance. |
| Not executed without gate | Setup/runtime/build/test/use requires exact future gate. |
| License/trust/adoption required | Adoption is separate from source presence. |
| Dependency/runtime artifacts excluded | `node_modules`, caches, and built artifacts remain outside memory inputs. |

### R4 - Dependency / Runtime Artifacts

Includes:

| Class | Examples |
| --- | --- |
| Dependency directories | `node_modules/**`. |
| Package caches | Bun/npm/global package caches. |
| Package manager outputs | Lock/install/build side effects not accepted as governance. |
| Compiled binaries | Generated binaries or build outputs. |
| Runtime temp files | Temporary runtime output. |
| Browser state | Browser daemon state, cookies, local profiles. |
| Tool caches | GBrain/GStack/Graphify/tool caches. |

Policy:

| Rule | Requirement |
| --- | --- |
| Untracked | Do not track dependency/runtime artifacts. |
| Not memory input | Do not index or import into operational memory. |
| Safe metadata only | Governance records may retain path/class/incident metadata. |
| Exact audit gate required | Recursive inspection requires exact dependency/runtime audit gate. |

### R5 - Blocked / Sensitive Material

Includes:

| Class | Examples |
| --- | --- |
| Secrets and credentials | `.env`, `.env.*`, `credentials/**`, `secrets/**`, API keys, tokens. |
| Auth/browser state | Browser auth, cookies, local credential stores. |
| Provider configs | OpenAI, Anthropic, Gemini, Ollama, Claude, or other provider configs. |
| Normal user tool state | Normal user `.gbrain`, `.gstack`, `.claude`, `.codex`, `.config/opencode`. |
| Product/Siamese source | `2_products/**`, `product/**`, `products/**`. |

Policy:

| Rule | Requirement |
| --- | --- |
| Never retained in memory | Do not index or import. |
| Never copied into reports | Do not quote or summarize sensitive contents. |
| Never staged | Staging/tracking is an incident. |
| Incident if accessed/captured | Treat access or capture as I4/I5 depending on class. |

Decision marker:

`retention_policy_defined`

## 5. Generated Output Retention Policy

P12.9 sandbox outputs stay under:

`9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/`

Policy:

| Rule | Requirement |
| --- | --- |
| Remain local/untracked | Do not stage sandbox DBs, homes, exports, logs, reports, or manifests by default. |
| Not source of truth | Canonical governance files remain source of truth. |
| Not operational memory | P12.9 outputs are not OM-1 or OM-2. |
| Not staged | Sandbox outputs must not be staged for commit. |
| Not promoted automatically | Promotion requires exact future governance review. |
| Governance record only | The accepted P12.9 governance execution record is the trackable evidence. |

Allowed future actions:

| Action | Boundary |
| --- | --- |
| Metadata-only review | Path/class/count/tracked posture only unless exact gate expands. |
| Retention/downranking classification | CLEAN or later cleanup ticket may classify. |
| Explicit promotion of exact generated evidence | Only if needed and approved by exact governance review. |
| Explicit cleanup | CLEAN or later cleanup ticket may delete/archive/move with review. |

Blocked actions:

| Action | Reason |
| --- | --- |
| Tracking sandbox DBs | DBs are generated local evidence. |
| Tracking generated homes | Generated homes are not canonical. |
| Tracking exports by default | Exports are Tier C generated evidence. |
| Tracking logs/reports by default | Logs/reports may contain sensitive or stale context. |
| Importing generated exports into operational memory | Exports are not canonical. |
| Using exports as canonical files | Canonical source remains repo governance files. |
| Using graph/query outputs as authority | Graph/query outputs are generated evidence. |

Decision marker:

`generated_output_retention_policy_defined`

## 6. GBrain Sandbox Retention Policy

Sandbox retention posture:

| Sandbox | Classification | Retention posture |
| --- | --- | --- |
| P12.0D governance import sandbox | Historical feasibility sandbox | Archive/discard candidate after P12.R/CLEAN. |
| P12.9 canonical local memory sandbox | Current canonical local memory sandbox candidate | Temporarily retain as latest validated canonical retrieval evidence, local/untracked. |
| Future P12.9/P12.11/P12.R memory sandboxes | Future generated evidence | Disposable/rebuildable from accepted manifests. |

Policy:

| Rule | Requirement |
| --- | --- |
| Not production memory | No sandbox is production operational memory. |
| Disposable/rebuildable | Rebuild only from accepted source manifests after approval. |
| No internals by default | DB/home internals are not inspected by default. |
| Exports generated evidence | Sandbox exports are Tier C generated evidence. |
| Temporary until CLEAN/P12.R | Long-term handling is deferred. |
| Fresh reindex required for production | Future production memory requires CLEAN and fresh approved reindex, not direct P12.9 promotion. |

Expected cleanup candidates:

| Candidate | Possible future action |
| --- | --- |
| P12.0D sandbox | `archive_candidate` or `discard_candidate` after P12.R/CLEAN. |
| P12.9 sandbox | Temporary retention until P12.R/CLEAN decides. |
| Future sandboxes | Retain only exact accepted metadata unless promoted. |

Decision marker:

`gbrain_sandbox_retention_policy_defined`

## 7. Rollback Policy

### 7.1 Memory Index Rollback

If a memory index is wrong, contaminated, stale, or out of scope:

| Step | Requirement |
| --- | --- |
| Stop using index | Mark index as blocked for operational use. |
| Classify severity | Apply I0-I5 severity model. |
| Preserve governance record | Record safe metadata and decision route. |
| Avoid DB internals | Do not inspect DB internals unless exact gate authorizes. |
| No silent cleanup | Delete/discard only under future cleanup/rollback ticket. |
| Rebuild only after approval | Rebuild from accepted source manifest only after approval. |
| Do not promote exports | Exports cannot replace canonical sources. |
| Do not silently reindex | Reindex requires explicit memory integration gate. |

Decision marker:

`memory_index_rollback_policy_defined`

### 7.2 Generated Output Rollback

If generated outputs are accidentally staged/tracked:

| Step | Requirement |
| --- | --- |
| Stop | Do not commit. |
| Check status | Run `git status --short`. |
| Exact-path unstage only | If staged, unstage exact paths only after command review. |
| Remove tracking through explicit review | No broad cleanup. |
| Preserve incident record | Record path metadata, class, and severity. |
| Check sensitivity safely | Verify no secrets/product source are included using exact safe gate. |
| Avoid destructive broad commands | Do not use broad `git clean`; do not use `git add .`. |

### 7.3 GStack Setup Rollback

If future GStack setup is run under a controlled plan, rollback must define:

| Rollback field | Requirement |
| --- | --- |
| Exact state paths | All touched paths must be declared. |
| `GSTACK_HOME` path | Sandbox or approved home path required. |
| Host skill directories touched | Must be listed before setup. |
| Settings files touched | Must be listed and restorable. |
| Hooks registered | Must include unregister route. |
| Browser assets installed | Must include cleanup and credential incident route. |
| Generated files created | Must include generated-output classification. |
| Dependency artifacts created | Must include dependency cleanup plan. |
| Cleanup commands | Must be exact and reviewed before execution. |
| Manual review before deletion | Required. |
| Credential/cookie/provider incident route | Required. |

Until that plan exists, GStack setup remains blocked.

Decision marker:

`gstack_setup_rollback_policy_defined`

### 7.4 Skill Runtime Rollback

Any future skill execution must define rollback before execution:

| Rollback field | Requirement |
| --- | --- |
| File diff rollback | Exact file path rollback route. |
| Runtime output cleanup | Generated output classification and cleanup plan. |
| Memory rollback/reindex route | Memory write rollback and reindex gate. |
| Hook/settings restore route | Hook and settings restoration. |
| Browser daemon shutdown | Browser state shutdown and incident route. |
| MCP unregister route | Exact MCP unregister and config backup route. |
| Provider credential revocation route | Provider/cost/credential incident path. |
| Git revert route | Exact Git rollback route and owner. |
| Deployment rollback route | Production/deploy rollback route if applicable. |

Decision marker:

`skill_runtime_rollback_policy_defined`

## 8. Incident Severity Model

| Severity | Name | Examples | Response |
| --- | --- | --- | --- |
| I0 | Non-incident / expected limitation | Empty graph-query result, content-sanity warning, search quality limitation, large/markup-heavy file warning. | Record limitation; do not debug-chain automatically; route to CLEAN if structural. |
| I1 | Safe block | Missing approval, missing preflight, blocked runtime, blocked provider, blocked setup. | Stop before execution; record safe block; do not create generated outputs; resume only with explicit approval. |
| I2 | Boundary drift | Unapproved command attempt, source path outside allowed scope, sandbox root mismatch, unexpected generated output path, `GBRAIN_HOME` not scoped correctly. | Stop immediately; record incident; do not continue alternate commands; do not inspect sensitive contents; require hardening/review ticket. |
| I3 | Generated output contamination | Sandbox output includes unexpected source, generated output staged accidentally, export/log/report contains unexpected path classes, artifact enters memory scope without promotion. | Stop; do not commit; quarantine by non-use; record exact path metadata; review sensitivity with exact gate; rollback staging/tracking if applicable. |
| I4 | Sensitive boundary incident | Credential access, `.env` read, token/cookie capture, provider config exposure, normal user home state access, browser auth access. | Stop; do not quote secret values; do not copy content; record metadata only; require credential incident review; consider external rotation/revocation manually. |
| I5 | Product/source authority incident | Product/Siamese source accessed without gate, blocked external source body imported into memory, generated output containing product source staged/tracked, runtime modifies source outside allowed scope. | Stop; do not inspect further; record path metadata only; require source boundary incident review; do not continue P12.R until resolved. |

Decision marker:

`incident_severity_model_defined`

## 9. Incident Stop Rules

Stop immediately if any future P12 work attempts:

| Stop trigger | Severity baseline |
| --- | --- |
| Credential inspection | I4 |
| `.env` read | I4 |
| Provider key access | I4 |
| Browser cookie import | I4 |
| Normal user home state read/write | I4 |
| Product/Siamese source access | I5 |
| DB internal inspection without gate | I2/I3 |
| Generated home internal inspection without gate | I2/I3 |
| Graphify output import without gate | I3 |
| Sandbox output tracking | I3 |
| GStack setup without controlled plan | I2 |
| Skill execution without execution gate | I2 |
| MCP registration without MCP gate | I2/I4 |
| Provider call without provider gate | I2/I4 |
| Git mutation without exact human request | I2/I3 |
| `git add .` | I2/I3 |

Decision marker:

`incident_stop_rules_defined`

## 10. Credential Incident Boundary

Credential incidents are metadata-only records.

Rules:

| Rule | Requirement |
| --- | --- |
| Never quote secret values | Governance records must not include credential values. |
| Never copy sensitive content | Do not copy tokens, API keys, cookies, provider configs, browser auth, or env contents. |
| Never index credentials | Credentials must not enter GBrain, Graphify, GStack, memory store, reports, logs, or generated evidence. |
| Record path class only | Record class such as `.env`, token store, browser auth, provider config; do not inspect content. |
| Stop runtime | Do not continue runtime or alternate commands. |
| Require incident review | Explicit credential incident review required. |
| Consider manual rotation | Rotation/revocation is outside P12.11 and must be handled manually/exactly. |

Decision marker:

`credential_incident_boundary_defined`

## 11. Product / Source Incident Boundary

Product/Siamese source remains blocked unless a future exact product/source gate authorizes it.

If product source is accessed or indexed accidentally:

| Step | Requirement |
| --- | --- |
| Stop immediately | Do not inspect further. |
| Do not summarize source content | Avoid reproducing product/source details. |
| Record metadata only | Path class and incident class only. |
| Quarantine by non-use | Do not use contaminated output or index. |
| Require source boundary review | Exact review required before P12.R. |
| Block P12.R if unresolved | Do not proceed to P12.R until resolved. |

Decision marker:

`product_source_incident_boundary_defined`

## 12. Memory Contamination Boundary

Memory contamination includes:

| Contamination class | Example |
| --- | --- |
| Blocked source imported into GBrain | Product, credential, external, generated, or user-home content indexed. |
| Generated outputs treated as canonical | Exports/logs/reports used as source of truth. |
| Debug records dominate operational context | OM-1/OM-2 polluted by old failed runs or command-prep records. |
| Credentials indexed | Credential material enters GBrain/Graphify/memory store. |
| Product source indexed | Product/Siamese source enters memory without gate. |
| External source indexed without adoption | External source bodies indexed without source/adoption gate. |
| Sandbox exports imported as authority | Generated exports override canonical governance files. |

Response:

| Step | Requirement |
| --- | --- |
| Stop using contaminated index | Mark index as blocked. |
| Do not inspect internals by default | DB/export/log internals require exact gate. |
| Create incident record | Record safe metadata and severity. |
| Rebuild only after approval | Use accepted source manifest only. |
| Do not silently patch memory | Reindex/patch requires explicit gate. |
| Preserve governance boundary | Canonical governance remains authority. |

Decision marker:

`memory_contamination_incident_boundary_defined`

## 13. CLEAN Handoff

P12.11 hands off cleanup and operational readiness to:

`CLEAN - Knowledge Base Cleanup / Memory Operational Readiness`

CLEAN must later handle:

| CLEAN responsibility | Purpose |
| --- | --- |
| Markdown inventory | Identify canonical, historical, duplicate, obsolete, and debug records. |
| Canonical vs historical classification | Separate active authority from traceability history. |
| Debug/downrank/archive rules | Decide OM-0 versus OM-1/OM-2 eligibility. |
| Duplicate rerun compaction | Collapse repeated reruns into closure plus citations. |
| Large/markup-heavy governance file review | Address P12.9 content-sanity warnings structurally. |
| Obsolete provider branch downranking | Reduce stale provider-path noise. |
| Safe-block record retention | Preserve audit value without operational dominance. |
| Clean canonical reindex | Fresh GBrain index after cleanup approval. |
| OM-2 readiness | Decide whether production operational memory can become usable. |

P12.11 does not perform CLEAN.

Decision marker:

`cleanup_handoff_to_clean_defined`

## 14. P12.R Readiness Checklist

P12.R may proceed only after:

| Requirement | Status rule |
| --- | --- |
| P12.2 accepted | Required. |
| P12.3 accepted | Required. |
| P12.4 accepted | Required. |
| P12.5 accepted | Required. |
| P12.6 accepted | Required. |
| P12.7 accepted | Required. |
| P12.8 accepted or explicitly deferred | Required before closure; P12.8 readiness marker observed in P12.11 checks. |
| P12.9 accepted with successful sandbox execution | Required; P12.9 success markers confirmed. |
| P12.10 accepted or explicitly deferred based on P12.8 | Required before closure; P12.8 currently points to a no-runtime P12.10 bootstrap path. |
| P12.11 accepted | Required. |
| No unresolved I3/I4/I5 incidents | Required. |
| No sandbox outputs staged | Required. |
| No dependency artifacts staged | Required. |
| No GStack runtime accidentally enabled | Required. |
| No production memory authority claimed | Required. |
| CLEAN dependency recorded | Required; recorded by this document. |

Decision marker:

`p12_r_integration_closure_ready_after_hardening`

## 15. Created / Not Created Register

Created:

| Item | Status |
| --- | --- |
| `0_architecture/governance/agent_platform_retention_rollback_incident_hardening.md` | Created as P12.11 hardening governance file. |

Not created / not approved:

| Item | Status |
| --- | --- |
| Cleanup execution | Not performed / not approved. |
| File deletion | Not performed / not approved. |
| Archive move | Not performed / not approved. |
| Markdown rewrite | Not performed / not approved. |
| Memory reindex | Not run / not approved. |
| GBrain execution | Not run. |
| GStack execution | Not run. |
| Graphify execution | Not run. |
| Ollama command | Not run. |
| Embeddings | Not generated. |
| Provider/API call | Not performed. |
| Skill execution | Not performed. |
| MCP registration | Not performed. |
| Browser daemon | Not launched. |
| Generated output tracking | Not approved. |
| Sandbox output staging | Not performed / not approved. |
| Dependency artifact staging | Not performed / not approved. |
| Credential inspection | Not performed. |
| Product/Siamese source access | Not performed. |
| DB/internal inspection | Not performed. |
| Git mutation | Not performed. |
| `git add .` | Not recommended. |

## 16. Acceptance Criteria Mapping

| Criterion | Status |
| --- | --- |
| Creates exactly one hardening governance file | Satisfied by this file only. |
| Confirms P12.9 successful sandbox spike | Satisfied. |
| Defines retention classes | Satisfied. |
| Defines generated output retention policy | Satisfied. |
| Defines GBrain sandbox retention policy | Satisfied. |
| Defines memory index rollback policy | Satisfied. |
| Defines generated output rollback policy | Satisfied. |
| Defines GStack setup rollback policy | Satisfied. |
| Defines skill runtime rollback policy | Satisfied. |
| Defines incident severity model | Satisfied. |
| Defines incident stop rules | Satisfied. |
| Defines credential incident boundary | Satisfied. |
| Defines product/source incident boundary | Satisfied. |
| Defines memory contamination boundary | Satisfied. |
| Defines CLEAN handoff | Satisfied. |
| Defines P12.R readiness checklist | Satisfied. |
| Does not run tools | Satisfied. |
| Does not clean files | Satisfied. |
| Does not inspect sensitive contents | Satisfied. |
| Does not mutate Git | Satisfied. |

## 17. Decision Markers

retention_rollback_incident_hardening_ready

retention_policy_defined

generated_output_retention_policy_defined

gbrain_sandbox_retention_policy_defined

memory_index_rollback_policy_defined

skill_runtime_rollback_policy_defined

gstack_setup_rollback_policy_defined

incident_severity_model_defined

incident_stop_rules_defined

credential_incident_boundary_defined

product_source_incident_boundary_defined

memory_contamination_incident_boundary_defined

cleanup_handoff_to_clean_defined

p12_r_integration_closure_ready_after_hardening

## 18. Final Verdict

P12.11 defines Project 12 retention, rollback, incident handling, and CLEAN handoff policy after the successful P12.9 canonical local memory sandbox spike.

Canonical governance remains tracked authority. P12.9 sandbox outputs remain local/untracked Tier C generated evidence. GBrain sandboxes are disposable/rebuildable and not production memory. Future GStack setup, skill runtime, browser/MCP/provider/Git/memory-write surfaces require rollback and incident routes before any execution gate.

Credential incidents, product/source incidents, and memory contamination require immediate stop, safe metadata-only recording, and exact follow-up review. CLEAN remains required before production operational memory and production agent taxonomy execution.

P12.R may proceed only after P12.11 acceptance and the readiness checklist is satisfied, including no unresolved I3/I4/I5 incidents and no sandbox/dependency artifacts staged.
