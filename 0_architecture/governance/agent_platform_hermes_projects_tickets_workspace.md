# P13.4 - Hermes Projects and Tickets Workspace

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.4 - Projects and Tickets Workspace |
| Date | 2026-07-15 |
| Status | Implemented and validation-ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_projects_tickets_workspace.md` |
| Accepted start commit | `96ab6bb222677a1a09c6bc0f84752865c7b4960e` |
| Accepted prerequisite | Committed P13.3 Hermes Runtime Overview |
| Git mutation by agent | Prohibited and not performed |

## Purpose

Record the bounded P13.4 implementation of three read-only product
presentations over existing Hermes Kanban data: Projects, Project Detail and
Ticket Detail. The implementation does not create another work-control plane.
Hermes Kanban remains a provisional source and future Paperclip remains the
canonical project, task, dependency, assignment, approval and work-control
authority.

The implementation compiles three additional first-party descriptors but does
not enable the product feature, select any extension module, register any
runtime product route or expose any Kanban mutation or execution control.

## Prerequisite Result

```yaml
P13_4_PrerequisiteStatus:
  branch: main
  accepted_head: 96ab6bb222677a1a09c6bc0f84752865c7b4960e
  origin_main: 96ab6bb222677a1a09c6bc0f84752865c7b4960e
  head_equals_origin_main: true
  start_commit_subject: P13.3 Implement Hermes Runtime Overview
  git_index_empty_at_start: true
  tracked_product_clean_at_start: true
  immutable_upstream_clean_at_start: true
  product_files_at_start: 6147
  modification_register_rows_at_start: 29
  modification_register_hash_mismatches_at_start: 0
  product_UI_feature_at_start: disabled
  extension_modules_at_start: []
  compiled_descriptors_at_start: 1
  resolved_descriptors_at_start: 0
  prerequisite_result: pass
```

A read-only `graphify query` was used for scoped navigation. No Graphify output
was regenerated or modified.

## Kanban Source Audit

### Existing Read Endpoints

The product client consumes only these existing authenticated plugin reads:

| Endpoint | Product use | Qualification |
| --- | --- | --- |
| `GET /api/plugins/kanban/boards?include_archived=false` | Project collection and exact-board preflight | No process-current fallback accepted |
| `GET /api/plugins/kanban/board?board={boardSlug}&include_archived=false` | One Project and its source Ticket summaries | Explicit validated board required by product client |
| `GET /api/plugins/kanban/tasks/{taskId}?board={boardSlug}` | One board-qualified Ticket and optional detail sections | Explicit validated board and task required |

The source `/board` and `/tasks/{taskId}` handlers allow an omitted board and
then resolve the process-current board. P13.4 never uses that behavior. A
Project or Ticket request first loads the board collection, requires the exact
slug to exist, then sends the explicit board parameter. A missing board or a
task `404` becomes `unavailable`; it does not select `current`, `default` or any
other board.

The source task response bundles task fields, links, comments, attachment
metadata, events, runs and computed diagnostics. The source also exposes
separate diagnostics, attachment, worker, log and mutation endpoints. P13.4
does not call them. In particular, `/workers/active` includes worker PIDs and
claim/runtime details that are outside this product contract.

### Source Scope Limitation

Hermes Kanban boards are shared source state rather than profile-scoped state.
P13.4 preserves the selected profile in product navigation and GET query
identity so every route/profile change resets the poller, but the current
Kanban plugin read handlers do not partition board content by that query
parameter. The UI labels profile-assignee values as source labels, not Agent or
assignment authority.

### Broad Fields Rejected

The source responses can contain more detail than the product needs. P13.4
drops or redacts:

```text
database and workspace paths
process IDs and worker claims
commands and command output
provider, model and credential detail
authorization values, tokens, secrets and OAuth state
raw payloads, stack traces and transport errors
run result, outcome, summary and failure detail
active-board/current-board authority
raw source dictionaries and unknown fields
```

## Safe Projection Contract

Every source response enters as `unknown`. `contract.ts` requires plain
dictionaries, bounded arrays, safe integers, bounded identifiers and bounded
plain text before returning deeply frozen product projections.

The immutable source marker on every projected object is:

```yaml
source_system: hermes-kanban
source_authority: provisional
future_authority: paperclip-control-plane
```

Board slugs, task IDs and profile names use closed character sets and length
bounds before they enter a path or query. Source status preserves one bounded
original label and maps known Hermes values to a visual enum; unknown values
map only to `other`. It does not infer platform workflow semantics.

Plain-text fields remove controls and redact bearer values, token/secret/key
assignments, local paths and traceback tails. Attachment projections retain
only safe filename, media type, byte size and timestamp metadata. Diagnostic
messages come from a product-owned allowlist or a generic fallback rather than
raw diagnostic text.

Optional Ticket sections fail independently as `ready`, `empty` or
`unavailable`:

```text
dependencies
comments
attachment metadata
events
Hermes run summaries
diagnostics
```

A malformed optional section cannot expose raw content and does not discard a
separately valid Ticket summary.

## Authority Boundary

The visible workspace repeatedly states these non-equivalences:

| Hermes source concept | P13.4 treatment |
| --- | --- |
| Board | Provisional Project presentation, not canonical Project authority |
| Task | Provisional Ticket presentation, not a WorkPacket |
| `ready` | May be dispatcher-eligible in Hermes; not executable here |
| `running` | Source state; not governed WorkPacket execution |
| `review` | Source state; not an ApprovalRequest |
| `blocked` | Source state; not a pending approval |
| `scheduled` | Source state; no wake timestamp inferred |
| Assignee | Profile source label; not Agent assignment authority |
| Tenant | Source label; not access control |
| Comment | Discussion or evidence candidate only |
| Attachment | Metadata only |
| Run | Source-labelled summary; not governed execution evidence |

Paperclip remains the future single canonical work-control authority. P13.4
does not implement Paperclip, map canonical WorkPackets or create dual-writable
state.

## Read-Only Boundary

`kanban-client.ts` imports the existing authenticated `fetchJSON<unknown>`
transport and defines GET URL construction only. No `method`, request body,
upload, WebSocket, mutation client or execution client exists in the module.

The visible controls are limited to:

```text
refresh
local text/status filtering
product navigation
source navigation
```

There is no create, edit, delete, drag, assign, reprioritize, link, unlink,
comment, attachment upload, board switch, status transition, dispatch, run,
retry, approval or worker control.

## Freshness and Identity Model

The workspace starts an immediate read and schedules the next read with
`setTimeout` only after the current request settles. The interval is ten
seconds and an in-flight guard prevents overlap. Manual refresh cancels a
pending timer but does not start concurrent work.

| Phase | Meaning |
| --- | --- |
| `loading` | No request has completed for the exact route/profile identity |
| `ready` | A validated non-empty projection is current |
| `empty` | A validated collection or board contains no source items |
| `stale` | Refresh failed after success; last safe projection retained |
| `error` | Initial transport failed; no raw error retained or rendered |
| `unavailable` | Exact source identity is missing or response is unsafe |

Route kind, board slug, task ID and selected profile form the poller identity.
Changing any part creates a fresh loading state and stops the previous poller.

## Product Surfaces

### Projects

Projects lists validated board summaries, task counts, source freshness and
local text/status filters. Each card retains its exact board slug and provides
read navigation only.

### Project Detail

Project Detail renders one exact board, groups Tickets by known Hermes source
status and displays the semantic disclaimers for execution-, approval- and
schedule-adjacent statuses.

### Ticket Detail

Ticket Detail renders one exact board-qualified task plus independently safe
optional sections. Long plain text wraps and remains escaped; attachment paths,
run detail and raw diagnostics never enter the view.

All three pages use real Nous UI primitives and the accepted P13.1
`--agent-platform-*` semantic token layer. They provide responsive layouts,
semantic headings, labels in addition to color and keyboard-native controls.

## Static Descriptors and Activation Boundary

The production catalog now compiles four reviewed descriptors in deterministic
order:

| ID | Route | Navigation |
| --- | --- | --- |
| `agent_platform.ui.overview` | `/agent-platform/overview` | Overview |
| `agent_platform.ui.projects` | `/agent-platform/projects` | Projects |
| `agent_platform.ui.project_detail` | `/agent-platform/projects/:boardSlug` | None |
| `agent_platform.ui.ticket_detail` | `/agent-platform/projects/:boardSlug/tickets/:taskId` | None |

All descriptors are first-party static imports owned by `AGENT_PLATFORM`, use
feature `agent_platform.product_ui` and remain subject to both explicit module
selection and feature-state resolution. `visibleWhenExperimental` does not
bypass those gates.

Committed configuration remains:

```yaml
feature_flags:
  agent_platform.product_ui: disabled
extension_modules: []
compiled_product_descriptors: 4
resolved_product_descriptors: 0
runtime_product_routes: 0
agent_platform_navigation_items: 0
```

No `App.tsx`, backend route, configuration default, manifest, package file,
lockfile or upstream-derived source file was modified.

## Implementation Path Set

Created product-owned files:

```text
2_products/hermes-agent/web/src/agent-platform/projects-tickets/contract.ts
2_products/hermes-agent/web/src/agent-platform/projects-tickets/kanban-client.ts
2_products/hermes-agent/web/src/agent-platform/projects-tickets/use-projects-workspace.ts
2_products/hermes-agent/web/src/agent-platform/projects-tickets/projects-page.tsx
2_products/hermes-agent/web/src/agent-platform/projects-tickets/project-detail-page.tsx
2_products/hermes-agent/web/src/agent-platform/projects-tickets/ticket-detail-page.tsx
2_products/hermes-agent/web/src/agent-platform/projects-tickets/descriptors.ts
2_products/hermes-agent/web/src/agent-platform/projects-tickets/index.ts
2_products/hermes-agent/web/src/agent-platform/projects-tickets/projects-tickets.test.tsx
```

Modified existing product-owned files:

```text
2_products/hermes-agent/web/src/agent-platform/extensions.ts
2_products/hermes-agent/web/src/agent-platform/extensions.test.ts
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

Created canonical governance record:

```text
0_architecture/governance/agent_platform_hermes_projects_tickets_workspace.md
```

The conditional P13.3 Runtime Overview test path was not modified because no
P13.4 change required it.

## Modification-Register Reconciliation

```yaml
rows: 38
columns: 18
duplicate_ids: 0
duplicate_paths: 0
missing_required_fields: 0
hash_mismatches: 0
P13_4_rows_added:
  - P13.4-001
  - P13.4-002
  - P13.4-003
  - P13.4-004
  - P13.4-005
  - P13.4-006
  - P13.4-007
  - P13.4-008
  - P13.4-009
cumulative_rows_updated:
  - P12.6-008
  - P12.6-010
```

The final candidate product inventory is 6,156 files: the 6,147-file accepted
baseline plus exactly nine authorized additions.

## Validation Results

| Lane | Result | Evidence |
| --- | --- | --- |
| Targeted dashboard tests | Pass | 5 files, 55 tests |
| Full dashboard tests | Pass | 12 files, 97 tests |
| TypeScript | Pass | `tsc -p . --noEmit` |
| Affected ESLint | Pass | P13.4 module and both extension files |
| Dashboard production build | Pass | 511 modules transformed |
| Windows-footgun scanner | Pass | 755 Python files, no findings |
| Register validation | Pass | 38 rows, 18 columns, zero duplicates, missing fields or hash mismatches |
| Human visual review | Pass with observations | Styled populated Projects and styled unavailable state accepted on port 5175 |

## Integrated Runtime Evidence

The isolated provider-null backend listened only on `127.0.0.1:9124` and used
a synthetic board under the temporary P13.4 runtime tree. No provider, gateway,
worker or agent was enabled or started.

Synthetic source identity:

```yaml
board: p13-4-projects-preview
tasks:
  - id: t_05a70783
    status: triage
  - id: t_491f0be6
    status: scheduled
  - id: t_6c15d3dd
    status: done
links: 1
comments: 1
runs: 0
ready_or_running_tasks: 0
active_workers: 0
```

| Request | Result |
| --- | --- |
| Authenticated board list | `200`; exact synthetic board present |
| Authenticated exact board detail | `200`; triage, scheduled and done counts each one |
| Authenticated exact task detail | `200`; safe source sections available |
| Wrong-board task lookup | `404`; no fallback |
| Board diagnostics | `200`; one source diagnostic in fixture |
| Active workers | `200`; count zero |
| Product configuration | `200`; product UI disabled and extension modules empty |
| Runtime status | `200`; gateway false, active agents zero, providers empty |
| Unauthenticated Kanban read | `401` |
| Headless backend root | Expected `404` |

No POST, PATCH, PUT, DELETE, upload, dispatch, worker, run, gateway, provider,
MCP, Chat or agent endpoint was invoked.

## Accepted Visual Evidence

The ignored preview imported the real P13.4 pages, Hermes `ThemeProvider`,
profile context, router, Nous UI, P13.1 semantic tokens and the real compiled
dashboard stylesheet. It did not change committed product configuration or
activate the production extension registry.

Human review accepted these separate states:

- a populated Projects response rendered with the Hermes visual system;
- after refresh, a styled `Hermes Kanban could not be reached` state rendered;
- the unavailable state explicitly preserved board isolation and rejected
  alternate-board, alternate-task and process-current fallback;
- background, application surface, typography, spacing, borders, cards,
  badges, buttons and status treatments were styled rather than browser
  defaults;
- P13.1 semantic tokens were visibly applied;
- source and provisional-authority labels were visible;
- no create, edit, delete, drag, assignment, status-transition or execution
  controls were visible.

The unavailable state is not recorded as a successful live Kanban response.
The populated state and integrated HTTP checks provide separate live-source
evidence. Remaining empty, detail, stale, unavailable-identity, long-content,
profile-preservation and control-absence behaviors are covered by component,
client and poller tests and source inspection; a second live checkpoint was not
requested after the explicit closure instruction.

## Cleanup Evidence

The exact P13.4 process roots were backend PID `1784` and final preview PID
`24664`. At closure both PIDs were absent, neither port was listening and no
surviving Node/Python/cmd process referenced the P13.4 artifact tree.

```yaml
backend_PID_1784: absent
preview_PID_24664: absent
port_9124: free
port_5175: free
P13_4_owned_processes: none
temporary_tree_9_artifacts_hermes_p13_4: absent
runtime_preview_fixture_stdout_stderr_residue: none
hermes_shared_link_type: Junction
hermes_shared_link_target: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent\apps\shared
```

No Chrome or unrelated browser process was terminated as part of closure.

## Security and Trust Boundaries

- All Kanban input remains untrusted until projected.
- Raw source responses and transport errors are not retained in React state.
- Exact board/task qualification prevents current-board fallback.
- Profile context is preserved but is not overstated as Kanban tenancy.
- Text remains escaped by React and receives additional secret/path redaction.
- Optional unsafe sections degrade independently rather than exposing raw data.
- Dynamic import paths, filesystem discovery, eval and runtime code loading were
  not added.
- Product configuration remains disabled and no descriptor resolves.
- Kanban writes and execution controls remain absent.
- Providers, gateway, workers, agents, MCP and Chat remain inactive.

## Source and Lockfile No-Drift Verification

```yaml
upstream_derived_source_changed: false
backend_changed: false
App_tsx_changed: false
product_configuration_changed: false
package_manifest_changed: false
lockfile_changed: false
dependency_install_performed: false
immutable_upstream_changed: false
P13_3_runtime_overview_test_changed: false
```

## Limitations

- Routes are compiled but intentionally unavailable under committed
  configuration.
- Hermes Kanban remains provisional shared source state and is not profile
  partitioned by the current read handlers.
- The workspace is read-only presentation, not a WorkControlPlanePort or
  Paperclip implementation.
- Source timestamps and statuses preserve Hermes semantics only.
- Attachment content, raw diagnostics, detailed runs, worker state and logs are
  intentionally excluded.
- Human visual acceptance covered populated Projects and the styled unavailable
  response; the broader state matrix is automated evidence, not additional
  human visual acceptance.

## Sequencing

P13.4 is ready for human source review and commit with constraints. Any future
route activation requires a separate authorized ticket that explicitly changes
both product feature state and selected extension modules. Any write,
dispatcher, worker, provider, execution or Paperclip integration requires its
own governance and runtime gates. P14 and P15 remain unauthorized by P13.4.

## Rollback Procedure

1. Remove the nine `web/src/agent-platform/projects-tickets/*` files.
2. Remove `PROJECTS_TICKETS_DESCRIPTORS` from the static extension registry.
3. Remove the P13.4 catalog and activation assertions from
   `extensions.test.ts`.
4. Remove register rows `P13.4-001` through `P13.4-009`.
5. Restore the prior content and hashes for cumulative rows `P12.6-008` and
   `P12.6-010`.
6. Remove this governance record.

No backend, configuration, dependency, lockfile, upstream or runtime-state
rollback is required.

## Result Markers

```text
hermes_P13_4_projects_tickets_workspace_implemented
hermes_P13_4_safe_kanban_projection_verified
hermes_P13_4_exact_board_task_identity_verified
hermes_P13_4_read_only_boundary_verified
hermes_P13_4_compiled_descriptor_count_4
hermes_P13_4_resolved_descriptor_count_0
hermes_P13_4_runtime_product_route_count_0
hermes_P13_4_provider_null_runtime_passed
hermes_P13_4_manual_visual_passed_with_observations
no_product_UI_feature_activation
no_extension_module_activation
no_kanban_mutation
no_gateway_lifecycle_action
no_provider_activation
no_worker_or_agent_execution
no_upstream_derived_source_modification
no_git_mutation_by_agent
```

## Final Verdict

```yaml
P13_4_HermesProjectsTicketsWorkspaceVerdict:
  accepted_start_commit: 96ab6bb222677a1a09c6bc0f84752865c7b4960e
  implementation:
    product_additions: 9
    existing_product_owned_source_files_modified: 2
    product_control_files_modified: 1
    governance_records_created: 1
    upstream_derived_source_files_modified: 0
    backend_files_modified: 0
    modification_register_rows: 38
    product_file_inventory: 6156
  activation:
    compiled_descriptor_count: 4
    resolved_descriptor_count: 0
    runtime_product_route_count: 0
    product_UI_enabled: false
    extension_modules: []
  validation:
    targeted_tests: 55_passed
    full_dashboard_tests: 97_passed
    typecheck: passed
    affected_lint: passed
    dashboard_build: passed_511_modules
    windows_footgun_scan: passed_755_files
    kanban_read_only_runtime: passed
    human_visual: passed_with_observations
    temporary_artifacts_removed: true
  execution:
    staged_by_agent: false
    committed_by_agent: false
    pushed_by_agent: false
  final_verdict: hermes_projects_tickets_workspace_ready_with_constraints
```

## Human Commit Boundary

The agent did not stage, commit or push. Human review must include the nine new
Projects/Tickets files, the two extension files, the modification register and
this canonical governance record. Temporary runtime and preview files must not
be included.
