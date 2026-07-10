# GBrain Mode A Direct Governance Import Sandbox Rerun Record

## Summary

P12.0D-RERUN executed the corrected GBrain Mode A direct-governance import sandbox rerun once, using `0_architecture/governance` as the only input path and keeping GBrain home, DB, exports, logs, and reports under the approved fresh sandbox root.

Result marker:

```text
gbrain_mode_a_direct_governance_import_sandbox_rerun_record_ready
```

Decision markers:

```text
gbrain_direct_governance_import_rerun_success
gbrain_governance_input_git_visible
gbrain_governance_markdown_import_success
gbrain_governance_keyword_search_success
gbrain_governance_export_success
gbrain_generated_outputs_local_untracked
gbrain_graph_query_still_deferred
gbrain_mode_b_ollama_still_blocked
gbrain_provider_calls_still_blocked
p12_0e_gov_review_ready_after_rerun
```

Runtime result:

```text
Git-visible governance markdown before runtime: 119
GBrain import collected: 119 markdown files
GBrain import completed: 119 pages imported, 0 skipped, 0 errors, 1644 chunks created
Search completed and returned ranked governance results
Export completed: 119 pages exported
```

```yaml
P12_0D_RERUN_Decision:
  ticket: P12.0D-RERUN
  date: "2026-07-10"
  outcome: "Outcome A - direct governance import success"
  human_rerun_approval_present: true
  preflight_completed: true
  governance_input_exists: true
  governance_input_ignored: false
  governance_visible_markdown_count: 119
  rerun_sandbox_root_existed_before_execution: false
  sandbox_directories_created: true
  gbrain_runtime_sequence_attempted_once: true
  gbrain_init_success: true
  keyword_only_config_success: true
  direct_governance_import_success: true
  imported_markdown_files: 119
  imported_pages: 119
  skipped_pages: 0
  import_errors: 0
  chunks_created: 1644
  keyword_search_success: true
  export_success: true
  exported_pages: 119
  graph_query_attempted: false
  mode_b_ollama_attempted: false
  provider_calls_attempted: false
  graphify_attempted: false
  generated_outputs_staged: false
  p12_0e_gov_review_ready_now: true
  final_marker: "gbrain_mode_a_direct_governance_import_sandbox_rerun_record_ready"
```

## Files Inspected

Governance files inspected read-only by marker search or presence check:

```text
0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction.md
0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
0_architecture/governance/agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
```

Direct governance input metadata inspected before runtime:

```text
0_architecture/governance
0_architecture/governance/**/*.md via git ls-files metadata count
```

Direct governance input read by GBrain runtime:

```text
0_architecture/governance/**/*.md
```

GBrain runtime metadata checked by path existence only:

```text
4_external/sources/gbrain-master
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
4_external/sources/gbrain-master/node_modules
4_external/sources/gbrain-master/src/cli.ts
```

No credential files, environment secrets, normal user `.gbrain`, `node_modules` contents, DB internals, generated home internals, product/Siamese paths, Graphify outputs, package caches, or external source roots outside the allowed GBrain metadata paths were inspected.

## Files Created

Approved rerun sandbox directories were created under:

```text
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/
```

Created directories:

```text
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/gbrain_home/
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/db/
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/exports/
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/logs/
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/reports/
```

No copied input fixture directory was created.

GBrain generated local sandbox state under the approved rerun sandbox root, including local PGLite DB state under `db/`, configuration state under `gbrain_home/`, and exported markdown under `exports/`. Generated internals were not recursively inspected.

## Files Modified

The existing P12.0D-RERUN governance execution record was replaced with this successful execution record:

```text
0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_sandbox_rerun_record.md
```

No other governance file, source file, dependency file, package file, PATH configuration, shell profile, or Git metadata was modified by P12.0D-RERUN.

## Commands Run

Allowed preflight commands run:

```powershell
git status --short
Test-Path 0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction.md
Test-Path 0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
Test-Path 0_architecture/governance
Test-Path 4_external/sources/gbrain-master
Test-Path 4_external/sources/gbrain-master/package.json
Test-Path 4_external/sources/gbrain-master/bun.lock
Test-Path 4_external/sources/gbrain-master/node_modules
Test-Path 4_external/sources/gbrain-master/src/cli.ts
Get-Command bun -ErrorAction SilentlyContinue
bun --version
bun --revision
Test-Path 9_artifacts/gbrain_sandbox/p12_0d_governance_import_01
```

Allowed sandbox setup commands run:

```powershell
$RepoRoot = (Get-Location).Path
$GBrainRoot = Join-Path $RepoRoot "4_external\sources\gbrain-master"
$GovernanceInput = Join-Path $RepoRoot "0_architecture\governance"
$SandboxRoot = Join-Path $RepoRoot "9_artifacts\gbrain_sandbox\p12_0d_governance_import_01"
$GBrainHome = Join-Path $SandboxRoot "gbrain_home"
$DbPath = Join-Path $SandboxRoot "db"
$ExportsPath = Join-Path $SandboxRoot "exports"
$LogsPath = Join-Path $SandboxRoot "logs"
$ReportsPath = Join-Path $SandboxRoot "reports"
Test-Path $SandboxRoot
New-Item -ItemType Directory -Force -Path $GBrainHome,$DbPath,$ExportsPath,$LogsPath,$ReportsPath | Out-Null
```

Approved Mode A runtime commands run once from `4_external/sources/gbrain-master`:

```powershell
Push-Location $GBrainRoot
$env:GBRAIN_HOME = $GBrainHome
bun run src/cli.ts init --pglite --path "$DbPath" --no-embedding
bun run src/cli.ts config set search.mcp_keyword_only true
bun run src/cli.ts import "$GovernanceInput" --no-embed
bun run src/cli.ts search "GBrain Graphify controlled sandbox evidence"
bun run src/cli.ts export --dir "$ExportsPath"
Remove-Item Env:GBRAIN_HOME
Pop-Location
```

The PowerShell wrapper checked `$LASTEXITCODE` between native runtime commands to enforce the stop rule. No extra GBrain, Graphify, Ollama, provider, package, test, build, or Git mutation command was executed.

Approved post-run verification commands run:

```powershell
git status --short
Test-Path $SandboxRoot
Test-Path $GovernanceInput
Test-Path $GBrainHome
Test-Path $DbPath
Test-Path $ExportsPath
Test-Path $LogsPath
Test-Path $ReportsPath
Test-Path Env:GBRAIN_HOME
Get-ChildItem -LiteralPath $SandboxRoot -Force
Get-ChildItem -LiteralPath $ExportsPath -Force
```

Forbidden commands not run:

```text
No gbrain binary command
No graph-query
No bun run src/cli.ts graph-query
No sources/doctor/apply-migrations/provider command
No bun run without explicit src/cli.ts subcommand
No bun build/test/install/x
No npm/node/npx/pnpm/yarn command
No Graphify command
No Ollama command
No provider/API command
No credential/environment secret command
No package install
No build/test/CI
No Git mutation
No staging command
```

## Human Approval Status

The required P12.0D-RERUN Mode A approval statement was present in the user request before sandbox setup and runtime execution.

```yaml
human_rerun_approval_present: true
sandbox_setup_allowed: true
runtime_execution_allowed: true
```

## P12.0D-IMPORT-FIX Dependency Status

P12.0D-IMPORT-FIX exists:

```text
0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction.md
```

Confirmed markers:

```text
gbrain_mode_a_direct_governance_import_strategy_correction_ready
p12_0d_rerun_ready_after_direct_governance_import_fix
```

## P12.0E Dependency Status

P12.0E exists:

```text
0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
```

Confirmed markers:

```text
gbrain_sandbox_output_review_graph_query_follow_up_preparation_ready
```

## P12.0D / P12.INSTALL Dependency Status

P12.0D execution record exists:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
```

Confirmed P12.0D markers:

```text
gbrain_controlled_local_memory_sandbox_execution_record_ready
p12_0e_ready_after_mode_a_execution
```

P12.INSTALL execution record exists:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
```

Confirmed P12.INSTALL markers:

```text
gbrain_controlled_local_dependency_install_execution_record_ready
```

## Preflight Status

Preflight results:

```yaml
gbrain_source_root_present: true
package_json_present: true
bun_lock_present: true
node_modules_present: true
src_cli_present: true
bun_available: true
bun_path: "C:\Users\pablo\.bun\bin\bun.exe"
bun_version: "1.3.14"
bun_revision: "1.3.14+0d9b296af"
governance_input_present: true
governance_input_ignored: false
governance_visible_markdown_count: 119
rerun_sandbox_root_existed_before_execution: false
```

Initial `git status --short` observed before runtime:

```text
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

The Graphify confirmation file was pre-existing and was not inspected, staged, or modified.

## Governance Input Git Visibility Status

Direct governance input:

```text
0_architecture/governance
```

Git ignore check:

```yaml
git_check_ignore_output: "<none>"
governance_input_ignored: false
```

Visible markdown count:

```yaml
git_visible_governance_markdown_count: 119
git_visible_governance_markdown_count_gt_zero: true
```

Decision marker:

```text
gbrain_governance_input_git_visible
```

## Sandbox Path Status

Selected rerun sandbox root:

```text
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/
```

Sandbox directories observed after runtime:

```text
db/
exports/
gbrain_home/
logs/
reports/
```

Post-run path checks:

```yaml
sandbox_root_exists: true
governance_input_exists: true
gbrain_home_exists: true
db_path_exists: true
exports_path_exists: true
logs_path_exists: true
reports_path_exists: true
input_fixture_directory_created: false
```

## Runtime Execution Status

The approved runtime sequence was attempted exactly once and completed without a nonzero command failure.

```yaml
runtime_sequence_attempted_once: true
runtime_working_directory: "4_external/sources/gbrain-master"
runtime_prefix: "bun run src/cli.ts"
runtime_completed_without_nonzero_tool_failure: true
gbrain_home_scope: "shell-scoped PowerShell process only"
```

Nonfatal runtime output noted during init:

```text
El sistema no puede encontrar la ruta especificada.
GStack: not found
recommended skills message printed by GBrain
```

No recommended skill install command was run.

## Init Result

Init command:

```powershell
bun run src/cli.ts init --pglite --path "$DbPath" --no-embedding
```

Observed result:

```text
Setting up local brain with PGLite (no server needed)...
--no-embedding: deferred setup
117 migration(s) applied
Brain ready at ...\9_artifacts\gbrain_sandbox\p12_0d_governance_import_01\db
0 pages. Engine: PGLite (local Postgres).
```

```yaml
gbrain_init_success: true
local_pglite_init_success: true
```

## Keyword-Only Config Result

Config command:

```powershell
bun run src/cli.ts config set search.mcp_keyword_only true
```

Observed result:

```text
Set search.mcp_keyword_only = true
```

```yaml
keyword_only_config_success: true
```

## Direct Governance Import Result

Import command:

```powershell
bun run src/cli.ts import "$GovernanceInput" --no-embed
```

Observed result:

```text
[gbrain phase] import.collect_files start dir=...\0_architecture\governance strategy=markdown
[gbrain phase] import.collect_files done 25ms files=119
Found 119 markdown files
Import complete (16.0s):
  119 pages imported
  0 pages skipped (0 unchanged, 0 errors)
  1644 chunks created
```

Import also emitted content-sanity warnings and markup-heavy flags for some large governance documents. These did not fail the import.

Decision marker:

```text
gbrain_governance_markdown_import_success
```

```yaml
direct_governance_import_success: true
imported_markdown_files: 119
imported_pages: 119
skipped_pages: 0
import_errors: 0
chunks_created: 1644
```

## Search Result

Search command:

```powershell
bun run src/cli.ts search "GBrain Graphify controlled sandbox evidence"
```

Observed result:

```text
Ranked governance results were returned.
Top observed results included:
agent_platform_gbrain_ollama_controlled_sandbox_plan
agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review
agent_platform_gbrain_controlled_sandbox_exact_command_preparation
agent_platform_gbrain_controlled_local_memory_sandbox_execution_record
agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction
agent_platform_gbrain_controlled_local_install_build_plan
agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation
agent_platform_external_tool_execution_gate_model
```

Decision marker:

```text
gbrain_governance_keyword_search_success
```

```yaml
keyword_search_success: true
ranked_results_observed: true
```

## Export Result

Export command:

```powershell
bun run src/cli.ts export --dir "$ExportsPath"
```

Observed result:

```text
Exporting 119 pages to ...\9_artifacts\gbrain_sandbox\p12_0d_governance_import_01\exports/
Exported 119 pages to ...\9_artifacts\gbrain_sandbox\p12_0d_governance_import_01\exports/
```

Decision marker:

```text
gbrain_governance_export_success
```

```yaml
export_success: true
exported_pages: 119
exports_top_level_files_observed: true
```

## Generated Output Metadata

Generated outputs were confined to:

```text
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/
```

Observed top-level sandbox entries:

```text
db/
exports/
gbrain_home/
logs/
reports/
```

Observed exports top-level metadata:

```text
119 markdown files were exported under exports/.
```

Representative observed export filenames:

```text
agent_platform_gbrain_mode_a_direct_governance_import_sandbox_rerun_record.md
agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction.md
agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md
agent_platform_gbrain_ollama_controlled_sandbox_plan.md
agent_platform_graphify_ignore_exclusion_strategy.md
agent_platform_external_tool_execution_gate_model.md
```

Generated DB, home, log, and report internals were not recursively inspected.

Decision marker:

```text
gbrain_generated_outputs_local_untracked
```

Important output-review note:

```text
The earlier blocked P12.0D-RERUN record already existed under 0_architecture/governance before runtime, so it was included in the 119 imported/exported governance pages. This success record was written after runtime and is not reflected in the already-created export copy until a future approved rerun or output review handles that distinction.
```

## GBRAIN_HOME Cleanup Status

`GBRAIN_HOME` was set only inside the runtime PowerShell process and removed after export.

Post-run check:

```yaml
Test-Path_Env_GBRAIN_HOME: false
cleanup_required_after_postcheck: false
```

## Post-Run Git Status

Post-runtime `git status --short` before this record update:

```text
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

No sandbox outputs, dependency artifacts, or generated artifacts were staged. The approved sandbox path is under ignored `9_artifacts/` and did not appear in `git status --short`.

Final worktree status after this record update is expected to include this governance record modification and the pre-existing Graphify confirmation file only.

## Graph-Query Boundary Confirmation

Graph-query was not run and remains deferred.

Decision marker:

```text
gbrain_graph_query_still_deferred
```

Reason:

```text
This ticket validates corrected import/search/export only. Graph-query requires a separate output review and deterministic slug preparation gate.
```

## Mode B / Ollama Boundary Confirmation

Mode B remains blocked.

Decision markers:

```text
gbrain_mode_b_ollama_still_blocked
```

P12.0D-RERUN did not authorize or run:

```text
Ollama model inventory
Ollama model pull
Ollama inference
embedding generation
provider/API calls
hosted provider fallback
Graphify with Ollama
```

## Incident Status

No boundary violation was observed.

```yaml
incident_status: "completed_with_content_sanity_warnings"
runtime_safe_failure: false
output_boundary_violation: false
credentials_exposed: false
normal_user_gbrain_used: false
path_modified: false
git_mutated: false
```

Runtime caveat:

```text
GBrain init printed a no-OpenAI-key advisory and recommended skills matrix. No provider command, provider API call, package install, or skill scaffold command was run.
```

## P12.0E-GOV-REVIEW Handoff Decision

P12.0E-GOV-REVIEW is ready as a sandbox output review and graph-query preparation ticket.

Decision marker:

```text
p12_0e_gov_review_ready_after_rerun
```

```yaml
P12_0E_GOV_REVIEW_HandoffDecision:
  status: "ready_after_successful_direct_governance_import_rerun"
  direct_graph_query_ready_now: false
  reason: "Import/export succeeded, but graph-query still requires output review and deterministic slug selection."
  recommended_next_ticket: "P12.0E-GOV-REVIEW - GBrain Governance Import Output Review / Graph Query Preparation"
```

## Created / Not Created Register

Created or written locally:

```text
0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_sandbox_rerun_record.md
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/gbrain_home/**
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/db/**
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/exports/**
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/logs/**
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/reports/**
```

Not created or not run:

```text
No copied fixture directory
No fixture copies
No governance modifications except this allowed execution record update
No graph-query
No embeddings
No Ollama command
No Ollama model pull
No provider/API call
No Graphify command
No credential inspection command
No product/Siamese path access
No normal user .gbrain write
No PATH mutation
No package install
No build
No test
No Git mutation
No staging sandbox outputs
No staging dependency artifacts
No git add .
```

## Limitations

This ticket did not inspect generated DB internals, generated home internals, exported file contents, or governance document contents beyond GBrain's approved runtime import.

This ticket did not run graph-query. Deterministic slug selection remains a follow-up review task.

The export includes the pre-runtime version of this rerun record, because the success record was written after GBrain export completed.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.0E-GOV-REVIEW - GBrain Governance Import Output Review / Graph Query Preparation
```

Do not proceed directly to graph-query.

## Commit Commands

If this execution record is accepted for commit, stage only the intended governance record. Do not stage sandbox outputs. Do not stage dependency artifacts. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_sandbox_rerun_record.md
git commit -m "Record GBrain direct governance import sandbox rerun"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainModeADirectGovernanceImportSandboxRerunRecord:
  ticket: P12.0D-RERUN
  date: "2026-07-10"
  target_file: "0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_sandbox_rerun_record.md"
  p12_0d_import_fix_confirmed: true
  p12_0e_confirmed: true
  p12_0d_confirmed: true
  p12_install_confirmed: true
  human_rerun_approval_present: true
  bun_available: true
  bun_version: "1.3.14"
  bun_revision: "1.3.14+0d9b296af"
  source_root_present: true
  node_modules_present: true
  src_cli_present: true
  governance_input_present: true
  governance_input_ignored: false
  governance_visible_markdown_count: 119
  rerun_sandbox_root_existed_before_execution: false
  sandbox_directories_created: true
  gbrain_home_set_by_ticket: true
  gbrain_home_cleaned_up: true
  runtime_sequence_attempted_once: true
  gbrain_init_success: true
  keyword_only_config_success: true
  direct_governance_import_success: true
  imported_markdown_files: 119
  imported_pages: 119
  skipped_pages: 0
  import_errors: 0
  chunks_created: 1644
  keyword_search_success: true
  export_success: true
  exported_pages: 119
  graph_query_attempted: false
  embeddings_generated: false
  ollama_attempted: false
  provider_calls_attempted: false
  graphify_attempted: false
  generated_outputs_confined_to_sandbox: true
  generated_outputs_staged: false
  credentials_inspected_by_agent_command: false
  path_modified: false
  git_mutated: false
  p12_0e_gov_review_ready_now: true
  final_marker: "gbrain_mode_a_direct_governance_import_sandbox_rerun_record_ready"
```

Final marker:

```text
gbrain_mode_a_direct_governance_import_sandbox_rerun_record_ready
```
