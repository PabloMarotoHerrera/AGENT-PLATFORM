# GBrain Bun Refreshed Shell Availability Verification

## Summary

P12.BUN-PATH-VERIFY checked Bun availability after the controlled user-level Bun installation and approved User PATH repair recorded by P12.BUN-INSTALL-EXEC.

Outcome: Bun files exist under the expected user-level path, but `Get-Command bun -ErrorAction SilentlyContinue` still returns no output in the shell available to this agent. Therefore `bun --version` and `bun --revision` were not run, because this ticket permits them only after `Get-Command bun` succeeds.

P12.INSTALL remains blocked. P12.0D remains blocked.

Result marker:

```text
gbrain_bun_refreshed_shell_availability_verification_ready
```

Decision markers:

```text
bun_binary_present_but_not_on_path
p12_install_still_blocked_after_bun_path_verify
```

```yaml
P12_BUN_PATH_VERIFY_Decision:
  ticket: P12.BUN-PATH-VERIFY
  date: "2026-07-09"
  outcome: "Outcome B - binary exists but bun is not on PATH"
  bun_binary_present: true
  bun_uninstall_script_present: true
  get_command_bun_result: "no output"
  bun_version_checked: false
  bun_revision_checked: false
  get_command_gbrain_result: "no output"
  p12_install_ready_now: false
  p12_0d_execution_authorized_now: false
  final_marker: "gbrain_bun_refreshed_shell_availability_verification_ready"
```

## Files Inspected

Governance files inspected read-only:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
0_architecture/governance/agent_platform_gbrain_bun_controlled_local_installation_plan.md
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

No credentials, `.env`, provider configs, token stores, browser auth, local credential stores, API keys, Claude credentials, package caches, `node_modules`, normal user `.gbrain`, `9_artifacts`, `graphify-out`, product paths, generated outputs, or raw Graphify outputs were inspected.

## Files Created

```text
0_architecture/governance/agent_platform_gbrain_bun_refreshed_shell_availability_verification.md
```

## Files Modified

No existing file was modified. The only file change for this ticket is the new P12.BUN-PATH-VERIFY record.

## Commands Run

Allowed verification commands run:

```powershell
git status --short
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/bun.lock"
Get-Command bun -ErrorAction SilentlyContinue
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
Test-Path "$env:USERPROFILE\.bun\uninstall.ps1"
Get-Command gbrain -ErrorAction SilentlyContinue
```

Allowed read-only searches and file reads were used to confirm governance markers and root GBrain package metadata.

Commands not run because `Get-Command bun` did not succeed:

```powershell
bun --version
bun --revision
```

Forbidden commands were not run:

```text
powershell -c "irm bun.sh/install.ps1|iex"
powershell -c ~\.bun\uninstall.ps1
[System.Environment]::SetEnvironmentVariable(...)
bun install
bun run
bun build
bun test
```

## P12.BUN-INSTALL-EXEC Dependency Status

P12.BUN-INSTALL-EXEC exists at:

```text
0_architecture/governance/agent_platform_gbrain_bun_controlled_user_level_installation_execution_record.md
```

P12.BUN-INSTALL-EXEC final marker is present:

```text
gbrain_bun_controlled_user_level_installation_execution_record_ready
```

P12.BUN-INSTALL-EXEC reported:

```text
bun_user_level_install_success
bun_user_level_install_path_repair_completed
installed_files_present_current_shell_path_refresh_pending
p12_install_still_blocked_after_bun_install_attempt
gbrain_runtime_still_blocked
```

Dependency decision:

```yaml
p12_bun_install_exec_dependency_confirmed: true
p12_bun_install_exec_final_marker_confirmed: true
install_success_recorded: true
path_repair_completed_recorded: true
path_refresh_pending_recorded: true
```

## Bun Binary Path Status

Allowed path check:

```powershell
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
```

Result:

```text
True
```

Decision:

```yaml
bun_binary_present: true
bun_binary_path_candidate: "C:\\Users\\pablo\\.bun\\bin\\bun.exe"
```

## Bun Uninstall Script Status

Allowed path check:

```powershell
Test-Path "$env:USERPROFILE\.bun\uninstall.ps1"
```

Result:

```text
True
```

Decision:

```yaml
bun_uninstall_script_present: true
bun_uninstall_script_path_candidate: "C:\\Users\\pablo\\.bun\\uninstall.ps1"
```

The uninstall script was not executed.

## Bun PATH Availability Status

Allowed PATH discovery command:

```powershell
Get-Command bun -ErrorAction SilentlyContinue
```

Result:

```text
No output
```

Decision:

```yaml
bun_discoverable_on_path: false
bun_binary_present_but_not_on_path: true
decision_marker: "bun_binary_present_but_not_on_path"
```

## Bun Version Result

`bun --version` was not run.

Reason:

```text
P12.BUN-PATH-VERIFY permits `bun --version` only if `Get-Command bun` succeeds first. `Get-Command bun` returned no output.
```

Decision:

```yaml
bun_version_verified: false
bun_version_result: "not run because bun is not discoverable on PATH"
```

## Bun Revision Result

`bun --revision` was not run.

Reason:

```text
P12.BUN-PATH-VERIFY permits `bun --revision` only if `Get-Command bun` succeeds first. `Get-Command bun` returned no output.
```

Decision:

```yaml
bun_revision_verified: false
bun_revision_result: "not run because bun is not discoverable on PATH"
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

Root GBrain `package.json` still declares:

```text
bin.gbrain = src/cli.ts
engines.bun >=1.3.10
postinstall can invoke gbrain apply-migrations if a gbrain command is discoverable
```

Decision:

```yaml
gbrain_available_on_path: false
gbrain_executed: false
gbrain_dependency_install_authorized_now: false
gbrain_runtime_authorized_now: false
```

## Verification Decision

Outcome B applies: binary exists but Bun is not on PATH.

```yaml
VerificationDecision:
  outcome: "Outcome B - binary exists but Bun is not on PATH"
  bun_binary_present: true
  bun_uninstall_script_present: true
  bun_get_command_succeeded: false
  bun_version_verified: false
  bun_revision_verified: false
  p12_install_ready_now: false
  p12_0d_execution_authorized_now: false
```

Decision markers:

```text
bun_binary_present_but_not_on_path
p12_install_still_blocked_after_bun_path_verify
```

## P12.INSTALL Handoff Decision

P12.INSTALL may not be generated from this verification result.

Reason:

```text
Bun binary exists, but `bun` is not discoverable through `Get-Command`; version and revision were not verified.
```

Decision:

```yaml
P12_INSTALL_HandoffDecision:
  status: "blocked"
  reason: "Bun is not discoverable on PATH in this shell."
  bun_binary_present: true
  bun_discoverable_on_path: false
  bun_version_verified: false
  bun_revision_verified: false
  p12_install_may_be_generated_now: false
  decision_marker: "p12_install_still_blocked_after_bun_path_verify"
```

When Bun becomes discoverable and version/revision verification succeeds, P12.INSTALL must still use only:

```powershell
bun install --ignore-scripts --frozen-lockfile
```

from:

```text
4_external/sources/gbrain-master
```

and must still block postinstall, build, runtime, GBrain execution, Ollama, providers, Graphify, and Git mutation.

## P12.0D Handoff Decision

P12.0D remains blocked regardless of this verification result.

Decision:

```yaml
P12_0D_HandoffDecision:
  status: "blocked"
  reason: "P12.INSTALL has not completed and GBrain dependency state is unavailable."
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
0_architecture/governance/agent_platform_gbrain_bun_refreshed_shell_availability_verification.md
```

Not created / not approved:

```text
No Bun installation
No Bun uninstall
No PATH mutation
No User PATH mutation
No System PATH mutation
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

This verification shell still does not discover `bun` through `Get-Command`, despite the expected Bun files being present. This may mean the agent process has not received the User PATH update, or that PATH repair requires a true terminal/editor restart outside the current process tree.

P12.BUN-PATH-VERIFY did not inspect User PATH or System PATH contents, did not modify PATH, and did not run environment variable dump commands.

P12.BUN-PATH-VERIFY did not run the Bun executable by absolute path because the ticket permits `bun --version` and `bun --revision` only after `Get-Command bun` succeeds.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.BUN-PATH - Bun PATH Boundary / Shell Availability Plan
```

That ticket should decide whether to verify or use the approved absolute Bun path, refresh the process environment, or perform another constrained PATH availability step without reinstalling Bun.

Do not proceed to P12.INSTALL until Bun is discoverable and `bun --version` / `bun --revision` succeed, or until an approved absolute Bun path boundary is explicitly accepted.

## Commit Commands

If this verification record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_bun_refreshed_shell_availability_verification.md
git commit -m "Verify Bun refreshed shell availability"
```

Push only if explicitly approved:

```powershell
git push
```

## Final Decision Record

```yaml
GBrainBunRefreshedShellAvailabilityVerification:
  ticket: P12.BUN-PATH-VERIFY
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_bun_refreshed_shell_availability_verification.md"
  p12_bun_install_exec_dependency_confirmed: true
  p12_bun_install_exec_final_marker_confirmed: true
  bun_install_success_recorded: true
  bun_path_repair_completed_recorded: true
  source_root_present: true
  package_json_present: true
  bun_lock_present: true
  bun_binary_present: true
  bun_uninstall_script_present: true
  bun_discoverable_on_path: false
  bun_version_checked: false
  bun_version_verified: false
  bun_revision_checked: false
  bun_revision_verified: false
  gbrain_available_on_path: false
  gbrain_executed: false
  bun_installation_performed: false
  path_mutated: false
  gbrain_dependency_install_attempted: false
  node_modules_created: false
  git_mutated: false
  p12_install_ready_now: false
  p12_0d_execution_authorized: false
  final_marker: "gbrain_bun_refreshed_shell_availability_verification_ready"
```

Final marker:

```text
gbrain_bun_refreshed_shell_availability_verification_ready
```
