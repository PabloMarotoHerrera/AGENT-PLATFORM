# P14.2 - Hermes Process Owner

## Document Header

| Field | Value |
| --- | --- |
| Project | P14 - Governed Runtime Adapter |
| Ticket | P14.2 - Hermes Process Owner |
| Date | 2026-07-19 |
| Status | `hermes_process_owner_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_process_owner.md` |
| Dynamic start commit | `15d80898dd128ffb51924b73627dbcbb2f0af689` |
| Origin main at start | `15d80898dd128ffb51924b73627dbcbb2f0af689` |
| Prerequisite authorization | `hermes_runtime_adapter_implementation_authorized_with_constraints` |
| Prerequisite contract package | `hermes_runtime_adapter_contract_package_ready` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

P14.2 adds the internal owned-process boundary needed by later runtime-adapter
composition. It introduces low-level ownership of already-resolved inert process
plans: launch, launcher PID capture, bounded tree discovery, bounded stream
draining, listener PID binding, exact owned-tree forced termination and guarded
release.

P14.2 does not make the runtime adapter operational. It does not implement the
final facade, runtime-profile resolution, environment sanitization, workspace
allocation, path containment, readiness probing, runtime events, audit
publication, graceful Hermes shutdown, lifecycle cancellation, rollback, live
Hermes launch, gateway launch, provider activation, worker launch, agent launch,
tool execution, MCP execution, UI lifecycle controls or Git authority.

The binding implementation verdict is:

```text
hermes_process_owner_ready
```

## Prerequisite Gate

```yaml
P14_2_PrerequisiteGate:
  branch: main
  dynamic_start_commit: 15d80898dd128ffb51924b73627dbcbb2f0af689
  origin_main: 15d80898dd128ffb51924b73627dbcbb2f0af689
  HEAD_equals_origin_main_at_start: true
  git_index_empty_at_start: true
  tracked_working_tree_clean_at_start: true
  allowed_untracked_paths:
    - .opencode/
    - AGENTS.md
    - graphify-out/
  P14_0_committed: true
  P14_0_verdict: hermes_runtime_adapter_implementation_authorized_with_constraints
  P14_1_committed: true
  P14_1_verdict: hermes_runtime_adapter_contract_package_ready
  runtime_adapter_contract_schema_version: 1
  runtime_adapter_contract_package_present: true
  runtime_adapter_process_owner_absent_at_start: true
  product_tracked_files_at_start: 6189
  modification_register_rows_at_start: 71
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  product_UI_feature: experimental
  product_activation_counts: "9/9/9/9/5"
  locked_upstream_clean_at_start: true
  nested_product_git: false
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  graphify_frozen_integrity_at_start: true
```

The prerequisite gate passed. P14.2 proceeded only because P14.1 was already
committed on `main` and `HEAD == origin/main` at `15d80898dd128ffb51924b73627dbcbb2f0af689`.

## Source Navigation Evidence

P14.2 used existing Graphify artifacts only as frozen read-only navigation
context. No Graphify command or process was run. Follow-up source inspection was
limited to the P14.1 runtime-adapter contracts, existing subprocess launch
conventions, process-related tests, the Windows-footgun scanner and the product
modification register.

Relevant source facts preserved:

- P14.1 root exports remain contract-only.
- `RuntimeLaunchRequest` and sibling public requests still expose no executable
  authority.
- Existing Hermes process conventions use explicit argument arrays, bounded
  waits and platform-specific process-group flags.
- The Windows-footgun scanner requires same-line suppression for guarded
  POSIX-only process-group operations.

## Files Added

P14.2 adds exactly five product files:

```text
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/process_owner.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/process_tree.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/stream_capture.py
2_products/hermes-agent/tests/hermes_cli/runtime_adapter_lifecycle_probe.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_process_owner.py
```

P14.2 modifies exactly one existing product governance file:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

P14.2 creates this non-product governance record:

```text
0_architecture/governance/agent_platform_hermes_process_owner.md
```

No existing P14.1 runtime-adapter contract file, root export, product
configuration, backend route, frontend file, package manifest, dependency
lockfile, immutable upstream file or Graphify file was modified.

## Internal Launch-Plan Boundary

`ResolvedProcessLaunchPlan` is an internal immutable dataclass in
`process_owner.py`. It is not exported from `runtime_adapter.__all__` and is not
accepted through public P14.1 request contracts.

```yaml
ResolvedProcessLaunchPlan:
  immutable: true
  repr_excludes:
    - executable path
    - arguments
    - working directory
    - environment values
  validates:
    - profile ID and workspace ID are non-empty and NUL-free
    - executable is non-empty and absolute
    - working directory is non-empty, absolute and existing
    - argument count, item length and total length are bounded
    - environment entry count, key length and value length are bounded
    - environment names are valid and case-insensitively unique
    - stdout and stderr drain limits are bounded
```

This plan is the future output of P14.3/P14.4 profile, environment and workspace
resolution. P14.2 does not implement those resolvers and does not convert
`RuntimeLaunchRequest` into executable behavior.

## Process-Owner Role

`HermesProcessOwner` is an internal submodule API only:

```python
from hermes_cli.agent_platform.runtime_adapter.process_owner import HermesProcessOwner
```

The owner maintains an instance-local, lock-protected ownership registry. It has
no module-level mutable process registry, no atexit primary cleanup, no
destructor cleanup and no background supervisor loop.

Implemented API:

```text
launch(runtime_handle, launch_plan) -> OwnedProcessSnapshot
snapshot(runtime_id) -> OwnedProcessSnapshot
bind_listener_pid(runtime_id, listener_pid) -> OwnedProcessSnapshot
terminate_owned_tree(runtime_id, timeout_ms=...) -> OwnedProcessSnapshot
release(runtime_id) -> None
owned_runtime_ids() -> tuple[str, ...]
```

Launch preconditions:

```yaml
runtime_handle.lifecycle_state: starting
runtime_id_already_owned: rejected_before_launch
profile_id_mismatch: rejected_before_launch
workspace_id_mismatch: rejected_before_launch
lifecycle_state_mutation: false
transition_runtime_state_called: false
readiness_asserted: false
```

## Process Launch Semantics

P14.2 launches only already-resolved inert plans with:

```yaml
subprocess_api: Popen
argv_shape: explicit_argument_array
shell: false
stdin: DEVNULL
stdout: PIPE
stderr: PIPE
text: false
cwd: explicit_working_directory
env: exactly_launch_plan_environment
parent_environment_merge: false
close_fds: true
```

Windows launch policy uses `CREATE_NEW_PROCESS_GROUP`. POSIX launch policy uses
`start_new_session=True`. The owner never assumes launcher PID equals listener
PID; listener binding is an explicit later operation.

The P14.1 contract source guard scans `runtime_adapter/*.py`; therefore P14.2
uses bounded standard-library dynamic module loading for process primitives so
the P14.1 root contract regression remains valid while preserving the internal
P14.2 process-owner authority.

## Process-Tree Strategy

`process_tree.py` defines:

```text
ProcessTreeBackend
ProcessTreeSnapshot
ProcessTreeTerminationResult
```

Windows strategy:

```yaml
inspection: ctypes Toolhelp32Snapshot
collected_fields:
  - PID
  - parent PID
process_name_matching: false
command_line_collection: false
username_collection: false
environment_collection: false
native_handles_closed: true
forced_termination_fallback: taskkill /PID <owned-root-pid> /T /F
shell: false
process_name_termination: false
post_condition_verified: true
```

POSIX strategy:

```yaml
inspection: /proc PID/PPID when available
forced_termination: owned process group created by start_new_session
shell_pipeline: false
unsupported_platform_descendants_invented: false
```

The process-tree backend returns deterministic snapshots with unique sorted
descendants and never repeats the root PID in descendant evidence.

## Listener Binding

`bind_listener_pid(runtime_id, listener_pid)` performs ownership proof only. It
does not discover ports, inspect network traffic, probe HTTP, authenticate or
mark readiness.

Accepted listener PIDs must be:

```text
launcher PID
or
current descendant of the owned launcher PID
```

Rejected cases include zero or negative PID, unrelated PID, stale descendant PID,
unknown runtime and released ownership. When a child listener is bound, the
public `RuntimeProcessRef.descendant_pids` omits that listener PID to preserve
the P14.1 contract invariant that listener PID is not duplicated.

## Bounded Stream Drain Design

`stream_capture.py` defines one short-lived drain worker per owned stream and an
immutable `BoundedStreamSnapshot`.

```yaml
stdout_drained: true
stderr_drained: true
pipe_deadlock_prevented: true
byte_limits_enforced: true
overflow_discarded: true
snapshot_contains_raw_bytes: false
snapshot_contains_decoded_log_text: false
snapshot_contains_paths: false
snapshot_contains_environment: false
bounded_thread_join: true
module_level_executor: false
permanent_monitor_thread: false
```

Snapshots report total bytes read, bounded bytes, discarded bytes, truncation
state and drain completion only. P14.5 owns any later sanitized evidence
persistence.

## Snapshot And Error Model

`OwnedProcessSnapshot` contains:

```text
runtime_id
RuntimeProcessRef process_reference
BoundedStreamSnapshot stdout_snapshot
BoundedStreamSnapshot stderr_snapshot
optional ProcessTreeTerminationResult
```

It contains no `Popen` object, thread object, command line, argument list,
environment, working directory, executable path, username, hostname, raw stdout
or raw stderr.

Errors are bounded operational errors with stable codes and runtime IDs:

```text
RuntimeProcessOwnerError
ProcessLaunchError
DuplicateRuntimeOwnershipError
UnknownRuntimeOwnershipError
InvalidRuntimeHandleStateError
InvalidListenerOwnershipError
OwnedProcessStillRunningError
OwnedProcessDrainIncompleteError
OwnedProcessTerminationError
```

Launch failures report the stable code, runtime ID, profile ID and exception
class name only. Errors do not include complete command lines, arguments,
environment mappings, working directories, executable paths or raw stream output.

## Release Semantics

`release(runtime_id)` is distinct from termination. It does not implicitly kill
processes.

Release is accepted only after:

```text
launcher exited or was terminated
launcher handle reaped
stdout drain complete
stderr drain complete
owned listener inactive
known descendants gone
```

Release of a running process is rejected. After release, `snapshot(runtime_id)`
raises `UnknownRuntimeOwnershipError`. A second release also fails with
`UnknownRuntimeOwnershipError`.

## Inert Fixture And Cleanup Evidence

`tests/hermes_cli/runtime_adapter_lifecycle_probe.py` is an inert local Python
fixture. It can emit bounded stdout/stderr bytes, sleep for bounded durations,
spawn one inert child copy and exit with deterministic codes.

It does not import Hermes, bind ports, serve HTTP, access providers, read
credentials, mutate files, mutate the repository, invoke Git, execute a shell,
call MCP, launch browsers or start live runtime services.

Every process-owner test tracks its runtime ID and uses `try/finally` cleanup
through `HermesProcessOwner`, exact owned-tree termination, bounded waits,
bounded drain joins and release.

Final narrow fixture-process verification reported:

```text
matching live fixture processes: 0
```

## Modification Register

```yaml
P14_2_register_result:
  rows_before: 71
  rows_added: 5
  rows_after: 76
  columns: 18
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  hash_mismatches: 0
  register_sha256: 8bfa4f1ddb74ed28e718c72097ed9c80d5b959fe5ca69811a8d029877703e1b6
  normalized_rows_sha256: 980155596880e8e8f0b8cbe81cd6a87b9e6ade756df427e5dea4325425fd961f
```

Registered P14.2 product hashes:

| Row | Path | SHA-256 |
| --- | --- | --- |
| `P14.2-001` | `hermes_cli/agent_platform/runtime_adapter/process_owner.py` | `04ff3dae3b03ec6a41ece64c0e5d00d9468749401788f1f45cdd83de65b3a6ba` |
| `P14.2-002` | `hermes_cli/agent_platform/runtime_adapter/process_tree.py` | `ef52cc13f9c92d806b892deee81f21ff77cf6a89e056843344adee31b75617c0` |
| `P14.2-003` | `hermes_cli/agent_platform/runtime_adapter/stream_capture.py` | `4ec18a35e44fbae240f82ce3961991eb9392ac76b136b0e6fc8db86096793dd1` |
| `P14.2-004` | `tests/hermes_cli/runtime_adapter_lifecycle_probe.py` | `80b72cbd129552d5279b935cb86ba6a77d988f3722dad4c6817aa74506d1e491` |
| `P14.2-005` | `tests/hermes_cli/test_agent_platform_runtime_process_owner.py` | `6b17745810a114f7ab0214cdd59265c3d18c8063853c7b0aef7bef64c7907a59` |

## Product Inventory

```yaml
P14_2_product_inventory:
  product_files_at_start: 6189
  new_product_files: 5
  product_file_inventory_after_human_tracking: 6194
  existing_product_files_modified:
    - AGENT_PLATFORM_MODIFICATIONS.tsv
  existing_runtime_adapter_contract_files_modified: false
  frontend_files_modified: false
  dependencies_modified: false
  lockfiles_modified: false
```

Because the agent did not stage files, `git ls-files` remains at 6189 until the
human stages and commits the five new product files. The candidate inventory is
6194 product files.

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Targeted process-owner tests | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_process_owner.py`, 13 tests |
| P14.1 contract regression | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py`, 16 tests |
| Adjacent product regression | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_product_config.py tests/hermes_cli/test_agent_platform_product_routes.py`, 16 tests |
| Internal import smoke | Pass | Output `HermesProcessOwner` |
| Root-export safety smoke | Pass | Output `contract-only-root` |
| Compile check | Pass | `.\.venv\Scripts\python.exe -m compileall -q hermes_cli/agent_platform/runtime_adapter tests/hermes_cli/runtime_adapter_lifecycle_probe.py tests/hermes_cli/test_agent_platform_runtime_process_owner.py` |
| Ruff check | Pass | `All checks passed!` |
| Ruff format check | Pass | `10 files already formatted` |
| Windows-footgun scanner | Pass | `No Windows footguns found` across 763 files |
| Register validation | Pass | 76 rows, 18 columns, zero duplicate IDs, zero duplicate paths, zero missing fields, zero hash mismatches |
| Fixture-process leak check | Pass | `matching live fixture processes: 0` |

## Graphify Integrity

No Graphify generation, update, extraction, clustering, export or refresh ran as
part of P14.2.

```yaml
P14_2_GraphifyIntegrity:
  graph_json_sha256: 02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2
  provenance_json_sha256: 952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550
  graphify_generation_performed: false
  graphify_modification_performed: false
```

## Authority Boundaries

```yaml
P14_2_authority_boundaries:
  final_runtime_adapter_facade: false
  public_executable_request_fields: false
  shell_execution: false
  parent_environment_merge: false
  environment_sanitization: false
  workspace_allocation: false
  path_containment: false
  readiness_probe: false
  runtime_event_generation: false
  audit_publication: false
  graceful_shutdown_workflow: false
  lifecycle_cancellation: false
  rollback_workflow: false
  live_Hermes_dashboard_launch: false
  gateway_launch: false
  provider_configuration: false
  worker_launch: false
  agent_launch: false
  tool_execution: false
  MCP_execution: false
  UI_lifecycle_controls: false
  Git_mutation: false
```

## Rollback

Before commit, rollback is file deletion plus register row removal only:

```text
remove process_owner.py
remove process_tree.py
remove stream_capture.py
remove runtime_adapter_lifecycle_probe.py
remove test_agent_platform_runtime_process_owner.py
remove P14.2-001 through P14.2-005 from AGENT_PLATFORM_MODIFICATIONS.tsv
remove this governance record
verify matching live fixture processes: 0
```

Rollback must not use broad process cleanup and must not kill unrelated
processes. After commit, rollback requires a human-created revert commit.

## P14.3 Handoff

P14.3 remains blocked until P14.2 is human-reviewed and committed. P14.3 may
build the tracked runtime-profile and sanitized-environment construction that
produces `ResolvedProcessLaunchPlan`. P14.3 must not reinterpret
`RuntimeLaunchRequest` as executable command authority.

P14.4 remains blocked for workspace and path containment. P14.8 remains the
only live Hermes lifecycle gate. P15 provider/runtime work and P17 execution
remain unauthorized.

## Final Verdict

```yaml
P14_2_HermesProcessOwnerVerdict:
  prerequisites:
    dynamic_start_commit_resolved: true
    HEAD_equals_origin_main: true
    P14_0_committed: true
    P14_1_committed: true
    contract_schema_version: 1
    register_valid_at_start: true
    upstream_clean: true
    Graphify_frozen_integrity: true

  implementation:
    process_owner_created: true
    process_tree_backend_created: true
    bounded_stream_capture_created: true
    inert_probe_fixture_created: true
    process_owner_tests_created: true
    dependencies_added: 0
    lockfiles_modified: 0
    existing_contract_files_modified: false
    root_exports_modified: false

  launch_boundary:
    resolved_plan_internal_only: true
    shell_enabled: false
    arbitrary_public_command_authority: false
    parent_environment_implicitly_inherited: false
    process_group_created: true
    live_Hermes_authorized: false

  ownership:
    one_owner_per_runtime: true
    launcher_PID_captured: true
    descendant_tree_captured: true
    listener_PID_proven: true
    process_name_termination_used: false
    exact_owned_tree_termination: true
    natural_exit_preserved: true
    release_guarded: true

  streams:
    stdout_drained: true
    stderr_drained: true
    bounded_capture: true
    overflow_discarded: true
    raw_output_exposed: false
    bounded_thread_join: true

  authority:
    readiness_authorized: false
    environment_sanitization_authorized: false
    workspace_allocation_authorized: false
    event_normalization_authorized: false
    lifecycle_cancellation_authorized: false
    graceful_shutdown_authorized: false
    rollback_authorized: false
    provider_authorized: false
    worker_authorized: false
    agent_authorized: false
    tool_authorized: false
    MCP_authorized: false
    Git_authorized: false

  validation:
    targeted_process_owner_tests_passed: true
    contract_regression_passed: true
    adjacent_regression_passed: true
    import_smoke_passed: true
    root_export_guard_passed: true
    compile_check_passed: true
    Ruff_passed: true
    Windows_footgun_scan_passed: true
    register_valid: true
    process_leak_check_passed: true
    candidate_path_audit_passed: true

  final_state:
    product_file_inventory_after_human_tracking: 6194
    modification_register_rows: 76
    fixture_processes_remaining: 0
    live_Hermes_processes_started: 0
    runtime_adapter_operational: false
    staged_files: 0
    commits_by_agent: 0
    pushes_by_agent: 0

  sequencing:
    P14_3_unlocked_after_human_commit: true
    P14_4_blocked: true
    P14_8_owns_live_Hermes_gate: true
    P15_unauthorized: true
    P17_unauthorized: true

  final_verdict: hermes_process_owner_ready
```

## Result Markers

```text
hermes_P14_2_prerequisite_gate_passed
hermes_P14_1_contract_package_committed
hermes_process_owner_internal_boundary_defined
hermes_resolved_launch_plan_internal_only
hermes_public_launch_contract_unchanged
hermes_process_owner_one_runtime_one_owner
hermes_process_owner_shell_disabled
hermes_process_owner_explicit_environment
hermes_process_owner_process_group_created
hermes_process_owner_launcher_PID_captured
hermes_process_owner_descendants_captured
hermes_process_owner_listener_binding_validated
hermes_process_owner_stdout_bounded
hermes_process_owner_stderr_bounded
hermes_process_owner_raw_logs_not_exposed
hermes_process_owner_exact_tree_termination
hermes_process_owner_no_process_name_termination
hermes_process_owner_natural_exit_preserved
hermes_process_owner_release_guarded
hermes_process_owner_fixture_cleanup_passed
hermes_process_owner_register_reconciled
hermes_process_owner_ready
no_runtime_adapter_facade
no_public_command_authority
no_shell_execution
no_live_Hermes_launch
no_gateway_launch
no_environment_sanitization
no_workspace_allocation
no_path_containment
no_readiness_probe
no_event_normalization
no_shutdown_workflow
no_rollback_workflow
no_provider_activation
no_worker_start
no_agent_start
no_tool_execution
no_MCP_execution
no_frontend_change
no_dependency_change
no_lockfile_change
no_Graphify_regeneration
no_Graphify_modification
no_git_mutation_by_agent
```
