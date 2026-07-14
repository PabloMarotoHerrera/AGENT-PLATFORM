# P13.1 - Hermes Design Tokens and Branding Foundation

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.1 - Design Tokens and Branding Foundation |
| Type | Bounded frontend implementation and governance record |
| Execution class | Product-owned frontend source, targeted validation and provider-null visual verification |
| Date | 2026-07-14 |
| Status | Ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_design_tokens_branding_foundation.md` |
| Product root | `2_products/hermes-agent` |
| Immutable upstream | `4_external/sources/hermes-agent` |
| Start commit | `c37abb4fa878ceb3a269f16b58b6016d122d5ea0` |
| Initial/final product count | 6,132 / projected committed 6,137 |
| Initial/final register rows | 14 / 19 |
| Upstream-derived source edits | Zero |
| Feature/route/navigation activation | Prohibited and not performed |
| Git mutation by agent | Prohibited and not performed |

## Purpose

Establish the minimum product-owned semantic token and text-first branding
foundation needed by P13.2 and later product surfaces while preserving the
existing Nous UI component library, Hermes ThemeProvider, active-theme palette,
dual product/upstream identity and fail-closed product configuration.

The implementation adds infrastructure only. Existing pages do not consume the
new aliases, the shell is visually unchanged, no brand asset is selected, and
P13.2 remains the owner of visible branding and shell composition.

## Scope

P13.1 creates exactly five files under
`web/src/agent-platform/design-system/**`, adds one stylesheet import to the
existing product configuration provider, updates the modification register and
creates this one governance record.

It does not modify upstream-derived source, `App.tsx`, `main.tsx`, `index.css`,
themes, components, pages, backend code, dependencies or locks. It adds no
route, navigation item, page, theme, palette, font, logo, asset, provider field,
credential field or runtime capability.

## Authoritative Inputs

Applied canonical records:

```text
0_architecture/governance/agent_platform_hermes_ui_product_brief_information_architecture.md
0_architecture/governance/agent_platform_hermes_product_extension_configuration_seams.md
0_architecture/governance/agent_platform_hermes_productization_foundation_closure.md
0_architecture/governance/agent_platform_hermes_baseline_build_test_ui_snapshot.md
0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md
```

Implementation authority inspected:

```text
web/src/index.css
web/src/themes/types.ts
web/src/themes/context.tsx
web/src/themes/presets.ts
web/src/themes/fonts.ts
web/src/themes/index.ts
web/src/components/**
web/src/agent-platform/product-config.ts
web/src/agent-platform/product-config-context.ts
web/src/agent-platform/product-config-provider.tsx
AGENT_PLATFORM_MODIFICATIONS.tsv
```

Current source was authoritative. Deleted historical Markdown was not restored,
and Graphify was not used.

## Prerequisite Status

```yaml
P13_1_PrerequisiteStatus:
  branch: main
  head: c37abb4fa878ceb3a269f16b58b6016d122d5ea0
  origin_main: c37abb4fa878ceb3a269f16b58b6016d122d5ea0
  P13_0_committed: true
  git_index_empty: true
  product_tracked_status_clean: true
  product_tracked_files: 6132
  product_tree: 274527e686fa50a320a92a5738e8c8c083669b24
  modification_register_rows: 14
  modification_register_hash_mismatches: 0
  nested_product_git: false
  locked_upstream_clean: true
  locked_upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  product_UI_feature: disabled
  extension_modules: []
  prerequisite_result: pass
```

Allowed unrelated local paths were `.opencode/`, `AGENTS.md`,
`graphify-out/` and ignored `9_artifacts/hermes/**`. No stop rule fired.

## Existing Design-System Baseline

| Existing capability | Current authority | P13.1 posture |
| --- | --- | --- |
| Components | `@nous-research/ui` plus existing dashboard components | Reuse; no parallel component library |
| Styling | Tailwind CSS 4, Nous CSS and shadcn-compatible aliases | Reuse as primitive/value authority |
| Themes | Existing Hermes ThemeProvider and eight built-in themes | Reuse unchanged |
| Palette | Active theme palette and optional existing theme overrides | Active theme remains authority |
| Typography | Theme font stacks, base size, line height, letter spacing and curated override | Inherit; add no font or URL |
| Layout | Theme radius, density multiplier and layout variants | Inherit; semantic spacing aliases only |
| Status colors | Existing primary/success/warning/destructive/muted roles | Alias without changing values |
| Responsive shell | Existing sidebar/mobile behavior | Unchanged; P13.2 owns shell work |
| Icons | Existing Lucide registry | Unchanged; no logo/monogram inferred |
| Terminal colors | Theme-specific terminal fields | Unchanged |

Existing operator-trusted external font URLs, theme asset URLs, custom CSS,
component-style strings, user YAML and dynamic plugin CSS remain inherited
trust surfaces. P13.1 neither consumes nor expands them.

## Selected Design Direction

```yaml
HermesProductDesignDirection:
  foundation: existing Hermes dashboard
  component_library: "@nous-research/ui"
  styling_system: Tailwind CSS 4 plus CSS custom properties
  theme_authority: existing Hermes ThemeProvider
  token_strategy: product-owned semantic aliases
  product_palette: inherited from active theme
  brand_strategy: text-first, configuration-derived
  product_logo: deferred
  product_icon: deferred
  product_font: inherited from active theme
  upstream_attribution: preserved
  visible_shell_integration: deferred to P13.2
```

The dependency direction is fixed:

```text
Existing Hermes/Nous primitives
        -> AGENT PLATFORM semantic aliases
        -> future P13 product components
```

No independent product palette, theme engine or component system exists.

## Semantic Token Architecture

The stable public CSS namespace is `--agent-platform-`. CSS remains the value
authority. TypeScript exposes only frozen token names and categories for tests,
future component contracts, documentation and controlled tooling.

The stylesheet is loaded once by the existing product configuration provider.
It defines only `:root` variables plus a reduced-motion media override. No
current selector consumes the variables, so loading the file changes no visual
behavior.

Semantic status roles do not grant operational authority. Future components
must pair status color with text, icon, accessible name or structured state.
Disabled/unavailable and warning/experimental may share initial values while
remaining semantically distinct tokens.

## Semantic Token Contract

| Category | Exact tokens | Count |
| --- | --- | ---: |
| Surface | `surface-canvas`, `surface-panel`, `surface-subtle`, `surface-elevated` | 4 |
| Text | `text-primary`, `text-secondary`, `text-muted`, `text-inverse` | 4 |
| Border/focus | `border-default`, `border-strong`, `focus-ring` | 3 |
| Action | `action-primary`, `action-primary-foreground` | 2 |
| Status | `status-success`, `status-warning`, `status-danger`, `status-info`, `status-disabled`, `status-unavailable`, `status-experimental` | 7 |
| Typography | `font-body`, `font-display`, `font-mono` | 3 |
| Shape | `radius-control`, `radius-panel` | 2 |
| Spacing | `space-1`, `space-2`, `space-3`, `space-4` | 4 |
| Motion | `motion-fast`, `motion-standard` | 2 |
| Total | All names prefixed `--agent-platform-` | 31 |

The catalog is deterministically ordered, frozen at both array and definition
levels, contains no duplicate and stores no CSS value.

## Token Derivation Map

| Product semantic role | Existing value authority |
| --- | --- |
| `--agent-platform-surface-canvas` | `var(--background-base)` |
| `--agent-platform-surface-panel` | `var(--color-card)` |
| `--agent-platform-surface-subtle` | `var(--color-muted)` |
| `--agent-platform-surface-elevated` | `var(--color-popover)` |
| `--agent-platform-text-primary` | `var(--color-foreground)` |
| `--agent-platform-text-secondary` | `var(--color-muted-foreground)` |
| `--agent-platform-text-muted` | 72% `--color-muted-foreground` mixed with transparency |
| `--agent-platform-text-inverse` | `var(--color-primary-foreground)` |
| `--agent-platform-border-default` | `var(--color-border)` |
| `--agent-platform-border-strong` | 30% `--midground-base` mixed with transparency |
| `--agent-platform-focus-ring` | `var(--color-ring)` |
| `--agent-platform-action-primary` | `var(--color-primary)` |
| `--agent-platform-action-primary-foreground` | `var(--color-primary-foreground)` |
| `--agent-platform-status-success` | `var(--color-success)` |
| `--agent-platform-status-warning` | `var(--color-warning)` |
| `--agent-platform-status-danger` | `var(--color-destructive)` |
| `--agent-platform-status-info` | `var(--color-primary)` |
| `--agent-platform-status-disabled` | `var(--color-muted-foreground)` |
| `--agent-platform-status-unavailable` | `var(--color-muted-foreground)` |
| `--agent-platform-status-experimental` | `var(--color-warning)` |
| `--agent-platform-font-body` | `var(--theme-font-sans)` |
| `--agent-platform-font-display` | `var(--theme-font-display)` |
| `--agent-platform-font-mono` | `var(--theme-font-mono)` |
| `--agent-platform-radius-control` | `var(--radius-md)` |
| `--agent-platform-radius-panel` | `var(--radius-lg)` |
| `--agent-platform-space-1` | `0.25rem * var(--theme-spacing-mul, 1)` |
| `--agent-platform-space-2` | `0.5rem * var(--theme-spacing-mul, 1)` |
| `--agent-platform-space-3` | `1rem * var(--theme-spacing-mul, 1)` |
| `--agent-platform-space-4` | `1.5rem * var(--theme-spacing-mul, 1)` |
| `--agent-platform-motion-fast` | `120ms`, reduced to `0ms` for reduced motion |
| `--agent-platform-motion-standard` | `180ms`, reduced to `0ms` for reduced motion |

No mapping deviation was required. `tokens.css` contains no hexadecimal,
RGB/RGBA/HSL/HSLA color, URL, import, font declaration, asset, product identity,
route selector, component class or global element restyling.

## Brand Identity Projection

`createProductBrandIdentity(configuration)` is a pure, side-effect-free
projection of validated `ProductConfiguration`:

```yaml
ProductBrandIdentity:
  product:
    id: configuration.productId
    displayName: configuration.productDisplayName
    version: configuration.productVersion
  upstream:
    displayName: configuration.upstreamProductName
    version: configuration.upstreamVersion
    commit: configuration.upstreamCommit
    shortCommit: first 12 characters of configuration.upstreamCommit
```

The outer object and both nested objects are frozen. The full upstream commit
is retained, the short form is deterministic, the source object is not mutated,
and null configuration returns null.

There is no frontend fallback identity, parsing of display names, DOM/network/
localStorage/theme access or hardcoded production name/version/commit.

Unavailable behavior:

```yaml
ProductBrandUnavailableBehavior:
  duplicate_default_identity: false
  synthetic_product_name: false
  synthetic_product_version: false
  product_brand_projection: null
  existing_Hermes_shell_fallback: unchanged
```

## Branding Constraints

```yaml
HermesP13_1BrandingConstraints:
  authoritative_product_name_source: ProductConfiguration.productDisplayName
  authoritative_product_version_source: ProductConfiguration.productVersion
  authoritative_upstream_name_source: ProductConfiguration.upstreamProductName
  authoritative_upstream_version_source: ProductConfiguration.upstreamVersion
  authoritative_upstream_commit_source: ProductConfiguration.upstreamCommit
  final_logo_selected: false
  logo_asset_added: false
  new_font_added: false
  independent_brand_palette_added: false
  Hermes_upstream_attribution_removed: false
  package_or_distribution_name_changed: false
```

Branding is text-first. P13.1 defines identity structure but no presentation
string such as "Powered by" or "Official", no trademark claim, no approved
public-release identity and no complete branding or asset-rights clearance.
P13.2 owns visible formatting and localization.

## Theme Compatibility

The structural test iterated every current `BUILTIN_THEMES` entry without
asserting a frozen collection size. Eight themes were observed:

```text
default
default-large
nous-blue
midnight
ember
mono
cyberpunk
rose
```

Every theme supplied background, midground, foreground, fontSans, fontMono,
baseSize, lineHeight, letterSpacing, radius and density. The semantic layer
therefore inherits palette, typography, shape and density from every current
built-in theme and will validate future additions through the same invariant.

Theme names/defaults/persistence, font selection, terminal colors, YAML
parsing, custom CSS, assets, layout variants and component-style overrides are
unchanged. Existing external fonts remain inherited operator-trusted behavior;
P13.1 adds and exposes none.

## Security and Trust Boundaries

P13.1 adds no external font or image URL, font file, remote asset, custom CSS
input, HTML injection, plugin script, dynamic import, filesystem discovery,
provider/credential/raw-config field, user-controlled CSS value or environment
override.

The CSS contains static semantic declarations only. The TypeScript catalog is
inert frozen metadata. Branding consumes only validated product configuration.
No value comes from environment variables, raw YAML, localStorage, providers,
plugin manifests, query parameters or Kanban state.

The existing theme escape hatches remain outside the AGENT PLATFORM branding
contract and are not re-exported by `design-system/index.ts`.

## Accessibility Foundation

```yaml
P13_1_AccessibilityFoundation:
  semantic_state_not_color_only: true
  focus_token_defined: true
  reduced_motion_supported: true
  system_font_fallback_preserved: true
  base_theme_scaling_preserved: true
  high_level_contrast_target:
    normal_text: WCAG_AA_4_5_to_1
    large_text_and_UI: WCAG_AA_3_to_1
```

The focus role inherits the active theme ring. Motion durations become zero
under `prefers-reduced-motion: reduce`. Typography and density remain active-
theme controlled. Status color alone is prohibited. This is a foundation, not
a complete accessibility audit; rendered-route and assistive-technology
validation remain P13.8 responsibilities.

## Implementation Path Set

Created product-owned files:

```text
2_products/hermes-agent/web/src/agent-platform/design-system/brand.ts
2_products/hermes-agent/web/src/agent-platform/design-system/index.ts
2_products/hermes-agent/web/src/agent-platform/design-system/tokens.css
2_products/hermes-agent/web/src/agent-platform/design-system/tokens.ts
2_products/hermes-agent/web/src/agent-platform/design-system/design-system.test.ts
```

Modified product-owned source:

```text
2_products/hermes-agent/web/src/agent-platform/product-config-provider.tsx
  added exactly one import of ./design-system/tokens.css
```

Modified product control:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

No additional product path was needed. The provider API, props, context and
rendering behavior are unchanged.

## Modification-Register Reconciliation

```yaml
HermesP13_1ModificationRegister:
  previous_rows: 14
  new_rows: 5
  final_rows: 19
  columns: 18
  added_ids: [P13.1-001, P13.1-002, P13.1-003, P13.1-004, P13.1-005]
  duplicate_paths: 0
  current_hash_mismatches: 0
  required_field_failures: 0
  upstream_derived_new_modifications: 0
  self_exempt_register_model: retained
```

The existing `P12.6-014` provider row retains its original modification ID,
P12.6 owner, upstream baseline, addition class and rollback target. Its current
hash, cumulative intent, reapplication condition, security impact, validation
lanes, retirement condition and approval lineage now record P13.1 stylesheet
participation. No duplicate provider path or multi-owner syntax was introduced.

New product hashes:

| ID | Path | SHA-256 |
| --- | --- | --- |
| P13.1-001 | `web/src/agent-platform/design-system/brand.ts` | `ae9b8de443d09af6ac86ed9acc041af36c6c98477cbd329ca338a5f1eb5f434d` |
| P13.1-002 | `web/src/agent-platform/design-system/index.ts` | `169d0c241540fd12298fc3c978977fe383f8a3e77fd06800e9d93621eca8f6aa` |
| P13.1-003 | `web/src/agent-platform/design-system/tokens.css` | `af4c41a6a788018a0f57d443bd83eb3e6e564951371c3e75d8dffb9129a081e9` |
| P13.1-004 | `web/src/agent-platform/design-system/tokens.ts` | `78e062844ab683eb9a4802b26f096d416a1e0104e6247585209ff00194763981` |
| P13.1-005 | `web/src/agent-platform/design-system/design-system.test.ts` | `6008faf17746838ef7260b722e75c9289a0e7f33222dbdc9e0212390f3b5ff58` |

Updated provider hash:

```text
57ce0592e70af42a4084d4e95ca294ba00f96d7dbf822d4d09d42bccaa8bcd25
```

## Validation Results

| Lane | Result | Evidence |
| --- | --- | --- |
| Targeted P13.1 Vitest | Pass | 1 file, 11 tests passed |
| Full dashboard Vitest | Pass | 9 files, 57 tests passed |
| Dashboard TypeScript | Pass | `tsc -p . --noEmit` |
| Affected ESLint | Pass | Four new TS files, test and provider checked |
| Production dashboard build | Pass | 487 modules transformed; integrated assets emitted |
| Windows-footgun scanner | Pass | 755 Python files scanned; no findings |
| Register reconciliation | Pass | 19 rows, 18 columns, zero mismatches |
| Built asset token check | Pass | One CSS asset; required normal tokens once, motion token twice including reduced-motion override |
| Route absence | Pass | No product route string in built CSS and extension registry remained empty |
| Source/lock drift | Pass | Prohibited source, manifests and locks unchanged |

The first targeted import attempt exposed the existing OneDrive-untrusted
`node_modules/@hermes/shared` junction and collected no tests. Validation used
a temporary plain copy of the already tracked `apps/shared` workspace package,
without installing or changing dependencies, then restored the original
junction exactly. The targeted and full final runs passed after that bounded
environment workaround.

The build retained its existing large-chunk warning. No new warning was
introduced or reclassified.

## Provider-Null Runtime Verification

The dashboard ran from integrated built assets on `127.0.0.1:9121` with
isolated `HERMES_HOME`, `HOME`, `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`,
`TEMP`, `TMP`, shared-auth and browser roots. The child environment was cleared,
the dashboard token was synthetic, external proxies were directed to a failing
loopback endpoint and a current synthetic update cache suppressed update access.

```yaml
P13_1_ProviderNullRuntimeVerification:
  command: .venv/Scripts/python.exe -m hermes_cli.main dashboard --host 127.0.0.1 --port 9121 --no-open --skip-build
  ready_sentinel_observed: true
  root_HTTP: 200
  root_bytes: 704
  status_HTTP: 200
  product_configuration_HTTP: 200
  unauthenticated_product_configuration_HTTP: 401
  product_id: agent-platform-hermes
  product_version: 0.1.0-dev
  upstream_product_name: Hermes Agent
  upstream_version: 0.18.2
  upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  product_UI_feature: disabled
  extension_modules: []
  gateway_running: false
  active_agents: 0
  active_sessions: 0
  provider_request_attempted: false
  worker_or_agent_execution_performed: false
  external_network_operation_performed: false
  isolated_state_removed: true
```

The human browser activated the existing persistently mounted Chat WebSocket,
which repeated the inherited native-Windows `WinError 448` junction failure
before any TUI or agent spawned. This known shell/runtime limitation did not
affect ordinary pages, themes, token loading or the provider-null verdict.

Windows refused graceful console-tree termination, so the exact owned launcher,
dashboard child and console host required the documented forced fallback. Port
`9121` closed and the full ignored runtime, token, logs, JSON and browser root
were removed.

## Manual Visual Verification

The human inspected the isolated UI through loopback/VS Code forwarding and
confirmed all required states:

```yaml
P13_1_ManualVisualVerification:
  actual_port: 9121
  default_Hermes_Teal_checked: true
  Nous_Blue_light_checked: true
  sidebar_expanded_checked: true
  sidebar_collapsed_checked: true
  ordinary_builtin_page_checked: true
  theme_switcher_checked: true
  existing_font_rendering_intact: true
  existing_focus_outline_visible: true
  visible_regression_observed: false
  unexpected_AGENT_PLATFORM_page: false
  route_change_observed: false
  duplicated_shell_observed: false
  broken_theme_variable_observed: false
  product_stylesheet_flash_observed: false
  theme_switching_intact: true
```

No external-font-dependent theme was required, and no browser profile, cookie,
session token, credential or real user theme state was retained.

## Source and Lockfile No-Drift Verification

No diff exists in:

```text
web/src/App.tsx
web/src/main.tsx
web/src/index.css
web/src/themes/**
web/src/components/**
web/src/pages/**
hermes_cli/**
package.json
package-lock.json
pyproject.toml
uv.lock
locked upstream
```

No dependency was installed or changed. The only existing product source edit
is the product-owned provider import. The five additions are product-owned.
Generated `hermes_cli/web_dist/**` remains ignored. Product UI defaults and the
empty static extension registry are unchanged.

The current Git index remains empty. Since the five additions are intentionally
untracked until the human boundary, `git ls-files` remains 6,132 now; the exact
human commit projects the required final tracked count of 6,137.

## Rollback Procedure

1. Require an empty index and identify the committed P13.1 commit and parent.
2. Remove only the five exact P13.1 design-system additions through an explicit
   revert.
3. Restore `web/src/agent-platform/product-config-provider.tsx` from the P13.1
   parent.
4. Restore `AGENT_PLATFORM_MODIFICATIONS.tsv` from the same parent.
5. Remove this canonical record only as part of that explicit revert commit.
6. Rebuild and verify no `--agent-platform-*` declaration remains in generated
   dashboard assets.
7. Verify tracked product count returns from 6,137 to 6,132.
8. Verify product tree equals the P13.1 parent tree.
9. Verify `agent_platform.product_ui` remains disabled and modules remain empty.
10. Preserve history; never use reset, clean, wildcard deletion or semantic
    rollback guesses.

`git reset --hard`, `git clean` and `git add .` are prohibited.

## P13.2 Handoff

P13.2 receives:

```text
31 stable --agent-platform-* semantic tokens
theme-adaptive values over existing Hermes/Nous variables
zero-duration reduced-motion aliases
immutable configuration-derived ProductBrandIdentity
full and short upstream commit fields
one bounded design-system export
globally loaded but currently unconsumed token stylesheet
no logo, palette, font or asset dependency
```

P13.2 may render `productDisplayName`, product/upstream version details, consume
semantic tokens, add navigation groups through the P12.6 central seam and
create the visible text-first lockup. It must not hardcode identity, invent a
logo, add another theme engine, replace Nous UI, rewrite all pages, remove
Hermes attribution or activate routes before its own gate.

P13.2 may proceed only after human acceptance and commit of P13.1. P13.3 remains
blocked until P13.2 acceptance.

## Limitations

- Branding remains text-first; no logo, icon, trademark wording or public-
  release identity is approved.
- Existing themes own palette and may carry inherited external-font, asset,
  custom-CSS and component-style trust boundaries outside this contract.
- The semantic variables are infrastructure and have no visible consumer yet.
- WCAG targets are established, but complete rendered contrast and assistive-
  technology validation remains P13.8 work.
- The OneDrive workspace package junction required a temporary plain-copy
  validation projection; the original junction was restored.
- The existing hidden Chat PTY reconnect issue and forced Windows shutdown
  fallback remain inherited runtime debt.
- The production build retains the existing large-chunk warning.
- Product UI stays disabled and no production-readiness claim is made.

## Created / Modified / Generated / Removed / Not Created Register

Created tracked paths:

```text
0_architecture/governance/agent_platform_hermes_design_tokens_branding_foundation.md
2_products/hermes-agent/web/src/agent-platform/design-system/brand.ts
2_products/hermes-agent/web/src/agent-platform/design-system/index.ts
2_products/hermes-agent/web/src/agent-platform/design-system/tokens.css
2_products/hermes-agent/web/src/agent-platform/design-system/tokens.ts
2_products/hermes-agent/web/src/agent-platform/design-system/design-system.test.ts
```

Modified tracked paths:

```text
2_products/hermes-agent/web/src/agent-platform/product-config-provider.tsx
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

Generated and retained only as ignored build output:

```text
2_products/hermes-agent/hermes_cli/web_dist/**
```

Generated and removed:

```text
9_artifacts/hermes/p13.1/runtime/**
temporary node_modules/@hermes/shared plain validation projection
temporary renamed junction holder; original junction restored
```

Not created, modified, activated or retained:

```text
additional governance Markdown
upstream-derived source edits
routes, pages, navigation or shell branding
new palette, theme, font, logo, icon, image or remote asset
theme provider/preset/YAML/custom-CSS behavior
provider, gateway, dispatcher, worker, agent, OAuth or MCP state
dependencies, manifests or lockfile changes
candidate checkout or synchronization workspace
real user state, credentials, cookies or browser profiles
Git staging, commits, refs or push state
```

## Result Markers

```text
hermes_existing_design_system_reused
hermes_Nous_UI_reuse_confirmed
hermes_theme_provider_reuse_confirmed
hermes_product_semantic_token_layer_ready
hermes_product_token_catalog_ready
hermes_31_semantic_tokens_verified
hermes_theme_adaptive_tokens_verified
hermes_reduced_motion_tokens_verified
hermes_product_brand_projection_ready
hermes_product_identity_derived_from_configuration
hermes_dual_product_upstream_identity_preserved
hermes_no_duplicate_identity_constants
hermes_no_parallel_design_system
hermes_no_independent_brand_palette
hermes_no_new_font_or_remote_asset
hermes_all_builtin_themes_structurally_compatible
hermes_design_system_tests_passed
hermes_dashboard_build_preserved
hermes_provider_null_branding_foundation_verified
hermes_modification_register_reconciled
hermes_P13_2_ready
no_product_UI_feature_activation
no_route_or_navigation_change
no_upstream_derived_source_modification
no_provider_activation
no_worker_or_agent_execution
no_git_mutation_by_agent
```

## Final Verdict

```yaml
P13_1_HermesDesignTokensBrandingFoundationVerdict:
  P13_0_committed: true
  initial_repository_clean: true

  reuse:
    Nous_UI_reused: true
    Hermes_theme_provider_reused: true
    existing_theme_variables_reused: true
    parallel_design_system_created: false
    independent_theme_engine_created: false

  tokens:
    semantic_token_layer_created: true
    semantic_token_count: 31
    token_namespace: --agent-platform-
    undocumented_token_count: 0
    duplicate_token_count: 0
    hardcoded_color_count: 0
    external_URL_count: 0
    font_declaration_count: 0
    reduced_motion_supported: true
    theme_adaptive: true

  branding:
    branding_projection_created: true
    product_identity_source: ProductConfiguration
    duplicate_identity_constants: false
    dual_product_upstream_identity_preserved: true
    text_first_branding: true
    final_logo_selected: false
    logo_asset_added: false
    new_font_added: false
    independent_brand_palette_added: false

  implementation:
    product_additions: 5
    existing_product_source_files_modified: 1
    upstream_derived_source_files_modified: 0
    modification_register_rows: 19
    product_tracked_files: 6137

  validation:
    targeted_tests_passed: true
    full_dashboard_tests_passed: true
    web_typecheck_passed: true
    affected_lint_passed: true
    dashboard_build_passed: true
    built_asset_tokens_verified: true
    provider_null_runtime_passed: true
    dark_theme_visual_check_passed: true
    light_theme_visual_check_passed: true
    source_and_lockfiles_unchanged: true

  boundaries:
    product_UI_enabled: false
    extension_modules_added: false
    route_added: false
    navigation_changed: false
    provider_activation_performed: false
    worker_or_agent_execution_performed: false
    dependencies_changed: false

  sequencing:
    P13_2_may_proceed: true
    P13_3_may_proceed: false
    P13_3_requires_P13_2_acceptance: true
    P14_execution_remains_blocked: true
    P15_provider_enablement_remains_unauthorized: true

  execution:
    git_mutated_by_agent: false

  final_verdict: hermes_design_tokens_branding_foundation_ready_with_constraints
```

Binding constraints: branding is text-first, no final logo is selected, the
active Hermes theme remains palette authority, the tokens are infrastructure
rather than a visible redesign, product UI remains disabled and P13.2 owns
visible shell branding.

## Human Commit Boundary

P13.1 did not stage, commit or push. After human acceptance, stage exactly the
eight authorized paths:

```powershell
$Paths = @(
    "0_architecture/governance/agent_platform_hermes_design_tokens_branding_foundation.md",
    "2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv",
    "2_products/hermes-agent/web/src/agent-platform/product-config-provider.tsx",
    "2_products/hermes-agent/web/src/agent-platform/design-system/brand.ts",
    "2_products/hermes-agent/web/src/agent-platform/design-system/index.ts",
    "2_products/hermes-agent/web/src/agent-platform/design-system/tokens.css",
    "2_products/hermes-agent/web/src/agent-platform/design-system/tokens.ts",
    "2_products/hermes-agent/web/src/agent-platform/design-system/design-system.test.ts"
)

git add -- $Paths
git diff --cached --check
git diff --cached --stat
git commit -m "P13.1 - Add Hermes design tokens and branding foundation"
git push origin main
```

Never use `git add .`, `git add -A` or `git add -f`. Add, commit and push remain
human actions.
