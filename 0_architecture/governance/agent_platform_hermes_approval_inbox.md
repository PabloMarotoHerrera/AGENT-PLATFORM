# P13.5 - Hermes Approval Inbox

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.5 - Approval Inbox |
| Date | 2026-07-15 |
| Status | Implemented and validation-ready with constraints |
| Canonical output | `0_architecture/governance/agent_platform_hermes_approval_inbox.md` |
| Accepted start commit | `ba36431efa0c2396695db1317a5e66edfd5310d0` |
| Accepted prerequisite | Committed P13.4 Projects and Tickets workspace |
| Reuse decision | `wrap_existing` |
| Git mutation by agent | Prohibited and not performed |

## Purpose

Record the bounded P13.5 implementation of a read-only Approval Inbox and
Approval Detail presentation. The ticket audits current Hermes approval and
confirmation behavior, preserves only source-qualified facts, and explicitly
declines to invent an approval backend when no safe authenticated dashboard
list/detail boundary exists.

P13.5 does not create a canonical `ApprovalRequest`, approval database,
decision runtime, WorkPacket approval engine, Paperclip approval authority,
provider approval system or tool-execution approval system. It does not expose
approve, reject, confirm, deny, cancel, retry, execution or policy mutations.

## Dynamic Prerequisite Result

```yaml
P13_5_PrerequisiteStatus:
  branch: main
  accepted_head: ba36431efa0c2396695db1317a5e66edfd5310d0
  origin_main: ba36431efa0c2396695db1317a5e66edfd5310d0
  head_equals_origin_main: true
  start_commit_subject: P13.4 Implement Projects and Tickets workspace
  git_index_empty_at_start: true
  tracked_product_clean_at_start: true
  P13_4_governance_record_present: true
  P13_4_projects_tickets_workspace_committed: true
  product_tracked_files_at_start: 6156
  modification_register_rows_at_start: 38
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  compiled_product_descriptors_at_start: 4
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

The four prerequisite descriptors were exactly:

```text
agent_platform.ui.overview
agent_platform.ui.projects
agent_platform.ui.project_detail
agent_platform.ui.ticket_detail
```

A read-only Graphify query was used for scoped navigation. Graphify output was
not regenerated or modified.

## Approval-Source Audit

### Areas Inspected

Current implementation and tests were searched across:

```text
web/src/**
hermes_cli/**
gateway/**
tools/**
plugins/**
packages/**
apps/shared/**
acp_adapter/**
agent/transports/**
tests/**
```

Search terms included approval, approve, reject, deny, allow, confirmation,
confirm, permission request, pending decision, human decision, requires
approval and requires confirmation. Current implementation behavior, storage
and endpoint registration were authoritative; UI labels and documentation
alone were not treated as source evidence.

### Eligible Underlying Source

The only durable source family with genuine explicit human decision semantics
and stable source-local pending IDs is the staged memory/skill write store:

| Property | Evidence and result |
| --- | --- |
| Source identity | `tools.write_approval`; subsystems `memory` and `skills` |
| Genuine semantics | Explicitly stages a write until an operator applies or rejects it |
| Source-local ID | Eight lowercase hexadecimal UUID prefix, persisted as `id` |
| Durability | Profile-local JSON under `HERMES_HOME/pending/{memory,skills}` |
| Python list read | `list_pending(subsystem)` |
| Python detail read | `get_pending(subsystem, pending_id)` |
| Source fields | ID, subsystem, action, summary, origin, creation time and raw replay payload |
| Decision behavior | Apply or reject deletes the pending record |
| Historical decisions | None; no tombstone or decision ledger |
| Expiry | None |
| Ownership | Profile-local store, not request/session/actor-qualified |
| Default state | Write-approval gate disabled unless explicitly enabled |
| HTTP list/detail | None |

The raw record is not a safe frontend contract. Memory payloads may contain
private content, and skill payloads may contain complete files, patches and
paths. List/detail Python methods return raw dictionaries, have no pagination,
and are not exposed through a safe authenticated dashboard route. P13.5 did not
add such a route because backend modification is unauthorized.

### Genuine but Transient Sources

Hermes has real interactive approvals for dangerous commands, `execute_code`,
plugin tool escalation, MCP elicitation, ACP/Codex execution and file changes,
gateway slash confirmations and Console commands. These sources are not safe
Inbox records:

| Source | Why not consumed |
| --- | --- |
| Runtime tool approval queue | In-memory, session-keyed FIFO entries without request IDs or list/detail reads |
| API run approval | `run_id` identifies the agent run, not an individual approval; approval resolution is POST-only |
| MCP elicitation | Transient per call; no stable request history; may contain sensitive form schemas |
| ACP/Codex permission requests | Transport-local IDs, raw commands/files, no durable list/history |
| Slash confirmations | Process-local, expiring and non-listable |
| Safe Console confirmation | One raw command per WebSocket; no durable cross-connection read |

The API-run surface is:

```text
POST /v1/runs
GET  /v1/runs/{run_id}
GET  /v1/runs/{run_id}/events
POST /v1/runs/{run_id}/approval
POST /v1/runs/{run_id}/stop
```

There is no run collection read, approval collection read, approval detail
read or approval-local identity. Starting a run would execute an agent and was
therefore prohibited. The SSE stream can contain reasoning and tool lifecycle
data and is not a bounded approval read.

### Rejected False Sources

P13.5 explicitly rejects:

```text
Hermes Kanban review, blocked and ready states
Kanban comments, runs and diagnostics
worker claims and heartbeats
provider login and provider authentication state
OAuth and API authentication state
Chat messages and transport buttons
gateway busy state
generic warnings and logs
filesystem and terminal prompts without durable approval identity
client-only browser confirmation dialogs
shell-hook allowlists and other current grants without pending request identity
```

Messaging pairing was also not projected. It is an explicit access-grant flow,
but its dashboard pending list does not expose the internal entry ID, labels a
salted-hash prefix as a code, has no approval detail read or decision history,
and is not management-profile scoped. It cannot satisfy the exact stable
source-local approval identity contract safely.

### Audit Classification

```yaml
approval_source_classification: safe_partial_read_source
eligible_underlying_source: hermes-write-approval
durable_python_list_read: true
durable_python_detail_read: true
safe_authenticated_dashboard_list_read: false
safe_authenticated_dashboard_detail_read: false
production_frontend_availability: unavailable
```

`safe_partial_read_source` records that a genuine durable source exists in the
current product. It does not claim the source is safe for browser consumption.
Because the required HTTP boundary is absent, the production adapter returns
unavailable without network access. No fake endpoint, log scraper, terminal
reader or fallback source was created.

## Authority Model

Every projected fixture object uses:

```yaml
source_system: hermes-write-approval
source_authority: provisional
canonical_approval_authority: not_yet_established
```

The surface visibly preserves these distinctions:

| Source fact | P13.5 boundary |
| --- | --- |
| Approval presentation | Not a canonical `ApprovalRequest` |
| Source-local ID | Preserved exactly; no replacement canonical ID generated |
| Pending in source | Not governed AGENT PLATFORM pending approval |
| Approved/rejected in source | Not a governed AGENT PLATFORM decision |
| Source requester | Not governed Agent identity |
| Source target | Not a WorkPacket |
| Source risk label | Not AGENT PLATFORM risk assessment |
| Source evidence | Not canonical `EvidenceRef` |
| Source decision history | Not canonical audit log |

No current canonical approval authority is claimed. Future authority remains
reserved for separately governed P14, P17 and later work-control integration.
Paperclip is not described as the current approval authority.

## Safe Projection Contract

All external fixture input enters `contract.ts` as `unknown`. Projection
requires a plain source envelope, exact audited source system, explicit
approval/confirmation/permission semantics, bounded arrays, validated IDs,
bounded plain text and finite non-negative timestamps.

Eligible semantics are closed to:

```text
explicit_approval_request
explicit_confirmation_request
explicit_permission_decision_request
explicit_allow_deny_decision_record
```

Known source statuses map visually to pending, approved, rejected, expired and
cancelled. The original bounded source status is always retained. Unknown
values map only to `other`; text, colors, timestamps, worker state and gateway
state never infer status.

Required projections include exact source-local ID, title, summary, original
source status/type, request category/time, optional expiry/requester/risk,
closed safe target type and safe target label. Detail optionally projects safe
reason, evidence labels with opaque source-local IDs and historical source
decision summaries.

Evidence and decision-history sections independently resolve to `ready`,
`empty` or `unavailable`. Malformed optional sections expose no raw data and do
not discard a separately valid approval summary. Returned objects and arrays
are deeply frozen and retain no raw source references.

## Sensitive-Data Exclusion

The projection does not retain or render:

```text
commands, shell text, tool arguments or spawn arguments
filesystem, workspace or worktree paths
process IDs, ports, worker claims or heartbeat data
provider or model identifiers
credentials, API keys, tokens, OAuth state, authorization or cookies
arbitrary URLs
raw request, tool, result or response payloads
stack traces and raw errors
gateway topology
unknown executable fields or raw dictionaries
```

Safe target type is closed to tool, filesystem, network, configuration,
runtime or other source action. It never retains the executable action itself.
React renders all source text as escaped plain text; no source HTML, Markdown
renderer or arbitrary URL fetch exists.

## Read-Only Client Boundary

The audited source has no safe dashboard API. `approval-client.ts` therefore
implements a product-owned unavailable adapter rather than a second HTTP
client or invented endpoint. Production `listApprovals` and `getApproval`
return unavailable after semantic profile/ID validation and make no network
request.

Tests prove the module contains no API endpoint, direct `fetch`, POST, PUT,
PATCH, DELETE or decision operation. It never calls an approve, reject,
confirm, deny, cancel, retry, execution, provider, worker or gateway mutation.

The client still provides validated profile-preserving product paths. IDs are
validated before `encodeURIComponent`; path traversal, absolute paths,
controls, separators and overlong values are rejected.

## Data-State and Freshness Model

| Phase | Meaning |
| --- | --- |
| `loading` | No source-qualified result for the current route/profile identity |
| `ready` | A validated non-empty projection is current |
| `empty` | A safe source response contains no approval presentations |
| `stale` | Refresh failed after success; last safe projection retained |
| `error` | Initial transport failed; raw error not retained or rendered |
| `unavailable` | No safe live source, unsafe response or exact identity unavailable |

Polling starts immediately and uses recursive `setTimeout` ten seconds after a
request settles. An in-flight guard prevents overlap. Manual refresh cancels a
pending timer but never starts concurrent work. Stop suppresses late responses
and clears timers.

Profile, route kind and approval ID form the request identity. Any change stops
the previous poller, resets visible route state and performs a fresh load.
Profile query identity is not described as backend tenancy because the audited
source has no dashboard endpoint proving that behavior.

## Product Surfaces

### Approval Inbox

The Inbox renders source label, provisional authority, inactive canonical
authority, selected profile, freshness, source pending/historical counts,
source-local ID, safe title/status/type/target/timestamps, local text/status/type
filters and profile-preserving detail links.

Allowed controls are refresh, local filtering and navigation. Filter state is
not persisted to a source.

### Approval Detail

Detail renders one exact source-local identity with safe summary, request
metadata, target metadata, reason, evidence summaries, source decision history
and authority limitations. It explicitly states:

```text
No approval or rejection action is available in P13.5.
```

No approve, reject, allow, deny, confirm, cancel, retry, execute, terminal,
payload, assignment, escalation or policy control exists.

## Descriptor and Activation Boundary

The static catalog now contains six descriptors in deterministic order:

| ID | Route | Navigation |
| --- | --- | --- |
| `agent_platform.ui.overview` | `/agent-platform/overview` | Overview |
| `agent_platform.ui.projects` | `/agent-platform/projects` | Projects |
| `agent_platform.ui.project_detail` | `/agent-platform/projects/:boardSlug` | None |
| `agent_platform.ui.ticket_detail` | `/agent-platform/projects/:boardSlug/tickets/:taskId` | None |
| `agent_platform.ui.approvals` | `/agent-platform/approvals` | Approvals |
| `agent_platform.ui.approval_detail` | `/agent-platform/approvals/:approvalId` | None |

All are static first-party imports owned by `AGENT_PLATFORM`, use feature
`agent_platform.product_ui`, and remain subject to explicit module selection
plus feature-state resolution. `visibleWhenExperimental` does not bypass those
gates.

Committed configuration remains:

```yaml
agent_platform.product_ui: disabled
extension_modules: []
compiled_product_descriptors: 6
resolved_product_descriptors: 0
registered_runtime_product_routes: 0
agent_platform_navigation_items: 0
```

No `App.tsx`, backend, product configuration, package manifest, dependency
lockfile or upstream-derived source file was modified.

## Implementation Path Set

Created product files:

```text
2_products/hermes-agent/web/src/agent-platform/approval-inbox/contract.ts
2_products/hermes-agent/web/src/agent-platform/approval-inbox/approval-client.ts
2_products/hermes-agent/web/src/agent-platform/approval-inbox/use-approval-inbox.ts
2_products/hermes-agent/web/src/agent-platform/approval-inbox/approval-inbox-page.tsx
2_products/hermes-agent/web/src/agent-platform/approval-inbox/approval-detail-page.tsx
2_products/hermes-agent/web/src/agent-platform/approval-inbox/descriptors.ts
2_products/hermes-agent/web/src/agent-platform/approval-inbox/index.ts
2_products/hermes-agent/web/src/agent-platform/approval-inbox/approval-inbox.test.tsx
```

Modified existing product-owned files:

```text
2_products/hermes-agent/web/src/agent-platform/extensions.ts
2_products/hermes-agent/web/src/agent-platform/extensions.test.ts
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

Created canonical governance record:

```text
0_architecture/governance/agent_platform_hermes_approval_inbox.md
```

Neither conditional global-catalog test was modified because neither asserted
global catalog cardinality.

## Count and Register Reconciliation

```yaml
initial_product_files: 6156
new_product_files: 8
final_product_files: 6164
register_rows: 46
register_columns: 18
duplicate_ids: 0
duplicate_paths: 0
missing_required_fields: 0
current_hash_mismatches: 0
P13_5_rows_added:
  - P13.5-001
  - P13.5-002
  - P13.5-003
  - P13.5-004
  - P13.5-005
  - P13.5-006
  - P13.5-007
  - P13.5-008
cumulative_rows_updated:
  - P12.6-008
  - P12.6-010
```

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Focused dashboard tests | Pass | 6 files, 79 tests |
| Full dashboard tests | Pass | 13 files, 121 tests |
| TypeScript | Pass | `tsc -p . --noEmit` |
| Affected ESLint | Pass | Approval Inbox module and both extension files |
| Production build | Pass | 520 modules transformed |
| Windows-footgun scanner | Pass | Existing product `.venv`; 755 Python files |
| Git whitespace check | Pass | `git diff --check` |
| Register integrity | Pass | 46 rows, 18 columns, zero duplicates, missing fields or mismatches |

The production build emitted only the inherited large-chunk warning.

## Provider-Null Integrated Runtime

The isolated headless FastAPI backend listened only on `127.0.0.1:9125` with
`HERMES_HOME` under `9_artifacts/hermes/p13.5/runtime`. The launch root was PID
`3984`; the existing Windows environment launcher created child listener PID
`27408` and console host PID `19088`.

| Check | Result |
| --- | --- |
| `GET /api/status` | `200` |
| Loopback unauthenticated status | `200`; current public loopback status behavior |
| Product configuration | `200`; UI disabled and extension modules empty |
| Headless root | Expected `404` headless-backend message |
| Gateway | False |
| Active agents | 0 |
| Active sessions | 0 |
| Auth providers | Empty |
| Live approval source | `safe_partial_read_source`, production frontend unavailable |

No live approval endpoint was called because none exists. No Kanban, Chat,
log, provider, OAuth, worker or transient queue fallback was attempted. No
approval record was created, no run was started, and no decision/mutation
endpoint was called.

## Visual Preview Evidence

The ignored preview on `127.0.0.1:5176` used:

```text
real ApprovalInboxPage and ApprovalDetailPage
real contract, client and polling hook boundaries
real BrowserRouter and ProfileContext behavior
real Hermes ThemeProvider
real Nous UI
real compiled dashboard stylesheet
real P13.1 semantic tokens
preview-only bounded source fixtures
```

It did not activate production routes or configuration and did not copy product
page implementation.

Human review accepted the populated/mixed Hermes Teal desktop Inbox with a
pending source item and historical source item. Accepted evidence included
Hermes styling, clear hierarchy, source-local metadata, visible provisional and
inactive-authority language, and absence of every decision/execution control.
Fixture records are not live production requests or governed decisions.

Bounded headless browser verification covered:

```text
Inbox empty
Inbox stale after retained success
Inbox initial error
Inbox production source unavailable
Approval Detail populated
Detail optional sections empty
Detail optional sections unavailable
missing approval ID
long bounded safe content
mobile responsive breakpoint
Nous Blue
keyboard focus with a visible 2px focus outline
profile-preserving navigation
```

All 13 technical renders had a false preview error-boundary flag, non-empty
Hermes semantic variables, styled control padding and borders, usable
dimensions and empty Chrome stderr. Root, main module, Vite client and both CSS
`?direct` assets returned `200`; CSS content type was `text/css`. Vite stderr
was empty.

## Process Ownership and Cleanup

```yaml
backend_root_PID: 3984
backend_listener_PID: 27408
backend_console_PID: 19088
preview_root_and_listener_PID: 5064
preview_console_PID: 22436
headless_browser_processes: bounded_and_exited
port_9125_after_cleanup: free
port_5176_after_cleanup: free
P13_5_owned_processes_after_cleanup: none
temporary_tree_9_artifacts_hermes_p13_5: absent
```

Preview PID `5064` had already exited before the exact cleanup call and was not
restarted. Backend PID `3984` was terminated with its exact child tree. No
unrelated browser or process was terminated.

The shared package link was not replaced:

```yaml
link: 2_products/hermes-agent/node_modules/@hermes/shared
type: Junction
target: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent\apps\shared
```

## Source and Lockfile No-Drift

```yaml
backend_files_modified: 0
App_tsx_modified: false
product_configuration_modified: false
package_manifest_modified: false
dependency_lockfile_modified: false
dependency_install_performed: false
immutable_upstream_modified: false
runtime_overview_test_modified: false
projects_tickets_test_modified: false
product_provider_enabled: false
gateway_started: false
worker_started: false
agent_started: false
tool_executed: false
```

## Limitations

- The production Approval Inbox truthfully renders unavailable because no safe
  authenticated approval list/detail HTTP boundary exists.
- The underlying staged-write source is durable but defaults disabled, exposes
  raw payloads internally, lacks expiry/ownership/pagination and deletes records
  on resolution without durable decision history.
- Transient runtime approvals lack approval-local IDs, list/detail reads and
  durable history.
- No approval decision can be submitted from P13.5.
- Source decisions are provisional source facts only.
- Canonical approval authority is not active.
- Profile query identity is a UI/load identity, not proven backend tenancy.
- P13.8 retains full browser and accessibility ownership beyond this bounded
  responsive and focus evidence.

## Rollback Procedure

1. Remove the eight `web/src/agent-platform/approval-inbox/*` files.
2. Remove `APPROVAL_INBOX_DESCRIPTORS` from the static extension registry.
3. Remove the P13.5 catalog assertions from `extensions.test.ts`.
4. Remove register rows `P13.5-001` through `P13.5-008`.
5. Restore prior cumulative content and hashes for `P12.6-008` and
   `P12.6-010`.
6. Remove this governance record.

No backend, configuration, dependency, lockfile, upstream or runtime-state
rollback is required.

## Sequencing and Handoff

- P13.6 may proceed only after human acceptance and commit of P13.5.
- P13.7 remains blocked until P13.6.
- P14 runtime-adapter work remains blocked by its own future gate.
- P15 provider enablement remains unauthorized.
- P17 governed WorkPacket execution remains future work.
- Any real approval adapter or decision action requires a separate backend,
  identity, authorization, persistence and audit governance ticket.

## Result Markers

```text
hermes_P13_5_prerequisite_gate_passed
hermes_P13_5_dynamic_start_SHA_accepted
hermes_approval_sources_audited
hermes_false_approval_sources_rejected
hermes_approval_source_classified
hermes_approval_safe_projection_created
hermes_approval_source_IDs_preserved
hermes_approval_sensitive_fields_excluded
hermes_approval_inbox_read_only
hermes_approval_inbox_page_created
hermes_approval_detail_page_created
hermes_approval_descriptors_compiled
hermes_approval_descriptors_not_selected
hermes_approval_routes_not_registered
hermes_product_UI_feature_remains_disabled
hermes_extension_modules_remain_empty
hermes_P13_5_targeted_tests_passed
hermes_P13_5_full_dashboard_tests_passed
hermes_P13_5_typecheck_passed
hermes_P13_5_affected_lint_passed
hermes_P13_5_production_build_passed
hermes_P13_5_provider_null_runtime_passed
hermes_P13_5_preview_passed
hermes_P13_5_process_cleanup_passed
hermes_approval_inbox_ready_with_constraints
no_canonical_ApprovalRequest_created
no_Kanban_status_approval_equivalence
no_provider_auth_approval_equivalence
no_approval_mutation
no_backend_modification
no_product_configuration_activation
no_provider_activation
no_worker_or_agent_execution
no_tool_execution
no_upstream_derived_source_modification
no_dependency_or_lockfile_modification
no_git_mutation_by_agent
```

## Final Verdict

```yaml
P13_5_HermesApprovalInboxVerdict:
  start_commit:
    resolved_dynamically: true
    sha: ba36431efa0c2396695db1317a5e66edfd5310d0
    HEAD_equals_origin_main: true
    P13_4_committed: true
  implementation:
    product_additions: 8
    existing_product_owned_source_files_modified: 2
    product_control_files_modified: 1
    backend_files_modified: 0
    upstream_derived_source_files_modified: 0
    final_product_files: 6164
    final_modification_register_rows: 46
  authority:
    source_authority: provisional
    live_source_classification: safe_partial_read_source
    production_source_availability: unavailable
    canonical_approval_authority_active: false
    canonical_ApprovalRequest_created: false
    Kanban_review_equivalence_claimed: false
    Kanban_blocked_equivalence_claimed: false
    provider_auth_equivalence_claimed: false
    governed_decision_equivalence_claimed: false
  writes:
    product_surface_read_only: true
    approve_exposed: false
    reject_exposed: false
    confirm_exposed: false
    deny_exposed: false
    cancel_exposed: false
    execution_exposed: false
    policy_mutation_exposed: false
  activation:
    compiled_descriptor_count: 6
    resolved_descriptor_count: 0
    runtime_product_route_count: 0
    product_UI_enabled: false
    extension_modules_added: false
    agent_platform_navigation_visible: false
  validation:
    targeted_tests: 79_passed
    full_dashboard_tests: 121_passed
    web_typecheck: passed
    affected_lint: passed
    dashboard_build: passed_520_modules
    windows_footgun_scan: passed_755_files
    provider_null_integrated_runtime: passed
    temporary_preview: passed
    process_cleanup: passed
  execution:
    provider_enabled: false
    gateway_started: false
    worker_started: false
    agent_started: false
    tool_executed: false
    staged_by_agent: false
    committed_by_agent: false
    pushed_by_agent: false
  sequencing:
    P13_6_may_proceed_after_human_acceptance_and_commit: true
    P13_7_remains_blocked_until_P13_6: true
    P14_runtime_adapter_remains_blocked: true
    P15_provider_enablement_remains_unauthorized: true
    P17_governed_execution_remains_future: true
  final_verdict: hermes_approval_inbox_ready_with_constraints
```

## Human Commit Boundary

The agent did not stage, commit or push. Human review must include the eight
new Approval Inbox files, the two extension files, the modification register
and this canonical governance record. Temporary runtime and preview artifacts
must not be included.
