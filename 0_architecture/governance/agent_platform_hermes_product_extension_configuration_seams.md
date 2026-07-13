# P12.6 - Hermes Product Extension and Configuration Seams

## Document Header

| Field | Value |
| --- | --- |
| Project | P12 - Hermes Productization Foundation |
| Ticket | P12.6 - Hermes Product Extension and Configuration Seams |
| Status | `product_extension_configuration_seams_ready` |
| Date | 2026-07-13 |
| Product root | `2_products/hermes-agent` |
| Upstream reference | `4_external/sources/hermes-agent` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_product_extension_configuration_seams.md` |
| Modification register | `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Start commit | `dcc110229e2fbc7e45095a129ced3976793b5200` |
| Initial product tree | `07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7` |
| Upstream commit | `9de9c25f620ff7f1ce0fd5457d596052d5159596` |
| Execution actor | OpenCode agent under human commit control |

## Purpose

P12.6 establishes the minimum stable product identity, validated configuration,
feature-state, backend transport and dashboard route/navigation extension seams
required before P13 product UI work. It introduces the first deliberate AGENT
PLATFORM divergence while preserving explicit synchronization intent.

This ticket does not redesign the dashboard, enable a provider, add a product
page, implement an adapter, synchronize upstream, alter dependencies or change
upstream package version metadata.

## Prerequisite Gate

| Gate | Evidence | Result |
| --- | --- | --- |
| P12.2 committed | `e3455d9135096e1901f563359d7911abbf3d4bbc` | Pass |
| P12.3 committed | `0b5ea15bc2ce8d36b0218eb3d03639944637ffb7` | Pass |
| P12.4 committed | `a7328ac6ce67227243a9daad43d65c424fe22565` | Pass |
| P12.5 committed | `dcc110229e2fbc7e45095a129ced3976793b5200` | Pass |
| Branch | `main` | Pass |
| Accepted main | `HEAD == origin/main == dcc110229e2fbc7e45095a129ced3976793b5200` | Pass |
| Initial index | Zero staged paths | Pass |
| Initial product status | Zero modified or untracked product paths | Pass |
| Initial tracked count | 6,120 | Pass |
| Initial product tree | `07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7` | Pass |
| Nested product Git | None | Pass |
| P12.2 records | All accepted SHA-256 values matched | Pass |
| P12.3 manifests and locks | All accepted SHA-256 values matched | Pass |
| Locked upstream | Clean at exact commit and tag `v2026.7.7.2` | Pass |
| Candidate checkout | Absent | Pass |
| Synchronization workspace | Absent | Pass |
| Prior modification register | Absent, as required before first divergence | Pass |

Permitted unrelated untracked paths remained `.opencode/`, `AGENTS.md` and
`graphify-out/`. They were not inspected, modified or staged for P12.6.

## Initial Product Identity

```yaml
P12_6_InitialProductIdentity:
  main_commit: dcc110229e2fbc7e45095a129ced3976793b5200
  origin_main_commit: dcc110229e2fbc7e45095a129ced3976793b5200
  product_tree: 07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7
  product_tracked_files: 6120
  product_status_paths: 0
  staged_paths: 0
  upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  upstream_status_paths: 0
```

## Product Extension Principles

```yaml
HermesProductExtensionPrinciples:
  composition_over_scattered_patchwork: true
  product_owned_files_preferred: true
  existing_upstream_seams_reused_when_stable: true
  one_integration_point_per_subsystem_preferred: true
  configuration_is_explicit_and_validated: true
  features_default_disabled: true
  secrets_excluded_from_product_configuration: true
  provider_configuration_separate: true
  dynamic_arbitrary_code_loading: prohibited
  stable_identifiers_required: true
  deterministic_registration_order_required: true
  synchronization_intent_registered: true
  baseline_regression_required: true
```

The implementation adds product-owned modules and only three localized edits to
upstream-derived source. Existing Hermes provider, plugin, user configuration,
skill, worker and runtime registries are not reused as product UI registries.

## Bounded Source Inspection

Inspection was limited to configuration and environment loading, FastAPI app
construction and auth, dashboard bootstrap, routes/navigation, API transport,
identity/version surfaces, plugin registries, `apps/shared`, TUI theming,
desktop bootstrap/version handling and relevant tests/build configuration.
Unrelated skill implementations were not inspected. Graphify was not used.

Important source findings:

- `hermes_cli/config.py` merges broad user and managed configuration, may create
  Hermes home state and can contain provider/secret references. It is not a safe
  product metadata authority.
- `hermes_cli/main.py` loads existing Hermes environment sources before the
  dashboard server is dispatched. P12.6 therefore guarantees that its own
  loader and endpoint do not consult or expose those sources; it does not claim
  to replace upstream process startup.
- `hermes_cli/web_server.py` constructs the FastAPI app and already composes
  routers near `app = FastAPI(...)`. This is the narrow backend integration
  point.
- `/api/status` is public, operational, profile-sensitive and reads unrelated
  runtime state. It is not extended.
- `web/src/lib/api.ts::fetchJSON` already supplies base-path, session-header,
  cookie-auth and reauthentication behavior. It is reused without modification.
- `web/src/main.tsx` previously mounted React immediately. Pre-mount loading
  prevents feature-route deep links from racing an asynchronous route table.
- `web/src/App.tsx` centrally composes built-in route and navigation tables with
  dashboard plugins. Product descriptors can be inserted once before plugins.
- Existing dashboard plugins dynamically load reviewed external scripts and
  CSS. That executable trust model is not reused for first-party product routes.
- TUI identity currently combines local defaults with gateway skin overrides.
  Desktop identity spans Electron, package, renderer, native resource and
  translation layers. Partial adoption would create divergent constants.

## Extension Seam Candidate Inventory

| seam_id | current_path_or_component | current_owner | current_extension_mechanism | stability | reuse_decision | required_existing_file_edits | synchronization_risk | rationale |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| `backend_user_config` | `hermes_cli/config.py` | upstream | Broad defaults, user YAML, environment expansion and managed overlay | high_conflict | defer | 0 | high | Contains unrelated provider/user state and is not a strict product schema. |
| `backend_status_response` | `hermes_cli/web_server.py::get_status` | upstream | Public operational response | high_conflict | defer | 0 | high | Public liveness and runtime state must not become product bootstrap authority. |
| `backend_product_router` | `hermes_cli/agent_platform/routes.py` plus FastAPI router inclusion | mixed | Product-owned APIRouter composed once into upstream app | stable | create_new | 1 | medium | Narrow protected GET avoids broad status/config edits. |
| `product_schema` | `hermes_cli/agent_platform/product_config.py` | AGENT_PLATFORM | Strict Pydantic model over tracked defaults | stable | create_new | 0 | low | One credential-free Python truth defines identity and feature state. |
| `frontend_transport` | `web/src/lib/api.ts::fetchJSON` | upstream | Authenticated typed JSON transport | stable | adopt_existing | 0 | low | Reuses base path, cookie and session-token behavior. |
| `frontend_bootstrap` | `web/src/main.tsx` | mixed | Load once before React mount, then provide nullable context | stable | extend_existing | 1 | medium | Prevents route-table races and avoids duplicated frontend defaults. |
| `frontend_configuration_context` | `web/src/agent-platform/product-config-context.ts` and provider | AGENT_PLATFORM | Immutable application bootstrap context | stable | create_new | 0 | low | Future product components consume one validated instance. |
| `frontend_route_navigation` | `web/src/App.tsx` | mixed | Built-ins, then static product descriptors, then dashboard plugins | high_conflict | extend_existing | 1 | high | Existing centralized composition is preferable to edits across pages and shell. |
| `dashboard_plugin_runtime` | `web/src/plugins/**` | upstream | Runtime script/CSS manifests and component registration | provisional | defer | 0 | high | Executable plugin loading is the wrong trust boundary for product-owned routes. |
| `tui_skin_identity` | `ui-tui/src/theme.ts` and gateway skin events | upstream | Local defaults overridden by data-only gateway skin | stable | defer | 0 | medium | P12.6 is not an adapter ticket; partial identity adoption would duplicate truth. |
| `desktop_identity` | `apps/desktop` renderer, Electron and package metadata | upstream | Multiple compile-time and native identity sources | high_conflict | defer | 0 | high | Requires one later atomic adapter and explicit client/core/backend version facets. |
| `shared_package` | `apps/shared/src/index.ts` | upstream | JSON-RPC and WebSocket transport exports | stable | defer | 0 | medium | Adding identity now would force package/export and consumer changes with no P12.6 need. |

## Seam Decision Matrix

| Seam | Decision | Implementation or posture |
| --- | --- | --- |
| Product identity | Create product-owned validated authority | `ProductConfiguration` holds product and locked upstream identity separately. |
| Configuration source | Tracked Python defaults | `_PRODUCT_DEFAULTS` in `hermes_cli/agent_platform/product_config.py`. |
| Configuration precedence | Closed, single tracked tier | No environment, user, managed, provider or runtime override is accepted in P12.6. |
| Backend configuration | New narrow protected GET | `GET /api/agent-platform/product-configuration`. |
| Frontend configuration | Load once before mount | Strict frontend parser, nullable context and no independent identity fallback. |
| Feature flags | Four explicit serialized states | Missing feature is disabled; unavailable configuration is unavailable. |
| Route/navigation extension | Static compile-time descriptors | Ordered IDs select reviewed descriptors; built-in path collisions are rejected. |
| Capability exposure | State without activation | Metadata can distinguish enabled, disabled, unavailable and experimental; authorization remains separate. |
| TUI/desktop reuse | Explicitly deferred | Future adapters consume the same authority without new independent constants. |
| Branding tokens | Identity fields exposed, rendering deferred | P12.6 does not redesign or rename existing visible shell branding. |
| Version display | Dual-version response ready | Product `0.1.0-dev` and upstream `0.18.2` coexist; P13 owns visible treatment. |
| Extension ownership | Mirrored `agent_platform` namespace | Python and TypeScript source use language-valid forms of one ownership boundary. |

## Selected Product-Owned Namespace

The selected logical namespace is `agent_platform`.

| Surface | Path | Ownership |
| --- | --- | --- |
| Backend | `hermes_cli/agent_platform/**` | AGENT PLATFORM |
| Dashboard | `web/src/agent-platform/**` | AGENT PLATFORM |

The underscore and hyphen are language/tooling conventions for the same logical
namespace, not competing systems.

Allowed contents:

- validated product identity and non-secret metadata;
- stable feature-state identifiers;
- protected read-only transport;
- static first-party route/navigation descriptors;
- narrow adapters and tests approved by later tickets.

Blocked contents:

- provider credentials, tokens, OAuth state or private registry data;
- arbitrary import paths or runtime code-loading instructions;
- filesystem discovery, dynamic evaluation or implicit registration side effects;
- user session state, database paths or personal browser state;
- provider, worker, MCP or agent activation logic.

P13 consumes the frontend descriptor/context seam. Later adapter tickets may
consume the same validated identity in TUI and desktop. P12.5 treats all files
in this namespace as explicit product divergence.

## Product Configuration Contract

The authoritative tracked default is:

```yaml
HermesProductConfiguration:
  schema_version: 1
  product_id: agent-platform-hermes
  product_display_name: AGENT PLATFORM Hermes
  product_version: 0.1.0-dev
  upstream_product_name: Hermes Agent
  upstream_version: 0.18.2
  upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  feature_flags:
    agent_platform.product_ui: disabled
  extension_modules: []
  documentation_url: null
  support_url: null
```

Backend validation uses Pydantic with `extra="forbid"`, frozen top-level model
instances, stable identifier patterns, full commit SHA validation, explicit URL
types and duplicate extension-ID rejection. A new model instance is validated
for each request.

Frontend validation treats the response as `unknown`, requires the exact field
set and schema version, validates every identifier/state/SHA/URL, rejects
duplicate extension IDs and freezes normalized collections. Malformed or
unavailable configuration resolves to `null`; no duplicated frontend product
identity defaults are substituted.

## Configuration Precedence

```yaml
HermesProductConfigurationPrecedence:
  1_tracked_product_defaults: authoritative
  2_approved_non_secret_environment_overrides: none_permitted
  3_user_or_runtime_preferences: excluded
  4_provider_or_secret_configuration: separate_and_excluded
```

Permitted product-configuration environment variable names: none.

`HERMES_DASHBOARD_SESSION_TOKEN` remains an existing dashboard authentication
transport mechanism. It does not override product configuration. P12.6 used
only a synthetic value during isolated runtime validation.

This closed precedence is intentional. Adding an override source later requires
a schema/precedence change, trust-boundary review, tests and register updates.

## Product Identity and Dual Version

```yaml
HermesProductIdentity:
  upstream_name: Hermes Agent
  upstream_version: 0.18.2
  upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  product_name: AGENT PLATFORM Hermes
  product_id: agent-platform-hermes
  product_version: 0.1.0-dev
  display_both_versions: true
```

P12.6 does not alter `hermes_cli.__version__`, `pyproject.toml`, npm package
versions or distribution names. The endpoint exposes both identities. P13 may
render both but may not replace upstream runtime diagnostics with the product
version or create a second product-version constant.

## Feature and Capability Model

| State | Meaning | Route/navigation visibility |
| --- | --- | --- |
| `enabled` | Product capability is approved for exposure | Visible only when its extension ID is also registered and statically compiled |
| `disabled` | Known capability is intentionally off | Hidden; default for missing feature IDs |
| `unavailable` | Capability or whole configuration cannot be provided | Hidden |
| `experimental` | Capability is classified experimental | Hidden unless a reviewed static descriptor explicitly permits experimental visibility |

Presence of a flag does not import code, activate a provider, bypass
authorization, start a worker or invoke a workflow. The initial
`agent_platform.product_ui` flag is disabled and the extension list is empty.

## Backend Configuration Boundary

```yaml
HermesBackendConfigurationBoundary:
  method: GET
  path: /api/agent-platform/product-configuration
  response_model: ProductConfiguration
  public_allowlist_entry: false
  existing_dashboard_auth_required: true
  write_methods: absent
  provider_reads: false
  credential_reads: false
  user_config_reads: false
  filesystem_path_response_fields: false
  side_effects: false
```

`hermes_cli/web_server.py` includes the product-owned router beside the existing
router composition point. The route is not added to `PUBLIC_API_PATHS`, so both
existing loopback-token and gated-cookie middleware protect it.

## Frontend Configuration and Extension Boundary

`web/src/main.tsx` calls `loadProductConfiguration()` before React mounts and
provides the resulting validated object or `null` through one context.

`web/src/agent-platform/extensions.ts` defines the only P12.6 product extension
registry. Descriptors are statically imported, first-party values containing:

- stable extension ID and AGENT PLATFORM ownership;
- stable required feature ID;
- route path, statically compiled component and title;
- optional navigation label, icon and before/after/end placement;
- explicit experimental visibility posture.

Resolution order is the exact `extension_modules` order in validated product
configuration. Resolution rejects duplicate descriptor IDs, duplicate paths,
built-in route collisions and non-built-in navigation anchors. A descriptor is
included only when its ID is configured and its feature state allows visibility.

Composition order in `App.tsx` is:

1. built-in Hermes routes and navigation;
2. resolved static AGENT PLATFORM descriptors;
3. existing dashboard plugin manifests.

The initial registry is empty. No P13 page, workflow or branding redesign is
implemented. Backend data cannot name an import path or supply executable code.

## TUI and Desktop Posture

TUI and desktop adoption is explicitly deferred because P12.6 is not an adapter
implementation ticket.

TUI future adapter boundary:

- consume validated identity as fallback-only data;
- preserve gateway skin overrides;
- retain backend-provided runtime version ownership;
- do not duplicate product constants in `ui-tui`.

Desktop future adapter boundary:

- migrate Electron host, package metadata, renderer, native resources and
  translations atomically;
- separate desktop client, Hermes core and connected backend versions;
- do not use one ambiguous `version` field;
- do not add renderer-only constants before the atomic adapter exists.

`apps/shared` remains unchanged. No TUI, desktop or shared product identity
constant was introduced.

## Implemented Path Set

Created product paths:

```text
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
2_products/hermes-agent/hermes_cli/agent_platform/__init__.py
2_products/hermes-agent/hermes_cli/agent_platform/product_config.py
2_products/hermes-agent/hermes_cli/agent_platform/routes.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_product_config.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_product_routes.py
2_products/hermes-agent/web/src/agent-platform/extensions.test.ts
2_products/hermes-agent/web/src/agent-platform/extensions.ts
2_products/hermes-agent/web/src/agent-platform/product-config-context.ts
2_products/hermes-agent/web/src/agent-platform/product-config-provider.tsx
2_products/hermes-agent/web/src/agent-platform/product-config.test.ts
2_products/hermes-agent/web/src/agent-platform/product-config.ts
```

Modified upstream-derived product paths:

```text
2_products/hermes-agent/hermes_cli/web_server.py
2_products/hermes-agent/web/src/App.tsx
2_products/hermes-agent/web/src/main.tsx
```

Existing upstream-derived files modified: 3. The limit of 8 is respected.

## Upstream File Preimages

| Path | Baseline blob | Baseline SHA-256 | Current SHA-256 | Localized intent |
| --- | --- | --- | --- | --- |
| `hermes_cli/web_server.py` | `30c86e9e90a54fd40e554f94cb5afb34f662e781` | `ea79bfd62f1079fd43924fab508c20c2f1401208fb3bad249c9c7173c3ecc4a3` | `f3034f92e20152d1f8f1e613537768600b6d90fc1ce19bfb7b5b7e10ea3735c8` | Import and include one product-owned router |
| `web/src/main.tsx` | `e0d00fdf6365b57289e0a970707c222ce4f76e52` | `f55c05c44b424069c881ffa42bf3c78493f328bcda7d41723cfcfda29cd81b26` | `fc83d0f55f392c936231725731ff55deabb6f70b624c5aa6b5ff9cbb8bfd3dc9` | Pre-mount fetch and one product context provider |
| `web/src/App.tsx` | `79f7e4853504663289906caf29f70173da134857` | `ccccbb3f3d1ae54c54c303b994b052bc66926ace2204bfb12a4c360f550694db` | `477259e4d307f5f73793fb37e7c2fa32b548d06aabe26fc51ea3b14d89223652` | Compose product descriptors at the central route/navigation seam |

Tracked-file diff for the three existing files is 64 insertions and 20
deletions. No opportunistic cleanup was performed.

## Product Modification Register

`AGENT_PLATFORM_MODIFICATIONS.tsv` contains the required 18 columns and 14
rows. The register itself is a self-exempt product control file to avoid
recursive self-hashing.

```yaml
HermesProductModificationRegisterValidation:
  row_count: 14
  actual_divergence_paths_excluding_register: 14
  missing_rows: 0
  extra_rows: 0
  current_sha256_mismatches: 0
  non_implemented_status_rows: 0
  status: implemented_pending_human_approval
```

Every addition and modified upstream-derived file records intent, reapplication
predicate, conflict owner, security/compatibility impact, validation lanes,
upstream disposition, rollback target, retirement condition and approval state.

## Synchronization-Sensitive Paths

| Path | Classification | Future candidate comparison rule | Reapplication predicate | Retirement condition | Conflict owner | Validation lanes |
| --- | --- | --- | --- | --- | --- | --- |
| `AGENT_PLATFORM_MODIFICATIONS.tsv` | `product_control_file` | Regenerate from accepted product divergence; never take from upstream | Required while any registered product divergence exists | No registered divergence remains | Product architecture owner | Register reconciliation, hash validation |
| `hermes_cli/agent_platform/__init__.py` | `low_conflict_product_owned` | Candidate absence is expected | Recreate while product namespace remains external to upstream | Equivalent governed upstream namespace accepted | Product architecture owner | Ruff, Windows scanner, Python tests |
| `hermes_cli/agent_platform/product_config.py` | `low_conflict_product_owned` | Compare semantic contract and locked identity | Recreate unless candidate provides equivalent strict credential-free schema | Equivalent accepted upstream product contract | Product architecture owner | Python tests, Ruff, runtime |
| `hermes_cli/agent_platform/routes.py` | `low_conflict_product_owned` | Compare protected endpoint semantics | Recreate while dashboard needs product configuration transport | Equivalent protected typed endpoint accepted | Product architecture owner | Python tests, runtime |
| `tests/hermes_cli/test_agent_platform_product_config.py` | `test_only` | Reapply with product schema | Required whenever product schema exists | Schema retired with equivalent tests elsewhere | Product architecture owner | Targeted Python tests |
| `tests/hermes_cli/test_agent_platform_product_routes.py` | `test_only` | Reapply with product route | Required whenever product route exists | Route retired with equivalent tests elsewhere | Product architecture owner | Targeted Python tests |
| `web/src/agent-platform/product-config.ts` | `low_conflict_product_owned` | Compare wire schema and fail-closed parser | Recreate while dashboard consumes backend contract | Equivalent upstream typed consumer accepted | Product architecture owner | Typecheck, tests, build, runtime |
| `web/src/agent-platform/product-config-context.ts` | `low_conflict_product_owned` | Compare single-instance context semantics | Recreate while product components need one validated object | Equivalent upstream bootstrap context accepted | Product architecture owner | ESLint, typecheck, build |
| `web/src/agent-platform/product-config-provider.tsx` | `low_conflict_product_owned` | Compare provider-only component semantics | Recreate with context/bootstrap seam | Equivalent upstream provider accepted | Product architecture owner | ESLint, typecheck, build |
| `web/src/agent-platform/extensions.ts` | `low_conflict_product_owned` | Compare descriptor, collision and ordering contracts | Recreate while P13 uses governed static descriptors | Equivalent safe upstream first-party extension seam accepted | Product architecture owner | Typecheck, tests, build |
| `web/src/agent-platform/product-config.test.ts` | `test_only` | Reapply with frontend parser/transport | Required while frontend contract exists | Contract retired with equivalent tests elsewhere | Product architecture owner | Dashboard tests |
| `web/src/agent-platform/extensions.test.ts` | `test_only` | Reapply with extension resolver | Required while descriptor seam exists | Seam retired with equivalent tests elsewhere | Product architecture owner | Dashboard tests |
| `hermes_cli/web_server.py` | `high_conflict_upstream_file` | Three-way compare app construction/router composition | Reapply one import/include only if equivalent route is absent | Upstream supplies equivalent route or product endpoint retires | Product architecture owner | Python tests, Ruff, scanner, runtime |
| `web/src/main.tsx` | `thin_upstream_integration_point` | Three-way compare React bootstrap | Reapply pre-mount load/provider if equivalent bootstrap is absent | Upstream supplies equivalent typed bootstrap | Product architecture owner | ESLint, typecheck, tests, build, runtime |
| `web/src/App.tsx` | `high_conflict_upstream_file` | Three-way compare central route/navigation composition | Reapply localized product composition if equivalent seam is absent | Equivalent safe upstream route/navigation seam or P13 retirement | Product architecture owner | Typecheck, tests, build, runtime |

The canonical governance record is outside the product synchronization set. It
is a `product_control_file` for main-repository governance and must travel with
the P12.6 commit.

## Targeted Tests

Python targeted execution used the P12.4 native-Windows exception because the
authoritative POSIX wrapper cannot use `.venv/Scripts/python.exe`. The child
environment was cleared and rebuilt with only OS essentials, an approved temp
home and no provider variables.

| Lane | Command or scope | Result |
| --- | --- | --- |
| Product schema/route tests | `python -m pytest -q tests/hermes_cli/test_agent_platform_product_config.py tests/hermes_cli/test_agent_platform_product_routes.py` | 16 passed |
| Product frontend tests | Two `web/src/agent-platform/*.test.ts` files | 13 passed |
| Full dashboard tests | `npm run --prefix web test` | 8 files, 46 tests passed |
| Dashboard typecheck | `npm run --prefix web typecheck` | Pass |
| Affected frontend ESLint | Product namespace plus `web/src/main.tsx` | Pass, zero findings |
| Dashboard production build | `npm run --prefix web build` | Pass, 486 modules transformed |
| Python Ruff | Product Python, tests and router integration | Pass |
| Windows footgun scanner | `scripts/check-windows-footguns.py --all` | Pass, 755 files scanned |

Tests cover schema/default validation, invalid and unknown-field rejection,
closed precedence, absence of secret/provider fields, missing-feature default,
all four feature states, stable extension order, duplicate ID/path rejection,
built-in collision rejection, frontend fetch normalization, auth protection,
GET-only behavior and backend response shape.

## Dependency and Lockfile Validation

| Input | Before SHA-256 | After SHA-256 | Result |
| --- | --- | --- | --- |
| `pyproject.toml` | `7f0180b23c28ea3f7a32e037bcfb1d986fa1925d0a9331112bdce82ef1bfbf45` | Same | Unchanged |
| `uv.lock` | `92d8153c76379a4d427eaf37cd77cedef9dc093c6c44c1386abd4546578f709a` | Same | Unchanged |
| `package.json` | `07b1b0c8d196c93cc4876092907e7350cfc8b04db18ce34debb522aead4ad1c0` | Same | Unchanged |
| `package-lock.json` | `bc11d099f043e142764e66f60f2b558add882948649101645d56319d188861df` | Same | Unchanged |

`npm ls --all --depth=0` exited 0 and retained the five known optional/platform
extraneous-package limitation from P12.3. `.venv/Scripts/python.exe -m pip
check` reported no broken requirements.

The temporary pinned `uv 0.11.6` bootstrap was intentionally removed after
P12.4. Neither `uv` nor the Python module is present. P12.6 prohibits `pip
install`, so the agent did not recreate it and did not rerun `uv lock --check`.
This lane is not affected by P12.6 source changes; exact manifest/lock hashes and
installed-environment integrity are the retained bounded evidence.

No install, update, audit-fix, lock generation or dependency command ran.

## Configuration Security Validation

| Field group | Trust boundary |
| --- | --- |
| `schema_version` | Tracked integer; exact version 1 only |
| Product ID/name/version | Tracked non-secret identity; stable ID and non-empty strings |
| Upstream name/version/commit | Tracked locked provenance; full lowercase SHA required |
| `feature_flags` | Tracked stable IDs and four closed states; cannot execute or authorize |
| `extension_modules` | Ordered stable IDs only; cannot contain paths, URLs or module specifiers |
| Documentation/support URLs | Optional tracked HTTP(S) values; no credentials or arbitrary schemes |

Verified properties:

- no secret-bearing field exists;
- extra API-key, token, provider and credential-path fields are rejected;
- no environment dump or filesystem path is returned;
- no provider key is required for startup;
- no arbitrary file path or import string selects an extension;
- no dynamic eval, runtime network code loading or filesystem discovery exists;
- feature enablement cannot bypass dashboard auth or downstream authorization;
- normal transport failure cannot enable a product feature.

## Provider-Null Runtime Validation

The final runtime used a cleared process environment, isolated OS-temporary
home/appdata/temp roots, a current synthetic update-check cache and one
synthetic dashboard session token. No real `.env`, user Hermes state,
credential, provider, OAuth, MCP, gateway, worker or agent task was used.

```yaml
P12_6_ProviderNullDashboardValidation:
  command: .venv/Scripts/python.exe -m hermes_cli.main dashboard --host 127.0.0.1 --port 0 --no-open --skip-build
  bound_port: 55002
  root_http: 200
  status_http: 200
  product_configuration_authenticated_http: 200
  product_configuration_unauthenticated_http: 401
  product_id: agent-platform-hermes
  product_version: 0.1.0-dev
  upstream_version: 0.18.2
  product_ui_feature_state: disabled
  extension_module_count: 0
  gateway_running: false
  active_agents: 0
  isolated_hermes_home_confirmed: true
  browser_opened: false
  provider_request_attempted: false
  process_exited: true
  listener_remaining_after_cleanup: false
```

No visible dashboard page or branding changed, so manual browser evidence was
not required. Browser automation and screenshot acquisition were not used.

## P12.4 Regression Comparison

| P12.4 lane | P12.6 classification | Evidence |
| --- | --- | --- |
| Python lock validation | `not_affected` | Lock and manifest hashes unchanged; removed uv bootstrap was not reinstalled |
| Frozen Python environment | `unchanged` | `pip check` passes; no dependency command or manifest drift |
| Ruff | `unchanged` | Affected scope passes |
| Windows footgun scanner | `unchanged` | Full authoritative scope passes |
| Root npm dependency integrity | `unchanged` | `npm ls --all --depth=0` exits 0 |
| Dashboard typecheck | `unchanged` | Pass |
| Dashboard tests | `improved` | Green lane preserved and 13 focused tests increase total from 33 to 46 |
| Dashboard build | `unchanged` | Production build passes with the known large-chunk warning |
| Provider-null dashboard readiness | `unchanged` | Root/status ready, product endpoint ready, no gateway/provider activity |
| Human-observed shell | `not_affected` | No visible identity/page/navigation change; registry is empty |
| TUI/shared/desktop checks and builds | `not_affected` | No source or package input changed in those surfaces |
| Known P12.4 Python/desktop/lint failures | `not_affected` | Not rerun or reclassified; no affected input changed |
| Source and lockfile drift absence | `unchanged` | Protected hashes match; only declared P12.6 paths differ |

```yaml
P12_6_RegressionComparison:
  affected_green_lanes_preserved: true
  new_failures_introduced: false
  known_baseline_failures_reclassified: false
  import_or_exclusion_regression: false
```

## Source and Control Drift Validation

The following accepted hashes remain unchanged:

| Path | SHA-256 |
| --- | --- |
| `UPSTREAM_PROVENANCE.md` | `78db7acccd38cacc1771792ca9c99cf3a063f60ac2e04d966e05cae22c335b43` |
| `SOURCE_IMPORT_MANIFEST.tsv` | `58a3392c7515ec2a8aaaf8e43530ae6299b2696957d095be461df51e8a080d5c` |
| `SOURCE_EXCLUSIONS.tsv` | `7a413310330e4625146bcad9c73e62af2634f5f3130530111a9b766daf25d64e` |
| `NOTICE` | `4ac2353fc0b52c937b43ba6ae54d9d28ce3c4d400b87b7dd4894c2cc2026c145` |
| `THIRD_PARTY_NOTICES.md` | `c3c564d96a3ef0e9ee9afccd44ae43785c311ef1a5262e5043c786da8df0e5aa` |
| `.gitignore` | `cc50d6a4e5789a08f19a4f17d306ce14cfda4032b5ec248e2c1383106959cc30` |
| `hermes_cli/main.py` | `c9d1965fdb2e6d7b4d54aca3ad7a7fc3ab7cdc70fff34be625ae2582144be60e` |
| `web/vite.config.ts` | `ae93313111185abe5884374b9218b23f85d54bb88abe04098372fba191b85588` |

Final source posture before human staging:

```yaml
P12_6_SourceDriftValidation:
  product_status_paths: 15
  declared_product_paths: 15
  registered_divergence_paths_excluding_self_exempt_register: 14
  staged_product_paths: 0
  staged_total_paths: 0
  dependency_or_lockfile_status_paths: 0
  p12_2_control_drift: false
  generated_state_exposed: false
  nested_git_count: 0
  candidate_checkout_exists: false
  synchronization_workspace_exists: false
  locked_upstream_status_paths: 0
```

## Rollback Posture

Pre-change rollback authority:

```yaml
P12_6_RollbackPreimage:
  main_commit: dcc110229e2fbc7e45095a129ced3976793b5200
  product_tree: 07bc27d2cc3b015b3865d62d7fdbc7dfe0ab6fb7
  planned_created_product_paths: 12
  planned_modified_upstream_paths: 3
  modified_preimage_blob_ids_recorded: true
  modified_preimage_sha256_recorded: true
  generated_runtime_root: C:/Users/pablo/AppData/Local/Temp/opencode/p12.6-runtime
```

Before commit, rollback is exact-path only:

1. Stop only P12.6-owned processes and verify released listeners.
2. Compare actual product status with the 15-path P12.6 set.
3. Stop for human review if any unexplained path exists.
4. Remove only the exact 12 P12.6-created product paths.
5. Restore only the three recorded upstream-derived preimages by their exact
   baseline content under human control.
6. Preserve P12.2 controls and P12.3 environments.
7. Verify product tree `07bc27d...`, baseline hashes, empty index and clean
   product status.

No Git clean, hard reset, broad restore, wildcard deletion, parent-directory
deletion or history rewrite is authorized. After commit, rollback requires an
explicit human-created revert commit.

## Limitations

- The product configuration currently has one tracked defaults tier and no
  approved deployment/user override source.
- The initial frontend extension registry is empty and the product UI feature
  is disabled; no P13 page is proven by P12.6.
- TUI and desktop consume the contract only after later explicit adapter work.
- Normal upstream dashboard startup may load existing Hermes environment state
  before the web server module. The new loader and endpoint do not consult or
  serialize it; isolated validation proves provider-null operation.
- `uv lock --check` was not rerun because the intentionally transient pinned uv
  bootstrap is absent and reinstalling it is prohibited in P12.6.
- Full known-non-green Python, desktop and project lint lanes were not rerun;
  they are unaffected and remain P12.4 baseline debt.
- `web_server.py` and `App.tsx` are high-conflict upstream files despite the
  localized edits. P12.5 must use their exact predicates and human conflict
  review during synchronization.

## P12.7 Handoff

P12.7 may proceed after human acceptance, exact-path commit, clean main and
availability of the P12.3 environment recreation procedure.

P12.7 must validate:

- clean Python and Node environment recreation;
- reproducible product configuration response;
- modification-register path/hash completeness;
- focused tests, dashboard typecheck/build and provider-null startup;
- exact shutdown and rollback posture;
- restoration/reapplication of the three upstream-derived integration edits.

Marker: `hermes_P12_7_ready`.

## P13 Handoff

P13 receives:

- product identity `agent-platform-hermes` and version `0.1.0-dev`;
- locked upstream identity in the same contract;
- protected product configuration endpoint and strict frontend parser;
- feature ID `agent_platform.product_ui`, initially disabled;
- the static `ProductExtensionDescriptor` contract;
- ordered extension-module registration and route/navigation collision rules;
- the mirrored `agent_platform` product namespace;
- all synchronization-sensitive paths and validation lanes;
- the provider-null dashboard startup boundary.

P13 may not invent another configuration authority, duplicate identity/version
constants, bypass the static registry, add secret fields, dynamically load code
or modify a registered path without updating the modification register.

P13 execution remains gated by P12.7 and P12.R.

Marker: `hermes_P13_foundation_inputs_ready`.

## Created Modified and Generated Register

Created governance path:

```text
0_architecture/governance/agent_platform_hermes_product_extension_configuration_seams.md
```

Created product paths: 12, listed under `Implemented Path Set`.

Modified upstream-derived product paths: 3, listed under `Upstream File
Preimages`.

Generated and ignored only:

```text
2_products/hermes-agent/.pytest_cache
2_products/hermes-agent/hermes_cli/web_dist
C:/Users/pablo/AppData/Local/Temp/opencode/p12.6-runtime
```

Not modified:

```text
root .gitignore
P12.2 legal/provenance controls
SOURCE_IMPORT_MANIFEST.tsv
SOURCE_EXCLUSIONS.tsv
pyproject.toml
uv.lock
package.json
package-lock.json
workspace package manifests
Cargo manifests and locks
locked upstream reference
sibling products
P12.3, P12.4 and P12.5 records
.opencode/**
AGENTS.md
```

## Result Markers

```text
hermes_product_extension_configuration_seams_ready
hermes_product_configuration_contract_defined
hermes_configuration_precedence_defined
hermes_product_identity_seam_defined
hermes_feature_flag_seam_defined
hermes_frontend_extension_seam_defined
hermes_backend_configuration_boundary_defined
hermes_product_divergence_register_created
hermes_product_divergence_registered
hermes_synchronization_sensitive_paths_recorded
hermes_P12_4_baseline_preserved
hermes_lockfiles_unchanged
hermes_provider_boundary_preserved
hermes_P12_7_ready
hermes_P13_foundation_inputs_ready
no_upstream_sync
no_dependency_change
no_provider_activation
no_credentials_used
no_git_mutation_by_agent
```

`no_git_mutation_by_agent` means no staging, commit, branch, ref, remote, merge,
rebase or push operation. Authorized working-tree source creation/modification is
the P12.6 deliverable and is not an index/history mutation.

## Final Verdict

```yaml
P12_6_ProductExtensionConfigurationSeamsVerdict:
  p12_5_committed: true
  initial_product_baseline_clean: true
  seam_inventory_complete: true
  product_owned_namespace_selected: true
  product_configuration_contract_defined: true
  configuration_precedence_defined: true
  product_identity_seam_ready: true
  dual_version_model_ready: true
  feature_flag_seam_ready: true
  frontend_extension_seam_ready: true
  backend_configuration_boundary_ready: true
  tui_desktop_configuration_posture_defined: true
  modification_register_created: true
  all_product_divergence_registered: true
  existing_upstream_files_modified_count: 3
  existing_upstream_file_limit_respected: true
  lockfiles_unchanged: true
  dependencies_unchanged: true
  affected_green_baseline_lanes_preserved: true
  new_regression_detected: false
  credentials_used: false
  provider_activation_performed: false
  upstream_sync_performed: false
  git_mutated_by_agent: false
  P12_7_may_proceed: true
  P13_foundation_inputs_ready: true
  P13_execution_remains_gated_by_P12_R: true
  final_verdict: product_extension_configuration_seams_ready
```

## Human Commit Boundary

The exact approved commit path set is:

```text
0_architecture/governance/agent_platform_hermes_product_extension_configuration_seams.md
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
2_products/hermes-agent/hermes_cli/agent_platform/__init__.py
2_products/hermes-agent/hermes_cli/agent_platform/product_config.py
2_products/hermes-agent/hermes_cli/agent_platform/routes.py
2_products/hermes-agent/hermes_cli/web_server.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_product_config.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_product_routes.py
2_products/hermes-agent/web/src/agent-platform/extensions.test.ts
2_products/hermes-agent/web/src/agent-platform/extensions.ts
2_products/hermes-agent/web/src/agent-platform/product-config-context.ts
2_products/hermes-agent/web/src/agent-platform/product-config-provider.tsx
2_products/hermes-agent/web/src/agent-platform/product-config.test.ts
2_products/hermes-agent/web/src/agent-platform/product-config.ts
2_products/hermes-agent/web/src/App.tsx
2_products/hermes-agent/web/src/main.tsx
```

Human-only staging, commit and push script:

```powershell
$ErrorActionPreference = "Stop"

$ProductRoot = "2_products/hermes-agent"
$Register = "$ProductRoot/AGENT_PLATFORM_MODIFICATIONS.tsv"
$Approved = @(
    "0_architecture/governance/agent_platform_hermes_product_extension_configuration_seams.md"
    "$Register"
    "$ProductRoot/hermes_cli/agent_platform/__init__.py"
    "$ProductRoot/hermes_cli/agent_platform/product_config.py"
    "$ProductRoot/hermes_cli/agent_platform/routes.py"
    "$ProductRoot/hermes_cli/web_server.py"
    "$ProductRoot/tests/hermes_cli/test_agent_platform_product_config.py"
    "$ProductRoot/tests/hermes_cli/test_agent_platform_product_routes.py"
    "$ProductRoot/web/src/agent-platform/extensions.test.ts"
    "$ProductRoot/web/src/agent-platform/extensions.ts"
    "$ProductRoot/web/src/agent-platform/product-config-context.ts"
    "$ProductRoot/web/src/agent-platform/product-config-provider.tsx"
    "$ProductRoot/web/src/agent-platform/product-config.test.ts"
    "$ProductRoot/web/src/agent-platform/product-config.ts"
    "$ProductRoot/web/src/App.tsx"
    "$ProductRoot/web/src/main.tsx"
) | Sort-Object -Unique

if ((git branch --show-current) -ne "main") {
    throw "P12.6 must be committed from main"
}
if ((git rev-parse HEAD) -ne (git rev-parse origin/main)) {
    throw "main no longer matches origin/main; revalidate before staging"
}

$StagedBefore = @(git diff --cached --name-only)
if ($StagedBefore.Count -ne 0) {
    throw "Index is not empty: $($StagedBefore -join ', ')"
}

foreach ($Path in $Approved) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing approved path: $Path"
    }
}

$ForbiddenPrefixes = @(
    "4_external/"
    "9_artifacts/"
    ".opencode/"
    "graphify-out/"
)
foreach ($Path in $Approved) {
    if ($Path -eq "AGENTS.md" -or
        @($ForbiddenPrefixes | Where-Object { $Path.StartsWith($_) }).Count -ne 0) {
        throw "Forbidden approved path: $Path"
    }
}

$ProductPrefix = "$ProductRoot/"
$ActualProductPaths = @(
    git status --porcelain=v1 -uall -- $ProductRoot |
        ForEach-Object {
            $Path = $_.Substring(3).Replace("\", "/")
            if ($Path.StartsWith($ProductPrefix)) { $Path } else { "$ProductPrefix$Path" }
        } |
        Sort-Object -Unique
)
$ExpectedProductPaths = @(
    $Approved | Where-Object { $_.StartsWith($ProductPrefix) }
)
if (@(Compare-Object $ExpectedProductPaths $ActualProductPaths).Count -ne 0) {
    throw "Actual product diff does not match the approved P12.6 path set"
}

$Rows = @(Import-Csv -Delimiter "`t" -LiteralPath $Register)
$RegisteredPaths = @(
    $Rows | ForEach-Object { "$ProductRoot/$($_.path)" } | Sort-Object -Unique
)
$ExpectedRegisteredPaths = @(
    $ExpectedProductPaths | Where-Object { $_ -ne $Register }
)
if (@(Compare-Object $ExpectedRegisteredPaths $RegisteredPaths).Count -ne 0) {
    throw "Modification register paths do not match product divergence"
}
foreach ($Row in $Rows) {
    $Path = "$ProductRoot/$($Row.path)"
    $Hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
    if ($Hash -ne $Row.current_product_sha256_or_none) {
        throw "Modification register hash mismatch: $Path"
    }
}

$NestedGit = @(
    Get-ChildItem -LiteralPath $ProductRoot -Force -Recurse -Directory `
        -Filter ".git" -ErrorAction Stop
)
if ($NestedGit.Count -ne 0) {
    throw "Nested Git metadata found under the product root"
}

$ForbiddenManifests = @(
    "$ProductRoot/pyproject.toml"
    "$ProductRoot/uv.lock"
    "$ProductRoot/package.json"
    "$ProductRoot/package-lock.json"
)
if (@($Approved | Where-Object {
    $_ -in $ForbiddenManifests -or
    $_ -match "/package\.json$" -or
    $_ -match "/Cargo\.(toml|lock)$"
}).Count -ne 0) {
    throw "A dependency or lockfile path is in the approved set"
}

foreach ($Path in $Approved) {
    git add -- $Path
    if ($LASTEXITCODE -ne 0) { throw "Failed to stage: $Path" }
}

$Staged = @(git diff --cached --name-only | Sort-Object -Unique)
if (@(Compare-Object $Approved $Staged).Count -ne 0) {
    throw "Staged paths do not match the exact approved set"
}
if (@($Staged | Where-Object {
    $_ -eq "AGENTS.md" -or
    $_.StartsWith("4_external/") -or
    $_.StartsWith("9_artifacts/") -or
    $_.StartsWith(".opencode/") -or
    $_.StartsWith("graphify-out/") -or
    $_ -match "/node_modules/|/web_dist/|/dist/|/build/|\.pytest_cache/|__pycache__/"
}).Count -ne 0) {
    throw "Forbidden or generated path was staged"
}

git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "git diff --cached --check failed" }

git diff --cached --stat
git commit -m "P12.6 - Add Hermes product extension and configuration seams"
git push origin main
```

The executing agent did not stage, commit or push.
