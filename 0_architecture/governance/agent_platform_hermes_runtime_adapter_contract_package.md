# P14.1 - Hermes Runtime Adapter Contract Package

## Document Header

| Field | Value |
| --- | --- |
| Project | P14 - Governed Runtime Adapter |
| Ticket | P14.1 - Adapter Contract Package |
| Date | 2026-07-19 |
| Status | `hermes_runtime_adapter_contract_package_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_runtime_adapter_contract_package.md` |
| Dynamic start commit | `a14a7f06d3364a1f932101a3d23df130ca72310a` |
| Origin main at start | `a14a7f06d3364a1f932101a3d23df130ca72310a` |
| Prerequisite authorization | `hermes_runtime_adapter_implementation_authorized_with_constraints` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

P14.1 creates the governed Hermes runtime adapter contract package under the
AGENT PLATFORM-owned backend namespace. This ticket defines immutable data
models, stable vocabularies, bounded contract errors and a pure lifecycle state
machine only.

P14.1 does not launch Hermes, start dashboard runtime processes, create runtime
workspaces, sanitize live environments, implement process ownership, expose UI
lifecycle controls, configure providers, start workers, execute agents, execute
tools, call MCP servers, modify Git state or regenerate Graphify output.

The binding implementation verdict is:

```text
hermes_runtime_adapter_contract_package_ready
```

## Prerequisite Gate

```yaml
P14_1_PrerequisiteGate:
  branch: main
  dynamic_start_commit: a14a7f06d3364a1f932101a3d23df130ca72310a
  origin_main: a14a7f06d3364a1f932101a3d23df130ca72310a
  HEAD_equals_origin_main_at_start: true
  P14_0_authorization_present: true
  P14_0_authorization_verdict: hermes_runtime_adapter_implementation_authorized_with_constraints
  P13_R_committed: true
  P13_R_commit: aa91147b760fa1211ebd1f33dd0853d85083699a
  P13_residual_correction_committed: true
  P13_residual_correction_commit: ed5af2681ae842941aeb41e2d78fb83ba5fa4037
  P13_final_verdict: hermes_product_ui_foundation_closed_experimental_with_constraints
  product_UI_feature: experimental
  product_activation_counts: "9/9/9/9/5"
  product_tracked_files_at_start: 6183
  modification_register_rows_at_start: 65
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  runtime_adapter_package_absent_at_start: true
  locked_upstream_clean_at_start: true
  nested_product_git: false
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  graphify_frozen_integrity_at_start: true
```

The prerequisite gate passed. P14.1 proceeded only because P14.0 was already
committed on `main` and `HEAD == origin/main` at `a14a7f06d3364a1f932101a3d23df130ca72310a`.

## Files Added

P14.1 adds exactly six product files:

```text
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/__init__.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/enums.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/errors.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/contracts.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/state_machine.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py
```

P14.1 modifies exactly one existing product governance file:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

No frontend, UI, dependency, lockfile, Graphify, immutable upstream, gateway,
provider, worker, agent, tool, MCP or Git-control file was modified by P14.1.

## Contract Surface

The public package exports only reviewed contract symbols from
`hermes_cli.agent_platform.runtime_adapter`.

```yaml
P14_1_ContractSurface:
  schema_version: 1
  authorized_profile_ids:
    - test.lifecycle_probe
    - hermes.dashboard.experimental
  modules:
    __init__.py: public contract API exports
    enums.py: stable runtime vocabularies
    errors.py: bounded contract error hierarchy
    contracts.py: immutable Pydantic contract models
    state_machine.py: pure deterministic lifecycle transition functions
  immutable_models: true
  pydantic_extra_forbid: true
  deterministic_serialization_required: true
  arbitrary_command_execution_fields_excluded: true
```

The contract package defines the required lifecycle states:

```text
created
validating
starting
waiting_for_readiness
ready
cancellation_requested
stopping
stopped
cancelled
failed
rollback_pending
rolled_back
rollback_failed
```

The pure state machine preserves the P14.0 distinctions between process
launched and runtime ready, cancelled and failed, stopped and rolled back, and
rollback succeeded and rollback failed.

## Safety Boundaries

P14.1 request contracts deliberately exclude raw execution authority fields:

```text
command
argv
executable
executable_path
shell
cwd
working_directory
output_path
signal
kill_command
```

The contract package contains no imports or calls for subprocess launch, network
access, filesystem mutation, environment construction, provider access, worker
startup, agent startup, tool execution, MCP execution, UI controls or Git
mutation.

Runtime profile references identify policies by stable IDs. They do not expose
arbitrary executables, arbitrary arguments, arbitrary working directories,
arbitrary environments or arbitrary caller paths. Dashboard-class profile
references require a files-root policy identifier to preserve the P13.R Files
containment regression boundary.

## Modification Register

```yaml
P14_1_register_result:
  rows_before: 65
  rows_after: 71
  columns: 18
  rows_added:
    - P14.1-001
    - P14.1-002
    - P14.1-003
    - P14.1-004
    - P14.1-005
    - P14.1-006
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  hash_mismatches: 0
  register_sha256: dd7994128ad9f36e47562aef4f75c334d3d9c2aef26396f7f94941ba5dfbd52e
  normalized_rows_sha256: 608c1a81049b3d5dcfac85b875a9a6cfc4ffe0cfbf904c5e416c08e64719fc6b
```

Registered P14.1 product hashes:

| Row | Path | SHA-256 |
| --- | --- | --- |
| `P14.1-001` | `hermes_cli/agent_platform/runtime_adapter/__init__.py` | `b6e00f1d0de9e50da42ba820edb147a4a67c02fd9ef97b324834823a5172ff60` |
| `P14.1-002` | `hermes_cli/agent_platform/runtime_adapter/enums.py` | `57b7244f9c37d8ede7009f2df47e9a40258eb89b88b9f6284c77f221a3c2d0e4` |
| `P14.1-003` | `hermes_cli/agent_platform/runtime_adapter/errors.py` | `68205a2d6ba18be7feaa05f1568a15a442c1799ad1df8a120feab1ee7184e465` |
| `P14.1-004` | `hermes_cli/agent_platform/runtime_adapter/contracts.py` | `d4df7e8949c5a614bb468412dd407252801ed84882ff0ea619175077a62f5b1b` |
| `P14.1-005` | `hermes_cli/agent_platform/runtime_adapter/state_machine.py` | `6dd45719c19e905168d15a6e3627a8e96b3c7a153719e43cc7da64ff97e5b7fe` |
| `P14.1-006` | `tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py` | `3ec3f2b7cc4c2207f05617a534ebc22a42411f534949b5f0ed2bb3d47cd54ab7` |

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Runtime adapter contract tests | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py`, 16 tests |
| Product activation regression tests | Pass | `.\.venv\Scripts\python.exe -m pytest -q tests/hermes_cli/test_agent_platform_product_config.py tests/hermes_cli/test_agent_platform_product_routes.py`, 16 tests |
| Import smoke test | Pass | `.\.venv\Scripts\python.exe -c "from hermes_cli.agent_platform import runtime_adapter; print(runtime_adapter.RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION)"`, output `1` |
| Python compilation | Pass | `.\.venv\Scripts\python.exe -m compileall -q hermes_cli/agent_platform/runtime_adapter tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py` |
| Ruff lint | Pass | `.\.venv\Scripts\python.exe -m ruff check hermes_cli/agent_platform/runtime_adapter tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py` |
| Ruff format | Pass | `.\.venv\Scripts\python.exe -m ruff format --check hermes_cli/agent_platform/runtime_adapter tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py` |
| Modification register | Pass | 71 rows, 18 columns, zero duplicate IDs, zero duplicate paths, zero missing fields, zero hash mismatches |

The POSIX wrapper `bash scripts/run_tests.sh tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py -q`
was also attempted, but this Windows checkout exposes `.venv\Scripts` rather
than a POSIX `.venv/bin/activate`, so the wrapper could not locate a virtual
environment. The underlying per-file runner was invoked with the Windows venv
and completed with `1 files, 16 tests passed, 0 failed`; it emitted a Windows
console encoding progress-glyph warning after the test result had completed.

## Graphify Integrity

P14.1 did not run `graphify update`, extraction, clustering, export, refresh or
any other Graphify process. This intentionally follows the P14.1 frozen-graph
constraint even though the general repository guidance normally asks for a graph
update after code modification.

```yaml
P14_1_GraphifyIntegrity:
  graph_json_sha256: 02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2
  provenance_json_sha256: 952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550
  graphify_generation_performed: false
  graphify_modification_performed: false
```

## Final Verdict

```yaml
P14_1_RuntimeAdapterContractPackageVerdict:
  prerequisites:
    HEAD_equals_origin_main_at_start: true
    P14_0_authorization_committed: true
    P13_R_preserved: true
    P13_residual_correction_preserved: true
    product_UI_experimental: true
    product_activation_counts: "9/9/9/9/5"
    register_valid_before: true
    graphify_frozen_integrity: true

  implementation:
    runtime_adapter_package_created: true
    immutable_contracts_created: true
    stable_vocabularies_created: true
    bounded_errors_created: true
    pure_state_machine_created: true
    source_guard_tests_created: true
    dependencies_modified: false
    lockfiles_modified: false
    frontend_modified: false
    UI_lifecycle_controls_added: false

  authority:
    arbitrary_command_execution_authorized: false
    subprocess_launch_authorized: false
    live_Hermes_launch_authorized: false
    provider_authorized: false
    inference_authorized: false
    worker_authorized: false
    agent_authorized: false
    tool_execution_authorized: false
    MCP_execution_authorized: false
    Git_authorized: false

  validation:
    runtime_adapter_contract_tests_passed: true
    product_activation_regression_tests_passed: true
    import_smoke_passed: true
    compileall_passed: true
    ruff_check_passed: true
    ruff_format_check_passed: true
    register_hashes_match: true

  deliverable:
    canonical_contract_record_created: true
    product_register_rows_added: 6
    product_files_added: 6
    runtime_processes_started_by_adapter: false
    graphify_updated: false
    staged_by_agent: false
    committed_by_agent: false
    pushed_by_agent: false

  sequencing:
    P14_2_process_owner_unlocked_after_human_acceptance: true
    P14_8_owns_live_Hermes_gate: true
    P15_remains_unauthorized: true
    P17_remains_unauthorized: true

  final_verdict: hermes_runtime_adapter_contract_package_ready
```

## Result Markers

```text
hermes_P14_1_prerequisite_gate_passed
hermes_runtime_adapter_contract_package_created
hermes_runtime_adapter_contract_schema_version_1
hermes_runtime_adapter_public_api_reviewed
hermes_runtime_adapter_vocabularies_defined
hermes_runtime_adapter_immutable_models_defined
hermes_runtime_adapter_bounded_errors_defined
hermes_runtime_adapter_pure_state_machine_defined
hermes_runtime_adapter_transition_invalidity_rejected
hermes_runtime_adapter_terminal_policy_defined
hermes_runtime_adapter_profile_ids_defined
hermes_runtime_adapter_request_execution_fields_excluded
hermes_runtime_adapter_dashboard_files_root_policy_required
hermes_runtime_adapter_event_envelope_bounded
hermes_runtime_adapter_failure_envelope_bounded
hermes_runtime_adapter_result_envelope_validated
hermes_runtime_adapter_source_guard_tests_passed
hermes_P13_product_activation_preserved
hermes_modification_register_updated_for_P14_1
hermes_modification_register_valid
no_subprocess_launch_implementation
no_live_Hermes_launch
no_provider_activation
no_worker_start
no_agent_start
no_tool_execution_authority
no_MCP_execution_authority
no_UI_lifecycle_controls
no_dependency_change
no_lockfile_change
no_Graphify_regeneration
no_Graphify_modification
no_git_mutation_by_agent
```
