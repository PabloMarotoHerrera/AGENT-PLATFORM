# P13.2 - Hermes Application Shell and Navigation

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.2 - Application Shell and Navigation |
| Type | Bounded frontend implementation and governance record |
| Execution class | Product-owned shell source, one localized upstream-derived integration edit, validation and provider-null visual verification |
| Date | 2026-07-15 |
| Status | Ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_application_shell_navigation.md` |
| Product root | `2_products/hermes-agent` |
| Immutable upstream | `4_external/sources/hermes-agent` |
| Start commit | `54741f8e5d4da5fea35eb96751b2b4cda10cde6d` |
| Initial/final product count | 6,137 / projected committed 6,141 |
| Initial/final register rows | 19 / 23 |
| Upstream-derived source edits | One localized edit to `web/src/App.tsx` |
| Feature/route/page activation | Prohibited and not performed |
| Git mutation by agent | Prohibited and not performed |

## Purpose

Extend the existing Hermes dashboard shell with configuration-derived product
branding, semantic navigation groups and explicit ownership protection for the
`/agent-platform/**` namespace without adding another router, sidebar, plugin
loader, page, provider or runtime authority.

P13.2 establishes shell composition only. Product UI remains disabled, the
static extension registry remains empty and the AGENT PLATFORM group is
therefore intentionally absent from the rendered navigation.

## Scope

P13.2 creates exactly four product-owned files under
`web/src/agent-platform/shell/**`, modifies the existing first-party extension
contract and tests, applies one localized composition edit to `web/src/App.tsx`,
updates the modification register and creates this governance record.

It does not modify `main.tsx`, `index.css`, themes, pages, shared components,
plugins, i18n catalogs, backend code, manifests, dependencies or locks. It adds
no route, page, descriptor, extension module, feature activation, provider,
gateway, dispatcher, worker or agent behavior.

## Authoritative Inputs

Applied canonical records:

```text
0_architecture/governance/agent_platform_hermes_ui_product_brief_information_architecture.md
0_architecture/governance/agent_platform_hermes_design_tokens_branding_foundation.md
0_architecture/governance/agent_platform_hermes_product_extension_configuration_seams.md
0_architecture/governance/agent_platform_hermes_productization_foundation_closure.md
0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md
```

Implementation authority inspected:

```text
web/src/App.tsx
web/src/agent-platform/extensions.ts
web/src/agent-platform/extensions.test.ts
web/src/agent-platform/design-system/**
web/src/agent-platform/product-config-context.ts
web/src/plugins/types.ts
web/src/plugins/usePlugins.ts
web/src/contexts/PageHeaderProvider.tsx
web/src/lib/resolve-page-title.ts
AGENT_PLATFORM_MODIFICATIONS.tsv
```

Current source was authoritative. Deleted historical Markdown was not restored,
and Graphify was not used.

## Prerequisite Status

```yaml
P13_2_PrerequisiteStatus:
  branch: main
  head: 54741f8e5d4da5fea35eb96751b2b4cda10cde6d
  origin_main: 54741f8e5d4da5fea35eb96751b2b4cda10cde6d
  P13_1_committed: true
  git_index_empty: true
  product_tracked_status_clean: true
  product_tracked_files: 6137
  modification_register_rows: 19
  modification_register_columns: 18
  modification_register_hash_mismatches: 0
  semantic_tokens_present: 31
  immutable_brand_projection_present: true
  nested_product_git: false
  locked_upstream_clean: true
  locked_upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  product_UI_feature: disabled
  extension_modules: []
  registered_product_descriptors: 0
  prerequisite_result: pass
```

Allowed unrelated local paths were `.opencode/`, `AGENTS.md`, `graphify-out/`
and ignored `9_artifacts/hermes/**`. No stop rule fired.

## Selected Shell Architecture

P13.2 implements the P13.0 Model B decision:

```text
Existing Hermes shell and router
  -> product-owned pure shell contracts
  -> one localized App composition seam
```

The existing sidebar, mobile drawer, React Router tree, profile scope, page
header provider, theme/language controls, plugin loader and system-action area
remain authoritative. No second shell or route root exists.

## Existing Shell Baseline

| Existing shell capability | Reused authority | P13.2 treatment |
| --- | --- | --- |
| Application root and providers | Existing `App`, product configuration provider, profile scope and page-header provider | Reused unchanged; no second root/provider tree |
| Router | Existing React Router `Routes` composition in `App.tsx` | Reused; product descriptors remain empty |
| Desktop sidebar | Existing responsive/collapsible sidebar and persistence key | Reused; semantic groups compose inside it |
| Mobile navigation | Existing fixed header, overlay, drawer, Escape handling and close behavior | Reused; product lockup replaces only visible brand content when identity exists |
| Theme and i18n | Existing theme and translation contexts | Reused; active theme remains style authority and existing translated route labels remain active |
| Profile scope | Existing profile selector, scope banner and keyed route remount | Reused without behavior change |
| Dynamic plugins | Existing loader, route/page component and slots | Reused with protected-namespace filtering at shell composition only |

No new application root, router, sidebar, mobile-navigation implementation,
profile system, theme provider, i18n provider or plugin loader was created.

## Product Brand Lockup

`ProductBrandLockup` accepts only the immutable P13.1
`ProductBrandIdentity`, an explicit caller-supplied fallback and a responsive
variant.

```yaml
ProductBrandLockupContract:
  identity_source: createProductBrandIdentity(ProductConfiguration)
  product_name: identity.product.displayName
  product_version: identity.product.version
  upstream_name: identity.upstream.displayName
  upstream_version: identity.upstream.version
  upstream_commit: identity.upstream.commit
  upstream_short_commit: identity.upstream.shortCommit
  sidebar:
    product_name_visible: true
    product_version_visible: true
    upstream_name_and_version_visible: true
    full_upstream_commit_available_as_title: true
  mobile:
    product_name_visible: true
    compact_product_and_upstream_detail_visible: true
    short_upstream_commit_visible: true
  null_identity:
    exact_caller_fallback_returned: true
    synthetic_identity_created: false
```

The desktop fallback remains the prior two-line `Hermes Agent` treatment and
the mobile fallback remains `t.app.brand`. The existing desktop collapsed class
hides the lockup, while mobile and expanded desktop render it. React text
escaping is retained; no HTML injection, logo, image, font, URL or hardcoded
production identity was added.

The lockup consumes the P13.1 display-font and muted-text semantic tokens while
the active Hermes theme remains palette and typography authority.

## Navigation Groups

Four stable group definitions exist in this order. IDs remain constants while
identity-bearing visible labels are supplied by `App.tsx` from the immutable
`ProductBrandIdentity` projection:

| ID | Visible label source | Membership rule |
| --- | --- | --- |
| `agent-platform` | `ProductBrandIdentity.product.displayName` | Statically compiled product navigation with `groupId: "agent-platform"` only |
| `hermes-tools` | `ProductBrandIdentity.upstream.displayName + " Tools"` | `/chat`, `/sessions`, `/files`, `/models`, `/cron`, `/skills` |
| `extensions` | Neutral `Extensions` label | Accepted dynamic plugin tabs after protected-namespace filtering |
| `administration` | Neutral `Administration` label | Remaining existing core navigation, including conditional Analytics |

Empty groups are omitted. Consequently, with product UI disabled and no static
descriptors registered, AGENT PLATFORM is not rendered. Hermes Tools and
Administration retain existing item order. Dynamic plugin position hints are
resolved by the existing merge logic before accepted plugin items are placed in
Extensions, preserving their relative order.

`navigation.ts` contains no hardcoded `"AGENT PLATFORM"`, `"Hermes Tools"` or
`"Hermes Agent"` visible label. With valid configuration, `App.tsx` passes
`productBrandIdentity.product.displayName` for the product group and
``${productBrandIdentity.upstream.displayName} Tools`` for Hermes tools. The
existing localized `t.app.brand` is used only as the null-configuration label
fallback; a null configuration cannot resolve any product extension, so it
cannot expose a synthetic product group.

Exact implementation/test evidence:

| Requirement | Source evidence | Test evidence |
| --- | --- | --- |
| Product label derives from product identity | `web/src/App.tsx` `shellNavigationLabels["agent-platform"]` | `shell.test.tsx` expects the synthetic `identity.product.displayName` group label |
| Tools label derives from upstream identity plus neutral suffix | `web/src/App.tsx` `shellNavigationLabels["hermes-tools"]` | `shell.test.tsx` expects ``${identity.upstream.displayName} Tools`` |
| Navigation owns stable IDs, not identity strings | `navigation.ts` receives `Readonly<Record<ShellNavigationGroupId, string>>` | Source assertion rejects the three hardcoded identity-label literals |

Existing route paths, route elements, direct deep links, conditional Analytics,
profile behavior, theme/language controls, system actions, mobile close behavior
and persisted collapse behavior are unchanged.

## Existing Route Preservation

The existing route table remains owned by `App.tsx`. P13.2 changed no route
path or page component and removed no primary entry.

```yaml
P13_2_ExistingRoutePreservation:
  built_in_paths_preserved:
    - /
    - /chat
    - /sessions
    - /files
    - /analytics
    - /models
    - /logs
    - /cron
    - /skills
    - /plugins
    - /mcp
    - /pairing
    - /channels
    - /webhooks
    - /system
    - /profiles
    - /profiles/new
    - /config
    - /env
    - /docs
  bundled_plugin_paths_observed: [/achievements, /kanban]
  existing_primary_routes_lost: 0
  existing_route_paths_changed: false
  product_route_registered: false
```

Grouping changes presentation only. Existing relative order inside each group,
direct links, unknown-route fallback, plugin route composition, persistent Chat
host behavior and page-title resolution remain intact.

## Static Descriptor Hardening

`ProductExtensionNavigation` now requires the literal group ID
`agent-platform`. Runtime validation rejects a descriptor when:

- its route is outside `/agent-platform/`;
- it claims the namespace root rather than a reviewed descendant;
- it contains percent encoding, a backslash, dot segment, wildcard, query,
  fragment, repeated slash or trailing slash;
- its route duplicates another descriptor or a reserved built-in path;
- its route pattern is ambiguous with another static descriptor at the same
  segment depth, including dynamic-segment and case-insensitive overlap;
- its navigation group is not `agent-platform`;
- its before/after anchor is not an existing built-in route.

Configuration order and existing before/after/end placement remain stable. A
resolved product navigation item carries the reviewed group ID into shell
composition.

## Dynamic Namespace Protection

Dynamic dashboard plugins remain operator-trusted and are not valid authority
for mandatory product routes. P13.2 filters any manifest whose `tab.path` or
`tab.override` claims `/agent-platform` or a descendant.

Literal comparison is case-insensitive, attempts safe URI decoding, applies
WHATWG URL path canonicalization and collapses repeated slashes. Backslash-
equivalent claims are also recognized. Accepted patterns must begin with a
fixed, non-product top-level segment. Malformed encoding, control/space,
optional, dynamic or wildcard syntax in that segment fails closed because it
may match the protected root or a descendant under React Router grammar.
Near-prefix paths such as `/agent-platform-other` remain outside the protected
namespace.

Only accepted manifests participate in:

```text
chat override resolution
sidebar navigation partitioning
route composition
page-title/plugin-tab metadata
```

Rejected manifest details are not logged. `App.tsx` emits one aggregate warning
containing only the blocked-manifest count and a generic protected-namespace
reason.

This is a route/navigation/title ownership boundary, not a plugin sandbox.
`usePlugins()` fetches manifests and loads declared JavaScript/CSS before App
composition can filter them. Registered plugin slots also remain available.
P13.2 therefore makes no claim that rejected manifest code or CSS did not load;
it only prevents protected path and override claims from entering shell
composition.

## Implementation Path Set

Created product-owned files:

```text
2_products/hermes-agent/web/src/agent-platform/shell/brand-lockup.tsx
2_products/hermes-agent/web/src/agent-platform/shell/index.ts
2_products/hermes-agent/web/src/agent-platform/shell/navigation.ts
2_products/hermes-agent/web/src/agent-platform/shell/shell.test.tsx
```

Modified product-owned source:

```text
2_products/hermes-agent/web/src/agent-platform/extensions.ts
2_products/hermes-agent/web/src/agent-platform/extensions.test.ts
```

Modified upstream-derived integration source:

```text
2_products/hermes-agent/web/src/App.tsx
```

Modified product control:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

No additional product path was needed.

## Upstream-Derived Edit Boundary

Exactly one upstream-derived source file is modified:

| Path | Baseline source object | Baseline SHA-256 | Current SHA-256 | Bounded edit |
| --- | --- | --- | --- | --- |
| `web/src/App.tsx` | `79f7e4853504663289906caf29f70173da134857` | `ccccbb3f3d1ae54c54c303b994b052bc66926ace2204bfb12a4c360f550694db` | `6be444c2cfc975df6095638898e6e9be9e7b2cb277e086053894579b41038506` | Consume product brand identity, supply identity-derived group labels, filter protected manifests and render semantic groups at the existing shell seam |

All pure identity presentation, navigation grouping, namespace protection and
tests remain under `web/src/agent-platform/**`. No second upstream-derived file
was edited, and the immutable upstream tree remains unchanged.

## Modification-Register Reconciliation

```yaml
HermesP13_2ModificationRegister:
  previous_rows: 19
  new_rows: 4
  cumulative_rows_updated: 3
  final_rows: 23
  columns: 18
  added_ids: [P13.2-001, P13.2-002, P13.2-003, P13.2-004]
  cumulative_ids: [P12.6-008, P12.6-010, P12.6-013]
  duplicate_ids: 0
  duplicate_paths: 0
  required_field_failures: 0
  current_hash_mismatches: 0
  upstream_derived_new_modifications: 0
  self_exempt_register_model: retained
```

The existing extension, extension-test and App rows retain their original IDs,
owners, baseline commit/source objects and rollback models. Their current
hashes, cumulative intents, validation lanes, security impacts, retirement
conditions and approval lineage now record P13.2 participation.

Current product hashes:

| ID | Path | SHA-256 |
| --- | --- | --- |
| P12.6-013 | `web/src/App.tsx` | `6be444c2cfc975df6095638898e6e9be9e7b2cb277e086053894579b41038506` |
| P12.6-008 | `web/src/agent-platform/extensions.ts` | `d287d74aa147bcc70bab3250dd137f8285b93a7912388159a50408812cd5a661` |
| P12.6-010 | `web/src/agent-platform/extensions.test.ts` | `41521db02bec72e3432f602c3d4ee694c74b2e165decbc5f3bda995f8ee38205` |
| P13.2-001 | `web/src/agent-platform/shell/brand-lockup.tsx` | `85d5acbee5cfb99c905e076c4d278f65d52073fb7341e9da388ea44a93b3502a` |
| P13.2-002 | `web/src/agent-platform/shell/index.ts` | `8ce7b9d1c43f56d2ac624e62629f90757ca9f44382238f51f89fb526fa4dd763` |
| P13.2-003 | `web/src/agent-platform/shell/navigation.ts` | `a91970b3382fd296f6b0cf45db862ceb65e2d63708dd87d3bb5c87988c3a728e` |
| P13.2-004 | `web/src/agent-platform/shell/shell.test.tsx` | `7f26d74cf20128eda894886f8d723f057ade585fd6277070866b7e06ba7b36e9` |

## Validation Results

| Lane | Result | Evidence |
| --- | --- | --- |
| Targeted P13.2 Vitest | Pass | 2 files, 14 tests passed |
| Full dashboard Vitest | Pass | 10 files, 67 tests passed |
| Dashboard TypeScript | Pass | `tsc -p . --noEmit` |
| Product-owned affected ESLint | Pass | Extension source/tests and all shell files |
| Localized App ESLint | Pass with inherited-rule isolation | No finding when the pre-existing `react-hooks/set-state-in-effect` finding at current `App.tsx:985` is disabled |
| Production dashboard build | Pass | 493 modules transformed; integrated assets emitted |
| Windows-footgun scanner | Pass | 755 Python files scanned; no findings |
| Register reconciliation | Pass | 23 rows, 18 columns, zero duplicates, missing fields or hash mismatches |
| Product count | Pass | 6,137 tracked before human commit; four additions project 6,141 |
| Runtime HTTP/auth | Pass | Root/status/product/plugin endpoints 200; unauthenticated product endpoint 401 |
| Product activation boundary | Pass | Product UI disabled, zero extension modules and zero static descriptors |
| Source/lock drift | Pass | Prohibited source, manifests, dependencies and locks unchanged |
| Immutable upstream | Pass | No upstream change |
| Diff whitespace | Pass | `git diff --check` produced no error |
| Independent constrained review | Pass after correction | Broad/optional/dynamic/wildcard claims, static canonicalization escapes and mobile-visible commit coverage were found, corrected, adversarially retested and revalidated |

The first targeted test attempt exposed the existing OneDrive-untrusted
`node_modules/@hermes/shared` junction and failed import collection. Final
targeted/full validation used a temporary plain copy of the already tracked
`apps/shared` package without installing or changing dependencies, then
restored the original junction exactly.

Unfiltered ESLint of the whole App continues to report the inherited
synchronous state update in `SidebarSystemActions` at current line 985. That
code is outside the P13.2 diff. App was also linted with only that existing rule
finding disabled and had no additional finding.

The build retained its existing large-chunk warning. No new dependency,
manifest or lockfile warning was introduced.

## Provider-Null Runtime Verification

The integrated dashboard ran on `127.0.0.1:9122` with isolated `HERMES_HOME`,
`HOME`, `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, `TEMP`, `TMP` and browser
profiles. The token was synthetic, external proxies resolved to a failing
loopback endpoint, headless browser host resolution blocked non-loopback hosts
and a synthetic future update cache prevented update access.

```yaml
P13_2_ProviderNullRuntimeVerification:
  command: .venv/Scripts/python.exe -m hermes_cli.main dashboard --host 127.0.0.1 --port 9122 --no-open --skip-build
  ready_sentinel_observed: true
  root_HTTP: 200
  root_bytes: 708
  status_HTTP: 200
  product_configuration_HTTP: 200
  unauthenticated_product_configuration_HTTP: 401
  plugin_manifest_HTTP: 200
  product_id: agent-platform-hermes
  product_version: 0.1.0-dev
  upstream_product_name: Hermes Agent
  upstream_version: 0.18.2
  product_UI_feature: disabled
  extension_modules: []
  registered_product_descriptors: 0
  gateway_running: false
  active_agents: 0
  active_sessions: 0
  bundled_plugin_routes_observed: [/achievements, /kanban]
  provider_request_attempted: false
  worker_or_agent_execution_performed: false
  external_network_operation_performed: false
  isolated_state_removed: true
```

Loading the existing persistent Chat host repeated the inherited native-Windows
`WinError 448` on the OneDrive `node_modules/@hermes/ink` junction before a TUI,
worker or agent could spawn. This known runtime issue did not affect shell,
ordinary pages or HTTP evidence.

Windows refused graceful console-tree termination. The exact owned dashboard
launcher/child tree required the documented forced fallback. Port 9122 closed
and all isolated state, logs, screenshots, browser profiles and synthetic token
material were removed.

## Visual Verification

An initial disposable desktop capture exposed product-name truncation. The
lockup typography was corrected, full tests/build were rerun and final desktop
and mobile captures showed the complete intended identity treatment.

The human then inspected the final isolated dashboard at port 9122 and accepted
all required states:

```yaml
P13_2_HumanVisualVerification:
  desktop_expanded_checked: true
  desktop_collapsed_checked: true
  mobile_header_checked: true
  mobile_drawer_checked: true
  dark_theme_checked: true
  light_theme_checked: true
  complete_product_identity_checked: true
  product_and_upstream_versions_checked: true
  collapsed_lockup_hidden_checked: true
  AGENT_PLATFORM_empty_group_absent_checked: true
  Hermes_Tools_group_checked: true
  Extensions_group_checked: true
  Administration_group_checked: true
  route_and_relative_item_order_checked: true
  visual_result: pass
```

No real user state, provider credential, external browser profile or network
resource was used.

## Accessibility Verification

```yaml
P13_2_AccessibilityVerification:
  existing_nav_landmark_preserved: true
  existing_navigation_accessible_name_preserved: true
  semantic_groups_use_role_group: true
  semantic_groups_reference_visible_headings: true
  collapsed_links_retain_accessible_labels: true
  collapsed_tooltips_and_keyboard_focus_preserved: true
  mobile_open_close_accessible_names_preserved: true
  mobile_expanded_state_and_controls_preserved: true
  text_first_identity_uses_escaped_React_text: true
  identity_not_conveyed_by_color_alone: true
  reduced_motion_token_contract_preserved: true
  complete_assistive_technology_audit_deferred_to: P13.8
```

The correction changes group-label data only. Existing `nav`, `ul`/`li`,
`NavLink`, focus-ring, tooltip, drawer-control and keyboard behavior remains
unchanged. Product and upstream identities are visible text, not inferred from
an icon, color, monogram or inaccessible asset.

## Security and Trust Boundaries

P13.2 adds no raw HTML, dynamic import, filesystem discovery, provider field,
credential field, environment override, remote asset, external font, custom CSS
input, backend endpoint, public path or authorization bypass.

Product identity still comes only from the validated credential-free bootstrap
configuration. Static extensions remain compiled and configuration-selected.
Dynamic protected-path claims are removed from shell composition but dynamic
plugin JavaScript, CSS and slots remain inherited operator-trusted surfaces.

The aggregate warning does not include plugin names, labels, source locations,
paths or override values.

## Compatibility and Synchronization

The sole upstream-derived edit is localized to centralized App composition.
All pure branding, grouping, namespace matching and tests live in the product
namespace. This keeps future upstream review bounded to one existing high-
conflict integration file and three existing product-owned rows.

No existing route path, route component, profile target, sidebar persistence
key, mobile breakpoint, theme provider, language provider, plugin loader or
system action changed.

## Source and Lockfile No-Drift Verification

```yaml
P13_2_SourceAndLockfileNoDrift:
  immutable_upstream_changed: false
  main_tsx_changed: false
  index_css_changed: false
  themes_changed: false
  pages_changed: false
  shared_components_changed: false
  i18n_catalogs_changed: false
  backend_changed: false
  plugin_sources_changed: false
  package_manifests_changed: false
  dependency_lockfiles_changed: false
  product_feature_flags_changed: false
  extension_modules_changed: false
  product_descriptors_added: 0
  tracked_paths_outside_authorized_set_added: 0
```

Final Git/path checks confirmed that only the nine authorized P13.2 paths are
part of this change set. Existing unrelated `.opencode/`, `AGENTS.md` and
`graphify-out/` paths remain outside it. The index remains empty.

## Rollback

P13.2 rollback is bounded:

1. Restore `web/src/App.tsx`, `web/src/agent-platform/extensions.ts`,
   `web/src/agent-platform/extensions.test.ts` and
   `AGENT_PLATFORM_MODIFICATIONS.tsv` from parent commit
   `54741f8e5d4da5fea35eb96751b2b4cda10cde6d`.
2. Delete the four `web/src/agent-platform/shell/**` files created by P13.2.
3. Re-run dashboard tests, typecheck, affected lint and production build.
4. Verify the existing Hermes branding/flat-core-plus-plugin navigation returns,
   product UI remains disabled and no `/agent-platform/**` route exists.

No database, configuration, user-state, provider, worker or upstream rollback is
required.

## Limitations

- Dynamic plugin assets load before App can filter protected manifest claims;
  plugin slots remain unsandboxed and operator-trusted.
- Dynamic pattern protection is validated against the current React Router path
  grammar and must be revalidated when that grammar changes.
- Product and upstream group identity derives from `ProductBrandIdentity`;
  neutral `Tools`, `Extensions` and `Administration` suffix/labels remain
  English because P13.2 was prohibited from modifying i18n catalogs.
- The AGENT PLATFORM group is structurally ready but absent while product UI and
  all descriptors remain disabled.
- Branding remains text-first; no final logo, icon, trademark wording or public-
  release identity is approved.
- Complete accessibility/browser automation remains P13.8 work.
- The pre-existing App lint finding at current line 985 remains unresolved.
- The OneDrive shared-package junction required a temporary validation copy;
  the original junction was restored.
- The hidden Chat PTY reconnect/WinError 448 behavior and forced Windows shutdown
  fallback remain inherited runtime debt.
- The production build retains the existing large-chunk warning.
- No production-readiness, provider-readiness or external redistribution claim
  is made.

## Created / Modified / Generated / Removed / Not Created Register

Created tracked paths:

```text
0_architecture/governance/agent_platform_hermes_application_shell_navigation.md
2_products/hermes-agent/web/src/agent-platform/shell/brand-lockup.tsx
2_products/hermes-agent/web/src/agent-platform/shell/index.ts
2_products/hermes-agent/web/src/agent-platform/shell/navigation.ts
2_products/hermes-agent/web/src/agent-platform/shell/shell.test.tsx
```

Modified tracked paths:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
2_products/hermes-agent/web/src/App.tsx
2_products/hermes-agent/web/src/agent-platform/extensions.ts
2_products/hermes-agent/web/src/agent-platform/extensions.test.ts
```

Generated and retained only as ignored build output:

```text
2_products/hermes-agent/hermes_cli/web_dist/**
```

Generated and removed:

```text
9_artifacts/hermes/p13.2/runtime/**
temporary node_modules/@hermes/shared plain validation projection
temporary renamed junction holder; original junction restored
headless browser profiles and desktop/mobile screenshots
```

Not created, modified, activated or retained:

```text
additional governance Markdown
new routes, pages or product descriptors
new router, sidebar, plugin loader or provider
main.tsx, index.css, themes, pages, shared components or i18n catalogs
new palette, theme, font, logo, icon, image or remote asset
backend endpoints or configuration fields
provider, gateway, dispatcher, worker, agent, OAuth or MCP state
dependencies, manifests or lockfile changes
candidate checkout or synchronization workspace
real user state, credentials, cookies or browser profiles
Git staging, commits, refs or push state
```

## P13.3 Handoff

P13.3 may proceed from the accepted shell foundation under these exact bounds:

- P13.3 puede crear `/agent-platform/overview` como primer componente de
  página.
- P13.3 puede añadir un adaptador de estado read-only y un descriptor estático.
- P13.3 no puede activar `agent_platform.product_ui`.
- P13.3 no puede añadir `extension_modules` sin su gate aceptado.
- P13.3 no puede iniciar providers, workers, gateway ni agentes.
- P13.4 permanece bloqueado hasta la aceptación y commit de P13.3.

The first page must reuse the existing router/sidebar and P12.6 static
descriptor seam, stay under `/agent-platform/overview`, remain read-only, and
preserve every P13.2 namespace and no-activation boundary.

## Result Markers

```text
hermes_existing_application_shell_reused
hermes_existing_router_reused
hermes_existing_sidebar_reused
hermes_product_brand_lockup_ready
hermes_product_identity_visible_from_configuration
hermes_upstream_identity_attribution_preserved
hermes_text_first_shell_branding_ready
hermes_navigation_groups_ready
hermes_AGENT_PLATFORM_navigation_group_ready
hermes_Hermes_tools_navigation_group_ready
hermes_extensions_navigation_group_ready
hermes_administration_navigation_group_ready
hermes_product_route_namespace_reserved
hermes_static_product_namespace_validation_ready
hermes_dynamic_plugin_product_namespace_protected
hermes_existing_route_paths_preserved
hermes_mobile_shell_preserved
hermes_collapsed_sidebar_preserved
hermes_theme_compatibility_preserved
hermes_modification_register_reconciled
hermes_P13_3_ready
no_product_route_registered
no_product_UI_feature_activation
no_extension_module_activation
no_new_router_or_sidebar
no_provider_activation
no_worker_or_agent_execution
no_git_mutation_by_agent
```

## Final Verdict

```yaml
P13_2_HermesApplicationShellNavigationVerdict:
  P13_1_committed: true
  initial_repository_clean: true

  reuse:
    existing_application_root_reused: true
    existing_router_reused: true
    existing_sidebar_reused: true
    existing_mobile_navigation_reused: true
    existing_profile_scope_reused: true
    existing_theme_and_i18n_reused: true
    second_router_created: false
    second_sidebar_created: false
    second_plugin_loader_created: false

  branding:
    brand_lockup_created: true
    product_identity_source: ProductConfiguration
    product_tokens_consumed: true
    dual_product_upstream_identity_visible: true
    hardcoded_identity_constants: false
    final_logo_selected: false
    monogram_created: false
    null_configuration_preserves_Hermes_fallback: true

  navigation:
    semantic_navigation_groups_created: true
    agent_platform_group_ready: true
    agent_platform_group_initially_empty: true
    hermes_tools_group_ready: true
    extensions_group_ready: true
    administration_group_ready: true
    existing_route_paths_changed: false
    existing_primary_routes_lost: 0

  namespace:
    reserved_prefix: /agent-platform/
    static_product_paths_restricted_to_prefix: true
    dynamic_plugin_path_claims_blocked: true
    dynamic_plugin_override_claims_blocked: true
    dynamic_plugins_sandboxed_claimed: false

  implementation:
    product_additions: 4
    existing_product_owned_source_files_modified: 2
    upstream_derived_source_files_modified: 1
    modification_register_rows: 23
    product_tracked_files: 6141

  validation:
    targeted_tests_passed: true
    full_dashboard_tests_passed: true
    web_typecheck_passed: true
    affected_lint_passed: true
    inherited_App_lint_exception_present: true
    new_lint_regression_count: 0
    dashboard_build_passed: true
    provider_null_runtime_passed: true
    desktop_expanded_visual_check_passed: true
    desktop_collapsed_visual_check_passed: true
    mobile_shell_visual_check_passed: true
    dark_theme_visual_check_passed: true
    light_theme_visual_check_passed: true
    source_and_lockfiles_unchanged: true

  boundaries:
    product_UI_enabled: false
    extension_modules_added: false
    product_route_registered: false
    product_page_created: false
    provider_activation_performed: false
    worker_or_agent_execution_performed: false
    dependencies_changed: false

  sequencing:
    P13_3_may_proceed: true
    P13_4_may_proceed: false
    P13_4_requires_P13_3_acceptance: true
    P14_execution_remains_blocked: true
    P15_provider_enablement_remains_unauthorized: true

  execution:
    git_mutated_by_agent: false

  final_verdict: hermes_application_shell_navigation_ready_with_constraints
```

Binding constraints: product UI remains disabled, static product descriptors
remain empty, dynamic plugins remain unsandboxed operator-trusted code, no route
or page is activated, P13.3 may proceed only within the handoff above, and P13.4
remains blocked until P13.3 acceptance and commit.

## Human Commit Boundary

P13.2 did not stage, commit or push. After final human acceptance, stage exactly
the nine authorized paths:

```powershell
$Paths = @(
    "0_architecture/governance/agent_platform_hermes_application_shell_navigation.md",
    "2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv",
    "2_products/hermes-agent/web/src/App.tsx",
    "2_products/hermes-agent/web/src/agent-platform/extensions.ts",
    "2_products/hermes-agent/web/src/agent-platform/extensions.test.ts",
    "2_products/hermes-agent/web/src/agent-platform/shell/brand-lockup.tsx",
    "2_products/hermes-agent/web/src/agent-platform/shell/index.ts",
    "2_products/hermes-agent/web/src/agent-platform/shell/navigation.ts",
    "2_products/hermes-agent/web/src/agent-platform/shell/shell.test.tsx"
)

git add -- $Paths
git diff --cached --check
git diff --cached --stat
git commit -m "P13.2 - Add Hermes application shell navigation"
git push origin main
```

Never use `git add .`, `git add -A` or `git add -f`. Add, commit and push remain
human actions.
