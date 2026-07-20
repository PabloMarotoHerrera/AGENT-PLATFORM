# P14.R - Governed Runtime Adapter Closure

## Verdict

```text
hermes_governed_runtime_adapter_closed_with_constraints
```

P14 is closed as an internal governed runtime-adapter foundation. It proves one
isolated loopback Hermes dashboard lifecycle under fixed profile, exact process
ownership, sanitized environment, contained workspace, bounded readiness,
governed shutdown and explicit rollback. It does not authorize general-purpose
runtime execution, provider activation, worker launch, agent launch, tool or MCP
execution, public lifecycle HTTP APIs, UI lifecycle controls, audit persistence,
event publication, deployment, or Git authority.

## Dynamic Start State

| Field | Value |
| --- | --- |
| Dynamic start SHA | `f3cd08cf9fb695b171af21f27c2c189b9a9dfd73` |
| `origin/main` at start | `f3cd08cf9fb695b171af21f27c2c189b9a9dfd73` |
| Branch | `main` |
| HEAD equals origin/main | `true` |
| Index empty at start | `true` |
| Tracked working tree clean at start | `true` |
| Allowed unrelated untracked paths | `.opencode/**`; `AGENTS.md`; `graphify-out/**` |
| Agent Git mutation | No staging, commit or push performed. |

## Accepted P14 Sequence

| Ticket | Canonical Governance Record | Accepted Verdict |
| --- | --- | --- |
| P14.0 | `agent_platform_hermes_runtime_adapter_implementation_authorization.md` | `hermes_runtime_adapter_implementation_authorized_with_constraints` |
| P14.1 | `agent_platform_hermes_runtime_adapter_contract_package.md` | `hermes_runtime_adapter_contract_package_ready` |
| P14.2 | `agent_platform_hermes_process_owner.md` | `hermes_process_owner_ready` |
| P14.3 | `agent_platform_hermes_runtime_profile_environment_sanitization.md` | `hermes_runtime_profile_environment_sanitization_ready` |
| P14.4 | `agent_platform_hermes_runtime_workspace_path_containment.md` | `hermes_runtime_workspace_containment_ready` |
| P14.5 | `agent_platform_hermes_runtime_events_audit_normalization.md` | `hermes_runtime_events_audit_normalization_ready` |
| P14.6 | `agent_platform_hermes_runtime_cancellation_shutdown_rollback.md` | `hermes_runtime_shutdown_rollback_ready` |
| P14.7 | `agent_platform_hermes_runtime_adapter_conformance.md` | `hermes_runtime_adapter_conformance_ready` |
| P14.8 | `agent_platform_hermes_runtime_adapter_controlled_lifecycle_gate.md` | `hermes_runtime_adapter_controlled_lifecycle_passed` |

The canonical P14.5 verdict uses the committed plural form
`hermes_runtime_events_audit_normalization_ready`; P14.R resolves prerequisites
through current canonical records rather than obsolete historical filename or
spelling identity.

## Architecture Inventory

The committed runtime-adapter package contains exactly 19 Python source files:

```text
hermes_cli/agent_platform/runtime_adapter/__init__.py
hermes_cli/agent_platform/runtime_adapter/enums.py
hermes_cli/agent_platform/runtime_adapter/errors.py
hermes_cli/agent_platform/runtime_adapter/contracts.py
hermes_cli/agent_platform/runtime_adapter/state_machine.py
hermes_cli/agent_platform/runtime_adapter/process_owner.py
hermes_cli/agent_platform/runtime_adapter/process_tree.py
hermes_cli/agent_platform/runtime_adapter/stream_capture.py
hermes_cli/agent_platform/runtime_adapter/profiles.py
hermes_cli/agent_platform/runtime_adapter/environment.py
hermes_cli/agent_platform/runtime_adapter/path_containment.py
hermes_cli/agent_platform/runtime_adapter/workspace.py
hermes_cli/agent_platform/runtime_adapter/event_normalization.py
hermes_cli/agent_platform/runtime_adapter/audit_normalization.py
hermes_cli/agent_platform/runtime_adapter/lifecycle_control.py
hermes_cli/agent_platform/runtime_adapter/rollback.py
hermes_cli/agent_platform/runtime_adapter/listener_discovery.py
hermes_cli/agent_platform/runtime_adapter/readiness.py
hermes_cli/agent_platform/runtime_adapter/adapter.py
```

| Component | Closure Posture |
| --- | --- |
| Contract package | Schema-versioned immutable request, handle, process, readiness, event, failure and operation-result contracts. |
| Process owner | One owner per runtime ID, exact launcher/descendant/listener ownership, bounded stream drains, graceful stop and exact-tree forced fallback. |
| Profile registry | Exactly `test.lifecycle_probe` and `hermes.dashboard.experimental`; no provider, worker or agent profile. |
| Environment sanitizer | Explicit source mapping only; parent environment copy denied; managed HOME/USERPROFILE/HERMES_HOME/APPDATA/LOCALAPPDATA/TEMP/TMP/TMPDIR. |
| Workspace allocator | Internally generated workspace IDs, trusted base root, exclusive marker-owned layout and managed Files-root binding. |
| Path containment | Component containment, Windows case-insensitive behavior, POSIX case-sensitive behavior, symlink/reparse/UNC/device escape rejection. |
| Event normalizer | 20 fixed event descriptors, generated event IDs, state compatibility, typed references and bounded failures. |
| Audit projection | Non-authoritative in-memory projection only; no audit file, event spool, database, broker or telemetry. |
| Termination coordinator | Cancellation and shutdown remain distinct from failure and rollback; release requires verified process exit and stream drain. |
| Rollback coordinator | Explicit rollback only; marker verification, tree preflight, redirect/special-file rejection and exact contained deletion. |
| Listener discovery | Exact owned loopback listener proof only. |
| Readiness probe | Seven fixed dashboard checks with bounded scalar evidence only. |
| GovernedRuntimeAdapter | Internal composition boundary for one controlled dashboard lifecycle. |
| Lifecycle runner | Stdout-only gate over the committed adapter; no result JSON or durable audit/event persistence. |

## Contract And State Closure

| Field | Value |
| --- | --- |
| `RUNTIME_ADAPTER_CONTRACT_SCHEMA_VERSION` | `1` |
| Lifecycle state count | `13` |
| Lifecycle action count | `12` |
| Operational root exports public | `false` |

Lifecycle states:

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

Lifecycle actions:

```text
validate
start
wait_for_readiness
mark_ready
request_cancellation
begin_stop
mark_stopped
mark_cancelled
mark_failed
begin_rollback
mark_rolled_back
mark_rollback_failed
```

The state machine remains fail-closed for invalid transitions. Stop and
cancellation are idempotent only where defined. Rollback remains distinct from
stop, failed remains distinct from cancelled, and process-ready remains distinct
from process-started.

## Profile And Environment Closure

| Profile ID | Scope | Purpose |
| --- | --- | --- |
| `test.lifecycle_probe` | `inert_test_only` | P14 inert conformance probe only. |
| `hermes.dashboard.experimental` | `p14_8_only` | One controlled live dashboard lifecycle. |

The environment boundary excludes provider variables, proxy variables, Git/SSH
variables, MCP variables, Python path/home injection and dynamic-loader injection.
`PATH` is explicit-only. No provider or worker profile exists.

## Workspace And Files-Root Closure

| Workspace Policy | Purpose |
| --- | --- |
| `runtime.workspace.test.lifecycle_probe.v1` | Pytest-owned inert conformance workspaces. |
| `runtime.workspace.hermes.dashboard.experimental.v1` | Adapter-owned dashboard workspace with locked Files root. |

Dashboard Files-root live evidence proves `default_path == locked_root`,
`can_change_path == false`, and a synthetic gate-local outside candidate is
rejected with HTTP `403`. Rollback performs no Git operations and no recursive
broad deletion outside a verified owned workspace root.

## Event And Audit Closure

| Field | Value |
| --- | --- |
| Runtime event descriptor count | `20` |
| Event IDs | Internally generated. |
| Ordering | Monotonic sequence with nondecreasing timestamps. |
| Raw stdout/stderr in events | `false` |
| Raw exception text in failures | `false` |
| Environment values in events/audit | `false` |
| Host paths in events/audit | `false` |
| Audit persistence | `false` |

Audit remains projection-only, in memory, non-authoritative and derived from the
event stream. It preserves runtime subject and correlation while avoiding a
second audit authority.

## Cancellation, Shutdown And Rollback Closure

P14 preserves these separations:

```text
cancellation != failure
shutdown != rollback
process termination != workspace deletion
rollback requires explicit request
```

Successful shutdown requires graceful stop where supported, exact-tree forced
fallback when needed, launcher/listener/descendant absence, process reaping,
complete stream drains and owner release. Successful rollback requires owner
release, marker verification, complete tree preflight, redirect and special-file
rejection, contained workspace deletion, allocator release and absent workspace
root.

## Conformance Closure

P14.7 conformance remains exactly 24 fixed cases covering contracts, profiles,
environment, workspace, path containment, process ownership, stream capture,

The P14.8-FQ-TEST-001 Windows bounded-wait correction is test-only:

```text
15-second hard maximum
monotonic deadline
bounded polling
diagnostic-preserving
non-authority-expanding
```

## Controlled Live Lifecycle Evidence

The committed lifecycle gate was run once for P14.R from the repository root:

```text
.
\2_products\hermes-agent\.venv\Scripts\python.exe
10_scripts\hermes\agent_platform_runtime_adapter_lifecycle_gate.py
--repository-root "."
--port 9130
```

| Field | Value |
| --- | --- |
| Exit code | `0` |
| Verdict | `hermes_runtime_adapter_controlled_lifecycle_passed` |
| Profile | `hermes.dashboard.experimental` |
| Host | `127.0.0.1` |
| Port | `9130` |
| Product-local interpreter | `true` |
| Readiness check count | `7` |
| Event count | `15` |
| In-memory audit projection count | `15` |
| Launch outcome | `ready` |
| Shutdown outcome | `stopped` |
| Rollback outcome | `rolled_back` |
| Final lifecycle interpretation | `rolled_back` |
| Gate status | `passed` |
| Duration | `8.063000000000102 seconds` |

Seven readiness checks, in order:

| Check ID | Status | Required Evidence |
| --- | ---: | --- |
| `dashboard.root` | `200` | Production assets present; no Vite dev marker; no Vite overlay marker; no external redirect. |
| `dashboard.status` | `200` | `gateway_running=false`; active agents `0`; active sessions `0`; provider count `0`. |
| `dashboard.product_config_unauthenticated` | `401` | Product configuration denied without the session token. |
| `dashboard.product_config_authenticated` | `200` | Product UI `experimental`; extension module count `9`; exact module order valid. |
| `dashboard.plugin_manifest` | `200` | Manifest valid; protected product-route conflict count `0`. |
| `dashboard.files_root` | `200` | Default path and locked root equal the managed root; path change disabled. |
| `dashboard.files_outside_root` | `403` | Synthetic gate-local outside candidate denied. |

Exact product module order:

```text
agent_platform.ui.overview
agent_platform.ui.projects
agent_platform.ui.project_detail
agent_platform.ui.ticket_detail
agent_platform.ui.approvals
agent_platform.ui.approval_detail
agent_platform.ui.executions
agent_platform.ui.execution_detail
agent_platform.ui.settings
```

## Validation Evidence

| Check | Result |
| --- | --- |
| Complete P14 regression | `148 passed`, `0 skipped`, `0 failed`, `19.22s` |
| Adjacent product config/routes regression | `16 passed`, `0 skipped`, `0 failed`, `1.05s` |
| Lifecycle-gate runner tests | `11 passed`, `0 skipped`, `0 failed`, `0.07s` |
| Internal adapter import | `GovernedRuntimeAdapter` |
| Listener/readiness import | `RuntimeListenerDiscovery RuntimeDashboardReadinessProbe` |
| Root export guard | `contract-only-root` |
| Product compileall | `passed` |
| Runner compileall | `passed` |
| Ruff check, product scope | `passed` |
| Ruff check, runner scope | `passed` |
| Ruff format check, product scope | `36 files already formatted` |
| Ruff format check, runner scope | `2 files already formatted` |
| Full Windows-footgun scanner | `passed: 774 file(s) scanned` |
| Dashboard production build | `passed`; inherited Vite chunk-size warning only. |

## Zero-Residue Evidence

Pre-live gate:

| Check | Count |
| --- | ---: |
| Port 9130 listeners | `0` |
| Attributable P14 gate/dashboard/probe processes | `0` |
| P14.8 artifact/gate roots | `0` |
| P14.8 result JSON files | `0` |
| Browser processes attributable to P14 | `0` |
| DevTools listeners attributable to P14 | `0` |

Post-live gate:

| Check | Count |
| --- | ---: |
| Port 9130 listeners | `0` |
| Owned runtime IDs | `0` |
| P14 dashboard processes | `0` |
| Lifecycle probe processes | `0` |
| P14 workspaces | `0` |
| Ownership markers beneath P14.8 | `0` |
| Non-empty P14 gate roots | `0` |
| P14 result JSON files | `0` |
| Audit files | `0` |
| Event spools | `0` |
| Database files | `0` |
| Persistent runtime logs | `0` |
| Browser processes attributable to P14 | `0` |
| DevTools listeners attributable to P14 | `0` |
| Temporary virtual environments attributable to P14.8 | `0` |

No live dashboard was retained. No browser was launched by P14.R.

## Register And Product Inventory

| Field | Value |
| --- | ---: |
| Product tracked files at start | `6219` |
| New product files from P14.R | `0` |
| Product tracked files after validation | `6219` |
| Modification-register rows | `101` |
| Modification-register columns | `18` |
| Duplicate modification IDs | `0` |
| Duplicate product paths | `0` |
| Missing fields | `0` |
| Hash mismatches | `0` |

Verified P14.8 register rows:

```text
P14.8-001 hermes_cli/agent_platform/runtime_adapter/listener_discovery.py
P14.8-002 hermes_cli/agent_platform/runtime_adapter/readiness.py
P14.8-003 hermes_cli/agent_platform/runtime_adapter/adapter.py
P14.8-004 tests/hermes_cli/test_agent_platform_runtime_listener_discovery.py
P14.8-005 tests/hermes_cli/test_agent_platform_runtime_readiness.py
P14.8-006 tests/hermes_cli/test_agent_platform_runtime_adapter_integration.py
```

Verified conditional correction rows:

```text
P14.1-006 tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py
P14.6-004 tests/hermes_cli/test_agent_platform_runtime_rollback.py
P14.7-001 tests/hermes_cli/runtime_adapter_conformance_harness.py
```

P14.R does not modify `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv`.

## Upstream And Graphify Integrity

| Boundary | Result |
| --- | --- |
| Immutable upstream path | `4_external/sources/hermes-agent` |
| Locked upstream commit | `9de9c25f620ff7f1ce0fd5457d596052d5159596` |
| Locked upstream tracked diff | `clean` |
| Nested product Git directory | `absent` |
| Candidate checkout | `absent` |
| Synchronization workspace | `absent` |
| Graphify process during P14.R | `not run` |
| Graphify regeneration | `false` |
| `graphify-out/graph.json` SHA-256 | `02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2` |
| `graphify-out/provenance.json` SHA-256 | `952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550` |

## Authority Denials

```yaml
arbitrary_command_authority: false
arbitrary_argv_authority: false
arbitrary_environment_authority: false
arbitrary_workspace_path_authority: false
provider_credentials_authorized: false
provider_inference_authorized: false
worker_launch_authorized: false
agent_launch_authorized: false
tool_execution_authorized: false
MCP_execution_authorized: false
WorkPacket_execution_authorized: false
gateway_lifecycle_authorized: false
Chat_lifecycle_authorized: false
public_runtime_HTTP_API_authorized: false
runtime_UI_controls_authorized: false
audit_persistence_authorized: false
event_publication_authorized: false
Git_authority: false
deployment_authority: false
```

## Known Constraints

```text
runtime adapter remains internal
only one controlled dashboard runtime validated
only loopback local execution validated
only Windows and available POSIX test paths covered
provider-null only
no worker runtime
no agent runtime
no tool execution
no MCP execution
no public lifecycle API
no lifecycle UI controls
no durable audit persistence
no remote host
no container runtime
no production deployment
```

The adapter is ready as infrastructure for P15. It is not ready as a
general-purpose runtime service.

## P15 Handoff

P15 may use the P14 governed runtime adapter as infrastructure only after the
human commits this P14.R closure record.

Required P15 sequence:

```text
P15.0 Provider and Model Strategy
P15.1 Credential Delivery Boundary
P15.2 Provider Runtime Profile
P15.3 Bounded Worker Profile
P15.4 Tool-Free Inference Gate
P15.5 Usage, Cost and Timeout Accounting
P15.6 Provider Failure and Retry Policy
P15.7 Single Worker Controlled Gate
P15.R Secure Worker Enablement Closure
```

Provider credential delivery remains unauthorized until P15.1. Worker launch
remains unauthorized until the relevant P15 gate. P15 must not reuse
`hermes.dashboard.experimental` as a provider or worker profile.

## P17 Boundary

P14.R does not unlock WorkPacket execution. Repository command execution,
validation-command execution, tool permission profiles, ticket execution, diff
production, artifact production and Git handoff automation remain reserved for
P17 - Governed WorkPacket Execution MVP.

## Result Markers

```text
hermes_P14_R_prerequisite_gate_passed
hermes_P14_sequence_accepted
hermes_P14_0_authorization_committed
hermes_P14_1_contract_package_committed
hermes_P14_2_process_owner_committed
hermes_P14_3_profile_sanitization_committed
hermes_P14_4_workspace_containment_committed
hermes_P14_5_event_audit_normalization_committed
hermes_P14_6_shutdown_rollback_committed
hermes_P14_7_conformance_committed
hermes_P14_8_controlled_lifecycle_committed
hermes_runtime_adapter_contract_schema_1
hermes_runtime_adapter_process_owner_closed
hermes_runtime_adapter_profile_registry_closed
hermes_runtime_adapter_environment_sanitization_closed
hermes_runtime_adapter_workspace_containment_closed
hermes_runtime_adapter_event_normalization_closed
hermes_runtime_adapter_audit_projection_closed
hermes_runtime_adapter_shutdown_closed
hermes_runtime_adapter_rollback_closed
hermes_runtime_adapter_conformance_24_cases
hermes_runtime_adapter_seven_readiness_checks_passed
hermes_runtime_adapter_event_count_15
hermes_runtime_adapter_audit_projection_count_15
hermes_runtime_adapter_shutdown_stopped
hermes_runtime_adapter_rollback_rolled_back
hermes_runtime_adapter_zero_residue
hermes_runtime_adapter_register_reconciled
hermes_governed_runtime_adapter_closed_with_constraints
no_arbitrary_command_authority
no_parent_environment_copy
no_real_user_state
no_gateway_start
no_provider_activation
no_worker_start
no_agent_start
no_tool_execution
no_MCP_execution
no_public_runtime_HTTP_API
no_runtime_UI_controls
no_audit_persistence
no_dependency_change
no_lockfile_change
no_frontend_change
no_backend_route_change
no_Graphify_regeneration
no_Graphify_modification
no_git_mutation_by_agent
```

## Final State Expected For Human Commit

```yaml
P14_R_GovernedRuntimeAdapterClosureVerdict:
  prerequisites:
    dynamic_start_commit_resolved: true
    HEAD_equals_origin_main: true
    P14_0_through_P14_8_committed: true
    contract_schema_version: 1
    register_valid_at_start: true
    product_inventory_valid: true
    upstream_clean: true
    Graphify_frozen_integrity: true
  architecture:
    contract_package_ready: true
    process_owner_ready: true
    profile_registry_ready: true
    environment_sanitizer_ready: true
    workspace_allocator_ready: true
    path_containment_ready: true
    event_normalizer_ready: true
    audit_projection_ready: true
    termination_coordinator_ready: true
    rollback_coordinator_ready: true
    listener_discovery_ready: true
    readiness_probe_ready: true
    governed_adapter_ready: true
    lifecycle_runner_ready: true
  contracts:
    schema_version: 1
    lifecycle_state_count: 13
    lifecycle_action_count: 12
    operational_root_exports_public: false
    arbitrary_command_authority: false
  conformance:
    inert_case_count: 24
    complete_P14_regression_passed: true
    adjacent_product_regression_passed: true
    runner_tests_passed: true
    import_guards_passed: true
    compile_check_passed: true
    Ruff_passed: true
    Windows_footgun_scan_passed: true
    dashboard_build_passed: true
  live_gate:
    profile: hermes.dashboard.experimental
    interpreter_product_local: true
    loopback_only: true
    readiness_check_count: 7
    root_200: true
    status_200: true
    gateway_running: false
    active_agents: 0
    active_sessions: 0
    provider_count: 0
    unauthenticated_config_401: true
    authenticated_config_200: true
    product_UI_experimental: true
    extension_modules_9_exact_order: true
    plugin_manifest_valid: true
    plugin_route_conflicts: 0
    Files_root_locked: true
    outside_Files_root_403: true
    event_count: 15
    audit_projection_count: 15
    launch_state: ready
    shutdown_state: stopped
    rollback_state: rolled_back
  cleanup:
    port_free: true
    process_ownership_released: true
    workspaces_removed: true
    gate_roots_removed: true
    result_JSON_absent: true
    audit_files_absent: true
    event_spools_absent: true
    databases_absent: true
    persistent_logs_absent: true
    browsers_absent: true
  authority:
    provider_authorized: false
    inference_authorized: false
    worker_authorized: false
    agent_authorized: false
    tool_authorized: false
    MCP_authorized: false
    WorkPacket_execution_authorized: false
    public_HTTP_lifecycle_API_authorized: false
    UI_lifecycle_controls_authorized: false
    audit_persistence_authorized: false
    Git_authorized: false
  final_state:
    product_tracked_files: 6219
    modification_register_rows: 101
    tracked_candidate_count: 1
    staged_files: 0
    commits_by_agent: 0
    pushes_by_agent: 0
  sequencing:
    P14_closed_after_human_commit: true
    P15_0_unlocked_after_human_commit: true
    P15_1_owns_credential_delivery_authority: true
    P15_worker_gate_required: true
    P17_WorkPacket_execution_remains_unauthorized: true
  final_verdict: hermes_governed_runtime_adapter_closed_with_constraints
```
