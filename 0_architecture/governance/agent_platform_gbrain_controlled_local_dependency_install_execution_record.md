# GBrain Controlled Local Dependency Install Execution Record

## Summary

P12.INSTALL performed one controlled GBrain dependency installation from the approved local source root:

```text
4_external/sources/gbrain-master
```

The effective package-manager command ran exactly once:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

The dependency install completed successfully. Bun reported `276 packages installed`. `node_modules` and `node_modules/.bin` exist after installation. `package.json` and `bun.lock` were not modified according to the approved `git diff --name-only` check. `git status --short` did not surface `node_modules`, so dependency artifacts appear ignored or otherwise not shown by Git status.

No GBrain command was run. No lifecycle/postinstall/build/test/runtime command was run. No provider, Ollama, Graphify, sandbox, DB/storage, credential, PATH, or Git mutation was performed by P12.INSTALL.

Result marker:

```text
gbrain_controlled_local_dependency_install_execution_record_ready
```

Decision markers:

```text
gbrain_dependency_install_success
p12_0d_ready_to_generate_after_dependency_install
```

```yaml
P12_INSTALL_Decision:
  ticket: P12.INSTALL
  date: "2026-07-09"
  outcome: "Outcome A - dependency install success"
  human_install_approval_present: true
  install_command_attempted: true
  install_command_execution_count: 1
  install_command_completed_successfully: true
  command: "bun install --ignore-scripts --frozen-lockfile"
  working_directory: "4_external/sources/gbrain-master"
  packages_installed_reported_by_bun: 276
  node_modules_present_after_install: true
  node_modules_bin_present_after_install: true
  package_json_modified_by_install: false
  bun_lock_modified_by_install: false
  package_lifecycle_scripts_run: false
  postinstall_run: false
  gbrain_executed: false
  gbrain_available_on_path_after_install: false
  p12_0d_ready_to_generate_now: true
  p12_0d_execution_authorized_now: false
  final_marker: "gbrain_controlled_local_dependency_install_execution_record_ready"
```

## Files Inspected

Governance files inspected read-only:

```text
0_architecture/governance/agent_platform_gbrain_bun_refreshed_shell_verification_resolution.md
0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
.graphifyignore
```

GBrain source metadata inspected read-only before installation:

```text
4_external/sources/gbrain-master/package.json
```

Presence-only checks were performed for:

```text
4_external/sources/gbrain-master
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
4_external/sources/gbrain-master/node_modules
4_external/sources/gbrain-master/node_modules/.bin
```

No credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, Claude credentials, package caches, `node_modules` contents, normal user `.gbrain`, `9_artifacts`, `graphify-out`, product paths, generated outputs, raw Graphify outputs, or external source roots outside the approved GBrain source metadata paths were inspected.

## Files Created

Repo governance record:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
```

Dependency artifacts created outside the governance record:

```text
4_external/sources/gbrain-master/node_modules/
4_external/sources/gbrain-master/node_modules/.bin/
```

Only presence was checked. Dependency contents were not inspected.

## Files Modified

Repo file modified:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
```

Approved dependency install side effects:

```text
4_external/sources/gbrain-master/node_modules/**
Bun dependency cache/state as required by Bun package installation
```

Approved mutation checks showed no `package.json` or `bun.lock` diff:

```text
git diff --name-only -- 4_external/sources/gbrain-master/package.json 4_external/sources/gbrain-master/bun.lock
```

Result: no output.

## Commands Run

Allowed preflight commands run:

```powershell
git status --short
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_bun_refreshed_shell_verification_resolution.md"
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md"
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/bun.lock"
Get-Command bun -ErrorAction SilentlyContinue
bun --version
bun --revision
Get-Command gbrain -ErrorAction SilentlyContinue
Test-Path -LiteralPath "4_external/sources/gbrain-master/node_modules"
```

Approved dependency install command run exactly once from the required working directory:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

Allowed post-install verification commands run:

```powershell
git status --short
Test-Path -LiteralPath "4_external/sources/gbrain-master/node_modules"
Test-Path -LiteralPath "4_external/sources/gbrain-master/node_modules/.bin"
Get-Command bun -ErrorAction SilentlyContinue
bun --version
bun --revision
Get-Command gbrain -ErrorAction SilentlyContinue
git diff --name-only -- "4_external/sources/gbrain-master/package.json" "4_external/sources/gbrain-master/bun.lock"
```

Forbidden commands were not run:

```text
bun run
bun build
bun test
bun upgrade
bun add
bun remove
bun x
bunx
npm install
npm run
node --version
npx
pnpm
yarn
ollama list
ollama run
ollama show
```

## Human Approval Status

Required P12.INSTALL approval statement was present:

```text
I approve one controlled GBrain dependency installation by running `bun install --ignore-scripts --frozen-lockfile` from `4_external/sources/gbrain-master`. Network access is allowed only for dependency resolution/downloads required by the existing GBrain package manifests and lockfile. Do not run GBrain, do not run `gbrain`, do not run builds, tests, migrations, postinstall, package lifecycle scripts, providers, Ollama, Graphify, sandbox runtime, or any command outside the approved dependency install boundary. Do not inspect credentials, do not modify PATH, do not mutate Git, and do not stage dependency artifacts.
```

Decision:

```yaml
human_install_approval_present: true
package_manager_execution_allowed: true
```

## P12.BUN-PATH-VERIFY-R Dependency Status

P12.BUN-PATH-VERIFY-R exists at:

```text
0_architecture/governance/agent_platform_gbrain_bun_refreshed_shell_verification_resolution.md
```

P12.BUN-PATH-VERIFY-R final marker is present:

```text
gbrain_bun_refreshed_shell_verification_resolution_ready
```

P12.BUN-PATH-VERIFY-R decision marker is present:

```text
p12_install_ready_after_bun_path_resolution
```

Dependency decision:

```yaml
p12_bun_path_verify_r_confirmed: true
bun_available_for_p12_install: true
p12_install_execution_approved: true
```

## Bun Availability Status

Preflight and post-install Bun availability:

```yaml
get_command_bun_succeeded: true
bun_command_source: "C:\\Users\\pablo\\.bun\\bin\\bun.exe"
bun_version: "1.3.14"
bun_revision: "1.3.14+0d9b296af"
```

## GBrain Source Root Status

Approved install target root exists:

```text
4_external/sources/gbrain-master
```

Required metadata exists:

```text
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
```

Root `package.json` evidence:

```text
bin.gbrain = src/cli.ts
scripts include Bun-oriented dev/build/test/check commands
postinstall can invoke gbrain apply-migrations if gbrain is discoverable
engines.bun >=1.3.10
```

Decision:

```yaml
working_directory_confirmed: true
install_working_directory: "4_external/sources/gbrain-master"
postinstall_risk_confirmed: true
ignore_scripts_used: true
```

## Pre-Install Working Tree Status

Initial `git status --short` observed before dependency install:

```text
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

That implementation file was not inspected, staged, or modified by P12.INSTALL.

Pre-install dependency artifact state:

```yaml
node_modules_present_before_install: false
```

## Dependency Install Execution Status

Dependency install executed exactly once.

Command:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

Working directory:

```text
4_external/sources/gbrain-master
```

Install output summary:

```text
bun install v1.3.14 (0d9b296a)
276 packages installed [27.87s]
```

Dependency packages listed by Bun included runtime and dev dependencies from the existing package manifest and lockfile. No credentials were requested. No GBrain command output was observed. No lifecycle/postinstall/build/test/runtime command was run by the agent.

Decision:

```yaml
install_command_attempted: true
install_command_execution_count: 1
install_command_completed_successfully: true
packages_installed_reported_by_bun: 276
ignore_scripts_used: true
frozen_lockfile_used: true
dependency_install_success: true
decision_marker: "gbrain_dependency_install_success"
```

## Created Dependency Artifact Metadata

Post-install presence checks:

| Path | Result |
| --- | --- |
| `4_external/sources/gbrain-master/node_modules` | `True` |
| `4_external/sources/gbrain-master/node_modules/.bin` | `True` |

Dependency contents were not inspected. No binaries from `node_modules/.bin` were run.

## Package Manifest / Lockfile Mutation Check

Approved mutation check:

```powershell
git diff --name-only -- "4_external/sources/gbrain-master/package.json" "4_external/sources/gbrain-master/bun.lock"
```

Result:

```text
No output
```

Decision:

```yaml
package_json_modified_by_install: false
bun_lock_modified_by_install: false
unexpected_manifest_or_lockfile_mutation: false
```

## Post-Install Working Tree Status

Post-install `git status --short` observed:

```text
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

`node_modules` did not appear in `git status --short`. Dependency artifacts were not staged or committed.

After this execution record is written, expected status includes this governance record plus the pre-existing untracked Graphify implementation file.

Decision:

```yaml
node_modules_unignored: false
dependency_artifacts_staged: false
git_mutated: false
```

## GBrain CLI Metadata

Allowed metadata check:

```powershell
Get-Command gbrain -ErrorAction SilentlyContinue
```

Result:

```text
No output
```

GBrain was not executed.

Decision:

```yaml
gbrain_available_on_path: false
gbrain_executed: false
gbrain_runtime_authorized_now: false
decision_marker: "gbrain_runtime_still_blocked"
```

## Incident Status

No dependency install incident was observed.

```yaml
incident_status: "none_observed"
frozen_lockfile_failure: false
unexpected_manifest_mutation: false
node_modules_unignored: false
secrets_exposed: false
path_modified: false
git_mutated: false
runtime_attempted: false
```

## P12.0D Handoff Decision

P12.0D may now be generated as a separate ticket, but P12.INSTALL does not authorize P12.0D execution.

Decision:

```yaml
P12_0D_HandoffDecision:
  status: "ready_to_generate_next_ticket"
  reason: "Dependency install completed successfully with no manifest/lockfile mutation and no observed install incident."
  p12_0d_ready_to_generate_now: true
  p12_0d_execution_authorized: false
  decision_marker: "p12_0d_ready_to_generate_after_dependency_install"
```

P12.0D still requires:

```text
separate P12.0D ticket acceptance
GBrain runtime command boundary approval
sandbox GBRAIN_HOME approval
sandbox DB path approval
exact runtime commands approval
human runtime approval present
```

## Graphify / Ollama Boundary Confirmation

P12.INSTALL did not authorize or run:

```text
Graphify execution
Graphify with Ollama
Ollama model inventory
Ollama model pull
Ollama inference
provider calls
OpenAI / Anthropic / Gemini calls
```

Graphify plus Ollama remains a separate optional path:

```text
P10.OLLAMA.0 - Graphify Ollama Local Provider Command / Scope Amendment
```

## Created / Not Created Register

Created in repo:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
```

Created outside governance record:

```text
4_external/sources/gbrain-master/node_modules/**
Bun dependency cache/state required by install
```

Not created / not approved:

```text
No GBrain runtime execution
No gbrain command execution
No gbrain --help
No gbrain --version
No bun run
No bun build
No bun test
No package lifecycle scripts run by agent
No postinstall run by agent
No migrations
No DB/storage/output
No sandbox directories
No Ollama inference
No Graphify execution
No provider/API calls
No credential inspection
No PATH mutation
No Git mutation
No staging dependency artifacts
No git add .
```

## Limitations

Dependency contents under `node_modules` were not inspected. Only presence of `node_modules` and `node_modules/.bin` was checked.

Bun/user cache contents were not inspected.

P12.INSTALL does not prove GBrain runtime behavior. Runtime remains separately gated.

`Get-Command gbrain` still returns no output because this was a local dependency install, not a global install or link.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.0D-PREP - GBrain Controlled Sandbox Exact Command Preparation
```

or, if the user wants to proceed directly to the sandbox execution gate:

```text
P12.0D - GBrain Controlled Local Memory Sandbox Execution
```

P12.0D must still remain sandboxed and explicitly approved before any GBrain runtime command.

## Commit Commands

If this execution record is accepted for commit, stage only the intended governance record. Do not stage `node_modules`. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md
git commit -m "Record GBrain controlled dependency install"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainControlledLocalDependencyInstallExecutionRecord:
  ticket: P12.INSTALL
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_controlled_local_dependency_install_execution_record.md"
  p12_bun_path_verify_r_confirmed: true
  p12_setup_confirmed: true
  p12_1_confirmed: true
  human_install_approval_present: true
  bun_available: true
  bun_version: "1.3.14"
  bun_revision: "1.3.14+0d9b296af"
  source_root_present: true
  package_json_present: true
  bun_lock_present: true
  node_modules_present_before_install: false
  install_command_attempted: true
  install_command_execution_count: 1
  install_command_completed_successfully: true
  dependency_install_success: true
  packages_installed_reported_by_bun: 276
  node_modules_present_after_install: true
  node_modules_bin_present_after_install: true
  package_manager_execution_performed: true
  package_lifecycle_scripts_run_by_agent: false
  postinstall_run_by_agent: false
  gbrain_available_on_path_after_install: false
  gbrain_executed: false
  runtime_attempted: false
  package_json_modified_by_install: false
  bun_lock_modified_by_install: false
  node_modules_unignored: false
  credentials_inspected: false
  path_modified: false
  git_mutated: false
  p12_0d_ready_to_generate_now: true
  p12_0d_execution_authorized: false
  final_marker: "gbrain_controlled_local_dependency_install_execution_record_ready"
```

Final marker:

```text
gbrain_controlled_local_dependency_install_execution_record_ready
```
