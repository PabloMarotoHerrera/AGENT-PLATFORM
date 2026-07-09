# GBrain Controlled Local Install Build Plan

## Document Header

| Field | Value |
| --- | --- |
| Title | GBrain Controlled Local Install Build Plan |
| Ticket | P12.SETUP |
| Status | Plan-only setup boundary ready for human approval; install, build, runtime execution, sandbox creation, and P12.0D remain blocked |
| Date | 2026-07-09 |
| Scope | Define a controlled future setup/install/build boundary for the local GBrain source repository without executing GBrain, Bun, Node, npm, package managers, tests, builds, scripts, providers, Ollama, Graphify, databases, embeddings, or generated output inspection. |
| Authority | Governance plan only; not package installation, dependency resolution, lifecycle execution, binary build, runtime execution, provider activation, credential inspection, database creation, embedding generation, sandbox materialization, generated-output tracking, source-of-truth promotion, frontend reuse, Graphify retry, Git mutation, or Cognitive Semantic System substrate selection. |
| Target file | `0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md` |

Final declaration: `gbrain_controlled_local_install_build_plan_ready`.

Decision markers:

```text
gbrain_setup_plan_ready_for_human_approval
gbrain_setup_plan_requires_bun_availability_resolution
gbrain_setup_plan_blocks_postinstall_by_default
gbrain_setup_plan_uses_local_source_runtime_candidate
gbrain_setup_plan_blocks_global_install
gbrain_setup_plan_blocks_runtime_execution
gbrain_setup_plan_blocks_p12_0d_until_setup_completion
```

## Summary

P12.SETUP defines the next safe setup boundary after P12.CMD and P12.1. It does not execute setup. It selects a future local source dependency-install candidate using Bun with lifecycle scripts suppressed, blocks global install/link, blocks build scripts, blocks runtime commands, and keeps P12.0D blocked.

The preferred future setup path is a local source install inside `4_external/sources/gbrain-master` using the existing `bun.lock`, with no postinstall/lifecycle scripts and no global binary creation. The preferred future command candidate is:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

The fallback candidate, only if explicitly accepted later, is:

```powershell
bun install --ignore-scripts
```

Both commands are candidates only. P12.SETUP does not authorize running them.

Current blocker: `bun` is not discoverable on `PATH` from the current shell. Therefore P12.INSTALL cannot proceed until a separate `P12.BUN - Bun Availability / Installation Boundary` or equivalent explicit approval resolves Bun availability.

```yaml
P12_SETUP_Decision:
  plan_only: true
  source_root: "4_external/sources/gbrain-master"
  preferred_install_working_directory: "4_external/sources/gbrain-master"
  package_manager_candidate: "bun"
  bun_available_on_current_path: false
  gbrain_available_on_current_path: false
  ollama_available_on_current_path: false
  preferred_install_candidate: "bun install --ignore-scripts --frozen-lockfile"
  fallback_install_candidate_requires_explicit_acceptance: "bun install --ignore-scripts"
  lifecycle_scripts_allowed_by_default: false
  global_install_allowed: false
  bun_link_allowed: false
  build_allowed: false
  runtime_execution_allowed: false
  sandbox_creation_allowed: false
  p12_install_ready_now: false
  p12_0d_execution_authorized_now: false
  final_marker: "gbrain_controlled_local_install_build_plan_ready"
```

## Prior Authority

P12.CMD exists at:

```text
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
```

P12.CMD declared `gbrain_runtime_entrypoint_install_boundary_discovery_ready`, discovered the `gbrain` bin mapping to `src/cli.ts`, identified Bun TypeScript as the source runtime, found `bun.lock`, found the `postinstall` migration risk, and confirmed `gbrain` and `bun` were not discoverable on `PATH` from the current shell.

P12.1 exists at:

```text
0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
```

P12.1 declared `gbrain_license_dependency_storage_audit_ready`, found the root MIT license posture acceptable for controlled setup planning, found dependency posture requiring hardening, required postinstall/lifecycle gating, accepted storage only with sandbox boundaries, and kept runtime blocked.

P12.0C exists at:

```text
0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
```

P12.0C declared `gbrain_ollama_controlled_sandbox_plan_ready`, preferred a future Mode A keyword-only no-embedding sandbox, and kept P12.0D blocked pending command/setup resolution.

The local `.graphifyignore` remains controlling scope evidence. Graphify remains evidence/supporting visualization only, not authority, runtime, source of truth, approval engine, or Cognitive Semantic System substrate.

## Commands Run

Allowed presence-only commands observed for this setup planning sequence:

```powershell
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/bun.lock"
Test-Path -LiteralPath "4_external/sources/gbrain-master/src/cli.ts"
Get-Command bun -ErrorAction SilentlyContinue
Get-Command gbrain -ErrorAction SilentlyContinue
Get-Command node -ErrorAction SilentlyContinue
Get-Command npm -ErrorAction SilentlyContinue
Get-Command ollama -ErrorAction SilentlyContinue
git status --short
```

Observed command results:

| Check | Result |
| --- | --- |
| P12.1 audit file | `True` |
| GBrain source root | `True` |
| `package.json` | `True` |
| `bun.lock` | `True` |
| `src/cli.ts` | `True` |
| `Get-Command bun` | No output |
| `Get-Command gbrain` | No output |
| `Get-Command node` | `C:\Program Files\nodejs\node.exe` |
| `Get-Command npm` | `C:\Program Files\nodejs\npm.ps1` |
| `Get-Command ollama` | No output |

Observed `git status --short` before this file existed:

```text
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

That implementation file was not inspected, staged, or modified by P12.SETUP.

Read-only file tools were also used to inspect allowed governance and source files. No forbidden runtime command was executed.

## Files Inspected

Governance files inspected:

```text
0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
```

GBrain source files inspected read-only during P12.SETUP context building:

```text
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/README.md
4_external/sources/gbrain-master/INSTALL_FOR_AGENTS.md
4_external/sources/gbrain-master/docs/INSTALL.md
4_external/sources/gbrain-master/docs/integrations/embedding-providers.md
4_external/sources/gbrain-master/src/cli.ts
4_external/sources/gbrain-master/src/core/config.ts
4_external/sources/gbrain-master/src/commands/init.ts
4_external/sources/gbrain-master/src/commands/import.ts
4_external/sources/gbrain-master/src/commands/export.ts
4_external/sources/gbrain-master/src/core/self-upgrade.ts
4_external/sources/gbrain-master/scripts/build-admin-embedded.ts
4_external/sources/gbrain-master/scripts/build-llms.ts
4_external/sources/gbrain-master/scripts/build-pglite-snapshot.ts
4_external/sources/gbrain-master/scripts/build-schema.sh
```

No credentials, `.env`, provider configs, `node_modules`, global package caches, user home GBrain state, generated outputs, product paths, Graphify outputs, or external source roots outside `4_external/sources/gbrain-master/**` were inspected.

## Files Created

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
```

## Files Modified

No existing file was modified. The only file change is the new P12.SETUP governance document.

## Source Runtime Assessment

The local source runtime candidate is Bun TypeScript.

Evidence:

```text
package.json maps bin.gbrain to src/cli.ts.
src/cli.ts has a Bun shebang: #!/usr/bin/env bun.
package.json scripts use bun run, bun build, and bun test patterns.
package.json declares engines.bun >=1.3.10.
The repository has a root bun.lock.
INSTALL_FOR_AGENTS.md says Bun is required because GBrain is a Bun + TypeScript runtime.
```

Decision:

```yaml
source_runtime_candidate: "Bun TypeScript"
local_source_runtime_candidate_selected_for_future_setup: true
compiled_binary_required_for_minimal_source_runtime: false
node_runtime_substitute_accepted: false
npm_install_substitute_accepted: false
decision_marker: "gbrain_setup_plan_uses_local_source_runtime_candidate"
```

`node` and `npm` are discoverable on this machine, but they are not accepted substitutes for GBrain setup because the repository itself points to Bun.

## Bun Availability Boundary

`bun` is not discoverable on `PATH` from the current shell.

Decision:

```yaml
bun_required_for_source_runtime: true
bun_required_for_preferred_install_candidate: true
bun_current_shell_discoverable: false
package_manager_execution_authorized_now: false
next_gate: "P12.BUN - Bun Availability / Installation Boundary"
decision_marker: "gbrain_setup_plan_requires_bun_availability_resolution"
```

P12.BUN should resolve only Bun availability and installation posture. It should not install GBrain dependencies, run GBrain, run package scripts, run tests/builds, create GBrain sandbox directories, inspect credentials, activate providers, run Ollama, run Graphify, or mutate Git unless explicitly approved in that future gate.

## Install Strategy Decision

Preferred future setup route:

```yaml
strategy: "local source dependency install"
working_directory: "4_external/sources/gbrain-master"
command_candidate: "bun install --ignore-scripts --frozen-lockfile"
lockfile_required: true
lifecycle_scripts_suppressed: true
global_install: false
global_link: false
build: false
runtime_execution: false
```

Rationale:

| Requirement | Decision |
| --- | --- |
| Use local reviewed source | Use `4_external/sources/gbrain-master`, not a fresh global GitHub install. |
| Use lockfile | Prefer `bun.lock` with `--frozen-lockfile` to avoid lockfile mutation. |
| Suppress lifecycle scripts | Require `--ignore-scripts` because root `postinstall` can invoke `gbrain apply-migrations`. |
| Avoid global state | Block `bun install -g` and `bun link`. |
| Avoid build artifacts | Do not run `bun run build`, `build:all`, `build:admin`, generated-doc, schema, or snapshot scripts. |
| Avoid runtime side effects | Do not run `gbrain`, `bun run src/cli.ts`, `bun run dev`, `--help`, or `--version` in P12.SETUP. |

Fallback candidate:

```yaml
fallback_command_candidate: "bun install --ignore-scripts"
fallback_allowed_now: false
fallback_condition: "Only if a later P12.INSTALL approval explicitly accepts lockfile mutation risk or Bun flag compatibility requires it."
```

P12.SETUP does not authorize either command. It only defines the candidate route for later human approval.

## Global Install And Link Boundary

Upstream docs describe global install/link paths such as `bun install -g github:garrytan/gbrain`, local `bun install`, and `bun link`. Those paths are not selected for this platform setup boundary.

Decision:

```yaml
global_bun_install_allowed: false
fresh_github_install_allowed: false
bun_link_allowed: false
global_binary_creation_allowed: false
path_mutation_allowed: false
reason: "Global install/link can create broad state and bypass the reviewed local source boundary."
decision_marker: "gbrain_setup_plan_blocks_global_install"
```

Any future global install or link request requires a separate gate and must justify why local source runtime is insufficient.

## Lifecycle And Postinstall Boundary

P12.1 found the root `postinstall` script can execute:

```text
gbrain apply-migrations --yes --non-interactive
```

if a `gbrain` command is discoverable.

Decision:

```yaml
postinstall_allowed_by_default: false
package_lifecycle_scripts_allowed_by_default: false
install_candidate_requires_ignore_scripts: true
migration_command_allowed_during_install: false
decision_marker: "gbrain_setup_plan_blocks_postinstall_by_default"
```

P12.INSTALL must treat any lifecycle execution as a stop condition unless a later approval explicitly changes this decision after sandbox home and DB boundaries are already proven safe.

## Build Boundary

Build scripts remain blocked by P12.SETUP.

Blocked build and generated-artifact routes include:

```text
bun run build
bun run build:all
bun run build:admin
bun run build:admin-embedded
bun run build:schema
bun run build:llms
bun run build:pglite-snapshot
bun run test
bun run verify
bun run typecheck
```

Build risk evidence:

| Script | Reason Blocked |
| --- | --- |
| `build` / `build:all` | Creates compiled binaries under `bin/`. |
| `build:admin` | Builds admin UI and can create `admin/dist` and rewrite embedded asset source. |
| `build:admin-embedded` | Rewrites `src/admin-embedded.ts`. |
| `build:schema` | Rewrites `src/core/schema-embedded.ts`. |
| `build:llms` | Rewrites `llms.txt` and `llms-full.txt`. |
| `build:pglite-snapshot` | Boots PGLite, runs schema/migrations, and writes snapshot fixtures. |
| `test` / `verify` / `typecheck` | Executes tooling outside this setup-planning boundary. |

Decision:

```yaml
build_required_for_preferred_source_runtime_setup: false
build_authorized_now: false
generated_artifacts_authorized_now: false
future_gate_if_needed: "P12.BUILD"
```

## Runtime Boundary

Runtime execution remains blocked.

Blocked runtime examples:

```text
gbrain
gbrain --help
gbrain --version
gbrain init
gbrain import
gbrain search
gbrain query
gbrain graph-query
gbrain export
bun run src/cli.ts
bun run dev
ollama list/show/run/pull/serve/ps
Graphify or /graphify
```

Runtime risk evidence from source review:

```text
GBrain config writes can create config.json and .gitignore under the active GBrain home.
Without GBRAIN_HOME, GBrain falls back to the normal user home .gbrain.
PGLite init can create/connect a database and run schema initialization.
Imports can create chunks and, without --no-embed, validate embedding credentials and generate embeddings.
Exports can create directories and .raw JSON sidecars.
Self-upgrade state and audit logs can write under GBrain home.
Provider recipes include hosted providers and local providers; provider calls remain blocked.
```

Decision:

```yaml
runtime_execution_authorized_now: false
runtime_help_or_version_authorized_now: false
provider_calls_authorized_now: false
ollama_commands_authorized_now: false
graphify_runtime_retry_authorized_now: false
decision_marker: "gbrain_setup_plan_blocks_runtime_execution"
```

`--help` and `--version` remain runtime execution because they still load the Bun/TypeScript entrypoint and dependencies.

## Sandbox Boundary For Future Runtime

P12.SETUP must not create sandbox directories or runtime state.

Future sandbox root candidate from P12.0C:

```text
9_artifacts/gbrain_sandbox/p12_0d/
```

Future runtime storage candidates only:

```text
GBRAIN_HOME=<absolute path under 9_artifacts/gbrain_sandbox/p12_0d/gbrain_home>
PGLite DB path=9_artifacts/gbrain_sandbox/p12_0d/db/
```

P12.SETUP decision:

```yaml
sandbox_root_created_now: false
gbrain_home_created_now: false
db_path_created_now: false
gbrain_home_value_set_now: false
runtime_storage_authorized_now: false
```

A future P12.0D approval must use an absolute sandbox-only `GBRAIN_HOME` path and a sandbox-only DB path before any GBrain runtime command. It must not use the normal user home `.gbrain` state.

## P12.INSTALL Handoff

P12.INSTALL is not ready now because Bun availability is unresolved.

Required preconditions before P12.INSTALL:

```text
P12.SETUP accepted by human approval.
P12.BUN or equivalent approval confirms Bun is available and acceptable.
The working directory is exactly 4_external/sources/gbrain-master.
The install command is exactly approved.
Lifecycle suppression is preserved with --ignore-scripts.
Global install/link remains blocked.
Build scripts remain blocked.
Runtime commands remain blocked.
Rollback/cleanup posture is approved before execution.
```

Preferred future P12.INSTALL command candidate:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

Future P12.INSTALL stop conditions:

```text
bun is not discoverable or version posture is unacceptable
the command would run outside 4_external/sources/gbrain-master
the command would omit --ignore-scripts
the command would mutate bun.lock without explicit approval
the command would create a global binary or link
the command would run postinstall or migrations
the command would execute gbrain, provider calls, Ollama, Graphify, tests, builds, or CI
the command requests credentials or provider configuration
the command writes outside expected install/cache locations without approval
```

P12.INSTALL may verify only install side effects that are explicitly approved in that gate. It must not run GBrain after install unless a later runtime gate authorizes exact commands.

## P12.0D Handoff

P12.0D remains blocked by this plan.

P12.0D may be proposed only after:

```text
P12.SETUP is accepted.
P12.BUN resolves Bun availability.
P12.INSTALL is approved and completed, or an equivalent executable-safe dependency state is proven.
Sandbox GBRAIN_HOME and DB roots are approved.
Exact runtime command candidates are approved.
Human runtime approval is present.
```

Decision:

```yaml
p12_0d_runtime_execution_authorized_now: false
p12_0d_mode_a_authorized_now: false
p12_0d_mode_b_authorized_now: false
graphify_retry_authorized_now: false
decision_marker: "gbrain_setup_plan_blocks_p12_0d_until_setup_completion"
```

The P12.0D preferred first runtime posture remains Mode A keyword-only no-embedding sandbox. Mode B local Ollama embeddings remain separately gated.

## Rollback Plan

P12.SETUP creates only this governance document, so no runtime rollback is needed now.

If a future P12.INSTALL is approved and creates state, rollback must be reviewed before execution and limited to exact approved install artifacts. Candidate rollback scope for future review:

```text
remove only newly created dependency folders under 4_external/sources/gbrain-master, if approved
review any lockfile diff before any restoration decision
do not delete normal user .gbrain state
do not delete Graphify outputs
do not delete product files
do not delete unrelated external source files
do not delete package-manager caches without explicit approval
do not use git reset --hard
do not use git checkout --
do not stage generated outputs by default
```

If lifecycle scripts run unexpectedly, if GBrain migrations execute, if global links/binaries are created, if provider/Ollama/Graphify commands run, or if files are written outside approved paths, treat it as an install-boundary incident and stop for human review.

## Human Approval Wording

Minimum approval to accept this plan only:

```text
I approve P12.SETUP as a plan only. Do not run Bun, GBrain, Node, npm, package managers, tests, builds, scripts, Ollama, Graphify, providers, migrations, databases, embeddings, sandbox creation, credential inspection, generated-output inspection, or Git mutation.
```

Minimum approval for P12.BUN:

```text
I approve P12.BUN to resolve Bun availability only. Do not install GBrain dependencies, run GBrain, run package scripts, run tests/builds/CI, create sandbox directories, inspect credentials, activate providers, run Ollama, run Graphify, or mutate Git unless explicitly approved in that future gate.
```

Minimum approval for future P12.INSTALL after Bun availability is resolved:

```text
I approve P12.INSTALL only from `4_external/sources/gbrain-master` using `bun install --ignore-scripts --frozen-lockfile`. Do not run lifecycle scripts, global install, bun link, builds, tests, typecheck, GBrain runtime commands, provider calls, Ollama, Graphify, sandbox creation, credential inspection, generated-output tracking, or Git mutation. Stop if the lockfile would change or if Bun cannot honor the approved flags.
```

Fallback approval wording, only if explicitly chosen later:

```text
I approve the P12.INSTALL fallback `bun install --ignore-scripts` from `4_external/sources/gbrain-master` and accept that lockfile mutation risk must be reviewed. Do not run lifecycle scripts, global install, bun link, builds, tests, GBrain runtime commands, provider calls, Ollama, Graphify, sandbox creation, credential inspection, generated-output tracking, or Git mutation.
```

Minimum approval for later P12.0D Mode A must remain separate from P12.INSTALL and must include sandbox-only `GBRAIN_HOME`, sandbox-only DB path, `--no-embedding`, `--no-embed`, keyword-only search posture, explicit fixture scope, local generated untracked evidence handling, and no Ollama/model/provider/Graphify/Git authorization.

## Commit Commands

If this governance record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
git commit -m "Add GBrain controlled local setup plan"
```

If `0_architecture/implementation/graphify_command_candidate_confirmation.md` should also be committed, stage it explicitly in a separate decision or include it explicitly after review. This P12.SETUP document does not authorize staging unrelated untracked files.

## Verification Plan

Allowed verification after creating this file:

```powershell
rg "gbrain_controlled_local_install_build_plan_ready|gbrain_setup_plan_ready_for_human_approval|gbrain_setup_plan_requires_bun_availability_resolution|gbrain_setup_plan_blocks_postinstall_by_default|gbrain_setup_plan_uses_local_source_runtime_candidate|gbrain_setup_plan_blocks_global_install|gbrain_setup_plan_blocks_runtime_execution|gbrain_setup_plan_blocks_p12_0d_until_setup_completion" 0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
git status --short
```

No runtime verification is authorized by P12.SETUP.

## Final Decision Record

```yaml
GBrainControlledLocalInstallBuildPlan:
  ticket: P12.SETUP
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md"
  plan_ready: true
  human_approval_required_before_install: true
  source_root: "4_external/sources/gbrain-master"
  package_manager_candidate: "bun"
  bun_available_on_current_path: false
  gbrain_available_on_current_path: false
  ollama_available_on_current_path: false
  preferred_install_candidate: "bun install --ignore-scripts --frozen-lockfile"
  fallback_install_candidate_requires_explicit_acceptance: "bun install --ignore-scripts"
  lifecycle_scripts_allowed_by_default: false
  postinstall_allowed_by_default: false
  global_install_allowed: false
  bun_link_allowed: false
  build_authorized: false
  runtime_execution_authorized: false
  p12_bun_required_first: true
  p12_install_ready_now: false
  p12_0d_execution_authorized: false
  gbrain_executed: false
  bun_executed: false
  node_executed: false
  npm_executed: false
  package_install_performed: false
  tests_or_builds_run: false
  credentials_inspected: false
  provider_config_inspected: false
  product_source_inspected: false
  generated_output_inspected: false
  database_created: false
  embeddings_generated: false
  sandbox_root_created: false
  final_marker: "gbrain_controlled_local_install_build_plan_ready"
```

Final marker:

```text
gbrain_controlled_local_install_build_plan_ready
```
