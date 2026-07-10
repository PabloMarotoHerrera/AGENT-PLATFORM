# GBrain Controlled Sandbox Exact Command Preparation

## Summary

P12.0D-PREP prepares the exact future Mode A sandbox command sequence for GBrain. It does not execute GBrain, does not run `bun run src/cli.ts`, does not create sandbox directories, does not copy fixtures, does not create DB/storage/output, does not run Ollama, does not run Graphify, and does not mutate Git.

P12.INSTALL completed successfully and local GBrain dependencies are present. The future runtime invocation must use the local source runtime from the GBrain source root because `gbrain` is not globally discoverable:

```text
working_directory: 4_external/sources/gbrain-master
runtime_prefix: bun run src/cli.ts
```

Mode A is selected for the first future execution gate: no embeddings, keyword-only search, local PGLite sandbox, local governed fixture only.

Result marker:

```text
gbrain_controlled_sandbox_exact_command_preparation_ready
```

Decision markers:

```text
gbrain_p12_0d_mode_a_selected
gbrain_source_runtime_command_prefix_selected
gbrain_sandbox_paths_prepared_for_future_execution
gbrain_fixture_set_prepared_for_future_execution
gbrain_runtime_execution_still_blocked
p12_0d_ready_for_execution_gate_after_prep
```

```yaml
P12_0D_PREP_Decision:
  ticket: P12.0D-PREP
  date: "2026-07-09"
  plan_only: true
  mode_selected: "Mode A - no embeddings, keyword-only, local PGLite sandbox"
  gbrain_runtime_invocation_prefix: "bun run src/cli.ts"
  gbrain_runtime_working_directory: "4_external/sources/gbrain-master"
  sandbox_root: "9_artifacts/gbrain_sandbox/p12_0d/"
  gbrain_home_scope: "shell-only under sandbox root"
  db_path_scope: "sandbox-only"
  fixture_copy_authorized_now: false
  runtime_execution_authorized_now: false
  graph_query_included_in_first_p12_0d: false
  mode_b_ollama_authorized_now: false
  p12_0d_ready_to_generate_execution_gate: true
  final_marker: "gbrain_controlled_sandbox_exact_command_preparation_ready"
```

## Files Inspected

Governance files inspected read-only:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
0_architecture/governance/agent_platform_gbrain_bun_refreshed_shell_verification_resolution.md
.graphifyignore
```

GBrain source metadata inspected read-only:

```text
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/src/cli.ts
4_external/sources/gbrain-master/src/commands/config.ts
4_external/sources/gbrain-master/src/commands/export.ts
4_external/sources/gbrain-master/src/commands/graph-query.ts
4_external/sources/gbrain-master/src/commands/import.ts
4_external/sources/gbrain-master/src/commands/init.ts
4_external/sources/gbrain-master/src/commands/search.ts
4_external/sources/gbrain-master/src/commands/sources.ts
4_external/sources/gbrain-master/src/core/config.ts
4_external/sources/gbrain-master/src/core/operations.ts
```

Presence-only fixture checks were performed for:

```text
README.md
0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md
0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md
3_platform/_governed_skeleton/agent_platform_mvp0/contracts.py
```

No credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, package caches, `node_modules` contents, normal user `.gbrain`, `9_artifacts`, `graphify-out`, product paths, generated outputs, raw Graphify outputs, or external source roots outside the approved GBrain source metadata paths were inspected.

## Files Created

```text
0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md
```

## Files Modified

No existing file was modified. The only file change for this ticket is the new P12.0D-PREP governance record.

## Commands Run

Allowed preparation commands run:

```powershell
git status --short
Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
Test-Path 0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
Test-Path 4_external/sources/gbrain-master
Test-Path 4_external/sources/gbrain-master/package.json
Test-Path 4_external/sources/gbrain-master/bun.lock
Test-Path 4_external/sources/gbrain-master/node_modules
Test-Path 4_external/sources/gbrain-master/node_modules/.bin
Test-Path 4_external/sources/gbrain-master/src/cli.ts
Get-Command bun -ErrorAction SilentlyContinue
bun --version
bun --revision
Get-Command gbrain -ErrorAction SilentlyContinue
Test-Path README.md
Test-Path 0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md
Test-Path 0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md
Test-Path 3_platform/_governed_skeleton/agent_platform_mvp0/contracts.py
```

Tooling note: the terminal shell initially interpreted PowerShell cmdlets through `cmd.exe`; those `Test-Path` / `Get-Command` attempts failed as shell-dispatch errors and were rerun through PowerShell with the same allowed checks. No GBrain runtime, sandbox, package-manager install, build, test, Ollama, Graphify, provider, secret, or Git mutation command was run.

Allowed read-only searches and file reads were used to confirm source command surfaces.

Forbidden commands were not run:

```text
bun run src/cli.ts
bun run
bun build
bun test
bun install
ollama
graphify
/graphify
```

## P12.INSTALL Dependency Status

P12.INSTALL exists at:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
```

P12.INSTALL final marker is present:

```text
gbrain_controlled_local_dependency_install_execution_record_ready
```

P12.INSTALL decision markers are present:

```text
gbrain_dependency_install_success
p12_0d_ready_to_generate_after_dependency_install
```

Dependency decision:

```yaml
p12_install_dependency_confirmed: true
p12_install_success_confirmed: true
gbrain_dependency_state_available: true
p12_0d_prep_authorized: true
```

## Bun / Dependency Availability Status

Preflight state:

```yaml
bun_get_command_succeeded: true
bun_source: "C:\\Users\\pablo\\.bun\\bin\\bun.exe"
bun_version: "1.3.14"
bun_revision: "1.3.14+0d9b296af"
gbrain_source_root_present: true
package_json_present: true
bun_lock_present: true
node_modules_present: true
node_modules_bin_present: true
src_cli_present: true
global_gbrain_available: false
```

`Get-Command gbrain -ErrorAction SilentlyContinue` returned no output. This is acceptable because P12.0D-PREP selects the local source runtime prefix and does not require a global `gbrain` command.

## GBrain Runtime Invocation Decision

P12.0D must not rely on a global `gbrain` command.

Selected future runtime invocation:

```yaml
GBrainRuntimeInvocation:
  global_gbrain_command_required: false
  global_gbrain_command_available_now: false
  source_runtime_prefix: "bun run src/cli.ts"
  working_directory: "4_external/sources/gbrain-master"
  build_required_for_mode_a: false
  build_authorized_now: false
  runtime_authorized_by_p12_0d_prep: false
  decision_marker: "gbrain_source_runtime_command_prefix_selected"
  runtime_block_marker: "gbrain_runtime_execution_still_blocked"
```

Source evidence:

```text
package.json maps bin.gbrain to src/cli.ts.
src/cli.ts routes CLI-only commands including init, import, search, export, graph-query, config, and sources.
src/cli.ts is already usable by Bun as a TypeScript source runtime after P12.INSTALL dependencies are present.
```

## Sandbox Path Decision

Future sandbox root:

```text
9_artifacts/gbrain_sandbox/p12_0d/
```

Future subdirectories:

```text
9_artifacts/gbrain_sandbox/p12_0d/input_fixture/
9_artifacts/gbrain_sandbox/p12_0d/gbrain_home/
9_artifacts/gbrain_sandbox/p12_0d/db/
9_artifacts/gbrain_sandbox/p12_0d/exports/
9_artifacts/gbrain_sandbox/p12_0d/logs/
9_artifacts/gbrain_sandbox/p12_0d/reports/
```

Future shell-scoped `GBRAIN_HOME` value:

```powershell
$env:GBRAIN_HOME = "<absolute path to repo>\9_artifacts\gbrain_sandbox\p12_0d\gbrain_home"
```

Rules:

```text
GBRAIN_HOME must be shell-scoped only.
Do not persist GBRAIN_HOME.
Do not write to normal user .gbrain.
Do not use system/user environment mutation.
Do not modify PATH.
Do not use product paths.
Do not use graphify-out.
```

Decision:

```yaml
SandboxPathDecision:
  sandbox_root: "9_artifacts/gbrain_sandbox/p12_0d/"
  gbrain_home_scope: "shell-only"
  db_path_scope: "sandbox-only"
  exports_path_scope: "sandbox-only"
  runtime_state_outside_sandbox_allowed: false
  sandbox_created_now: false
  decision_marker: "gbrain_sandbox_paths_prepared_for_future_execution"
```

Source evidence:

```text
src/core/config.ts honors GBRAIN_HOME as an absolute parent path and appends .gbrain.
src/core/config.ts gbrainPath(...) resolves under the active GBrain home.
P12.0C requires future DB/export/log/report outputs under 9_artifacts/gbrain_sandbox/p12_0d/ only.
```

## Fixture Decision

Future P12.0D fixture files and existence status:

| Fixture | Existence |
| --- | --- |
| `README.md` | `True` |
| `0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md` | `True` |
| `0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md` | `True` |
| `3_platform/_governed_skeleton/agent_platform_mvp0/contracts.py` | `True` |

Future destination:

```text
9_artifacts/gbrain_sandbox/p12_0d/input_fixture/
```

Future copy command candidates:

```powershell
Copy-Item -LiteralPath "README.md" -Destination (Join-Path $InputFixture "README.md")

Copy-Item -LiteralPath "0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md" -Destination (Join-Path $InputFixture "agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md")

Copy-Item -LiteralPath "0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md" -Destination (Join-Path $InputFixture "agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md")

Copy-Item -LiteralPath "3_platform/_governed_skeleton/agent_platform_mvp0/contracts.py" -Destination (Join-Path $InputFixture "contracts.py")
```

Fixture exclusions:

```text
.env*
credentials/**
secrets/**
tokens/**
provider configs
4_external/sources/**
9_artifacts/** except the approved sandbox root
2_products/**
product/**
products/**
node_modules/**
```

Decision:

```yaml
FixtureDecision:
  fixture_set_ready_for_future_execution: true
  fixture_files_copied_now: false
  destination_scope: "9_artifacts/gbrain_sandbox/p12_0d/input_fixture/"
  decision_marker: "gbrain_fixture_set_prepared_for_future_execution"
```

## Future P12.0D Command Sequence

The following commands are candidates for the next execution ticket only. P12.0D-PREP did not run them.

### Preflight

```powershell
git status --short

Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md

Test-Path 0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md

Test-Path 4_external/sources/gbrain-master

Test-Path 4_external/sources/gbrain-master/package.json

Test-Path 4_external/sources/gbrain-master/bun.lock

Test-Path 4_external/sources/gbrain-master/node_modules

Test-Path 4_external/sources/gbrain-master/src/cli.ts

Get-Command bun -ErrorAction SilentlyContinue

bun --version

bun --revision
```

### Define Absolute Paths

```powershell
$RepoRoot = (Get-Location).Path

$GBrainRoot = Join-Path $RepoRoot "4_external\sources\gbrain-master"

$SandboxRoot = Join-Path $RepoRoot "9_artifacts\gbrain_sandbox\p12_0d"

$InputFixture = Join-Path $SandboxRoot "input_fixture"

$GBrainHome = Join-Path $SandboxRoot "gbrain_home"

$DbPath = Join-Path $SandboxRoot "db"

$ExportsPath = Join-Path $SandboxRoot "exports"

$LogsPath = Join-Path $SandboxRoot "logs"

$ReportsPath = Join-Path $SandboxRoot "reports"
```

### Create Sandbox Directories

```powershell
New-Item -ItemType Directory -Force -Path $InputFixture,$GBrainHome,$DbPath,$ExportsPath,$LogsPath,$ReportsPath | Out-Null
```

### Copy Fixture Files

```powershell
Copy-Item -LiteralPath "README.md" -Destination (Join-Path $InputFixture "README.md")

Copy-Item -LiteralPath "0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md" -Destination (Join-Path $InputFixture "agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md")

Copy-Item -LiteralPath "0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md" -Destination (Join-Path $InputFixture "agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md")

Copy-Item -LiteralPath "3_platform/_governed_skeleton/agent_platform_mvp0/contracts.py" -Destination (Join-Path $InputFixture "contracts.py")
```

### Execute Mode A Runtime Commands

```powershell
Push-Location $GBrainRoot

$env:GBRAIN_HOME = $GBrainHome

bun run src/cli.ts init --pglite --path "$DbPath" --no-embedding

bun run src/cli.ts config set search.mcp_keyword_only true

bun run src/cli.ts import "$InputFixture" --no-embed

bun run src/cli.ts search "GBrain Graphify controlled sandbox evidence"

bun run src/cli.ts export --dir "$ExportsPath"

Remove-Item Env:GBRAIN_HOME

Pop-Location
```

### Post-Run Verification

```powershell
git status --short

Test-Path $SandboxRoot

Test-Path $InputFixture

Test-Path $GBrainHome

Test-Path $DbPath

Test-Path $ExportsPath
```

Generated outputs under:

```text
9_artifacts/gbrain_sandbox/p12_0d/**
```

must remain untracked local sandbox evidence unless a separate generated-output review approves tracking.

Command-surface evidence:

```text
src/commands/init.ts confirms --pglite, --path, and --no-embedding.
src/commands/config.ts confirms config set <key> <value>.
src/core/operations.ts confirms search.mcp_keyword_only routes search to keyword-only retrieval.
src/commands/import.ts confirms --no-embed.
src/commands/export.ts confirms --dir.
src/commands/graph-query.ts confirms graph-query <slug> [--type T] [--depth N] [--direction in|out|both], but graph-query is deferred.
```

## Graph-Query Decision

Do not include `graph-query` in the first P12.0D execution.

Reason:

```text
P12.0D-PREP does not know the exact imported slug before runtime output exists.
Using a placeholder slug would make the first runtime command sequence non-deterministic.
Graph traversal can be gated after reviewing the first sandbox execution output.
```

Deferred ticket candidate:

```text
P12.0E - GBrain Sandbox Graph Query Follow-Up
```

or:

```text
P12.0D-GRAPH - GBrain Sandbox Graph Query Exact Slug Execution
```

Decision:

```yaml
graph_query_included_in_first_p12_0d: false
graph_query_deferred_until_import_output_review: true
```

## Mode B / Ollama Decision

Mode B remains blocked.

P12.0D-PREP does not authorize:

```text
Ollama model inventory
Ollama model pull
Ollama inference
embedding generation
provider/API calls
hosted provider fallback
Graphify with Ollama
```

Mode B may be considered only after Mode A succeeds:

```text
P12.0F - GBrain Local Ollama Embedding Sandbox Preparation
```

or separate Graphify path:

```text
P10.OLLAMA.0 - Graphify Ollama Local Provider Command / Scope Amendment
```

Decision:

```yaml
mode_a_selected_now: true
mode_b_ollama_authorized_now: false
embedding_generation_authorized_now: false
provider_calls_authorized_now: false
decision_marker: "gbrain_p12_0d_mode_a_selected"
```

## P12.0D Handoff Decision

P12.0D may now be generated as a separate execution gate. P12.0D-PREP does not authorize P12.0D execution.

Decision:

```yaml
P12_0D_HandoffDecision:
  status: "ready_to_generate_execution_gate"
  p12_0d_execution_authorized_now: false
  required_next_ticket: "P12.0D - GBrain Controlled Local Memory Sandbox Execution"
  decision_marker: "p12_0d_ready_for_execution_gate_after_prep"
```

Future P12.0D execution must require this approval, or a stricter equivalent:

```text
I approve P12.0D Mode A only. Create `9_artifacts/gbrain_sandbox/p12_0d/`, copy only the approved fixture files into `input_fixture/`, set shell-scoped `GBRAIN_HOME` only to the approved sandbox home path, initialize GBrain with local PGLite under the approved sandbox DB path using `--no-embedding`, force keyword-only search, import the approved fixture with `--no-embed`, run the approved keyword search, export only to the approved sandbox exports path, and keep all generated outputs local and untracked. Do not run Ollama, do not pull models, do not generate embeddings, do not call providers, do not inspect credentials, do not use product/Siamese paths, do not run Graphify, do not run graph-query in this ticket, do not modify PATH, do not mutate Git, and do not stage sandbox outputs.
```

## Stop Rules For Future P12.0D

Future P12.0D must stop if:

```text
P12.0D-PREP is missing
P12.INSTALL success record is missing
Bun is not available
node_modules is missing
src/cli.ts is missing
working directory is not 4_external/sources/gbrain-master
any fixture file is missing
any command would read outside approved fixture/sandbox paths
GBRAIN_HOME would point outside sandbox
DB path would point outside sandbox
exports path would point outside sandbox
any command would use embeddings
any command would call Ollama
any command would call OpenAI/Anthropic/Gemini/provider APIs
any command would inspect credentials
any command would use normal user .gbrain
any command would run Graphify
any command would mutate Git
any command would stage generated outputs
```

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md
```

Not created / not approved:

```text
No sandbox directories
No fixture copies
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
No Graphify command
No provider/API call
No credential inspection
No DB/storage/output
No PATH mutation
No Git mutation
No git add .
```

## Limitations

P12.0D-PREP did not create the sandbox root and did not copy fixtures. Fixture contents were not re-read in this ticket; only source/interface metadata and fixture path existence were checked.

P12.0D-PREP did not verify runtime behavior. All future runtime behavior remains gated by P12.0D.

`graph-query` is deferred because the imported slug is not known until after runtime import output exists.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.0D - GBrain Controlled Local Memory Sandbox Execution
```

If the operator wants one more approval layer before execution, use:

```text
P12.0D-AUTH - GBrain Controlled Sandbox Runtime Approval
```

## Commit Commands

If this preparation record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md
git commit -m "Prepare GBrain controlled sandbox commands"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainControlledSandboxExactCommandPreparation:
  ticket: P12.0D-PREP
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_controlled_sandbox_exact_command_preparation.md"
  p12_install_success_confirmed: true
  gbrain_dependency_state_confirmed: true
  bun_available: true
  bun_version: "1.3.14"
  bun_revision: "1.3.14+0d9b296af"
  source_root_present: true
  node_modules_present: true
  node_modules_bin_present: true
  src_cli_present: true
  global_gbrain_available: false
  mode_a_selected: true
  source_runtime_prefix_selected: "bun run src/cli.ts"
  source_runtime_working_directory: "4_external/sources/gbrain-master"
  sandbox_root: "9_artifacts/gbrain_sandbox/p12_0d/"
  gbrain_home_scope: "shell-only sandbox path"
  db_path_scope: "sandbox-only"
  fixture_set_ready: true
  runtime_execution_authorized_now: false
  graph_query_included_in_first_p12_0d: false
  mode_b_ollama_authorized_now: false
  provider_calls_authorized_now: false
  sandbox_created_now: false
  fixtures_copied_now: false
  db_created_now: false
  git_mutated: false
  p12_0d_ready_to_generate_execution_gate: true
  final_marker: "gbrain_controlled_sandbox_exact_command_preparation_ready"
```

Final marker:

```text
gbrain_controlled_sandbox_exact_command_preparation_ready
```
