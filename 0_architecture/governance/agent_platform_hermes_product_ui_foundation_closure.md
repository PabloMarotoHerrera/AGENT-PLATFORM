# P13.R - Hermes Product UI Foundation Closure

## Document Header

| Field | Value |
| --- | --- |
| Project | P13 - Hermes Product UI Foundation |
| Ticket | P13.R - Product UI Foundation Closure |
| Date | 2026-07-18 |
| Status | `hermes_product_ui_foundation_closed_experimental_with_constraints` |
| Canonical output | `0_architecture/governance/agent_platform_hermes_product_ui_foundation_closure.md` |
| Accepted start commit | `1fefa7135484f7b7c590945a040b6e7f267608e7` |
| Accepted prerequisite | Committed P13.8 Hermes Frontend Quality Gate |
| Reuse decision | `activate_reviewed_descriptors` |
| Git mutation by agent | No staging, commit or push performed |

## Purpose

Close the P13 Hermes Product UI Foundation by activating the reviewed nine
AGENT PLATFORM dashboard descriptors through the tracked product configuration.
P13.R changes the committed product UI posture from disabled and unselected to
experimental and explicitly selected.

This closure does not grant production, provider/model, gateway lifecycle,
worker lifecycle, agent lifecycle, approval-decision, execution-control,
assignment-dispatch, feature-toggle UI, plugin, MCP, secret, OAuth or raw
configuration authority. It also does not set `agent_platform.product_ui` to
`enabled`.

## Dynamic Prerequisite Result

```yaml
P13_R_PrerequisiteStatus:
  branch: main
  accepted_head: 1fefa7135484f7b7c590945a040b6e7f267608e7
  origin_main: 1fefa7135484f7b7c590945a040b6e7f267608e7
  head_equals_origin_main: true
  git_index_empty_at_start: true
  tracked_product_clean_at_start: true
  P13_8_governance_record_present: true
  P13_8_frontend_quality_gate_committed: true
  product_tracked_files_at_start: 6183
  modification_register_rows_at_start: 65
  modification_register_columns_at_start: 18
  modification_register_duplicate_ids_at_start: 0
  modification_register_duplicate_paths_at_start: 0
  modification_register_missing_fields_at_start: 0
  modification_register_hash_mismatches_at_start: 0
  compiled_product_descriptors_at_start: 9
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

Allowed unrelated untracked paths at start were `.opencode/`, `AGENTS.md` and
`graphify-out/`. They remain outside the P13.R source output.

## P13 Closure Matrix

| Ticket | Commit | Material result | Closure decision |
| --- | --- | --- | --- |
| P13.0 | `c37abb4fa878ceb3a269f16b58b6016d122d5ea0` | Product brief and information architecture | Accepted |
| P13.1 | `54741f8e5d4da5fea35eb96751b2b4cda10cde6d` | Design tokens and branding foundation | Accepted |
| P13.2 | `9dd371b82b6f169aa975003c146a29f924fe3cb9` | Application shell and navigation | Accepted |
| P13.3-PRE | `c19310fee5af0d321bdd0655afe4f4f3085e72aa` | Activation semantic test correction | Accepted |
| P13.3 | `96ab6bb222677a1a09c6bc0f84752865c7b4960e` | Runtime Overview | Accepted |
| P13.4 | `ba36431efa0c2396695db1317a5e66edfd5310d0` | Projects and Tickets workspace | Accepted |
| P13.5 | `9e8306234e183c44d63eb52441e7075de83a0c73` | Approval Inbox | Accepted |
| P13.6 | `a427689b1f9078321dc59a7fa5e589a3fe31fb16` | Execution Inspector | Accepted |
| P13.7 | `3460738cb1597c46272bc7f10040222da8570e9d` | Safe Settings and feature posture | Accepted |
| P13.8 | `1fefa7135484f7b7c590945a040b6e7f267608e7` | Frontend Quality Gate | Accepted with constraints |

All prerequisite P13 implementation records are present in current main history.
P13.R relies on the P13.8 human visual checkpoint result `ACCEPTED` for the
compiled surfaces before changing the tracked activation posture.

## Activation Decision

P13.R changes only the authoritative tracked product configuration default:

```yaml
P13_R_ActivationDecision:
  agent_platform.product_ui: experimental
  forbidden_state: enabled
  extension_modules:
    - agent_platform.ui.overview
    - agent_platform.ui.projects
    - agent_platform.ui.project_detail
    - agent_platform.ui.ticket_detail
    - agent_platform.ui.approvals
    - agent_platform.ui.approval_detail
    - agent_platform.ui.executions
    - agent_platform.ui.execution_detail
    - agent_platform.ui.settings
```

The resolved activation posture is:

```yaml
P13_R_ActivationStatus:
  compiled_descriptors: 9
  selected_descriptors: 9
  resolved_descriptors: 9
  product_routes_registered: 9
  product_navigation_items: 5
  product_UI_feature: experimental
```

## Files Updated

P13.R updated the tracked product defaults and the tests/evidence contracts that
assert the new activation posture:

```text
2_products/hermes-agent/hermes_cli/agent_platform/product_config.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_product_config.py
2_products/hermes-agent/tests/hermes_cli/test_agent_platform_product_routes.py
2_products/hermes-agent/web/src/agent-platform/product-config.test.ts
2_products/hermes-agent/web/src/agent-platform/extensions.test.ts
2_products/hermes-agent/web/src/agent-platform/design-system/design-system.test.ts
2_products/hermes-agent/web/src/agent-platform/safe-settings/safe-settings.test.tsx
2_products/hermes-agent/web/src/agent-platform/frontend-quality/quality-contract.ts
2_products/hermes-agent/web/src/agent-platform/frontend-quality/quality-matrix.ts
2_products/hermes-agent/web/src/agent-platform/frontend-quality/frontend-quality-gate.test.tsx
2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

No P13.R source edit was made to route composition, `web/src/App.tsx`,
`web/src/main.tsx`, `web/src/agent-platform/extensions.ts`, product pages,
product hooks, backend route composition, schema/transport code, manifests,
lockfiles, immutable upstream or Graphify output.

## Modification Register

```yaml
P13_R_register_result:
  rows_before: 65
  rows_after: 65
  columns: 18
  rows_added: []
  duplicate_ids: 0
  duplicate_paths: 0
  missing_fields: 0
  hash_mismatches: 0
  product_owned_additions: 62
  upstream_derived_modifications: 3
  register_sha256: 14a27d5b424dc7c7463fa16f53a647f2b85f9ef22039a51bd1dc9532d399ee03
  normalized_rows_sha256: 077fb199ad94e8059b0d85164c414b94a2eb702527289abc899c5dede596e57a
```

## Automated Validation

| Lane | Result | Evidence |
| --- | --- | --- |
| Backend product configuration/routes | Pass | Temp venv `p13r-venv`; `scripts/run_tests_parallel.py tests/hermes_cli/test_agent_platform_product_config.py tests/hermes_cli/test_agent_platform_product_routes.py -q`, 16 tests |
| Python style | Pass | `ruff check` on P13.R Python files |
| Python format | Pass | `ruff format --check` on P13.R Python files |
| Frontend product UI slice | Pass | `npm test --workspace web -- src/agent-platform`, 10 files, 156 tests |
| TypeScript | Pass | `npm run typecheck --workspace web` |
| Scoped ESLint | Pass | `node ..\node_modules\eslint\bin\eslint.js src/agent-platform` |
| Web build | Pass | `npm run build --workspace web`; Vite completed with existing large-chunk warning |
| Modification register | Pass | 65 rows, 18 columns, zero hash mismatches |

The temporary Python environment used for backend validation lives under the
approved temp directory:

```text
C:\Users\pablo\AppData\Local\Temp\opencode\p13r-venv
```

## Graphify Integrity

P13.R used Graphify only for bounded read-only prerequisite and defect-diagnosis
queries. No Graphify generation, update, extraction, clustering, export or
refresh command ran as part of P13.R.

```yaml
P13_R_GraphifyIntegrity:
  graph_json_sha256: 02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2
  provenance_json_sha256: 952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550
  graphify_generation_performed: false
```

## Phase A Human Review

```yaml
P13_R_PhaseA_InitialHandoff:
  status: changes_requested
  dashboard_url: http://127.0.0.1:9129/agent-platform/overview?profile=default
  runtime_artifacts_root: 9_artifacts/hermes/p13.r
  dashboard_process_root_pid: 14636
  dashboard_serving_pid: 8844
  dashboard_ready_file: 9_artifacts/hermes/p13.r/runtime/dashboard-ready.json
  dashboard_ready_port: 9129
  readiness_probe:
    api_status_http: 200
    root_http: 200
    unauthenticated_product_configuration_http: 401
    authenticated_product_configuration_http: 200
    authenticated_product_UI_feature: experimental
    authenticated_extension_modules: 9
    overview_route_http: 200
  human_result: CHANGES_REQUESTED
  accepted_evidence:
    product_group_navigation_order: correct
    existing_hermes_routes: reachable
    safe_settings_counts: correct
    main_product_pages: render
    approval_execution_mutation_controls: absent
    gateway_provider_worker_agent_session_controls: inactive
  material_defect: Native Hermes Files defaulted to C:\Users\pablo and exposed real user directories and mutation controls there.

P13_R_PhaseA_CorrectedHandoff:
  status: accepted
  dashboard_url: http://127.0.0.1:9129/agent-platform/overview?profile=default
  runtime_artifacts_root: 9_artifacts/hermes/p13.r
  dashboard_wrapper: 9_artifacts/hermes/p13.r/dashboard/start-corrected.cmd
  dashboard_process_root_pid: 28352
  dashboard_parent_python_pid: 25724
  dashboard_serving_pid: 34152
  dashboard_ready_file: 9_artifacts/hermes/p13.r/runtime/dashboard-ready-corrected.json
  dashboard_ready_port: 9129
  isolation_environment:
    HERMES_HOME: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\9_artifacts\hermes\p13.r\runtime\hermes-home
    HERMES_DASHBOARD_FILES_ROOT: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\9_artifacts\hermes\p13.r\runtime\files-root
    HERMES_SHARED_AUTH_DIR: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\9_artifacts\hermes\p13.r\runtime\shared-auth
    HOME: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\9_artifacts\hermes\p13.r\runtime\windows-home
    USERPROFILE: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\9_artifacts\hermes\p13.r\runtime\windows-home
  readiness_probe:
    api_status_http: 200
    root_http: 200
    unauthenticated_product_configuration_http: 401
    authenticated_product_configuration_http: 200
    authenticated_product_UI_feature: experimental
    authenticated_extension_modules: 9
    overview_route_http: 200
  files_revalidation:
    default_path: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\9_artifacts\hermes\p13.r\runtime\files-root
    files_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\9_artifacts\hermes\p13.r\runtime\files-root
    locked_root: C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\9_artifacts\hermes\p13.r\runtime\files-root
    can_change_path: false
    entries: 0
    real_user_home_probe_http: 403
    real_user_home_probe_detail: Path outside managed files root
  human_result: ACCEPTED
  accepted_activation_evidence:
    agent_platform_product_group_visible: true
    primary_navigation_order:
      - Overview
      - Projects
      - Approvals
      - Executions
      - Settings
    contextual_detail_routes_excluded_from_primary_navigation: true
    native_hermes_tools_extensions_administration_available: true
    existing_native_hermes_routes_reachable: true
    product_surfaces_rendered:
      - Runtime Overview
      - Projects
      - Approval Inbox
      - Execution Inspector
      - Safe Settings
    safe_settings_counts:
      product_ui_feature: experimental
      compiled_descriptors: 9
      selected_modules: 9
      resolved_descriptors: 9
      registered_routes: 9
      navigation_items: 5
    visible_experimental_posture: true
    approval_execution_source_local_boundaries_preserved: true
    unauthorized_approval_execution_provider_worker_agent_controls_absent: true
    gateway_providers_workers_agents_sessions_inactive: true
    hermes_teal_rendered_correctly: true
    preserved_native_surfaces:
      - Chat
      - Sessions
      - Files
      - Models
      - Cron
      - Skills
      - Kanban
      - Achievements
      - Administration
      - Documentation
  accepted_files_isolation_evidence:
    page_no_longer_enumerates_real_user_home: true
    managed_root_empty_and_isolated: true
    can_change_path: false
    real_user_home_probe_http: 403
    no_real_user_file_or_directory_mutation_during_review: true
  accepted_experimental_constraints:
    native_administration_pages_retain_existing_write_controls: true
    native_pages_may_display_absolute_paths_inside_isolated_runtime: true
    files_upload_create_controls_limited_to_isolated_managed_root: true
    native_channels_config_profiles_surfaces_remain_experimental_administration_tools: true
    acceptance_does_not_authorize_provider_setup_gateway_startup_channel_activation_plugin_installation_file_mutation_worker_startup_agent_execution_or_production_deployment: true
```

Phase A initially received `CHANGES_REQUESTED` because the first dashboard launch
left the native Hermes Files page rooted at the real user home. The corrected
dashboard was relaunched with `HERMES_DASHBOARD_FILES_ROOT` locked to
`9_artifacts/hermes/p13.r/runtime/files-root`; authenticated `/api/files`
defaulted to that root and rejected `C:\Users\pablo` with HTTP 403. Human review
accepted the corrected activation checkpoint and completed Phase A.

## Phase B Cleanup and Reconciliation

```yaml
P13_R_PhaseB_Result:
  verdict: hermes_product_ui_foundation_closed_experimental_with_constraints
  dashboard_cleanup:
    explicitly_stopped_serving_pid: 34152
    related_pids_absent_after_stop:
      - 28352
      - 25724
      - 34152
      - 16060
    p13r_dashboard_processes_remaining: 0
    port_9129_listener_remaining: false
    automated_browser_remaining: false
    devtools_listener_remaining: false
  artifact_cleanup:
    removed_artifact_root: 9_artifacts/hermes/p13.r
    removed_validation_venv: C:\Users\pablo\AppData\Local\Temp\opencode\p13r-venv
    p13r_artifact_root_remaining: false
    p13r_validation_venv_remaining: false
  runtime_isolation:
    corrected_runtime_paths_were_under: 9_artifacts/hermes/p13.r/runtime
    real_user_home_files_page_probe_http: 403
    human_review_reported_no_real_user_file_or_directory_mutation: true
    no_real_user_hermes_state_path_configured_for_corrected_runtime: true
  workspace_junctions:
    hermes_shared_path: 2_products/hermes-agent/node_modules/@hermes/shared
    hermes_shared_attributes: Directory, ReparsePoint
    hermes_shared_link_type: Junction
    hermes_shared_target: 2_products/hermes-agent/apps/shared
    hermes_shared_package_json_present: true
  graphify_integrity_after_cleanup:
    graph_json_sha256: 02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2
    provenance_json_sha256: 952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550
    graphify_generation_performed: false
  final_register_reconciliation:
    status: passed
    rows: 65
    columns: 18
    product_owned_additions: 62
    upstream_derived_modifications: 3
    duplicate_ids: 0
    duplicate_paths: 0
    missing_fields: 0
    hash_mismatches: 0
    register_sha256: 14a27d5b424dc7c7463fa16f53a647f2b85f9ef22039a51bd1dc9532d399ee03
    normalized_rows_sha256: 077fb199ad94e8059b0d85164c414b94a2eb702527289abc899c5dede596e57a
  final_git_state:
    staged_paths: []
    tracked_product_paths_modified: 11
    closure_record_untracked: true
    allowed_untracked_paths_present:
      - .opencode/
      - AGENTS.md
      - graphify-out/
    git_add_commit_push_performed: false
```

Phase B performed cleanup only. No implementation, automated browser validation,
runtime verification, Graphify regeneration, provider setup, gateway startup,
worker startup, agent execution, staging, commit or push was performed.

## Constraints

The activated product UI remains a read-only product foundation. The selected
routes expose navigation, refresh, filtering and trusted display-preference
writes only where already allowed by P13.7. Approval decisions, execution
controls, work mutation, assignment, feature toggles, provider/model mutation,
plugin/MCP/hook controls, secrets, OAuth flows, raw configuration and lifecycle
actions remain excluded.
