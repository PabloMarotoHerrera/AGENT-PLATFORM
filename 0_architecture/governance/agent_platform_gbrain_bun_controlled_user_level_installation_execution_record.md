# GBrain Bun Controlled User-Level Installation Execution Record

## Summary

P12.BUN-INSTALL-EXEC performed one controlled user-level Bun installation attempt after explicit human approval was provided. The approved installer command ran exactly once:

```powershell
powershell -c "irm bun.sh/install.ps1|iex"
```

Installer output reported:

```text
Bun 1.3.14 was installed successfully.
The binary is located at C:\Users\pablo\.bun\bin\bun.exe
To get started, restart your terminal/editor, then type "bun"
```

Post-install checks confirmed `C:\Users\pablo\.bun\bin\bun.exe` and `C:\Users\pablo\.bun\uninstall.ps1` exist. `Get-Command bun -ErrorAction SilentlyContinue` still returned no output in the current agent shell. Because explicit User PATH repair approval was present, the User PATH repair command was run once. A terminal/editor restart or refreshed process environment is likely required before `bun` is discoverable in this agent shell.

`bun --version` and `bun --revision` were not run because `bun` was not discoverable through `Get-Command` after installation and PATH repair in the current agent shell.

P12.INSTALL remains blocked until Bun availability is verified in a refreshed shell or an approved absolute Bun path boundary is accepted. P12.0D remains blocked.

Result marker:

```text
gbrain_bun_controlled_user_level_installation_execution_record_ready
```

Result markers:

```text
bun_user_level_install_success
bun_user_level_install_path_repair_completed
p12_install_still_blocked_after_bun_install_attempt
```

```yaml
P12_BUN_INSTALL_EXEC_Result:
  ticket: P12.BUN-INSTALL-EXEC
  date: "2026-07-09"
  execution_status: "installed_path_repaired_current_shell_not_discoverable"
  human_install_approval_present: true
  human_path_repair_approval_present: true
  install_command_attempted: true
  install_command_execution_count: 1
  install_command_completed_successfully: true
  installed_version_reported_by_installer: "1.3.14"
  bun_available_before_install: false
  bun_user_binary_present_before_install: false
  bun_uninstall_script_present_before_install: false
  bun_user_binary_present_after_install: true
  bun_uninstall_script_present_after_install: true
  get_command_bun_after_install_before_path_repair: "no output"
  path_repair_attempted: true
  path_repair_scope: "User PATH only"
  get_command_bun_after_path_repair: "no output in current agent shell"
  bun_version_checked: false
  bun_revision_checked: false
  p12_install_ready_now: false
  p12_0d_execution_authorized_now: false
  final_marker: "gbrain_bun_controlled_user_level_installation_execution_record_ready"
```

## Files Inspected

Governance files inspected read-only:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_local_installation_plan.md
0_architecture/governance/agent_platform_gbrain_bun_availability_installation_boundary.md
0_architecture/governance/agent_platform_gbrain_controlled_local_install_build_plan.md
```

GBrain source metadata inspected read-only:

```text
4_external/sources/gbrain-master/package.json
```

Presence-only checks were performed for:

```text
4_external/sources/gbrain-master
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
```

No credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, Claude credentials, package caches, `node_modules`, normal user `.gbrain`, `9_artifacts`, `graphify-out`, product paths, generated outputs, raw Graphify outputs, or external source roots outside the approved GBrain source metadata paths were inspected.

## Files Created

Repo output file:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
```

Outside-repo files confirmed created by the Bun installer:

```text
C:\Users\pablo\.bun\bin\bun.exe
C:\Users\pablo\.bun\uninstall.ps1
```

The parent Bun user installation directory also exists by implication:

```text
C:\Users\pablo\.bun\
C:\Users\pablo\.bun\bin\
```

## Files Modified

Repo file modified:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
```

Outside-repo user environment modified:

```text
User PATH was updated with C:\Users\pablo\.bun\bin by the approved User PATH repair command.
```

System PATH was not modified by the agent. Shell profiles were not modified by the agent.

## Commands Run

Allowed preflight commands run:

```powershell
git status --short
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_bun_controlled_local_installation_plan.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/bun.lock"
Get-Command bun -ErrorAction SilentlyContinue
Get-Command gbrain -ErrorAction SilentlyContinue
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
Test-Path "$env:USERPROFILE\.bun\uninstall.ps1"
```

Approved install command run exactly once:

```powershell
powershell -c "irm bun.sh/install.ps1|iex"
```

Allowed post-install checks run:

```powershell
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
Test-Path "$env:USERPROFILE\.bun\uninstall.ps1"
Get-Command bun -ErrorAction SilentlyContinue
```

Approved User PATH repair command run once:

```powershell
[System.Environment]::SetEnvironmentVariable(
  "Path",
  [System.Environment]::GetEnvironmentVariable("Path", "User") + ";$env:USERPROFILE\.bun\bin",
  [System.EnvironmentVariableTarget]::User
)
```

Allowed post-repair checks run:

```powershell
Get-Command bun -ErrorAction SilentlyContinue
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
Test-Path "$env:USERPROFILE\.bun\uninstall.ps1"
```

Commands not run:

```text
bun --version
bun --revision
bun install
bun run
bun build
bun test
```

## Human Approval Status

Required installation approval was present:

```text
I approve one controlled user-level Bun installation using `powershell -c "irm bun.sh/install.ps1|iex"`. Network access is allowed only for the Bun installer endpoint. Expected created files are limited to the user Bun installation directory under `%USERPROFILE%\.bun`. Do not install GBrain dependencies, do not run GBrain, do not run `bun install` inside GBrain, do not create node_modules, do not run package lifecycle scripts, do not run providers, do not run Ollama, do not run Graphify, do not inspect credentials, do not create sandbox outputs, do not modify System PATH, and do not mutate Git.
```

Optional PATH repair approval was present:

```text
I also approve adding `%USERPROFILE%\.bun\bin` to User PATH if Bun installs successfully but is not discoverable. Do not modify System PATH.
```

Decision:

```yaml
human_install_approval_present: true
human_path_repair_approval_present: true
install_execution_allowed: true
path_repair_allowed: true
```

## Preflight Status

P12.BUN-INSTALL exists at:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_local_installation_plan.md
```

P12.BUN-INSTALL final marker is present:

```text
gbrain_bun_controlled_local_installation_plan_ready
```

GBrain source root exists:

```text
4_external/sources/gbrain-master
```

Preflight results before install:

```yaml
get_command_bun_before_install: "no output"
get_command_gbrain_before_install: "no output"
bun_user_binary_before_install: false
bun_uninstall_script_before_install: false
gbrain_source_root_present: true
package_json_present: true
bun_lock_present: true
safe_to_run_install_command: true
```

## Bun Install Execution Status

The approved install command ran once and completed successfully according to installer output.

```yaml
install_command_candidate: 'powershell -c "irm bun.sh/install.ps1|iex"'
install_command_attempted: true
install_command_execution_count: 1
install_command_completed_successfully: true
installer_reported_version: "1.3.14"
installer_reported_binary_path: "C:\\Users\\pablo\\.bun\\bin\\bun.exe"
installer_reported_restart_required: true
result_marker: "bun_user_level_install_success"
```

No GBrain dependency install was attempted.

## Created Path Metadata

Preflight path status before install:

| Path | Status |
| --- | --- |
| `%USERPROFILE%\.bun\bin\bun.exe` | `False` |
| `%USERPROFILE%\.bun\uninstall.ps1` | `False` |

Post-install path status:

| Path | Status |
| --- | --- |
| `%USERPROFILE%\.bun\bin\bun.exe` | `True` |
| `%USERPROFILE%\.bun\uninstall.ps1` | `True` |

Created outside repo by install:

```text
C:\Users\pablo\.bun\bin\bun.exe
C:\Users\pablo\.bun\uninstall.ps1
```

No GBrain source files, `node_modules`, sandbox directories, databases, or generated outputs were created by this ticket.

## PATH Status

`Get-Command bun -ErrorAction SilentlyContinue` returned no output after install, even though `bun.exe` existed at the expected path. Approved User PATH repair was therefore performed.

PATH repair status:

```yaml
user_path_repair_required_after_install: true
user_path_repair_approved: true
user_path_repair_performed: true
system_path_modified_by_agent: false
shell_profile_modified_by_agent: false
terminal_restart_likely_required: true
result_marker: "bun_user_level_install_path_repair_completed"
```

Post-repair `Get-Command bun -ErrorAction SilentlyContinue` still returned no output in the current agent shell. This is consistent with the installer restart note and with User PATH registry changes not necessarily refreshing the already-running agent process environment.

## Verification Results

Pre-install discovery:

```yaml
get_command_bun_before_install: "no output"
bun_user_binary_before_install: false
bun_uninstall_script_before_install: false
```

Post-install and post-repair verification:

```yaml
bun_user_binary_after_install: true
bun_uninstall_script_after_install: true
get_command_bun_after_install_before_path_repair: "no output"
get_command_bun_after_path_repair: "no output in current agent shell"
bun_version_checked: false
bun_revision_checked: false
verification_status: "installed_files_present_current_shell_path_refresh_pending"
```

`bun --version` and `bun --revision` were not run because `bun` was not discoverable through `Get-Command` after installation and PATH repair in the current agent shell.

## Incident Status

No installer failure was observed. The remaining issue is current-shell PATH refresh, not a failed Bun installation.

```yaml
incident_status: "path_refresh_pending"
installer_failed: false
bun_executable_missing: false
verification_failure: false
secrets_exposed: false
system_path_modified_by_agent: false
git_mutated: false
gbrain_dependency_install_attempted: false
runtime_attempted: false
```

## P12.INSTALL Handoff Decision

P12.INSTALL remains blocked for the current agent shell because `Get-Command bun` still returns no output and `bun --version` / `bun --revision` were not verified.

```yaml
P12_INSTALL_HandoffDecision:
  status: "blocked_pending_refreshed_shell_bun_verification"
  reason: "Bun installed and User PATH repair completed, but current agent shell does not yet discover bun."
  bun_installed_under_expected_user_path: true
  user_path_repair_completed: true
  bun_discoverable_in_current_agent_shell: false
  bun_version_verified: false
  bun_revision_verified: false
  p12_install_may_be_generated_now: false
  decision_marker: "p12_install_still_blocked_after_bun_install_attempt"
```

Future P12.INSTALL must still use only the approved GBrain dependency install candidate after Bun is discoverable and after separate human approval:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

P12.BUN-INSTALL-EXEC does not authorize running that command.

## P12.0D Handoff Decision

P12.0D remains blocked.

```yaml
P12_0D_HandoffDecision:
  status: "blocked"
  reason: "P12.INSTALL was not completed and GBrain dependency state is unavailable."
  p12_0d_execution_authorized: false
  decision_marker: "gbrain_runtime_still_blocked"
```

P12.0D still requires:

```text
P12.INSTALL accepted and completed
GBrain dependency state available
sandbox GBRAIN_HOME approved
sandbox DB path approved
exact runtime commands approved
human runtime approval present
```

## Created / Not Created Register

Created in repo:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
```

Created outside repo:

```text
C:\Users\pablo\.bun\bin\bun.exe
C:\Users\pablo\.bun\uninstall.ps1
```

Modified outside repo:

```text
User PATH repaired with C:\Users\pablo\.bun\bin
```

Not created / not approved:

```text
No GBrain dependency install
No node_modules
No GBrain execution
No gbrain --help
No gbrain --version
No bun install inside GBrain
No package lifecycle scripts
No postinstall
No migrations
No build
No runtime
No sandbox directories
No DB/storage/output
No Ollama inference
No Graphify execution
No provider/API calls
No credential inspection
No System PATH mutation by agent
No shell profile mutation by agent
No Git mutation
No git add .
```

## Limitations

`bun --version` and `bun --revision` were not run because `bun` was not discoverable in the current agent shell after install and User PATH repair.

System PATH was not inspected; it was only not modified by the agent.

User PATH content was not printed. The approved User PATH repair command reads and updates User PATH without exposing environment values in output.

A refreshed terminal/editor or new agent process may be required before `Get-Command bun` resolves through PATH.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.BUN-PATH-VERIFY - Bun Refreshed Shell Availability Verification
```

That ticket should run only:

```powershell
Get-Command bun -ErrorAction SilentlyContinue
bun --version
bun --revision
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
Test-Path "$env:USERPROFILE\.bun\uninstall.ps1"
```

If Bun is discoverable and version/revision verification succeeds, then proceed to:

```text
P12.INSTALL - GBrain Controlled Local Dependency Install
```

## Commit Commands

If this execution record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
git commit -m "Record Bun controlled user-level installation"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainBunControlledUserLevelInstallationExecutionRecord:
  ticket: P12.BUN-INSTALL-EXEC
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md"
  p12_bun_install_plan_confirmed: true
  p12_bun_install_marker_confirmed: true
  human_install_approval_present: true
  human_path_repair_approval_present: true
  install_blocked_before_execution: false
  install_command_attempted: true
  install_command_execution_count: 1
  install_command_completed_successfully: true
  installer_reported_version: "1.3.14"
  bun_available_before_install: false
  bun_user_binary_present_before_install: false
  bun_uninstall_script_present_before_install: false
  bun_user_binary_present_after_install: true
  bun_uninstall_script_present_after_install: true
  get_command_bun_after_path_repair: "no output in current agent shell"
  bun_version_checked: false
  bun_revision_checked: false
  path_repair_attempted: true
  path_repair_completed: true
  user_path_modified: true
  system_path_modified_by_agent: false
  gbrain_available_on_path: false
  gbrain_dependency_install_attempted: false
  gbrain_runtime_attempted: false
  node_modules_created: false
  sandbox_created: false
  git_mutated: false
  p12_install_ready_now: false
  p12_0d_execution_authorized: false
  final_marker: "gbrain_bun_controlled_user_level_installation_execution_record_ready"
```

Final marker:

```text
gbrain_bun_controlled_user_level_installation_execution_record_ready
```
