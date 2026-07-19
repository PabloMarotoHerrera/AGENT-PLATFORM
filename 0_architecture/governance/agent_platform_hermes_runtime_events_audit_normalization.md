# P14.5 - Runtime Events And Audit Normalization

## Document Header

| Field | Value |
| --- | --- |
| Project | P14 - Governed Runtime Adapter |
| Ticket | P14.5 - Runtime Events and Audit Normalization |
| Date | 2026-07-19 |
| Status | `hermes_runtime_events_audit_normalization_ready` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_runtime_events_audit_normalization.md` |
| Dynamic start commit | `d7372dfc8e9117f4495a2aa81032fd80ebae8d01` |
| Origin main at start | `d7372dfc8e9117f4495a2aa81032fd80ebae8d01` |
| Prerequisite workspace/path containment | `hermes_runtime_workspace_containment_ready` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

P14.5 adds internal runtime-event normalization, stable failure-code mapping and
non-authoritative audit projection over the P14.1 runtime contracts and P14.2 to
P14.4 internal evidence boundaries.

P14.5 does not make the runtime adapter operational. It does not implement
process launch composition, executable resolution, argv resolution, parent
environment acquisition, listener discovery, readiness probing, HTTP response
mapping, audit persistence, audit publication, lifecycle cancellation, graceful
shutdown, forced shutdown composition, workspace cleanup, rollback, provider
credentials, inference, workers, agents, tools, MCP, UI controls, Graphify
regeneration or Git authority.

The binding implementation verdict is:

```text
hermes_runtime_events_audit_normalization_ready
```

## Prerequisite Gate

```yaml
P14_5_PrerequisiteGate:
  branch: main
  dynamic_start_commit: d7372dfc8e9117f4495a2aa81032fd80ebae8d01
  origin_main: d7372dfc8e9117f4495a2aa81032fd80ebae8d01
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
  runtime_adapter_contract_schema_version: 1
  runtime_adapter_contract_package_present: true
  process_owner_present: true
  runtime_profile_registry_present: true
  environment_sanitizer_present: true
  workspace_allocator_present: true
  path_containment_present: true
  event_normalizer_absent_at_start: true
  audit_normalizer_absent_at_start: true
  product_tracked_files_at_start: 6202
  modification_register_rows_at_start: 84
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  graphify_frozen_integrity_at_start: true
```

The prerequisite gate passed. P14.5 proceeded only because P14.4 was already
committed on `main` and `HEAD == origin/main` at
`d7372dfc8e9117f4495a2aa81032fd80ebae8d01`.

## Source Navigation Evidence

P14.5 honored the stricter frozen-Graphify instruction. No Graphify CLI,
update, extraction, clustering, export or refresh process ran.

Follow-up inspection was limited to:

- P14.1 runtime event, failure, evidence and operation result contracts.
- P14.1 lifecycle, event, failure-stage, severity, retryability, process,
  workspace and cleanup vocabularies.
- P14.2 process ownership snapshots and bounded process-owner errors.
- P14.3 environment sanitization reports and bounded environment errors.
- P14.4 workspace allocations, path-containment errors and workspace errors.
- Existing P14 test and governance-record patterns.
- Existing broad audit-related code, which did not provide a directly reusable
  canonical audit model without persistence or runtime authority.

## Files Added

P14.5 adds exactly four product files:

```text
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/event_normalization.py
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/audit_normalization.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_event_normalization.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_runtime_audit_normalization.py
```

P14.5 modifies exactly one existing product governance file:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

P14.5 creates this non-product governance record:

```text
0_architecture/governance/agent_platform_hermes_runtime_events_audit_normalization.md
```

No P14.1, P14.2, P14.3 or P14.4 implementation file, root export, product
configuration, backend route, frontend file, package manifest, dependency
lockfile, immutable upstream file or Graphify file was modified.

## Event Normalization

`event_normalization.py` defines internal descriptors for every
`RuntimeEventType`. Each descriptor fixes:

- allowed lifecycle states;
- fixed failure stage or failure-derived stage policy;
- severity;
- stable message code;
- sanitized message;
- required evidence references.

`RuntimeEventJournal` is instance-local and appends `RuntimeEvent` contracts
with deterministic sequence numbers. It rejects:

- unknown event descriptors;
- disallowed lifecycle states;
- naive timestamps;
- timestamp or monotonic-offset regression;
- duplicate or malformed generated event IDs;
- missing required process, workspace, readiness or failure references;
- unexpected references;
- cross-runtime process, workspace or failure references;
- event streams above the P14.1 `RuntimeOperationResult` limit of 256 events.

The journal does not transition lifecycle state, launch processes, discover
listeners, probe readiness, mutate workspaces or persist events.

## Failure Normalization

`event_normalization.py` also defines internal mappings from stable P14.1 to
P14.4 operational error codes to safe `RuntimeFailure` facts.

The normalizer accepts only the reviewed error hierarchies:

```text
RuntimeAdapterContractError
RuntimeProcessOwnerError
RuntimeProfileRegistryError
RuntimeEnvironmentError
RuntimePathContainmentError
RuntimeWorkspaceError
```

For supported error codes, it emits:

- stable failure ID evidence;
- failure stage;
- sanitized summary independent of the source exception message;
- retryability;
- default or caller-supplied cleanup status;
- process and workspace status;
- sorted bounded evidence references.

Unsupported error classes, unknown error codes, duplicate evidence references and
malformed failure IDs fail closed with bounded normalization errors.

## Audit Projection

`audit_normalization.py` defines frozen internal DTOs:

```text
RuntimeAuditEventProjection
RuntimeAuditFailureProjection
RuntimeAuditProjection
```

The projection is explicitly non-authoritative:

```yaml
projection_kind: runtime_audit_projection
authority: non_authoritative
schema_version: 1
```

The projection is built from `RuntimeOperationResult`, `RuntimeEvent`,
`RuntimeFailure` and `RuntimeEvidenceRef`. It keeps only bounded contract facts:

- runtime, correlation, profile and workspace identifiers;
- lifecycle state and operation outcome;
- runtime creation timestamp;
- event projections;
- failure projection when present;
- log evidence references only;
- booleans indicating whether process, workspace or readiness evidence was
  present in the operation result.

It excludes raw process references, PIDs, workspace paths, readiness details,
listener ports, log bodies, commands, arguments, environment items, exception
messages and source objects.

Audit projection rejects:

- event sequence regression;
- event timestamp regression;
- monotonic-offset regression;
- missing failure event references when a failure is present;
- mismatched failure references;
- duplicate evidence IDs inside event, failure or log evidence collections;
- mutable or extra DTO fields.

The audit projection does not write audit logs, append to persistence, emit
events externally, start background tasks or become a canonical decision source.

## Public Export Boundary

P14.5 does not modify `hermes_cli/agent_platform/runtime_adapter/__init__.py`.
The root `runtime_adapter` package remains contract-only. Internal normalizer
and audit projection types are importable only from their submodules.

## Hash Register

```yaml
P14_5_FileHashes:
  hermes_cli/agent_platform/runtime_adapter/event_normalization.py: 22cb095507cd9da6d9520524ee4be8b35771ee5cd06c720c669755e9e1672b14
  hermes_cli/agent_platform/runtime_adapter/audit_normalization.py: 37ad195259dd8506ba4490dcae0414cddd89c1e7a5a753cb34236e6962dfd116
  tests/hermes_cli/test_agent_platform_runtime_event_normalization.py: 6fa6603238a060f02eeb33e7faad5276231e2253277bcb0d71c68ea1bafcb8cb
  tests/hermes_cli/test_agent_platform_runtime_audit_normalization.py: 6a4d449baa0c4dd1852b65d13cec19f9d0a69754920cdab671219e443baa3b11
```

`AGENT_PLATFORM_MODIFICATIONS.tsv` was updated with exactly four P14.5 rows:

```text
P14.5-001
P14.5-002
P14.5-003
P14.5-004
```

## Validation Evidence

The following commands passed from `2_products/hermes-agent`:

```text
python -m py_compile "hermes_cli/agent_platform/runtime_adapter/event_normalization.py" "hermes_cli/agent_platform/runtime_adapter/audit_normalization.py" "tests/hermes_cli/test_agent_platform_runtime_event_normalization.py" "tests/hermes_cli/test_agent_platform_runtime_audit_normalization.py"
python -m ruff check "hermes_cli/agent_platform/runtime_adapter/event_normalization.py" "hermes_cli/agent_platform/runtime_adapter/audit_normalization.py" "tests/hermes_cli/test_agent_platform_runtime_event_normalization.py" "tests/hermes_cli/test_agent_platform_runtime_audit_normalization.py"
scripts/run_tests.sh "tests/hermes_cli/test_agent_platform_runtime_event_normalization.py" "tests/hermes_cli/test_agent_platform_runtime_audit_normalization.py" "tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py" -q
scripts/run_tests.sh "tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py" "tests/hermes_cli/test_agent_platform_runtime_process_owner.py" "tests/hermes_cli/test_agent_platform_runtime_profiles.py" "tests/hermes_cli/test_agent_platform_runtime_environment.py" "tests/hermes_cli/test_agent_platform_runtime_path_containment.py" "tests/hermes_cli/test_agent_platform_runtime_workspace.py" "tests/hermes_cli/test_agent_platform_runtime_event_normalization.py" "tests/hermes_cli/test_agent_platform_runtime_audit_normalization.py" -q
```

Validation covered:

- event descriptor coverage for all P14.1 event types;
- sequence and timestamp guards;
- evidence-reference presence and runtime-identity guards;
- supported failure-code mapping across P14.1 to P14.4 error hierarchies;
- bounded failure evidence references;
- non-authoritative audit projection shape;
- failure-reference consistency;
- duplicate evidence rejection;
- model immutability and extra-field rejection;
- package-wide runtime-adapter source guard;
- root export preservation;
- P14.1 to P14.4 regression compatibility.

## Authority Decision

```yaml
P14_5_Authority:
  runtime_adapter_operational: false
  process_launch_composition_authorized: false
  executable_resolution_authorized: false
  argv_resolution_authorized: false
  parent_environment_read_authorized: false
  workspace_allocation_authorized_by_P14_5: false
  listener_discovery_authorized: false
  readiness_probe_authorized: false
  cancellation_authorized: false
  graceful_shutdown_authorized: false
  forced_shutdown_composition_authorized: false
  cleanup_authorized: false
  rollback_authorized: false
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
P14_5_DecisionMatrix:
  prerequisites:
    dynamic_start_commit_resolved: true
    HEAD_equals_origin_main: true
    P14_0_committed: true
    P14_1_committed: true
    P14_2_committed: true
    P14_3_committed: true
    P14_4_committed: true
    contract_schema_version: 1
    register_valid_at_start: true
    upstream_clean: true
    Graphify_frozen_integrity: true

  implementation:
    event_normalizer_created: true
    failure_normalizer_created: true
    audit_projection_created: true
    event_tests_created: true
    audit_tests_created: true
    dependencies_added: 0
    lockfiles_modified: 0
    existing_runtime_adapter_contract_files_modified: false
    root_exports_modified: false

  normalization:
    runtime_event_descriptor_coverage: all_RuntimeEventType_values
    sequence_journal_instance_local: true
    generated_event_ID_guarded: true
    generated_failure_ID_guarded: true
    evidence_reference_presence_guarded: true
    cross_runtime_reference_rejected: true
    failure_summaries_sanitized: true
    unsupported_errors_fail_closed: true
    unknown_error_codes_fail_closed: true

  audit_projection:
    non_authoritative: true
    persistence_authority: false
    publication_authority: false
    raw_process_reference_exposed: false
    raw_workspace_path_exposed: false
    readiness_detail_exposed: false
    log_body_exposed: false
    command_or_environment_exposed: false
    failure_event_reference_required: true
    duplicate_evidence_IDs_rejected: true

  validation:
    compile_check_passed: true
    Ruff_passed: true
    targeted_event_tests_passed: true
    targeted_audit_tests_passed: true
    contract_regression_passed: true
    P14_runtime_regression_passed: true
    source_guard_passed: true
    root_export_guard_passed: true

  final_state:
    new_product_files: 4
    modification_register_rows: 88
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
    P14_6_unlocked_after_human_commit: true
    P14_8_owns_live_Hermes_gate: true
    P15_unauthorized: true
    P17_unauthorized: true

  final_verdict: hermes_runtime_events_audit_normalization_ready
```

## Result Markers

```text
hermes_P14_5_prerequisite_gate_passed
hermes_P14_4_workspace_containment_committed
hermes_runtime_event_normalizer_created
hermes_runtime_event_descriptors_cover_all_event_types
hermes_runtime_event_sequence_journal_created
hermes_runtime_event_reference_guards_created
hermes_runtime_failure_normalizer_created
hermes_runtime_failure_codes_mapped
hermes_runtime_failure_evidence_refs_bounded
hermes_runtime_audit_projection_created
hermes_runtime_audit_projection_non_authoritative
hermes_runtime_audit_projection_excludes_raw_runtime_detail
hermes_runtime_audit_failure_reference_guarded
hermes_runtime_audit_evidence_ambiguity_rejected
hermes_runtime_events_audit_register_reconciled
hermes_runtime_events_audit_normalization_ready
no_runtime_adapter_operation
no_process_launch_composition
no_parent_environment_read
no_listener_discovery
no_readiness_probe
no_shutdown_workflow
no_runtime_rollback
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
