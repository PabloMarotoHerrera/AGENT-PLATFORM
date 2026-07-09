# GBrain Bun Availability Installation Boundary

## Summary

P12.BUN reviewed Bun availability for the future controlled GBrain dependency install. It did not install Bun, execute Bun, execute GBrain, run package managers, create dependencies, modify PATH, create sandbox state, run Ollama, run Graphify, inspect credentials, or mutate Git.

Outcome: Bun is not available in the current shell and no allowed common Bun binary path was found. P12.INSTALL remains blocked. The next required gate is:

```text
P12.BUN-INSTALL - Bun Controlled Local Installation Plan
```

Result marker:

```text
gbrain_bun_availability_installation_boundary_ready
```

Decision markers:

```text
bun_not_available_installation_gate_required
bun_installation_boundary_blocks_p12_install
```

```yaml
P12_BUN_Decision:
  ticket: P12.BUN
  date: "2026-07-09"
  outcome: "Outcome C - Bun missing from allowed checks"
  bun_available_on_path: false
  bun_candidate_binary_found_in_allowed_paths: false
  bun_executed: false
  bun_installed_now: false
  path_modified: false
  p12_install_can_proceed_now: false
  p12_0d_can_proceed_now: false
  recommended_next_ticket: "P12.BUN-INSTALL - Bun Controlled Local Installation Plan"
  final_marker: "gbrain_bun_availability_installation_boundary_ready"
```

## Files Inspected

Governance files inspected read-only:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
.graphifyignore
```

GBrain source metadata inspected read-only:

```text
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
4_external/sources/gbrain-master/README.md
4_external/sources/gbrain-master/INSTALL_FOR_AGENTS.md
4_external/sources/gbrain-master/docs/INSTALL.md
```

No credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, `node_modules`, global package caches, user home GBrain state, normal user `.gbrain`, `9_artifacts`, `graphify-out`, product paths, or generated output contents were inspected.

## Files Created

```text
0_architecture/governance/agent_platform_gbrain_bun_availability_installation_boundary.md
```

## Files Modified

No existing file was modified. The only file change is the new P12.BUN boundary document.

## Commands Run

Allowed presence-only commands run:

```powershell
git status --short
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/bun.lock"
Get-Command bun -ErrorAction SilentlyContinue
Get-Command gbrain -ErrorAction SilentlyContinue
Get-Command node -ErrorAction SilentlyContinue
Get-Command npm -ErrorAction SilentlyContinue
Get-Command ollama -ErrorAction SilentlyContinue
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
Test-Path "$env:LOCALAPPDATA\bun\bun.exe"
Test-Path "$env:APPDATA\bun\bun.exe"
```

Observed command results:

| Check | Result |
| --- | --- |
| Initial `git status --short` | `?? 0_architecture/implementation/graphify_command_candidate_confirmation.md` |
| P12.SETUP file | `True` |
| GBrain source root | `True` |
| `package.json` | `True` |
| `bun.lock` | `True` |
| `Get-Command bun` | No output |
| `Get-Command gbrain` | No output |
| `Get-Command node` | `C:\Program Files\nodejs\node.exe` |
| `Get-Command npm` | `C:\Program Files\nodejs\npm.ps1` |
| `Get-Command ollama` | No output |
| `$env:USERPROFILE\.bun\bin\bun.exe` | `False` |
| `$env:LOCALAPPDATA\bun\bun.exe` | `False` |
| `$env:APPDATA\bun\bun.exe` | `False` |

Allowed read-only file searches were also used to inspect approved governance and GBrain metadata files. No Bun, GBrain, Node, npm, package-manager, Ollama, Graphify, test, build, script, CI, Docker, or Python command was executed.

## P12.SETUP Dependency Status

P12.SETUP exists at:

```text
0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
```

P12.SETUP final marker is present:

```text
gbrain_controlled_local_install_build_plan_ready
```

P12.SETUP states:

```yaml
bun_available_on_current_path: false
gbrain_available_on_current_path: false
ollama_available_on_current_path: false
preferred_install_candidate: "bun install --ignore-scripts --frozen-lockfile"
p12_install_ready_now: false
```

P12.SETUP also declares `gbrain_setup_plan_requires_bun_availability_resolution` and routes Bun availability to P12.BUN before P12.INSTALL.

Dependency decision:

```yaml
p12_setup_dependency_confirmed: true
p12_setup_final_marker_confirmed: true
bun_availability_unresolved_by_p12_setup: true
p12_bun_authorized_to_install_bun: false
```

## Bun Availability Status

Current-shell Bun discovery:

```yaml
get_command_bun_output: "no output"
bun_available_on_path: false
bun_version_checked: false
bun_executed: false
```

No Bun version is available from the allowed checks because running `bun --version` is prohibited and no Bun command path was discoverable.

Decision:

```yaml
bun_availability_status: "not_available_from_allowed_checks"
decision_outcome: "Outcome C - Bun missing"
decision_marker: "bun_not_available_installation_gate_required"
```

## Bun Candidate Path Status

Allowed common Bun binary path checks:

| Candidate path | Result |
| --- | --- |
| `$env:USERPROFILE\.bun\bin\bun.exe` | `False` |
| `$env:LOCALAPPDATA\bun\bun.exe` | `False` |
| `$env:APPDATA\bun\bun.exe` | `False` |

Decision:

```yaml
bun_not_on_path_but_candidate_binary_found: false
bun_path_boundary_required_now: false
bun_candidate_binary_found_in_allowed_paths: false
installation_gate_required: true
decision_marker: "bun_installation_boundary_blocks_p12_install"
```

This does not prove Bun is absent from every possible disk location. It proves only that Bun is not on `PATH` and not present in the three allowed common path checks.

## GBrain CLI Metadata

Current-shell GBrain discovery:

```yaml
get_command_gbrain_output: "no output"
gbrain_available_on_path: false
gbrain_executed: false
```

GBrain source metadata:

```text
package.json declares bin.gbrain mapped to src/cli.ts.
package.json scripts use bun run, bun build, and bun test patterns.
package.json declares engines.bun >=1.3.10.
The repository has a root bun.lock.
P12.CMD recorded src/cli.ts as a Bun TypeScript entrypoint.
```

Decision:

```yaml
gbrain_cli_available_for_runtime_now: false
gbrain_dependency_install_authorized_now: false
gbrain_runtime_authorized_now: false
decision_marker: "gbrain_dependency_install_still_blocked"
```

## Ollama Metadata

Current-shell Ollama discovery:

```yaml
get_command_ollama_output: "no output"
ollama_available_on_path: false
ollama_executed: false
ollama_model_inventory_checked: false
ollama_inference_authorized: false
```

P12.BUN does not authorize Ollama model inventory, model pulls, serving, inference, or Graphify-with-Ollama execution.

Decision:

```yaml
ollama_relevant_to_p12_bun_install_boundary: false
graphify_ollama_path_authorized_by_p12_bun: false
```

## Decision Marker

Primary decision marker:

```text
bun_not_available_installation_gate_required
```

Supporting decision markers:

```text
bun_installation_boundary_blocks_p12_install
```

Decision record:

```yaml
decision_outcome: "Outcome C - Bun missing"
required_next_gate: "P12.BUN-INSTALL - Bun Controlled Local Installation Plan"
p12_install_allowed_next: false
p12_0d_allowed_next: false
```

## P12.INSTALL Handoff Decision

P12.INSTALL may not proceed now.

Required before P12.INSTALL can be generated or executed:

```text
P12.BUN accepted.
P12.BUN-INSTALL accepted and completed, or another approved gate proves a safe Bun path.
P12.SETUP remains accepted.
Working directory remains 4_external/sources/gbrain-master.
Install command remains exact.
Postinstall remains blocked with --ignore-scripts.
--frozen-lockfile remains preferred if supported.
Global install and bun link remain blocked.
Build/runtime remain blocked.
Human approval is present.
```

Future P12.INSTALL command candidate remains unchanged from P12.SETUP:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

P12.BUN decision:

```yaml
p12_install_ready_now: false
p12_install_blocker: "Bun is not available from allowed checks"
decision_marker: "gbrain_dependency_install_still_blocked"
```

## P12.0D Handoff Decision

P12.0D remains blocked in this outcome.

P12.0D still requires:

```text
P12.BUN accepted.
P12.INSTALL accepted and completed.
GBrain dependency state available.
Sandbox GBRAIN_HOME approved.
Sandbox DB path approved.
Exact runtime commands approved.
Human runtime approval present.
```

Decision:

```yaml
p12_0d_runtime_execution_authorized_now: false
gbrain_runtime_authorized_now: false
ollama_runtime_authorized_now: false
graphify_runtime_authorized_now: false
decision_marker: "gbrain_runtime_still_blocked"
```

## Installation Boundary If Needed

Because Bun was not found, P12.BUN-INSTALL is required before P12.INSTALL.

P12.BUN-INSTALL must define:

```text
official installation source
exact install command
whether installation is user-level or system-level
expected created files
expected modified environment variables
PATH behavior
cache behavior
rollback/uninstall plan
whether admin rights are required
whether network access is required
human approval wording
```

P12.BUN-INSTALL must not:

```text
install GBrain dependencies
run GBrain
run bun install inside GBrain
create node_modules
run package lifecycle scripts
run postinstall
run migrations
run tests/builds/scripts/CI
run Ollama
run Graphify
inspect credentials
mutate Git
```

## Side-Effect Expectations For Future Bun Installation

Potential Bun installation side effects requiring future review:

| Side-effect surface | Required future decision |
| --- | --- |
| Network download | Approve official source and exact command before use. |
| User-level files | Identify expected created paths before install. |
| System-level files | Determine whether admin rights or machine-wide changes are required. |
| PATH/environment | Define whether PATH changes are temporary shell-scoped, user-scoped, or system-scoped. |
| Shell profile edits | Identify and approve any profile mutation or block it. |
| Caches | Identify Bun cache behavior and cleanup posture. |
| Rollback | Define uninstall/removal and PATH rollback before execution. |
| Version posture | Confirm supported Bun version without running unapproved setup commands. |

No side effects were created by P12.BUN.

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_gbrain_bun_availability_installation_boundary.md
```

Not created / not approved:

```text
No Bun execution
No Bun installation
No Bun version command
No GBrain execution
No package manager execution
No dependency installation
No node_modules
No postinstall
No build
No runtime
No sandbox directories
No DB/storage/output
No Ollama inference
No Graphify execution
No provider/API calls
No credential inspection
No PATH mutation
No Git mutation
No git add .
```

## Limitations

P12.BUN did not perform an exhaustive disk search for Bun. Only `Get-Command bun` and the three approved common path checks were used.

P12.BUN did not run `bun --version`, so no version was confirmed.

P12.BUN did not inspect official web installation docs. Official source and installation method must be reviewed in P12.BUN-INSTALL.

P12.BUN did not inspect global package caches, user shell profiles, user/system environment variables, or installed application inventories.

P12.BUN did not prove whether another shell with a different PATH could find Bun.

## Recommended Next Ticket

Because Bun is missing from allowed checks, the recommended next ticket is:

```text
P12.BUN-INSTALL - Bun Controlled Local Installation Plan
```

P12.INSTALL remains blocked until Bun availability is resolved by an accepted P12.BUN-INSTALL or equivalent safe Bun path boundary.

If a separate Graphify local-model experiment is desired, it must use a separate path and must not reuse P12.BUN or P12.INSTALL authorization:

```text
P10.OLLAMA.0 - Graphify Ollama Local Provider Command / Scope Amendment
P10.OLLAMA.1 - Graphify Controlled Ollama Rerun On Tiny Fixture
```

## Commit Commands

If this governance record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_bun_availability_installation_boundary.md
git commit -m "Define GBrain Bun availability boundary"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainBunAvailabilityInstallationBoundary:
  ticket: P12.BUN
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_bun_availability_installation_boundary.md"
  p12_setup_dependency_confirmed: true
  p12_setup_final_marker_confirmed: true
  source_root_present: true
  package_json_present: true
  bun_lock_present: true
  bun_available_on_path: false
  bun_candidate_binary_found_in_allowed_paths: false
  gbrain_available_on_path: false
  ollama_available_on_path: false
  node_available_on_path: true
  npm_available_on_path: true
  bun_executed: false
  gbrain_executed: false
  node_executed: false
  npm_executed: false
  ollama_executed: false
  bun_installed_now: false
  gbrain_dependencies_installed_now: false
  package_manager_execution_performed: false
  path_modified: false
  git_mutated: false
  p12_install_ready_now: false
  p12_0d_execution_authorized: false
  recommended_next_ticket: "P12.BUN-INSTALL - Bun Controlled Local Installation Plan"
  final_marker: "gbrain_bun_availability_installation_boundary_ready"
```

Final marker:

```text
gbrain_bun_availability_installation_boundary_ready
```
