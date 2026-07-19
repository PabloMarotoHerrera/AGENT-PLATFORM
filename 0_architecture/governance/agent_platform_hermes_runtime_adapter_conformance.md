# P14.7 - Runtime Adapter Conformance Tests

## Document Header

| Field | Value |
| --- | --- |
| Project | P14 - Governed Runtime Adapter |
| Ticket | P14.7 - Adapter Conformance Tests |
| Date | 2026-07-19 |
| Status | `hermes_runtime_adapter_conformance_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_runtime_adapter_conformance.md` |
| Dynamic start commit | `d51608a47229bc6e95a29956e9df5cd3d7a8e155` |
| Origin main at start | `d51608a47229bc6e95a29956e9df5cd3d7a8e155` |
| Prerequisite runtime shutdown and rollback | `hermes_runtime_shutdown_rollback_ready` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

P14.7 adds adapter conformance coverage over the committed P14.1 to P14.6
runtime-adapter internals. The coverage is test-only and uses the repository
owned inert lifecycle probe plus synthetic contracts, temporary workspaces,
synthetic environments and deterministic failure inputs.

P14.7 does not make the runtime adapter operational. It does not implement the
final facade, process launch composition for live Hermes, executable discovery,
argv discovery, parent environment acquisition, dashboard launch, gateway
launch, readiness probing, provider credentials, inference, workers, agents,
tools, MCP, UI controls, audit persistence, audit publication, Graphify
regeneration or Git authority.

The binding implementation verdict is:

```text
hermes_runtime_adapter_conformance_ready
```

## Prerequisite Gate

```yaml
P14_7_PrerequisiteGate:
  branch: main
  dynamic_start_commit: d51608a47229bc6e95a29956e9df5cd3d7a8e155
  origin_main: d51608a47229bc6e95a29956e9df5cd3d7a8e155
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
  P14_6_committed: true
  runtime_adapter_contract_schema_version: 1
  runtime_adapter_contract_package_present: true
  process_owner_present: true
  runtime_profile_registry_present: true
  environment_sanitizer_present: true
  workspace_allocator_present: true
  path_containment_present: true
  event_normalizer_present: true
  audit_normalizer_present: true
  shutdown_coordinator_present: true
  rollback_coordinator_present: true
  conformance_harness_absent_at_start: true
  final_adapter_facade_absent_at_start: true
  product_tracked_files_at_start: 6210
  modification_register_rows_at_start: 92
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  graphify_frozen_integrity_at_start: true
```

The prerequisite gate passed. P14.7 proceeded only because P14.6 was already
committed on `main` and `HEAD == origin/main` at
`d51608a47229bc6e95a29956e9df5cd3d7a8e155`.

## Source Navigation Evidence

P14.7 honored the frozen-Graphify instruction. No Graphify CLI, update,
extraction, clustering, export or refresh process ran.

Follow-up inspection was limited to:

- P14.1 runtime request, handle, result, event, failure and lifecycle state contracts.
- P14.2 process-owner launch, stream drain, tree ownership and release behavior.
- P14.3 profile registry and sanitized environment behavior.
- P14.4 workspace allocation, marker, managed-files and path containment behavior.
- P14.5 runtime-event journal, failure normalization and audit projection behavior.
- P14.6 cancellation, shutdown, listener release and workspace rollback behavior.
- Existing P14 test and governance-record patterns.

## Files Added

P14.7 adds exactly three product test files:

```text
2_products/hermes-agent/tests/hermes_cli/runtime_adapter_conformance_harness.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_adapter_conformance.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_adapter_failure_conformance.py
```

P14.7 modifies exactly one existing product test fixture:

```text
2_products/hermes-agent/tests/hermes_cli/runtime_adapter_lifecycle_probe.py
```

P14.7 modifies one existing product governance file:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

P14.7 creates this non-product governance record:

```text
0_architecture/governance/agent_platform_hermes_runtime_adapter_conformance.md
```

No production runtime-adapter file, P14.1 contract file, enum file,
state-machine file, root export, product configuration, backend route,
frontend file, package manifest, dependency lockfile, immutable upstream file
or Graphify file was modified.

## Conformance Harness

`runtime_adapter_conformance_harness.py` defines a test-only immutable harness
with the fixed P14.7 24-case registry. It composes committed internals under
controlled test conditions and returns in-memory summaries only.

The harness defines:

```text
RuntimeAdapterConformanceHarness
RuntimeAdapterConformanceCase
RuntimeAdapterConformanceOutcome
RuntimeAdapterConformanceResult
RuntimeAdapterConformanceSummary
EXPECTED_CASE_IDS
ConformanceExecutionDenied.error_code = conformance.profile.execution_scope_denied
```

The harness uses only:

```yaml
P14_7_HarnessInputs:
  executable: sys.executable
  process_target: tests/hermes_cli/runtime_adapter_lifecycle_probe.py
  workspaces: pytest_or_tempfile_temporary_paths
  source_environment: synthetic_mapping_only
  runtime_profiles:
    allowed: runtime.profile.test.lifecycle_probe.v1
    denied: runtime.profile.hermes_dashboard.experimental.v1
  audit_storage: in_memory_projection_only
  event_storage: in_memory_journal_only
```

The harness intentionally includes a small `_GracefulTimeoutProcessOwner`
test seam for `SHUTDOWN-002`. The seam returns a bounded timed-out graceful
stop result and delegates actual ownership, exact process-tree termination,
release and snapshot behavior to the real `HermesProcessOwner`. This avoids
Windows `CTRL_BREAK_EVENT` timing ambiguity while still exercising the governed
forced-termination fallback with the inert probe process tree.

The harness does not expose a production facade and is not exported from
`hermes_cli.agent_platform.runtime_adapter`.

## Lifecycle Probe Extension

`runtime_adapter_lifecycle_probe.py` remains an inert subprocess fixture. P14.7
adds child-side verification modes:

```text
--verify-managed-environment
--verify-provider-null
--expected-workspace-root
--expect-no-path
```

The new probe checks return bounded exit codes only:

```yaml
P14_7_ProbeExitCodes:
  21: managed_environment_variable_missing
  22: provider_variable_present
  23: home_resolution_mismatch
  24: managed_environment_path_outside_workspace
  25: working_directory_mismatch
  26: PATH_present_when_forbidden
  27: windows_home_drive_or_path_mismatch
  28: expected_workspace_root_missing
```

The probe does not print paths, environment values, exception messages or
secrets. It still performs no provider call, worker launch, agent launch, tool
execution, MCP execution, network access, repository write, Graphify action or
Git action.

## Conformance Matrix

```yaml
P14_7_ConformanceMatrix:
  CONTRACT-001:
    title: contract_authority_preserved
    coverage: launch, stop, cancel and rollback requests expose no executable, argv, environment, cwd, signal, pid or path authority.
  CONTRACT-002:
    title: immutable_contract_round_trip
    coverage: request, handle, process, workspace, event, failure and operation result models round-trip and remain frozen.
  PROFILE-001:
    title: test_profile_resolved
    coverage: inert lifecycle-probe profile resolves to current product Python, lifecycle-probe arguments and no managed files root.
  PROFILE-002:
    title: dashboard_execution_denied
    coverage: dashboard profile remains P14.8-only and conformance execution fails closed with conformance.profile.execution_scope_denied.
  ENVIRONMENT-001:
    title: synthetic_environment_isolated
    coverage: sanitized environment excludes PATH and prohibited provider or host variables while binding managed home paths.
  ENVIRONMENT-002:
    title: child_home_isolated
    coverage: child process observes managed HOME, USERPROFILE, temp and working-directory paths inside the allocated workspace.
  ENVIRONMENT-003:
    title: provider_null_child
    coverage: child process observes no provider variables and no PATH when that profile output forbids PATH.
  WORKSPACE-001:
    title: test_workspace_allocated
    coverage: test workspace allocation creates exact workspace id, marker, workdir, temp and no managed files root.
  WORKSPACE-002:
    title: dashboard_workspace_files_root_locked
    coverage: dashboard workspace profile requires managed files root and rejects invalid or unsafe managed files paths.
  PATH-001:
    title: path_escape_matrix_without_symlink
    coverage: containment rejects traversal, invalid segments, outside roots and unsafe path chains while accepting contained paths.
  PROCESS-001:
    title: natural_process_lifecycle
    coverage: inert process starts, exits naturally, drains streams and releases ownership.
  PROCESS-002:
    title: exact_tree_ownership
    coverage: descendant ownership, listener binding and exact process-tree termination preserve ownership boundaries.
  STREAM-001:
    title: bounded_streams
    coverage: stdout and stderr accounting records total, bounded, discarded and truncation behavior without unbounded capture.
  CANCELLATION-001:
    title: pre_process_cancellation
    coverage: created and validating runtimes cancel before any process ownership exists.
  CANCELLATION-002:
    title: active_cancellation
    coverage: active runtime cancellation stops the owned inert process, emits cancellation and process-exit events, and releases ownership.
  SHUTDOWN-001:
    title: graceful_shutdown
    coverage: graceful shutdown stops the owned inert process and emits listener release without forced fallback.
  SHUTDOWN-002:
    title: forced_fallback
    coverage: timed-out graceful stop falls back to exact owned-tree termination and leaves no descendant PIDs.
  ROLLBACK-001:
    title: successful_rollback
    coverage: stopped runtime rolls back only the owned workspace and preserves sibling directories.
  ROLLBACK-002:
    title: marker_failure_closed
    coverage: marker defects fail closed without deleting the workspace or sibling data.
  EVENT-001:
    title: cross_component_event_sequence
    coverage: request, profile, workspace, environment, process, shutdown and rollback events remain normalized and ordered.
  AUDIT-001:
    title: in_memory_audit_projection
    coverage: audit projection is sanitized and in-memory only, with no persistence, raw paths, environment values or exception text.
  FAILURE-001:
    title: failure_matrix
    coverage: unknown profile, duplicate ownership, listener rejection, path escape, workspace duplicate, environment path, invalid state and unsupported error failures normalize safely.
  CONCURRENCY-001:
    title: runtime_isolation
    coverage: concurrent runtimes keep ownership, workspaces and lifecycle locks isolated; operation conflicts fail closed.
  CLEANUP-001:
    title: zero_residue
    coverage: harness cleanup removes markers, drain threads and known inert-process PIDs.
```

Standalone harness summary passed all cases:

```yaml
P14_7_RunAllSummary:
  passed: 24
  skipped: 0
  failed: 0
  failed_case_ids: []
  skipped_reasons: {}
```

## Failure And Cleanup Coverage

`test_agent_platform_runtime_adapter_failure_conformance.py` verifies that
failure paths do not convert cleanup failures to success and do not delete
sibling workspaces or unrelated processes.

Failure conformance covers:

- workspace marker absence, malformed marker and marker identity mismatch;
- unknown profile rejection;
- dashboard execution-scope denial;
- duplicate process ownership;
- invalid listener PID binding;
- path escape and unsafe path-chain rejection;
- duplicate workspace allocation;
- invalid managed environment paths;
- invalid event or lifecycle state transitions;
- unsupported error normalization;
- exact cleanup after synthetic assertion failure.

The failure matrix intentionally verifies bounded evidence only. It does not
assert or persist raw exception messages, raw paths, environment values,
provider credentials or repository artifacts.

## Public Export Boundary

P14.7 does not modify `hermes_cli/agent_platform/runtime_adapter/__init__.py`.
The root `runtime_adapter` package remains contract-only. The conformance
harness is importable only from the test module path.

## Hash Register

```yaml
P14_7_FileHashes:
  tests/hermes_cli/runtime_adapter_lifecycle_probe.py: ef4dec9f47eb96fb99eac72b307f1311a03560b56dc9d1bf7f58bb886548dad3
  tests/hermes_cli/runtime_adapter_conformance_harness.py: cfb3ea7ec3a63d7836635f43de234c026fdd0cc90b0556a76b2ee8b136c4e7dc
  tests/hermes_cli/test_agent_platform_runtime_adapter_conformance.py: 9e21229877b048ba54b732bfb321dd0475a642e5ad3879cb402cbb1aec0b3ed4
  tests/hermes_cli/test_agent_platform_runtime_adapter_failure_conformance.py: d6d1b8d62f8b9ba7d54260b3cf9a606d20b34b91e5e0faee80d10b84ef7c723e
```

`AGENT_PLATFORM_MODIFICATIONS.tsv` was updated with exactly three P14.7 rows:

```text
P14.7-001
P14.7-002
P14.7-003
```

P14.7 also reconciles cumulative hash and evidence text for the prior
registered row `P14.2-004` because the inert lifecycle probe was intentionally
extended by P14.7.

## Validation Evidence

The following P14.7 validation passed from `2_products/hermes-agent`:

```text
Standalone conformance harness summary: 24 passed, 0 skipped, 0 failed
P14.7 targeted tests: 8 passed
Complete P14 runtime regression tests: 133 passed, 5 skipped
Adjacent product regression tests: 16 passed
Import smoke: RuntimeAdapterConformanceHarness
Root-export guard: contract-only-root
Compileall: passed
Ruff check: All checks passed
Ruff format check: 20 files already formatted
Windows footgun scanner: No Windows footguns found (771 files scanned)
```

Validation covered:

- fixed 24-case registry integrity;
- immutable runtime contract round trips;
- denied dashboard profile execution scope;
- synthetic provider-null environment behavior in parent and child processes;
- managed home, temp and working-directory isolation;
- workspace marker and managed-files-root policy behavior;
- path traversal and unsafe path-chain rejection;
- natural process lifecycle and exact process-tree ownership;
- bounded stdout and stderr stream accounting;
- pre-process and active-runtime cancellation;
- graceful shutdown and forced fallback over owned inert processes;
- successful rollback and marker-failure rollback denial;
- cross-component event ordering;
- in-memory sanitized audit projection;
- failure normalization across expected P14 failure surfaces;
- runtime isolation and operation-conflict failure closure;
- zero residue for markers, drain threads and known PIDs;
- source safety and root-export preservation.

Final reconciliation checks passed from the repository root:

```yaml
P14_7_FinalReconciliation:
  modification_register:
    status: passed
    rows: 95
    columns: 18
    duplicate_ids: 0
    duplicate_paths: 0
    missing_fields: 0
    hash_mismatches: 0
    register_sha256: f07fefe712e08d9c51ea74ff7199d3d7de45452f92ecceb1b7d6d18b2bfa8ddf
    normalized_rows_sha256: 16de96c9f12368b52bdc4d0f9c5ca9766d3c718d0763704b3d0b6be7227478bc
  product_inventory_files: 6213
  process_leak_check: passed
  repository_runtime_artifacts_created: false
  runtime_workspace_markers_in_repository: 0
  p147_artifact_paths_in_repository: 0
  sqlite_or_db_artifact_paths_in_repository: 0
  candidate_artifact_path_audit: passed
  git_diff_check: passed_with_line_ending_warnings_only
  graphify_out_graph_json_sha256: 02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2
  graphify_out_provenance_json_sha256: 952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550
  graphify_frozen_integrity_final: true
```

## Authority Decision

```yaml
P14_7_Authority:
  runtime_adapter_operational: false
  final_facade_authorized: false
  production_process_launch_authorized: false
  live_Hermes_dashboard_launch_authorized: false
  gateway_launch_authorized: false
  readiness_probe_authorized: false
  executable_resolution_authorized: false
  argv_resolution_authorized: false
  parent_environment_read_authorized: false
  conformance_harness_authorized: test_only
  inert_lifecycle_probe_authorized: test_only
  synthetic_environment_authorized: test_only
  temporary_workspace_authorized: test_only
  deterministic_failure_inputs_authorized: test_only
  graceful_timeout_test_seam_authorized: test_only
  cancellation_coordination_authorized: already_committed_internal_boundary
  graceful_shutdown_authorized: already_committed_internal_owned_process_only
  forced_shutdown_fallback_authorized: already_committed_internal_owned_process_only
  workspace_rollback_authorized: already_committed_verified_owned_workspace_only
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
P14_7_DecisionMatrix:
  prerequisites:
    dynamic_start_commit_resolved: true
    HEAD_equals_origin_main: true
    P14_0_committed: true
    P14_1_committed: true
    P14_2_committed: true
    P14_3_committed: true
    P14_4_committed: true
    P14_5_committed: true
    P14_6_committed: true
    contract_schema_version: 1
    register_valid_at_start: true
    upstream_clean: true
    Graphify_frozen_integrity: true

  implementation:
    conformance_harness_created: true
    primary_conformance_tests_created: true
    failure_conformance_tests_created: true
    lifecycle_probe_child_environment_checks_added: true
    fixed_case_registry_count: 24
    dependencies_added: 0
    lockfiles_modified: 0
    production_runtime_adapter_files_modified: 0
    runtime_adapter_contract_files_modified: false
    enum_files_modified: false
    state_machine_modified: false
    root_exports_modified: false

  conformance:
    contracts_covered: true
    profiles_covered: true
    environments_covered: true
    workspaces_covered: true
    paths_covered: true
    processes_covered: true
    streams_covered: true
    cancellation_covered: true
    shutdown_covered: true
    rollback_covered: true
    events_covered: true
    audit_projection_covered: true
    deterministic_failures_covered: true
    concurrency_covered: true
    cleanup_covered: true
    readiness_probe_started: false
    live_Hermes_started: false

  validation:
    standalone_24_case_harness_passed: true
    targeted_conformance_tests_passed: true
    P14_runtime_regression_passed: true
    adjacent_product_regression_passed: true
    import_smoke_passed: true
    root_export_guard_passed: true
    compile_check_passed: true
    Ruff_passed: true
    Ruff_format_check_passed: true
    Windows_footgun_scan_passed: true
    register_valid: true
    process_leak_check_passed: true
    repository_artifact_check_passed: true
    candidate_path_audit_passed: true

  final_state:
    product_inventory_files: 6213
    new_product_files: 3
    modified_existing_product_files: 1
    modification_register_rows: 95
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
    P14_8_unlocked_after_human_commit: true
    P14_R_closure_pending: true
    P15_unauthorized: true
    P17_unauthorized: true

  final_verdict: hermes_runtime_adapter_conformance_ready
```

## Result Markers

```text
hermes_P14_7_prerequisite_gate_passed
hermes_P14_6_shutdown_rollback_committed
hermes_runtime_adapter_conformance_harness_created
hermes_runtime_adapter_conformance_registry_fixed_24_cases
hermes_runtime_adapter_conformance_contracts_covered
hermes_runtime_adapter_conformance_profiles_covered
hermes_runtime_adapter_conformance_environments_covered
hermes_runtime_adapter_conformance_workspaces_covered
hermes_runtime_adapter_conformance_paths_covered
hermes_runtime_adapter_conformance_processes_covered
hermes_runtime_adapter_conformance_streams_covered
hermes_runtime_adapter_conformance_cancellation_covered
hermes_runtime_adapter_conformance_shutdown_covered
hermes_runtime_adapter_conformance_rollback_covered
hermes_runtime_adapter_conformance_events_covered
hermes_runtime_adapter_conformance_audit_projection_covered
hermes_runtime_adapter_conformance_failures_covered
hermes_runtime_adapter_conformance_concurrency_covered
hermes_runtime_adapter_conformance_cleanup_covered
hermes_runtime_adapter_conformance_register_reconciled
hermes_runtime_adapter_conformance_ready
no_runtime_adapter_operation
no_final_adapter_facade
no_live_Hermes_launch
no_dashboard_launch
no_gateway_launch
no_readiness_probe
no_parent_environment_read
no_provider_activation
no_worker_start
no_agent_start
no_tool_execution
no_MCP_execution
no_frontend_change
no_dependency_change
no_lockfile_change
no_audit_persistence
no_audit_publication
no_repository_runtime_artifact
no_Graphify_regeneration
no_Graphify_modification
no_git_mutation_by_agent
```
