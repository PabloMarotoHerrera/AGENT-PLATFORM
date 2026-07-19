# P14.4 - Runtime Workspace And Path Containment

## Document Header

| Field | Value |
| --- | --- |
| Project | P14 - Governed Runtime Adapter |
| Ticket | P14.4 - Workspace and Path Containment |
| Date | 2026-07-19 |
| Status | `hermes_runtime_workspace_containment_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_runtime_workspace_path_containment.md` |
| Dynamic start commit | `0a71588ce391bdba7dee1af3f5eeadc1c2570fd0` |
| Origin main at start | `0a71588ce391bdba7dee1af3f5eeadc1c2570fd0` |
| Prerequisite profile/environment sanitizer | `hermes_runtime_profile_environment_sanitization_ready` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

P14.4 establishes the internal workspace allocation and host-path containment
boundary used by later governed runtime-adapter composition. It binds tracked
runtime profiles to tracked workspace policies, allocates opaque workspace IDs
below a trusted base root, creates fixed contained directory layouts, writes a
deterministic ownership marker, projects P14.3 environment paths and locks a
managed dashboard Files root.

P14.4 does not make the runtime adapter operational. It does not implement
process launch, executable resolution, argv resolution, parent environment
acquisition, listener discovery, readiness, Files API routes, HTTP response
mapping, runtime events, audit publication, lifecycle cancellation, graceful
shutdown, forced shutdown composition, general workspace cleanup, rollback,
provider credentials, inference, workers, agents, tools, MCP, UI controls or Git
authority.

The binding implementation verdict is:

```text
hermes_runtime_workspace_containment_ready
```

## Prerequisite Gate

```yaml
P14_4_PrerequisiteGate:
  branch: main
  dynamic_start_commit: 0a71588ce391bdba7dee1af3f5eeadc1c2570fd0
  origin_main: 0a71588ce391bdba7dee1af3f5eeadc1c2570fd0
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
  P14_2_committed: true
  P14_2_verdict: hermes_process_owner_ready
  P14_3_committed: true
  P14_3_verdict: hermes_runtime_profile_environment_sanitization_ready
  runtime_adapter_contract_schema_version: 1
  runtime_adapter_contract_package_present: true
  process_owner_present: true
  runtime_profile_registry_present: true
  environment_sanitizer_present: true
  workspace_allocator_absent_at_start: true
  path_containment_absent_at_start: true
  product_tracked_files_at_start: 6198
  modification_register_rows_at_start: 80
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

The prerequisite gate passed. P14.4 proceeded only because P14.3 was already
committed on `main` and `HEAD == origin/main` at
`0a71588ce391bdba7dee1af3f5eeadc1c2570fd0`.

## Source Navigation Evidence

P14.4 used frozen Graphify artifacts only as read-only navigation context. The
ticket text had conflicting instructions: it requested a bounded Graphify query
and also prohibited any Graphify process. The stricter frozen-graph instruction
was honored. No Graphify CLI, update, extraction, clustering, export or refresh
process ran.

Follow-up inspection was limited to:

- P14.1 workspace contracts and stable identifier constraints.
- P14.2 `ResolvedProcessLaunchPlan` working-directory and environment shape.
- P14.3 `RuntimeProfileDefinition`, `RuntimeEnvironmentPaths` and workspace IDs.
- Existing dashboard Files-root policy behavior.
- Existing path handling and P14 source-guard constraints.
- The product modification register and previous P14 governance records.

## Files Added

P14.4 adds exactly four product files:

```text
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/path_containment.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/workspace.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_path_containment.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_workspace.py
```

P14.4 modifies exactly one existing product governance file:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

P14.4 creates this non-product governance record:

```text
0_architecture/governance/agent_platform_hermes_runtime_workspace_path_containment.md
```

No P14.1, P14.2 or P14.3 implementation file, root export, product
configuration, backend route, frontend file, package manifest, dependency
lockfile, immutable upstream file or Graphify file was modified.

## Workspace Policy Registry

`workspace.py` defines exactly two immutable workspace policies:

```yaml
registered_workspace_policies:
  - policy_id: runtime.workspace.test.lifecycle_probe.v1
    scope: inert_test_temporary
    require_managed_files_root: false
    ownership_marker_required: true
    directory_layout:
      - home
      - user-profile
      - hermes-home
      - appdata
      - localappdata
      - temp
      - logs
      - state
      - evidence
      - workdir
  - policy_id: runtime.workspace.hermes.dashboard.experimental.v1
    scope: p14_8_artifact_only
    require_managed_files_root: true
    ownership_marker_required: true
    directory_layout:
      - home
      - user-profile
      - hermes-home
      - appdata
      - localappdata
      - temp
      - logs
      - state
      - evidence
      - workdir
      - files-root
```

No mutable registration API, dynamic discovery API or external workspace policy
input is present.

## Trusted Base-Root Boundary

The allocator accepts one trusted base root from an internal composition
boundary. It does not accept base roots, workspace roots, Files-root paths or
workspace IDs from public P14.1 request contracts, query parameters, frontend
requests, environment variables, plugin descriptors or arbitrary configuration
files.

`validate_trusted_base_root` requires the supplied root to be absolute,
existing, a directory, not a filesystem or drive root, not UNC, not a Windows
device path, not a symlink and not a Windows reparse point. It resolves the root
deterministically and never creates it.

## Path Containment

`path_containment.py` provides internal primitives for:

```text
validate_trusted_base_root
validate_safe_path_segment
join_contained_child
assert_existing_path_contained
assert_path_chain_safe
is_reparse_or_symlink
validate_managed_files_root_candidate
```

Safe path segments are single components: non-empty, at most 128 characters, no
slash, backslash, colon, NUL, control character, leading/trailing whitespace,
`.` or `..`. Windows mode also rejects trailing dots/spaces and reserved device
basenames including `CON.txt`.

Containment is component-based, not string-prefix-based. Canonical comparisons
preserve full path components, reject sibling-prefix paths, reject parent
segments, reject outside absolute paths and reject anchor/drive changes.

Comparison semantics:

```yaml
Windows: case_insensitive_components
POSIX: case_sensitive_components
```

Redirect policy:

```yaml
POSIX_symlink_detection: os.lstat + stat.S_ISLNK
Windows_reparse_detection: os.lstat + st_file_attributes + FILE_ATTRIBUTE_REPARSE_POINT
symlink_inside_root: rejected
symlink_escape: rejected
junction_or_reparse_escape: rejected
ambiguous_inspection: fail_closed
```

Nonexistent children are validated by proving every existing ancestor is already
contained and redirect-free, then validating each missing component as a safe
single segment. The validation function does not create the candidate.

## Workspace Allocation

`RuntimeWorkspaceAllocator` is an internal submodule API only:

```python
from hermes_cli.agent_platform.runtime_adapter.workspace import RuntimeWorkspaceAllocator
```

The public `hermes_cli.agent_platform.runtime_adapter` root remains
contract-only and does not export allocator, path-containment or Files-root
binding types.

Allocator properties:

```yaml
trusted_base_root_required: true
opaque_workspace_ID_generated_internally: true
workspace_ID_shape: ws_<lowercase opaque token>
caller_workspace_ID: false
fixed_directory_layout: true
exclusive_workspace_root_creation: true
exclusive_marker_creation: true
instance_local_registry: true
thread_safe_registry_access: true
module_level_workspace_registry: false
background_thread: false
atexit_primary_cleanup: false
general_cleanup_API: false
```

Allocation sequence:

```text
validate request
resolve tracked workspace policy
generate opaque workspace ID
derive contained workspace-root candidate
create workspace root exclusively
verify workspace root containment and redirect-free status
create fixed subdirectories exclusively
verify every created directory
write deterministic ownership marker exclusively
construct RuntimeWorkspaceRef with status allocated
project RuntimeEnvironmentPaths
bind managed Files root when policy requires it
register allocation by runtime ID
```

`get(runtime_id)` returns only allocations created by the current allocator
instance. It does not scan directories or reconstruct ownership from host files.
`allocated_runtime_ids()` returns a sorted tuple.

## Ownership Marker

Every successful allocation writes exactly one marker:

```text
.agent-platform-runtime-workspace.json
```

Marker contract:

```yaml
schema_version: 1
fields:
  - runtime_id
  - schema_version
  - workspace_id
  - workspace_policy_id
serialization:
  encoding: UTF-8
  sorted_keys: true
  single_trailing_newline: true
  platform_dependent_values: false
excluded:
  - absolute paths
  - usernames
  - hostnames
  - environment variables
  - commands
  - arguments
  - provider information
  - credentials
  - host-clock timestamps
  - arbitrary metadata
```

The marker is future rollback evidence. It is not an audit event.

## Files Root

Dashboard workspaces allocate `files-root` under the workspace root and bind it
through `RuntimeFilesRootBinding`:

```yaml
default_path_equals_locked_root: true
can_change_path: false
safe_repr_exposes_absolute_path: false
```

The test lifecycle-probe workspace has no Files-root and no binding.

`validate_managed_files_path` accepts the locked root itself and contained
children, rejects outside paths, rejects sibling-prefix paths, rejects relative
paths, rejects drive or anchor changes, rejects UNC/device paths and rejects
symlink/junction/reparse escapes. It performs no HTTP mapping; later integration
may map governed outside-root failures to HTTP 403.

## Environment-Path Projection

The allocator projects exact P14.3 `RuntimeEnvironmentPaths` values:

```yaml
hermes_home: paths.hermes_home
home: paths.home
user_profile: paths.user_profile
app_data: paths.app_data
local_app_data: paths.local_app_data
temp: paths.temp
files_root: paths.files_root_or_null
```

Each projected non-null path exists, is a directory, is contained beneath the
workspace root and is not a symlink or reparse point. P14.4 does not call
`sanitize_runtime_environment` during allocation; compatibility is proven in
tests with synthetic source mappings.

## Allocation Compensation

Allocation-time compensation is local to one failed allocation attempt. It may
remove only the marker or empty directories that were created by that same call,
in reverse creation order, after revalidating containment. It does not use
recursive deletion, broad globs, base-root deletion or cleanup of successful
workspaces.

Compensation failure remains explicit via `WorkspaceAllocationCompensationError`.
General cleanup belongs to P14.6.

## Modification Register

```yaml
P14_4_register_result:
  rows_before: 80
  rows_added: 4
  rows_after: 84
  columns: 18
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  missing_files: 0
  hash_mismatches: 0
  register_sha256: 23db3ce207f49d59abf001395a9d60d3da0f64bde3efcaf57c2bfd8da4c93476
  normalized_rows_sha256: e34cfbb2b416f0cf846f3a7fc837146fb8ed46185eecd7db8fe4b9d8ee1d2796
```

Registered P14.4 product hashes:

| Row | Path | SHA-256 |
| --- | --- | --- |
| `P14.4-001` | `hermes_cli/agent_platform/runtime_adapter/path_containment.py` | `9bd5b97c16c8de1f041e6a0e40be0d16707940a7abc9aa945767db276e8e5888` |
| `P14.4-002` | `hermes_cli/agent_platform/runtime_adapter/workspace.py` | `7e43f6e91bd3547b16d423e2612750aa596ea809c9d606ad38aa714609f9a9ec` |
| `P14.4-003` | `tests/hermes_cli/test_agent_platform_runtime_path_containment.py` | `72cbb1042c540d80ecda7fed486965200a149e7950cfbabe298364f67b93fef9` |
| `P14.4-004` | `tests/hermes_cli/test_agent_platform_runtime_workspace.py` | `faafbc3bb4b8b31aa178ddbb4ce6889a041d9ef556f8bfd4d4c8c76afaa9d1a1` |

## Product Inventory

```yaml
P14_4_product_inventory:
  product_files_at_start: 6198
  new_product_files: 4
  product_file_inventory_after_human_tracking: 6202
  existing_product_files_modified:
    - AGENT_PLATFORM_MODIFICATIONS.tsv
  existing_runtime_adapter_files_modified: false
  frontend_files_modified: false
  dependencies_modified: false
  lockfiles_modified: false
```

Because the agent did not stage files, `git ls-files` remains at 6198 until the
human stages and commits the four new product files. The candidate inventory is
6202 product files.

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Targeted P14.4 tests | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_path_containment.py tests/hermes_cli/test_agent_platform_runtime_workspace.py`, 45 passed, 3 skipped host symlink-permission cases |
| P14.3 regression | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_profiles.py tests/hermes_cli/test_agent_platform_runtime_environment.py`, 17 tests |
| P14.2 regression | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_process_owner.py`, 13 tests |
| P14.1 regression | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py`, 16 tests |
| Adjacent product regression | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_product_config.py tests/hermes_cli/test_agent_platform_product_routes.py`, 16 tests |
| Internal import smoke | Pass | Output `RuntimeWorkspaceAllocator` |
| Root-export safety smoke | Pass | Output `contract-only-root` |
| Compile check | Pass | `.\.venv\Scripts\python.exe -m compileall -q hermes_cli/agent_platform/runtime_adapter tests/hermes_cli/test_agent_platform_runtime_path_containment.py tests/hermes_cli/test_agent_platform_runtime_workspace.py` |
| Ruff check | Pass | `All checks passed!` |
| Ruff format check | Pass | `14 files already formatted` |
| Windows-footgun scanner | Pass | `No Windows footguns found (767 file(s) scanned).` |
| Register validation | Pass | 84 rows, 18 columns, zero duplicate IDs, zero duplicate paths, zero missing fields, zero missing files, zero hash mismatches |
| Fixture-process leak check | Pass | `runtime_adapter_lifecycle_probe.py python processes: 0` |
| Repository-artifact check | Pass | No `9_artifacts/**` files found |
| Workspace marker artifact check | Pass | No `.agent-platform-runtime-workspace.json` files found under the repository |
| Diff whitespace check | Pass with line-ending warning | `git diff --check` emitted only the existing Windows LF-to-CRLF warning for the register |
| Candidate path audit | Pass | Exactly six authorized P14.4 candidate paths, zero unexpected and zero missing |

## Graphify Integrity

No Graphify generation, update, extraction, clustering, export, query or refresh
process ran as part of P14.4.

```yaml
P14_4_GraphifyIntegrity:
  graph_json_sha256: 02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2
  provenance_json_sha256: 952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550
  graphify_generation_performed: false
  graphify_modification_performed: false
```

## Authority Boundaries

```yaml
P14_4_authority_boundaries:
  final_runtime_adapter_facade: false
  public_workspace_path_authority: false
  caller_workspace_ID: false
  real_user_path_discovery: false
  parent_environment_read: false
  process_launch: false
  executable_resolution: false
  argv_resolution: false
  listener_discovery: false
  port_probe: false
  HTTP_readiness: false
  Files_API_routes: false
  HTTP_response_mapping: false
  runtime_event_generation: false
  audit_publication: false
  lifecycle_cancellation: false
  graceful_shutdown: false
  forced_shutdown_composition: false
  successful_workspace_cleanup: false
  runtime_rollback: false
  provider_credentials: false
  provider_inference: false
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
remove path_containment.py
remove workspace.py
remove test_agent_platform_runtime_path_containment.py
remove test_agent_platform_runtime_workspace.py
remove P14.4-001 through P14.4-004 from AGENT_PLATFORM_MODIFICATIONS.tsv
remove this governance record
verify no repository-local test workspace exists
verify runtime_adapter_lifecycle_probe.py python processes: 0
```

Rollback must not use recursive deletion, `git reset`, `git clean`, `git
checkout` or `git restore`. After commit, rollback requires a human-created
revert commit.

## P14.5 Handoff

P14.5 remains blocked until P14.4 is human-reviewed and committed. P14.5 may
consume the internal workspace allocation and containment results, but must not
reinterpret public launch requests as arbitrary workspace path or executable
authority.

P14.6 remains blocked for cancellation, shutdown and rollback. P14.8 remains the
only live Hermes lifecycle gate. P15 provider/runtime work and P17 execution
remain unauthorized.

## Final Verdict

```yaml
P14_4_WorkspaceAndPathContainmentVerdict:
  prerequisites:
    dynamic_start_commit_resolved: true
    HEAD_equals_origin_main: true
    P14_0_committed: true
    P14_1_committed: true
    P14_2_committed: true
    P14_3_committed: true
    contract_schema_version: 1
    register_valid_at_start: true
    upstream_clean: true
    Graphify_frozen_integrity: true

  implementation:
    workspace_policy_registry_created: true
    workspace_allocator_created: true
    path_containment_created: true
    managed_files_root_binding_created: true
    workspace_marker_created: true
    path_tests_created: true
    workspace_tests_created: true
    dependencies_added: 0
    lockfiles_modified: 0
    existing_runtime_adapter_files_modified: false
    root_exports_modified: false

  policies:
    registered_count: 2
    test_workspace_policy_registered: true
    dashboard_workspace_policy_registered: true
    mutable_registration_available: false
    dynamic_discovery_available: false
    dashboard_managed_files_root_required: true

  containment:
    trusted_base_required: true
    caller_path_authority: false
    workspace_ID_generated_internally: true
    string_prefix_containment_used: false
    component_containment_used: true
    Windows_case_insensitive: true
    POSIX_case_sensitive: true
    symlink_escape_rejected: true
    junction_escape_rejected: true
    reparse_escape_rejected: true
    drive_escape_rejected: true
    UNC_rejected: true
    device_path_rejected: true

  allocation:
    exclusive_workspace_creation: true
    fixed_directory_layout: true
    deterministic_marker: true
    runtime_workspace_ref_created: true
    environment_paths_projected: true
    duplicate_runtime_rejected: true
    preexisting_workspace_rejected: true
    partial_failure_compensated: true
    recursive_deletion_used: false
    general_cleanup_available: false

  files_root:
    dashboard_files_root_created: true
    default_equals_locked_root: true
    can_change_path: false
    outside_path_rejected: true
    HTTP_mapping_implemented: false

  authority:
    process_launch_authorized: false
    readiness_authorized: false
    event_normalization_authorized: false
    audit_publication_authorized: false
    successful_workspace_cleanup_authorized: false
    runtime_rollback_authorized: false
    provider_authorized: false
    worker_authorized: false
    agent_authorized: false
    tool_authorized: false
    MCP_authorized: false
    Git_authorized: false

  validation:
    targeted_workspace_tests_passed: true
    profile_environment_regression_passed: true
    process_owner_regression_passed: true
    contract_regression_passed: true
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
    product_tracked_files: 6202
    modification_register_rows: 84
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
    P14_5_unlocked_after_human_commit: true
    P14_6_blocked: true
    P14_8_owns_live_Hermes_gate: true
    P15_unauthorized: true
    P17_unauthorized: true

  final_verdict: hermes_runtime_workspace_containment_ready
```

## Result Markers

```text
hermes_P14_4_prerequisite_gate_passed
hermes_P14_3_profile_sanitization_committed
hermes_runtime_workspace_policy_registry_created
hermes_runtime_workspace_policies_registered_2
hermes_runtime_workspace_allocator_created
hermes_runtime_workspace_ID_generated_internally
hermes_runtime_workspace_exclusive_creation
hermes_runtime_workspace_fixed_layout
hermes_runtime_workspace_marker_created
hermes_runtime_workspace_paths_contained
hermes_runtime_workspace_environment_paths_projected
hermes_runtime_workspace_duplicate_allocation_rejected
hermes_runtime_workspace_partial_allocation_compensated
hermes_runtime_path_string_prefix_rejected
hermes_runtime_path_parent_traversal_rejected
hermes_runtime_path_symlink_escape_rejected
hermes_runtime_path_junction_escape_rejected
hermes_runtime_path_reparse_escape_rejected
hermes_runtime_path_drive_escape_rejected
hermes_runtime_files_root_allocated
hermes_runtime_files_root_locked
hermes_runtime_files_root_path_change_denied
hermes_runtime_files_root_outside_path_rejected
hermes_runtime_workspace_register_reconciled
hermes_runtime_workspace_containment_ready
no_public_workspace_path_authority
no_caller_workspace_ID
no_real_user_path_access
no_process_launch
no_live_Hermes_launch
no_readiness_probe
no_event_normalization
no_shutdown_workflow
no_runtime_rollback
no_recursive_deletion
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
