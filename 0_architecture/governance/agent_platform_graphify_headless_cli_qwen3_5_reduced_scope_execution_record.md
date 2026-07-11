# Graphify Headless CLI qwen3.5 Reduced-Scope Execution Record

## Summary

P10.5K records the already-completed user-run Graphify headless CLI extraction against the approved reduced input scope using local Ollama and `qwen3.5:9b`.

Classification:

```text
Outcome A - reduced-scope headless extraction and graph build succeeded with non-fatal quality warnings
```

The run detected 20 documentation files, completed all three semantic chunks, and produced a final graph containing 40 nodes, 33 edges, and 14 communities. The run used 14,259 input tokens and 4,194 output tokens at an estimated cost of $0.

The graph build succeeded, but the supplied terminal evidence reported non-fatal extraction-quality warnings: three cross-chunk node-ID collisions with duplicate nodes dropped, and 30 extraction-quality issues including missing `source_file` metadata. Final report generation and HTML visualization were not performed.

This record is based only on user-supplied terminal evidence. Generated output contents were not inspected. No extraction retry, `cluster-only`, report generation, visualization export, cleanup, deletion, output staging, or Git mutation was performed while creating this record.

Result marker:

```text
graphify_headless_cli_qwen3_5_reduced_scope_execution_record_ready
```

## P10.5K-A Marker Compatibility Amendment

Amendment date:

```text
2026-07-11
```

This amendment adds compatibility aliases only.
No execution fact, output, warning, limitation, outcome, or authority
classification is changed.

The original P10.5K markers remain unchanged. The following exact aliases are added solely to align the P10.5K evidence vocabulary with the P10.5K-A dependency contract:

```text
graphify_headless_qwen3_5_reduced_scope_execution_success
graphify_headless_ollama_backend_verified
graphify_headless_semantic_chunks_completed
graphify_headless_structured_output_accepted
graphify_headless_graph_build_success
graphify_headless_graph_json_generated
graphify_headless_quality_warnings_present
graphify_headless_outputs_local_untracked_unvalidated
```

Exact marker-to-evidence mapping:

| P10.5K-A compatibility marker | Existing P10.5K supporting evidence |
| --- | --- |
| `graphify_headless_qwen3_5_reduced_scope_execution_success` | Outcome A and original marker `graphify_qwen3_5_headless_reduced_scope_execution_success`. |
| `graphify_headless_ollama_backend_verified` | YAML records `backend: "ollama"`, `backend_scope: "local"`, model `qwen3.5:9b`, and successful execution. |
| `graphify_headless_semantic_chunks_completed` | YAML records three total and three completed chunks; original marker `graphify_qwen3_5_headless_semantic_chunks_completed`. |
| `graphify_headless_structured_output_accepted` | All three semantic chunks completed and Graphify accepted sufficient structured extraction output to merge/build and report a final `graph.json` path. This marker does not assert content validation. |
| `graphify_headless_graph_build_success` | YAML records `graph_build_succeeded: true`; original marker `graphify_qwen3_5_headless_graph_build_success`; final metrics are 40 nodes, 33 edges, and 14 communities. |
| `graphify_headless_graph_json_generated` | The exact final graph path is recorded and the supplied Graphify terminal evidence reported the graph write. Contents remain uninspected. |
| `graphify_headless_quality_warnings_present` | Three cross-chunk ID collisions, dropped duplicate nodes, 30 extraction-quality issues, and missing `source_file` are recorded. |
| `graphify_headless_outputs_local_untracked_unvalidated` | Outputs are recorded as local/untracked raw generated evidence; contents were not inspected or validated. |

Structured-output interpretation boundary:

```text
graphify_headless_structured_output_accepted means that Graphify's parser/pipeline
accepted sufficient structured extraction output to complete graph construction.

It does not assert semantic correctness, completeness, provenance quality,
schema perfection, or content validation.
```

Original facts explicitly preserved:

```text
three cross-chunk node-ID collisions
duplicate nodes dropped
30 extraction-quality issues
missing source_file issue present
GRAPH_REPORT.md not generated
graph.html not generated
generated output contents not inspected
no extraction retry
no cluster-only execution
outputs remain local/untracked raw generated evidence
```

Amendment markers:

```text
graphify_p10_5k_marker_compatibility_amendment_applied
graphify_p10_5k_original_facts_preserved
```

Outcome markers:

```text
graphify_qwen3_5_headless_reduced_scope_execution_success
graphify_qwen3_5_headless_semantic_chunks_completed
graphify_qwen3_5_headless_graph_build_success
graphify_qwen3_5_headless_quality_warnings_recorded
graphify_qwen3_5_headless_outputs_local_untracked
graphify_qwen3_5_headless_report_not_generated
graphify_qwen3_5_headless_html_not_generated
graphify_qwen3_5_headless_no_retry
graphify_qwen3_5_headless_outputs_not_inspected
graphify_no_git_mutation
p10_5k_closed
```

```yaml
P10_5K_Graphify_Headless_CLI_Qwen3_5_Reduced_Scope_Execution_Record:
  ticket: "P10.5K"
  date: "2026-07-11"
  status: "closed"
  outcome: "Outcome A - reduced-scope headless extraction and graph build succeeded with non-fatal quality warnings"
  output_file: "0_architecture/governance/agent_platform_graphify_headless_cli_qwen3_5_reduced_scope_execution_record.md"
  evidence_source: "user-supplied terminal evidence"
  execution_performed_by_user: true
  execution_rerun_by_gpt_5_6: false
  input_path: "3_platform/_governed_skeleton/agent_platform_mvp0/skills"
  input_scope: "reduced"
  backend: "ollama"
  backend_scope: "local"
  model: "qwen3.5:9b"
  requested_context: 65536
  token_budget: 4000
  max_concurrency: 1
  api_timeout_seconds: 900
  output_root: "graphify-out/p10_5k_qwen35_headless_reduced_01"
  detection:
    code_files: 0
    document_files: 20
    paper_files: 0
    image_files: 0
  semantic_chunks_total: 3
  semantic_chunks_completed: 3
  graph_nodes: 40
  graph_edges: 33
  graph_communities: 14
  input_tokens: 14259
  output_tokens: 4194
  estimated_cost_usd: 0
  final_graph_path: "graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.json"
  analysis_sidecar_path: "graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/.graphify_analysis.json"
  cross_chunk_node_id_collisions: 3
  duplicate_nodes_dropped: true
  extraction_quality_issues: 30
  missing_source_file_issue_present: true
  warnings_fatal: false
  graph_build_succeeded: true
  final_report_generated: false
  html_visualization_generated: false
  generated_output_contents_inspected: false
  cluster_only_executed_after_run: false
  extraction_retried: false
  outputs_cleaned_or_deleted: false
  graphify_outputs_staged: false
  git_mutated: false
  p10_5k_closed: true
  final_marker: "graphify_headless_cli_qwen3_5_reduced_scope_execution_record_ready"
```

## Execution Scope

Approved and observed input:

```text
3_platform/_governed_skeleton/agent_platform_mvp0/skills
```

The execution was reduced-scope only. It did not process the complete repository according to the supplied evidence.

Runtime selection:

```text
backend: local Ollama
model: qwen3.5:9b
requested context: 65536
token budget: 4000
max concurrency: 1
API timeout: 900 seconds
```

Output root:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01
```

## Detection Result

The supplied terminal evidence reported:

| Input category | Files detected |
| --- | ---: |
| code | 0 |
| documents | 20 |
| papers | 0 |
| images | 0 |

The corpus was documentation-oriented. Zero code files and absence of AST code entities are therefore not classified as failures.

## Semantic Extraction Result

Semantic chunk result:

```text
3 of 3 chunks completed
```

Token accounting:

```text
input tokens: 14,259
output tokens: 4,194
estimated cost: $0
```

Completion of all semantic chunks establishes that the local qwen3.5 headless semantic extraction route progressed beyond the prior direct qwen2.5 structured-output failures and the prior OpenCode routing failures.

It does not establish that every extracted node or relationship is correct.

## Graph Build Result

Final graph metrics from the supplied terminal evidence:

```text
nodes: 40
edges: 33
communities: 14
```

Final graph path:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.json
```

Analysis sidecar path:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/.graphify_analysis.json
```

These paths are recorded as generated-output references only. Their contents were not opened, parsed, summarized, imported, or validated while creating this record.

## Quality Warnings

The supplied terminal evidence reported three cross-chunk node-ID collisions.

Observed handling:

```text
duplicate nodes were dropped
graph construction continued
the warnings were non-fatal
```

The supplied evidence also reported:

```text
30 extraction-quality issues
```

Known issue class included:

```text
missing source_file metadata
```

These warnings limit confidence in provenance completeness and cross-chunk identity quality. The generated graph must remain raw generated evidence pending any future metadata-only review gate and any separately authorized content-quality review.

No warning was repaired, suppressed, or re-extracted during closure.

## Output Completion Status

Generated successfully according to supplied evidence:

```text
graph.json
.graphify_analysis.json
```

Not yet generated:

```text
GRAPH_REPORT.md
```

Therefore P10.5K establishes successful reduced-scope extraction and graph build, but not a complete Graphify report/visualization pipeline.

`cluster-only` remains unexecuted and is not authorized by this closure record.

## Evidence Boundary

This governance record consumes only the terminal facts supplied by the user.

Not inspected:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/** contents
graph.json contents
.graphify_analysis.json contents
semantic chunk contents
intermediate JSON contents
cache contents
source corpus contents during closure
provider configuration
credentials
.env files
token stores
normal-user application configuration
```

No claim is made beyond the supplied terminal evidence and recorded generated-output metadata.

## Commands Run During Closure

No Graphify, Ollama, OpenCode, provider, model, extraction, clustering, report, export, cleanup, test, build, CI, staging, commit, or push command was run while creating this closure record.

Specifically not run:

```text
graphify extract
graphify cluster-only
graphify export
/graphify
/graphify .
ollama run
ollama pull
OpenCode runtime
git add
git commit
git push
```

## Outcome Classification

Final classification:

```text
Outcome A - reduced-scope headless extraction and graph build succeeded with non-fatal quality warnings
```

Classification basis:

```text
reduced input scope was used
local Ollama qwen3.5:9b was used
20 documentation files were detected
all 3 semantic chunks completed
graph build completed
40 nodes were produced
33 edges were produced
14 communities were produced
final graph and analysis sidecar paths were reported
quality warnings did not prevent graph construction
```

Completion limitations:

```text
three node-ID collision warnings
30 extraction-quality issues
missing source_file metadata among known issues
final report absent
HTML visualization absent
generated output contents uninspected
```

## Authority And Output Classification

The generated Graphify files remain:

```text
raw generated evidence
local/untracked
not authority
not source of truth
not approval
not runtime authority
not operational memory
not semantic retrieval authority
not imported into GBrain
not Cognitive Semantic System substrate
```

The successful local model execution does not promote qwen3.5, Ollama, Graphify, the graph, extracted relationships, or community assignments to authority.

The quality warnings reinforce the requirement that generated nodes and edges remain unreviewed evidence until a future exact review gate says otherwise.

## Created / Not Created Register

Created by the already-completed user-run execution according to supplied evidence:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.json
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/.graphify_analysis.json
other local generated intermediates under the approved output root may exist but were not inspected
```

Created by this closure step:

```text
0_architecture/governance/agent_platform_graphify_headless_cli_qwen3_5_reduced_scope_execution_record.md
```

Not created or not yet generated:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/GRAPH_REPORT.md
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.html
```

Not performed or approved during closure:

```text
extraction retry
cluster-only
report generation
HTML export
generated-output content inspection
quality-warning repair
output cleanup or deletion
Graphify-output staging
Git mutation
git add .
```

## Limitations

This record relies on user-supplied terminal evidence. It does not independently verify generated file contents, graph schema, node/edge correctness, community quality, source provenance, or the completeness of the generated output directory.

The three cross-chunk node-ID collisions may have removed duplicate representations that were either genuinely redundant or semantically distinct. That distinction was not reviewed.

The 30 extraction-quality issues, including missing `source_file`, may affect provenance, incremental replacement, evidence traceability, and later report reliability.

The presence of graph and analysis paths does not imply that report and HTML outputs exist. The supplied evidence explicitly states they were not generated.

## P10.5K Closure

P10.5K is closed as a successful reduced-scope headless extraction and graph build with non-fatal quality warnings and incomplete report/visualization outputs.

Closure marker:

```text
p10_5k_closed
```

P10.5K-A must not be treated as started by this record. Any later `cluster-only`, report generation, visualization export, quality review, warning remediation, output-content inspection, or broader-scope execution requires a separate explicit gate.

## Final Declaration

The already-completed user-run headless execution successfully processed the reduced documentation corpus with local Ollama `qwen3.5:9b`, completed all semantic chunks, and built a 40-node, 33-edge graph with 14 communities. Three cross-chunk node-ID collisions and 30 extraction-quality issues remain recorded as non-fatal warnings. Report and HTML outputs remain ungenerated. No rerun, clustering, output inspection, cleanup, staging, or Git mutation occurred during closure.

Final marker:

```text
graphify_headless_cli_qwen3_5_reduced_scope_execution_record_ready
```
