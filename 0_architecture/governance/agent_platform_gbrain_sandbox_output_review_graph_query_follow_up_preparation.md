# GBrain Sandbox Output Review / Graph Query Follow-Up Preparation

## Summary

P12.0E reviewed the P12.0D sandbox output metadata and allowed GBrain import source surfaces without rerunning GBrain, modifying sandbox outputs, inspecting DB internals, running graph-query, or staging anything.

Result marker:

```text
gbrain_sandbox_output_review_graph_query_follow_up_preparation_ready
```

Decision markers:

```text
gbrain_p12_0d_zero_page_import_confirmed
gbrain_fixture_files_present_in_sandbox
gbrain_import_path_or_strategy_issue_candidate_identified
gbrain_graph_query_still_blocked_no_slug
gbrain_mode_a_rerun_required_before_graph_query
gbrain_mode_b_ollama_still_blocked
gbrain_provider_calls_still_blocked
p12_0d_import_fix_ready_to_generate
p12_0d_rerun_ready_after_import_fix_preparation
```

Finding:

```text
The approved fixture files are present in the sandbox input directory, including three .md files. P12.0D still imported zero pages because the import collector likely used its Git-aware fast path inside the repository and honored Git exclude rules for the ignored 9_artifacts sandbox path. In that case, git ls-files returned an empty list and collectSyncableFiles returned it directly instead of falling back to recursive filesystem walking.
```

Graph-query remains blocked because P12.0D produced no imported page slug.

```yaml
P12_0E_Decision:
  ticket: P12.0E
  date: "2026-07-10"
  outcome: "Outcome A - zero-page import caused by import path / Git-aware strategy mismatch candidate"
  p12_0d_record_confirmed: true
  zero_page_import_confirmed: true
  fixture_files_present: true
  fixture_markdown_files_present: true
  exports_empty: true
  deterministic_imported_slug_available: false
  graph_query_ready: false
  graph_query_still_blocked: true
  direct_gbrain_execution_performed: false
  sandbox_outputs_modified: false
  db_internals_inspected: false
  mode_b_ollama_still_blocked: true
  provider_calls_still_blocked: true
  recommended_next_ticket: "P12.0D-IMPORT-FIX - GBrain Mode A Import Path / Strategy Correction"
  final_marker: "gbrain_sandbox_output_review_graph_query_follow_up_preparation_ready"
```

## Files Inspected

Governance files inspected read-only:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
```

GBrain source surfaces inspected read-only by targeted search or targeted line reads:

```text
4_external/sources/gbrain-master/src/cli.ts
4_external/sources/gbrain-master/src/commands/import.ts
4_external/sources/gbrain-master/src/core/operations.ts
4_external/sources/gbrain-master/src/core/sync.ts
```

Sandbox metadata inspected read-only:

```text
9_artifacts/gbrain_sandbox/p12_0d/
9_artifacts/gbrain_sandbox/p12_0d/input_fixture/
9_artifacts/gbrain_sandbox/p12_0d/exports/
```

Only top-level sandbox directory names, input fixture filename/extension/size metadata, and exports top-level entries were reviewed.

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

Created this governance review document:

```text
0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
```

## Files Modified

No existing file was modified by P12.0E.

## Commands Run

Approved review commands run:

```powershell
git status --short
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
Test-Path 4_external/sources/gbrain-master
Test-Path 4_external/sources/gbrain-master/package.json
Test-Path 4_external/sources/gbrain-master/src/cli.ts
Test-Path 4_external/sources/gbrain-master/src/commands/import.ts
Test-Path 4_external/sources/gbrain-master/src/core/operations.ts
Test-Path 9_artifacts/gbrain_sandbox/p12_0d
Test-Path 9_artifacts/gbrain_sandbox/p12_0d/input_fixture
Test-Path 9_artifacts/gbrain_sandbox/p12_0d/db
Test-Path 9_artifacts/gbrain_sandbox/p12_0d/gbrain_home
Test-Path 9_artifacts/gbrain_sandbox/p12_0d/exports
Get-ChildItem -LiteralPath 9_artifacts/gbrain_sandbox/p12_0d -Force
Get-ChildItem -LiteralPath 9_artifacts/gbrain_sandbox/p12_0d/input_fixture -File -Force | Select-Object Name,Extension,Length
Get-ChildItem -LiteralPath 9_artifacts/gbrain_sandbox/p12_0d/exports -Force
```

Allowed read-only marker searches were performed for P12.0D execution markers, zero-page evidence, P12.0D-PREP import boundary text, and import source discovery patterns.

Forbidden commands were not run:

```text
No GBrain command
No gbrain command
No bun run src/cli.ts command
No init
No config
No import
No search
No export
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

## P12.0D Dependency Status

P12.0D execution record exists:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_memory_sandbox_execution_record.md
```

Confirmed final marker:

```text
gbrain_controlled_local_memory_sandbox_execution_record_ready
```

Confirmed P12.0D success markers:

```text
gbrain_mode_a_sandbox_execution_success
p12_0e_ready_after_mode_a_execution
```

Confirmed P12.0D zero-page evidence:

```text
Found 0 markdown files
0 pages imported
0 chunks created
No results.
Exported 0 pages
```

P12.0D-PREP confirmed the runtime boundary included:

```text
input_fixture
bun run src/cli.ts import "$InputFixture" --no-embed
```

## Sandbox Metadata Review

Sandbox root exists:

```text
9_artifacts/gbrain_sandbox/p12_0d/
```

Approved top-level sandbox directories observed:

```text
db/
exports/
gbrain_home/
input_fixture/
logs/
reports/
```

Path checks:

```yaml
sandbox_root_exists: true
input_fixture_exists: true
db_exists: true
gbrain_home_exists: true
exports_exists: true
```

Generated DB/home/log/report internals were not inspected.

## Input Fixture Metadata Review

Fixture files present in `input_fixture/`:

```text
agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md | .md | 23904 bytes
agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md | .md | 20195 bytes
contracts.py | .py | 11014 bytes
README.md | .md | 139 bytes
```

Fixture metadata decision:

```yaml
approved_fixture_file_count_present: 4
markdown_fixture_file_count_present: 3
python_fixture_file_count_present: 1
fixture_files_missing: false
fixture_copy_failure_likely: false
```

Decision marker:

```text
gbrain_fixture_files_present_in_sandbox
```

## Export Metadata Review

Exports directory exists:

```text
9_artifacts/gbrain_sandbox/p12_0d/exports/
```

Top-level exports observed:

```text
<none>
```

Export metadata decision:

```yaml
exports_directory_exists: true
exports_top_level_entries: 0
exports_empty: true
```

## Zero-Page Import Confirmation

P12.0D import command completed but produced no imported content:

```text
Found 0 markdown files
0 pages imported
0 chunks created
```

Search and export effects were consistent with zero imported pages:

```text
No results.
Exported 0 pages
```

Decision marker:

```text
gbrain_p12_0d_zero_page_import_confirmed
```

No deterministic imported slug is available from approved output metadata.

## GBrain Import Source-Surface Review

Relevant `src/commands/import.ts` behavior:

```text
Line 164: dirArg is the first non-flag argument.
Line 176: default import strategy is markdown.
Lines 178-185: import logs collect_files and prints Found <N> markdown files.
Lines 497-507: markdown strategy collects isMarkdownFilePath(path).
Lines 522-524: Git-aware collection intentionally honors .gitignore via git ls-files --cached --others --exclude-standard.
Lines 529-538: gitListSyncableFiles runs git -C <dir> ls-files --cached --others --exclude-standard -z.
Lines 591-592: collectSyncableFiles returns gitFiles directly when gitListSyncableFiles returns a value.
Lines 598-646: recursive filesystem walk is only reached if gitListSyncableFiles returns null.
```

Relevant `src/core/sync.ts` behavior found by targeted source search:

```text
Line 173: export function isMarkdownFilePath(path: string): boolean
Line 174: return path.endsWith('.md') || path.endsWith('.mdx')
```

Import source-surface conclusions:

```yaml
default_strategy: "markdown"
markdown_extensions_supported: [".md", ".mdx"]
no_embed_affects_collection: false
recursive_fs_walk_exists: true
recursive_fs_walk_reached_when_git_files_empty: false
git_aware_fast_path_honors_exclude_standard: true
empty_git_file_list_short_circuits_fs_walk: true
```

## Likely Zero-Page Cause Classification

Outcome A applies: zero-page import caused by an import path / strategy mismatch candidate.

The strongest candidate is:

```text
The input fixture path was under 9_artifacts/gbrain_sandbox/p12_0d/input_fixture inside the repository. The importer detected a Git worktree and used git ls-files --cached --others --exclude-standard. Because the sandbox path does not appear in git status output and is likely ignored/excluded, git returned zero syncable markdown files. collectSyncableFiles returned that empty Git result directly, so the recursive filesystem walker never inspected the three .md fixture files that are physically present.
```

Why other causes are less likely:

```yaml
fixture_files_missing: false
extension_filter_mismatch_for_markdown_files: false
  reason: "Three copied fixture files end in lowercase .md, and source search confirms .md/.mdx are accepted."
no_embed_collection_issue: false
  reason: "--no-embed affects embedding preflight; collection still uses collectSyncableFiles."
non_recursive_discovery_issue: false
  reason: "Files are top-level in input_fixture, so recursion is not required."
unsupported_python_file_expected: true
  reason: "contracts.py is not expected to import under default markdown strategy, but the three .md files should have been considered if the filesystem walker or a non-ignored Git listing saw them."
registered_source_required_candidate: "not supported by observed evidence"
  reason: "The import command directly accepts a directory and reached collect_files for that directory."
```

Decision marker:

```text
gbrain_import_path_or_strategy_issue_candidate_identified
```

## Graph-Query Readiness Decision

Graph-query remains blocked.

Decision marker:

```text
gbrain_graph_query_still_blocked_no_slug
```

Reason:

```text
P12.0D imported 0 pages, exported 0 pages, and produced no deterministic imported slug from approved output metadata. Running graph-query now would not be deterministic and is outside P12.0E scope.
```

```yaml
graph_query_attempted_in_p12_0e: false
deterministic_imported_slug_available: false
direct_graph_query_ready: false
separate_graph_query_gate_required: true
```

## Mode B / Ollama Boundary Confirmation

Mode B remains blocked.

Decision markers:

```text
gbrain_mode_b_ollama_still_blocked
gbrain_provider_calls_still_blocked
```

P12.0E did not authorize or run:

```text
Ollama model inventory
Ollama model pull
Ollama inference
embedding generation
provider/API calls
hosted provider fallback
Graphify with Ollama
```

## Recommended Correction Path

Recommended next ticket:

```text
P12.0D-IMPORT-FIX - GBrain Mode A Import Path / Strategy Correction
```

Correction requirement:

```text
A rerun must make the approved .md fixtures visible to GBrain's import collector without staging generated outputs, creating embeddings, using providers, running Graphify, running graph-query, or modifying Git.
```

Prepared correction candidates, not executed:

```text
1. Preferred: use a new Mode A rerun sandbox for DB/home/exports under 9_artifacts/gbrain_sandbox/p12_0d_rerun/, but place the import fixture input in a separately approved non-ignored path or outside any Git worktree so collectSyncableFiles falls back to the filesystem walker or receives non-ignored Git files.
2. Alternative: use a separately approved non-ignored fixture path under the repository and keep it untracked, then import that directory. This must be checked with read-only metadata before runtime and must not stage fixture copies.
3. Alternative: copy fixture files under the GBrain source root only if separately approved, because it writes into an external source checkout and may create nested worktree noise.
4. Source-level alternative: prepare a GBrain-side import option to force filesystem walking / bypass Git-aware listing for explicitly supplied fixture directories. No such runtime option was confirmed in the reviewed source surface.
```

Important rerun warning:

```text
Using only a new sandbox root under 9_artifacts/gbrain_sandbox/p12_0d_rerun/ may not fix the import if the input fixture directory remains ignored by Git. The correction must address import visibility, not just sandbox freshness.
```

Rerun remains Mode A only and must still block:

```text
Ollama
embeddings
providers
Graphify
product/Siamese paths
normal user .gbrain
PATH mutation
Git mutation
staging sandbox outputs
```

Decision markers:

```text
gbrain_mode_a_rerun_required_before_graph_query
p12_0d_import_fix_ready_to_generate
p12_0d_rerun_ready_after_import_fix_preparation
```

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
```

Not created / not approved:

```text
No new sandbox directories
No fixture copies
No fixture modifications
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

This review did not inspect DB internals, generated home internals, fixture file contents, or `.gitignore` contents.

The ignore-rule conclusion is a strong source-surface and metadata-based candidate, not a direct `.gitignore` inspection result. The evidence is that the importer uses `git ls-files --exclude-standard`, the fixture path is under `9_artifacts`, the sandbox outputs do not appear in `git status --short`, and physically present `.md` files were not collected.

No correction candidate was executed in P12.0E.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.0D-IMPORT-FIX - GBrain Mode A Import Path / Strategy Correction
```

The next ticket should prepare an exact rerun boundary that proves the fixture input directory will be visible to GBrain import before running Mode A again.

## Commit Commands

If this review record is accepted for commit, stage only the intended governance review file. Do not stage sandbox outputs. Do not stage dependency artifacts. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md
git commit -m "Review GBrain sandbox output and graph query follow-up"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainSandboxOutputReviewGraphQueryFollowUpPreparation:
  ticket: P12.0E
  date: "2026-07-10"
  target_file: "0_architecture/governance/agent_platform_gbrain_sandbox_output_review_graph_query_follow_up_preparation.md"
  p12_0d_execution_record_confirmed: true
  p12_0d_success_markers_confirmed: true
  zero_page_import_confirmed: true
  sandbox_root_exists: true
  approved_top_level_sandbox_dirs_exist: true
  fixture_files_present_in_sandbox: true
  markdown_fixture_files_present: 3
  python_fixture_files_present: 1
  exports_empty: true
  deterministic_imported_slug_available: false
  import_cause_classification: "Git-aware import listing likely excluded ignored 9_artifacts fixture path"
  graph_query_attempted: false
  graph_query_ready: false
  graph_query_still_blocked: true
  gbrain_runtime_executed_in_p12_0e: false
  sandbox_outputs_modified: false
  db_internals_inspected: false
  embeddings_generated: false
  ollama_attempted: false
  provider_calls_attempted: false
  graphify_attempted: false
  path_modified: false
  git_mutated: false
  recommended_next_ticket: "P12.0D-IMPORT-FIX - GBrain Mode A Import Path / Strategy Correction"
  final_marker: "gbrain_sandbox_output_review_graph_query_follow_up_preparation_ready"
```

Final marker:

```text
gbrain_sandbox_output_review_graph_query_follow_up_preparation_ready
```
