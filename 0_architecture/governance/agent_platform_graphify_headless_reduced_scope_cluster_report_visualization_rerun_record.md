# Graphify Headless Reduced-Scope Cluster, Report and Visualization Rerun Record

## Summary

P10.5K-A-RERUN completed one controlled local Graphify `cluster-only` execution against the existing P10.5K reduced-scope graph.

Outcome:

```text
Outcome A - cluster, report, and visualization completion succeeds
```

The existing 40-node, 33-edge graph was loaded, reclustered, and labeled with local Ollama `qwen3.5:9b`. Graphify completed 14 communities and updated the required generated outputs:

```text
graph.json
GRAPH_REPORT.md
graph.html
```

Metadata-only validation confirmed that all three required files exist and are non-empty. The automatic dated backup directory exists inside the exact approved reduced-run output root. The four shell-scoped runtime variables were removed. Git showed no staged changes and only untracked paths.

The execution did not rerun semantic extraction. Generated contents were not opened or parsed. Historical extraction-quality limitations remain preserved and unresolved.

Result marker:

```text
graphify_headless_reduced_scope_cluster_report_visualization_rerun_record_ready
```

Outcome markers:

```text
graphify_headless_cluster_only_rerun_execution_success
graphify_headless_qwen3_5_community_naming_success
graphify_headless_existing_graph_loaded
graphify_headless_semantic_extraction_not_rerun
graphify_headless_graph_json_retained
graphify_headless_graph_report_generated
graphify_headless_html_visualization_generated
graphify_headless_reduced_scope_completion_success
graphify_headless_known_quality_warnings_preserved
graphify_headless_outputs_local_untracked_unvalidated
graphify_no_hosted_provider_calls
graphify_no_git_mutation
p10_5k_b_reduced_scope_quality_review_ready
```

```yaml
P10_5K_A_RERUN_Graphify_Headless_Reduced_Scope_Cluster_Report_Visualization:
  ticket: "P10.5K-A-RERUN"
  date: "2026-07-11"
  status: "completed"
  outcome: "Outcome A - cluster, report, and visualization completion succeeds"
  output_file: "0_architecture/governance/agent_platform_graphify_headless_reduced_scope_cluster_report_visualization_rerun_record.md"
  explicit_human_approval_present: true
  fresh_preflight_passed: true
  historical_safe_block_consumed_runtime: false
  cluster_only_executed: true
  cluster_only_execution_count: 1
  backend: "ollama"
  backend_scope: "local"
  model: "qwen3.5:9b"
  semantic_extraction_rerun: false
  existing_graph_loaded: true
  pre_cluster_nodes: 40
  pre_cluster_edges: 33
  final_communities: 14
  graph_json_bytes: 27410
  graph_report_bytes: 7965
  graph_html_bytes: 42093
  required_outputs_non_empty: true
  backup_directory_name: "2026-07-11"
  backup_directory_inside_approved_root: true
  backup_reported_file_count: 5
  current_cluster_validation_issues: 10
  historical_cross_chunk_id_collisions: 3
  historical_duplicate_nodes_dropped: true
  historical_extraction_quality_issues: 30
  missing_source_file_issue_present: true
  generated_output_contents_inspected: false
  hosted_provider_used: false
  approved_environment_variables_absent_after_run: true
  git_staged_changes_present: false
  git_mutated: false
  selected_next_ticket: "P10.5K-B - Graphify Reduced-Scope Evidence Quality and Collision Assessment"
  final_marker: "graphify_headless_reduced_scope_cluster_report_visualization_rerun_record_ready"
```

## Files Inspected

Only approved governance records and generated-output metadata were inspected.

Governance dependencies reviewed during preflight:

```text
0_architecture/governance/agent_platform_graphify_headless_cli_qwen3_5_reduced_scope_execution_record.md
0_architecture/governance/agent_platform_graphify_headless_cli_qwen3_5_marker_contract_alignment.md
0_architecture/governance/agent_platform_graphify_headless_reduced_scope_cluster_report_visualization_completion_record.md
```

Generated files were checked only for:

```text
existence
file length
last-write timestamp
```

Generated file contents were not opened or parsed.

## Files Created

Created by this governance closure:

```text
0_architecture/governance/agent_platform_graphify_headless_reduced_scope_cluster_report_visualization_rerun_record.md
```

Created automatically by Graphify according to terminal and metadata evidence:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/GRAPH_REPORT.md
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.html
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/2026-07-11/
```

The dated directory is a Graphify-owned backup directory inside the exact approved output root. Its contents were not inspected.

## Files Modified

Modified automatically by Graphify:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.json
```

Graphify also reported updating report and visualization outputs:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/GRAPH_REPORT.md
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.html
```

No governance record other than this new rerun record was modified.

## Commands Run

Exactly one Graphify runtime command was executed manually from the repository root:

```powershell
$RunRoot = (Resolve-Path "graphify-out/p10_5k_qwen35_headless_reduced_01").Path

$env:OLLAMA_MODEL = "qwen3.5:9b"
$env:GRAPHIFY_OLLAMA_NUM_CTX = "65536"
$env:GRAPHIFY_LLM_TEMPERATURE = "0"
$env:GRAPHIFY_API_TIMEOUT = "900"

try {
    graphify cluster-only `
      $RunRoot `
      --backend ollama `
      --model qwen3.5:9b `
      --max-concurrency 1
}
finally {
    Remove-Item Env:OLLAMA_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:GRAPHIFY_OLLAMA_NUM_CTX -ErrorAction SilentlyContinue
    Remove-Item Env:GRAPHIFY_LLM_TEMPERATURE -ErrorAction SilentlyContinue
    Remove-Item Env:GRAPHIFY_API_TIMEOUT -ErrorAction SilentlyContinue
}
```

Execution count:

```text
1
```

No retry occurred.

Phase C used metadata-only path, size, timestamp, environment-variable, and Git-status checks. No generated content was inspected.

## Human Approval Status

Explicit human approval existed for:

```text
one fresh preflight
one local cluster-only execution
local qwen3.5 community naming
modification of the existing reduced graph
creation or modification of report, HTML, and Graphify sidecars inside the approved output root
metadata-only post-run validation
creation of this governance record
```

No approval existed for semantic re-extraction, content inspection, warning remediation, hosted-provider use, output cleanup, output staging, or Git mutation.

## P10.5K Dependency Status

Status:

```text
passed
```

The accepted P10.5K record established:

```text
local Ollama qwen3.5:9b extraction success
3/3 semantic chunks completed
graph build success
40 nodes
33 edges
14 communities
graph.json generated
known quality warnings preserved
outputs local, untracked, and unvalidated
```

## P10.5K Marker-Alignment Status

Status:

```text
passed
```

The accepted marker-alignment record added the exact compatibility aliases required by P10.5K-A-RERUN without changing any original execution fact or warning.

## Historical P10.5K-A Safe-Block Status

The historical P10.5K-A record remains valid as:

```text
Outcome B - preflight safe block
```

It recorded:

```text
cluster_only_executed: false
cluster_only_execution_count: 0
outputs_modified: false
```

Therefore the historical ticket consumed no runtime attempt. It was not modified by this rerun.

## Graphify Executable/Version Status

Fresh preflight passed.

Resolved runtime:

```text
graphifyy 0.9.5
```

The required `cluster-only`, `--backend`, `--model`, and `--max-concurrency` syntax was available.

## qwen3.5 Inventory Status

Fresh preflight passed.

Approved local model:

```text
qwen3.5:9b
```

No model pull, replacement, copy, removal, or hosted model was used.

## Reduced Graph Dependency Preflight

Required graph:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.json
```

Preflight status:

```text
exists
regular file
non-empty
```

`GRAPH_REPORT.md` and `graph.html` were absent before runtime, so no overwrite collision blocked execution.

## Environment-Variable Baseline

The approved environment-variable baseline passed before runtime:

```text
OLLAMA_MODEL absent
GRAPHIFY_OLLAMA_NUM_CTX absent
GRAPHIFY_LLM_TEMPERATURE absent
GRAPHIFY_API_TIMEOUT absent
```

No unknown pre-existing value was overwritten.

## Pre-Run Output Metadata

Before runtime:

```text
graph.json existed and was non-empty
GRAPH_REPORT.md absent
graph.html absent
```

The exact pre-run `graph.json` length and last-write timestamp were collected during Phase A but are not reproduced in the recovery evidence available for this record. No value is invented here.

## Cluster-Only Command Status

Status:

```text
completed normally
```

Visible terminal progression:

```text
Loading existing graph...
Graph: 40 nodes, 33 edges
Re-clustering...
Labeling communities...
Done - 14 communities. GRAPH_REPORT.md, graph.json and graph.html updated.
```

The PowerShell prompt returned normally. No manual interruption occurred.

## Local Ollama Community-Naming Status

Status:

```text
completed
```

Community labeling ran through the approved local Ollama backend using exactly:

```text
qwen3.5:9b
```

No hosted provider or external API key was used.

## Graph Clustering Status

The existing graph was loaded and reclustered.

Observed pre-cluster graph metrics:

```text
40 nodes
33 edges
```

Final community count:

```text
14 communities
```

This result does not validate the semantic correctness of community assignments.

## GRAPH_REPORT.md Metadata

Path:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/GRAPH_REPORT.md
```

Post-run metadata:

```text
exists: true
length: 7,965 bytes
non-empty: true
```

Contents were not inspected.

## graph.html Metadata

Path:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.html
```

Post-run metadata:

```text
exists: true
length: 42,093 bytes
non-empty: true
```

The visualization was not opened.

## graph.json Post-Run Metadata

Path:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/graph.json
```

Post-run metadata:

```text
exists: true
length: 27,410 bytes
non-empty: true
```

Contents were not parsed.

## Generated Sidecar and Backup Metadata

Graphify reported:

```text
backed up semantic graph (5 files) -> 2026-07-11/
```

Metadata validation confirmed that the dated backup directory exists inside:

```text
graphify-out/p10_5k_qwen35_headless_reduced_01/graphify-out/
```

Backup contents were not inspected.

The recovery evidence supplied for this record does not include exact post-run sizes for:

```text
.graphify_analysis.json
.graphify_labels.json
cost.json
```

Their presence was not required for Outcome A because all mandatory outputs passed. No unsupported sidecar claim is made.

## Known Extraction-Quality Warnings

Historical P10.5K limitations remain preserved:

```text
three cross-chunk node-ID collisions
duplicate nodes dropped
30 extraction-quality issues
missing source_file metadata present
```

During `cluster-only`, Graphify reported:

```text
Extraction warning (10 issues)
```

Visible example:

```text
Node 7 (id='runtime_profile_s1') missing required field 'source_file'
```

The 10 current validation issues must not be interpreted as proof that the historical 30 extraction-quality issues were reduced, repaired, or superseded.

No claim is made that:

```text
ID collisions were resolved
dropped nodes were restored
source provenance became complete
semantic output became correct
content was validated
```

## Environment Cleanup Status

Post-run checks confirmed that all four shell-scoped variables were absent:

```text
OLLAMA_MODEL
GRAPHIFY_OLLAMA_NUM_CTX
GRAPHIFY_LLM_TEMPERATURE
GRAPHIFY_API_TIMEOUT
```

The `finally` cleanup completed successfully.

## Generated-Output Classification

The completed outputs remain:

```text
local generated evidence
ignored/untracked
content-unvalidated
completeness-unvalidated
provenance-limited
non-authoritative
not source of truth
not approval
not runtime authority
not operational memory
not semantic retrieval authority
not imported into GBrain
not Cognitive Semantic System substrate
```

Technical generation does not promote the graph, report, visualization, labels, or communities to authority.

## Post-Run Git Status

Observed status:

```text
no staged paths
only untracked paths
```

No Git mutation was performed by Graphify or during Phase C.

Generated Graphify outputs remain unstaged.

## Outcome Classification

Final outcome:

```text
Outcome A - cluster, report, and visualization completion succeeds
```

Basis:

```text
fresh preflight passed
cluster-only executed exactly once
existing graph loaded
local qwen3.5 community naming completed
semantic extraction was not rerun
graph.json exists and is non-empty
GRAPH_REPORT.md exists and is non-empty
graph.html exists and is non-empty
automatic backup remained inside the approved output root
approved environment variables were removed
no hosted provider was used
no blocked boundary was observed
no Git mutation occurred
```

## Created / Not Created Register

Created or updated by Graphify inside the approved output root:

```text
graph.json
GRAPH_REPORT.md
graph.html
2026-07-11/ backup directory
```

Potential Graphify-owned sidecars may exist inside the approved output root, but no unsupported presence or content claim is made here.

Created by governance closure:

```text
0_architecture/governance/agent_platform_graphify_headless_reduced_scope_cluster_report_visualization_rerun_record.md
```

Not performed or created:

```text
no semantic re-extraction
no per-subfolder extraction
no merge-graphs
no collision remediation
no dropped-node restoration
no source_file repair
no full-scope graph
no OpenCode skill runtime
no slash-command runtime
no hosted-provider call
no model pull
no dependency installation
no MCP registration
no graph-database push
no Git hooks
no generated-output staging
no Git mutation
no git add .
```

## Limitations

This record relies on visible terminal evidence and approved metadata summaries. Generated output contents were not independently inspected.

The exact pre-run `graph.json` size and timestamp and exact optional sidecar metadata are not reproduced in the available recovery evidence. They are therefore not invented.

The report and visualization may reflect nodes lost through the historical cross-chunk ID collisions and may contain entities with incomplete `source_file` provenance.

Outcome A establishes technical pipeline completion only. It does not establish semantic correctness, representational completeness, provenance completeness, or readiness for operational import.

## Recommended Next Ticket

```text
P10.5K-B - Graphify Reduced-Scope Evidence Quality and Collision Assessment
```

The next ticket may perform a bounded content review to determine:

```text
whether graph structure is usable
whether the report accurately reflects the reduced corpus
which entities were affected by ID collisions
whether missing source_file fields impair traceability
whether per-subfolder extraction plus merge is justified
whether authorized root-scope headless execution is ready
```

It must not automatically rerun extraction.

## Commit Commands

After acceptance, stage only this governance record:

```powershell
git status --short

git add 0_architecture/governance/agent_platform_graphify_headless_reduced_scope_cluster_report_visualization_rerun_record.md

git commit -m "Complete Graphify reduced-scope report rerun"

git push
```

Do not stage:

```text
graphify-out/**
.opencode/**
AGENTS.md
0_architecture/implementation/graphify_command_candidate_confirmation.md
0_architecture/governance/agent_platform_graphify_headless_reduced_scope_cluster_report_visualization_completion_record.md
```

Do not use:

```text
git add .
```

## Final Declaration

P10.5K-A-RERUN successfully completed one local Graphify `cluster-only` execution against the existing reduced graph. The graph was loaded, reclustered, and labeled into 14 communities using local Ollama `qwen3.5:9b`. `graph.json`, `GRAPH_REPORT.md`, and `graph.html` are present and non-empty. The dated Graphify backup remained within the approved output root, environment cleanup completed, and no Git mutation occurred.

Historical quality warnings remain unresolved, and all generated outputs remain local, untracked, content-unvalidated, and non-authoritative.

Final marker:

```text
graphify_headless_reduced_scope_cluster_report_visualization_rerun_record_ready
```
