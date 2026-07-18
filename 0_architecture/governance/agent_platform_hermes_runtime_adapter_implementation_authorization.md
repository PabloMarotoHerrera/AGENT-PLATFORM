# P14.0 - Hermes Runtime Adapter Implementation Authorization

## Document Header

| Field | Value |
| --- | --- |
| Project | P14 - Governed Runtime Adapter |
| Ticket | P14.0 - Runtime Adapter Implementation Authorization |
| Date | 2026-07-18 |
| Status | `hermes_runtime_adapter_implementation_authorized_with_constraints` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_runtime_adapter_implementation_authorization.md` |
| Dynamic start commit | `ed5af2681ae842941aeb41e2d78fb83ba5fa4037` |
| Origin main at start | `ed5af2681ae842941aeb41e2d78fb83ba5fa4037` |
| Git mutation by agent | No staging, commit or push performed |

## Authorization Purpose

P14.0 authorizes the controlled implementation sequence for the governed Hermes
runtime adapter. It does not implement the adapter, create the runtime adapter
package, launch Hermes processes, add lifecycle controls to the UI, enable
providers, start workers or execute agents.

The binding authorization verdict is:

```text
hermes_runtime_adapter_implementation_authorized_with_constraints
```

This verdict means implementation may begin only through the governed P14.1 to
P14.R sequence. It does not mean that the adapter is implemented, integrated,
operational or production-ready.

## Prerequisite Gate

```yaml
P14_0_PrerequisiteGate:
  branch: main
  dynamic_start_commit: ed5af2681ae842941aeb41e2d78fb83ba5fa4037
  origin_main: ed5af2681ae842941aeb41e2d78fb83ba5fa4037
  HEAD_equals_origin_main: true
  git_index_empty: true
  tracked_working_tree_clean: true
  allowed_untracked_paths:
    - .opencode/
    - AGENTS.md
    - graphify-out/
  P13_R_committed: true
  P13_R_commit: aa91147b760fa1211ebd1f33dd0853d85083699a
  P13_residual_correction_committed: true
  P13_residual_correction_commit: ed5af2681ae842941aeb41e2d78fb83ba5fa4037
  P13_governance_closure_present: true
  P13_final_verdict: hermes_product_ui_foundation_closed_experimental_with_constraints
  product_UI_feature: experimental
  configured_extension_modules: 9
  compiled_descriptors: 9
  selected_descriptors: 9
  resolved_descriptors: 9
  runtime_product_routes: 9
  product_navigation_items: 5
  product_tracked_files: 6183
  modification_register_rows: 65
  modification_register_columns: 18
  modification_register_duplicate_ids: 0
  modification_register_duplicate_paths: 0
  modification_register_missing_fields: 0
  modification_register_hash_mismatches: 0
  provider_enabled: false
  gateway_started_by_P14_0: false
  worker_started_by_P14_0: false
  agent_started_by_P14_0: false
  locked_upstream_clean: true
  nested_product_git: false
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  graphify_frozen_integrity: true
```

The prerequisite gate passed. If any of these conditions fails in a later P14
ticket, that ticket must stop before implementation and report the exact
substantive blocker.

## Source Inspection Evidence

P14.0 used bounded read-only Graphify navigation and exact source inspection.
No Graphify update, extraction, clustering, export or refresh was performed.

Current canonical evidence inspected:

```text
0_architecture/governance/agent_platform_hermes_product_ui_foundation_closure.md
0_architecture/governance/agent_platform_hermes_frontend_quality_gate.md
2_products/hermes-agent/hermes_cli/agent_platform/product_config.py
2_products/hermes-agent/hermes_cli/agent_platform/routes.py
2_products/hermes-agent/hermes_cli/main.py
2_products/hermes-agent/hermes_cli/web_server.py
2_products/hermes-agent/hermes_cli/dashboard_auth/audit.py
2_products/hermes-agent/hermes_cli/console_engine.py
2_products/hermes-agent/web/src/agent-platform/extensions.ts
2_products/hermes-agent/web/src/agent-platform/*/descriptor*.ts
2_products/hermes-agent/web/src/agent-platform/frontend-quality/quality-contract.ts
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_product_config.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_product_routes.py
```

Relevant current facts:

- P13.R closed the Product UI Foundation as experimental with constraints.
- P13 residual correction committed the activation test and quality-contract
  residuals that the product register already referenced.
- Product configuration is a strict, frozen, credential-free Pydantic contract.
- The AGENT PLATFORM product configuration endpoint is protected and read-only.
- Current dashboard launch logic lives in `cmd_dashboard()` and `start_server()`.
- Dashboard readiness is surfaced through `HERMES_DASHBOARD_READY` and optional
  `HERMES_DESKTOP_READY_FILE` JSON.
- `/api/status` is the current dashboard liveness/status endpoint.
- The Files surface is governed by `HERMES_DASHBOARD_FILES_ROOT`, locked-root
  metadata, `can_change_path`, and outside-root HTTP 403 rejection.
- Existing audit conventions include secret-stripping JSONL dashboard-auth audit
  events under `$HERMES_HOME/logs`.
- Existing contract conventions prefer frozen dataclasses, explicit status/result
  values, strict Pydantic models, immutable TypeScript contracts and tests over
  raw untyped dictionaries.

## Authorized Architectural Role

The governed runtime adapter is authorized as the sole AGENT PLATFORM-owned
process-lifecycle boundary between governed orchestration and local Hermes
runtime processes.

Conceptual flow:

```text
governed caller
  -> typed lifecycle request
  -> governed runtime adapter
  -> fixed tracked runtime profile
  -> sanitized environment and contained workspace
  -> owned Hermes subprocess tree
  -> normalized bounded lifecycle events
  -> audit and rollback evidence
```

The adapter is infrastructure. It is not an autonomous agent, provider adapter,
worker, tool executor, shell interface, generic command runner, deployment
platform, workflow engine, project authority, approval authority or Git
authority.

Visible P13 UI, registered P13 routes and experimental activation do not imply
runtime authority. P13 read-only surfaces must remain read-only until a later
ticket explicitly authorizes UI lifecycle integration.

## Package Ownership Root

Future implementation is authorized only under:

```text
2_products/hermes-agent/hermes_cli/agent_platform/runtime_adapter/**
```

This package is owned by AGENT PLATFORM. P14.0 does not create it. P14.1 owns
the exact package and symbol design.

The adapter package must not be placed in immutable upstream, `web/**`, generic
Hermes core namespaces, upstream-oriented scripts, Graphify namespaces, future
G-Brain namespaces or future Paperclip namespaces.

Conceptual future modules may cover contracts, errors, profiles, process
ownership, environment sanitization, workspace containment, events, audit
normalization, cancellation, shutdown, rollback and adapter composition. These
names are not authorized as concrete files by P14.0.

## Caller Contract Restriction

The adapter must never expose arbitrary command execution.

Prohibited public request fields include raw command strings, raw shell scripts,
arbitrary argv, arbitrary executable paths, arbitrary environment mappings,
arbitrary working directories, arbitrary output paths, arbitrary signal names
and arbitrary kill commands.

Governed callers must request a tracked runtime profile by stable ID. Profile
resolution must determine the fixed executable strategy, fixed argument
construction, fixed environment policy, fixed workspace policy, fixed readiness
policy and fixed shutdown policy.

User-provided strings must never become executable commands. Future process
launch code must use explicit argument arrays and must not use `shell=True`.

## Runtime Profile Authority

Initial profile classes authorized by P14 are:

```text
test.lifecycle_probe
hermes.dashboard.experimental
```

`test.lifecycle_probe` is authorized for inert, repository-owned unit and
conformance test processes.

`hermes.dashboard.experimental` is authorized only for P14.8 and only for a
controlled local lifecycle integration gate.

P14 does not authorize provider-backed worker profiles, agent execution profiles,
tool-enabled profiles, MCP-enabled execution profiles, shell profiles,
Git-mutation profiles, browser automation runtime targets, deployment profiles,
remote-host profiles or container orchestration profiles.

Future worker and agent runtime profiles belong to P15 and P17 governance, not
P14.

## Live Execution Policy By Ticket

| Ticket | Authorized live/process behavior | Not authorized |
| --- | --- | --- |
| P14.0 | Documentation and authorization only | Runtime adapter package, process launch, environment creation, live lifecycle tests |
| P14.1 | Contracts and immutable data models only | Subprocess launch, live Hermes execution, provider logic, worker logic, UI controls |
| P14.2 | Process ownership implementation with inert controlled child-process tests | Live Hermes dashboard, provider or worker process, generic shell commands |
| P14.3 | Runtime profile and sanitized-environment construction | Live Hermes launch |
| P14.4 | Workspace and path containment; filesystem tests in temporary controlled roots | Real-user path access, live Hermes launch |
| P14.5 | Event and audit normalization with test doubles or inert process evidence | Parallel audit authority, live provider/worker/agent behavior |
| P14.6 | Cancellation, shutdown and rollback for owned inert process trees | Git cleanup, source deletion, user-data deletion |
| P14.7 | Adapter conformance tests with inert subprocesses and deterministic failures | Production provider, worker or agent execution |
| P14.8 | One isolated Hermes dashboard lifecycle gate with provider-null, worker-null and agent-null verification | Provider setup, gateway agent execution, worker start, agent start, Chat, tools, MCP calls, Git mutations |
| P14.R | Closure and final evidence | New implementation unless explicitly governed by a closure defect |

## Lifecycle State Model Requirements

P14.1 must formalize a deterministic state model preserving these semantics:

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

The final model may refine names, but it must provide an explicit transition
table, terminal-state identification, invalid-transition rejection, idempotent
stop and cancellation behavior, one active owner per runtime handle, bounded
readiness, bounded shutdown, bounded forced termination, monotonic event
sequence and failure-stage preservation.

The model must distinguish process launched from runtime ready, cancelled from
failed, and process stopped from workspace rollback completed.

## Process Ownership Policy

Every launched process tree must have exactly one explicit owner. Ownership
evidence must capture the adapter-generated runtime ID, launcher PID, listener
PID when discoverable, child-process tree, creation timestamp, profile ID,
workspace ID, stdout reference, stderr reference, readiness state, termination
state, exit code and cleanup state.

Mandatory rules:

- Never kill by process name.
- Never kill all Node, Python, Chrome or Hermes processes.
- Never assume launcher PID equals listener PID.
- Never terminate a PID not proven to belong to the runtime handle.
- Never reuse stale PID ownership evidence.
- Never wait for persistent process lifetime.

Preferred Windows strategy is owned process group or job-object semantics, exact
descendant discovery, graceful stop, bounded wait and exact-tree forced
termination only when required. Any fallback such as `taskkill` must target an
exact owned PID using an explicit argument array, be bounded, record its use and
verify the post-condition.

## Non-Blocking Runtime Protocol

Persistent process operations must follow this bounded protocol:

```text
resolve tracked profile
-> create isolated workspace
-> build sanitized environment
-> launch detached
-> capture ownership evidence
-> poll readiness with hard timeout
-> return a runtime handle
-> perform bounded checks
-> stop or cancel through the owner
-> verify listener cleanup
-> clean or retain workspace by explicit policy
-> emit normalized result
```

The adapter must not use unbounded `Wait-Process`, unbounded `communicate()`,
unbounded stdout/stderr reads, silent waiting, recursive polling without a
deadline, indefinite readiness or port checks, indefinite log tailing or tool
calls that wait for human interaction.

Human review must remain a two-phase handoff: automated work completes, retained
process ownership is explicitly declared, the tool call ends, human review
occurs, and a later request triggers exact cleanup. The adapter itself must not
block on human confirmation.

## Environment Sanitization Policy

P14.3 must define explicit environment construction. Child processes must not
inherit the entire parent environment by default.

Environment construction must be:

```text
minimal base allowlist
+ adapter-owned runtime paths
+ explicitly approved non-secret variables
```

Required isolated Windows and Hermes variables:

```text
HERMES_HOME
HOME
USERPROFILE
HOMEDRIVE
HOMEPATH
APPDATA
LOCALAPPDATA
TEMP
TMP
```

The adapter must verify that child `Path.home()` and `os.path.expanduser("~")`
equivalents do not resolve to the real Windows user profile. Effective runtime
state paths must resolve inside the owned workspace or an explicitly authorized
product path.

Credential-sensitive variables are denied during P14 unless introduced later by
P15. Denied inherited material includes provider API keys, cloud credentials,
Git credentials, SSH agent configuration, AWS credentials, Azure credentials,
OpenAI credentials, Anthropic credentials, Google provider credentials, MCP
secrets, database credentials and deployment tokens.

Evidence must report variable names and containment status, not secret values.
The full parent or child environment must not be logged.

## Workspace And Path Containment Policy

P14.4 must allocate one adapter-owned workspace per runtime instance. Conceptual
local integration root:

```text
9_artifacts/hermes/runtime-adapter/<runtime-id>/
```

P14.8 may use:

```text
9_artifacts/hermes/p14.8/<runtime-id>/
```

Contained areas may include `home/`, `appdata/`, `localappdata/`, `temp/`,
`logs/`, `files-root/`, `state/`, `evidence/` and `browser-profile/` only when
separately required by the integration gate.

Runtime IDs must be adapter-generated opaque identifiers. Callers must not
provide absolute workspace paths.

Containment must use canonical path resolution, ancestor verification, symlink
and junction awareness, reparse-point escape rejection, relative traversal
rejection, drive-change rejection, UNC-path rejection unless governed later,
case-insensitive Windows comparison and nonexistent-child validation against an
existing contained ancestor.

Prohibited runtime roots include `C:\Users\<real-user>`, the repository root,
immutable upstream, system temp without an adapter-owned subdirectory, OneDrive
root, arbitrary caller paths and network shares. The adapter must fail closed
when containment cannot be proven.

## Files-Root Containment Requirement

The P13.R Files isolation defect is binding regression evidence. Every Hermes
runtime profile capable of exposing a file API must bind an explicit managed
files root.

Required behavior:

```text
default file path == managed files root
locked_root == managed files root
can_change_path == false
outside-root request == HTTP 403 or equivalent governed rejection
```

No runtime lifecycle gate may expose the real user profile, repository root,
parent directories of the runtime workspace, provider credential directories,
SSH directories or cloud configuration directories through Files or equivalent
file surfaces.

## Runtime Event And Audit Normalization Policy

P14.5 must normalize lifecycle evidence into immutable, ordered, bounded,
serializable, secret-free, path-sanitized runtime events.

Minimum conceptual event fields:

```text
event_id
runtime_id
correlation_id
sequence
event_type
lifecycle_state
profile_id
timestamp_utc
monotonic_offset
stage
severity
message_code
sanitized_message
process_reference
workspace_reference
readiness_reference
failure_reference
```

Required event categories include request received/rejected, workspace created,
profile resolved, environment sanitized, process started, listener discovered,
readiness probe started, runtime ready, readiness timeout, cancellation
requested, graceful shutdown started, forced termination started, process exited,
listener released, workspace cleanup started/completed, rollback
started/completed and runtime failed.

Raw stdout and stderr must not become unbounded event payloads. Use bounded
references or bounded excerpts. Existing dashboard-auth audit patterns are
usable for secret stripping and JSONL audit shape, but P14 must not create a
parallel audit authority when surviving canonical audit/evidence contracts are
substantively compatible.

## Failure Model

The adapter must return typed failures rather than uncaught process-management
exceptions.

Minimum failure stages:

```text
request_validation
profile_resolution
environment_construction
workspace_creation
path_containment
process_launch
ownership_capture
listener_discovery
readiness
runtime_operation
cancellation
graceful_shutdown
forced_termination
workspace_cleanup
rollback
event_normalization
```

Failures must preserve runtime ID when allocated, profile ID, stage, failure
code, sanitized summary, retryability classification, cleanup status, process
status, workspace status and evidence references.

Failures must not contain credentials, complete environments, arbitrary file
contents, unbounded logs, real-user secret paths or shell command strings
derived from user input.

## Cancellation, Shutdown And Rollback

P14.6 must define cancellation, shutdown and rollback as separate operations.

Cancellation means the requested runtime activity should no longer continue. It
does not mean rollback has succeeded.

Shutdown means the owned process tree has been terminated and listeners have
been released. Required order is graceful request when supported, bounded wait,
exact owned-tree termination, bounded verification and listener-release
verification.

Rollback means adapter-owned temporary runtime effects have been reverted
according to policy. Rollback may include temporary workspace removal, temporary
runtime-state removal, temporary logs/evidence cleanup according to retention
policy, temporary browser-profile removal and port/listener verification.

Rollback must never include Git reset, Git restore, Git clean, Git checkout,
source-file deletion, user-data deletion, provider credential deletion or
arbitrary repository cleanup. Rollback failure must be reported explicitly and
must not be converted into a successful stop result.

## Authority Boundaries

P14 grants no authority for:

- Arbitrary command execution.
- Provider credential reads or writes.
- Provider or model selection.
- Inference.
- Worker startup.
- Agent startup.
- Agent tool execution.
- MCP execution.
- Git mutation.
- UI lifecycle controls.
- Runtime lifecycle configuration in P13 product configuration or Safe Settings.

Runtime profiles must not be selected by environment variable, arbitrary JSON,
dynamic import, plugin discovery or downloaded remote profile. Runtime profile
authority belongs inside the future runtime adapter package.

P14 does not authorize edits to `web/src/App.tsx`, `web/src/main.tsx` or
`web/src/agent-platform/**`. P13 Runtime Overview remains read-only.

P14 must not add dependencies in P14.0. Later P14 tickets must stop for explicit
review before adding process-management or sandboxing dependencies such as
`psutil`, `pywin32`, process supervisors, container SDKs, event-bus libraries or
filesystem sandbox libraries.

## Concurrency And Observability Boundaries

P14 contracts may prepare for multiple runtime handles, but P14.8 validates only
one controlled runtime instance. Initial behavior is one runtime handle, one
owning adapter instance, one workspace, one process tree and one lifecycle
operation at a time per handle.

Conflicting transitions must be rejected, including two simultaneous starts for
one handle, stop/cancel races without arbitration, workspace reuse by active
handles and duplicate ownership of one PID.

P14 must provide enough evidence to answer what was requested, which profile was
selected, which workspace was allocated, which process was launched, whether
readiness succeeded, which process tree was owned, why the runtime stopped,
whether cleanup succeeded and whether rollback succeeded. It must not introduce
Prometheus, OpenTelemetry infrastructure, external log aggregation, remote
tracing, a new database or an event broker.

## Ticket Authority Matrix

| Ticket | Expected verdict |
| --- | --- |
| P14.1 - Adapter Contract Package | `hermes_runtime_adapter_contract_package_ready` |
| P14.2 - Hermes Process Owner | `hermes_process_owner_ready` |
| P14.3 - Runtime Profile and Environment Sanitization | `hermes_runtime_profile_sanitization_ready` |
| P14.4 - Workspace and Path Containment | `hermes_runtime_workspace_containment_ready` |
| P14.5 - Runtime Events and Audit Normalization | `hermes_runtime_event_normalization_ready` |
| P14.6 - Cancellation, Shutdown and Rollback | `hermes_runtime_shutdown_rollback_ready` |
| P14.7 - Adapter Conformance Tests | `hermes_runtime_adapter_conformance_ready` |
| P14.8 - Controlled Lifecycle Integration Gate | `hermes_runtime_adapter_controlled_lifecycle_passed` |
| P14.R - Governed Runtime Adapter Closure | `hermes_governed_runtime_adapter_closed_with_constraints` |

## Stop Conditions

Future P14 work must stop if P13.R or the residual correction is not committed,
HEAD differs from `origin/main`, tracked files are dirty, the index is non-empty,
the modification register has any defect, product UI is not experimental,
activation counts differ from 9/9/9/9/5, immutable upstream is modified,
Graphify frozen hashes differ or current source contradicts a core P14 boundary.

P14.0 must also stop if it would require runtime adapter implementation, a new
Python package, product source modification, test modification, dependency or
lockfile change, dashboard launch, provider configuration, worker or agent
launch, Graphify regeneration or a second durable Markdown file.

## P14.1 Handoff

P14.1 is authorized to design and create the adapter contract package under
`hermes_cli/agent_platform/runtime_adapter`. It must implement contracts and
immutable data models only, with serialization and validation tests. It must not
launch subprocesses or Hermes, modify UI controls, add provider logic, add worker
logic or introduce dependencies without separate review.

P14.1 remains blocked until P14.0 is human-committed.

## Final Verdict

```yaml
P14_0_RuntimeAdapterImplementationAuthorizationVerdict:
  prerequisites:
    dynamic_start_commit_resolved: true
    HEAD_equals_origin_main: true
    P13_R_committed: true
    P13_residual_correction_committed: true
    tracked_working_tree_clean_at_start: true
    index_empty_at_start: true
    register_valid: true
    product_UI_experimental: true
    product_activation_counts: "9/9/9/9/5"
    upstream_clean: true
    Graphify_frozen_integrity: true

  authorization:
    runtime_adapter_implementation_authorized: true
    package_root: "hermes_cli/agent_platform/runtime_adapter"
    arbitrary_command_execution_authorized: false
    initial_test_profile_authorized: true
    experimental_dashboard_profile_authorized_for_P14_8_only: true
    provider_profiles_authorized: false
    worker_profiles_authorized: false
    agent_profiles_authorized: false

  implementation:
    adapter_package_created: false
    product_source_modified: false
    tests_modified: false
    dependencies_modified: false
    lockfiles_modified: false
    processes_started: false

  authority:
    provider_authorized: false
    inference_authorized: false
    worker_authorized: false
    agent_authorized: false
    tool_execution_authorized: false
    MCP_execution_authorized: false
    Git_authorized: false
    UI_lifecycle_controls_authorized: false

  deliverable:
    canonical_authorization_record_created: true
    additional_Markdown_created: false
    product_register_modified: false

  sequencing:
    P14_1_unlocked_after_human_commit: true
    P14_8_owns_live_Hermes_gate: true
    P15_remains_unauthorized: true
    P17_remains_unauthorized: true

  final_verdict: hermes_runtime_adapter_implementation_authorized_with_constraints
```

## Result Markers

```text
hermes_P14_0_prerequisite_gate_passed
hermes_P13_R_committed
hermes_P13_residual_correction_committed
hermes_P13_product_activation_preserved
hermes_runtime_adapter_architectural_role_defined
hermes_runtime_adapter_package_root_authorized
hermes_runtime_adapter_call_surface_restricted
hermes_runtime_profile_authority_defined
hermes_process_ownership_policy_defined
hermes_non_blocking_runtime_protocol_defined
hermes_environment_sanitization_policy_defined
hermes_workspace_containment_policy_defined
hermes_files_root_containment_required
hermes_runtime_event_policy_defined
hermes_runtime_failure_model_defined
hermes_runtime_cancellation_policy_defined
hermes_runtime_shutdown_policy_defined
hermes_runtime_rollback_policy_defined
hermes_runtime_git_authority_denied
hermes_runtime_provider_authority_denied
hermes_runtime_worker_authority_denied
hermes_runtime_agent_authority_denied
hermes_runtime_tool_authority_denied
hermes_runtime_UI_mutation_authority_denied
hermes_P14_8_live_gate_boundary_defined
hermes_P14_1_handoff_authorized
no_runtime_adapter_implementation
no_product_source_change
no_dependency_change
no_lockfile_change
no_process_launch
no_provider_activation
no_worker_start
no_agent_start
no_Graphify_regeneration
no_Graphify_modification
no_git_mutation_by_agent
```
