# GBrain Bun Controlled Local Installation Plan

## Summary

P12.BUN-INSTALL defines a controlled future Bun installation plan for the Windows development machine. It is plan-only. It does not install Bun, run Bun, run `bun --version`, run GBrain, install GBrain dependencies, modify PATH, create `node_modules`, create sandbox outputs, inspect credentials, or mutate Git.

P12.BUN confirmed Bun is missing from the allowed checks. P12.BUN-INSTALL therefore records the official Windows Bun install command as a future execution candidate only and keeps P12.INSTALL blocked until Bun is installed or otherwise safely available.

Result marker:

```text
gbrain_bun_controlled_local_installation_plan_ready
```

Decision markers:

```text
bun_official_windows_install_source_identified
bun_user_level_install_candidate_selected
bun_install_execution_still_blocked
bun_path_update_candidate_identified
bun_uninstall_rollback_candidate_identified
bun_install_execution_requires_human_approval
p12_install_still_blocked_until_bun_installed
```

```yaml
P12_BUN_INSTALL_Decision:
  ticket: P12.BUN-INSTALL
  date: "2026-07-09"
  plan_only: true
  bun_install_authorized_now: false
  bun_execution_authorized_now: false
  path_mutation_authorized_now: false
  preferred_install_scope_candidate: "user-level"
  official_install_command_candidate: 'powershell -c "irm bun.sh/install.ps1|iex"'
  expected_install_root_candidate: "$env:USERPROFILE\\.bun\\"
  expected_binary_candidate: "$env:USERPROFILE\\.bun\\bin\\bun.exe"
  expected_uninstall_candidate: "$env:USERPROFILE\\.bun\\uninstall.ps1"
  p12_bun_install_exec_may_be_generated_after_acceptance: true
  p12_install_ready_now: false
  p12_0d_execution_authorized_now: false
  final_marker: "gbrain_bun_controlled_local_installation_plan_ready"
```

## Files Inspected

Governance files inspected read-only:

```text
0_architecture/governance/agent_platform_gbrain_bun_availability_installation_boundary.md
0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
```

GBrain source metadata inspected read-only:

```text
4_external/sources/gbrain-master/package.json
```

Path and presence checks were performed for:

```text
4_external/sources/gbrain-master
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
```

No credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, Claude credentials, package caches, `node_modules`, normal user `.gbrain`, `9_artifacts`, `graphify-out`, product paths, generated outputs, or raw Graphify outputs were inspected.

## Files Created

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_local_installation_plan.md
```

## Files Modified

No existing file was modified. The only file change is the new P12.BUN-INSTALL plan document.

## Commands Run

Allowed presence-only commands run:

```powershell
git status --short
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_bun_availability_installation_boundary.md"
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/bun.lock"
Get-Command bun -ErrorAction SilentlyContinue
Get-Command gbrain -ErrorAction SilentlyContinue
Get-Command node -ErrorAction SilentlyContinue
Get-Command npm -ErrorAction SilentlyContinue
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
Test-Path "$env:USERPROFILE\.bun\uninstall.ps1"
Test-Path "$env:LOCALAPPDATA\bun\bun.exe"
Test-Path "$env:APPDATA\bun\bun.exe"
```

Observed command results:

| Check | Result |
| --- | --- |
| Initial `git status --short` | `?? 0_architecture/implementation/graphify_command_candidate_confirmation.md` |
| P12.BUN boundary file | `True` |
| P12.SETUP file | `True` |
| GBrain source root | `True` |
| `package.json` | `True` |
| `bun.lock` | `True` |
| `Get-Command bun` | No output |
| `Get-Command gbrain` | No output |
| `Get-Command node` | `C:\Program Files\nodejs\node.exe` |
| `Get-Command npm` | `C:\Program Files\nodejs\npm.ps1` |
| `$env:USERPROFILE\.bun\bin\bun.exe` | `False` |
| `$env:USERPROFILE\.bun\uninstall.ps1` | `False` |
| `$env:LOCALAPPDATA\bun\bun.exe` | `False` |
| `$env:APPDATA\bun\bun.exe` | `False` |

Allowed read-only searches were used for P12.BUN markers, P12.SETUP markers, and root GBrain package metadata. One package metadata search returned incidental headings for nested GBrain package manifests due search behavior; those nested results were not used for this decision.

No Bun, GBrain, Node, npm, package-manager, Ollama, Graphify, test, build, script, CI, Docker, Python, install, uninstall, PATH modification, or environment mutation command was executed.

## P12.BUN Dependency Status

P12.BUN exists at:

```text
0_architecture/governance/agent_platform_gbrain_bun_availability_installation_boundary.md
```

P12.BUN final marker is present:

```text
gbrain_bun_availability_installation_boundary_ready
```

P12.BUN decision markers are present:

```text
bun_not_available_installation_gate_required
bun_installation_boundary_blocks_p12_install
```

P12.BUN recommended:

```text
P12.BUN-INSTALL - Bun Controlled Local Installation Plan
```

Dependency decision:

```yaml
p12_bun_dependency_confirmed: true
p12_bun_final_marker_confirmed: true
bun_missing_state_confirmed: true
p12_bun_install_plan_authorized: true
```

## Bun Current Availability Status

Current availability from allowed checks:

```yaml
bun_available_on_path: false
bun_candidate_binary_found_in_allowed_paths: false
bun_uninstall_script_found_in_allowed_path: false
bun_version_checked: false
bun_executed: false
bun_installed_by_this_ticket: false
```

Decision:

```yaml
bun_installation_plan_required: true
bun_install_execution_authorized_now: false
decision_marker: "bun_install_execution_still_blocked"
```

## Official Install Source Decision

Official Windows install source candidate from the Bun documentation context supplied for this ticket:

```powershell
powershell -c "irm bun.sh/install.ps1|iex"
```

Decision:

```yaml
official_source_required: true
official_windows_install_source_identified: true
install_command_executed_now: false
network_access_authorized_now: false
decision_marker: "bun_official_windows_install_source_identified"
```

P12.BUN-INSTALL does not fetch or verify web documentation. It records the official source candidate provided by the ticket context and routes execution to a later gate.

## Install Command Candidate

Future execution command candidate only:

```powershell
powershell -c "irm bun.sh/install.ps1|iex"
```

Rejected strategies by default:

| Strategy | Candidate | Reason |
| --- | --- | --- |
| npm global install | `npm install -g bun` | Uses npm/global package state and is not preferred while the official Bun script exists. |
| Scoop | `scoop install bun` | Requires Scoop availability and a package-manager boundary not yet reviewed. |
| winget | `winget install Oven-sh.Bun` | Uses a system package-manager path and requires separate winget/source/admin/PATH review. |
| Docker | `docker pull oven/bun` | Adds container/runtime boundary not needed for local GBrain source setup. |
| Direct zip/manual binary | manual download | Requires artifact verification and manual placement plan. |

Decision:

```yaml
preferred_future_install_command_candidate: 'powershell -c "irm bun.sh/install.ps1|iex"'
alternative_install_strategies_rejected_by_default: true
install_execution_requires_future_gate: true
decision_marker: "bun_install_execution_requires_human_approval"
```

## Install Scope

Preferred future installation scope:

```yaml
install_scope: "user-level"
expected_install_root_candidate: "$env:USERPROFILE\\.bun\\"
expected_binary_candidate: "$env:USERPROFILE\\.bun\\bin\\bun.exe"
expected_uninstall_candidate: "$env:USERPROFILE\\.bun\\uninstall.ps1"
admin_rights_expected: "false_or_unknown"
system_install_allowed_now: false
```

Decision:

```yaml
bun_user_level_install_candidate_selected: true
system_level_install_rejected_by_default: true
decision_marker: "bun_user_level_install_candidate_selected"
```

## Expected Created Files

Expected created paths if a future install runs successfully:

```text
$env:USERPROFILE\.bun\
$env:USERPROFILE\.bun\bin\
$env:USERPROFILE\.bun\bin\bun.exe
$env:USERPROFILE\.bun\uninstall.ps1
```

Possible created paths requiring future verification:

```text
$env:USERPROFILE\.bun\install\
Bun cache/state under the user profile
```

Blocked side effects:

```text
system PATH mutation unless explicitly approved
admin-level install unless explicitly approved
GBrain dependency install
node_modules creation
GBrain runtime config
GBrain DB/storage
Ollama model changes
Graphify execution
provider/API calls
Git mutation
```

No files or directories were created by P12.BUN-INSTALL except this plan document.

## PATH Boundary

Official Windows PATH repair candidate from the Bun documentation context supplied for this ticket:

```powershell
[System.Environment]::SetEnvironmentVariable(
  "Path",
  [System.Environment]::GetEnvironmentVariable("Path", "User") + ";$env:USERPROFILE\.bun\bin",
  [System.EnvironmentVariableTarget]::User
)
```

PATH decision:

```yaml
path_mutation_allowed_now: false
future_path_scope_candidate: "User PATH only"
system_path_mutation_allowed: false
shell_profile_mutation_allowed: false
candidate_user_path_entry: "$env:USERPROFILE\\.bun\\bin"
path_repair_candidate_identified: true
path_repair_authorized_now: false
terminal_restart_required_after_install: "true_or_unknown"
decision_marker: "bun_path_update_candidate_identified"
```

If future installation succeeds but `bun` remains undiscoverable, the next gate may be:

```text
P12.BUN-PATH - Bun PATH Boundary / Shell Availability Plan
```

unless P12.BUN-INSTALL-EXEC explicitly includes User PATH repair.

## Network / Download Boundary

Future Bun installation requires network download unless a direct local binary is approved under a separate gate.

```yaml
NetworkDownloadBoundary:
  network_required_for_future_install: true
  network_authorized_now: false
  allowed_destination_candidate:
    - "official Bun install endpoint only"
  blocked_destinations:
    - "GitHub arbitrary downloads unless exact official release artifact is approved"
    - "package registries for GBrain dependencies"
    - "OpenAI / Anthropic / Gemini / provider APIs"
    - "MCP servers"
    - "Graphify / external source fetching"
```

P12.BUN-INSTALL does not authorize network access. It identifies only that future installation execution will require network access.

## Rollback / Uninstall Posture

Future rollback/uninstall candidate only:

```powershell
powershell -c ~\.bun\uninstall.ps1
```

Decision:

```yaml
uninstall_candidate_identified: true
uninstall_script_present_now: false
rollback_authorized_now: false
decision_marker: "bun_uninstall_rollback_candidate_identified"
```

Future rollback plan must account for:

```text
whether uninstall.ps1 exists
whether PATH entry was added
whether PATH entry must be removed manually
whether temporary files/cache remain
whether terminal restart is needed
whether any unrelated Bun files existed before install
```

Forbidden rollback actions by default:

```text
edit system PATH
```

## Verification Candidates

Allowed verification in this plan was limited to presence checks. Future post-install verification candidates for P12.BUN-INSTALL-EXEC may include:

```powershell
Get-Command bun -ErrorAction SilentlyContinue
bun --version
bun --revision
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
Test-Path "$env:USERPROFILE\.bun\uninstall.ps1"
```

`bun --version` and `bun --revision` remain future execution verification commands only. They were not run by P12.BUN-INSTALL.

## P12.BUN-INSTALL-EXEC Handoff Decision

If this plan is accepted, the next execution ticket may be:

```text
P12.BUN-INSTALL-EXEC - Bun Controlled User-Level Installation Execution
```

It must require exact human approval and define:

```text
exact install command
network allowance
expected created paths
PATH behavior
rollback/uninstall
verification commands
incident stop rules
no GBrain dependency install
no GBrain execution
no node_modules
no providers
no Graphify
no Ollama
no Git mutation
```

Decision:

```yaml
p12_bun_install_exec_may_be_generated: true
p12_bun_install_exec_authorized_by_this_plan: false
must_stop_before_p12_install: true
```

Minimum approval for future Bun install execution:

```text
I approve one controlled user-level Bun installation using the exact approved official Bun installation command. Network access is allowed only for the Bun installer endpoint. Expected created files are limited to the user Bun installation directory. User PATH changes are allowed only if explicitly recorded and reversible. Do not install GBrain dependencies, do not run GBrain, do not create node_modules, do not run package managers inside GBrain, do not run providers, do not run Ollama, do not run Graphify, do not inspect credentials, do not create sandbox outputs, and do not mutate Git.
```

If PATH repair is included in the future execution ticket, the approval must explicitly include:

```text
I also approve adding the Bun user bin directory to User PATH if Bun installs successfully but is not discoverable from a new shell. Do not modify System PATH.
```

## P12.INSTALL Handoff Decision

P12.INSTALL remains blocked.

```yaml
P12_INSTALL_HandoffDecision:
  status: "blocked"
  reason: "Bun installation plan only; Bun not installed by this ticket."
  required_before_p12_install:
    - "P12.BUN-INSTALL accepted"
    - "P12.BUN-INSTALL-EXEC completed or Bun otherwise safely available"
    - "bun discoverable or approved absolute bun path available"
    - "P12.SETUP remains accepted"
    - "human approval for GBrain dependency install"
  decision_marker: "p12_install_still_blocked_until_bun_installed"
```

Future P12.INSTALL command candidate remains:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

P12.BUN-INSTALL does not authorize running that command.

## P12.0D Handoff Decision

P12.0D remains blocked.

```yaml
P12_0D_HandoffDecision:
  status: "blocked"
  reason: "Bun and GBrain dependency install are not completed."
  p12_0d_execution_authorized: false
  decision_marker: "gbrain_runtime_still_blocked"
```

P12.0D still requires:

```text
Bun available
P12.INSTALL accepted and completed
GBrain dependency state available
sandbox GBRAIN_HOME approved
sandbox DB path approved
exact runtime commands approved
human runtime approval present
```

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_local_installation_plan.md
```

Not created / not approved:

```text
No Bun execution
No Bun installation
No Bun version command
No PATH mutation
No user environment mutation
No system environment mutation
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
No Git mutation
No git add .
```

## Limitations

P12.BUN-INSTALL did not fetch official Bun documentation. It used the official Windows command candidates supplied in the ticket context.

P12.BUN-INSTALL did not run the installer, so expected created files and PATH behavior remain candidates for future execution verification.

P12.BUN-INSTALL did not run `bun --version` or `bun --revision`, so no Bun version or revision was confirmed.

P12.BUN-INSTALL did not inspect user or system environment variables, shell profiles, package caches, or installed application inventories.

P12.BUN-INSTALL did not prove whether another shell with a different PATH could find Bun.

## Recommended Next Ticket

If this plan is accepted, recommended next ticket:

```text
P12.BUN-INSTALL-EXEC - Bun Controlled User-Level Installation Execution
```

After Bun is installed and verified:

```text
P12.INSTALL - GBrain Controlled Local Dependency Install
```

Then, only after GBrain dependencies are installed under gate:

```text
P12.0D - GBrain Ollama Controlled Sandbox Execution
```

Graphify plus Ollama remains a separate optional path:

```text
P10.OLLAMA.0 - Graphify Ollama Local Provider Command / Scope Amendment
```

## Commit Commands

If this governance record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_bun_controlled_local_installation_plan.md
git commit -m "Plan Bun controlled local installation"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainBunControlledLocalInstallationPlan:
  ticket: P12.BUN-INSTALL
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_bun_controlled_local_installation_plan.md"
  plan_only: true
  p12_bun_dependency_confirmed: true
  p12_bun_final_marker_confirmed: true
  p12_bun_missing_marker_confirmed: true
  p12_setup_dependency_confirmed: true
  source_root_present: true
  package_json_present: true
  bun_lock_present: true
  bun_available_on_path: false
  bun_candidate_binary_found_in_allowed_paths: false
  bun_uninstall_script_found_in_allowed_path: false
  gbrain_available_on_path: false
  node_available_on_path: true
  npm_available_on_path: true
  official_windows_install_source_identified: true
  user_level_install_candidate_selected: true
  install_command_candidate: 'powershell -c "irm bun.sh/install.ps1|iex"'
  path_update_candidate_identified: true
  uninstall_rollback_candidate_identified: true
  network_required_for_future_install: true
  bun_install_executed: false
  bun_version_command_executed: false
  path_modified: false
  gbrain_executed: false
  package_manager_execution_performed: false
  dependencies_installed: false
  node_modules_created: false
  sandbox_created: false
  git_mutated: false
  p12_bun_install_exec_may_be_generated: true
  p12_install_ready_now: false
  p12_0d_execution_authorized: false
  final_marker: "gbrain_bun_controlled_local_installation_plan_ready"
```

Final marker:

```text
gbrain_bun_controlled_local_installation_plan_ready
```
