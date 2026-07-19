# P14.3 - Runtime Profile And Environment Sanitization

## Document Header

| Field | Value |
| --- | --- |
| Project | P14 - Governed Runtime Adapter |
| Ticket | P14.3 - Runtime Profile And Environment Sanitization |
| Date | 2026-07-19 |
| Status | `hermes_runtime_profile_environment_sanitization_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_runtime_profile_environment_sanitization.md` |
| Dynamic start commit | `c22a182884d2b57894fcb5b8114cd4907fa0cadd` |
| Origin main at start | `c22a182884d2b57894fcb5b8114cd4907fa0cadd` |
| Prerequisite process owner | `hermes_process_owner_ready` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

P14.3 adds the internal tracked runtime-profile registry and pure child-process
environment sanitizer that later P14 composition will use to produce a
`ResolvedProcessLaunchPlan` for the P14.2 process owner.

P14.3 does not make the runtime adapter operational. It does not implement the
final facade, workspace allocation, path containment beyond lexical validation,
readiness probing, runtime events, audit publication, graceful Hermes shutdown,
lifecycle cancellation, rollback, live Hermes launch, gateway launch, provider
activation, worker launch, agent launch, tool execution, MCP execution, UI
lifecycle controls or Git authority.

The binding implementation verdict is:

```text
hermes_runtime_profile_environment_sanitization_ready
```

## Prerequisite Gate

```yaml
P14_3_PrerequisiteGate:
  branch: main
  dynamic_start_commit: c22a182884d2b57894fcb5b8114cd4907fa0cadd
  origin_main: c22a182884d2b57894fcb5b8114cd4907fa0cadd
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
  P14_2_commit: c22a182884d2b57894fcb5b8114cd4907fa0cadd
  P14_2_verdict: hermes_process_owner_ready
  runtime_adapter_contract_schema_version: 1
  runtime_adapter_profiles_absent_at_start: true
  runtime_adapter_environment_absent_at_start: true
  product_tracked_files_at_start: 6194
  modification_register_rows_at_start: 76
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  product_UI_feature: experimental
  product_extension_modules: 9
  locked_upstream_clean_at_start: true
  nested_product_git: false
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  graphify_frozen_integrity_at_start: true
```

The prerequisite gate passed. P14.3 proceeded only because P14.2 was already
committed on `main` and `HEAD == origin/main` at
`c22a182884d2b57894fcb5b8114cd4907fa0cadd`.

## Source Navigation Evidence

P14.3 used existing Graphify artifacts only as frozen read-only navigation
context. No Graphify command or process was run.

Follow-up inspection was limited to:

- P14.1 runtime-adapter contracts and source guards.
- P14.2 `ResolvedProcessLaunchPlan` shape.
- Existing Hermes home/environment conventions.
- P13.R Files-root isolation context.
- The product modification register and prior governance records.

## Files Added

P14.3 adds exactly four product files:

```text
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/profiles.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/environment.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_profiles.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_environment.py
```

P14.3 modifies exactly one existing product governance file:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

P14.3 creates this non-product governance record:

```text
0_architecture/governance/agent_platform_hermes_runtime_profile_environment_sanitization.md
```

No existing P14.1 or P14.2 runtime-adapter file, root export, product
configuration, backend route, frontend file, package manifest, dependency
lockfile, immutable upstream file or Graphify file was modified.

## Runtime Profile Registry

`profiles.py` defines exactly two internal tracked runtime profiles:

```text
test.lifecycle_probe
hermes.dashboard.experimental
```

The registry is immutable and deterministic. It exposes internal submodule APIs
only:

```text
get_runtime_profile(profile_id)
list_runtime_profiles()
list_runtime_profile_ids()
```

The root `hermes_cli.agent_platform.runtime_adapter` package remains
contract-only and does not export registry classes or lookup functions.

Profile definitions contain only stable references and logical selectors:

```yaml
RuntimeProfileDefinition:
  executable_selector: logical_current_product_python
  argument_selector: logical_profile_specific_selector
  execution_scope:
    test.lifecycle_probe: inert_test_only
    hermes.dashboard.experimental: p14_8_only
  timeout_policy: RuntimeTimeoutPolicy
  default_workspace_binding: RuntimeWorkspaceBinding
```

The registry does not resolve `sys.executable`, materialize arguments, choose a
working directory, read configuration, read environment variables, scan dynamic
plugins or launch processes.

## Environment Sanitizer

`environment.py` implements the pure function:

```text
sanitize_runtime_environment(
  profile,
  platform_family,
  source_environment,
  paths,
  explicit_path_entries=(),
) -> SanitizedRuntimeEnvironment
```

The sanitizer reads only caller-supplied mappings and path values. It does not
read `os.environ`, call `Path.home()`, expand user paths, import dotenv files,
start subprocesses, mutate the filesystem, log raw values or merge the parent
environment.

Managed variables are always adapter-controlled:

```text
HERMES_HOME
HOME
USERPROFILE
APPDATA
LOCALAPPDATA
TEMP
TMP
TMPDIR
HOMEDRIVE
HOMEPATH
```

Windows bootstrap inheritance is intentionally narrow:

```text
SystemRoot
WINDIR
```

`PATH` is never inherited. Dashboard profile callers may supply explicit path
entries. The lifecycle-probe profile rejects explicit `PATH` entries. Every path
entry is lexically absolute, bounded and duplicate-checked before output.

The dashboard profile requires a managed Files root. P14.3 validates that the
Files-root value is syntactically present and lexically safe. P14.4 still owns
workspace creation and containment enforcement.

Denied source variables are excluded by name and are represented in reports only
by bounded names and counts. Provider secrets, proxy variables and dynamic-loader
injection variables are not emitted.

## Sanitization Evidence

`SanitizedRuntimeEnvironment` is immutable and copy-safe:

```yaml
SanitizedRuntimeEnvironment:
  items: tuple[tuple[str, str], ...]
  as_mapping_returns_new_copy: true
  repr_excludes_values: true
  compatible_with_ResolvedProcessLaunchPlan_environment_items: true
```

`RuntimeEnvironmentSanitizationReport` contains secret-free evidence only:

```yaml
RuntimeEnvironmentSanitizationReport:
  profile_id: included
  environment_policy_id: included
  platform_family: included
  source_variable_count: included
  output_variable_count: included
  inherited_variable_names: names_only
  managed_variable_names: names_only
  fixed_variable_names: names_only
  explicit_path_entry_count: included
  excluded_variable_count: included
  excluded_sensitive_variable_names: bounded_names_only
  managed_home_bound: boolean
  managed_files_root_required: boolean
  managed_files_root_supplied: boolean
  provider_variables_present_in_output: must_be_false
```

## Modification Register

```yaml
P14_3_register_result:
  rows_before: 76
  rows_added: 4
  rows_after: 80
  columns: 18
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  missing_files: 0
  hash_mismatches: 0
  register_sha256: 074b1fb3501e4cc002f0eb805f176f9ad318d430df33d65c4c0338c32703c923
  normalized_rows_sha256: 4533014231359f50279ebad366a0dadc8ee84fea0b7580bfdf8e42a90f561188
```

Registered P14.3 product hashes:

| Row | Path | SHA-256 |
| --- | --- | --- |
| `P14.3-001` | `hermes_cli/agent_platform/runtime_adapter/profiles.py` | `936d735a338b3de9cd1e1d3de22aa5411b62de728ae56170a4427c7268cbfa88` |
| `P14.3-002` | `hermes_cli/agent_platform/runtime_adapter/environment.py` | `0ef8510525e9ec62fb8016fd94f21f33584e1c05d6ec8ca0f338ecb72e118c52` |
| `P14.3-003` | `tests/hermes_cli/test_agent_platform_runtime_profiles.py` | `1b43068f13100e8eb8b45b7a1eac3241753c9f74862b1aa2bcf9d0444eb5b60a` |
| `P14.3-004` | `tests/hermes_cli/test_agent_platform_runtime_environment.py` | `67843a5b5bdaf0cb25fe0e7627ad59b9dde062d57d0266b66811e6f89e566bc4` |

## Product Inventory

```yaml
P14_3_product_inventory:
  product_files_at_start: 6194
  new_product_files: 4
  product_file_inventory_after_human_tracking: 6198
  existing_product_files_modified:
    - AGENT_PLATFORM_MODIFICATIONS.tsv
  existing_runtime_adapter_contract_files_modified: false
  existing_runtime_adapter_process_owner_files_modified: false
  frontend_files_modified: false
  dependencies_modified: false
  lockfiles_modified: false
```

Because the agent did not stage files, `git ls-files` remains at 6194 until the
human stages and commits the four new product files. The candidate inventory is
6198 product files.

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Wrapper attempt | Blocked by checkout shape | `bash scripts/run_tests.sh tests/hermes_cli/test_agent_platform_runtime_profiles.py tests/hermes_cli/test_agent_platform_runtime_environment.py -q` reported no POSIX virtualenv under `.venv/bin` or `venv/bin` |
| P14.3 targeted tests | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_profiles.py tests/hermes_cli/test_agent_platform_runtime_environment.py`, 17 tests |
| Runtime-adapter regression | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py tests/hermes_cli/test_agent_platform_runtime_process_owner.py tests/hermes_cli/test_agent_platform_runtime_profiles.py tests/hermes_cli/test_agent_platform_runtime_environment.py`, 46 tests |
| Adjacent product regression | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_product_config.py tests/hermes_cli/test_agent_platform_product_routes.py`, 16 tests |
| Import smoke | Pass | Output `1` for `runtime_adapter.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION` |
| Compile check | Pass | `.\.venv\Scripts\python.exe -m compileall -q hermes_cli/agent_platform/runtime_adapter tests/hermes_cli/test_agent_platform_runtime_profiles.py tests/hermes_cli/test_agent_platform_runtime_environment.py` |
| Ruff check | Pass | `All checks passed!` |
| Ruff format check | Pass | `4 files already formatted` |
| Windows-footgun scanner | Pass | `No Windows footguns found (4 file(s) scanned).` |
| Register validation | Pass | 80 rows, 18 columns, zero duplicate IDs, zero duplicate paths, zero missing fields, zero missing files, zero hash mismatches |
| Diff whitespace check | Pass with line-ending warning | `git diff --check` emitted only the existing Windows LF-to-CRLF warning for the register |

## Graphify Integrity

No Graphify generation, update, extraction, clustering, export or refresh ran as
part of P14.3.

```yaml
P14_3_GraphifyIntegrity:
  graph_json_sha256: 02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2
  provenance_json_sha256: 952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550
  graphify_generation_performed: false
  graphify_modification_performed: false
```

## Authority Boundaries

```yaml
P14_3_authority_boundaries:
  final_runtime_adapter_facade: false
  public_executable_request_fields: false
  profile_registry_public_root_export: false
  environment_sanitizer_public_root_export: false
  dynamic_profile_discovery: false
  executable_resolution: false
  argument_materialization: false
  shell_execution: false
  process_launch_by_P14_3: false
  parent_environment_read: false
  parent_environment_merge: false
  PATH_inheritance: false
  provider_secret_output: false
  proxy_variable_output: false
  dynamic_loader_variable_output: false
  workspace_allocation: false
  path_containment_enforcement: false
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
remove profiles.py
remove environment.py
remove test_agent_platform_runtime_profiles.py
remove test_agent_platform_runtime_environment.py
remove P14.3-001 through P14.3-004 from AGENT_PLATFORM_MODIFICATIONS.tsv
remove this governance record
```

After commit, rollback requires a human-created revert commit.

## P14.4 Handoff

P14.4 may use P14.3 sanitized environment output and tracked profile metadata to
bind workspace allocation and path containment. P14.4 must not reinterpret
`RuntimeLaunchRequest` as executable command authority.

P14.8 remains the only live Hermes lifecycle gate. P15 provider/runtime work and
P17 execution remain unauthorized.

## Final Verdict

```yaml
P14_3_RuntimeProfileEnvironmentSanitizationVerdict:
  prerequisites:
    dynamic_start_commit_resolved: true
    HEAD_equals_origin_main: true
    P14_0_committed: true
    P14_1_committed: true
    P14_2_committed: true
    contract_schema_version: 1
    register_valid_at_start: true
    upstream_clean: true
    Graphify_frozen_integrity: true

  implementation:
    profile_registry_created: true
    environment_sanitizer_created: true
    profile_registry_tests_created: true
    environment_sanitizer_tests_created: true
    dependencies_added: 0
    lockfiles_modified: 0
    existing_contract_files_modified: false
    existing_process_owner_files_modified: false
    root_exports_modified: false

  profile_registry:
    exact_authorized_profile_count: 2
    test_lifecycle_probe_profile_present: true
    dashboard_experimental_profile_present: true
    immutable_definitions: true
    deterministic_order: true
    logical_selectors_only: true
    dynamic_loading: false
    executable_authority: false

  environment_sanitization:
    pure_function: true
    explicit_source_mapping_only: true
    parent_environment_read: false
    parent_environment_merge: false
    managed_home_bound: true
    windows_bootstrap_allowlist_only: true
    inherited_PATH: false
    explicit_PATH_profile_scoped: true
    provider_secret_output: false
    proxy_output: false
    dynamic_loader_output: false
    files_root_required_for_dashboard: true
    values_excluded_from_repr: true
    compatible_with_resolved_launch_plan: true

  authority:
    workspace_allocation_authorized: false
    path_containment_authorized: false
    readiness_authorized: false
    event_normalization_authorized: false
    lifecycle_cancellation_authorized: false
    graceful_shutdown_authorized: false
    rollback_authorized: false
    live_Hermes_authorized: false
    provider_authorized: false
    worker_authorized: false
    agent_authorized: false
    tool_authorized: false
    MCP_authorized: false
    Git_authorized: false

  validation:
    targeted_profile_environment_tests_passed: true
    runtime_adapter_regression_passed: true
    adjacent_regression_passed: true
    import_smoke_passed: true
    compile_check_passed: true
    Ruff_passed: true
    Windows_footgun_scan_passed: true
    register_valid: true
    graphify_hashes_unchanged: true

  final_state:
    product_file_inventory_after_human_tracking: 6198
    modification_register_rows: 80
    live_Hermes_processes_started: 0
    runtime_adapter_operational: false
    staged_files: 0
    commits_by_agent: 0
    pushes_by_agent: 0

  sequencing:
    P14_4_unlocked_after_human_commit: true
    P14_8_owns_live_Hermes_gate: true
    P15_unauthorized: true
    P17_unauthorized: true

  final_verdict: hermes_runtime_profile_environment_sanitization_ready
```

## Result Markers

```text
hermes_P14_3_prerequisite_gate_passed
hermes_process_owner_committed
hermes_runtime_profile_registry_internal_boundary_defined
hermes_runtime_profile_registry_exact_two_profiles
hermes_runtime_profile_registry_logical_selectors_only
hermes_runtime_environment_sanitizer_defined
hermes_runtime_environment_explicit_source_mapping_only
hermes_runtime_environment_parent_env_not_read
hermes_runtime_environment_parent_env_not_merged
hermes_runtime_environment_managed_home_bound
hermes_runtime_environment_windows_bootstrap_allowlist
hermes_runtime_environment_path_not_inherited
hermes_runtime_environment_explicit_path_profile_scoped
hermes_runtime_environment_provider_secrets_excluded
hermes_runtime_environment_proxies_excluded
hermes_runtime_environment_loader_injection_excluded
hermes_runtime_environment_files_root_profile_policy_enforced
hermes_runtime_environment_resolved_launch_plan_compatible
hermes_runtime_environment_register_reconciled
hermes_runtime_profile_environment_sanitization_ready
no_runtime_adapter_facade
no_public_command_authority
no_shell_execution
no_process_launch_by_P14_3
no_live_Hermes_launch
no_gateway_launch
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
