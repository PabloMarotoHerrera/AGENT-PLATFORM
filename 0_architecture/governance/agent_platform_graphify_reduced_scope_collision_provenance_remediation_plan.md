# P10.5K-C - Graphify Reduced-Scope Collision and Provenance Remediation Plan

## Summary

P10.5K-C selects a planning-only remediation architecture for the collision, provenance, coverage, and validation-accounting defects measured by P10.5K-B. The preferred architecture is **Partitioned Provenance-Safe Graph Build**, using per-file extraction as the selected partition unit, deterministic source-qualified node IDs, strict provenance enforcement, endpoint rewriting, validation before merge, and clustering/report generation only after global integrity gates pass.

Native `merge-graphs` is **unproven pending pilot**. Graphify 0.9.5 help documents a multi-graph merge interface and output option, but does not document collision handling, provenance retention, endpoint rewriting, merge-order independence, or silent-drop prevention. Native merge alone is therefore insufficient. The fallback is a federation of independently validated, unmerged partition graphs with a federation manifest; it must never be represented as one global Graphify graph.

The repository-wide Markdown cleanup has completed successfully. One final local root-scope Graphify extraction is authorized for P10.6 as an exploratory, non-authoritative evidence refresh. The provenance-safe pilot is not a prerequisite for generating that evidence map, but remains mandatory before any operational import, authority promotion, GBrain ingestion, semantic-memory use, or Cognitive Semantic System adoption. This plan itself performs no implementation or runtime work.

Result marker:

```text
graphify_reduced_scope_collision_provenance_remediation_plan_ready
```

## Human approval status

Explicit approval was supplied outside the original ticket body for a planning-only review, bounded CLI-help inspection, read-only inspection of the approved governance records and exact reduced source corpus, and creation of exactly this remediation plan. The later repository-wide cleanup decision completed the documentation prerequisite and now authorizes one local exploratory root-scope Graphify extraction for P10.6. It does not authorize Ollama, operational import, output promotion, GBrain ingestion, semantic-memory use, Cognitive Semantic System adoption, or Git mutation.

## Dependencies reviewed

| Dependency | Required result | Status |
| --- | --- | --- |
| P10.5K-B assessment | Outcome B | Passed |
| P10.5K-B markers | Four remediation-required markers | Passed |
| P10.5K execution record | Reduced extraction and warning baseline | Passed |
| P10.5K marker alignment | Compatibility contract | Passed |
| Historical P10.5K-A safe block | No runtime consumed | Reviewed |
| P10.5K-A-RERUN | `p10_5k_b_reduced_scope_quality_review_ready` | Passed |
| Graphify evidence classification | Generated evidence remains non-authoritative | Preserved |

P10.5K-B established valid topology but Outcome B due to material traceability defects. No dependency contradiction was found.

## Files inspected

Read-only planning inputs:

```text
.graphifyignore
.gitignore
3_platform/_governed_skeleton/agent_platform_mvp0/skills/**
```

The exact reduced corpus inventory contains 20 files: 13 Markdown and seven YAML. It has eight leaf locations: corpus root, registry, and six skill blueprint package directories. The repeated basenames `gate_map.md`, `instructions.md`, and `skill.blueprint.yaml` each occur six times.

Generated Graphify output contents were not inspected.

## Commands run

Only the approved interface-discovery commands were run:

```powershell
graphify --version
graphify --help
graphify extract --help
graphify merge-graphs --help
graphify cluster-only --help
```

Observed version:

```text
graphify 0.9.5
```

The top-level help documented the command signatures. Each subcommand-help invocation returned only `Run 'graphify --help' for full usage.` No extraction, merge, cluster, label, export, update, query, model, test, build, or Git mutation command ran.

No-runtime declaration:

```text
Graphify runtime executed: false
Ollama inference executed: false
semantic extraction executed: false
merge executed: false
cluster-only executed: false
generated outputs inspected: false
generated outputs modified: false
source corpus modified: false
implementation created: false
Git mutated: false
```

## Measured defect baseline

P10.5K-B remains the accepted measurement authority for this plan:

| Defect domain | Measured baseline |
| --- | --- |
| Topology | 40 nodes, 33 edges, 14 communities; all endpoints resolve |
| Exact identity | No exact duplicate final IDs; three extraction-time cross-chunk collisions dropped second nodes |
| Case portability | Two runtime-profile ID pairs differ only by case |
| Provenance | 26/40 nodes valid in-scope; 10 missing `source_file`; four out of scope |
| Coverage | 13/20 source files represented; seven unrepresented |
| Material collision | `skill_docs_release_notes_candidate` classified S2 |
| Warning accounting | Historical 30 and current 10 cannot be directly reconciled |
| Post-cluster topology | No node, edge, or numeric-community assignment change |

These defects are independent. Valid topology does not establish sufficient traceability.

## Identity-collision problem statement

Model-generated semantic IDs are not globally safe identifiers. The reduced run produced the same raw IDs from different source artifacts, dropped second nodes, and conflated canonical concepts with registry, blueprint, or gate-map document roles. Repeated basenames and registry/blueprint overlap enlarge this collision domain. Survivor selection may depend on chunk or merge ordering.

The remediation contract must preserve every source-local node before any optional semantic aliasing. Silent first-wins and second-wins behavior is prohibited.

## Provenance problem statement

Fourteen of 40 nodes lacked valid in-scope provenance. Without one exact authorized source per source-qualified node, evidence cannot be safely audited, replaced incrementally, namespaced, or merged. Edge provenance cannot silently substitute for node provenance.

Missing provenance may be injected **only from deterministic single-source context**. It may never be guessed from labels, IDs, neighboring nodes, or first matching paths.

## Coverage problem statement

Seven of 20 files had no traceable node representation. The prior run cannot distinguish legitimate zero-entity output from skip, failure, collision loss, merge/conflation, or missing provenance. Future coverage must be file-manifest driven and terminal-state complete, not inferred from aggregate Graphify detection counts.

## Warning-accounting problem statement

The historical extraction reported 30 issues; later cluster validation reported 10. Those are not evidence of remediation because validator, stage, scope, and deduplication semantics were not retained. Future processing requires one canonical issue ledger with stage-specific counts and stable issue identities.

## Graphify native capability boundary

Documented CLI interfaces in Graphify 0.9.5 are limited to:

```text
extract <path> --out DIR --no-cluster
merge-graphs <g1> <g2> [additional graph inputs] --out <path>
cluster-only <path> --graph <path> --no-label --no-viz and labeling controls
```

The help does not establish:

```text
that extract accepts a single file rather than a directory
that merge namespaces duplicate IDs
that duplicate entities are preserved
that edge endpoints are rewritten after ID changes
that source_file is retained or enforced
that merge order is irrelevant
that collision warnings are machine-readable
that no node is silently dropped
```

CLI presence is interface evidence only. Installed package source was not inspected, and undocumented semantics are not assumed. Native `merge-graphs` is **unproven pending pilot** and cannot be the sole remediation mechanism.

## Remediation options

### Option A - Single root extraction with current behavior

Authorized once for the final P10.6 exploratory evidence refresh after repository-wide Markdown cleanup. It retains the measured collision/provenance failure modes while expanding their domain, so its outputs must remain local, untracked, content-unvalidated, completeness-unvalidated, provenance-limited, collision-affected, and non-authoritative. Completion cannot satisfy any operational-readiness or promotion gate.

### Option B - Per-subfolder extraction plus native merge only

Deferred as unverified and insufficient by itself. Partitioning reduces collision domains, but native help provides no preservation, namespacing, provenance, rewrite, or order-independence guarantees.

### Option C - Partition plus deterministic namespace/provenance adapter

Selected. Every source is manifest-addressed; source-local extraction is validated; provenance is enforced; IDs become source-qualified; endpoints are rewritten; collisions and coverage enter explicit ledgers; only validated partitions may merge; final clustering/reporting occurs after global validation.

### Option D - Federated graphs without physical merge

Retained as fallback. Each partition remains an independently validated graph, and a federation manifest records membership and cross-partition references. No physical global graph or global Graphify authority is implied.

## Decision matrix

| Option | Collision safety | Provenance safety | Native-only | Root-scale suitability | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| Single root extraction | Low | Low | Yes | Exploratory evidence map only | Authorize once for P10.6; reject for operational use |
| Partition + native merge only | Unknown | Medium | Yes | Unproven | Defer |
| Partition + namespace/provenance adapter | High when validated | High when validated | No | Preferred | Select |
| Federated unmerged graphs | High | High | Partially | Viable fallback | Retain |

## Selected architecture

Selected architecture: **Partitioned Provenance-Safe Graph Build**.

Required future stages, in order:

1. Authorized source manifest.
2. Deterministic per-file partition selection.
3. Per-partition Graphify extraction.
4. Partition-local schema validation.
5. Provenance enforcement.
6. Deterministic ID namespacing.
7. Edge endpoint rewriting.
8. Collision detection and ledger update.
9. Validated graph merge.
10. Global integrity validation.
11. Community clustering and labeling.
12. Report and HTML generation.
13. Evidence classification and publication-boundary review.

No stage is executed by P10.5K-C.

## Fallback architecture

If a physical merge cannot demonstrate preservation and order independence, retain one validated graph per source partition. A deterministic federation manifest maps partition IDs, source IDs, graph locations, validation status, and explicit cross-partition reference records. Queries across partitions require a future separately governed evidence layer. Federated output must not be called one merged Graphify graph and must remain non-authoritative.

## Source manifest design

The future manifest contains exactly one entry for every authorized source file:

| Field | Contract |
| --- | --- |
| `source_id` | Deterministic identifier derived from normalized repo-relative path |
| `repo_relative_path` | Original reviewable repository-relative path |
| `normalized_path` | Separator- and dot-segment-normalized canonical path |
| `extension` | Normalized lowercase extension |
| `partition_id` | Deterministic partition key |
| `content_class` | Registry, blueprint, instructions, gate map, or corpus documentation |
| `processing_status` | One controlled terminal-state vocabulary |
| `extraction_output` | Future partition artifact reference, never authority |
| `entity_count` | Validated source-local node count |
| `edge_count` | Validated source-local edge count |
| `provenance_status` | Complete, deterministically injected, invalid, or blocked |
| `collision_status` | None, recorded, reviewed, or unresolved |
| `validation_status` | Passed, failed, quarantined, or blocked |

Allowed processing statuses are `pending`, `processed_with_entities`, `processed_zero_entities`, `failed`, `blocked`, and `excluded_by_policy`. Every authorized file must end in exactly one terminal status. Hashing may shorten a namespace only when the original path remains recoverable and collision-checked.

## Partition strategy

Explicit selection: **per-file extraction**.

Comparison:

| Strategy | Strength | Defect |
| --- | --- | --- |
| One file per partition | Deterministic provenance; smallest collision domain | Single-file CLI support is not documented and must be established by the pilot architecture |
| One leaf directory | Keeps each skill package together | Six package leaves contain three files each, so omitted provenance remains ambiguous |
| One skill package | Preserves package context | Same multi-source ambiguity and repeated artifact roles |
| One top-level category | Fewer runs | Registry/blueprint overlap and larger collision domain |

Per-file extraction is selected because provenance correctness outranks run-count convenience. If Graphify does not natively accept a file path, P10.5K-D must design a controlled, reviewable single-source partition mechanism before runtime; it must not silently fall back to a multi-file partition. Leaf-directory extraction may be used only where Graphify demonstrably emits valid per-file provenance for every node and all validation gates pass. This conditional exception does not change the selected default.

The registry, debug blueprint, docs-release gate map, docs-release blueprint, and safety blueprint remain separate provenance domains.

## Node-ID namespace contract

Canonical source-local global ID:

```text
<source_namespace>::<local_node_id>
```

`source_namespace` is deterministically and reversibly derived from normalized repository-relative source path. Example:

```text
blueprints/docs-release-notes-candidate/skill.blueprint.yaml::skill_docs_release_notes_candidate
registry/skill_registry.yaml::skill_docs_release_notes_candidate
```

Requirements:

```text
globally unique under exact and case-insensitive comparison
stable when source path and local ID are unchanged
reversible to the source manifest entry
independent of chunk and merge ordering
safe for endpoint rewriting
validated for delimiter escaping and length
```

Canonical multi-source concepts may later receive separately governed alias entities, but source-qualified nodes must remain. Label or raw-ID equality alone cannot authorize semantic merge.

## Provenance enforcement contract

Accepted provenance requires a non-empty string resolving to exactly one existing authorized source path within scope.

Deterministic injection answer:

```text
only from deterministic single-source context
```

When injection is authorized, add:

```text
provenance_origin: deterministic_partition_context
```

If a partition contains multiple possible sources and Graphify omits provenance, validation fails. Missing, empty, null, non-string, nonexistent, generated-output, absolute-local, out-of-scope, blocked, or ambiguous paths are rejected or quarantined. Invalid nodes cannot enter merge. Source paths are normalized for comparison without overwriting the original evidence value in an unreviewed artifact.

## Edge-rewrite contract

For every partition, construct an explicit mapping from `(source_namespace, local_node_id)` to canonical namespaced ID. Rewrite both endpoints atomically from that mapping. Validate that:

```text
every source resolves
every target resolves or has an explicit cross-partition state
no stale local endpoint remains
no endpoint resolves by first-match behavior
rewriting is deterministic and idempotent
edge provenance remains attached
```

Cross-file targets may be resolved only to an exact namespaced node through a manifest-backed rule, preserved as an unresolved external-reference record, or rejected. Similar labels and unqualified IDs are insufficient for selection. Dangling edges cannot enter a merged graph.

## Collision ledger design

The machine-readable ledger records:

```text
raw_node_id
source_namespaces
candidate_nodes
semantic_comparison_status
collision_classification
severity
selected_treatment
information_preserved
information_rejected
review_status
```

Allowed treatments are `preserve_as_distinct_namespaced_nodes`, `declare_explicit_alias`, `merge_after_human_review`, `reject_invalid_duplicate`, and `quarantine_unresolved`. No automatic semantic merge is permitted solely from ID or label equality. Every drop must be explicit, reviewed, and ledgered; silent drops are forbidden.

## Coverage ledger design

Each manifest source receives one coverage outcome:

```text
represented_by_traceable_nodes
processed_zero_entities_confirmed
represented_only_by_relationships
failed_extraction
lost_or_ambiguous_due_to_collision
missing_provenance
not_processed
```

Zero entities is acceptable only when extraction completed, zero is explicitly recorded, and no truncation/failure warning exists. Root readiness requires zero `not_processed`, zero silent failure, and zero unexplained unrepresented files. File representation never proves complete concept extraction.

## Canonical validator design

One validator contract produces one canonical issue ledger across stages. Categories:

```text
schema
node_identity
edge_integrity
provenance
scope
source_existence
collision
coverage
community_integrity
report_consistency
HTML_consistency
sensitive_path_exposure
```

Every issue includes `issue_id`, `stage`, `severity`, `category`, `artifact`, `node_or_edge_id`, `source_file`, `message`, and `status`. Status is one of `open`, `accepted_limitation`, `resolved`, or `false_positive`.

Issue identity must remain stable across reruns when the same stage/artifact/entity/category defect recurs. Stage summaries derive from the canonical ledger and state validator version, stage, category counts, deduplication key, and status counts. Counts such as 30 and 10 may coexist only when their scopes are explicitly explained.

## Partition merge gate

A partition cannot enter physical or federated publication unless:

```text
JSON is valid
all local IDs are present and unique
all canonical IDs are deterministic and unique
all nodes have accepted or permitted deterministic provenance
all local endpoints resolve
cross-partition endpoints have explicit states
all paths are authorized and in scope
no blocked or sensitive path appears
all collisions are ledgered
source coverage has a terminal status
partition issue ledger exists
```

Native merge cannot bypass this gate.

## Global validation gate

Clustering, labeling, report generation, and HTML generation remain blocked until:

```text
all global IDs are unique under exact and case-insensitive comparison
all final endpoints resolve
zero nodes lack valid provenance
zero out-of-scope provenance paths remain
zero unregistered collision drops occurred
all partitions and sources are accounted for
merge order produces the same canonical graph
rerun produces stable IDs
canonical issue ledger exists
blocked and sensitive path count is zero
```

Report and HTML counts must subsequently match the validated graph exactly.

### Report and HTML quality gate

Final reports and static HTML must not expose absolute local paths. Reports must disclose provenance, collision, coverage, and validation warnings; define the method used for weak or isolated-node counts; and identify the processing stage represented by token or cost totals. External HTML network dependencies must be declared, and an offline deliverable must be self-contained rather than silently depending on a CDN.

## Reduced remediation pilot corpus

Selected future pilot corpus:

```text
registry/skill_registry.yaml
blueprints/debug-investigation/skill.blueprint.yaml
blueprints/docs-release-notes-candidate/gate_map.md
blueprints/docs-release-notes-candidate/skill.blueprint.yaml
blueprints/safety-command-review/skill.blueprint.yaml
```

This five-file set covers all three known collision families, registry/blueprint overlap, the S2 collision, repeated artifact roles, and shared runtime profile identity. It is not repository root.

P10.5K-C does not authorize this pilot. P10.5K-D must first define the exact implementation, directories, cleanup/rollback behavior, runtime command contract, and human approval gate.

## Pilot acceptance criteria

The future pilot must demonstrate:

```text
all five sources have terminal manifest status
all colliding source-local entities survive extraction and pre-merge validation
100% nodes have valid or permitted deterministic provenance
100% namespaced IDs are exact- and case-insensitive-unique
100% final endpoints resolve
zero silent node or edge drops
merge order does not alter canonical nodes, edges, or ledgers
rerun produces stable IDs
runtime_profile_S2 remains source-distinct or becomes an explicitly reviewed alias
skill_debug_investigation remains source-distinct or becomes an explicitly reviewed alias
skill_docs_release_notes_candidate remains as distinct source-qualified entities unless human-reviewed
zero unresolved S2/S3 collisions
canonical warning ledger explains every stage count
no blocked or sensitive path appears
```

Native `merge-graphs` may be evaluated within that future pilot only after pre-merge namespacing/provenance gates. It is not accepted as safe merely because the command completes.

## Exploratory root refresh and operational-readiness contract

One final local Graphify root-scope extraction is authorized now for the P10.6 exploratory evidence refresh. The provenance-safe pilot is not a prerequisite for generating that map. The run must preserve the measured collision, dropped-node, missing/invalid provenance, source-coverage, case-sensitive identity, warning-accounting, report-consistency, and HTML-path/dependency limitations established by P10.5K-B.

The exploratory output is raw generated evidence only. It is not eligible for operational import, authority promotion, GBrain ingestion, semantic-memory use, Cognitive Semantic System adoption, source-of-truth status, approval use, or runtime use.

Before any such operational use, an authorized remediation pilot must prove all gates:

| Quantitative gate | Required result |
| --- | ---: |
| Globally unique final node IDs | 100% exact and case-insensitive uniqueness |
| Resolved final edge endpoints | 100% |
| Valid/deterministically injected provenance | 100% of nodes |
| Out-of-scope provenance | 0 nodes |
| Silent collision drops | 0 |
| Unresolved S2/S3 collisions | 0 |
| Unexplained unrepresented files | 0 |
| Source files with terminal status | 100% |
| Report counts matching graph | 100% |
| HTML structural counts matching graph | 100% |
| Blocked paths | 0 |
| Sensitive paths | 0 |
| Hosted-provider use | 0 |

Qualitative gates:

```text
namespacing deterministic and reversible
merge order invariant
rerun IDs stable
warning ledger stage-explicit
rollback and cleanup boundaries defined
evidence classification remains non-authoritative
```

Explicit status:

```text
exploratory root-scope evidence refresh authorized for P10.6
operational import and authority promotion remain blocked pending the provenance-safe pilot
```

The authorized P10.6 run may generate the exploratory root evidence map with current Graphify behavior under the governed root scope. Its warnings and limitations must be reported without remediation claims. A later pilot and every partition/global gate remain mandatory before the output, or any successor graph, can cross an operational or authority boundary. The P10.6 refresh is visualization/report/evidence-map work only and does not reopen Graphify as semantic retrieval, operational memory, or authority.

## Implementation components required

P10.5K-D may design an exact future implementation contract for:

```text
source manifest builder
partition runner
provenance validator
node-ID namespacer
edge rewriter
collision ledger
coverage ledger
validated merge adapter
global validator
report/HTML consistency validator
```

Components must be local, deterministic, provider-independent, non-authoritative, reviewable, reversible, and unable to silently alter semantic content. P10.5K-C implements none of them.

## Security and scope boundaries

Future work must use explicit allowlisted source manifests and default-deny path validation. Credentials, secrets, `.env*`, token stores, provider configuration, products, external sources, artifacts, generated outputs as source input, and absolute local paths are blocked. No hosted provider is required or authorized.

`.graphifyignore` expresses the governed controlled-root policy for the authorized exploratory refresh and includes broad exclusions plus selected re-inclusions. The later provenance-safe pilot must not assume this file admits its five pilot files; pilot input-policy alignment still requires a separate explicit design/approval decision. `.gitignore` is unchanged. Generated outputs must remain local and unstaged unless a separate governance decision says otherwise.

## Authorized exploratory root refresh input-policy contract

Policy-eligible inputs are limited to `README.md`, `0_architecture/**/*.md`, and `3_platform/_governed_skeleton/**/*.py` under the current governed scope. References or Markdown links to blocked paths do not grant traversal permission. Code fences and command examples are inert text. Unknown paths remain default-deny, and raw or generated outputs must never be recycled as refresh inputs.

## Authority classification

The plan, future manifests, ledgers, adapters, graphs, reports, and visualizations are evidence-control mechanisms, not authority. They cannot approve source changes, authorize runtime, become operational memory, serve as semantic retrieval authority, or become GBrain/Cognitive Semantic System substrate without separate review and promotion.

## Outcome classification

```text
Outcome A - Remediation architecture selected
```

Required markers:

```text
graphify_collision_provenance_remediation_architecture_selected
graphify_partitioned_provenance_safe_build_selected
graphify_deterministic_node_namespace_required
graphify_source_manifest_required
graphify_canonical_validation_ledger_required
graphify_native_merge_only_unproven
graphify_exploratory_root_scope_refresh_authorized
graphify_operational_use_remains_pilot_gated
graphify_partitioned_remediation_pilot_ready
```

Selection basis:

```text
preferred architecture selected
federated fallback selected
per-file partitioning selected
deterministic reversible namespace defined
single-source-only provenance injection defined
edge rewriting and collision controls defined
partition and global gates defined
five-file pilot corpus defined
exploratory root refresh and operational-readiness contract defined
no runtime or implementation occurred
```

## Selected next step

```text
One final local Graphify root-scope exploratory extraction for P10.6
```

P10.5K-D remains the required provenance-safe pilot architecture before operational import, authority promotion, GBrain ingestion, semantic-memory use, or Cognitive Semantic System adoption. It is no longer a prerequisite for generating the P10.6 exploratory evidence map and does not inherit runtime authorization beyond a separately approved pilot.

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_graphify_reduced_scope_collision_provenance_remediation_plan.md
```

Modified:

```text
none
```

Not created or executed:

```text
no adapter
no validator
no namespacer
no manifest
no partition extraction
no merge
no clustering
no report regeneration
no HTML regeneration
no source repair
no output repair
no root-scope extraction
no Graphify runtime
no Ollama inference
no hosted-provider call
no generated-output inspection
no generated-output staging
no Git mutation
```

## Limitations

The `no root-scope extraction` entry above records what P10.5K-C itself executed; it is not a current blocker on the separately authorized P10.6 exploratory run. CLI help proves only exposed syntax, not implementation semantics. Single-file extraction support, native merge behavior, endpoint rewriting, provenance retention, merge-order independence, rerun stability, and pilot resource requirements remain unproven. All measured collision and provenance limitations remain active. This plan defines future operational controls but does not demonstrate them.

## Commit commands

If accepted, stage only this plan:

```powershell
git status --short

git add 0_architecture/governance/agent_platform_graphify_reduced_scope_collision_provenance_remediation_plan.md

git commit -m "Plan Graphify collision and provenance remediation"

git push
```

Do not use `git add .`. Do not stage `graphify-out/**`, `.opencode/**`, or `AGENTS.md`.
