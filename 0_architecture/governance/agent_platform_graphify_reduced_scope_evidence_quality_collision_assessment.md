# P10.5K-B - Graphify Reduced-Scope Evidence Quality and Collision Assessment

## Summary

P10.5K-B performed the explicitly approved, bounded, read-only assessment of the completed reduced-scope Graphify evidence and its exact 20-file source corpus. The current graph is valid JSON with 40 nodes, 33 edges, and 14 communities. Exact node IDs are unique, every edge endpoint and hyperedge member resolves, and `cluster-only` did not change topology or community assignments.

The graph remains useful as exploratory evidence, but it is not sufficiently traceable for repository-root expansion. Only 26 of 40 nodes (65%) have verified in-scope `source_file` provenance. Ten nodes (25%) omit `source_file`, four nodes (10%) cite paths outside the approved reduced corpus, and seven of 20 source files (35%) have no node representation. The known `skill_docs_release_notes_candidate` collision conflates a registry entity with a gate-map-derived artifact and is assessed S2. The generated report also exposes an absolute local path, understates weakly connected nodes relative to a links-only calculation, and does not disclose the provenance warnings.

Decision: **Outcome B - Reduced evidence usable with limitations; remediation planning required before root scope.**

Result marker:

```text
graphify_reduced_scope_evidence_quality_collision_assessment_ready
```

Outcome markers:

```text
graphify_reduced_scope_evidence_conditionally_usable
graphify_reduced_scope_material_quality_defects_present
graphify_root_scope_execution_deferred
graphify_collision_provenance_remediation_plan_required
```

## Human approval status

Explicit approval was supplied outside the ticket body for reading the exact generated outputs, reading the exact reduced source corpus, parsing and comparing the generated evidence, assessing dropped semantic entities, and creating this one governance assessment. Approval was limited to P10.5K-B and was honored.

## Dependencies reviewed

| Dependency | Required evidence | Status |
| --- | --- | --- |
| P10.5K execution record | Five required execution, graph, warning, and classification markers | Passed |
| P10.5K marker-alignment record | `graphify_p10_5k_marker_contract_alignment_ready` | Passed |
| P10.5K-A-RERUN record | Four required cluster/report/HTML/review-ready markers | Passed |
| Reduced source root | Exact approved `skills/**` corpus available | Passed |
| Required generated outputs | `graph.json`, `GRAPH_REPORT.md`, and `graph.html` readable | Passed |

The historical P10.5K-A safe-block record was not treated as a substitute for the successful P10.5K-A-RERUN record.

## Files inspected

Generated evidence inspected read-only:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.json
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/.graphify_analysis.json
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/.graphify_labels.json
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/GRAPH_REPORT.md
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.html
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/2026-07-11/graph.json
```

All 20 `.md` and `.yaml` files under the exact approved source root were inventoried. Collision assessment read the exact relevant registry, blueprint, and gate-map files. Approved dependency and output-classification governance records were inspected only as needed for dependency and authority checks.

## Files not inspected

`cost.json` was absent. No other backup file was inspected. No path outside the ticket's allowed governance records, exact generated-output set, exact backup `graph.json`, or exact reduced source root was inspected. Credentials, secrets, environment files, provider configuration, token stores, products, external sources, artifacts, other Graphify runs, `.git/**`, normal-user configuration, and blocked repository paths were not inspected.

## Commands and parsing methods used

Repository read tools, bounded `Glob`/`Grep`, and local read-only PowerShell/Python-standard-library parsing were used. Parsing remained in memory and wrote no scripts or intermediate files. JSON was parsed without normalization or repair. Static HTML was read as text; its embedded arrays were parsed without opening a browser or executing JavaScript. `git status --short` was used only to confirm worktree/index state. No Graphify or Ollama command was run.

No-runtime declaration:

```text
Graphify runtime executed: false
Ollama inference executed: false
semantic extraction executed: false
cluster-only executed: false
report generation executed: false
HTML generation executed: false
generated outputs modified: false
source corpus modified: false
Git mutated: false
```

## Generated artifact inventory

| Artifact | Present | Length | Last-write timestamp | Inspection status |
| --- | ---: | ---: | --- | --- |
| `graph.json` | Yes | 27,410 bytes | `2026-07-11T19:29:52.6976753+02:00` | Parsed read-only |
| `.graphify_analysis.json` | Yes | 6,745 bytes | `2026-07-11T19:02:01.5807986+02:00` | Parsed read-only |
| `.graphify_labels.json` | Yes | 465 bytes | `2026-07-11T19:29:52.6976753+02:00` | Parsed read-only |
| `GRAPH_REPORT.md` | Yes | 7,965 bytes | `2026-07-11T19:29:52.6732617+02:00` | Inspected read-only |
| `graph.html` | Yes | 42,093 bytes | `2026-07-11T19:29:52.6996743+02:00` | Parsed as static text |
| `cost.json` | No | N/A | N/A | Not inspected; optional artifact absent |
| `2026-07-11/graph.json` | Yes | 25,226 bytes | `2026-07-11T19:02:01.5797989+02:00` | Parsed read-only |

## Source corpus inventory

The current source corpus contains exactly 20 files: 13 `.md`, seven `.yaml`, zero `.yml`, and zero `.json`. This matches the historical terminal total of 20 documentation inputs, while clarifying that the filesystem inventory consists of mixed Markdown and YAML documents rather than 20 Markdown files.

## Graph schema overview

Actual top-level fields are:

```text
directed
multigraph
graph
nodes
links
hyperedges
built_at_commit
```

The graph is undirected and non-multigraph. Node schema uses `file_type`, not a literal `type` field. All 40 nodes have `file_type`; all 40 omit literal `type`. This is recorded as a schema dialect difference, not silently normalized. The top-level `graph.hyperedges` and top-level `hyperedges` contain equivalent group structures.

### Graph integrity table

| Metric | Expected | Observed | Status |
| --- | ---: | ---: | --- |
| Nodes | 40 | 40 | Pass |
| Edges | 33 | 33 | Pass |
| Communities | 14 | 14 | Pass |
| Exact unique node IDs | 40 | 40 | Pass |
| Exact duplicate node IDs | 0 | 0 | Pass |
| Case-insensitive ID collisions | Not specified | 2 pairs | Warning |
| Nodes without ID | 0 | 0 | Pass |
| Edges without source | 0 | 0 | Pass |
| Edges without target | 0 | 0 | Pass |
| Unresolved source endpoints | 0 | 0 | Pass |
| Unresolved target endpoints | 0 | 0 | Pass |
| Self-loops | 0 | 0 | Pass |
| Duplicate `(source,target,relation)` edges | 0 | 0 | Pass |
| Nodes without literal `type` | 0 assumed by ticket | 40 | Schema warning; `file_type` is complete |
| Nodes without `file_type` | 0 | 0 | Pass |
| Nodes without label/name | 0 | 0 | Pass |
| Nodes without community | 0 | 0 | Pass |
| Unresolved hyperedge members | 0 | 0 | Pass |

The case-insensitive pairs are `runtime_profile_s1` / `runtime_profile_S1` and `runtime_profile_s2` / `runtime_profile_S2`. They are exact-ID distinct in JSON but unsafe for consumers that compare identifiers case-insensitively.

## Node integrity results

All 40 nodes have non-empty exact IDs, labels, `file_type`, and community assignments. Exact IDs are unique. The two case-only runtime-profile pairs represent concept duplication or distinction through capitalization alone and create a portability and merge risk. Ten nodes lack `source_file`; four more cite out-of-scope governance paths.

## Edge integrity results

All 33 links have source and target IDs, and every endpoint resolves to an exact node ID. No self-loop or duplicate `(source,target,relation)` tuple was found. Confidence distribution is 28 EXTRACTED (84.8%), four INFERRED (12.1%), and one AMBIGUOUS (3.0%), matching the rounded report percentages. Edge-level provenance was not substituted for missing node-level provenance.

## Community integrity results

Community IDs are exactly `0` through `13`; every node assignment resolves. `.graphify_analysis.json` lists the same 40 node IDs in the same 14 communities. `.graphify_labels.json` contains exactly 14 labels, no missing/extra IDs, and no duplicate label names. Every node's `community_name` matches its sidecar label.

## Provenance coverage

### Provenance table

| Classification | Node count | Percentage | Affected IDs |
| --- | ---: | ---: | --- |
| Valid in-scope path | 26 | 65.0% | `skill_review_architecture`, `skill_debug_investigation`, `skill_docs_release_notes_candidate`, `blueprints_docs_release_notes_candidate_instructions`, `blueprints_docs_release_notes_candidate_skill_blueprint`, `skill_memory_update_request_instructions`, `skill_memory_update_request_gate_map`, `skill_planning_request_review_instructions`, `skill_planning_request_review_gate_map`, `runtime_profile_S1`, `runtime_profile_S2`, `memory_authority_gate_for_any_memory_write`, `git_mutation_gate_for_any_stage_commit_tag_push`, `skill_safety_command_review`, `registry_agent_platform_mvp0_static_skill_registry`, `permission_classes_allowed_now`, `permission_classes_candidate_only`, `permission_classes_blocked`, `gate_local_tool_execution_gate_for_any_command_execution`, `gate_hook_registration_gate_for_any_enforcement_hook`, `gate_settings_mutation_gate_for_any_settings_change`, `memory_posture_no_memory_write`, `output_class_review_support`, `skill_planning_request_review`, `skill_architecture_review`, `skill_memory_update_request` |
| Missing field | 10 | 25.0% | `runtime_profile_s1`, `runtime_profile_s2`, `output_posture_review_support`, `output_posture_command_candidate`, `permission_class_read_docs`, `permission_class_write_memory`, `skill_family_implementation_review_debug`, `SKILL_READ_DOCS`, `SKILL_WRITE_MEMORY`, `SKILL_MUTATE_GIT` |
| Path outside approved source root | 4 | 10.0% | `0_architecture_governance_agent_platform_skill_stack_bootstrap_design`, `skill_authority_execution_boundary`, `gstack_adoption_decision`, `retention_rollback_incident_hardening` |
| Null | 0 | 0.0% | None |
| Empty string | 0 | 0.0% | None |
| Non-string | 0 | 0.0% | None |
| In-scope-looking nonexistent path | 0 | 0.0% | None |
| Ambiguous relative path | 0 | 0.0% | None |
| Generated-output path | 0 | 0.0% | None |

Verified provenance coverage is therefore 65%; 35% of nodes lack valid reduced-corpus provenance. Out-of-scope references were not followed and were not treated as verified source evidence.

## Missing or invalid source_file register

The ten missing-field nodes span concept nodes in communities 0, 1, 4, 6, 10, and 11. They cover runtime profiles, output postures, permission classes, and a taxonomy concept. Candidate provenance may be suggested by incident edges, but no candidate is promoted to verified provenance. The four out-of-scope governance-document nodes are internally connected and report-visible, but their content was outside this ticket's source-corpus authority and was not inspected.

## Historical/current warning reconciliation

The historical execution evidence records 30 extraction-quality issues, three cross-chunk ID collisions, dropped duplicates, and missing `source_file`. The later `cluster-only` terminal evidence records 10 current validation issues and visibly identifies missing `source_file` on `runtime_profile_s1`. The current graph contains exactly 10 nodes with no `source_file`, which is consistent with that visible current warning category.

`.graphify_analysis.json` contains community, cohesion, god-node, surprise, and token data; it does not contain a register of the historical 30 or current 10 validation issues. Direct one-to-one reconciliation is therefore unavailable. The relationship is classified as **different validator or validation stage, with insufficient retained issue detail to reconcile individual findings**. The three collision warnings are extraction-stage events; the 10 current warnings align with current node-schema validation. The historical 30 must remain preserved.

Required boundary statement:

```text
A lower reported issue count does not by itself establish that issues were fixed.
```

No conclusion is made that 20 issues were remediated, deduplicated, or otherwise resolved.

## Known collision summary

### Collision table

| Collision ID | Source files | Surviving provenance | Collision class | Severity | Material loss | Recommended treatment |
| --- | --- | --- | --- | --- | --- | --- |
| `runtime_profile_S2` | safety blueprint; docs-release blueprint | docs-release blueprint | Deliberate shared-profile alias | S1 | Minor provenance ambiguity; both incident relationships remain | Use an explicit shared profile entity plus source assertions; path-qualify document entities, not the shared profile |
| `skill_debug_investigation` | registry; debug blueprint | debug blueprint | Deliberate alias for one skill | S1 | Minor multi-source provenance loss; registry and blueprint relationships remain | Separate canonical skill identity from registry-entry and blueprint-document IDs |
| `skill_docs_release_notes_candidate` | registry; docs-release gate map | docs-release gate map | Overlapping but materially different artifact roles | S2 | Provenance and entity-role conflation | Namespace registry entry, blueprint document, and gate-map document before any larger run |

Path-qualified IDs would have prevented all three extraction collisions mechanically. Per-subfolder extraction would likely preserve separate local entities, but a merge would still require deterministic namespacing and an explicit alias/canonical-entity policy; per-subfolder extraction alone is not sufficient.

## Collision assessment — runtime_profile_S2

The surviving exact node is `runtime_profile_S2`, label `Runtime Profile S2`, `file_type=concept`, community 1 (`Memory and Git Permissions`), with provenance `blueprints/docs-release-notes-candidate/skill.blueprint.yaml`. It is targeted by an `implements` edge from the docs-release blueprint and another from the safety-command-review skill, with each edge retaining its own source file.

Both source blueprints explicitly declare `runtime_profile: S2`. The collision is therefore a deliberate alias to a shared profile concept rather than two materially different profile definitions. Dropping one duplicate loses multi-source node provenance but does not remove either observed relationship. Severity is S1. A path-qualified ID would prevent collision but could incorrectly duplicate a shared concept unless paired with a canonical profile identity. Namespaced document nodes plus a shared profile node is preferable future-ticket input.

## Collision assessment — skill_debug_investigation

The surviving node is `skill_debug_investigation`, label `Debug Investigation Skill Blueprint`, `file_type=document`, community 0 (`Platform Architecture Governance`), with provenance `blueprints/debug-investigation/skill.blueprint.yaml`. It has a registry `contains_entry_for` relationship plus blueprint-derived reference, runtime-profile, and taxonomy relationships.

The registry entry and blueprint describe the same skill but are distinct source artifacts and roles. The current graph preserves relationships from both and uses blueprint provenance on the node. This is a deliberate alias collision with minor multi-source provenance loss, severity S1. A future schema should model canonical skill, registry entry, and blueprint document separately, with explicit relations. Per-subfolder extraction is likely to preserve both source-local entities only if merge-time namespacing prevents recurrence.

## Collision assessment — skill_docs_release_notes_candidate

The surviving node is `skill_docs_release_notes_candidate`, label `Docs Release Notes Candidate Skill Blueprint`, `file_type=document`, community 0 (`Platform Architecture Governance`), with provenance `blueprints/docs-release-notes-candidate/gate_map.md`. It receives a registry `contains_entry_for` edge and has one gate-map-derived ambiguous governance reference. A separate node, `blueprints_docs_release_notes_candidate_skill_blueprint`, already represents the actual blueprint YAML in community 1.

The registry skill identity, gate-map document, and blueprint document overlap but are materially different artifact roles. Labeling a gate-map-sourced node as a skill blueprint while attaching the registry entry conflates those roles. This creates provenance ambiguity and can distort report entities and communities even though no edge endpoint is unresolved. Severity is S2. Path-qualified artifact IDs plus a canonical skill ID would prevent the collision and preserve traceability. Per-subfolder extraction plus a namespaced merge is likely to preserve the artifacts; unqualified merge is not.

## Source-file representation coverage

Representation means at least one node has the exact valid source path. It does not establish complete concept extraction. No file was represented only by edge provenance.

### Source coverage table

| Source file | Represented | Traceable | Collision affected | Notes |
| --- | --- | --- | --- | --- |
| `README.md` | No | No | No | No node representation |
| `blueprints/architecture-review/gate_map.md` | No | No | No | No node representation |
| `blueprints/architecture-review/instructions.md` | No | No | No | No node representation |
| `blueprints/architecture-review/skill.blueprint.yaml` | Yes | Yes | No | One node; also edge provenance |
| `blueprints/debug-investigation/gate_map.md` | No | No | No | No node representation |
| `blueprints/debug-investigation/instructions.md` | No | No | No | No node representation |
| `blueprints/debug-investigation/skill.blueprint.yaml` | Yes | Yes | Yes | Surviving provenance for `skill_debug_investigation` |
| `blueprints/docs-release-notes-candidate/gate_map.md` | Yes | Yes, with conflation | Yes | S2 collision role conflation |
| `blueprints/docs-release-notes-candidate/instructions.md` | Yes | Yes | No | One node |
| `blueprints/docs-release-notes-candidate/skill.blueprint.yaml` | Yes | Yes | Yes | Three nodes; S2 profile alias collision participant |
| `blueprints/memory-update-request/gate_map.md` | Yes | Yes | No | Two nodes |
| `blueprints/memory-update-request/instructions.md` | Yes | Yes | No | One node |
| `blueprints/memory-update-request/skill.blueprint.yaml` | Yes | Yes | No | One node |
| `blueprints/planning-request-review/gate_map.md` | Yes | Yes | No | One node |
| `blueprints/planning-request-review/instructions.md` | Yes | Yes | No | One node |
| `blueprints/planning-request-review/skill.blueprint.yaml` | No | No | No | No node representation |
| `blueprints/safety-command-review/gate_map.md` | Yes | Yes | No | Four nodes |
| `blueprints/safety-command-review/instructions.md` | No | No | No | No node representation |
| `blueprints/safety-command-review/skill.blueprint.yaml` | Yes | Yes | Yes | Five nodes; S2 profile alias collision participant |
| `registry/skill_registry.yaml` | Yes | Yes, with aliases | Yes | Four nodes; two known skill-ID collisions involve registry entries |

Totals: 20 source files; 13 represented; seven unrepresented; 65.0% file representation. Five files participate in known collision pairs. Files represented only through nodes without valid provenance cannot be verified as represented and are not counted.

## GRAPH_REPORT.md consistency assessment

### Report consistency table

| Report claim | Graph evidence | Assessment |
| --- | --- | --- |
| 40 nodes, 33 edges, 14 communities | Exact current JSON counts | Supported |
| 85% EXTRACTED, 12% INFERRED, 3% AMBIGUOUS | 28/33, 4/33, 1/33 | Supported after rounding |
| 14 community names | Labels and node assignments match all 14 | Supported |
| Largest shown communities are 9, 7, 7, 4, 3 nodes | Current community counts | Supported |
| God-node ordering and displayed degrees | Consistent with analysis sidecar; degree semantics may include grouped relationships | Supported by sidecar; partially independently verifiable |
| 19 isolated nodes defined as <=1 connection | Links-only degree calculation finds 23 nodes at degree <=1, including eight degree-zero nodes | Partially supported; counting method is not disclosed and does not match links-only topology |
| Nine thin communities omitted | Nine communities have fewer than three nodes | Supported |
| Token cost 0 input / 0 output | Analysis sidecar retains 14,259 input / 4,194 output from extraction; cluster-only report may mean current-stage tokens | Partially supported; stage scope is ambiguous |
| Corpus stats unavailable in cluster-only mode | Report contains no corpus inventory | Supported |
| Reported source scope | Absolute run root shown; reduced input root not identified | Incomplete |
| Quality warnings | Provenance gaps and collision history absent | Unsupported as a quality summary |

The report does not explicitly promote Graphify to authority, source of truth, approval mechanism, operational memory, or runtime substrate. It does contain imperative suggestions to run Graphify commands, but these are report-generated navigation suggestions and confer no authority. The absolute local Windows run path in the title is a path-disclosure/classification defect.

## Community-label assessment

All 14 communities have unique labels and every graph node uses the matching label. Most labels are clear or acceptable relative to their members. Singleton labels are necessarily low-evidence. `Platform Architecture Governance` is potentially misleading because the community mixes skill artifacts, runtime-profile/taxonomy concepts, and four out-of-scope governance-reference nodes. `Memory and Git Permissions` is acceptable but includes collision-affected `runtime_profile_S2`. No label is regenerated or promoted as authoritative.

## graph.html structural assessment

Static parsing found 40 embedded node records, 33 embedded edge records, and 14 legend entries. Every embedded edge endpoint resolves. Exact node IDs are 40, while a case-insensitive consumer would collapse the two runtime-profile case pairs to 38 keys. Community labels and counts are embedded and match the graph.

The HTML references one external network resource, `https://unpkg.com/vis-network@9.1.6/standalone/umd/vis-network.min.js`; no request was made. It embeds an absolute local Windows path in the title. No blocked repository path, credential, secret, `.env` path, or provider token was found by the bounded static check. The structural representation is complete, but it is not self-contained and exposes local path information.

## Backup graph comparison

The permitted backup contains 40 nodes and 33 edges. Compared with the current graph:

```text
node IDs added: 0
node IDs removed: 0
edges added: 0
edges removed: 0
community assignments changed: 0
community_name fields added or changed: 40
```

`cluster-only` changed community-name/reporting metadata, not topology or numeric community assignments. The current `built_at_commit` differs from the backup value, but no source or topology delta resulted. No other backup file was inspected.

## Cost/provider evidence

`cost.json` is absent, which is not a failure. `.graphify_analysis.json` records 14,259 input and 4,194 output tokens but contains no backend or billing fields. Local Ollama/qwen3.5 and no-hosted-provider claims therefore remain supported by the approved runtime governance evidence, not independently established by a cost sidecar in this assessment.

## Authority and evidence classification

The outputs remain raw generated evidence: content-assessed but completeness-limited, provenance-limited, collision-affected, local, untracked, and non-authoritative. This assessment does not promote them to operational memory, semantic retrieval authority, GBrain import material, Cognitive Semantic System substrate, approval mechanism, or source of truth.

## Measured defects

| Defect | Measured evidence | Impact |
| --- | --- | --- |
| Missing node provenance | 10/40 nodes omit `source_file` | 25% cannot be directly traced |
| Out-of-scope node provenance | 4/40 nodes cite `0_architecture/**` outside the reduced corpus | 10% cannot be verified within ticket scope |
| Source coverage gap | 7/20 source files have no node representation | 35% file-level gap |
| Material collision | `skill_docs_release_notes_candidate` conflates registry and gate-map roles | S2 provenance/entity-role ambiguity |
| Case-only IDs | Two runtime-profile pairs differ only by capitalization | Consumer and merge portability risk |
| Report weak-node mismatch | Report says 19; links-only degree <=1 count is 23 | Report method/claim is not fully reproducible |
| Report warning omission | Collision/provenance warnings absent | Readers may overestimate traceability |
| Local path disclosure | Report and HTML contain absolute run path | Portability and privacy/classification defect |
| External HTML dependency | One unpkg CDN script reference | Visualization is not self-contained/offline-safe |

## Inferred root-scope risks

### Root-scope risk table

| Risk | Measured evidence | Expected amplification | Severity | Mitigation required |
| --- | --- | --- | --- | --- |
| ID collisions | Three historical collisions in 20 files; two case-only pairs remain | More repeated names and shared concepts increase collision probability | High | Namespaced artifact IDs and canonical concept policy |
| Missing provenance | 14/40 nodes lack valid in-scope provenance | More chunks and concept nodes likely increase untraceable evidence | High | Make valid `source_file` mandatory and validate before merge |
| Chunk-boundary effects | Cross-chunk drops occurred in 3/3 extraction context | Larger corpus creates more boundaries and order-dependent survivors | High | Per-subfolder extraction trials and deterministic merge design |
| Duplicate filenames | Repeated `instructions.md`, `gate_map.md`, and `skill.blueprint.yaml` exist | Root scope contains many more repeated basenames | High | Path-qualified document identity |
| Registry/blueprint overlap | Two known collisions involve registry aliases | More registries/manifests will conflate entity and artifact roles | High | Separate canonical entities from source artifacts |
| Report traceability | Warning omission, 65% valid node provenance, weak-node mismatch | Larger reports become harder to audit | High | Provenance and validation sections in report contract |
| Community-label reliability | Labels map correctly but collision/out-of-scope nodes shape communities | Larger noisy topology can produce plausible but misleading labels | Medium | Quality gate before labeling; retain member evidence |
| Cost and duration | Reduced extraction used 14,259/4,194 tokens; no cost sidecar | Root scope is expected to require materially more local inference time | Unknown/medium | Bounded pilots, checkpoints, retained cost/runtime evidence |
| Failure recovery | Backup preserved topology; historical collisions dropped nodes | Larger runs increase restart/partial-output complexity | High | Atomic outputs, chunk manifests, resumable deterministic merge |

Measured defects are those directly listed in this record. Amplification statements are reasonable inferences from repetition and scale, not measured root-scope outcomes. Exact root-scope collision rate, runtime, resource use, and label quality remain unknown.

## Unknowns

- The exact 30 historical issue records were not retained in the inspected sidecars.
- The exact validator implementation and deduplication rules producing the current count of 10 are not evidenced here.
- Whether dropped duplicate payloads contained fields not represented by surviving nodes or edges cannot be fully reconstructed.
- Full concept-level recall cannot be inferred from file-level representation.
- Root-scope token volume, duration, memory pressure, failure rate, and collision rate remain unmeasured.
- Per-subfolder extraction plus merge is promising but remains untested and unauthorized in this ticket.

## Root-scope readiness decision

The reduced graph is technically valid but insufficiently traceable for root-scope expansion. Outcome A is prohibited by the S2 collision, substantial provenance deficit, out-of-scope path inclusion, report limitations, and case-sensitive identity risk. Outcome C is not selected because topology is internally valid, all endpoints resolve, communities and labels are consistent, HTML structurally represents the graph, and 65% of nodes retain verified in-scope provenance. Outcome D is not selected because dependencies and authorized content review passed.

Repository-root execution is deferred. Future planning should specify path-qualified artifact identities, canonical entity/alias handling, mandatory provenance, deterministic merge behavior, warning retention, and a bounded per-subfolder trial before any root-scope extraction.

## Outcome classification

```text
Outcome B - Reduced evidence usable with limitations; remediation planning required before root scope
```

```text
graphify_reduced_scope_evidence_conditionally_usable
graphify_reduced_scope_material_quality_defects_present
graphify_root_scope_execution_deferred
graphify_collision_provenance_remediation_plan_required
```

## Selected next ticket

```text
P10.5K-C - Graphify Reduced-Scope Collision and Provenance Remediation Plan
```

P10.5K-C may design but must not silently execute namespacing, prompt/schema changes, source repair, extraction, per-subfolder runs, merge, report regeneration, or root-scope Graphify work.

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_graphify_reduced_scope_evidence_quality_collision_assessment.md
```

Modified:

```text
none
```

Not created or executed:

```text
no new graph
no extraction
no clustering
no community relabeling
no report regeneration
no HTML regeneration
no collision repair
no provenance repair
no per-subfolder run
no merge-graphs
no root-scope run
no hosted-provider call
no model invocation
no generated-output staging
no Git mutation
```

## Limitations

This assessment is bounded to the authorized generated files, exact backup `graph.json`, approved governance dependencies, and exact reduced source corpus. It does not validate sources outside that corpus, reconstruct dropped node payloads, measure semantic recall, execute visualization code, make network requests, or prove how defects will behave at root scope. No remediation was performed.

## Commit commands

If this assessment is accepted, stage only this record:

```powershell
git status --short

git add 0_architecture/governance/agent_platform_graphify_reduced_scope_evidence_quality_collision_assessment.md

git commit -m "Assess Graphify reduced-scope evidence quality"

git push
```

Do not use `git add .`. Do not stage `graphify-out/**`, `.opencode/**`, `AGENTS.md`, the command-candidate confirmation file, or the historical safe-block completion record.
