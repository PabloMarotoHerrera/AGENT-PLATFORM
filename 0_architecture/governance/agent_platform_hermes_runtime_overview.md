# P13.3 - Hermes Runtime Overview

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.3 - Runtime Overview |
| Date | 2026-07-15 |
| Status | Implemented and validation-ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_runtime_overview.md` |
| Accepted start commit | `c19310fee5af0d321bdd0655afe4f4f3085e72aa` |
| Accepted prerequisite | P13.3-PRE semantic activation-boundary test |
| Git mutation by agent | Prohibited and not performed |

## Purpose

Record the bounded P13.3 implementation of a read-only Hermes Runtime
Overview. The surface validates the broad `/api/status` dictionary, retains
only reviewed low-sensitivity fields, and compiles one product descriptor
without activating any product route or navigation entry.

This document replaces the obsolete stale-SHA blocker record. The superseding
ticket explicitly accepted `c19310fee5af0d321bdd0655afe4f4f3085e72aa` as
the execution baseline.

## Prerequisite Result

```yaml
P13_3_PrerequisiteStatus:
  branch: main
  accepted_head: c19310fee5af0d321bdd0655afe4f4f3085e72aa
  origin_main: c19310fee5af0d321bdd0655afe4f4f3085e72aa
  head_equals_origin_main: true
  git_index_empty_at_start: true
  tracked_product_clean_at_start: true
  immutable_upstream_clean_at_start: true
  product_tracked_files_at_start: 6141
  modification_register_rows_at_start: 23
  modification_register_hash_mismatches_at_start: 0
  product_UI_feature_at_start: disabled
  extension_modules_at_start: []
  prerequisite_result: pass
```

Graphify was not used.

## Existing Runtime Status Baseline

The exact isolated provider-null response was collected from the current
`hermes serve` implementation before the frontend contract was frozen. The
loopback runtime used an isolated `HERMES_HOME` under
`9_artifacts/hermes/p13.3/runtime` and returned:

```yaml
HTTP_status: 200
version: 0.18.2
release_date: 2026.7.7.2
config_version: 33
latest_config_version: 33
can_update_hermes: true
gateway_running: false
gateway_state: null
gateway_platforms: {}
active_agents: 0
gateway_busy: false
gateway_drainable: false
active_sessions: 0
auth_required: false
auth_providers: []
nous_session_valid: unknown
profiles:
  - default
gateway_mode: none
gateway_pid: null
gateway_health_url: null
gateways: []
```

The source also returned isolated local paths for `hermes_home`,
`config_path`, and `env_path`. Those values were observed only to verify
isolation and were not admitted to the product contract.

## Status-Source Field Classification

Retained and normalized:

| Source field | Product projection | Reason |
| --- | --- | --- |
| `version` | `platform.version` | Bounded product version label |
| `release_date` | `platform.releaseDate` | Bounded release label |
| `config_version` | `platform.configVersion` | Non-negative schema readiness value |
| `latest_config_version` | `platform.latestConfigVersion` | Non-negative schema comparison value |
| `can_update_hermes` | Used only to derive `updateAvailable` | Boolean update readiness |
| `gateway_running` | `gateway.running` | Gateway liveness |
| `gateway_state` | Closed normalized state enum | No raw value retained |
| `gateway_busy` | `gateway.busy` | Gateway activity state |
| `gateway_drainable` | `gateway.drainable` | Read-only lifecycle readiness |
| `active_sessions` | `activity.activeSessions` | Recent five-minute session heuristic |
| `active_agents` | `activity.activeAgents` | In-flight Hermes gateway turns |
| `auth_required` | `access.authRequired` | Dashboard access-gate state |

Explicitly excluded:

```text
hermes_home
config_path
env_path
gateway_pid
gateway_health_url
gateways
profiles
gateway_mode
gateway_platforms raw object
gateway_exit_reason
gateway_updated_at
restart_drain_timeout
auth_providers
nous_session_valid
provider and OAuth detail
credentials and tokens
raw transport errors
raw source objects
unknown fields
```

## Safe Product Runtime Contract

`contract.ts` accepts `unknown`, requires a plain dictionary, validates every
retained field by type and bound, and returns an immutable projection. Missing,
malformed, negative, unsafe-integer, empty, or overlong required values fail
closed to `null`.

The projection never keeps the source dictionary. Tests inject local paths,
provider/auth arrays, topology, and a synthetic secret, then prove those
values do not survive serialization of the product snapshot.

`active_sessions` is labeled as the backend's recent five-minute heuristic.
`active_agents` is labeled as Hermes gateway activity and explicitly not as
governed AGENT PLATFORM Agents.

## Load and Freshness State Model

The hook and testable poller implement:

| State | Meaning |
| --- | --- |
| `loading` | No request has completed for the selected profile |
| `ready` | A validated response is current |
| `stale` | Refresh failed after a prior success; last safe snapshot retained |
| `error` | Initial transport request failed; no raw error rendered |
| `unavailable` | Initial response did not satisfy the bounded contract |

Polling starts immediately and recurs with `setTimeout` only after each request
settles. The interval is 10 seconds. An in-flight guard prevents overlap.
Manual refresh cancels a pending timer but never starts a concurrent request.
Cleanup stops timers and suppresses late publication after unmount. Profile
changes create a new poller while old work is stopped safely.

## Runtime Overview Surface

The page uses real Nous UI `Card`, `Badge`, `Button`, and `Spinner` primitives,
plus only the accepted P13.1 `--agent-platform-*` semantic token layer. It is
responsive at desktop and mobile widths and provides:

- explicit live/freshness text in addition to color;
- gateway state, busy state, drainability, and access-gate summaries;
- recent-session and gateway-activity metrics with semantic clarification;
- platform/configuration version readiness;
- keyboard-operable manual refresh;
- labeled loading, stale, error, and unavailable treatments;
- `aria-live`, `aria-busy`, `role=status`, and semantic heading/section usage.

The page is read-only. It has no control for gateway, provider, worker, agent,
MCP, session, configuration, or product activation.

## Static Descriptor and Activation Boundary

The production registry now compiles exactly one reviewed descriptor:

```yaml
id: agent_platform.ui.overview
owner: AGENT_PLATFORM
feature_id: agent_platform.product_ui
visible_when_experimental: true
route_path: /agent-platform/overview
route_title: Runtime Overview
navigation_group: agent-platform
navigation_label: Overview
navigation_placement: end
```

Committed product configuration remains unchanged:

```yaml
feature_flags:
  agent_platform.product_ui: disabled
extension_modules: []
compiled_product_descriptors: 1
resolved_product_descriptors: 0
runtime_product_routes: 0
agent_platform_navigation_items: 0
```

`visibleWhenExperimental` does not bypass explicit extension-module selection
or feature-state resolution. No `App.tsx`, backend, configuration, manifest,
dependency, lockfile, existing route, or existing page was modified.

## Implementation Path Set

Created product-owned files:

```text
2_products/hermes-agent/web/src/agent-platform/runtime-overview/contract.ts
2_products/hermes-agent/web/src/agent-platform/runtime-overview/use-runtime-overview.ts
2_products/hermes-agent/web/src/agent-platform/runtime-overview/runtime-overview-page.tsx
2_products/hermes-agent/web/src/agent-platform/runtime-overview/descriptor.ts
2_products/hermes-agent/web/src/agent-platform/runtime-overview/index.ts
2_products/hermes-agent/web/src/agent-platform/runtime-overview/runtime-overview.test.tsx
```

Modified existing product-owned files:

```text
2_products/hermes-agent/web/src/agent-platform/extensions.ts
2_products/hermes-agent/web/src/agent-platform/extensions.test.ts
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

The accepted P13.3-PRE file
`web/src/agent-platform/design-system/design-system.test.ts` was not modified.

## Modification-Register Reconciliation

```yaml
rows: 29
columns: 18
duplicate_ids: 0
duplicate_paths: 0
hash_mismatches: 0
P13_3_rows_added:
  - P13.3-001
  - P13.3-002
  - P13.3-003
  - P13.3-004
  - P13.3-005
  - P13.3-006
cumulative_rows_updated:
  - P12.6-008
  - P12.6-010
```

The final candidate product inventory is 6,147 files: the 6,141-file accepted
baseline plus exactly six authorized additions.

## Validation Results

| Lane | Result | Evidence |
| --- | --- | --- |
| Targeted dashboard tests | Pass | 3 files, 25 tests |
| Full dashboard tests | Pass | 11 files, 75 tests |
| TypeScript | Pass | `tsc -p . --noEmit` |
| Affected ESLint | Pass | All eight source/test paths |
| Dashboard production build | Pass | 497 modules transformed |
| Windows-footgun scanner | Pass | 755 Python files, no findings |
| Register validation | Pass | 29 rows, 18 columns, zero duplicates or hash mismatches |
| Human visual review | Pass | Desktop and mobile widths accepted on port 5174 |

The dashboard's OneDrive junction issue was handled by temporarily replacing
`node_modules/@hermes/shared` with an exact flat copy of `apps/shared`. After
validation, the copy was removed and the original junction was recreated and
queried with the exact original target.

## Provider-Null Integrated Runtime Verification

An isolated `hermes serve` backend listened only on `127.0.0.1:9123`.
All requests used explicit bounded timeouts.

| Request | Result |
| --- | --- |
| `GET /` | Expected `404` headless-backend message |
| `GET /api/status` | `200`; gateway false, agents 0, sessions 0, auth providers empty |
| `GET /api/agent-platform/product-configuration` | `200`; product UI disabled, extension modules empty |

No gateway, provider, worker, agent, MCP, Chat, or write endpoint was started or
invoked. The backend remained headless by design and was not used for visual
review.

## Temporary Preview Verification

The ignored preview under `9_artifacts/hermes/p13.3/preview` imported the real
`RuntimeOverviewPage`, Hermes `ThemeProvider`, `BrowserRouter`, `ProfileContext`,
Nous UI, dashboard CSS, and P13.1 tokens. It did not import product
configuration, the extension registry, `App.tsx`, or register a route.

An initial blank preview was traced to preview-root resolution of
`react-dom/client`. The correction was confined to the ignored harness by
adding product workspace aliases, required provider scaffolding, explicit root
dimensions, and a preview-only visible error boundary.

Final bounded evidence:

```yaml
preview_root_HTTP: 200
preview_main_module_HTTP: 200
preview_CSS_HTTP: 200
vite_client_HTTP: 200
backend_status_HTTP: 200
main_module_calls_createRoot: true
error_boundary_rendered: false
headless_DOM_state: Live / Offline / 0 sessions / 0 gateway activity
desktop_dimensions_verified: true
mobile_dimensions_verified: true
human_visual_acceptance: pass
```

The exact preview and backend process trees were terminated after acceptance.
Ports 5174 and 9123 were confirmed free. The complete temporary
`9_artifacts/hermes/p13.3` tree was removed.

## Security and Trust Boundaries

- Status input remains untrusted until parsed.
- Raw source dictionaries and raw errors are never stored in React state.
- Paths, process identifiers, URLs, topology, provider/auth details, OAuth
  state, credentials, exit reasons, and unknown fields are excluded.
- Polling uses the existing authenticated/profile-aware `fetchJSON` transport.
- No dynamic import path, runtime code loading, filesystem discovery, or eval
  was added.
- No product feature or module was enabled.
- No provider, gateway, worker, agent, MCP, Chat, or write action ran.

## Source and Lockfile No-Drift Verification

```yaml
upstream_derived_source_changed: false
backend_changed: false
App_tsx_changed: false
configuration_changed: false
package_manifest_changed: false
lockfile_changed: false
dependency_install_performed: false
immutable_upstream_changed: false
accepted_PRE_test_changed: false
```

## Rollback Procedure

1. Remove the six `web/src/agent-platform/runtime-overview/*` files.
2. Remove `RUNTIME_OVERVIEW_DESCRIPTOR` from the static extension registry.
3. Remove the P13.3 activation assertion from `extensions.test.ts`.
4. Remove register rows `P13.3-001` through `P13.3-006`.
5. Restore the prior cumulative hashes/content for register rows `P12.6-008`
   and `P12.6-010`.
6. Remove this governance record.

No backend, configuration, dependency, lockfile, upstream, or runtime-state
rollback is required.

## Limitations and Handoff

- The route is compiled but intentionally unavailable under committed
  configuration.
- The surface reflects the existing `/api/status` semantics and does not claim
  stronger liveness or session semantics than that endpoint provides.
- Human visual acceptance covers this temporary isolated surface, not Chat,
  providers, gateway operation, workers, agents, MCP, or activated shell
  navigation.
- P13.4 may proceed only after the P13.3 worktree is human-reviewed and
  accepted at the commit boundary.
- P14 and P15 provider enablement remain unauthorized.

## Result Markers

```text
hermes_P13_3_runtime_overview_implemented
hermes_P13_3_safe_status_projection_verified
hermes_P13_3_recursive_polling_verified
hermes_P13_3_compiled_descriptor_count_1
hermes_P13_3_resolved_descriptor_count_0
hermes_P13_3_runtime_product_route_count_0
hermes_P13_3_provider_null_runtime_passed
hermes_P13_3_manual_visual_passed
no_product_UI_feature_activation
no_extension_module_activation
no_gateway_lifecycle_action
no_provider_activation
no_worker_or_agent_execution
no_upstream_derived_source_modification
no_git_mutation_by_agent
```

## Final Verdict

```yaml
P13_3_HermesRuntimeOverviewVerdict:
  accepted_start_commit: c19310fee5af0d321bdd0655afe4f4f3085e72aa
  implementation:
    product_additions: 6
    existing_product_owned_source_files_modified: 2
    product_control_files_modified: 1
    upstream_derived_source_files_modified: 0
    backend_files_modified: 0
    modification_register_rows: 29
    product_file_inventory: 6147
  activation:
    compiled_descriptor_count: 1
    resolved_descriptor_count: 0
    runtime_product_route_count: 0
    product_UI_enabled: false
    extension_modules: []
  validation:
    targeted_tests: 25_passed
    full_dashboard_tests: 75_passed
    typecheck: passed
    affected_lint: passed
    dashboard_build: passed
    windows_footgun_scan: passed_755_files
    provider_null_runtime: passed
    human_visual: passed
    temporary_artifacts_removed: true
  execution:
    staged_by_agent: false
    committed_by_agent: false
    pushed_by_agent: false
  final_verdict: hermes_runtime_overview_ready_with_constraints
```

## Human Commit Boundary

The agent did not stage, commit, or push. Human review must include the six new
runtime-overview files, the two extension files, the modification register,
and this canonical governance record. Temporary runtime/preview files must not
be included.
