# Canonical Local Memory Sandbox Spike Record

## Summary

P12.9 executed one approved controlled GBrain Mode A runtime sequence in a fresh local sandbox. The spike created a canonical local memory sandbox candidate under the approved `9_artifacts` root, initialized local PGLite with `--no-embedding`, forced keyword-only search, imported the Git-visible governance markdown corpus with `--no-embed`, ran only the five approved keyword search smoke queries, and exported generated evidence to the approved sandbox exports path.

The sandbox is not production memory. It is not authority. It is local/untracked generated evidence and derived retrieval infrastructure only.

Result marker:

```text
canonical_local_memory_sandbox_spike_ready
```

Decision markers:

```text
p12_9_canonical_memory_sandbox_execution_success
p12_9_fresh_sandbox_created
p12_9_keyword_only_gbrain_index_created
p12_9_canonical_governance_input_imported
p12_9_memory_search_smoke_success
p12_9_exports_generated_local_untracked
p12_9_no_embeddings_no_ollama_no_providers
p12_9_no_graph_query
p12_9_no_production_memory_authority
p12_9_cleanup_dependency_preserved
p12_11_retention_rollback_ready_after_memory_spike
```

```yaml
P12_9_Canonical_Local_Memory_Sandbox_Spike_Record:
  ticket: P12.9
  date: "2026-07-10"
  outcome: "Outcome A - success"
  human_runtime_approval_present: true
  execution_attempts_allowed: 1
  gbrain_runtime_sequence_attempted_once: true
  fresh_sandbox_created: true
  sandbox_root: "9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01"
  gbrain_home_scoped_to_sandbox: true
  gbrain_home_env_removed_after_runtime: true
  local_pglite_init_success: true
  keyword_only_config_success: true
  governance_import_success: true
  git_visible_governance_markdown_count: 129
  imported_markdown_files: 129
  imported_pages: 129
  skipped_pages: 0
  import_errors: 0
  chunks_created: 1763
  approved_search_smokes_success: true
  export_success: true
  exported_pages: 129
  generated_outputs_confined_to_sandbox: true
  generated_outputs_staged: false
  embeddings_generated: false
  ollama_attempted: false
  provider_calls_attempted: false
  graphify_attempted: false
  graph_query_attempted: false
  gstack_command_attempted: false
  skill_execution_attempted: false
  mcp_registration_attempted: false
  browser_daemon_attempted: false
  credential_inspection_attempted: false
  product_or_siamese_path_access_attempted: false
  normal_user_gbrain_write_attempted: false
  normal_user_gstack_write_attempted: false
  db_internal_inspection_attempted: false
  generated_home_internal_inspection_attempted: false
  git_mutated: false
  production_memory_created: false
  p12_11_ready_after_spike: true
  final_marker: "canonical_local_memory_sandbox_spike_ready"
```

## Files Inspected

Governance files inspected read-only by path/marker checks:

```text
0_architecture/governance/agent_platform_memory_store_integration_design.md
0_architecture/governance/agent_platform_memory_authority_model.md
0_architecture/governance/agent_platform_gbrain_adoption_graphify_semantic_replacement_decision.md
0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_sandbox_rerun_record.md
```

GBrain metadata path checks performed:

```text
4_external/sources/gbrain-master
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
4_external/sources/gbrain-master/node_modules
4_external/sources/gbrain-master/src/cli.ts
```

Input scope checked:

```text
0_architecture/governance
```

Post-run top-level sandbox metadata checked only:

```text
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/exports/ top-level file names and lengths only
```

Not inspected:

```text
.env
.env.*
credentials/**
secrets/**
provider configs
token stores
browser auth
local credential stores
API keys
Claude credentials
Claude session files
Anthropic credentials
OpenAI credentials
Gemini credentials
Ollama configs
normal user .gbrain
normal user .gstack
normal user .claude
normal user .codex
normal user .config/opencode
browser cookie stores
graphify-out/**
9_artifacts/** contents outside approved P12.9 top-level metadata checks
2_products/**
product/**
products/**
raw Graphify outputs
4_external/sources/gbrain-master/node_modules/**
4_external/sources/gstack-main/node_modules/**
global package caches
Bun cache contents
DB internals under 9_artifacts/**
generated home internals under 9_artifacts/**
```

## Files Created

Created approved sandbox directories and generated manifest/export/state under:

```text
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/
```

Created approved subdirectories:

```text
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/gbrain_home/
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/db/
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/exports/
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/logs/
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/reports/
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/manifest/
```

Manifest files created under approved sandbox manifest path:

```text
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/manifest/git_visible_governance_markdown_files.txt
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/manifest/canonical_memory_manifest.md
```

Created or updated the single allowed governance execution record:

```text
0_architecture/governance/agent_platform_canonical_local_memory_sandbox_spike_record.md
```

## Files Modified

The single allowed governance execution record was updated with this successful approved-run record:

```text
0_architecture/governance/agent_platform_canonical_local_memory_sandbox_spike_record.md
```

No GBrain source, GStack source, existing governance file other than this output record, product/Siamese file, shell profile, PATH configuration, credential file, or Git metadata was modified.

## Commands Run

Allowed preflight command group was run:

```powershell
git status --short
Test-Path dependency governance files
Test-Path GBrain runtime metadata paths
Get-Command bun -ErrorAction SilentlyContinue
bun --version
bun --revision
git check-ignore -q 0_architecture/governance
git ls-files --cached --others --exclude-standard -- 0_architecture/governance
Test-Path 9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01
```

Observed preflight results:

```yaml
memory_store_integration_design_present: true
memory_authority_model_present: true
gbrain_adoption_decision_present: true
gbrain_mode_a_rerun_record_present: true
governance_input_present: true
gbrain_root_present: true
gbrain_package_json_present: true
gbrain_bun_lock_present: true
gbrain_node_modules_present: true
gbrain_cli_present: true
bun_available: true
bun_command: "C:/Users/pablo/.bun/bin/bun.exe"
bun_version: "1.3.14"
bun_revision: "1.3.14+0d9b296af"
governance_input_ignored: false
git_visible_governance_markdown_count: 129
sandbox_root_existed_before_setup: false
```

Allowed sandbox setup command group was run. It created only approved sandbox directories and manifest files.

Approved GBrain Mode A runtime sequence was run once from:

```text
4_external/sources/gbrain-master
```

Approved runtime commands run once:

```powershell
bun run src/cli.ts init --pglite --path "$DbPath" --no-embedding
bun run src/cli.ts config set search.mcp_keyword_only true
bun run src/cli.ts import "$GovernanceInput" --no-embed
bun run src/cli.ts search "memory authority model GBrain derived index canonical source"
bun run src/cli.ts search "GBrain Graphify semantic replacement memory retrieval authority"
bun run src/cli.ts search "memory store integration canonical source reference GBrain index"
bun run src/cli.ts search "GStack skill memory not authority execution gate"
bun run src/cli.ts search "CLEAN production operational memory blocked"
bun run src/cli.ts export --dir "$ExportsPath"
```

Post-run metadata command group was run:

```powershell
git status --short
Test-Path sandbox/input/state paths
Test-Path Env:GBRAIN_HOME
Get-ChildItem -LiteralPath $SandboxRoot -Force
Get-ChildItem -LiteralPath $ExportsPath -Force | Select-Object Name,Length
```

An initial PowerShell wrapper with malformed manifest here-string syntax failed at parse time before sandbox creation or runtime execution. A sandbox path check immediately after that failure confirmed the sandbox root was still absent. The approved GBrain runtime sequence itself was then run exactly once and completed successfully.

Commands explicitly not run:

```text
gbrain
gbrain --help
gbrain --version
bun install
bun build
bun test
bunx
npm
node
npx
python
pip
docker
ollama
graphify
/graphify
gstack
graph-query
provider commands
MCP servers
browser daemons
ngrok
builds
scripts
CI
git add
git commit
git push
```

## Human Approval Status

Explicit runtime approval was present outside the ticket body.

Classification:

```yaml
approval_required_for_runtime: true
approval_present_outside_ticket_body: true
runtime_may_execute_once: true
runtime_attempts_used: 1
```

## P12.3 Dependency Status

P12.3 exists:

```text
0_architecture/governance/agent_platform_memory_authority_model.md
```

Required marker confirmed:

```text
memory_authority_model_ready
```

Relevant confirmed markers and concepts:

```text
memory_conflict_resolution_rules_defined
cleanup_required_before_agent_taxonomy_production
Tier B - Derived memory index
Tier C - Generated evidence
```

P12.3 authority rule preserved:

```text
Derived memory indexes support retrieval and context assembly, but they are not authority. Generated outputs are supporting evidence only by default.
```

## P12.5 Dependency Status

P12.5 exists:

```text
0_architecture/governance/agent_platform_gbrain_adoption_graphify_semantic_replacement_decision.md
```

Required marker confirmed:

```text
gbrain_adoption_graphify_semantic_replacement_decision_ready
```

Relevant confirmed markers and facts:

```text
gbrain_adopted_as_local_semantic_retrieval_candidate
gbrain_not_adopted_as_authority
GBrain is not adopted as skill execution authority
GStack not validated
```

P12.5 boundary preserved:

```text
GBrain may support local retrieval and context assembly, but it is not authority and does not approve execution, memory promotion, Graphify replacement for visualization, or GStack adoption.
```

## P12.7 Dependency Status

P12.7 exists:

```text
0_architecture/governance/agent_platform_memory_store_integration_design.md
```

Required marker confirmed:

```text
memory_store_integration_design_ready
```

Relevant confirmed design rule:

```text
The memory store is a governed retrieval and context assembly layer that references canonical sources and derived indexes without becoming authority.
```

P12.7 handoff preserved:

```text
P12.9 used a fresh canonical local memory sandbox, keyword-only mode, no embeddings, no Ollama, no providers, no Graphify, no graph-query, and local/untracked generated outputs only.
```

## P12.0D-RERUN Dependency Status

P12.0D-RERUN exists:

```text
0_architecture/governance/agent_platform_gbrain_mode_a_direct_governance_import_sandbox_rerun_record.md
```

Required marker confirmed:

```text
gbrain_mode_a_direct_governance_import_sandbox_rerun_record_ready
```

Relevant confirmed evidence:

```text
gbrain_direct_governance_import_rerun_success
119 pages imported
1644 chunks created
```

P12.0D-RERUN remains historical feasibility evidence only. It was not reused as production memory.

## Preflight Status

Preflight succeeded.

```yaml
p12_7_marker_confirmed: true
p12_3_marker_confirmed: true
p12_5_marker_confirmed: true
p12_0d_rerun_marker_confirmed: true
gbrain_runtime_prerequisites_present: true
bun_available: true
governance_input_exists: true
governance_input_ignored: false
git_visible_governance_markdown_count: 129
sandbox_root_existed_before_setup: false
```

## Sandbox Path Status

Approved sandbox root:

```text
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/
```

Post-run top-level path status:

```yaml
sandbox_root_exists: true
gbrain_home_exists: true
db_exists: true
exports_exists: true
logs_exists: true
reports_exists: true
manifest_exists: true
```

Observed top-level sandbox entries:

```text
db/
exports/
gbrain_home/
logs/
manifest/
reports/
```

No recursive DB, home, export, log, or report internals were inspected.

## Input Scope Status

Approved primary input scope:

```text
0_architecture/governance
```

Input status:

```yaml
governance_input_exists: true
governance_input_ignored: false
git_visible_markdown_count: 129
input_classification: "canonical governance baseline import"
```

## Runtime Execution Status

Runtime execution status:

```yaml
runtime_started: true
runtime_completed: true
gbrain_runtime_sequence_attempted_once: true
alternate_commands_attempted: false
debug_chain_opened: false
```

GBrain init emitted advisory text about search mode, missing GStack, and optional recommended skills. No recommended GStack, skillpack, provider, MCP, or GStack action was taken.

## Init Result

Init command:

```powershell
bun run src/cli.ts init --pglite --path "$DbPath" --no-embedding
```

Observed result:

```yaml
init_attempted: true
local_pglite_init_success: true
migrations_applied: 117
schema_pack: "gbrain-base-v2"
embedding_setup_deferred_by_no_embedding: true
brain_ready_path: "9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/db"
pages_after_init: 0
```

## Keyword-only Config Result

Config command:

```powershell
bun run src/cli.ts config set search.mcp_keyword_only true
```

Observed result:

```yaml
keyword_only_config_attempted: true
keyword_only_config_success: true
observed_output: "Set search.mcp_keyword_only = true"
```

## Governance Import Result

Import command:

```powershell
bun run src/cli.ts import "$GovernanceInput" --no-embed
```

Observed result:

```yaml
governance_import_attempted: true
governance_import_success: true
import_collected_markdown_files: 129
imported_pages: 129
skipped_pages: 0
import_errors: 0
chunks_created: 1763
```

Import warnings:

```text
Several governance files triggered content-sanity warnings for size or markup-heavy ratio. They stayed searchable. These warnings do not change the success classification and should inform future cleanup/retention work.
```

## Search Smoke Results

Only approved keyword search smoke queries were run.

```yaml
search_smoke_1:
  query: "memory authority model GBrain derived index canonical source"
  success: true
search_smoke_2:
  query: "GBrain Graphify semantic replacement memory retrieval authority"
  success: true
search_smoke_3:
  query: "memory store integration canonical source reference GBrain index"
  success: true
search_smoke_4:
  query: "GStack skill memory not authority execution gate"
  success: true
search_smoke_5:
  query: "CLEAN production operational memory blocked"
  success: true
```

Observed search behavior:

```text
Search returned ranked governance results, including P12.3 memory authority, P12.5 GBrain/Graphify decision, P12.7 memory store integration, P12.4 skill authority, P12.6 GStack adoption, and this P12.9 execution record where relevant.
```

No `query`, `graph-query`, provider expansion, embedding search, or Ollama-backed search was run.

## Export Result

Export command:

```powershell
bun run src/cli.ts export --dir "$ExportsPath"
```

Observed result:

```yaml
export_attempted: true
export_success: true
exported_pages: 129
exports_path: "9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/exports"
exports_top_level_files_observed: 129
```

Only top-level export file names and lengths were listed. Export file contents were not inspected.

## Generated Output Metadata

Generated outputs were confined to:

```text
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/
```

Post-run metadata:

```yaml
generated_outputs_created: true
generated_outputs_confined_to_sandbox: true
generated_outputs_staged: false
generated_outputs_tracked: false
manifest_created: true
exports_created: true
db_created: true
gbrain_home_created: true
logs_dir_created: true
reports_dir_created: true
```

## GBRAIN_HOME Cleanup Status

`GBRAIN_HOME` was set only inside the runtime PowerShell process and removed after export.

Post-run check:

```yaml
gbrain_home_env_set_for_runtime: true
gbrain_home_value_was_sandbox_path: true
gbrain_home_cleanup_performed: true
test_path_env_gbrain_home_after_runtime: false
```

## Post-run Git Status

Post-run `git status --short` showed no sandbox outputs staged or tracked.

Observed status after runtime before this record update:

```text
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

This means the approved sandbox outputs under ignored `9_artifacts/` remained local/untracked and were not staged.

## Authority Classification

P12.9 authority classification:

```text
The GBrain sandbox is Tier B derived retrieval infrastructure.
The GBrain exports are Tier C generated evidence.
The sandbox is not source of truth.
The sandbox is not approval authority.
The sandbox is not operational production memory.
The sandbox cannot override governance docs.
The sandbox cannot decide tickets.
The sandbox cannot mutate Git.
```

## CLEAN / Production Memory Boundary

Production use remains blocked until:

```text
CLEAN.R or equivalent accepted cleanup closure
P12.11 retention / rollback / incident hardening
future exact memory reindex gate
```

P12.9 validates a fresh local retrieval sandbox candidate only. It does not create production operational memory and does not authorize production agent taxonomy use.

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_canonical_local_memory_sandbox_spike_record.md
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/gbrain_home/**
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/db/**
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/exports/**
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/logs/**
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/reports/**
9_artifacts/gbrain_sandbox/p12_9_canonical_memory_01/manifest/**
```

Not created / not approved:

```text
No production memory store
No operational memory promotion
No graph-query
No embeddings
No Ollama command
No Ollama model pull
No provider/API call
No Graphify command
No GStack command
No skill execution
No MCP registration
No browser daemon
No credential inspection
No product/Siamese path access
No normal user .gbrain write
No normal user .gstack write
No DB/internal inspection
No generated home/internal inspection
No generated output tracking
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

P12.9 does not validate:

```text
production memory readiness
semantic embeddings
Ollama Mode B
provider-backed search
graph traversal usefulness
graph-query behavior
GStack adoption
MCP registration
agent taxonomy production use
cleanup/reindex operational readiness
rollback automation
incident automation
```

P12.9 observed content-sanity warnings for some large or markup-heavy governance files. These are not runtime failures, but they should be considered by P12.11 and CLEAN.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.11 - Retention / Rollback / Incident Hardening
```

## Commit Commands

The following commands are not part of this execution and were not run. If this execution record is accepted, stage only the intended governance execution record:

```powershell
git status --short
git add 0_architecture/governance/agent_platform_canonical_local_memory_sandbox_spike_record.md
git commit -m "Run canonical local memory sandbox spike"
git push
```

Do not stage sandbox outputs. Do not stage dependency artifacts. Do not use `git add .`.

## Final Status

P12.9 completed successfully as a controlled local memory sandbox spike.

Final marker:

```text
canonical_local_memory_sandbox_spike_ready
```
