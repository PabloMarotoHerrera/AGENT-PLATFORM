# P13.8 - Hermes Frontend Quality Gate

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.8 - Frontend Quality Gate |
| Date | 2026-07-18 |
| Status | Validated and ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_frontend_quality_gate.md` |
| Accepted start commit | `3460738cb1597c46272bc7f10040222da8570e9d` |
| Accepted prerequisite | Committed P13.7 Safe Settings and Feature Flags |
| Reuse decision | `adapt_existing` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

Record the bounded P13.8 frontend quality gate for the compiled but inactive
AGENT PLATFORM Hermes product UI surfaces. P13.8 adds durable evidence contracts,
cross-surface invariants, an executable local quality-gate runner and browser
evidence without adding routes, selecting extension modules or enabling
`agent_platform.product_ui` in tracked configuration.

The browser lane uses request interception to supply a synthetic product
configuration only inside the local Chromium session. This does not change
backend configuration, tracked product configuration, feature flags, extension
modules, registered runtime routes or navigation state.

## Dynamic Prerequisite Result

```yaml
P13_8_PrerequisiteStatus:
  branch: main
  accepted_head: 3460738cb1597c46272bc7f10040222da8570e9d
  origin_main: 3460738cb1597c46272bc7f10040222da8570e9d
  head_equals_origin_main: true
  git_index_empty_at_start: true
  tracked_product_clean_at_start: true
  P13_7_governance_record_present: true
  product_tracked_files_at_start: 6179
  modification_register_rows_at_start: 61
  modification_register_columns_at_start: 18
  compiled_product_descriptors_at_start: 9
  resolved_product_descriptors_at_start: 0
  registered_runtime_product_routes_at_start: 0
  agent_platform_navigation_items_at_start: 0
  product_UI_feature_at_start: disabled
  extension_modules_at_start: []
  prerequisite_result: pass
```

Bounded read-only Graphify query output was used only as navigation evidence.
No Graphify generation, extraction, clustering, export or refresh completed as
part of P13.8, and no Graphify path is part of the P13.8 output.

## Quality Contract

P13.8 defines a frozen evidence contract for:

- ten frontend surfaces, including the application shell and nine compiled P13 descriptors;
- loading, ready, empty, stale, error, unavailable and not-configured states;
- read-only authority statements, allowed actions and forbidden capabilities;
- Hermes teal and Nous blue theme evidence;
- mobile, tablet and desktop viewport evidence;
- semantic, keyboard and security checks;
- activation posture proving committed product UI remains disabled.

The compiled descriptor IDs remain exactly the reviewed P13 set:

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

## Conditional Fixes

The quality gate surfaced and closed four frontend quality defects:

- recursive pollers now settle after 15 seconds even when an underlying request ignores cancellation;
- unknown Kanban source statuses remain visible under an explicit `other` group instead of being hidden;
- native select filters in Projects, Approval Inbox and Execution Inspector have visible wrapper focus rings;
- product page wrappers no longer create nested `<main>` landmarks inside the dashboard shell;
- recursive browser evidence no longer requires a source edit to `web/src/App.tsx`; shell focus changes are out of scope for P13.8.

These are behavior and accessibility corrections only. They add no backend
mutation, route activation, product configuration write, provider/model control,
approval decision, execution control or work mutation authority.

## Files Created And Updated

Created product-owned quality files:

```text
web/src/agent-platform/frontend-quality/quality-contract.ts
web/src/agent-platform/frontend-quality/quality-matrix.ts
web/src/agent-platform/frontend-quality/frontend-quality-gate.test.tsx
web/src/agent-platform/frontend-quality/index.ts
```

Created repository governance and runner files outside the product register:

```text
10_scripts/hermes/agent_platform_frontend_quality_gate.py
12_tests/hermes/test_agent_platform_frontend_quality_gate.py
0_architecture/governance/agent_platform_hermes_frontend_quality_gate.md
```

Updated existing product UI files for conditional fixes and cumulative register
hashes only. No dependency manifest, lockfile, feature flag, extension module
selection, backend configuration, route registration table, Graphify output or
immutable upstream source path was intentionally changed.

`web/src/App.tsx` is unchanged from the accepted P13.7 `HEAD` version and has
no P13.8 cumulative register update.

## Modification Register

```yaml
P13_8_register_result:
  rows_before: 61
  rows_after: 65
  columns: 18
  rows_added:
    - P13.8-001
    - P13.8-002
    - P13.8-003
    - P13.8-004
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  hash_mismatches: 0
  product_owned_additions: 62
  upstream_derived_modifications: 3
  register_sha256: 137518c26418daaf3d0fb6e34fea5eb06e3a2ad6753589efac9ca37c0bef2a8c
  normalized_rows_sha256: ec40a6feb808263ddab8b04a142351614d5636049a54c99388a007515771da9d
```

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Frontend quality focused suite | Pass | `npm test --workspace web -- src/agent-platform/frontend-quality/frontend-quality-gate.test.tsx`, 6 tests |
| Product UI slice | Pass | `npm test --workspace web -- src/agent-platform`, 10 files, 156 tests |
| Python runner unit tests | Pass | `.venv\Scripts\python.exe -m unittest discover -s ..\..\12_tests\hermes -p test_agent_platform_frontend_quality_gate.py`, 18 tests |
| TypeScript | Pass | `npm run typecheck --workspace web` |
| Scoped ESLint | Pass | `node ..\node_modules\eslint\bin\eslint.js src/agent-platform` |
| P13.8 full quality runner | Pass | `20260718T161822Z-50174d94`, source integrity + test + typecheck + lint + build + dashboard + browser |
| Dashboard readiness | Pass | HTTP 200 for `/api/status`, `/`, authenticated product configuration; unauthenticated product configuration 401 |
| Browser scenarios | Pass | 10 Chromium scenarios across desktop and mobile; no console/page/network errors except expected provider-null auth 401s; mobile shell focus source edit is not part of P13.8 |
| Preview handoff | Pass | Vite `127.0.0.1:5179`; `/agent-platform/overview` HTTP 200; isolated dashboard/backend stopped before human review |

The full runner wrote bounded evidence under the approved temp directory during
validation:

```text
C:\Users\pablo\AppData\Local\Temp\opencode\p13.8-frontend-quality-gate-scope-corrected.json
```

That temporary evidence file and the associated P13.8 runtime, preview, browser
and quality-runner artifacts were removed during Phase B cleanup after human
acceptance.

## Human Visual Checkpoint

```yaml
P13_8_human_visual_checkpoint:
  result: accepted
  accepted_at: 2026-07-18
  checkpoint_scope: consolidated_P13_8_frontend_preview
  reviewer_confirmation: ACCEPTED
  product_activation_deferred_to: P13.R
```

Accepted representative evidence:

- Application shell renders with the Hermes visual system.
- Runtime Overview renders correctly.
- Projects and contextual navigation render correctly.
- Ticket Detail renders correctly.
- Approval Inbox and Approval Detail preserve provisional-authority boundaries.
- Execution Inspector and Execution Detail preserve source-local execution boundaries and expose no execution controls.
- Safe Settings preserves read-only feature activation and exposes only trusted display preferences.
- Hermes Teal and Nous Blue render correctly.
- Desktop and mobile layouts are usable.
- Long bounded content wraps without horizontal document overflow.
- Keyboard focus is visible on inspected filters, links and controls.
- Loading, error and unavailable states are distinguishable and readable.
- Authority limitations are visible and not conveyed by color alone.
- No unauthorized create, edit, delete, approval, execution, feature-toggle, provider, secret, plugin, MCP, gateway, worker or agent controls are exposed.
- The classic Hermes `/sessions` route remaining unchanged is expected because product activation is reserved for P13.R.

## Activation Result

```yaml
P13_8_ActivationStatus:
  compiled_descriptors: 9
  selected_descriptors: 0
  resolved_descriptors: 0
  product_routes_registered: 0
  product_navigation_items: 0
  product_UI_feature: disabled
  extension_modules: []
  synthetic_browser_activation_scope: browser-request-interception-only
  tracked_configuration_changed: false
  backend_configuration_changed: false
```

## Phase B Cleanup

```yaml
P13_8_PhaseB_Cleanup:
  human_visual_checkpoint: accepted
  preview_process_root_pid: 11132
  preview_process_tree_terminated: true
  port_5179_free: true
  port_9128_free: true
  p13_8_temp_artifacts_remaining: 0
  vite_processes_remaining: 0
  dashboard_processes_remaining: 0
  automated_browser_processes_remaining: 0
  devtools_listeners_remaining: 0
  graphify_frozen_integrity: passed
  staging_performed: false
  commit_performed: false
  push_performed: false
```

## Constraints

P13.8 is a local frontend quality gate, not a formal WCAG certification or an
assistive-technology audit. Browser evidence is limited to the locally available
Chromium-family executable and deterministic CDP checks. Human visual review for
P13.8 is accepted; product activation remains reserved for a later P13.R decision.
