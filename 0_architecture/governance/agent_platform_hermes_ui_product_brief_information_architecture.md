# P13.0 - Hermes UI Product Brief and Information Architecture

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.0 - UI Product Brief and Information Architecture |
| Type | Product architecture, UI capability audit and information architecture |
| Execution class | Documentation plus bounded read-only source and provider-null UI inspection |
| Date | 2026-07-14 |
| Status | Ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_ui_product_brief_information_architecture.md` |
| Durable document count | Exactly one |
| Product root | `2_products/hermes-agent` |
| Immutable upstream | `4_external/sources/hermes-agent` |
| Start commit | `0d43f86ef5f734b8d4bb14e742caa70d124f17f7` |
| Product source implementation | Prohibited and not performed |
| Feature/provider/worker activation | Prohibited and not performed |
| Git mutation by agent | Prohibited and not performed |

## Purpose

Define the first authoritative product brief and information architecture for
the AGENT PLATFORM Hermes browser UI, grounded in the actual dashboard,
plugins, Kanban, APIs, data stores, tests and provider-null behavior.

This record binds every later P13 ticket to the following rule:

```text
No new UI capability may be implemented until the corresponding Hermes
capability has been inspected, safely observed where possible, classified and
assigned an adopt_existing, adapt_existing, wrap_existing, extend_existing,
replace_existing, defer or not_applicable decision in this record.
```

Terminology or visual differences alone do not justify replacement. P13 does
not authorize a second Kanban, task database, execution history, plugin
architecture, settings authority, identity constant or runtime contract.

## Scope

Phase A audited the existing Hermes UI and workflow capability. Phase B uses
that evidence to define the product brief, vocabulary, data authority,
navigation, routes, surfaces, states, activation sequence and P13.1-P13.8
handoffs.

The only tracked output is this document. Product and upstream source,
configuration, extension descriptors, routes, navigation, branding, tokens,
Kanban state and dependency files were not modified. The product feature stays
disabled and the extension registry stays empty.

P13.0 does not authorize provider/model use, OAuth, MCP startup, gateway or
dispatcher startup, workers, agent tasks, WorkPacket execution, Paperclip,
GBrain, production deployment, publication or redistribution.

## Authoritative Inputs

Governance evidence inspected:

| Authority | Material use in P13.0 |
| --- | --- |
| P11 Hermes evaluation and integration closure | Browser-dashboard-first posture; lifecycle, Windows PTY and authority limitations |
| P12.0 productization authorization | Product/upstream ownership and prohibited execution boundaries |
| P12.2 source/legal baseline | Controlled source, exclusions, notices and no redistribution authority |
| P12.3 reproducible environment | Existing frozen development environment authority |
| P12.4 build/test/UI baseline | Dashboard green lanes and inherited known failures |
| P12.5 synchronization strategy | Filtered three-way reapplication and semantic-conflict rules |
| P12.6 product extension seams | Product identity, protected bootstrap, feature states and static descriptors |
| P12.7 rebuild/rollback drill | Isolated provider-null runtime and exact rollback pattern |
| P12.R foundation closure | P13 authority, readiness limits and P14/P15 gates |

Minimum canonical records read were:

```text
0_architecture/governance/agent_platform_hermes_productization_foundation_closure.md
0_architecture/governance/agent_platform_hermes_product_extension_configuration_seams.md
0_architecture/governance/agent_platform_hermes_baseline_build_test_ui_snapshot.md
0_architecture/governance/agent_platform_hermes_upstream_synchronization_strategy.md
0_architecture/governance/agent_platform_hermes_clean_rebuild_rollback_drill.md
```

Product controls read were `UPSTREAM_PROVENANCE.md`,
`SOURCE_IMPORT_MANIFEST.tsv`, `SOURCE_EXCLUSIONS.tsv` and
`AGENT_PLATFORM_MODIFICATIONS.tsv`. Deleted historical Markdown was not
restored. Graphify was not used.

## Prerequisite Status

```yaml
P13_0_PrerequisiteStatus:
  branch: main
  head: 0d43f86ef5f734b8d4bb14e742caa70d124f17f7
  origin_main: 0d43f86ef5f734b8d4bb14e742caa70d124f17f7
  P12_R_commit_present_in_main: true
  git_index_empty: true
  initial_product_status_clean: true
  tracked_product_files: 6132
  product_tree: 274527e686fa50a320a92a5738e8c8c083669b24
  modification_register_rows: 14
  modification_register_required_field_failures: 0
  modification_register_hash_mismatches: 0
  nested_product_git: false
  locked_upstream_clean: true
  locked_upstream_commit: 9de9c25f620ff7f1ce0fd5457d596052d5159596
  product_UI_feature: disabled
  extension_modules: []
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  prerequisite_result: pass
```

Permitted unrelated local paths were `.opencode/`, `AGENTS.md`,
`graphify-out/` and ignored `9_artifacts/hermes/**`. No stop rule fired.

## Audit Method

Phase A used five evidence classes:

| Class | Method |
| --- | --- |
| Source | Read shell, route, plugin, API, data, Kanban, design and test sources |
| Data | Trace current SQLite/config/session authorities and DTOs |
| API | Inventory dashboard and plugin routes, authentication and write effects |
| Tests/docs | Compare tested behavior and user documentation with current code |
| Runtime | Start one isolated provider-null dashboard, use loopback HTTP, create synthetic Kanban state and remove it |

Every reuse decision records the required decision taxonomy fields in the
Capability Reuse Decision Matrix. Phase B was completed only after shell,
route, plugin, Kanban, reusable-surface and design-system audits were complete.

Compiled, registered, visible, reachable, configured, operational and
provider-dependent are treated as independent properties. A route label or
compiled component is never used as proof of operational authority.

## Current Application Shell Inventory

| Concern | Existing behavior | P13 conclusion | Evidence |
| --- | --- | --- | --- |
| Bootstrap | Plugin SDK, protected product configuration, router, i18n, theme, actions and product context mount centrally | Adopt the bootstrap; do not create another root | `web/src/main.tsx:13-32` |
| Desktop navigation | 16rem sidebar collapses to 3.5rem and persists preference | Adapt, preserving route paths | `web/src/App.tsx:352-379,574-640` |
| Mobile navigation | Fixed header, overlay, 16rem drawer, Escape and scroll lock | Adapt; add focus trap/return in P13.8 | `web/src/App.tsx:489-510,527-586` |
| Navigation grouping | Core routes are flat; dynamic plugins render in a separate plugin block; lifecycle actions form another System block | Extend the central seam with product groups, not a second sidebar | `web/src/App.tsx:648-717,924-1095` |
| Page headers | Context supplies title, after-title and end-action slots | Adopt; fill title registry gaps | `web/src/contexts/PageHeaderProvider.tsx:17-134` |
| Profile scope | `?profile=` is restored, routed pages remount on change, Chat changes PTY identity | Adopt as the write-target safety boundary | `web/src/contexts/ProfileProvider.tsx:12-79`; `web/src/App.tsx:823-836` |
| Status presentation | Footer/status strip shows gateway summary and recent-session heuristic | Wrap with freshness/error/source labels | `web/src/hooks/useSidebarStatus.ts:14-24`; `SidebarStatusStrip.tsx:21-47` |
| Language | Existing i18n context and switcher include responsive UI | Adopt and extend only for product strings | `web/src/i18n/**`; `LanguageSwitcher.tsx:25-104` |
| Theme | Existing theme provider, eight presets, custom theme escape hatch | Adopt/alias; do not create a parallel theme engine | `web/src/themes/**`; `index.css:1-187` |
| Plugin navigation | Manifest tabs load dynamically; before/after hints affect plugin order but plugins render after core entries | Keep third-party trust separate; do not use for mandatory product IA | `web/src/App.tsx:238-287` |
| Route collision | Static product descriptors reject exact built-in collisions; dynamic plugins can override product routes later | Extend protection before product activation | `web/src/agent-platform/extensions.ts:41-67`; `web/src/App.tsx:289-347,440-469` |
| Persistent Chat | Chat remains mounted with xterm/WebSocket/PTY while other routes display | Leave upstream-owned; do not rebuild chat in React | `web/src/App.tsx:129-136,783-809` |
| Unknown route | Redirects to `/sessions` after plugin discovery | Preserve until a governed product not-found state is implemented | `web/src/App.tsx:110-120` |

Current shell defects relevant to P13 are missing page-title mappings, no
mobile focus trap, distributed breakpoint/z-index literals, stale-silent
status polling and a hidden persistent Chat host that still attempts a PTY
connection on native Windows.

## Current Route and Page Inventory

All rows are compiled and registered. `C/R/V/D/O` means compiled, registered,
visible in primary navigation, directly reachable and operational in the
isolated provider-null state.

| Route | Label | Current purpose/data source | Read/write and sensitive dependency | State | P13 surface and decision |
| --- | --- | --- | --- | --- | --- |
| `/chat` | Chat | Embedded TUI over `/api/pty` | Runtime write; session/provider capable; WebSocket token | C/R/V/D; not O on native Windows | Hermes tool; `adopt_existing`, environment-constrained |
| `/sessions` | Sessions | Session DB, messages, stats and exports | Read/write rename/delete/prune; runtime history | C/R/V/D/O | Runtime/Execution evidence; `wrap_existing` |
| `/files` | Files | Managed filesystem roots | Read/upload/mkdir/delete; paths and arbitrary write risk | C/R/V/D/O locally | Hermes tool only; `defer` from product IA |
| `/analytics` | Analytics | Local token/cost estimates | Read-only; model metadata; no provider call | C/R; hidden/config disabled; D; not fetching | Observe context; `adapt_existing` when truthful |
| `/models` | Models | Model options, assignments and analytics | Writes provider/model assignments; provider-sensitive | C/R/V/D; UI O, models not configured | Administration; `defer` from safe settings |
| `/logs` | Logs | Agent/error/gateway files | Read-only but potentially sensitive text | C/R/V/D/O | Execution evidence link; `wrap_existing` |
| `/cron` | Cron | Job store and delivery targets | CRUD/run; can trigger agent/provider execution | C/R/V/D/O UI; execution blocked | Hermes tool; `defer` from product control |
| `/skills` | Skills | Local skills/toolsets and remote hub | Read/write/install/update; hub is network/subprocess capable | C/R/V/D/O local only | Hermes tool; `leave existing` |
| `/plugins` | Plugins | Plugin hub/configuration | Install/enable/remove code; Git/network/config writes | C/R/V/D/O local inventory | Administration; not product-extension authority |
| `/mcp` | MCP | MCP config/catalog | Add/test/install servers; commands, URLs, secrets and processes | C/R/V/D; no server O | Administration; unavailable to P13 safe UI |
| `/pairing` | Pairing | Gateway user access state | Approve/revoke identities; not command approval | C/R/V/D; empty without gateway | Administration; `not_applicable` to approvals |
| `/channels` | Channels | Messaging platform state/config | Credentials, onboarding, tests and gateway restart | C/R/V/D; unconfigured | Administration; `defer` |
| `/webhooks` | Webhooks | Webhook routes and gateway config | Secrets, routes, toggles and restart | C/R/V/D; unconfigured | Administration; `defer` |
| `/system` | System | Status, host stats, memory, hooks, updates and lifecycle | Mixed read/write; credentials, host actions, gateway controls | C/R/V/D/O read subset | Runtime source plus admin link; `wrap_existing` read-only |
| `/profiles` | Profiles | Machine profile registry | Create/rename/activate/delete/edit profile | C/R/V/D/O | Context selector; `adopt_existing` |
| `/profiles/new` | New Profile | Profile creation flow | Final create write; model/skill reads | C/R; no nav; D/O | Contextual child flow; leave untouched |
| `/config` | Config | Schema, merged config and raw YAML | Structured and full raw writes; may expose sensitive config/path | C/R/V/D/O | Administration; excluded from safe settings |
| `/env` | Keys | Masked environment and OAuth state | Set/delete/reveal secrets and OAuth tokens | C/R/V/D/O UI; no provider auth | Administration; excluded from safe settings |
| `/docs` | Documentation | Sandboxed remote Hermes documentation | External network/iframe; hardcoded URL | C/R/V/D; not inspected, network blocked | Help link; use product URL only after explicit contract |

Dynamic bundled routes observed were `/kanban` and `/achievements`. They are
registered after the public plugin-manifest response and are not built-in route
authority. `/kanban` is audited below; `/achievements` is not applicable to the
central P13 product surfaces.

## Plugin Architecture Audit

Hermes has two distinct dashboard extension boundaries:

| Boundary | Mechanism | Trust | Correct P13 use |
| --- | --- | --- | --- |
| P12.6 first-party product extension | Statically imported descriptors selected by validated configuration | Reviewed, compiled, fail-closed AGENT PLATFORM code | Mandatory product routes/navigation |
| Dynamic dashboard plugin | Public manifest, same-origin JS/CSS, optional protected Python API | Operator-trusted code with dashboard privileges | Third-party/bundled optional capabilities such as Kanban |

Dynamic plugins can use React, Nous UI, authenticated API/fetch/WebSockets,
i18n, utility helpers and shell slots. They are not sandboxed. User plugins
override same-named bundled plugins during discovery; bundled plugins are
active unless disabled; project plugins require a global environment gate.
Python APIs remain authenticated, while manifests and script/style assets are
public so browsers can load them.

Material findings:

| Finding | Effect | Evidence |
| --- | --- | --- |
| Dynamic `tab.override` can replace built-in and future product routes | Mandatory product routes need explicit override protection | `web/src/App.tsx:289-347,440-469` |
| Multiple overrides are last-manifest-wins; add-on plugin-to-plugin path collisions are not rejected | Route truth is nondeterministic under collision | `web/src/App.tsx:297-347` |
| Plugin SRI is supported by the loader but backend manifests omit `integrity`; CSS has no SRI | Compiled integrity path is not operational | `web/src/plugins/usePlugins.ts:43-80`; `web_server.py:15999-16013` |
| Enable/disable/rescan does not unload or refresh app-level plugin state | Configuration and current-page code can differ until reload | `web/src/plugins/usePlugins.ts:26-35` |
| Slot names, render sites and SDK signature drift | Slots cannot be treated as stable product IA | `web/src/plugins/slots.ts:21-135`; `web/src/plugins/sdk.d.ts:83-88` |
| Project plugin JavaScript receives same-origin privileges even though project Python APIs are blocked | Project-plugin gate is a code-trust decision | `web_server.py:16034-16070,16434-16500` |

Decision: `wrap_existing` for the plugin management surface and
`adopt_existing` for third-party extensibility, but `not_applicable` as the
first-party product route authority. P13.2 must keep the static descriptor
boundary separate and protect product-owned paths from dynamic override.

## Kanban and Swarm Capability Audit

Hermes Kanban is a substantial SQLite-backed operational work surface, not a
placeholder. It is technically durable for Hermes use but architecturally
provisional for AGENT PLATFORM because Paperclip remains the future canonical
work-control authority.

| Capability | Current behavior and authority | Fit | P13 decision |
| --- | --- | --- | --- |
| Boards | Per-board DB, workspace, logs and attachment roots; board slug is the hard worker boundary | `exact` operational isolation | `wrap_existing` as provisional project substrate |
| Tasks and IDs | `t_` plus random local ID; title/body/status/priority/tenant/assignee/workspace fields | `partial`; not platform identity | `adapt_existing` behind product projection IDs |
| Statuses | `triage`, `todo`, `scheduled`, `ready`, `running`, `blocked`, `review`, `done`, `archived` | `partial`; review ingress/cancellation/approval semantics missing | `adapt_existing`; never declare canonical Ticket states |
| Priorities | Integer dispatcher order | `partial`; no policy/budget class | Display as Hermes priority only |
| Assignees/profiles | String profile references used by dispatch | `partial`; no immutable capability snapshot | Adapt as profile/assignee, not Agent authority |
| Tenants | Soft namespace/filter within a board | `partial`; not access control | Do not map to Macroproject security boundary |
| Parent/dependency links | DAG cycle prevention, parent gating, promotion and recomputation | `exact` for Hermes tasks | Adopt visual/link behavior through adapter |
| Comments | Durable per-task thread and events | `compatible_with_adapter` | Evidence/discussion only, not approval truth |
| Attachments | Upload/list/download/delete with task directory | `partial`; retention/classification and task-delete cleanup gaps | Extend before product exposure |
| Events | Durable task event stream with run correlation where available | `compatible_with_adapter` | Wrap as source-labelled timeline evidence |
| Runs | Attempt status/outcome, PID, heartbeat, summaries, errors and result metadata | `compatible_with_adapter` | Wrap for inspector; not WorkPacket execution |
| Diagnostics | Structured warnings and remediation hints | `compatible_with_adapter` | Adopt presentation, validate commands |
| Filters/search | Server filters for selected fields; dashboard search is client-side over full board | `partial`; no FTS/pagination/cursor | Adapt for bounded board sizes |
| Drag/drop | Desktop/touch cards and dynamic columns | `partial`; multi-card defect exists | Adapt only after defect validation |
| Live updates | SQLite event tail over plugin WebSocket polling | `compatible_with_adapter` | Reuse for Kanban only, not universal event bus |
| Dispatcher | Reclaim, promote, claim and spawn assigned profiles | `future_authority_conflict` in P13 | `defer`; P14/P15 gate required |
| Workspaces | Scratch/worktree/dir concepts flow into worker spawn | `future_authority_conflict` for real repos | `defer`; no real path in P13 |
| Retry/reclaim | Stale-claim recovery, heartbeat, failure limit and auto-block | `compatible_with_adapter` mechanics | Defer execution; future external policy owns limits |
| Human-in-the-loop | Block/unblock, comments, reassignment and manual reclaim | `partial`; no approval object | Visualize carefully; do not claim ApprovalRequest |
| CLI/tools/gateway | CLI verbs, worker toolset and gateway watcher integrate the same DB | `exact` Hermes integration | Keep outside P13 runtime authority |
| Swarm/decomposition | Creates task graphs and can invoke auxiliary models/dispatch | `future_authority_conflict` | `defer`; no autonomous fan-out in P13 |

Deep source evidence included `hermes_cli/kanban.py`, `kanban_db.py`,
`kanban_swarm.py`, `kanban_decompose.py`, `kanban_specify.py`,
`kanban_diagnostics.py`, `tools/kanban_tools.py`,
`gateway/kanban_watchers.py`, `plugins/kanban/**`, relevant tests and the
current Kanban user documentation.

Material implementation and contract drift:

| Severity | Finding | Evidence and disposition |
| --- | --- | --- |
| High | Dashboard single/bulk deletion omits selected board and can target process-current board | `plugins/kanban/dashboard/dist/index.js:943-1008`; fix before P13.4 write exposure |
| High | Hard task deletion omits attachment rows/files and can leave downloadable orphan data | `kanban_db.py:1233-1248,5233-5279`; `plugin_api.py:762-784`; fix retention/cascade |
| High | Multi-card drag references undefined `DESTRUCTIVE_TRANSITIONS` | `dist/index.js:754-758`; add behavior coverage |
| High | Dashboard API directly writes Hermes schema/status transitions despite docs claiming common paths | `plugin_api.py:821-1078`; wrap with product-neutral projection |
| Medium | `review` is a backend column with dispatch logic but no supported UI/API/CLI/tool ingress | `kanban_db.py:3494-3566,7317-7397`; do not map to Approval |
| Medium | `scheduled` is a waiting state without timestamp/wake scheduling, contrary to docs | `kanban_db.py:5588-5630`; `kanban.py:573-577`; correct docs/labels |
| Medium | Swarm graph creation uses multiple transactions and can leave partial topology | `kanban_swarm.py:111-221`; defer autonomous use |
| Medium | Gateway decomposition mutates process-global board state while dashboard uses context-local scope | `gateway/kanban_watchers.py:1156-1208`; use scoped board before future execution |
| Medium | Diagnostic recommends nonexistent `hermes kanban events` command | `kanban_diagnostics.py:823-831`; correct before product surfacing |

Documentation also drifts on status lists, event retention, comment context
limits, direct Running actions, edit/schedule flags, endpoint inventory, run
fields and plugin API authentication. Code/tests/runtime remain authoritative.

Kanban reuse decision: `wrap_existing`. P13.4 may reuse and adapt the current
board/task/link/comment/event/run UI and data through a product-owned projection.
No second backend is authorized. Kanban remains a provisional operational
substrate subject to future Paperclip replacement; no permanent dual-write is
authorized. Dispatcher, workers, swarm and provider-backed decomposition stay
blocked.

## Kanban versus AGENT PLATFORM Semantic Mapping

| AGENT PLATFORM concept | Hermes candidate | Mapping | Binding interpretation |
| --- | --- | --- | --- |
| Macroproject | Board plus tenant | `partial` | Board is hard operational isolation; tenant is soft filtering, neither is canonical Macroproject authority |
| Project | Board | `compatible_with_adapter` | A board may project as a provisional Project workspace; future Paperclip owns canonical identity |
| Ticket | Task | `compatible_with_adapter` | Task can render as a Ticket-shaped projection but keeps Hermes source/ID labels |
| Ticket dependency | Task link | `exact` mechanics | Parent/child DAG is reusable; canonical dependency IDs remain future authority |
| Ticket status | Kanban status | `partial` | Preserve source status; map visually without freezing it as platform ontology |
| Agent assignment | Profile/assignee | `partial` | Assignee is a profile string, not a capability/permission grant |
| Approval request | Review/blocked/comment/event | `misleading` | None is a governed approval object; Approval UI remains unavailable without a contract |
| Execution | Task run | `compatible_with_adapter` | A run is a Hermes attempt, never a governed WorkPacket execution claim |
| Execution timeline | Task events | `compatible_with_adapter` | Useful source-labelled timeline, not the future universal event authority |
| Evidence | Attachments/comments/results | `partial` | Useful references; classification, retention and integrity are incomplete |
| Diagnostic | Kanban diagnostics | `compatible_with_adapter` | Reuse with command validation and source labels |
| WorkPacket | No direct equivalent | `absent` | Never infer WorkPacket scope, permissions, approvals or rollback from a task |
| Human gate | Block/comment/review | `partial` | Interaction hints only; no approve/reject authority |
| Durable control plane | Kanban DB now; Paperclip later | `future_authority_conflict` | Kanban is provisional and replaceable, not a Paperclip substitute |

## Other Reusable Hermes Surfaces

| Target surface | Existing assets | Truth boundary | Reuse decision |
| --- | --- | --- | --- |
| Runtime Overview | `/api/status`, `/api/system/stats`, `PlatformsCard`, sidebar status, Sessions/System pages | `active_sessions` is a five-minute heuristic; status types omit backend fields; failures can remain stale silently | `wrap_existing` and extend typed freshness/source states |
| Approval Inbox | `tools/approval.py`, TUI/desktop approval events and controls, API-server run approvals | Process-local/session-bound FIFO; no dashboard list; desktop has one slot/session and no approval ID; pairing is unrelated | `wrap_existing` visuals only after immutable IDs/list/stream/respond authority exists |
| Execution Inspector | API-server `/v1/runs`, session messages, logs, admin actions, Kanban runs/events | API runs are process-memory and platform-specific; sessions/logs do not prove execution state | `wrap_existing` as source-labelled evidence; future P14/P17 owns truth |
| Safe Settings | Product config, Theme/Language, profile scope, schema form | Config raw YAML, Env/OAuth, MCP, plugins, hooks, memory and Files include secrets/code/paths/processes | `adapt_existing` through a strict allowlist only |
| Frontend Quality | Strict TypeScript, Vitest utilities, responsive shell, release build | Node test environment has no rendered-page, browser, axe or visual coverage; PR CI omits web lint/test/build | `extend_existing` with P13-specific browser/a11y/deep-link gates |

The current command-approval queue can contain multiple items per session,
while the desktop prompt store can display one. An Approval Inbox must add an
immutable approval ID, owner/profile/session, allowed actions, timestamps,
expiry, authorization, list/snapshot, live subscription and exact-item conflict
handling before any action is operational.

The closest execution prototype is optional API-server `/v1/runs`, with
queued/running/waiting/completed/failed/cancelled events. It has no universal
list or durable product-wide store and is unavailable unless that platform is
running. Session activity and log text must not fill this authority gap.

## Design-System Inventory

| Element | Existing state | P13.1 disposition |
| --- | --- | --- |
| Component library | `@nous-research/ui`, shadcn-compatible primitives and Lucide icons | Adopt |
| CSS system | Tailwind 4 plus semantic/custom properties in `web/src/index.css` | Adopt, then alias product semantics |
| Themes | Eight presets, global provider, dark/light behavior and custom-theme escape hatch | Adopt presets; constrain managed product themes |
| Typography | Existing font variables and curated font picker; custom YAML may load arbitrary font URL | Adopt curated set; leave arbitrary URL outside product-safe settings |
| Spacing/borders/surfaces | Repeated Tailwind values and Nous primitives | Alias existing values; extend only missing product semantics |
| Status colors | Success/warning/destructive semantics exist; some chart colors are hardcoded | Adopt semantic colors; extend chart/status mapping |
| Responsive breakpoints | Shell 1024px, document behavior 768px, additional component literals | Alias/centralize in P13.1; do not redesign layout here |
| Icons | Lucide plus manifest string-to-icon map | Adopt; define product route icons centrally |
| Component variants | Existing buttons/dialogs/sheets/cards; repeated loading/empty/error patterns | Adopt and consolidate patterns |
| Accessibility | Some dialog semantics/focus return; no general focus trap; keyboard gaps remain | Extend through P13.8 |
| Legacy effects | `warmGlow`/`noiseOpacity` retained but unused by lightweight shell | Deprecate for product themes |
| Terminal/plugin visuals | xterm palette, remote docs and plugin-owned CSS have separate constraints | Leave untouched |

P13.1 must not create a parallel design system. It should adopt existing
components, alias background/midground/foreground into product semantic
surface/text/border/action names, extend only missing shell/focus/motion/chart
tokens, deprecate unused legacy effects for managed themes and leave terminal
and plugin visuals untouched.

## Provider-Null Manual Inspection

One isolated runtime was created under `9_artifacts/hermes/p13.0/runtime` with
separate `HERMES_HOME`, `HOME`, `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`,
`TEMP`, `TMP`, shared-auth and browser roots. The child environment was cleared
before launch; only Windows/Python essentials, an explicit synthetic session
token, loopback proxy bypass and failing external proxy endpoints were set. A
current synthetic `.update_check` prevented an update request.

Port `9119` was already held by an unrelated loopback Hermes dashboard and was
not terminated or inspected. The isolated dashboard therefore used the free
loopback-only port `9120`. The human manually confirmed that the UI at port
`9120` rendered correctly. Local inspection recorded:

```yaml
P13_0_ProviderNullInspection:
  command: .venv/Scripts/python.exe -m hermes_cli.main dashboard --host 127.0.0.1 --port 9120 --no-open --skip-build
  root_HTTP: 200
  root_bytes: 696
  status_HTTP: 200
  product_configuration_HTTP: 200
  plugin_manifest_HTTP: 200
  gateway_running: false
  active_agents: 0
  active_sessions: 0
  profiles: [default]
  provider_credentials_present: false
  product_id: agent-platform-hermes
  product_version: 0.1.0-dev
  upstream_version: 0.18.2
  product_UI_feature: disabled
  extension_modules: []
  bundled_plugin_routes_observed: [/achievements, /kanban]
  human_visual_reachability_confirmed: true
  VS_Code_loopback_forwarding_supported: true
  real_user_state_used: false
  external_network_operation_performed: false
```

Synthetic Kanban behavior was exercised only inside the isolated home:

- created board `p13-ui-audit` without changing the process-current board;
- created `P13 synthetic parent task` and `P13 synthetic review task`;
- created one parent-child link and one synthetic comment;
- observed tenant filtering, task drawer/detail, events, diagnostics, empty
  attachments and empty run history;
- moved one unassigned task through non-executing `triage`, `todo`,
  `scheduled` and back to `todo`;
- observed that `blocked` is not a generic transition from triage/todo;
- observed `triage_aux_unavailable` diagnostics truthfully reporting no main
  or auxiliary model.

The persistently mounted hidden Chat component repeatedly attempted its PTY
WebSocket even while another page was viewed. Native Windows resolution failed
with `WinError 448` on the OneDrive-mounted `node_modules/@hermes/ink` path
before a TUI, worker or agent task was spawned. This confirms compiled/visible
Chat is not operational in this environment and that hidden persistent runtime
work needs a later lifecycle review.

Graceful owned-tree termination was refused by Windows, so the exact isolated
dashboard launcher/child/console tree required the permitted forced fallback.
Port `9120` closed. The complete isolated runtime, synthetic DB, logs, response
JSON, token and browser root were removed. No user Hermes state was read.

## Capability Reuse Decision Matrix

| Target P13 capability | Existing Hermes assets | Manual evidence | Semantic fit | Decision | Missing capability | Downstream ticket |
| --- | --- | --- | --- | --- | --- | --- |
| Product identity | Product endpoint/context | Exact isolated response | `exact` | `adopt_existing` | Visible dual-version shell treatment | P13.1/P13.2 |
| Design system | Nous UI, themes, CSS variables, Tailwind | Existing shell rendered | `compatible_with_adapter` | `adapt_existing` | Product semantic aliases and quality rules | P13.1 |
| Application shell | App/sidebar/header/profile/plugin shell | Desktop shell reachable | `compatible_with_adapter` | `extend_existing` | Product groups, route protection, title metadata | P13.2 |
| Runtime overview | Status/system/session/sidebar surfaces | Gateway off and zero-agent state observed | `partial` | `wrap_existing` | Typed freshness, source and unavailable states | P13.3 |
| Projects and tickets | Kanban boards/tasks/links/comments/runs/events | Synthetic isolated board/task workflow | `compatible_with_adapter` | `wrap_existing` | Product-neutral projection and defect fixes | P13.4 |
| Approval inbox | Runtime approval queues and desktop controls | No dashboard authority observed | `partial` | `wrap_existing` | IDs, list/stream/respond and authorization contract | P13.5 |
| Execution inspector | Runs/events/sessions/logs/diagnostics | Empty Kanban runs and status evidence observed | `partial` | `wrap_existing` | Durable cross-source execution contract | P13.6 |
| Safe settings | Product config, theme, language, profile context | Disabled feature and safe identity observed | `compatible_with_adapter` | `adapt_existing` | Strict allowlist DTO and write consequences | P13.7 |
| Frontend quality | Typecheck/lint/test/build and responsive shell | Manual desktop reachability only | `partial` | `extend_existing` | Browser, a11y, mobile and deep-link coverage | P13.8 |

Complete binding decision records:

```yaml
P13_0_CapabilityReuseDecisions:
  - target_capability: Product identity
    existing_asset: GET /api/agent-platform/product-configuration and frontend product context
    existing_owner: AGENT_PLATFORM P12.6
    source_evidence: hermes_cli/agent_platform/** and web/src/agent-platform/product-config*
    runtime_evidence: isolated HTTP 200 returned exact product and upstream identity
    semantic_fit: exact
    data_authority: tracked P12.6 ProductConfiguration
    decision: adopt_existing
    rationale: one validated credential-free authority already exists
    required_product_owned_files: [future product-shell consumers only]
    required_upstream_derived_edits: [none preferred]
    upstream_sync_risk: low while consumption stays in product namespace
    security_impact: read-only protected identity; no secret or provider fields
    validation_obligations: schema, auth, null/failure, dual-version and no-duplicate-constant tests
    later_phase_dependency: P13.1 and P13.2
    retirement_or_replacement_condition: accepted upstream equivalent with matching trust boundary

  - target_capability: Design system
    existing_asset: Nous UI, Tailwind, theme provider/presets, CSS variables and Lucide
    existing_owner: Hermes dashboard upstream
    source_evidence: web/src/index.css, themes/** and shared components
    runtime_evidence: existing themed desktop shell rendered on loopback
    semantic_fit: compatible_with_adapter
    data_authority: Hermes theme context and local display preferences
    decision: adapt_existing
    rationale: components and themes are sufficient; product semantics need aliases, not replacement
    required_product_owned_files: [web/src/agent-platform/design-system/** if P13.1 authorizes]
    required_upstream_derived_edits: [none unless a generic component defect requires it]
    upstream_sync_risk: medium for shared CSS and duplicated theme/font catalogs
    security_impact: custom CSS/font URLs remain operator-trusted and outside safe settings
    validation_obligations: theme parity, contrast, responsive, keyboard and screen-reader checks
    later_phase_dependency: P13.1
    retirement_or_replacement_condition: replace_existing requires proof Nous UI cannot meet an accepted product need

  - target_capability: Application shell
    existing_asset: App router/sidebar/header/profile scope and P12.6 static descriptors
    existing_owner: Hermes dashboard upstream plus AGENT PLATFORM P12.6 seam
    source_evidence: web/src/App.tsx, main.tsx, contexts/** and agent-platform/extensions.ts
    runtime_evidence: shell, sidebar, profile status and plugin tabs rendered
    semantic_fit: compatible_with_adapter
    data_authority: central React route/navigation composition
    decision: extend_existing
    rationale: one shell/router already owns persistence, responsive behavior and plugin composition
    required_product_owned_files: [web/src/agent-platform/navigation/**, product page modules]
    required_upstream_derived_edits: [one localized App composition edit only if group/protection seam must widen]
    upstream_sync_risk: high because App.tsx is an upstream synchronization hotspot
    security_impact: product paths must reject dynamic plugin override and fail closed
    validation_obligations: route collision, feature state, deep-link, mobile, profile and plugin coexistence tests
    later_phase_dependency: P13.2 after P13.1 acceptance
    retirement_or_replacement_condition: accepted upstream shell descriptor API supersedes the localized seam

  - target_capability: Runtime overview
    existing_asset: /api/status, /api/system/stats, sidebar status, PlatformsCard, Sessions and System
    existing_owner: Hermes dashboard/runtime
    source_evidence: hermes_cli/web_server.py status/system routes and web status consumers
    runtime_evidence: gateway off, zero agents/sessions and isolated path state observed
    semantic_fit: partial
    data_authority: Hermes status endpoints with explicitly heuristic session activity
    decision: wrap_existing
    rationale: sources are real but incomplete and frontend typing/freshness currently drifts
    required_product_owned_files: [product status adapter and RuntimeOverviewPage]
    required_upstream_derived_edits: [status type correction only if generic seam is insufficient]
    upstream_sync_risk: medium
    security_impact: gated binds may omit host paths/PIDs; overview must not re-expose them
    validation_obligations: live/offline/stale/error/unavailable/profile/gated-bind tests
    later_phase_dependency: P13.3
    retirement_or_replacement_condition: future governed runtime status contract becomes authoritative

  - target_capability: Projects and tickets
    existing_asset: Kanban board/task/link/comment/attachment/event/run/diagnostic UI and API
    existing_owner: Hermes Kanban, provisional under AGENT PLATFORM
    source_evidence: plugins/kanban/**, hermes_cli/kanban*.py, tools and gateway watchers
    runtime_evidence: isolated synthetic board, two linked tasks, comment, events, diagnostics and empty runs
    semantic_fit: compatible_with_adapter
    data_authority: Hermes Kanban DB today; future Paperclip control plane
    decision: wrap_existing
    rationale: mature work UI exists, but raw schema/IDs/statuses cannot become canonical platform contracts
    required_product_owned_files: [Kanban projection DTO/adapter and product Projects/Tickets views]
    required_upstream_derived_edits: [bounded fixes for board deletion, attachment cleanup and multi-drag before write exposure]
    upstream_sync_risk: high across bundled plugin API/dist and fast-moving Kanban kernel
    security_impact: board selection, filesystem attachments and dispatcher-triggering fields require strict bounds
    validation_obligations: board isolation, CRUD target, dependency, non-executing status, retention, no-dispatch and projection tests
    later_phase_dependency: P13.4; Paperclip transition later
    retirement_or_replacement_condition: Paperclip cutover provides canonical projects/tickets with validated export and rollback

  - target_capability: Approval inbox
    existing_asset: process-local approval queue, TUI/API-run events and desktop approval controls
    existing_owner: Hermes runtime/session authority
    source_evidence: tools/approval.py, tui_gateway/server.py, gateway slash commands and desktop approval component/store
    runtime_evidence: no dashboard approval list or operational approval state in provider-null UI
    semantic_fit: partial
    data_authority: session-bound Hermes runtime queue only
    decision: wrap_existing
    rationale: interaction patterns are reusable but no product-wide identity/list/authorization contract exists
    required_product_owned_files: [approval projection types and unavailable-first ApprovalInboxPage]
    required_upstream_derived_edits: [generic approval ID/list/stream/respond seam only after separate runtime contract]
    upstream_sync_risk: high
    security_impact: exact request ownership, redaction, expiry and authorization are mandatory
    validation_obligations: multiple-pending, stale/conflict, keyboard/focus, redaction and unauthorized-response tests
    later_phase_dependency: P13.5 and later runtime authority
    retirement_or_replacement_condition: governed approval adapter supersedes process-local queue projection

  - target_capability: Execution inspector
    existing_asset: API-server runs, Kanban runs/events, sessions, logs, diagnostics and admin actions
    existing_owner: multiple Hermes subsystems
    source_evidence: gateway/platforms/api_server.py, session APIs, logs and Kanban run APIs
    runtime_evidence: source-labelled empty run history and diagnostics observed; no execution performed
    semantic_fit: partial
    data_authority: each current source owns only its local facts
    decision: wrap_existing
    rationale: composition can improve observability without inventing universal execution state
    required_product_owned_files: [execution source adapters and read-only ExecutionInspectorPage]
    required_upstream_derived_edits: [none in P13.6 unless a generic read API is approved]
    upstream_sync_risk: medium
    security_impact: logs/messages/artifacts may contain sensitive content and need bounded display
    validation_obligations: provenance, missing-source, ordering, redaction, deep-link and no-inference tests
    later_phase_dependency: P13.6; P14/P17 for future truth
    retirement_or_replacement_condition: governed durable execution/event contract becomes authoritative

  - target_capability: Safe settings
    existing_asset: product config, ThemeSwitcher, LanguageSwitcher, profile context and schema form
    existing_owner: AGENT PLATFORM product config plus Hermes display config
    source_evidence: product_config.py, ConfigPage, EnvPage, ModelsPage, PluginsPage and McpPage
    runtime_evidence: safe identity/disabled feature observed; no credential/provider state inherited
    semantic_fit: compatible_with_adapter
    data_authority: tracked product config for identity/features; whitelisted Hermes config for preferences
    decision: adapt_existing
    rationale: only a narrow non-secret/non-executable subset is safe
    required_product_owned_files: [safe-settings allowlist DTO and SafeSettingsPage]
    required_upstream_derived_edits: [none preferred]
    upstream_sync_risk: medium because config schemas evolve
    security_impact: raw YAML, env/OAuth, providers, MCP, plugins, hooks and arbitrary paths are excluded
    validation_obligations: allowlist, profile target, secret absence, restart impact and stale-write tests
    later_phase_dependency: P13.7
    retirement_or_replacement_condition: accepted centralized safe-preference API replaces the allowlist adapter

  - target_capability: Frontend quality
    existing_asset: strict TypeScript, ESLint, Vitest, production build and responsive shell
    existing_owner: Hermes web toolchain
    source_evidence: web/package.json, tsconfig, Vitest and CI/release workflows
    runtime_evidence: desktop shell and deep-link-capable SPA served from integrated assets
    semantic_fit: partial
    data_authority: repository validation configuration
    decision: extend_existing
    rationale: tooling exists but rendered browser, accessibility and PR gates are incomplete
    required_product_owned_files: [P13 tests and quality configuration only when P13.8 authorizes]
    required_upstream_derived_edits: [shared CI/config changes only with explicit ownership]
    upstream_sync_risk: medium
    security_impact: quality gate must test no secret exposure and no unauthorized network/runtime activation
    validation_obligations: unit, route, feature, type, lint, build, startup, deep-link, mobile, keyboard, screen-reader and console checks
    later_phase_dependency: P13.8
    retirement_or_replacement_condition: accepted upstream browser/a11y quality gate fully covers product routes
```

No `replace_existing` decision is made in P13.0. Consequently the count of
replacement decisions lacking structural evidence is zero.

## Product Brief

AGENT PLATFORM Hermes is a truthful, human-controlled browser workspace for a
product owner or engineer to understand platform health, navigate provisional
projects and tickets, find pending human decisions, inspect execution evidence
and use safe preferences while reusing Hermes as the implementation foundation.
P13 creates the product-facing information architecture and bounded UI; it does
not provide providers, autonomous workers, WorkPacket execution, canonical
Paperclip work control, GBrain knowledge or production readiness.

The product solves fragmentation, not lack of raw capability. Hermes already
has broad pages, plugins, Kanban and runtime data, but their terminology,
authority, safety and availability differ. P13 composes those facts into a
coherent product surface without claiming unavailable capabilities.

## Primary and Secondary Users

Primary user:

```yaml
role: human product owner / engineer
location: local workstation or remote development host
responsibilities:
  - review agent-related work manually
  - control ticket sequencing and blockers
  - approve repository changes through human Git authority
  - inspect evidence and diagnostics
  - distinguish available, disabled and unauthorized capability
needs:
  - truthful operational state
  - stable deep links and profile scope
  - explicit data provenance
  - safe non-secret preferences
```

Secondary/future users are reviewer, approver, platform operator, project
owner, agent developer and runtime administrator. They are not evidence of a
current enterprise multi-user product or access-control model.

## Jobs to Be Done

- Understand current product, upstream, gateway and capability state.
- Find a provisional project, board, ticket or task without confusing its
  current source authority.
- Understand dependencies, blockers, assignments and non-executing work state.
- Identify pending human decisions without fabricating an approval contract.
- Inspect what a Hermes run/session did and where each fact came from.
- Review comments, attachments, events, outcomes, errors and diagnostics.
- See disabled, unavailable, unconfigured, stale and provider-gated states.
- Navigate to existing Hermes tools without copying their implementations.
- Verify product version and immutable upstream version/commit together.
- Change only explicitly safe, non-secret, non-executable preferences.

## Product Principles

1. Truthful capability representation: visibility is not operational proof.
2. Human authority: UI actions never supersede review, Git or runtime gates.
3. Reuse before extension and extension before replacement.
4. Observable work: facts carry source, freshness and limitation labels.
5. Safe defaults: absent configuration fails closed and sensitive settings stay
   outside the product-safe surface.
6. Explicit unavailable states: disabled runtime/provider features are shown as
   unavailable, not simulated.
7. Reversible product divergence: product-owned files and localized upstream
   edits retain owners, rollback and synchronization predicates.
8. Upstream-aware customization: one shell, router, plugin loader, theme system
   and work substrate are reused.

## Non-Goals

- Provider or model activation, OAuth or credential management.
- Agent autonomy, dispatcher/worker startup or WorkPacket execution.
- A new task/work-control backend or permanent Kanban authority.
- Paperclip emulation, GBrain integration or durable knowledge UI.
- Production deployment, public SaaS, billing or enterprise multi-user access.
- Secret-management UI, raw environment/config editing or provider settings.
- A second router, plugin mechanism, design system, chat or execution history.
- A complete Hermes visual redesign or changes to existing route behavior in
  P13.0.

## Canonical UI Vocabulary

| UI term | User-facing definition | Current Hermes equivalent / authority | Future authority | Equivalence | P13 usage | Not to be inferred |
| --- | --- | --- | --- | --- | --- | --- |
| Project | Human-recognizable body of related work | Kanban Board in Hermes Kanban DB | Paperclip/control plane | `compatible_with_adapter` | Label a provisional board projection as Project | Board is not permanent canonical Project identity |
| Ticket | Unit of planned work with state and dependencies | Kanban Task in Hermes Kanban DB | Paperclip/control plane | `compatible_with_adapter` | Ticket presentation may wrap a task | Task is not a WorkPacket or governed Ticket contract |
| Board | Hermes operational container and isolation boundary | Kanban Board / Kanban DB root | Hermes adapter or retired after Paperclip | `exact` | Display source type and board slug | Tenant, project or access-control boundary |
| Task | Hermes work-queue record | Kanban Task | Hermes runtime projection | `exact` | Use in Hermes/source details | Canonical Ticket or authorized execution |
| Approval | Explicit human decision over a uniquely identified request | Session approval queue; no dashboard-wide authority | Governed approval adapter/runtime | `partial` | Unavailable until ID/list/respond contract exists | Review/blocked/pairing equals approval |
| Execution | Governed attempt with identity, state, evidence and authority | Partial API runs, Kanban runs, sessions/actions | P14/P17 runtime | `partial` | Source-labelled composition only | Recent session or task run equals WorkPacket execution |
| Run | One attempt recorded by its source system | Kanban run or optional API-server run | Governed execution adapter | `compatible_with_adapter` | Always display source and local ID | Universal execution record |
| Agent | Governed actor with accepted capabilities and permissions | No complete UI equivalent | P14/P15/P17 runtime | `absent` | Unavailable capability label | Profile, PID or session proves Agent authority |
| Profile | Hermes configuration/session isolation identity | Hermes profile registry | Hermes runtime | `exact` | Preserve selected profile scope | Assignee capability, person or access-control role |
| Worker | Process attempting an assigned Hermes task | Kanban dispatcher-spawned process | P14/P17 runtime | `compatible_with_adapter` | Read-only source detail when later authorized | Worker is an Agent or currently enabled |
| Capability | Product-visible ability and its truthful state | P12.6 feature-state contract plus observed Hermes surface | AGENT PLATFORM | `compatible_with_adapter` | Use enabled/disabled/unavailable/experimental | Route visibility means capability works |
| Feature | Product-controlled exposure unit | P12.6 feature flag and static descriptor | AGENT PLATFORM | `exact` | Stable product-owned ID | Feature flag authorizes runtime execution |
| Evidence | Source-attributed material supporting review | Comments, attachments, results, logs and messages | Governed evidence contract | `partial` | Link with source, classification and limits | Existing content has complete integrity/retention |
| Artifact | File or durable output produced/attached by a source | Kanban attachment, file, export or generated output | Governed artifact store | `partial` | Display only through bounded references | Arbitrary Files-page path is a safe artifact |
| Diagnostic | Structured or textual indication of a problem/action | Kanban diagnostics, logs and status errors | Source owner plus governed projection | `compatible_with_adapter` | Preserve severity/source and validate actions | Diagnostic suggestion is automatically safe |
| Event | Ordered source fact about a state change | Kanban task event or API-run event | Governed event contract | `compatible_with_adapter` | Source-labelled timeline item | Cross-source global ordering or causality |
| Provider | External model/service integration | Models, Env/OAuth and provider plugins | P15 | `exact` identity, unavailable authority | Show disabled/unavailable state only | Provider is configured, authorized or callable |
| Runtime | System that performs governed work | Hermes gateway/agent/worker mechanics | P14/P17 | `partial` | Show current Hermes status and future boundary | Dashboard availability means runtime authority |

This vocabulary is presentation and information architecture only. It creates
no backend schema, persistent identity, state machine or adapter contract.

## Data-Authority Map

| Information | Current available source | P13 posture | Future expected authority |
| --- | --- | --- | --- |
| Product identity | P12.6 product configuration | Adopt exactly | AGENT PLATFORM |
| Feature state | P12.6 product configuration | Adopt; never infer runtime authority | AGENT PLATFORM |
| Hermes sessions | Hermes session DB/runtime | Adopt or wrap with profile/source labels | Hermes runtime |
| Kanban tasks | Hermes Kanban DB | Wrap as provisional Projects/Tickets substrate | Hermes adapter, then Paperclip decision |
| Projects/tickets | No final canonical authority | Do not invent; use explicit provisional projection | Paperclip/control plane later |
| Approval requests | Session-local queue; no complete dashboard contract | Unavailable-first model; wrap only after authority exists | Governed approval adapter/runtime |
| Executions | Partial API/Kanban runs, sessions, events and actions | Compose read-only facts; never synthesize missing truth | P14/P17 runtime |
| Evidence/artifacts | Comments, attachments, logs, messages and results | Source-labelled, bounded and classification-aware | Governed evidence/artifact contracts |
| Durable knowledge | Not available in P13 | Unavailable | GBrain P19 |
| Work control plane | Not available in P13 | Do not create | Paperclip P20 |
| Provider status | Disabled/not authorized | Read-only unavailable state | P15 |
| Worker execution | Not authorized | Unavailable | P14/P15/P17 |

Binding statement:

```text
P13 must not create a new persistent project/ticket authority.
```

Kanban is classified as an existing operational work surface and provisional
product substrate. It is adaptable and wrappable, not permanent canonical
authority. Future Paperclip replacement requires a separate export, identity,
count-validation, cutover, rollback and no-dual-write decision.

## Information Architecture

Two models were evaluated:

| Model | Benefit | Cost/risk | Decision |
| --- | --- | --- | --- |
| A: Product-first top-level replacement | Product terms dominate immediately | Reorders/duplicates broad Hermes capabilities, raises App.tsx sync risk and suggests authority P13 lacks | Rejected |
| B: Product namespace inside existing shell | Reuses one shell/router, keeps Hermes tools reachable and permits fail-closed product routes | Requires a bounded group/protection extension to the P12.6 seam | Selected |

Selected hierarchy:

```text
Existing global Hermes shell
  AGENT PLATFORM
    Overview
    Projects
      Project / board context
      Ticket / task details
    Approvals
      Approval details (unavailable until authority exists)
    Executions
      Execution / source-run details
    Settings
  Hermes Tools
    Existing Hermes work and capability routes
  Administration
    Existing configuration, connection and system routes
  Contextual surfaces
    profile scope, source labels, evidence drawers, diagnostics
  Semantic states
    loading, empty, stale, error, unavailable, not configured
```

The product group is additive inside the existing shell. It does not replace
the router or plugin loader. Existing route paths remain stable. Direct Kanban
remains an upstream/plugin deep link, but once the Projects wrapper is accepted
it should not appear as a second primary product work entry.

Product-owned route namespace: `/agent-platform/**`.

Rationale:

- no current built-in or observed bundled plugin uses the prefix;
- the prefix makes ownership and future synchronization review explicit;
- static product descriptors can reject exact built-in collisions;
- product deep links remain distinct from upstream routes;
- dynamic plugin override still requires P13.2 hardening before activation;
- one high-level namespace avoids generic collisions such as `/projects`.

## Route Architecture

No route is registered by P13.0. Candidate exact descriptors are:

```yaml
P13_0_CandidateRoutes:
  - route_id: agent_platform.ui.overview
    candidate_path: /agent-platform/overview
    page_title: Overview
    navigation_group: AGENT PLATFORM
    owner: AGENT_PLATFORM
    P13_ticket: P13.3
    feature_id: agent_platform.product_ui
    visibility_state: first experimental route after P13.R authorization
    existing_surface_reused: status, system stats, sessions and sidebar status
    current_data_source: Hermes /api/status and /api/system/stats
    future_data_source: governed runtime status adapter
    read_only_or_write: read_only
    empty_state: No active or recent Hermes activity
    unavailable_state: Runtime status unavailable; no execution inferred
    error_state: Source-specific error with last-success timestamp
    deep_link_required: true
    collision_checked: no built-in or observed plugin exact-path collision

  - route_id: agent_platform.ui.projects
    candidate_path: /agent-platform/projects
    page_title: Projects
    navigation_group: AGENT PLATFORM
    owner: AGENT_PLATFORM
    P13_ticket: P13.4
    feature_id: agent_platform.product_ui
    visibility_state: disabled until P13.4 acceptance
    existing_surface_reused: Kanban boards and filters
    current_data_source: provisional Hermes Kanban DB through projection adapter
    future_data_source: Paperclip/control-plane adapter
    read_only_or_write: bounded non-executing writes only after defect fixes
    empty_state: No provisional projects/boards
    unavailable_state: Work-control source unavailable; no backend created
    error_state: Board-scoped error preserving selected source
    deep_link_required: true
    collision_checked: no built-in or observed plugin exact-path collision

  - route_id: agent_platform.ui.project_detail
    candidate_path: /agent-platform/projects/:boardSlug
    page_title: Project
    navigation_group: contextual
    owner: AGENT_PLATFORM
    P13_ticket: P13.4
    feature_id: agent_platform.product_ui
    visibility_state: disabled until P13.4 acceptance
    existing_surface_reused: Kanban board columns, filters and diagnostics
    current_data_source: selected Hermes Kanban board
    future_data_source: Paperclip project projection
    read_only_or_write: bounded non-executing writes only
    empty_state: Project contains no tickets/tasks
    unavailable_state: Selected board missing or source unavailable
    error_state: Board-specific error without fallback to process-current board
    deep_link_required: true
    collision_checked: namespace and dynamic-segment overlap conceptually checked

  - route_id: agent_platform.ui.ticket_detail
    candidate_path: /agent-platform/projects/:boardSlug/tickets/:taskId
    page_title: Ticket
    navigation_group: contextual
    owner: AGENT_PLATFORM
    P13_ticket: P13.4
    feature_id: agent_platform.product_ui
    visibility_state: disabled until P13.4 acceptance
    existing_surface_reused: Kanban task drawer, links, comments, attachments, events, runs and diagnostics
    current_data_source: selected-board Hermes task projection
    future_data_source: Paperclip ticket plus governed evidence/execution adapters
    read_only_or_write: comments, links and approved non-executing metadata/status writes only
    empty_state: No evidence, comments or runs yet
    unavailable_state: Task missing, board mismatch or source unavailable
    error_state: Source-specific failure; never search another board implicitly
    deep_link_required: true
    collision_checked: namespace and dynamic-segment overlap conceptually checked

  - route_id: agent_platform.ui.approvals
    candidate_path: /agent-platform/approvals
    page_title: Approvals
    navigation_group: AGENT PLATFORM
    owner: AGENT_PLATFORM
    P13_ticket: P13.5
    feature_id: agent_platform.product_ui
    visibility_state: unavailable until approval authority contract exists
    existing_surface_reused: desktop approval interaction patterns and runtime queue projection
    current_data_source: no complete dashboard authority
    future_data_source: governed approval adapter/runtime
    read_only_or_write: read_only unavailable state initially
    empty_state: No pending approval requests from an authoritative source
    unavailable_state: Approval inbox is not operational in P13
    error_state: Approval source error; actions remain disabled
    deep_link_required: true
    collision_checked: no built-in or observed plugin exact-path collision

  - route_id: agent_platform.ui.approval_detail
    candidate_path: /agent-platform/approvals/:approvalId
    page_title: Approval
    navigation_group: contextual
    owner: AGENT_PLATFORM
    P13_ticket: P13.5
    feature_id: agent_platform.product_ui
    visibility_state: unavailable until immutable approval IDs exist
    existing_surface_reused: redacted command/evidence and desktop decision controls
    current_data_source: none with required identity/authorization
    future_data_source: governed approval adapter/runtime
    read_only_or_write: no operational write until exact-item response contract
    empty_state: not_applicable
    unavailable_state: Approval identity is not operational
    error_state: stale/conflict/unauthorized request with no fallback action
    deep_link_required: true
    collision_checked: namespace and dynamic-segment overlap conceptually checked

  - route_id: agent_platform.ui.executions
    candidate_path: /agent-platform/executions
    page_title: Executions
    navigation_group: AGENT PLATFORM
    owner: AGENT_PLATFORM
    P13_ticket: P13.6
    feature_id: agent_platform.product_ui
    visibility_state: disabled until P13.6 acceptance
    existing_surface_reused: Kanban/API runs, sessions, events, logs and diagnostics
    current_data_source: multiple source-local Hermes records
    future_data_source: P14/P17 governed execution/event adapter
    read_only_or_write: read_only
    empty_state: No execution-like records from enabled sources
    unavailable_state: No authoritative execution source available
    error_state: Per-source errors without synthesized status
    deep_link_required: true
    collision_checked: no built-in or observed plugin exact-path collision

  - route_id: agent_platform.ui.execution_detail
    candidate_path: /agent-platform/executions/:executionId
    page_title: Execution
    navigation_group: contextual
    owner: AGENT_PLATFORM
    P13_ticket: P13.6
    feature_id: agent_platform.product_ui
    visibility_state: disabled until stable projection IDs exist
    existing_surface_reused: run/event/session/log/diagnostic detail patterns
    current_data_source: source-qualified local run or session reference
    future_data_source: governed execution/event adapter
    read_only_or_write: read_only
    empty_state: Execution has no linked evidence yet
    unavailable_state: Source or projected record unavailable
    error_state: Preserve source identity and show bounded failure
    deep_link_required: true
    collision_checked: namespace and dynamic-segment overlap conceptually checked

  - route_id: agent_platform.ui.settings
    candidate_path: /agent-platform/settings
    page_title: Settings
    navigation_group: AGENT PLATFORM
    owner: AGENT_PLATFORM
    P13_ticket: P13.7
    feature_id: agent_platform.product_ui
    visibility_state: disabled until safe allowlist acceptance
    existing_surface_reused: product config, theme, language and profile context
    current_data_source: P12.6 config plus whitelisted Hermes display settings
    future_data_source: AGENT PLATFORM safe preference contract
    read_only_or_write: read-only identity plus narrowly whitelisted preference writes
    empty_state: No optional safe preferences
    unavailable_state: Safe settings contract unavailable; link to no secret surface
    error_state: Target-profile and persistence failure with no raw-config fallback
    deep_link_required: true
    collision_checked: no built-in or observed plugin exact-path collision
```

Feature behavior is fail-closed. With `agent_platform.product_ui` disabled or
the descriptor ID absent from `extension_modules`, product routes and
navigation are not registered; current unknown-route behavior returns users to
`/sessions`. Experimental descriptors render only when explicitly marked
`visibleWhenExperimental`. Configuration failure registers nothing. P13.2 must
also prevent dynamic plugin override of `/agent-platform/**` and check dynamic
segment ambiguity before any route is enabled.

## Navigation Groups

Final order after later implementation and activation:

| Group | Ordered items | Existing-route treatment |
| --- | --- | --- |
| AGENT PLATFORM | Overview, Projects, Approvals, Executions, Settings | New static product descriptors only |
| Hermes Tools | Chat, Sessions, Files, Cron, Skills, Models, optional trusted plugin tabs | Retain route paths; keep current position relative to each other |
| Administration | Logs, conditional Analytics, Plugins, MCP, Channels, Webhooks, Pairing, Profiles, Config, Keys, System, Documentation | Retain route paths; move labels into group only through P13.2 central composition |
| Contextual | Project/Ticket, Approval and Execution details | Deep links/breadcrumbs; never primary sidebar entries |

Existing route decisions:

| Route | Navigation decision |
| --- | --- |
| `/chat`, `/sessions`, `/files`, `/cron`, `/skills`, `/models` | Retain under Hermes Tools |
| `/analytics` | Retain hidden unless its existing configuration enables truthful local estimates; place under Administration when visible |
| `/logs`, `/plugins`, `/mcp`, `/channels`, `/webhooks`, `/pairing`, `/profiles`, `/config`, `/env`, `/system`, `/docs` | Move to Administration group later without changing paths |
| `/profiles/new` | Keep contextual to Profiles; no primary entry |
| `/kanban` | Keep reachable as the underlying Hermes plugin; hide from primary product navigation only after the Projects wrapper reaches parity |
| `/achievements` | Leave optional plugin-owned position; not a P13 product capability |

P13.2 must extend the existing central composition rather than add another
router/sidebar/plugin loader. The current P12.6 descriptor has placement but no
group metadata; adding a generic product-navigation group field is preferred to
hardcoding each product page in `App.tsx`.

## Surface Definitions

### Runtime Overview - P13.3

Responsibilities:

- compose product/upstream identity, gateway liveness, state, active-agent
  count, busy/drainability, configured platform state, host metrics where
  authorized and recently active session heuristics;
- show source, selected profile, last successful refresh, stale/error and
  unavailable state;
- link to existing System, Sessions and Logs details;
- remain read-only.

Non-responsibilities:

- starting/stopping/restarting gateway, providers, workers or agents;
- presenting a recent session as a running execution;
- treating absent host paths/PIDs on gated binds as zero;
- inferring WorkPacket, Paperclip or GBrain availability.

### Projects and Tickets Workspace - P13.4

Decision: `wrap_existing` Kanban as a provisional substrate. Board projects and
task tickets must retain source IDs/labels and pass through a product-neutral
projection. P13.4 must first resolve wrong-board deletion, attachment cleanup
and multi-card drag defects or keep affected writes disabled.

Permitted P13 writes after specific validation are board/task metadata, parent
links, synthetic/non-secret comments, classified attachments and transitions
among non-executing states. Assignment to runnable profiles, `ready` dispatch,
worker claim, real `dir:`/worktree paths, decompose/specify/swarm, reclaim of a
real worker and dispatcher controls remain unavailable.

Comments and attachments are evidence candidates, not approvals or canonical
artifacts. Dependency links are reusable mechanics. A future Paperclip cutover
replaces canonical project/ticket authority; Kanban may remain a runtime
projection only if a later contract explicitly accepts it.

### Approval Inbox - P13.5

An approval request requires immutable identity, request type, owner/profile/
session, redacted description, evidence, allowed decisions, creation/expiry,
authorization and exact-item response semantics. Pairing approvals, Kanban
`review`, `blocked`, comments and events do not satisfy this definition.

Existing desktop controls may be wrapped for presentation after the runtime
contract exists. Until then the route shows a truthful unavailable state;
approve, reject and request-changes actions remain disabled, not demonstrative.
No Kanban status transition is a governed approval decision.

### Execution Inspector - P13.6

The inspector may compose source-qualified Kanban runs/events, optional
API-server runs, sessions/messages, logs, summaries, outcomes, errors,
diagnostics and artifact references. Every item carries source type/local ID,
profile, freshness and retention limitation.

It must not synthesize a universal status from session recency, log text or
admin PIDs; call a task run WorkPacket execution; imply durable event retention;
or offer stop/retry/rollback actions. P14/P17 is the future execution source.

### Safe Settings and Feature Flags - P13.7

Initial safe allowlist:

| Allowed | Conditions |
| --- | --- |
| Product/upstream identity and feature states | Read-only from P12.6 |
| Theme and curated font | Existing trusted identifiers only |
| Language | Existing supported locale identifiers |
| Layout density/navigation preference | Non-secret, non-executable, profile target shown |
| Product feature state | Read-only until a separate activation authority changes tracked config |

Blocked from Safe Settings:

```text
API keys and provider tokens
OAuth state
private endpoints or registry credentials
.env and raw secret-bearing environment variables
raw config YAML
arbitrary URLs, commands or filesystem paths
MCP configuration/secrets
plugin installation or code enablement
hooks, memory-provider setup or gateway lifecycle
```

Each write must show target profile, persistence authority, restart/session
impact and failure state. There is no fallback from a safe-form failure to raw
config or Keys.

### Frontend Quality Gate - P13.8

Every implementation ticket must preserve or add:

- targeted unit and behavior tests;
- route-resolution, collision and feature-state tests;
- TypeScript and affected ESLint checks;
- production dashboard build;
- provider-null dashboard startup;
- direct deep links, reload and back/forward behavior;
- selected-profile query persistence;
- mobile navigation and modal focus containment;
- keyboard operation and basic screen-reader semantics;
- explicit loading/empty/stale/error/unavailable states;
- no console errors, secret exposure or unauthorized external requests;
- modification-register hash/ownership reconciliation;
- upstream-derived versus product-owned diff classification.

Current Node-only Vitest utility tests are not sufficient browser UI coverage.
P13.8 should add rendered component/a11y tests and a browser smoke path without
reclassifying inherited P12.4 debt.

## UI State Model

Capability states reuse P12.6 exactly:

| State | UI meaning |
| --- | --- |
| `enabled` | Accepted capability is available under its own runtime/data rules |
| `disabled` | Intentionally off; no route/action registration unless a separate explanatory surface is accepted |
| `unavailable` | Product knows the capability but its authority/prerequisite does not exist |
| `experimental` | Explicitly opt-in preview; visibly labelled and never treated as production-ready |

Data states:

| State | Meaning |
| --- | --- |
| `loading` | First authoritative request is pending |
| `ready` | Current source responded with usable data |
| `empty` | Authoritative source responded successfully with no records |
| `stale` | Previously ready data remains visible with age/source and refresh warning |
| `error` | Source failed; preserve last-known data only as stale |
| `unavailable` | Authority/source is absent or prohibited |
| `not_configured` | Capability is permitted in principle but lacks non-secret setup |

Work state remains source-qualified Hermes Kanban state. P13 may visually map
`triage`, `todo`, `scheduled`, `ready`, `running`, `blocked`, `review`, `done`
and `archived`, but must not persist a new platform Ticket state machine.
`review` is labelled non-authoritative and `scheduled` is a waiting state.

Provisional approval vocabulary is `pending`, `approved`, `rejected`,
`changes_requested`, `cancelled` and `expired`. All remain non-operational until
the approval authority contract exists.

Provisional execution vocabulary is `queued`, `running`, `blocked`,
`awaiting_approval`, `succeeded`, `failed`, `cancelled` and `rolled_back`.
P13 does not persist these states; a source adapter may display only states it
can prove and must preserve the original source value.

## Product Feature Activation Plan

Current invariant:

```yaml
agent_platform.product_ui: disabled
extension_modules: []
```

Lifecycle:

1. P13.0 defines architecture only; feature and registry remain unchanged.
2. P13.1 establishes accepted aliases/tokens without activating a route.
3. P13.2 extends the existing shell/descriptor seam, protects the namespace and
   keeps descriptors unregistered.
4. P13.3 implements the first read-only candidate route,
   `/agent-platform/overview`, with route/feature/provider-null tests.
5. P13.4-P13.7 add only accepted descriptors/surfaces behind the same root
   feature and their own truthful unavailable states.
6. P13.8 validates type, lint, build, browser, deep-link, mobile, accessibility,
   secret and modification-register obligations.
7. P13.R alone may authorize tracked configuration to move the root feature
   from `disabled` to `experimental` and register the accepted module IDs.
8. `enabled` requires a later P13.R decision after all intended product routes,
   rollback and inherited-debt treatment are accepted; experimental is not an
   automatic path to enabled.

Rollback returns the tracked feature to `disabled`, removes the corresponding
module IDs, verifies no route/navigation resolution and uses the registered
P12.7/P13 divergence rollback predicates. It does not delete user Kanban data.

## P13 Downstream Handoff Matrix

| Ticket | Inputs from P13.0 | Existing capability to reuse | Allowed implementation class | Key prohibition |
| --- | --- | --- | --- | --- |
| P13.1 | Design-system inventory, values and product identity treatment | Nous UI, themes and CSS variables | Adopt/alias/extend tokens | No parallel design system |
| P13.2 | Model B shell, groups, namespace and collision rules | App/sidebar plus P12.6 descriptors | Adapt/extend central seam | No second router/sidebar/plugin loader |
| P13.3 | Runtime source map and state semantics | Status/system/session/sidebar | Compose/wrap read-only | No provider/worker/lifecycle activation |
| P13.4 | Provisional Kanban mapping, defects and write limits | Boards/tasks/links/comments/events/runs | Wrap/adapt after defect gates | No second task backend or permanent authority |
| P13.5 | Approval definition and missing authority | Runtime queue plus desktop controls | Wrap/unavailable-first | No false approval or pairing/review equivalence |
| P13.6 | Execution vocabulary/source map | Runs/events/sessions/logs/diagnostics | Compose/wrap read-only | No invented execution truth or WorkPacket claim |
| P13.7 | Safe allowlist and excluded trust surfaces | Product config, theme, language and profile | Narrow adapt/wrap | No secrets/providers/raw config/code/paths |
| P13.8 | Quality obligations and known gaps | Existing web tooling | Extend/validate | No reclassification of upstream/P12.4 debt |

P13.1 may proceed after this record is accepted and committed. P13.2 remains
blocked until P13.1 is accepted. Later implementation tickets must cite the
exact reuse decision row above and update the divergence register for every
new or modified tracked product path.

## Remote Development and Inspection Workflow

Supported development posture:

```text
Desktop PC:
  Hermes dashboard on 127.0.0.1:9119
  optional Vite on 127.0.0.1:5173 only when integrated assets are insufficient

VS Code Remote-SSH:
  forward remote port 9119 or 5173 to a local laptop port

Laptop:
  open the VS Code-provided localhost URL
```

PowerShell is required for supplied PowerShell commands; `cmd.exe` does not
accept PowerShell syntax. Ports remain loopback-only. No public IP, `0.0.0.0`,
LAN publication, router forwarding or firewall change is needed.

P13.0 used `9120` only because `9119` was occupied before the isolated audit.
The same VS Code forwarding model applies to the selected loopback port. This
is a development convenience, not a deployment model.

## Risk and Conflict Register

| ID | Risk/conflict | Required treatment |
| --- | --- | --- |
| R1 | Reimplementing Kanban under product terminology | Mandatory `wrap_existing` decision and decision-row citation |
| R2 | Treating Kanban as permanent Paperclip replacement | Keep provisional authority/source labels and define future cutover |
| R3 | UI claims nonexistent runtime/provider capability | Explicit disabled/unavailable states and source-qualified facts |
| R4 | Exposing secret-bearing settings | Strict allowlist; exclude Env/OAuth/raw config/providers/MCP/plugins/paths |
| R5 | Scattered upstream UI edits | Product-owned namespace and one central descriptor/group seam |
| R6 | Dynamic plugins override product routes | Protect `/agent-platform/**` before feature activation |
| R7 | Upstream synchronization conflicts | Classify every product/upstream edit with reapplication and rollback predicates |
| R8 | Parallel design system | Adopt Nous UI/themes and alias/extend only evidenced gaps |
| R9 | Task runs confused with WorkPacket execution | Use source-labelled Run; state direct non-equivalence |
| R10 | Remote UI inaccessible | Loopback dashboard plus VS Code port forwarding; no public bind |
| R11 | Visual inspection reads real user state | Mandatory isolated home/config/auth/temp roots |
| R12 | UI audit starts workers | Keep gateway/dispatcher/profile assignment/decompose/swarm off |
| R13 | Wrong-board Kanban deletion | Fix query scoping and add cross-board regression tests before product writes |
| R14 | Attachment orphan/leak on task deletion | Add DB/file cascade and retention tests before attachment exposure |
| R15 | Multi-card drag runtime exception | Replace undefined symbol path and test destructive/non-destructive drag |
| R16 | Review/blocked status presented as approval | Keep Approval unavailable until immutable authority contract exists |
| R17 | Session recency presented as execution | Label heuristic and never synthesize execution state |
| R18 | Plugin/custom-theme code or CSS treated as constrained data | Label operator-trusted boundary; keep outside product-safe settings |
| R19 | Hidden Chat starts runtime work on unrelated pages | Review connection lifecycle; keep native-Windows Chat constrained |
| R20 | Current broad baseline debt is hidden by targeted green checks | Carry P12.4 Python/type/lint/TUI/desktop failures into every P13 gate |

## Open Decisions

These are downstream design decisions, not blank central reuse decisions:

| Decision owner | Open detail | Fixed P13.0 boundary |
| --- | --- | --- |
| P13.1 | Exact semantic token names and contrast targets | Must alias/extend existing system, not replace it |
| P13.2 | Generic descriptor shape for navigation groups and protected product paths | Must use central shell/router and `/agent-platform/**` |
| P13.3 | Refresh interval and host-metric disclosure on gated binds | Must show source/freshness and remain read-only |
| P13.4 | Exact product DTO names and permitted write subset after defect fixes | Kanban is provisional; no second backend/dispatcher action |
| P13.5/runtime owner | Approval identity/list/stream/respond transport | Route remains unavailable until authority exists |
| P13.6/P14/P17 | Durable execution identity and retention | P13.6 remains source-labelled/read-only |
| P13.7 | Exact safe preference allowlist and persistence impact | Secrets, code, providers and arbitrary paths stay excluded |
| P13.8 | Browser/a11y tool selection compatible with frozen dependencies | No dependency install/change without separate authorization |

## Limitations

- Manual visual reachability was human-confirmed at loopback port `9120`; no
  retained screenshot or browser profile exists.
- Port `9119` was occupied at audit start, so the isolated audit used `9120`.
- The hidden persistent Chat host generated repeated native-Windows PTY errors;
  Chat was not operational and no TUI/agent was spawned.
- Only safe provider-null and synthetic Kanban behavior was exercised. Existing
  provider, OAuth, MCP, gateway, dispatcher, worker and agent surfaces were not
  run.
- Remote Docs and network-dependent hub/install flows were not loaded.
- Kanban's central source/data/API/UI behavior was sufficient for a reuse
  decision, but its known defects block unrestricted product write exposure.
- Current plugin integrity/lifecycle/slot behavior is incomplete and remains a
  third-party trust boundary.
- P12.4 known Python, type, lint, TUI, desktop, Windows shutdown and PTY debt is
  not reclassified.
- Product UI remains disabled; this record is architecture, not implementation
  or production evidence.

## Created / Modified / Generated / Removed / Not Created Register

Created durable tracked file:

```text
0_architecture/governance/agent_platform_hermes_ui_product_brief_information_architecture.md
```

Modified tracked files:

```text
none
```

Generated under the permitted ignored runtime root and removed after inspection:

```text
9_artifacts/hermes/p13.0/runtime/**
  isolated HOME/HERMES_HOME/APPDATA/LOCALAPPDATA/TEMP/shared-auth/browser roots
  synthetic update cache and dashboard token state
  dashboard PID/stdout/stderr
  local status/product/plugin response JSON
  synthetic p13-ui-audit Kanban board database and response JSON
```

Not created, modified, activated or retained:

```text
additional P13.0 Markdown or closure fragments
2_products/hermes-agent/** tracked or generated product outputs
4_external/sources/hermes-agent/**
.gitignore
P11 or P12 records
AGENT_PLATFORM_MODIFICATIONS.tsv
dependency manifests or lockfiles
product configuration, feature flags or extension modules
gateway, dispatcher, worker, agent, provider, OAuth or MCP state
real user Hermes state, credentials, cookies or browser profiles
candidate checkout or synchronization workspace
Graphify output
Git index, commit, ref, remote or push state
```

## Result Markers

```text
hermes_existing_ui_capability_audit_complete
hermes_application_shell_inventory_complete
hermes_route_inventory_complete
hermes_plugin_architecture_audited
hermes_kanban_capability_audit_complete
hermes_kanban_semantic_mapping_complete
hermes_kanban_reuse_decision_recorded
hermes_no_duplicate_work_control_ui_authorized
hermes_design_system_inventory_complete
hermes_ui_product_brief_ready
hermes_information_architecture_ready
hermes_route_architecture_ready
hermes_navigation_architecture_ready
hermes_ui_data_authority_map_ready
hermes_safe_settings_boundary_ready
hermes_product_ui_activation_plan_ready
hermes_remote_ui_inspection_path_confirmed
hermes_P13_downstream_handoffs_ready
hermes_P13_1_ready
no_product_ui_feature_activation
no_product_source_modification
no_provider_activation
no_worker_or_agent_execution
no_new_work_control_backend
no_git_mutation_by_agent
```

## Final Verdict

```yaml
P13_0_HermesUIProductBriefInformationArchitectureVerdict:
  P12_R_committed: true
  initial_repository_clean: true
  product_source_modified: false

  existing_capability_audit:
    application_shell_audited: true
    built_in_routes_audited: true
    plugin_architecture_audited: true
    kanban_audited: true
    kanban_swarm_and_worker_surfaces_audited: true
    design_system_audited: true
    code_docs_tests_runtime_drift_recorded: true

  reuse:
    all_target_surfaces_classified: true
    kanban_reuse_decision_recorded: true
    duplicate_task_backend_authorized: false
    duplicate_plugin_architecture_authorized: false
    duplicate_design_system_authorized: false
    replacement_without_evidence_count: 0

  product_brief:
    primary_user_defined: true
    jobs_to_be_done_defined: true
    product_principles_defined: true
    non_goals_defined: true

  information_architecture:
    canonical_vocabulary_defined: true
    data_authority_map_defined: true
    final_navigation_model_selected: true
    route_architecture_defined: true
    surface_responsibilities_defined: true
    UI_state_model_defined: true
    feature_activation_plan_defined: true

  boundaries:
    product_UI_enabled: false
    extension_modules_added: false
    provider_activation_performed: false
    worker_or_agent_execution_performed: false
    WorkPacket_execution_claimed: false
    Paperclip_integration_claimed: false
    GBrain_integration_claimed: false
    production_readiness_claimed: false

  remote_inspection:
    provider_null_UI_inspected: true
    isolated_HERMES_HOME_used: true
    loopback_only: true
    VS_Code_port_forwarding_supported: true
    real_user_state_used: false

  sequencing:
    P13_1_may_proceed: true
    P13_2_may_proceed: false
    P13_2_requires_P13_1_acceptance: true
    P14_execution_remains_blocked: true
    P15_provider_enablement_remains_unauthorized: true

  execution:
    network_operation_performed: false
    dependencies_installed: false
    product_files_modified: false
    git_mutated_by_agent: false

  final_verdict: hermes_ui_product_brief_information_architecture_ready_with_constraints
```

`network_operation_performed: false` means no external network operation. The
ticket-authorized loopback HTTP/WebSocket inspection was local-only.

Constraints are binding: P13 reuses existing Hermes capabilities wherever
structurally valid; Kanban is not permanent work-control authority; product UI
stays disabled; runtime/provider execution stays unavailable; Paperclip,
GBrain and WorkPacket authority remain future work.

## Human Commit Boundary

P13.0 did not stage, commit or push. After human acceptance, the commit must
contain only the canonical record.

```powershell
$Record = "0_architecture/governance/agent_platform_hermes_ui_product_brief_information_architecture.md"

git add -- $Record
git diff --cached --check
git diff --cached --stat
git commit -m "P13.0 - Define Hermes UI product brief and information architecture"
git push origin main
```

Never use `git add .`, `git add -A` or `git add -f`. Review the exact staged
path before committing; add, commit and push remain human actions.
