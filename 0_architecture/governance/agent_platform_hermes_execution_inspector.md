# P13.6 - Hermes Execution Inspector

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.6 - Execution Inspector |
| Date | 2026-07-16 |
| Status | Validated and ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_execution_inspector.md` |
| Accepted start commit | `9e8306234e183c44d63eb52441e7075de83a0c73` |
| Accepted prerequisite | Committed P13.5 Approval Inbox |
| Reuse decision | `wrap_existing` |
| Git mutation by agent | Prohibited and not performed |

## Purpose

Record the bounded P13.6 implementation of a read-only Execution Inspector
and Execution Detail presentation. The implementation audits existing Hermes
run, event, session, cron, log and process surfaces, selects only exact
board/task-qualified Kanban run evidence for production use, and preserves the
source-local identity and limitations of every projected item.

P13.6 does not create a canonical execution, WorkPacket execution, durable
event ledger, global execution collection, run controller, scheduler, retry
engine, rollback engine or approval authority. It does not expose start, stop,
terminate, retry, rollback, approve, assign, reclaim, dispatch, worker, process
inspection or terminal actions.

## Dynamic Prerequisite Result

```yaml
P13_6_PrerequisiteStatus:
  branch: main
  accepted_head: 9e8306234e183c44d63eb52441e7075de83a0c73
  origin_main: 9e8306234e183c44d63eb52441e7075de83a0c73
  head_equals_origin_main: true
  start_commit_subject: P13.5 Implement Approval Inbox
  git_index_empty_at_start: true
  tracked_product_clean_at_start: true
  P13_5_governance_record_present: true
  P13_5_approval_inbox_committed: true
  product_tracked_files_at_start: 6164
  modification_register_rows_at_start: 46
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  compiled_product_descriptors_at_start: 6
  resolved_product_descriptors_at_start: 0
  registered_runtime_product_routes_at_start: 0
  agent_platform_navigation_items_at_start: 0
  product_UI_feature_at_start: disabled
  extension_modules_at_start: []
  locked_upstream_clean_at_start: true
  nested_product_git: false
  candidate_checkout_absent: true
  synchronization_workspace_absent: true
  prerequisite_result: pass
```

The six prerequisite descriptors were exactly:

```text
agent_platform.ui.overview
agent_platform.ui.projects
agent_platform.ui.project_detail
agent_platform.ui.ticket_detail
agent_platform.ui.approvals
agent_platform.ui.approval_detail
```

A read-only Graphify query was used for scoped navigation before source
inspection. Graphify output was not used as execution truth.

## Execution-Source Audit

### Areas Inspected

Current implementation and tests were inspected across:

```text
gateway/platforms/api_server.py
plugins/kanban/dashboard/plugin_api.py
hermes_cli/kanban_db.py
cron/scheduler.py
cron/jobs.py
hermes_state.py
hermes_cli/web_server.py
web/src/lib/api.ts
web/src/agent-platform/projects-tickets/**
sessions, messages, logs, files, tools, plugins, packages and ACP surfaces
```

Current endpoint behavior, persistence and identity were authoritative. UI
labels, task state, process recency and log text were not treated as execution
facts.

### Source Classification

| Source | Classification | Decision | Reason |
| --- | --- | --- | --- |
| Kanban task runs/events | `safe_nested_partial_source` after projection | Consume only with exact board and task qualifiers | Stable board-local run/event IDs and a real nested GET read exist; no global list or complete event retention exists |
| API-server `/v1/runs/{id}` | `safe_detail_only_process_local_source` | Do not consume | No collection read; state is process-memory/platform-local and events may contain raw reasoning/tool data |
| Cron job runs endpoint | `safe_nested_partial_session_evidence` | Do not consume | Rows are sessions selected by ID naming convention; no-agent and early failures are absent and no per-attempt outcome exists |
| General sessions/messages | `evidence_only` | Do not consume | Session recency, messages and `cron_complete` do not prove execution state or outcome |
| Logs/files/attachments | `sensitive_evidence_only` | Do not consume | No exact per-run identity; content and paths may be sensitive |
| PIDs/worker inspection/claims | `unsafe_for_execution_truth` | Do not consume | Volatile host/process data, PID reuse and coordination fields are not durable execution state |
| Task state/diagnostics alone | `insufficient_identity` | Do not consume as executions | Task status and derived diagnostics are not run identity or universal execution state |

There is no safe universal execution index. The production collection therefore
requires an exact Kanban `board + task` context. Execution Detail additionally
requires the exact source-local run ID. Missing or invalid qualification returns
unavailable; no process-current board, alternate board, API run, cron session,
general session, log or process fallback is attempted.

## Authority And Identity Model

Every projected run uses:

```yaml
source_type: hermes-kanban-task-run
source_system: hermes-kanban
source_authority: source-local-evidence
future_authority: P14/P17-governed-execution-event-adapter
identity: [board_slug, task_id, source_local_run_id]
source_profile: task_runs.profile or null
freshness_basis: adapter-fetch-time
retention: task/board lifetime; linked events may be pruned or absent
```

Identity rules:

- board, task and run IDs are validated before reads or navigation;
- board membership is preflighted through the existing P13.4 board list so a
  missing board cannot fall back to the Kanban process-current board;
- the task response ID and every projected run `task_id` must match the
  requested task;
- duplicate run IDs fail the collection closed;
- detail selects one exact source-local run ID and never selects a nearest,
  current or latest run;
- only events whose explicit `run_id` equals the selected run are projected;
- task-wide events with null run ID and events for other runs are not linked;
- duplicate linked event IDs make the event section unavailable;
- selected dashboard profile is request/navigation context only because
  Hermes Kanban deliberately uses a shared board root across profiles;
- historical `task_runs.profile` is the source profile fact and is never
  replaced by the selected dashboard profile or current task assignee.

The surface visibly states that source status and outcome are local values, a
Kanban run is not a governed WorkPacket execution, task state is not run state,
missing events do not prove inactivity and ordering is within one task source
only.

## Safe Projection

The run allowlist contains only:

```text
source identity and authority labels
board slug
task ID and a fixed source-task-title-withheld marker
source-local run ID
source profile or null
original bounded source status
original bounded source outcome or null
source start/end timestamps
adapter observation time and freshness basis
explicit retention limitation
```

The linked-event allowlist contains only source identity, exact event ID,
exact linked run ID, bounded source event kind, source profile, event timestamp,
adapter observation time and retention limitation.

The optional detail projection additionally permits:

```text
one fixed safe action category and two fixed validation summaries
one generic result-presence summary with all raw result detail excluded
one generic failure-presence summary with all raw failure detail excluded
task-level artifact ID, safe display filename, media type, size and timestamp
an explicit marker that artifact metadata is not attributed to the selected run
run-qualified diagnostic kind, severity, count and first/last timestamps
fixed or generic safe diagnostic wording; no source title, detail or action
```

Result, failure, artifact and diagnostic sections each fail independently as
ready, empty or unavailable. Their failure does not discard an otherwise valid
exact run projection.

The projection excludes:

```text
source task title and all raw result/failure narrative detail
run and event metadata/payloads
task body/result/failure text and comments
attachment content, storage references and paths
logs and log paths
workspace, repository, database and attachment paths
claim locks and idempotency/session correlation fields
worker PIDs, command lines, heartbeat/process inspection and host metrics
provider/model/tool/credential/environment detail
diagnostic source titles/details, actions and command payloads
raw response dictionaries and unknown fields
```

The authenticated Kanban task endpoint remains broader than this frontend
allowlist, as it already is for the accepted P13.4 workspace. P13.6 immediately
projects the response and stores/renders only the bounded contract, but browser
network tooling can still observe the authenticated raw response. A future
backend safe DTO requires separate authorization and is not invented here.

Kanban GET handlers may initialize or migrate their source database. P13.6 is
GET-only at the HTTP contract and performs no execution mutation, but it does
not claim the underlying source reads are filesystem-pure.

## Client And Freshness Behavior

The client:

- reuses the existing authenticated `fetchJSON` transport and the exact P13.4
  Kanban endpoint shapes;
- validates detail run IDs before any source request;
- preflights exact board membership;
- performs only the board list GET and exact board-qualified task-detail GET;
- catches only source 404 as unavailable and retains no raw transport error;
- exposes no API-server, cron, session, log, WebSocket or process client;
- preserves board/task/profile query context in list, detail and failed-detail
  back navigation.

Polling is immediate and recursively scheduled at ten seconds. It prevents
overlap, applies a 15-second request timeout, propagates one abort signal through
board preflight and task detail, aborts on stop/unmount/identity replacement,
suppresses late responses after stop, resets on profile/board/task/run identity
changes, retains only the last safe projection as stale after a failed refresh
and never stores raw source responses or errors. Local filters are also qualified
by profile/board/task identity and cannot hide a newly selected source with stale
prior filters.

## Read-Only Surfaces

### Execution Inspector

`/agent-platform/executions` requires `board` and `task` query qualifiers to
show a collection. It presents:

- exact source board/task IDs, fixed task-title-withheld posture and record count;
- audited posture cards for the qualified Kanban source, rejected process-local
  API-run source and evidence-only cron-session source;
- local text and source-status filters;
- source run ID, source profile, source status/outcome and timestamps;
- profile-preserving, board/task-qualified detail navigation;
- explicit loading, ready, empty, stale, error and unavailable states;
- a truthful unavailable state when no qualified source exists.

### Execution Detail

`/agent-platform/executions/:executionId` requires the same board/task
qualifiers. It presents:

- exact board/task/run identity;
- source profile, source status/outcome and timing;
- retention and raw-field exclusion notes;
- fixed safe action category and validation summaries;
- independently ready, empty or unavailable explicitly linked event evidence;
- independently ready, empty or unavailable generic result/failure-presence,
  task-level artifact-reference and run-qualified diagnostic sections;
- preserved board/task context when detail loading fails;
- explicit absence of execution and approval controls.

Both pages use existing Nous UI, P13.1 semantic tokens and the P13.2 product
shell contract. Neither page registers unless configuration later selects its
descriptor and enables the product UI feature.

## Descriptor And Activation Result

The static registry now compiles exactly eight reviewed descriptors in order:

```text
agent_platform.ui.overview
agent_platform.ui.projects
agent_platform.ui.project_detail
agent_platform.ui.ticket_detail
agent_platform.ui.approvals
agent_platform.ui.approval_detail
agent_platform.ui.executions
agent_platform.ui.execution_detail
```

Only `agent_platform.ui.executions` owns navigation. Execution Detail is
contextual. Both use `agent_platform.product_ui`, are statically imported,
remain absent from `extension_modules` and resolve to no runtime route or
navigation item under committed configuration.

```yaml
P13_6_ActivationStatus:
  compiled_descriptors: 8
  selected_descriptors: 0
  resolved_descriptors: 0
  product_routes_registered: 0
  product_navigation_items: 0
  product_UI_feature: disabled
  extension_modules: []
```

## Files Created And Updated

Created:

```text
web/src/agent-platform/execution-inspector/contract.ts
web/src/agent-platform/execution-inspector/execution-client.ts
web/src/agent-platform/execution-inspector/use-execution-inspector.ts
web/src/agent-platform/execution-inspector/execution-inspector-page.tsx
web/src/agent-platform/execution-inspector/execution-detail-page.tsx
web/src/agent-platform/execution-inspector/descriptors.ts
web/src/agent-platform/execution-inspector/index.ts
web/src/agent-platform/execution-inspector/execution-inspector.test.tsx
```

Updated:

```text
web/src/agent-platform/extensions.ts
web/src/agent-platform/extensions.test.ts
AGENT_PLATFORM_MODIFICATIONS.tsv
```

No backend, product configuration, App shell, dependency, package manifest,
lockfile, upstream source, session, cron, log or runtime-state file was changed.

## Modification Register

```yaml
P13_6_register_result:
  rows_before: 46
  rows_after: 54
  columns: 18
  rows_added:
    - P13.6-001
    - P13.6-002
    - P13.6-003
    - P13.6-004
    - P13.6-005
    - P13.6-006
    - P13.6-007
    - P13.6-008
  cumulative_rows_updated:
    - P12.6-008
    - P12.6-010
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  hash_mismatches: 0
```

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Focused P13.6/catalog tests | Pass | 2 files, 39 tests |
| Exact P13 regression lane | Pass | 7 files, 110 tests |
| Full dashboard tests | Pass | 14 files, 152 tests |
| TypeScript | Pass | `tsc -p . --noEmit` |
| Affected ESLint | Pass | Execution Inspector module and both extension files |
| Production build | Pass | 527 modules transformed |
| Windows-footgun scanner | Pass | Existing product `.venv`; 755 Python files |
| Independent boundary review | Pass | No remaining actionable identity, leakage, fallback, polling or route defects; residual hook-level identity-switch test gap documented below |
| Git whitespace check | Pass | `git diff --check`; line-ending warnings only |
| Register integrity | Pass | 54 rows, 18 columns, zero duplicates, missing fields or hash mismatches |

The production build emitted only the inherited large-chunk warning.

## Runtime And Visual Posture

A bounded headless dashboard backend was started on `127.0.0.1:9126` for
provider-null and activation checks. `/api/status` returned HTTP 200 with the
gateway disabled, zero agents, sessions and workers, and no providers. Product
configuration remained disabled with `extension_modules: []`; all eight static
descriptors compiled while zero product descriptors, routes or navigation items
resolved. Global run and missing board/task/run reads returned 404 and no
alternate execution source was selected. No provider, gateway, worker, agent,
tool, run, cron job, API-server platform or Kanban dispatcher was started.

Because committed configuration correctly leaves the product routes inert, an
ignored Vite preview on `127.0.0.1:5177` rendered the real page components,
contracts, client and polling hooks against synthetic source fixtures. Preview
stderr was empty and the root, source modules, Vite client, dashboard CSS and
P13.1 token CSS all returned HTTP 200 with correct CSS media types.

The bounded Chrome DevTools matrix passed 15 page states and routes, including
populated, empty, stale, error, unavailable, missing-identity, long-content,
mobile, alternate-theme and real-page loader paths. It confirmed:

```yaml
required_content_missing: 0
preview_error_boundary: false
vite_overlay: false
runtime_exceptions: 0
browser_page_errors: 0
prohibited_controls_found: 0
raw_source_leaks_found: 0
profile_preserving_navigation: true
keyboard_focus_visible: true
mobile_viewport: 390x844
Hermes_Teal_background: "#041c1c"
Nous_Blue_background: "#E8F2FD"
themes_differ: true
P13_1_semantic_variables_nonempty: true
```

Chrome stderr contained only host USB discovery and disabled Google messaging
endpoint/quota diagnostics; there were no page console errors. Human visual
acceptance was completed for the populated Hermes Teal desktop collection with
its source classifications and authority boundaries. No real run, event, log,
session, attachment, credential or user mutation was used.

The subsequent independent boundary review tightened the final projection by
withholding source task titles and both source narratives, distinguishing omitted
optional evidence from explicit emptiness, and adding transport abort/timeout
behavior. These changes removed content and added no layout or control; final
server-rendering tests cover the changed markup and the browser matrix remains
the bounded layout, theme, focus and control-absence evidence.

Cleanup terminated only the owned browser and preview trees. The backend had
already exited before cleanup. Owned PIDs were absent, ports `5177`, `56385`
and `9126` had no listeners, and the ignored `9_artifacts/hermes/p13.6` tree
was removed.

## Source And Lockfile No-Drift

```yaml
backend_files_modified: 0
App_tsx_modified: false
product_configuration_modified: false
package_manifest_modified: false
dependency_lockfile_modified: false
dependency_install_performed: false
immutable_upstream_modified: false
runtime_overview_modified: false
projects_tickets_modified: false
approval_inbox_modified: false
product_provider_enabled: false
headless_dashboard_backend_started: true
synthetic_preview_started: true
headless_browser_started: true
gateway_started: false
worker_started: false
agent_started: false
run_started: false
tool_or_execution_control_exposed: false
owned_runtime_cleanup_passed: true
temporary_artifact_tree_removed: true
graphify_candidate_changes: 0
```

## Limitations

- There is no global execution list; collection availability requires an exact
  existing board and task.
- Kanban runs are source-local attempts, not governed WorkPacket executions.
- Board/task/run identity is board-store-local and not globally canonical.
- Selected profile is presentation/request context because Kanban storage is
  shared; the run's persisted profile is the historical source fact.
- The authenticated source response is broader than the frontend projection.
- Kanban GET reads may initialize or migrate source storage.
- Runs disappear with hard task/board deletion; event GC can prune linked
  history and historical events may have null run attribution.
- The task response is not a transactionally consistent multi-source snapshot.
- Source task titles and raw result/failure narratives are intentionally withheld;
  only their fixed posture/presence labels are shown.
- No per-run log is available; task logs, process inspection and raw diagnostic
  detail/actions are deliberately excluded. Only run-qualified bounded
  diagnostic identity/count/timing with safe wording is displayed.
- API-server runs remain process-local and have no collection read.
- Cron sessions omit valid scheduler outcomes and have no per-attempt outcome.
- P14/P17 remains the future durable execution/event authority.
- P13.8 retains broader accessibility and visual-regression ownership beyond
  this bounded P13.6 browser matrix.
- Cancellation is covered at the poller and authenticated transport seam, but a
  full React hook identity-switch integration test remains future coverage.

## Rollback Procedure

1. Remove the eight `web/src/agent-platform/execution-inspector/*` files.
2. Remove `EXECUTION_INSPECTOR_DESCRIPTORS` from the static extension registry.
3. Remove the P13.6 catalog assertions from `extensions.test.ts`.
4. Remove register rows `P13.6-001` through `P13.6-008`.
5. Restore prior cumulative content and hashes for `P12.6-008` and
   `P12.6-010`.
6. Remove this governance record.

No backend, configuration, dependency, lockfile, upstream or runtime-state
rollback is required.

## Sequencing And Handoff

- P13.7 may proceed only after human acceptance and commit of P13.6.
- P13.8 remains the later frontend quality consolidation ticket.
- P14/P17 remains responsible for future durable execution/event authority.
- Any global list, backend safe DTO, event stream or execution action requires
  separate identity, authorization, persistence, retention, audit and human
  approval governance.
- P15 provider enablement remains unauthorized.

## Result Markers

```text
hermes_P13_6_prerequisite_gate_passed
hermes_P13_6_dynamic_start_SHA_accepted
hermes_execution_sources_audited
hermes_false_execution_sources_rejected
hermes_execution_source_classified_safe_nested_partial
hermes_execution_safe_projection_created
hermes_execution_composite_ID_preserved
hermes_execution_source_profile_preserved
hermes_execution_freshness_and_retention_visible
hermes_execution_sensitive_fields_excluded_from_projection
hermes_execution_inspector_read_only
hermes_execution_inspector_page_created
hermes_execution_detail_page_created
hermes_execution_descriptors_compiled
hermes_execution_descriptors_not_selected
hermes_execution_routes_not_registered
hermes_product_UI_feature_remains_disabled
hermes_extension_modules_remain_empty
hermes_P13_6_targeted_tests_passed
hermes_P13_6_full_dashboard_tests_passed
hermes_P13_6_typecheck_passed
hermes_P13_6_affected_lint_passed
hermes_P13_6_production_build_passed
hermes_P13_6_windows_footgun_scan_passed
hermes_P13_6_boundary_review_passed
hermes_P13_6_provider_null_runtime_passed
hermes_P13_6_bounded_browser_matrix_passed
hermes_P13_6_human_visual_checkpoint_accepted
hermes_P13_6_owned_runtime_cleanup_passed
hermes_execution_inspector_ready_with_constraints
no_global_execution_index_invented
no_universal_execution_status_inferred
no_WorkPacket_execution_equivalence
no_api_run_or_cron_session_fallback
no_execution_mutation_or_control
no_backend_modification
no_product_configuration_activation
no_dependency_or_lockfile_change
no_execution_or_user_mutation_started
```
