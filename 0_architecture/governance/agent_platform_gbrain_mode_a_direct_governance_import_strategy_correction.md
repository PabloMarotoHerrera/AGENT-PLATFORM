# GBrain Mode A Direct Governance Import Strategy Correction

## Summary

P12.0D-IMPORT-FIX prepared a corrected Mode A rerun boundary. It did not rerun GBrain, import files, create sandbox directories, copy fixtures, run graph-query, generate embeddings, run Ollama, run Graphify, call providers, or mutate Git.

Result marker:

```text
gbrain_mode_a_direct_governance_import_strategy_correction_ready
```

Decision markers:

```text
gbrain_zero_page_import_root_cause_gitignore_visibility_confirmed
gbrain_direct_governance_import_strategy_selected
gbrain_real_governance_input_scope_selected
gbrain_outputs_remain_sandboxed
gbrain_mode_a_rerun_sandbox_root_selected
gbrain_graph_query_still_blocked_until_successful_import
gbrain_mode_b_ollama_still_blocked
gbrain_provider_calls_still_blocked
p12_0d_rerun_ready_after_direct_governance_import_fix
```

Selected correction:

```text
Import directly from 0_architecture/governance for the next Mode A rerun, while keeping all GBrain home, DB, exports, logs, and reports under a fresh ignored sandbox output root: 9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/.
```

```yaml
P12_0D_IMPORT_FIX_Decision:
  ticket: P12.0D-IMPORT-FIX
  date: "2026-07-10"
  outcome: "direct governance import strategy selected for future Mode A rerun"
  zero_page_import_confirmed: true
  fixture_files_physically_present: true
  markdown_fixture_files_physically_present: true
  markdown_extension_supported: true
  governance_input_exists: true
  governance_input_ignored: false
  governance_visible_markdown_count: 117
  direct_governance_import_selected: true
  copied_fixture_import_rejected: true
  rerun_sandbox_root: "9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/"
  graph_query_ready: false
  mode_b_ollama_ready: false
  provider_calls_ready: false
  gbrain_runtime_executed_now: false
  git_mutated: false
  final_marker: "gbrain_mode_a_direct_governance_import_strategy_correction_ready"
```

## Files Inspected

Governance files inspected read-only by marker search or presence check:

```text
0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
0_architecture/governance/agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
.gitignore
.graphifyignore
```

GBrain source metadata inspected read-only by targeted search:

```text
4_external/sources/gbrain-master/src/commands/import.ts
4_external/sources/gbrain-master/src/core/sync.ts
4_external/sources/gbrain-master/src/core/operations.ts
```

Sandbox metadata inspected read-only:

```text
9_artifacts/gbrain_sandbox/p12_0d/input_fixture/
9_artifacts/gbrain_sandbox/p12_0d/exports/
```

Direct governance input metadata inspected read-only:

```text
0_architecture/governance
0_architecture/governance/**/*.md via git ls-files metadata
```

No governance document contents were read for the direct input scope. Only filenames, extensions, Git visibility, and counts were reviewed.

Not inspected:

```text
DB internals under 9_artifacts/gbrain_sandbox/p12_0d/db/**
generated internals under 9_artifacts/gbrain_sandbox/p12_0d/gbrain_home/**
credentials
environment secrets
normal user .gbrain
node_modules contents
package caches
product/Siamese paths
Graphify outputs
external source roots outside 4_external/sources/gbrain-master/src/**
```

## Files Created

Created this correction record:

```text
0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction.md
```

## Files Modified

No existing file was modified by P12.0D-IMPORT-FIX.

## Commands Run

Approved preparation commands run:

```powershell
git status --short
Test-Path 0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
Test-Path 0_architecture/governance
Test-Path 4_external/sources/gbrain-master
Test-Path 4_external/sources/gbrain-master/src/cli.ts
Test-Path 4_external/sources/gbrain-master/src/commands/import.ts
Test-Path 4_external/sources/gbrain-master/src/core/sync.ts
Test-Path 9_artifacts/gbrain_sandbox/p12_0d
Test-Path 9_artifacts/gbrain_sandbox/p12_0d/input_fixture
Get-ChildItem -LiteralPath 9_artifacts/gbrain_sandbox/p12_0d/input_fixture -File -Force | Select-Object Name,Extension,Length
Get-ChildItem -LiteralPath 9_artifacts/gbrain_sandbox/p12_0d/exports -Force
```

Approved direct governance visibility checks run:

```powershell
git check-ignore -v 0_architecture/governance
git ls-files --cached --others --exclude-standard -- 0_architecture/governance
git ls-files --cached --others --exclude-standard -- 0_architecture/governance | Select-String "\.md$"
$GovernanceMarkdownVisible.Count
```

Approved read-only source searches run:

```powershell
Select-String -Path 4_external/sources/gbrain-master/src/commands/import.ts -Pattern "git ls-files","--exclude-standard","collectSyncableFiles","gitListSyncableFiles","markdown",".md",".mdx","--no-embed"
Select-String -Path 4_external/sources/gbrain-master/src/core/sync.ts -Pattern "isMarkdownFilePath",".md",".mdx"
Select-String -Path 4_external/sources/gbrain-master/src/core/operations.ts -Pattern "mcp_keyword_only","keyword"
```

Equivalent read-only grep tooling was also used for `.gitignore`, `.graphifyignore`, and marker confirmation.

Commands not run:

```text
No GBrain command
No gbrain command
No bun run src/cli.ts command
No GBrain init
No GBrain import
No GBrain search
No GBrain export
No graph-query
No Graphify
No Ollama
No provider command
No package install
No build
No test
No Git mutation
No staging command
```

## P12.0E Dependency Status

P12.0E review exists:

```text
0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
```

Confirmed P12.0E final marker:

```text
gbrain_sandbox_output_review_graph_query_follow_up_preparation_ready
```

Confirmed P12.0E decision markers:

```text
gbrain_p12_0d_zero_page_import_confirmed
```

## P12.0D Zero-Page Diagnosis Confirmation

P12.0D execution record confirms:

```text
Found 0 markdown files
0 pages imported
0 chunks created
No results.
Exported 0 pages
```

P12.0D input fixture metadata still shows physically present markdown files:

```text
agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md | .md | 23904 bytes
agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md | .md | 20195 bytes
README.md | .md | 139 bytes
contracts.py | .py | 11014 bytes
```

Root cause decision:

```yaml
RootCauseDecision:
  zero_page_import_confirmed: true
  fixture_files_physically_present: true
  markdown_fixture_files_physically_present: true
  markdown_extension_supported: true
  graph_query_slug_available: false
  likely_root_cause: "copied fixture input path was under ignored 9_artifacts and invisible to GBrain Git-aware import listing"
  original_governance_markdown_files_available: true
  graphify_precedent_consistent: true
```

Decision marker:

```text
gbrain_zero_page_import_root_cause_gitignore_visibility_confirmed
```

## Graphify-Like Ignore Visibility Precedent

Repository ignore metadata confirms the same visibility class:

```text
.gitignore includes 9_artifacts/
.graphifyignore excludes 9_artifacts/** and graphify-out/**
.graphifyignore explicitly re-includes 0_architecture/**/*.md
```

Observed `.gitignore` metadata:

```text
Line 20: 9_artifacts/
```

Observed `.graphifyignore` metadata:

```text
0_architecture/
9_artifacts/
graphify-out/
!0_architecture/
!0_architecture/**/
!0_architecture/**/*.md
9_artifacts/**
graphify-out/**
```

Interpretation:

```text
The P12.0D zero-page import pattern is consistent with earlier ignored-path visibility issues: synthetic copied input under generated artifact paths can be invisible to tools that honor ignore rules, while real governance markdown paths are intentionally visible.
```

## Direct Governance Input Visibility Review

Selected input directory:

```text
0_architecture/governance
```

Path check:

```yaml
governance_input_exists: true
```

Ignore check:

```yaml
git_check_ignore_0_architecture_governance_output: "<none>"
governance_input_ignored: false
```

Git visibility check:

```yaml
git_visible_governance_markdown_count: 117
git_visible_markdown_count_gt_zero: true
```

Decision:

```text
The direct real governance input scope is visible to Git-aware GBrain import discovery and contains more than one visible .md file.
```

Decision marker:

```text
gbrain_real_governance_input_scope_selected
```

## GBrain Import Source-Surface Confirmation

Targeted source review confirmed:

```text
src/commands/import.ts detects --no-embed.
src/commands/import.ts defaults import strategy to markdown.
src/commands/import.ts calls collectSyncableFiles(dir, { strategy }).
src/commands/import.ts contains a Git-aware fast path using git ls-files --cached --others --exclude-standard.
src/commands/import.ts returns the Git-aware file list directly when available.
src/core/sync.ts isMarkdownFilePath accepts .md and .mdx.
src/core/operations.ts checks search.mcp_keyword_only for keyword-only search behavior.
```

Relevant source-surface evidence:

```text
import.ts line 50: const noEmbed = args.includes('--no-embed')
import.ts line 176: const strategy: SyncStrategy = opts.strategy ?? 'markdown'
import.ts line 179: const allFiles = collectSyncableFiles(dir, { strategy })
import.ts line 522: git ls-files --cached --others --exclude-standard
import.ts line 538: ['-C', dir, 'ls-files', '--cached', '--others', '--exclude-standard', '-z']
import.ts lines 591-592: const gitFiles = gitListSyncableFiles(...); if (gitFiles) return gitFiles
sync.ts lines 173-174: isMarkdownFilePath returns path.endsWith('.md') || path.endsWith('.mdx')
operations.ts line 1443: search.mcp_keyword_only config is read for keyword-only path
```

Conclusion:

```yaml
direct_directory_import_supported: true
default_strategy_markdown: true
md_supported: true
mdx_supported: true
no_embed_supported: true
keyword_only_config_supported: true
git_visibility_matters_for_directory_import: true
```

## Corrected Direct Governance Import Strategy

Selected strategy:

```text
Import directly from the real governance tree: 0_architecture/governance
```

Future import path variable:

```powershell
$GovernanceInput = Join-Path $RepoRoot "0_architecture\governance"
```

Future import command candidate:

```powershell
bun run src/cli.ts import "$GovernanceInput" --no-embed
```

Rationale:

```text
The original .md governance files already live under the approved governance tree and are Git-visible. The previous failure came from importing copied fixtures inside ignored 9_artifacts. Direct governance import avoids artificial fixture duplication while preserving sandboxed generated state.
```

Rejected strategy:

```text
Do not import from 9_artifacts/gbrain_sandbox/**/input_fixture/ in the corrected rerun.
```

Reason:

```text
It may repeat the same ignored-path visibility failure.
```

Decision marker:

```text
gbrain_direct_governance_import_strategy_selected
```

## Corrected Rerun Sandbox Strategy

Selected fresh output sandbox root:

```text
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/
```

Future rerun subdirectories:

```text
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/gbrain_home/
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/db/
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/exports/
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/logs/
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/reports/
```

There is no copied input fixture directory in the corrected strategy.

Rationale:

```text
Use a fresh sandbox root to avoid mixing the zero-page P12.0D output with corrected direct-governance import output. Keep generated DB/home/export/log/report state local and ignored. Preserve the original P12.0D sandbox as evidence.
```

Decision markers:

```text
gbrain_outputs_remain_sandboxed
```

## Future P12.0D-RERUN Command Sequence

These commands are candidates only. P12.0D-IMPORT-FIX did not run them.

### Preflight

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

git check-ignore -v 0_architecture/governance
git ls-files --cached --others --exclude-standard -- 0_architecture/governance
git ls-files --cached --others --exclude-standard -- 0_architecture/governance | Select-String "\.md$"
```

Stop if no `.md` files are visible.

### Define Paths

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
```

### Stop If Prior Rerun Sandbox Already Exists

```powershell
Test-Path $SandboxRoot
```

If it exists:

```text
Stop and route to cleanup/review gate.
Do not overwrite.
Do not delete.
```

### Create Corrected Rerun Output Directories

```powershell
New-Item -ItemType Directory -Force -Path $GBrainHome,$DbPath,$ExportsPath,$LogsPath,$ReportsPath | Out-Null
```

### Execute Corrected Mode A Runtime

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

### Post-Run Verification

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

If `GBRAIN_HOME` still exists:

```powershell
Remove-Item Env:GBRAIN_HOME
```

Generated outputs under:

```text
9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/**
```

must remain local and untracked.

## Human Approval For Future P12.0D-RERUN

Future rerun must require this approval, or stricter equivalent:

```text
I approve P12.0D-RERUN Mode A direct-governance import only. Import directly from `0_architecture/governance` after proving Git-visible `.md` files exist there, use a fresh output sandbox under `9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/`, set shell-scoped `GBRAIN_HOME` only to the approved rerun sandbox home path, initialize GBrain with local PGLite under the approved rerun DB path using `--no-embedding`, force keyword-only search, import the governance directory with `--no-embed`, run the approved keyword search, export only to the approved rerun exports path, and keep all generated outputs local and untracked. Do not copy fixtures, do not run Ollama, do not pull models, do not generate embeddings, do not call providers, do not inspect credentials, do not use product/Siamese paths, do not run Graphify, do not run graph-query in this ticket, do not modify PATH, do not mutate Git, and do not stage sandbox outputs.
```

## Graph-Query Decision

Graph-query remains blocked.

Reason:

```text
The previous Mode A run imported 0 pages and no deterministic slug exists. P12.0D-IMPORT-FIX only prepares a corrected direct-governance rerun. Graph-query can be considered only after corrected Mode A import produces at least one page and a deterministic slug is identified.
```

Decision marker:

```text
gbrain_graph_query_still_blocked_until_successful_import
```

Future ticket after successful rerun:

```text
P12.0E-GOV-REVIEW - GBrain Governance Import Output Review / Graph Query Preparation
```

or:

```text
P12.0E-GRAPH-PREP - GBrain Graph Query Exact Slug Preparation
```

## Mode B / Ollama Boundary Confirmation

Mode B remains blocked.

P12.0D-IMPORT-FIX does not authorize:

```text
Ollama model inventory
Ollama model pull
Ollama inference
embedding generation
provider/API calls
hosted provider fallback
Graphify with Ollama
```

Decision markers:

```text
gbrain_mode_b_ollama_still_blocked
```

## Stop Rules For Future Rerun

Future P12.0D-RERUN must stop if:

```text
P12.0D-IMPORT-FIX missing
P12.0E missing
P12.0D success record missing
P12.INSTALL success record missing
Bun is not available
node_modules is missing
src/cli.ts is missing
0_architecture/governance is missing
0_architecture/governance is ignored
Git-visible .md count under 0_architecture/governance is 0
rerun sandbox root already exists
GBRAIN_HOME would point outside the rerun sandbox
DB path would point outside the rerun sandbox
exports path would point outside the rerun sandbox
any command would use embeddings
any command would call Ollama
any command would call providers
any command would inspect credentials
any command would use normal user .gbrain
any command would run Graphify
any command would run graph-query
any command would mutate Git
any command would stage generated outputs
```

If runtime import still produces 0 pages:

```text
Stop before graph-query.
Record safe functional limitation.
Route to P12.0D-IMPORT-RISK.
```

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction.md
```

Not created / not approved:

```text
No new sandbox directories
No copied fixture directory
No fixture copies
No governance modifications
No sandbox output modifications
No GBrain execution
No gbrain command execution
No bun run src/cli.ts execution
No GBrain init
No GBrain import
No GBrain search
No GBrain export
No graph-query
No embeddings
No Ollama command
No Ollama model pull
No provider/API call
No Graphify command
No credential inspection
No product/Siamese path access
No normal user .gbrain write
No DB/internal inspection
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

P12.0D-IMPORT-FIX is preparation only. It did not prove runtime import success because no GBrain command was authorized or run.

Direct governance import will import all Git-visible markdown under `0_architecture/governance`, not only the original three copied fixture markdown files. That broader direct governance scope is intentional in this correction and must be explicitly approved again before runtime.

The future rerun should not proceed directly to graph-query. It must first produce at least one imported page and expose a deterministic slug through approved output review.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.0D-RERUN - GBrain Mode A Direct Governance Import Sandbox Rerun
```

Do not proceed directly to graph-query.

## Commit Commands

If this correction record is accepted for commit, stage only the intended governance correction file. Do not stage sandbox outputs. Do not stage dependency artifacts. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction.md
git commit -m "Prepare GBrain direct governance import correction"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainModeADirectGovernanceImportStrategyCorrection:
  ticket: P12.0D-IMPORT-FIX
  date: "2026-07-10"
  target_file: "0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_strategy_correction.md"
  p12_0e_confirmed: true
  p12_0d_zero_page_import_confirmed: true
  p12_0d_fixture_markdown_files_present: true
  root_cause_gitignore_visibility_confirmed: true
  governance_input_exists: true
  governance_input_ignored: false
  governance_visible_markdown_count: 117
  direct_governance_import_strategy_selected: true
  real_governance_input_scope_selected: true
  copied_fixture_strategy_rejected: true
  rerun_sandbox_root_selected: "9_artifacts/gbrain_sandbox/p12_0d_governance_import_01/"
  outputs_remain_sandboxed: true
  future_runtime_approval_required: true
  graph_query_attempted: false
  graph_query_ready: false
  graph_query_still_blocked_until_successful_import: true
  mode_b_ollama_attempted: false
  mode_b_ollama_still_blocked: true
  provider_calls_attempted: false
  provider_calls_still_blocked: true
  gbrain_runtime_executed_now: false
  fixtures_copied_now: false
  sandbox_dirs_created_now: false
  sandbox_outputs_modified: false
  db_internals_inspected: false
  path_modified: false
  git_mutated: false
  recommended_next_ticket: "P12.0D-RERUN - GBrain Mode A Direct Governance Import Sandbox Rerun"
  final_marker: "gbrain_mode_a_direct_governance_import_strategy_correction_ready"
```

Final marker:

```text
gbrain_mode_a_direct_governance_import_strategy_correction_ready
```
