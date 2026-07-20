# P14.8 Controlled Lifecycle Gate - Passed

## Current Classification

`hermes_runtime_adapter_controlled_lifecycle_passed`

| Diagnostic | Outcome |
| --- | --- |
| Prior live gate verdict | `rejected_incomplete_readiness_evidence` |
| Required correction | `seven_check_readiness_contract` |
| Final controlled-lifecycle verdict | `hermes_runtime_adapter_controlled_lifecycle_passed` |

## Rejected Four-Check Gate

The earlier live gate exited `0` and reported
`hermes_runtime_adapter_controlled_lifecycle_passed`, but it is not accepted as
P14.8 completion evidence. The runner persisted only four readiness endpoint
checks and did not retain exact evidence for dashboard root production safety,
unauthenticated product-configuration denial, plugin manifest validity, dynamic
plugin product-route conflicts, `gateway_running`, active session count, or auth
provider count.

| Field | Rejected Run Value |
| --- | --- |
| Command | `.\2_products\hermes-agent\.venv\Scripts\python.exe 10_scripts\hermes\agent_platform_runtime_adapter_lifecycle_gate.py --repository-root "." --port 9130` |
| Exit code | `0` |
| Launch outcome | `ready` |
| Shutdown outcome | `stopped` |
| Rollback outcome | `rolled_back` |
| Event count | `15` |
| Persisted readiness check count | `4` |
| Acceptance status | `blocked` |

## Corrected Readiness Contract

The corrected runtime readiness contract is immutable and ordered:

| Order | Check ID | Required Evidence |
| ---: | --- | --- |
| 1 | `dashboard.root` | HTTP `200`, production `/assets/` references present, Vite dev/error markers absent, no redirect outside the loopback origin. |
| 2 | `dashboard.status` | HTTP `200`, `gateway_running == false`, `active_agents == 0`, `active_sessions == 0`, `auth_providers == []`. |
| 3 | `dashboard.product_config_unauthenticated` | HTTP `401` without `X-Hermes-Session-Token`. |
| 4 | `dashboard.product_config_authenticated` | HTTP `200` with adapter-owned token, product UI state `experimental`, nine extension modules in exact order. |
| 5 | `dashboard.plugin_manifest` | HTTP `200`, bounded manifest schema, `/agent-platform/**` dynamic tab route conflicts count `0`. |
| 6 | `dashboard.files_root` | HTTP `200`, root and locked root equal the managed files root, `can_change_path == false`. |
| 7 | `dashboard.files_outside_root` | HTTP `403` for a path outside the managed files root. |

The readiness probe stores only bounded scalar evidence. It does not retain HTTP
response bodies, paths, session tokens, cookies, environment values, commands,
PIDs, or raw manifests.

## Runner Evidence Contract

The corrected runner must reject any launch that does not emit exactly seven
readiness checks with the check IDs above. The JSON lifecycle summary must carry
these bounded fields:

| Field | Required Value |
| --- | --- |
| `readiness_check_count` | `7` |
| `event_count` | Integer final lifecycle event count. |
| `audit_projection_count` | Integer in-memory audit projection count; must equal `event_count`. |
| `gateway_running` | `false` |
| `active_agent_count` | `0` |
| `active_session_count` | `0` |
| `provider_count` | `0` |
| `unauthenticated_config_status` | `401` |
| `authenticated_config_status` | `200` |
| `product_feature_state` | `experimental` |
| `extension_module_count` | `9` |
| `extension_module_order_valid` | `true` |
| `plugin_manifest_valid` | `true` |
| `plugin_route_conflict_count` | `0` |
| `managed_files_root_matches` | `true` |
| `outside_files_root_denied` | `true` |

The runner now emits `<repository-root>`, `<artifact-dir>`, and
`<product-python>` placeholders instead of absolute filesystem paths. The audit
projection is created in memory only; only its count is emitted.

## Conditional Test Corrections

| Classification | Path | Scope |
| --- | --- | --- |
| Source-guard correction | `tests/hermes_cli/test_agent_platform_runtime_adapter_contracts.py` | Exact allowlist for `adapter.py`, `listener_discovery.py`, and `readiness.py` only. |
| Rollback-depth correction | `tests/hermes_cli/test_agent_platform_runtime_rollback.py` | Test-only monkeypatched depth to avoid Windows `MAX_PATH`; production rollback, containment, and deletion semantics unchanged. |
| `P14.8-FQ-TEST-001` | `tests/hermes_cli/runtime_adapter_conformance_harness.py` | Windows bounded conformance wait stabilization: existing 5-second harness-owned process waits were raised to a 15-second monotonic deadline, bounded polling was preserved, and failed waits/assertions now retain bounded diagnostic evidence with stable code, stage, expected condition, and observed state counts. No production runtime-adapter source changed. |

`P14.8-FQ-TEST-001` reproduced as intermittent Windows conformance failures in
`ENVIRONMENT-002`, `PROCESS-001`, and forced-fallback lifecycle assertions during
complete P14 regression runs. The correction is limited to the test harness: it
does not change contracts, enums, lifecycle transitions, process ownership,
shutdown, rollback, readiness, listener discovery, the live runner, dashboard
runtime behavior, persistence, or cleanup authority. Diagnostic evidence remains
bounded and excludes absolute paths, commands, environment values, PIDs, raw
stdout/stderr, secrets, and raw tracebacks.

## Register State

| Field | Value |
| --- | --- |
| Register row count target | `101` |
| Register column count target | `18` |
| Duplicate modification IDs target | `0` |
| Duplicate product paths target | `0` |
| Missing fields target | `0` |
| Hash mismatches target | `0` |
| P14.8 product rows | `6` |
| Approved candidate paths | `15` |
| Added candidate paths | `0` |

Updated P14.8 product hashes after the seven-check correction:

| Modification ID | Product path | SHA-256 |
| --- | --- | --- |
| `P14.8-002` | `hermes_cli/agent_platform/runtime_adapter/readiness.py` | `b3839ac6a9f5529fab941d2c297cb1d30500e9615b3ae554b97162d563288447` |
| `P14.8-003` | `hermes_cli/agent_platform/runtime_adapter/adapter.py` | `5dc9860558eb8b78b30f5dcbc5d87dc84caf38c8a3d67c72891a09902cb24e4d` |
| `P14.8-005` | `tests/hermes_cli/test_agent_platform_runtime_readiness.py` | `841530c5dc506046565f34a685de161744a2a14b7fe3276faad1896f6f901edd` |
| `P14.8-006` | `tests/hermes_cli/test_agent_platform_runtime_adapter_integration.py` | `19d9e93314a731c08403be5ff14b74058137796852948434d3bc542f5232b368` |

## Validation Status

| Check | Result |
| --- | --- |
| Focused `P14.8-FQ-TEST-001` regression | `passed: tests/hermes_cli/test_agent_platform_runtime_adapter_conformance.py::test_primary_runtime_adapter_conformance_matrix, 1 passed, 0 skipped, 0 failed, 5.1s`; bounded diagnostic preservation verified by synthetic timeout probe. |
| Complete P14 regression | `passed: 15 files, 148 tests passed, 0 failed, single worker, 23.3s` |
| Adjacent product config/routes regression | `passed: 16 tests passed, 0 failed, 2.3s` |
| Lifecycle-gate runner tests | `passed: 11 tests passed, 0 failed, 0.09s` |
| Product compile check | `passed` |
| Repository runner/test compile check | `passed` |
| Dashboard build | `passed`; Vite emitted only the existing chunk-size warning. |
| Ruff check | `passed` |
| Ruff format check | `passed` |
| Full prescribed Windows footgun scanner | `passed: 774 files scanned` |
| Register audit | `passed: 101 rows, 18 columns, 0 duplicate IDs, 0 duplicate paths, 0 missing fields, 0 hash mismatches` |
| Product candidate inventory | `passed: 6213 tracked product files + 6 approved untracked product candidates = 6219` |
| Git diff whitespace audit | `passed: CRLF normalization warnings only; no whitespace errors` |
| Graphify hashes | `unchanged` |
| Corrected live gate | `passed_once`; not rerun after `P14.8-FQ-TEST-001` because no production runtime behavior changed. |
| Final no-live residue scan | `passed: port 9130 listeners 0; attributable gate/dashboard/probe processes 0; P14.8 result JSON, markers, audit/spool and DB/sqlite files 0` |

## Corrected Live Controlled Lifecycle Evidence

| Field | Value |
| --- | --- |
| Exit code | `0` |
| Dashboard port | `9130` |
| Gate status | `passed` |
| Verdict | `hermes_runtime_adapter_controlled_lifecycle_passed` |
| Launch outcome | `ready` |
| Shutdown outcome | `stopped` |
| Rollback outcome | `rolled_back` |
| Lifecycle event count | `15` |
| Audit-projection count | `15` |
| Readiness check count | `7` |
| Gate duration | `7.811999999999898 seconds` |
| Failures | `[]` |

Corrected bounded readiness evidence:

| Field | Value |
| --- | --- |
| Check IDs | `dashboard.root`; `dashboard.status`; `dashboard.product_config_unauthenticated`; `dashboard.product_config_authenticated`; `dashboard.plugin_manifest`; `dashboard.files_root`; `dashboard.files_outside_root` |
| Dashboard root status | `200` |
| Root production asset refs present | `true` |
| Root Vite dev marker present | `false` |
| Root Vite error overlay marker present | `false` |
| Root redirect outside origin | `false` |
| `/api/status` status | `200` |
| `gateway_running` | `false` |
| `active_agents` | `0` |
| `active_sessions` | `0` |
| Auth provider count | `0` |
| Unauthenticated product config status | `401` |
| Authenticated product config status | `200` |
| Product feature state | `experimental` |
| Extension-module count | `9` |
| Extension-module order valid | `true` |
| Plugin manifest status | `200` |
| Plugin manifest valid | `true` |
| Plugin `/agent-platform/**` route conflict count | `0` |
| Files-root status | `200` |
| Managed files root matches | `true` |
| Outside files root status | `403` |
| Outside files root denied | `true` |

The corrected bounded evidence contained no session tokens, cookies,
environment values, commands, PIDs, raw HTTP response bodies, or absolute paths.
Audit projection remained in memory; only the count was emitted.

## Post-Run Residue

| Check | Result |
| --- | --- |
| Port 9130 bindable after live gate | `true` |
| P14.8 dashboard/gate/DevTools process matches | `0` |
| Ownership marker files beneath P14.8 artifacts | `0` |
| Workspace marker/path matches beneath P14.8 artifacts | `0` |
| Runtime DB files beneath P14.8 artifacts | `0` |
| Runtime log files beneath P14.8 artifacts | `0` |
| Live-run generated artifact directories | `removed_after_empty_directory_verification` |
| Remaining artifact entries before stdout-only runner correction | `runtime-adapter-lifecycle-gate.json`; pre-existing empty `manual-diagnostic/` |
