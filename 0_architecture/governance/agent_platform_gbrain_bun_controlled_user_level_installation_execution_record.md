# GBrain Bun Controlled User-Level Installation Execution Record

## Summary

P12.BUN-INSTALL-EXEC performed the allowed preflight checks for one controlled user-level Bun installation attempt, but did not run the Bun installer because the required explicit human approval statement was not present.

No Bun installation was attempted. No Bun verification command was run. No PATH repair was performed. No GBrain dependency installation, GBrain runtime command, `node_modules` creation, package lifecycle script, Ollama command, Graphify command, provider call, sandbox output, credential inspection, or Git mutation occurred.

Result marker:

```text
gbrain_bun_controlled_user_level_installation_execution_record_ready
```

Result markers:

```text
bun_user_level_install_blocked_before_execution
p12_install_still_blocked_after_bun_install_attempt
```

```yaml
P12_BUN_INSTALL_EXEC_Result:
  ticket: P12.BUN-INSTALL-EXEC
  date: "2026-07-09"
  execution_status: "blocked_before_installation"
  human_approval_present: false
  install_command_attempted: false
  install_command_allowed_candidate: 'powershell -c "irm bun.sh/install.ps1|iex"'
  bun_available_before_install: false
  bun_user_binary_present_before_install: false
  bun_uninstall_script_present_before_install: false
  path_repair_attempted: false
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

Presence-only checks were also performed for:

```text
4_external/sources/gbrain-master
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
```

No credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, Claude credentials, package caches, `node_modules`, normal user `.gbrain`, `9_artifacts`, `graphify-out`, product paths, generated outputs, raw Graphify outputs, or external source roots outside the approved GBrain source metadata paths were inspected.

## Files Created

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
```

## Files Modified

No existing file was modified. The only repo file change is this new P12.BUN-INSTALL-EXEC execution record.

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

Additional allowed presence-only checks run during preflight context:

```powershell
Get-Command node -ErrorAction SilentlyContinue
Get-Command npm -ErrorAction SilentlyContinue
```

Observed command results:

| Check | Result |
| --- | --- |
| Initial `git status --short` | `?? 0_architecture/implementation/graphify_command_candidate_confirmation.md` |
| P12.BUN-INSTALL plan file | `True` |
| GBrain source root | `True` |
| `package.json` | `True` |
| `bun.lock` | `True` |
| `Get-Command bun` | No output |
| `Get-Command gbrain` | No output |
| `Get-Command node` | `C:\Program Files\nodejs\node.exe` |
| `Get-Command npm` | `C:\Program Files\nodejs\npm.ps1` |
| `$env:USERPROFILE\.bun\bin\bun.exe` | `False` |
| `$env:USERPROFILE\.bun\uninstall.ps1` | `False` |

Allowed read-only searches were used to confirm P12.BUN-INSTALL, P12.BUN, P12.SETUP, and root GBrain package metadata markers.

Commands not run:

```text
powershell -c "irm bun.sh/install.ps1|iex"
bun --version
bun --revision
bun install
gbrain
node --version
npm install
ollama
graphify
/graphify
```

## Human Approval Status

Required approval statement was not present.

Required minimum installation approval:

```text
I approve one controlled user-level Bun installation using `powershell -c "irm bun.sh/install.ps1|iex"`. Network access is allowed only for the Bun installer endpoint. Expected created files are limited to the user Bun installation directory under `%USERPROFILE%\.bun`. Do not install GBrain dependencies, do not run GBrain, do not run `bun install` inside GBrain, do not create node_modules, do not run package lifecycle scripts, do not run providers, do not run Ollama, do not run Graphify, do not inspect credentials, do not create sandbox outputs, do not modify System PATH, and do not mutate Git.
```

Optional PATH repair approval was also not present:

```text
I also approve adding `%USERPROFILE%\.bun\bin` to User PATH if Bun installs successfully but is not discoverable. Do not modify System PATH.
```

Decision:

```yaml
human_install_approval_present: false
human_path_repair_approval_present: false
install_execution_allowed: false
path_repair_allowed: false
decision_marker: "bun_user_level_install_blocked_before_execution"
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

P12.BUN-INSTALL confirms:

```text
bun_install_execution_requires_human_approval
bun_install_execution_still_blocked
p12_install_still_blocked_until_bun_installed
```

GBrain source root exists:

```text
4_external/sources/gbrain-master
```

Preflight decision:

```yaml
p12_bun_install_plan_confirmed: true
p12_bun_install_marker_confirmed: true
gbrain_source_root_present: true
human_approval_gate_satisfied: false
safe_to_run_install_command: false
```

## Bun Install Execution Status

The official install candidate was not executed.

```yaml
install_command_candidate: 'powershell -c "irm bun.sh/install.ps1|iex"'
install_command_attempted: false
install_command_completed_successfully: false
install_command_failure_observed: false
blocker: "explicit human approval missing"
result_marker: "bun_user_level_install_blocked_before_execution"
```

No network access was authorized or used for Bun installation.

## Created Path Metadata

Preflight path status before any install command:

| Path | Status |
| --- | --- |
| `%USERPROFILE%\.bun\bin\bun.exe` | Not present from allowed check |
| `%USERPROFILE%\.bun\uninstall.ps1` | Not present from allowed check |

Created outside repo by this ticket:

```text
None
```

Expected Bun install paths remain future candidates only:

```text
%USERPROFILE%\.bun\
%USERPROFILE%\.bun\bin\bun.exe
%USERPROFILE%\.bun\uninstall.ps1
```

## PATH Status

PATH repair was not attempted.

```yaml
user_path_modified_by_this_ticket: false
system_path_modified_by_this_ticket: false
shell_profile_modified_by_this_ticket: false
path_repair_required_now: false
path_repair_allowed_now: false
```

Because Bun was not installed, PATH repair was not evaluated beyond noting that the optional human PATH repair approval was absent.

## Verification Results

Pre-install discovery:

```yaml
get_command_bun_before_install: "no output"
bun_user_binary_before_install: false
bun_uninstall_script_before_install: false
```

Post-install verification was not run because installation was blocked before execution.

```yaml
bun_version_checked: false
bun_revision_checked: false
get_command_bun_after_install: "not run"
bun_user_binary_after_install: "not checked after install because install did not run"
bun_uninstall_script_after_install: "not checked after install because install did not run"
```

## Incident Status

This is a controlled pre-execution block, not an installer failure.

```yaml
incident_status: "no_install_incident"
safe_stop_reason: "explicit human approval missing"
secrets_exposed: false
system_path_modified: false
git_mutated: false
gbrain_dependency_install_attempted: false
runtime_attempted: false
```

## P12.INSTALL Handoff Decision

P12.INSTALL remains blocked.

```yaml
P12_INSTALL_HandoffDecision:
  status: "blocked"
  reason: "Bun installation did not run because explicit human approval was missing."
  bun_installed_and_discoverable: false
  approved_absolute_bun_path_available: false
  p12_install_may_be_generated_now: false
  decision_marker: "p12_install_still_blocked_after_bun_install_attempt"
```

Future P12.INSTALL must still use only the approved GBrain dependency install candidate after Bun is available and after separate human approval:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

P12.BUN-INSTALL-EXEC does not authorize running that command.

## P12.0D Handoff Decision

P12.0D remains blocked.

```yaml
P12_0D_HandoffDecision:
  status: "blocked"
  reason: "Bun was not installed, P12.INSTALL was not completed, and GBrain dependency state is unavailable."
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

Created:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
```

Created outside repo:

```text
None
```

Not created / not approved:

```text
No Bun installation
No Bun version command
No Bun revision command
No PATH mutation
No User PATH mutation
No System PATH mutation
No shell profile mutation
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
No Git mutation
No git add .
```

## Limitations

No Bun install attempt occurred, so no installer success/failure, created files, PATH behavior, Bun version, or Bun revision were verified.

System PATH was not inspected; it was only not modified by this ticket.

User PATH was not inspected; it was only not modified by this ticket.

One allowed root package metadata search returned an incidental nested GBrain package manifest line due search behavior; nested metadata was not used for this execution decision.

## Recommended Next Ticket

Recommended next action: rerun or continue P12.BUN-INSTALL-EXEC only after explicit human approval is provided.

Minimum approval to proceed with installation:

```text
I approve one controlled user-level Bun installation using `powershell -c "irm bun.sh/install.ps1|iex"`. Network access is allowed only for the Bun installer endpoint. Expected created files are limited to the user Bun installation directory under `%USERPROFILE%\.bun`. Do not install GBrain dependencies, do not run GBrain, do not run `bun install` inside GBrain, do not create node_modules, do not run package lifecycle scripts, do not run providers, do not run Ollama, do not run Graphify, do not inspect credentials, do not create sandbox outputs, do not modify System PATH, and do not mutate Git.
```

If PATH repair should be allowed in the same execution ticket, also provide:

```text
I also approve adding `%USERPROFILE%\.bun\bin` to User PATH if Bun installs successfully but is not discoverable. Do not modify System PATH.
```

## Commit Commands

If this execution record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
git commit -m "Record Bun controlled user-level installation block"
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
  human_install_approval_present: false
  human_path_repair_approval_present: false
  install_blocked_before_execution: true
  install_command_attempted: false
  install_command_completed_successfully: false
  bun_available_before_install: false
  bun_user_binary_present_before_install: false
  bun_uninstall_script_present_before_install: false
  bun_version_checked: false
  bun_revision_checked: false
  path_repair_attempted: false
  user_path_modified: false
  system_path_modified: false
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
