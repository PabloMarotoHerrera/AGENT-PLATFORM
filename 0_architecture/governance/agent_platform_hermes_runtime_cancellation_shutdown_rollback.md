# P14.6 - Runtime Cancellation, Shutdown And Rollback

## Document Header

| Field | Value |
| --- | --- |
| Project | P14 - Governed Runtime Adapter |
| Ticket | P14.6 - Runtime Cancellation, Shutdown and Workspace Rollback |
| Date | 2026-07-19 |
| Status | `hermes_runtime_shutdown_rollback_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_runtime_cancellation_shutdown_rollback.md` |
| Dynamic start commit | `a69991d3074150b8bbe5b692ae1437142d3b29a5` |
| Origin main at start | `a69991d3074150b8bbe5b692ae1437142d3b29a5` |
| Prerequisite runtime event and audit normalization | `hermes_runtime_events_audit_normalization_ready` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

P14.6 adds the internal governed boundary for runtime cancellation, graceful
shutdown, forced shutdown fallback and explicit workspace rollback over the
P14.1 runtime contracts and P14.2 to P14.5 internal evidence boundaries.

P14.6 does not make the runtime adapter operational. It does not implement the
final facade, process launch composition, executable resolution, argv
resolution, parent environment acquisition, listener discovery, readiness
probing, HTTP response mapping, audit persistence, audit publication, general
workspace cleanup, provider credentials, inference, workers, agents, tools,
MCP, UI controls, Graphify regeneration or Git authority.

The binding implementation verdict is:

```text
hermes_runtime_shutdown_rollback_ready
```

## Prerequisite Gate

```yaml
P14_6_PrerequisiteGate:
  branch: main
  dynamic_start_commit: a69991d3074150b8bbe5b692ae1437142d3b29a5
  origin_main: a69991d3074150b8bbe5b692ae1437142d3b29a5
  HEAD_equals_origin_main_at_start: true
  git_index_empty_at_start: true
  tracked_working_tree_clean_at_start: true
  allowed_untracked_paths:
    - .opencode/
    - AGENTS.md
    - graphify-out/
  P14_0_committed: true
  P14_1_committed: true
  P14_2_committed: true
  P14_3_committed: true
  P14_4_committed: true
  P14_5_committed: true
  runtime_adapter_contract_schema_version: 1
  runtime_adapter_contract_package_present: true
  process_owner_present: true
  runtime_profile_registry_present: true
  environment_sanitizer_present: true
  workspace_allocator_present: true
  path_containment_present: true
  event_normalizer_present: true
  audit_normalizer_present: true
  shutdown_coordinator_absent_at_start: true
  rollback_coordinator_absent_at_start: true
  product_tracked_files_at_start: 6206
  modification_register_rows_at_start: 88
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  graphify_frozen_integrity_at_start: true
```

The prerequisite gate passed. P14.6 proceeded only because P14.5 was already
committed on `main` and `HEAD == origin/main` at
`a69991d3074150b8bbe5b692ae1437142d3b29a5`.

## Source Navigation Evidence

P14.6 honored the stricter frozen-Graphify instruction. No Graphify CLI,
update, extraction, clustering, export or refresh process ran.

Follow-up inspection was limited to:

- P14.1 runtime request, handle, operation-result, event, failure and state
  contracts.
- P14.1 lifecycle actions, terminal states, process status, workspace status,
  cleanup status and rollback outcome vocabulary.
- P14.2 process-owner snapshots, guarded release semantics, tree termination
  and bounded process-owner errors.
- P14.3 profile retention posture and environment path projection.
- P14.4 workspace allocation, ownership marker, containment primitives and
  allocator registry behavior.
- P14.5 runtime-event journal, failure-code normalization and audit projection.
- Existing P14 test and governance-record patterns.

## Files Added

P14.6 adds exactly four product files:

```text
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/lifecycle_control.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/rollback.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_lifecycle_control.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_rollback.py
```

P14.6 modifies exactly five existing product files:

```text
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/event_normalization.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/process_owner.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/workspace.py
2_products/hermes-agent/tests/hermes_cli/runtime_adapter_lifecycle_probe.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_event_normalization.py
```

P14.6 modifies one existing product governance file:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

P14.6 creates this non-product governance record:

```text
0_architecture/governance/agent_platform_hermes_runtime_cancellation_shutdown_rollback.md
```

No P14.1 contract file, enum file, state-machine file, root export, product
configuration, backend route, frontend file, package manifest, dependency
lockfile, immutable upstream file or Graphify file was modified.

## Termination Coordinator

`lifecycle_control.py` defines the internal `RuntimeTerminationCoordinator`.
It coordinates cancellation and shutdown only for existing runtime handles and
already-owned process records.

The coordinator enforces:

- request `runtime_id` and `correlation_id` identity checks before any state
  transition;
- per-runtime nonblocking locks so concurrent cancellation, shutdown or release
  paths fail closed;
- immutable runtime-handle snapshots through `with_runtime_state`;
- transition validation through the existing P14.1 state machine;
- event emission through the P14.5 `RuntimeEventJournal`;
- failure projection through the P14.5 `normalize_runtime_failure` boundary.

Cancellation behavior is state scoped:

```yaml
created_or_validating:
  emits: cancellation_requested
  final_state: cancelled
  process_owner_required: false
active_runtime:
  emits: cancellation_requested
  then: governed_stop_path
  final_state: cancelled
terminal_runtime:
  idempotent_result: true
```

Shutdown behavior is also state scoped:

```yaml
active_runtime:
  emits:
    - graceful_shutdown_started
    - forced_termination_started_if_needed
    - process_exited
    - listener_released_if_bound
  final_state: stopped_or_cancelled
terminal_runtime:
  idempotent_result: true
```

The coordinator does not accept caller-supplied PIDs, signals, executable
paths, commands, arguments, environment values, workspace paths or listener
ports. It starts no process and creates no workspace.

## Graceful And Forced Stop

`process_owner.py` now exposes a bounded internal graceful-stop primitive:

```text
HermesProcessOwner.request_graceful_stop(runtime_id, timeout_ms=...)
```

It returns `OwnedProcessGracefulStopResult` with only bounded evidence:

```yaml
fields:
  - runtime_id
  - mechanism
  - supported
  - exit_observed
  - timed_out
  - snapshot
mechanisms:
  - already_exited
  - windows_ctrl_break
  - posix_sigterm
  - unsupported
```

Windows graceful stop uses the already-created process group with
`CTRL_BREAK_EVENT` when available. POSIX graceful stop uses the already-created
process session with `SIGTERM` to the process group. Unsupported platforms or
unsupported mechanisms return a bounded unsupported result instead of exposing
signal authority to callers.

If graceful stop does not produce a bounded observed exit, P14.6 falls back to
the existing P14.2 exact owned-tree termination path:

```text
HermesProcessOwner.terminate_owned_tree(runtime_id, timeout_ms=...)
```

Release is attempted only after process exit evidence. Release failures become
`runtime_process_release_error` failures and never silently discard owner state.

## Workspace Rollback Coordinator

`rollback.py` defines the internal `RuntimeWorkspaceRollbackCoordinator`. It
rolls back only one already-stopped, allocator-owned runtime workspace.

Rollback preconditions are:

```yaml
identity_checks:
  request_matches_runtime_handle: true
  profile_matches_runtime_handle: true
  allocation_matches_runtime_handle: true
  profile_policy_matches_allocation_policy: true
state_checks:
  begin_rollback_transition_allowed: true
  process_owner_no_longer_registered: true
  profile_retention_policy: remove_on_terminal
allocator_checks:
  allocator_owns_runtime_id: true
  allocator_workspace_id_matches_allocation: true
```

Ownership-marker validation is exact and bounded:

```yaml
marker_name: .agent-platform-runtime-workspace.json
max_marker_bytes: 4096
required_json_fields:
  - schema_version
  - runtime_id
  - workspace_id
  - workspace_policy_id
redirect_or_symlink_allowed: false
non_regular_file_allowed: false
```

Workspace tree preflight is bounded and contained:

```yaml
max_tree_entries: 10000
max_tree_depth: 64
allowed_entry_types:
  - regular_file
  - directory
redirect_or_symlink_allowed: false
nested_mount_allowed: false
path_chain_revalidated: true
```

Deletion is deterministic and narrow:

```yaml
deletion_order:
  - non_marker_regular_files_deepest_first
  - ownership_marker
  - child_directories_deepest_first
  - workspace_root
uses_shutil_rmtree: false
uses_shell_deletion: false
revalidates_each_entry_before_deletion: true
sibling_preservation_required: true
```

After verified deletion, `RuntimeWorkspaceAllocator.release_after_cleanup`
removes only the allocator registry entry for the matching runtime and
workspace ID. It refuses release if the workspace root or ownership marker
still exists.

## Failure Normalization

`event_normalization.py` now reconciles P14.6 lifecycle and rollback failures
with the existing P14.5 internal failure-normalization boundary.

P14.6 adds stable failure-code mappings for:

```text
runtime_lifecycle_control_error
runtime_lifecycle_request_identity_error
runtime_lifecycle_operation_conflict
runtime_lifecycle_ownership_error
runtime_graceful_shutdown_error
runtime_forced_shutdown_error
runtime_process_release_error
runtime_rollback_error
runtime_rollback_identity_error
runtime_rollback_state_error
runtime_rollback_process_still_owned
runtime_rollback_marker_error
runtime_rollback_tree_limit_error
runtime_rollback_entry_type_error
runtime_rollback_containment_error
runtime_rollback_deletion_error
runtime_rollback_allocator_release_error
```

Event descriptor coverage remains tied to the existing P14.1 event vocabulary.
P14.6 does not add a new public event enum, failure enum or state-machine enum.

## Public Export Boundary

P14.6 does not modify `hermes_cli/agent_platform/runtime_adapter/__init__.py`.
The root `runtime_adapter` package remains contract-only. Lifecycle and
rollback coordinators are importable only from their internal submodules.

## Hash Register

```yaml
P14_6_FileHashes:
  hermes_cli/agent_platform/runtime_adapter/lifecycle_control.py: a7cf4a1b991f84d72ad95dad0f32d44cb14243236632d984e5f43be048ebb971
  hermes_cli/agent_platform/runtime_adapter/rollback.py: 7c913366dc885ddb8e909ceedc37d7fde45ca2db37ded1ffbf2471cc401ead53
  tests/hermes_cli/test_agent_platform_runtime_lifecycle_control.py: ef26f883eca65254364441a4cbca5f15715064bbaa72f6c6bbb5685a147027b3
  tests/hermes_cli/test_agent_platform_runtime_rollback.py: 2d40536e4e01c37893ac90915d61d4746f8da6db47b5995fd49c987a59fc4c47
  hermes_cli/agent_platform/runtime_adapter/process_owner.py: aeee84accc4911136d4236e8ebef71e91ffdc73fe2989b164e1a4cbe8ccf7024
  tests/hermes_cli/runtime_adapter_lifecycle_probe.py: fe32b2ab8dc47a6c95326dafd564dcfcd0767efe2c0ba5c3ae83a52d6d27bb90
  hermes_cli/agent_platform/runtime_adapter/workspace.py: 6936b449aba76fcebf3030218b8eb2e14c0fe0b48468492a4c0ac5f997a70b9b
  hermes_cli/agent_platform/runtime_adapter/event_normalization.py: 75c291fae3f543ed441d2f2f9f4f575fabcb8fa2c7ad716215ed528ca8afa0f3
  tests/hermes_cli/test_agent_platform_runtime_event_normalization.py: d968c2b12805accb9c44fff2245cb38b012f849a4140c62e5a7faa956a057762
```

`AGENT_PLATFORM_MODIFICATIONS.tsv` was updated with exactly four P14.6 rows:

```text
P14.6-001
P14.6-002
P14.6-003
P14.6-004
```

P14.6 also reconciles cumulative hashes and evidence text for these prior
registered rows because their files were intentionally extended by P14.6:

```text
P14.2-001
P14.2-004
P14.4-002
P14.5-001
P14.5-003
```

## Validation Evidence

The following P14.6 validation passed from `2_products/hermes-agent`:

```text
P14.6 targeted tests: 23 passed, 2 skipped
P14.5 regression tests: 11 passed
P14.4 regression tests: 45 passed, 3 skipped
P14.3 regression tests: 17 passed
P14.2 regression tests: 13 passed
P14.1 regression tests: 16 passed
Adjacent product regression tests: 16 passed
Import smoke: RuntimeTerminationCoordinator
Import smoke: RuntimeWorkspaceRollbackCoordinator
Root-export guard: contract-only-root
Compileall: passed
Ruff check: All checks passed
Ruff format check: 19 files already formatted
Windows footgun scanner: No Windows footguns found (771 files scanned)
```

Validation covered:

- request identity and correlation checks;
- cancellation before process ownership;
- active-runtime cancellation and shutdown;
- graceful stop and forced fallback paths;
- listener release event behavior;
- terminal idempotency;
- process-owner release failure normalization;
- per-runtime lifecycle locking;
- rollback identity and state preconditions;
- process-ownership rollback blocking;
- marker validation failures;
- redirect, symlink, mount and tree-limit rejection;
- exact contained cleanup and sibling preservation;
- allocator release after verified cleanup;
- rollback deletion failure normalization;
- P14.6 failure-code reconciliation;
- audit projection compatibility;
- source safety and root-export preservation.

Final reconciliation checks passed from the repository root:

```yaml
P14_6_FinalReconciliation:
  modification_register:
    status: passed
    rows: 92
    columns: 18
    duplicate_ids: 0
    duplicate_paths: 0
    missing_fields: 0
    hash_mismatches: 0
    register_sha256: 0521cf6bfa53a65319f7d5512679d827683970a64df5f5532f15f40f3f01bfad
    normalized_rows_sha256: 43c1948fad3c2116b468aad6d4df521dd324896ee66cb44b7a9cc1a56747ce86
  product_inventory_files: 6210
  process_leak_check: passed
  repository_runtime_artifacts_created: false
  runtime_workspace_markers_in_repository: 0
  runtime_workspace_artifact_paths_in_repository: 0
  candidate_artifact_path_audit: passed
  git_diff_check: passed_with_line_ending_warnings_only
  graphify_out_graph_json_sha256: 02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2
  graphify_out_provenance_json_sha256: 952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550
  graphify_frozen_integrity_final: true
```

## Authority Decision

```yaml
P14_6_Authority:
  runtime_adapter_operational: false
  final_facade_authorized: false
  process_launch_composition_authorized: false
  executable_resolution_authorized: false
  argv_resolution_authorized: false
  parent_environment_read_authorized: false
  listener_discovery_authorized: false
  readiness_probe_authorized: false
  cancellation_coordination_authorized: true
  graceful_shutdown_authorized: internal_owned_process_only
  forced_shutdown_fallback_authorized: internal_owned_process_only
  workspace_rollback_authorized: verified_owned_workspace_only
  general_workspace_cleanup_authorized: false
  arbitrary_path_deletion_authorized: false
  audit_persistence_authorized: false
  audit_publication_authorized: false
  provider_authorized: false
  worker_authorized: false
  agent_authorized: false
  tool_authorized: false
  MCP_authorized: false
  UI_authorized: false
  Graphify_process_authorized: false
  Git_mutation_authorized: false
```

## Decision Matrix

```yaml
P14_6_DecisionMatrix:
  prerequisites:
    dynamic_start_commit_resolved: true
    HEAD_equals_origin_main: true
    P14_0_committed: true
    P14_1_committed: true
    P14_2_committed: true
    P14_3_committed: true
    P14_4_committed: true
    P14_5_committed: true
    contract_schema_version: 1
    register_valid_at_start: true
    upstream_clean: true
    Graphify_frozen_integrity: true

  implementation:
    lifecycle_control_created: true
    rollback_coordinator_created: true
    process_owner_graceful_stop_added: true
    workspace_release_after_cleanup_added: true
    P14_6_failure_codes_mapped: true
    lifecycle_tests_created: true
    rollback_tests_created: true
    dependencies_added: 0
    lockfiles_modified: 0
    runtime_adapter_contract_files_modified: false
    enum_files_modified: false
    state_machine_modified: false
    root_exports_modified: false

  cancellation_shutdown:
    request_identity_guarded: true
    per_runtime_locking: true
    pre_process_cancellation_supported: true
    graceful_stop_bounded: true
    forced_fallback_bounded: true
    process_owner_release_guarded: true
    listener_release_event_guarded: true
    caller_signal_authority: false
    caller_pid_authority: false

  rollback:
    request_identity_guarded: true
    process_ownership_must_be_released: true
    allocator_ownership_required: true
    marker_identity_required: true
    tree_entry_limit: 10000
    tree_depth_limit: 64
    symlink_or_reparse_allowed: false
    nested_mount_allowed: false
    arbitrary_path_authority: false
    shell_deletion: false
    recursive_shutil_deletion: false

  validation:
    targeted_lifecycle_tests_passed: true
    targeted_rollback_tests_passed: true
    P14_5_regression_passed: true
    P14_4_regression_passed: true
    P14_3_regression_passed: true
    P14_2_regression_passed: true
    P14_1_regression_passed: true
    adjacent_product_regression_passed: true
    import_smoke_passed: true
    root_export_guard_passed: true
    compile_check_passed: true
    Ruff_passed: true
    Windows_footgun_scan_passed: true
    register_valid: true
    process_leak_check_passed: true
    repository_artifact_check_passed: true
    candidate_path_audit_passed: true

  final_state:
    product_inventory_files: 6210
    new_product_files: 4
    modified_existing_product_files: 5
    modification_register_rows: 92
    runtime_adapter_operational: false
    repository_runtime_artifacts_created: false
    live_Hermes_started: false
    providers_enabled: false
    workers_started: false
    agents_started: false
    staged_files: 0
    commits_by_agent: 0
    pushes_by_agent: 0

  sequencing:
    P14_7_unlocked_after_human_commit: true
    P14_8_owns_live_Hermes_gate: true
    P15_unauthorized: true
    P17_unauthorized: true

  final_verdict: hermes_runtime_shutdown_rollback_ready
```

## Result Markers

```text
hermes_P14_6_prerequisite_gate_passed
hermes_P14_5_events_audit_normalization_committed
hermes_runtime_termination_coordinator_created
hermes_runtime_cancellation_identity_guarded
hermes_runtime_pre_process_cancellation_supported
hermes_runtime_graceful_shutdown_started_evented
hermes_runtime_forced_shutdown_fallback_guarded
hermes_runtime_process_owner_release_guarded
hermes_runtime_listener_release_event_guarded
hermes_runtime_process_owner_graceful_stop_created
hermes_runtime_workspace_rollback_coordinator_created
hermes_runtime_workspace_rollback_marker_verified
hermes_runtime_workspace_rollback_tree_bounded
hermes_runtime_workspace_rollback_contained_deletion
hermes_runtime_workspace_allocator_release_after_cleanup_created
hermes_runtime_shutdown_rollback_failure_codes_mapped
hermes_runtime_shutdown_rollback_register_reconciled
hermes_runtime_shutdown_rollback_ready
no_runtime_adapter_operation
no_process_launch_composition
no_parent_environment_read
no_listener_discovery
no_readiness_probe
no_general_workspace_cleanup
no_arbitrary_path_deletion
no_audit_persistence
no_audit_publication
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
