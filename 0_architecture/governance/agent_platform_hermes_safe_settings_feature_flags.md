# P13.7 - Hermes Safe Settings And Feature Flags

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.7 - Safe Settings and Feature Flags |
| Date | 2026-07-18 |
| Status | Validated and ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_safe_settings_feature_flags.md` |
| Accepted start commit | `7b663dfd9bc0eb755e717df36d6f5216421f1c65` |
| Accepted prerequisite | Committed P13.6 Execution Inspector |
| Reuse decision | `adapt_existing` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

Record the bounded P13.7 implementation of Safe Settings and read-only feature
posture. The surface adapts validated product configuration, the static product
extension registry and existing Hermes theme, curated-font and locale
authorities. It does not create a second settings system, configuration writer,
feature-flag authority, persistence format or executable extension mechanism.

P13.7 permits writes only for exact members of reviewed source-owned display
catalogs. Product identity, upstream identity, feature state, module selection,
route activation and navigation activation remain read-only. P13.R remains the
owner of any tracked product activation decision.

## Dynamic Prerequisite Result

```yaml
P13_7_PrerequisiteStatus:
  branch: main
  accepted_head: 7b663dfd9bc0eb755e717df36d6f5216421f1c65
  origin_main: 7b663dfd9bc0eb755e717df36d6f5216421f1c65
  head_equals_origin_main: true
  git_index_empty_at_start: true
  tracked_product_clean_at_start: true
  P13_6_governance_record_present: true
  P13_6_execution_inspector_committed: true
  product_tracked_files_at_start: 6172
  modification_register_rows_at_start: 54
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  compiled_product_descriptors_at_start: 8
  resolved_product_descriptors_at_start: 0
  registered_runtime_product_routes_at_start: 0
  agent_platform_navigation_items_at_start: 0
  product_UI_feature_at_start: disabled
  extension_modules_at_start: []
  locked_upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  locked_upstream_clean_at_start: true
  nested_product_git: false
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  prerequisite_result: pass
```

One bounded read-only Graphify query was used during initial navigation. No
Graphify generation, update, extraction, clustering, export or scalable refresh
command ran, and no Graphify path was modified by P13.7.

## Settings-Source Audit

| Source or setting | Classification | P13.7 decision | Reason |
| --- | --- | --- | --- |
| Validated product/upstream identity | `safe_read_only` | Project bounded identity fields | Existing tracked product configuration is authoritative and credential-free |
| Product feature flags | `safe_read_only` | Display exact validated states only | Safe Settings has no feature mutation authority |
| Extension selection and registration posture | `safe_read_only` | Display aggregate counts only | P13.R owns tracked activation; no module selector is exposed |
| Built-in Hermes theme IDs | `safe_read_write` | Permit exact reviewed IDs | Existing dashboard endpoint persists the ID; custom definitions are excluded |
| Custom themes, CSS, assets and theme objects | `blocked_executable` | Exclude | Definitions may contain CSS, URLs, assets and component expressions |
| Curated Hermes font IDs | `safe_read_write` | Permit exact reviewed IDs | Existing frontend and backend catalogs reject arbitrary IDs/URLs |
| Arbitrary font URLs or files | `blocked_executable` | Exclude | URL/path input expands the network and filesystem trust boundary |
| Supported locale IDs | `safe_read_write` | Permit exact locale IDs | Existing browser-local locale authority owns the finite catalog |
| Layout density | `unavailable` | Read theme-derived value; no write | No independent reusable safe setter exists |
| Navigation collapse preference | `unavailable` | No read/write control | Setter remains internal to the application shell |
| Selected management profile | `safe_read_only` | Display context only | Display writes are not falsely represented as profile-local |
| Raw config, YAML, environment and paths | `blocked_sensitive` or `blocked_executable` | Exclude | Broad configuration can contain secrets, commands, URLs and lifecycle authority |
| Providers, models, OAuth, plugins, MCP, hooks and memory providers | `blocked_sensitive` or `blocked_executable` | Exclude | These are credential, code-loading or runtime-capability surfaces |
| Gateway, worker and agent lifecycle | `unavailable` | Exclude | P13.7 grants no runtime control authority |

## Authority, Scope And Impact Model

Writable theme IDs are exactly:

```text
default
```

Writable font IDs are exactly:

```text
theme
```

Writable locale IDs are exactly:

```text
en
```

Theme and font writes use the existing authenticated dashboard endpoints and
must receive an exact confirmation response. Their visible target is the
current dashboard backend plus this browser. The confirmed backend value is
applied through a dashboard reload because the existing ThemeProvider setters
also persist; reusing those setters after a confirmed PUT would issue an
untracked duplicate write. The surface therefore labels their impact as
`dashboard reload required`.

Language uses the existing browser-local key and locale context. P13.7 writes
and reads back the exact supported ID before applying the existing locale
setter. Its target is all profiles in this browser and its impact is immediate.

The selected profile is always visible, but no writable preference claims
profile-local persistence. Every preference displays classification, target,
persistence authority, impact, current trusted value and last successful write.

## Contract, Adapter And Freshness Behavior

The contract requires exact keys, bounded text/counts/timestamps, stable
identifiers, immutable projections, unique feature/preference/value IDs and
agreement between `safe_read_write` classification and write availability.
Unknown current values are visibly excluded rather than coerced to a default.
Write requests must name a writable preference and an exact catalog member.

The adapter immediately projects source contexts and retains no raw source
object. It uses a bounded 15-second post-write reconciliation value so React
context can converge after confirmation; once the source matches, or the bound
expires, current source context is authoritative again.

Polling starts immediately and recurs at ten seconds without overlap. Reads and
writes use a 15-second abort boundary, settle even when an injected dependency
ignores cancellation, suppress late results after stop, retain only the last
validated snapshot as stale and reset controller state on selected-profile
identity change. Raw transport errors are replaced with fixed bounded messages.
All preference controls are disabled while one write is active.

## Safe Settings Surface

`/agent-platform/settings` presents:

- read-only product and immutable upstream identity;
- read-only feature states and their tracked authority;
- compiled, selected, resolved, route and navigation counts;
- trusted theme, font and language choices;
- unavailable density and navigation postures;
- selected profile, target, persistence and impact labels;
- loading, ready, stale, error, unavailable and not-configured presentation;
- an explicit excluded-settings boundary and no raw-config fallback.

The page exposes no feature toggle, extension-module selector, key/token field,
OAuth action, provider/model selector, arbitrary URL/path input, raw YAML,
plugin/MCP/hook action or gateway/worker/agent lifecycle control.

## Descriptor And Activation Result

The registry now compiles nine reviewed descriptors in deterministic order:

```text
agent_platform.ui.overview
```

`agent_platform.ui.settings` is a statically imported descriptor at
`/agent-platform/settings`, belongs to the product navigation group and uses
`agent_platform.product_ui`. Committed configuration does not select it.

```yaml
P13_7_ActivationStatus:
  compiled_descriptors: 9
  selected_descriptors: 0
  resolved_descriptors: 0
  product_routes_registered: 0
  product_navigation_items: 0
  product_UI_feature: disabled
  extension_modules: []
  feature_mutation_exposed: false
```

## Files Created And Updated

Created:

```text
web/src/agent-platform/safe-settings/contract.ts
```

Updated:

```text
web/src/agent-platform/extensions.ts
```

Canonical governance output created outside the product register:

```text
0_architecture/governance/agent_platform_hermes_safe_settings_feature_flags.md
```

No backend, product configuration, application shell, ThemeProvider, locale
provider, profile provider, dependency, package manifest, lockfile, immutable
upstream, Graphify or conditional catalog-test path was changed.

## Modification Register

```yaml
P13_7_register_result:
  rows_before: 54
  rows_after: 61
  columns: 18
  rows_added:
    - P13.7-001
    - P13.7-002
    - P13.7-003
    - P13.7-004
    - P13.7-005
    - P13.7-006
    - P13.7-007
  cumulative_rows_updated:
    - P12.6-008
    - P12.6-010
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  hash_mismatches: 0
  final_product_files: 6179
```

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Focused Safe Settings/catalog | Pass | 2 files, 39 tests |
| Exact P13 regression lane | Pass | 8 files, 141 tests |
| Full dashboard tests | Pass | 15 files, 183 tests |
| TypeScript | Pass | `tsc -p . --noEmit` |
| Affected ESLint | Pass | Safe Settings module and both extension files |
| Production build | Pass | 536 modules transformed; inherited large-chunk warning only |
| Windows-footgun scanner | Pass | Existing product `.venv`; 755 Python files |
| Independent boundary review | Pass | No remaining actionable correctness or security findings |
| Git whitespace check | Pass | `git diff --check`; line-ending warnings only |
| Register integrity | Pass | 61 rows, 18 columns, zero duplicates, missing fields or hash mismatches |

The production build initially exposed three test-only Promise inference errors
not included by the standalone no-emit command. Explicit result types corrected
the tests; the full suite, typecheck, lint and production build then passed.

## Provider-Null Runtime Evidence

An isolated headless backend used external temporary root
`C:\Users\pablo\AppData\Local\Temp\opencode\p13.7-runtime-20260718` rather
than the preferred ignored artifact path. This bounded deviation kept runtime
state outside tracked files and the root was removed during closure.

The first detached backend tree (`4584`, `4520`, `27900`) was healthy, but its
ephemeral token had not been captured, so authenticated boundary verification
was impossible. Only that exact tree was terminated. One detached relaunch
(`26552`, `31340`, listener `19240`) used an explicit synthetic runtime-only
token and bounded readiness.

```yaml
P13_7_provider_null_runtime:
  listener: 127.0.0.1:9127
  status_HTTP: 200
  root_HTTP: 404
  root_posture: expected_headless_backend_UI_disabled
  authenticated_product_configuration_HTTP: 200
  unauthenticated_product_configuration_HTTP: 401
  product_identity_present: true
  upstream_identity_present: true
  product_UI_feature: disabled
  extension_modules: []
  compiled_descriptors: 9
  selected_descriptors: 0
  resolved_descriptors: 0
  product_routes_registered: 0
  product_navigation_items: 0
  gateway_running: false
  gateway_mode: none
  auth_providers: []
  active_agents: 0
  active_sessions: 0
  worker_processes: 0
  mutation_endpoints_called: 0
```

No raw config, environment/key, provider/model, OAuth, plugin, MCP, hook,
memory, gateway-lifecycle or Chat endpoint was called.

## Preview And Human Acceptance

An ignored Vite harness under `9_artifacts/hermes/p13.7/preview` imported the
real Safe Settings page, contract, adapter and hook; real React and React DOM
from the product workspace; the real ThemeProvider, I18nProvider,
ProfileProvider, router, Nous UI dependencies, dashboard stylesheet and P13.1
semantic tokens. It used preview-only safe fixtures and intercepted only the
required display/profile reads and safe display writes. It did not activate a
committed route or mutate tracked configuration.

The first preview (`14376`, listener `14376`) returned HTTP 200 for root, main
module and Vite client. A bounded headless Chrome tree rooted at `19240`
identified that the preview omitted the product `@tailwindcss/vite` pipeline,
so React content was browser-default and the preview failed technical visual
readiness. The exact Chrome tree was terminated and DevTools port `9227` was
released. Only the ignored preview config was corrected to use the same React
and Tailwind plugins as the real product bootstrap.

The corrected preview (`29888`, listener `29888`) became ready in 199 ms with
no compilation failure. The human accepted the corrected Hermes Teal desktop
surface and explicitly confirmed:

```yaml
P13_7_human_visual_acceptance:
  accepted: true
  Hermes_visual_system_active: true
  ThemeProvider_active: true
  Nous_UI_active: true
  P13_1_semantic_tokens_active: true
  blank_or_browser_default: false
  product_and_upstream_identity_read_only: true
  product_feature_state_read_only: true
  product_UI_visibly_disabled: true
  experimental_fixture_distinguished: true
  compiled_selected_resolved_routes_navigation: [9, 0, 0, 0, 0]
  P13_R_activation_authority_visible: true
  persistence_scope_profile_and_impact_visible: true
  raw_config_fallback_exposed: false
  prohibited_controls_visible: false
```

The planned full automated browser state matrix was not rerun after the
preview-only Tailwind correction because the Phase B acceptance instruction
explicitly prohibited relaunching browser automation. State rendering and
write behavior remain covered by the 39 focused tests and 141-test exact P13
lane; final styled visual evidence is the accepted human checkpoint. This is a
documented validation limitation, not represented as an automated matrix pass.

## Process And Artifact Cleanup

```yaml
P13_7_cleanup:
  initial_backend_tree_terminated: [4584, 4520, 27900]
  verified_backend_tree_terminated: [26552, 31340, 19240]
  initial_preview_tree_terminated: [14376, 29248]
  corrected_preview_tree_terminated: [29888, 4024]
  automated_Chrome_root_terminated: 19240
  automated_Chrome_descendants_terminated: [17668, 8244, 5512, 7844, 10900, 25640]
  port_5178: free
  port_9127: free
  port_9227: free
  P13_7_backend_processes: 0
  P13_7_preview_processes: 0
  P13_7_automated_Chrome_processes: 0
  artifact_tree_removed: true
  external_runtime_root_removed: true
  original_shared_junction_intact: true
  original_shared_junction_target: 2_products/hermes-agent/apps/shared
```

Only exact owned process trees and P13.7 temporary paths were terminated or
removed. No unrelated browser, Node, Python or user process was targeted.

## Source, Lockfile And Graph No-Drift

```yaml
backend_files_modified: 0
App_tsx_modified: false
product_configuration_modified: false
ThemeProvider_modified: false
locale_provider_modified: false
profile_provider_modified: false
package_manifest_modified: false
dependency_lockfile_modified: false
dependency_install_performed: false
immutable_upstream_modified: false
product_provider_enabled: false
feature_or_extension_activation_mutated: false
Graphify_generation_commands_run: 0
Graphify_paths_modified_by_P13_7: 0
staged_files: 0
commits_by_agent: 0
pushes_by_agent: 0
```

For subsequent work, the existing Graphify graph is frozen read-only
navigation evidence. Bounded Graphify queries should narrow source locations
before broad searches where useful; grep is a narrow verification fallback.
No Graphify update, extract, cluster-only, export or scalable refresh command
is authorized. Graphify is not repository authority or canonical memory;
G-Brain remains the intended durable memory and semantic-retrieval system.

## Limitations

- Theme and font writes are dashboard-backend preferences, not selected
  management-profile settings, and require a dashboard reload after confirmed
  persistence to avoid duplicate ThemeProvider writes.
- Language is browser-local and applies across selected profile contexts in the
  same browser.
- Layout density remains theme-derived and unavailable as an independent write.
- Navigation collapse remains application-shell-owned and unavailable here.
- The existing theme endpoint accepts broader names server-side; P13.7 submits
  only exact built-in IDs and does not expose custom definitions.
- Browser cancellation cannot roll back a write already committed by its
  existing persistence authority.
- The corrected styled preview received explicit human acceptance, but the full
  automated post-correction browser matrix was not rerun as described above.
- P13.8 retains broader accessibility, interaction and visual-regression
  consolidation ownership.

## Rollback Procedure

1. Remove the seven `web/src/agent-platform/safe-settings/*` files.
2. Remove `SAFE_SETTINGS_DESCRIPTOR` and activation-posture additions from the
   static extension registry.
3. Remove P13.7 catalog and protected-path assertions from
   `extensions.test.ts`.
4. Remove register rows `P13.7-001` through `P13.7-007`.
5. Restore prior cumulative content and hashes for `P12.6-008` and
   `P12.6-010`.
6. Remove this governance record.

No backend, configuration, dependency, lockfile, upstream, Graphify or runtime
state rollback is required.

## Sequencing And Handoff

- P13.8 may proceed after human commit of the accepted P13.7 candidate.
- P13.8 owns broader keyboard, screen-reader, interaction and visual-regression
  consolidation, including optional post-correction browser-matrix expansion.
- P13.R remains the only owner of tracked feature/module activation decisions.
- Any profile-local display persistence, new setting category, custom theme or
  font input, backend safe DTO or lifecycle control requires separate source,
  authorization, persistence, impact and human-approval governance.
- P15 provider enablement remains unauthorized.

## Result Markers

```text
hermes_P13_7_prerequisite_gate_passed
hermes_P13_7_dynamic_start_SHA_accepted
hermes_safe_settings_sources_audited
hermes_safe_settings_strict_projection_created
hermes_safe_settings_trusted_allowlists_enforced
hermes_safe_settings_theme_write_confirmed
hermes_safe_settings_font_write_confirmed
hermes_safe_settings_language_write_confirmed
hermes_safe_settings_feature_activation_read_only
hermes_safe_settings_no_raw_config_fallback
hermes_safe_settings_descriptor_compiled
hermes_safe_settings_descriptor_not_selected
hermes_safe_settings_route_not_registered
hermes_product_UI_feature_remains_disabled
hermes_extension_modules_remain_empty
hermes_P13_7_focused_tests_passed
hermes_P13_7_exact_regression_passed
hermes_P13_7_full_dashboard_tests_passed
hermes_P13_7_typecheck_passed
hermes_P13_7_affected_lint_passed
hermes_P13_7_production_build_passed
hermes_P13_7_windows_footgun_scan_passed
hermes_P13_7_boundary_review_passed
hermes_P13_7_provider_null_runtime_passed
hermes_P13_7_human_visual_checkpoint_accepted
hermes_P13_7_owned_runtime_cleanup_passed
no_feature_or_extension_activation_mutation
no_provider_gateway_worker_or_agent_activation
no_backend_or_dependency_change
no_Graphify_generation_or_mutation
```

## Final Verdict

P13.7 is complete and ready with constraints. Only exact trusted display
preferences are writable; product feature and extension activation remain
read-only and inert. The provider-null runtime, source boundary, tests, build,
register, cleanup and accepted visual checkpoint support the candidate. The
post-correction automated browser-matrix gap and existing persistence-scope
limitations are explicitly retained above for P13.8 rather than overstated.

## Human Commit Boundary

The human commit candidate is limited to this governance record and the ten
authorized product paths listed under Files Created And Updated. Exclude
`.opencode/**`, root `AGENTS.md`, `graphify-out/**`, `9_artifacts/**`, build
output and runtime state. Nothing is staged, committed or pushed by the agent.
