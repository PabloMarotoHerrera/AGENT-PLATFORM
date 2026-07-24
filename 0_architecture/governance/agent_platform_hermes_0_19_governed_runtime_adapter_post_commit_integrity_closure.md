# P15.M7R - Governed Runtime Adapter Post-Commit Integrity Closure

Status: P15.M7R post-commit governed runtime adapter integrity closed with constraints.

Final verdict: `hermes_0_19_governed_runtime_adapter_post_commit_integrity_closed_with_constraints`

## Authority

P15.M7R closes the post-commit integrity transition created by P15.M7. The
P15.M7 commit is accepted, committed and published. P15.M7R modifies only the
self-excluded Pepper baseline record and creates this closure record.

No runtime implementation, runtime tests, modification register, application
manifest, product configuration, web server, frontend, package manifest,
lockfile, Desktop, Workspace, provider, credential, worker or Graphify output
is modified by P15.M7R.

## Repository Gate

| Check | Result |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `5d680f46efdfc7c66fe1e74534322b662cc29580` |
| origin/p15.m-hermes-0.19-migration | `5d680f46efdfc7c66fe1e74534322b662cc29580` |
| HEAD equals remote | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Worktree clean at start | `true` |
| Visible untracked candidates at start | `0` |

## Prerequisites

| Record | Verdict | State |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_governed_runtime_adapter_closure.md` | `hermes_governed_runtime_adapter_closed_with_constraints` | tracked, committed, locally unmodified |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` | `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints` | tracked, committed, locally unmodified |
| `0_architecture/governance/agent_platform_hermes_0_19_governed_runtime_adapter_application.md` | `hermes_0_19_governed_runtime_adapter_application_ready_with_constraints` | tracked, committed, locally unmodified |
| `0_architecture/governance/agent_platform_hermes_0_19_runtime_adapter_application_manifest.tsv` | `not_applicable` | tracked, committed, locally unmodified |

Product identity remains `pepper`, display name `Pepper`, version
`0.1.0-dev`, upstream `Hermes Agent` `0.19.0`, upstream commit
`3ef6bbd201263d354fd83ec55b3c306ded2eb72a`, product UI `disabled`, extension
module count `0`.

## Resolved P15.M7 Commit

| Field | Value |
| --- | --- |
| P15.M7 commit | `5d680f46efdfc7c66fe1e74534322b662cc29580` |
| Commit message | `P15.M7 Apply governed runtime adapter to Pepper` |
| Commit is ancestor of HEAD | `true` |
| HEAD equals P15.M7 commit | `true` |
| Post-P15.M7 commits | `0` |
| Post-P15.M7 product mutation commits | `0` |
| P15.M7 committed files | `39` |
| Runtime source files | `19` |
| Runtime test, harness and inert-probe files | `17` |
| Register control files | `1` |
| Governance files | `2` |
| Missing expected files | `0` |
| Unexpected files | `0` |

The P15.M7 file set contains no frontend, web server, product configuration,
package manifest, lockfile, Desktop, Workspace, provider, credential, worker or
P13 page changes.

## Modification Register

The corrected P15.M7R authority is the committed mapping in
`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` reconciled with
`0_architecture/governance/agent_platform_hermes_0_19_runtime_adapter_application_manifest.tsv`.
The committed order is the P14 authority application sequence, not a
lexicographic product-path sequence.

| Check | Result |
| --- | ---: |
| Register rows | `58` |
| Register columns | `18` |
| Rows before P15.M7 | `22` |
| P15.M7 rows | `36` |
| Required P15.M7 IDs present exactly once | `36` |
| Duplicate modification IDs | `0` |
| Duplicate product paths | `0` |
| Duplicate P15.M7 paths | `0` |
| Blank mandatory fields | `0` |
| Invalid classifications | `0` |
| Missing committed product blobs | `0` |
| HEAD blob hash mismatches | `0` |
| Register rows without committed P15.M7 product file | `0` |
| Committed P15.M7 product files without register row | `0` |
| Register SHA-256 | `c7d3f6b114a071468b6e3523f8edb7256ef64838aa8193e29a96dbc5472254d1` |

## Application Manifest

| Check | Result |
| --- | --- |
| Path | `0_architecture/governance/agent_platform_hermes_0_19_runtime_adapter_application_manifest.tsv` |
| Rows | `36` |
| Columns | `19` |
| Bytes | `39142` |
| SHA-256 | `539aa878ed3fa4d3a5dcea4eb00d8fba9ea5ee33893ba03d482402f6589b6518` |
| Duplicate record IDs | `0` |
| Duplicate product paths | `0` |
| Blank mandatory fields | `0` |
| Manifest IDs missing from register | `0` |
| Register IDs missing from manifest | `0` |
| Register-manifest ID mismatches | `0` |
| Register-manifest path mismatches | `0` |
| Register-manifest hash mismatches | `0` |
| Unverified records | `0` |
| Runtime source coverage | `19` |
| Test, harness and inert-probe coverage | `17` |
| Manifest hash recorded in P15.M7 governance | `true` |

P14 provenance validation:

| Check | Result |
| --- | ---: |
| P14 runtime authority records | `36` |
| Missing P14 authority records | `0` |
| Missing P14 source paths | `0` |
| P14 authority source hash mismatches | `0` against referenced P14 authority file bytes |
| Duplicate P14 authority record IDs | `0` |
| Unexplained authority ordering | `0` |
| Ordering classification | `P14_authority_application_sequence` |

## Runtime Adapter Contract

| Check | Result |
| --- | --- |
| Package path | `2_products/pepper-agent/hermes_cli/agent_platform/runtime_adapter` |
| Source modules | `19` |
| Contract schema version | `1` |
| Contract-only root | `true` |
| Operational root exports | `false` |
| Process owner exported from root | `false` |
| Workspace allocator exported from root | `false` |
| Environment sanitizer exported from root | `false` |
| Readiness implementation exported from root | `false` |
| Rollback implementation exported from root | `false` |
| Prohibited request fields present | `0` |
| Lifecycle states | `13` |
| Lifecycle actions | `12` |
| Event descriptors | `20` |
| Readiness descriptors | `7` |

Root exports are limited to the contract version, profile constants, immutable
contract models, stable enums, bounded contract errors and pure state-machine
helpers.

## Profiles

| Field | Value |
| --- | --- |
| Profile count | `2` |
| Active profile IDs | `test.lifecycle_probe`, `pepper.dashboard.provider_null` |
| `hermes.dashboard.experimental` active | `false` |
| Provider profiles | `0` |
| Worker profiles | `0` |
| Agent profiles | `0` |
| Dynamic profile discovery | `false` |
| Unknown profile rejected | `true` |
| Registry immutable | `true` |
| Ordering | deterministic P14 authority application sequence |

`test.lifecycle_probe` remains inert test-only: no network, provider,
credential, worker, agent, tool or MCP authority.

`pepper.dashboard.provider_null` remains later controlled-lifecycle-only:
loopback-only readiness expectations, provider activation `false`, credential
access `false`, worker launch `false`, agent launch `false`, tool execution
`false`, MCP execution `false`, product ID `pepper`, product UI `disabled`, and
extension module count `0`.

## Process, Environment And Workspace

Validated boundaries:

| Boundary | Result |
| --- | --- |
| One owner per runtime ID | `true` |
| Launcher PID owned | `true` |
| Descendant tree owned | `true` |
| Listener ownership required | `true` |
| Foreign listener rejected | `true` |
| Foreign descendant rejected | `true` |
| Stdout drain bounded | `true` |
| Stderr drain bounded | `true` |
| Graceful stop before forced fallback | `true` |
| Exact tree forced fallback | `true` |
| Verified exit before release | `true` |
| Stream drain before release | `true` |
| Process-name kill | `false` |
| Broad port kill | `false` |
| Foreign PID termination | `false` |
| Shell execution authority | `false` |
| PID exposure to UI | `false` |

Environment sanitizer posture:

| Boundary | Result |
| --- | --- |
| Reads `os.environ` directly | `false` |
| Parent environment merge | `false` |
| PATH inheritance | `false` |
| dotenv loading | `false` |
| User home discovery | `false` |
| Allowed Windows bootstrap inheritance | `SystemRoot`, `WINDIR` only |
| Managed variables | `HERMES_HOME`, `HOME`, `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, `TEMP`, `TMP`, `TMPDIR`, `HOMEDRIVE`, `HOMEPATH` |
| Variable values in reports | `false` |
| Secret fragments in reports | `false` |
| Host paths in reports | `false` |
| Provider variables emitted | `0` |
| OAuth variables emitted | `0` |
| Credential variables emitted | `0` |

Workspace and path containment posture:

| Boundary | Result |
| --- | --- |
| Generated workspace ID | `true` |
| Trusted base root | `true` |
| Exclusive ownership marker | `true` |
| Managed `HERMES_HOME` | `true` |
| Managed Files root | `true` |
| Default Files root locked | `true` |
| Path change enabled | `false` |
| Shared writable `HERMES_HOME` | `false` |
| Windows case-insensitive behavior | `true` |
| POSIX case-sensitive behavior | `true` |
| Symlink and reparse escapes rejected | `true` |
| UNC, device, traversal and outside absolute paths rejected | `true` |
| Credential directory access | `false` |
| Host root access | `false` |
| Docker socket access | `false` |

Rollback deletion is owned-root-only, marker-verified, complete-tree-preflighted,
redirect-free, special-file-free and contained. Git rollback actions remain `0`.

## Lifecycle, Events And Audit

Lifecycle states: `created`, `validating`, `starting`,
`waiting_for_readiness`, `ready`, `cancellation_requested`, `stopping`,
`stopped`, `cancelled`, `failed`, `rollback_pending`, `rolled_back`,
`rollback_failed`.

Lifecycle actions: `validate`, `start`, `wait_for_readiness`, `mark_ready`,
`request_cancellation`, `begin_stop`, `mark_stopped`, `mark_cancelled`,
`mark_failed`, `begin_rollback`, `mark_rolled_back`,
`mark_rollback_failed`.

Invalid transitions are rejected. Cancellation remains distinct from failure,
shutdown remains distinct from rollback, stopped remains distinct from
cancelled, started remains distinct from ready, and rollback requires an
explicit request.

Event normalization uses generated event IDs, monotonic sequence validation,
nondecreasing timestamps, state compatibility validation, typed references and
bounded failure classification. Events contain no raw stdout, raw stderr, raw
exception text, environment values, credential values, host paths, provider
payloads or model payloads.

Audit remains projection-only, in-memory and non-authoritative. Persistent
files, database writes, event spools, brokers and telemetry export are absent.

## Readiness Descriptors

Descriptor count: `7`.

Descriptors: `dashboard.root`, `dashboard.status`,
`dashboard.product_config_unauthenticated`,
`dashboard.product_config_authenticated`, `dashboard.plugin_manifest`,
`dashboard.files_root`, `dashboard.files_outside_root`.

Static expectations remain: root HTTP `200` with production assets and no Vite
markers or external redirect; status HTTP `200`, gateway `false`, active agents
`0`, active sessions `0`, provider count `0`; unauthenticated product config
HTTP `401`; authenticated product config HTTP `200`, product ID `pepper`,
display name `Pepper`, version `0.1.0-dev`, upstream version `0.19.0`, product
UI `disabled`, extension modules `0`; plugin manifest HTTP `200`, protected
route conflicts `0`, product descriptors `0`; files root HTTP `200`, default
root equals managed root, path change `false`; outside root HTTP `403`.

No live Pepper dashboard was started. First controlled live candidate dashboard
lifecycle remains owned by P15.M9.

## Public Authority Denials

```yaml
public_lifecycle_HTTP_routes: 0
product_UI_lifecycle_controls: 0
CLI_lifecycle_controls: 0
TUI_lifecycle_controls: 0
Desktop_lifecycle_controls: 0
Workspace_lifecycle_controls: 0
provider_activation: false
credential_access: false
OAuth_execution: false
worker_launch: false
agent_launch: false
tool_execution: false
MCP_execution: false
arbitrary_process_launch: false
terminal_or_PTY: false
public_remote_bind: false
live_dashboard_launch: false
```

The adapter remains internal to `hermes_cli.agent_platform.runtime_adapter`.

## Validation Results

| Lane | Result |
| --- | --- |
| Runtime-adapter tests | `143 passed, 5 skipped, 0 failed, 0 errors` |
| Governance integrity tests | `Ran 14 tests`, `OK` |
| Syntax validation | `36` Python files, `0` syntax errors |
| Contract root import | `passed` |
| Profile registry import | `passed` |
| Event descriptor import | `passed` |
| Readiness descriptor import | `passed` |
| Inert lifecycle probe | `passed` |
| New external runtime dependencies | `0` |
| New external test dependencies | `0` |
| Undeclared imports | `0` |
| Package manifest changes | `0` |
| Lockfile changes | `0` |
| Registry queries | `0` |
| Dependency installations | `0` |

Skipped runtime tests:

| Test ID | Reason | Classification |
| --- | --- | --- |
| `test_agent_platform_runtime_path_containment.py::test_trusted_base_root_rejects_symlink_and_reparse_point` | `host does not allow directory symlink creation` | platform/environment-specific symlink privilege |
| `test_agent_platform_runtime_path_containment.py::test_symlink_redirect_rejected_even_when_target_is_inside_root` | `host does not allow directory symlink creation` | platform/environment-specific symlink privilege |
| `test_agent_platform_runtime_rollback.py::test_oversized_and_symlink_marker_are_rejected_without_deleting` | `symlink creation unavailable` | platform/environment-specific symlink privilege |
| `test_agent_platform_runtime_rollback.py::test_safe_preflight_rejects_redirects_special_files_depth_and_entry_bounds` | `symlink creation unavailable` | platform/environment-specific symlink privilege |
| `test_agent_platform_runtime_workspace.py::test_workspace_paths_are_contained_and_symlink_workspace_root_rejected` | `host does not allow directory symlink creation` | platform/environment-specific symlink privilege |

Unexpected skips: `0`. Skips hiding contract, profile, environment,
containment or process-ownership failure: `0`.

Inert probe evidence: direct execution of
`2_products/pepper-agent/tests/hermes_cli/runtime_adapter_lifecycle_probe.py`
with `--verify-provider-null --expect-no-path` returned `0`, wrote `0` stdout
bytes and `0` stderr bytes, spawned no child, opened no listener, performed no
provider, credential, worker, agent, tool or MCP action, and created no temp
file, audit file, event spool, result JSON or persistent log.

## Import Drift Reconciliation

| Check | Result |
| --- | ---: |
| Included import rows | `6681` |
| Missing import destinations | `0` |
| Duplicate import destinations | `0` |
| Unsupported import classifications | `0` |
| Destination hash mismatches total | `3` |
| Authorized preexisting P15.M6 destination mismatches | `3` |
| New P15.M7 destination mismatches | `0` |
| P15.M7 product-owned files outside import manifest | `36` |
| P15.M7 product-owned files inside import manifest | `0` |
| Unexplained destination hash mismatches | `0` |
| Destination mismatches without modification row | `0` |

Authorized preexisting P15.M6 mismatches: `P15.M6-002` (`hermes_cli/web_server.py`),
`P15.M6-020` (`web/src/main.tsx`), and `P15.M6-021` (`web/src/App.tsx`).

Authority model: import manifest remains upstream import provenance authority;
modification register remains downstream product delta authority; canonical v2
current HEAD identity remains product identity authority.

## Canonical Product Identity

The canonical utility was run twice before the baseline JSON update and once
after the update. Candidate and payload identities were stable. The baseline
JSON is excluded from candidate identity.

| Scope | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Pre-P15.M7 candidate | `6703` | `148235965` | `1897e20d93858c7125ad5ddee6ac5e56fe808b154c6e786ce42a204730a14146` |
| Post-P15.M7 candidate | `6739` | `148980102` | `f1ae63052455e39e4e259e432075de601123f0f0d538d492ac15acae4cda1d39` |
| Pre-P15.M7 payload | `6681` | `145409765` | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |
| Post-P15.M7 payload | `6681` | `145409765` | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |
| Baseline record before P15.M7R | `not_applicable` | `28119` | `dfbab65b5b5b960cba50c209ad3e18dc21c06b4a028322945b73f9b325633543` |

Candidate files added since P15.M6R: `36`. Payload identity matches pre-P15.M7:
`true`. Repeat candidate digest match: `true`. Repeat payload digest match:
`true`.

## Baseline Record Update

Updated path: `2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json`.

The baseline record now stores committed post-P15.M7 candidate and payload
integrity, preserves pre-P15.M7 candidate and payload identities, and records
bounded runtime-adapter state for P15.M7.

Candidate baseline-record working bytes: `30860`.

Candidate baseline-record working SHA-256:
`ce0c1875182b9aae46448102ed285f1cf9343b96724cf522a0503fc9f3873719`.

Self-reference: `false`. The baseline JSON does not store its own SHA-256.
Historical P15.M1, P15.M1D, P15.M6, P15.M6A and P15.M6R evidence is preserved.

Runtime-adapter state recorded: owner ticket `P15.M7`, commit
`5d680f46efdfc7c66fe1e74534322b662cc29580`, schema version `1`, source files
`19`, test and harness files `17`, profiles `test.lifecycle_probe` and
`pepper.dashboard.provider_null`, provider profiles `0`, worker profiles `0`,
agent profiles `0`, lifecycle states `13`, lifecycle actions `12`, event
descriptors `20`, readiness descriptors `7`, modification rows `36`, product UI
`disabled`, extension modules `0`, public lifecycle API `false`, provider
activation `false`, credential access `false`, OAuth execution `false`, worker
launch `false`, agent launch `false`, tool execution `false`, MCP execution
`false`.

## Repository Integrity

```yaml
runtime_implementation_changes: 0
runtime_test_changes: 0
current_product_changes_outside_baseline_record: 0
P15_M6_implementation_changes: 0
P15_M7_implementation_changes: 0
P15_M7_test_changes: 0
product_configuration_changes: 0
web_server_changes: 0
frontend_changes: 0
Workspace_source_changes: 0
Workspace_tracked_changes: 0
modification_register_changes: 0
application_manifest_changes: 0
import_manifest_changes: 0
exclusion_manifest_changes: 0
third_party_notice_changes: 0
dependency_or_lock_changes: 0
provider_changes: 0
credential_changes: 0
worker_changes: 0
Desktop_changes: 0
Graphify_commands: 0
Graphify_modifications: 0
dependency_installations: 0
registry_queries: 0
full_builds: 0
Pepper_dashboard_starts: 0
Desktop_starts: 0
Workspace_starts: 0
Docker_starts: 0
Compose_starts: 0
WSL_mutations: 0
OAuth_flows: 0
credential_reads: 0
provider_calls: 0
inference_calls: 0
```

## P15.M8 Handoff

P15.M8 may begin only after P15.M7R is accepted, staged, committed and pushed.

Required P15.M8 entry authority:

```yaml
P15_M6R_verdict: hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints
P15_M7_verdict: hermes_0_19_governed_runtime_adapter_application_ready_with_constraints
P15_M7R_verdict: hermes_0_19_governed_runtime_adapter_post_commit_integrity_closed_with_constraints
product_id: pepper
product_version: 0.1.0-dev
upstream_version: 0.19.0
product_UI: disabled
extension_modules: 0
runtime_adapter_contract_schema_version: 1
runtime_profiles:
  - test.lifecycle_probe
  - pepper.dashboard.provider_null
provider_profiles: 0
worker_profiles: 0
agent_profiles: 0
candidate_integrity:
  files: 6739
  bytes: 148980102
  SHA256: f1ae63052455e39e4e259e432075de601123f0f0d538d492ac15acae4cda1d39
payload_integrity:
  files: 6681
  bytes: 145409765
  SHA256: 56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7
baseline_record_candidate_SHA256: ce0c1875182b9aae46448102ed285f1cf9343b96724cf522a0503fc9f3873719
P15_M7_modification_rows: 36
```

P15.M8 must not bypass the runtime adapter, inherit parent credentials, expose
secrets to clients, add provider authority to `pepper.dashboard.provider_null`,
convert provider-null into a live provider profile without explicit contract, or
use the pre-P15.M7 candidate identity.

## Final Candidate Set

Modified:

```text
2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
```

Created:

```text
0_architecture/governance/agent_platform_hermes_0_19_governed_runtime_adapter_post_commit_integrity_closure.md
```

Candidate files: `2`. Unexpected candidates: `0`.

No staging, commit or push was performed by the agent.
