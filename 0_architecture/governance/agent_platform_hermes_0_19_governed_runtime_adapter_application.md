# P15.M7 - Governed Runtime Adapter Application

Status: P15.M7 governed runtime adapter application ready with constraints.

Final verdict: `hermes_0_19_governed_runtime_adapter_application_ready_with_constraints`

## Authority

P15.M7 applies the committed P14 governed runtime-adapter authority to the
Pepper product tree in the Hermes Agent 0.19.0-derived migration branch. The
application is bounded to the Pepper product checkout and uses only the P14
runtime-adapter source and test authority already present in this P15M
repository.

No state, file, branch or uncommitted artifact was copied from
`C:\Users\pablo\OneDrive\Escritorio\AGENT-PLATFORM-P15U`.

## Start Gate

| Check | Result |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Start HEAD | `045a420d83fe15932038880e76b3f5c00a1b39f5` |
| origin/p15.m-hermes-0.19-migration | `045a420d83fe15932038880e76b3f5c00a1b39f5` |
| HEAD equals branch remote at start | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |
| P15.M6R verdict present | `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints` |

## Committed Pepper Identity Gate

The committed Pepper identity was verified from `HEAD` with
`10_scripts/governance/pepper_baseline_integrity.py` before and after the
P15.M7 product edits.

| Scope | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate except baseline record | `6703` | `148235965` | `1897e20d93858c7125ad5ddee6ac5e56fe808b154c6e786ce42a204730a14146` |
| Payload | `6681` | `145409765` | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |
| Baseline record | `not_applicable` | `28119` | `dfbab65b5b5b960cba50c209ad3e18dc21c06b4a028322945b73f9b325633543` |

The baseline utility hashes committed Git blobs only; uncommitted P15.M7 files
do not alter this identity.

## Product Application

P15.M7 adds exactly 36 Pepper runtime-adapter product files:

| Class | Count |
| --- | ---: |
| Runtime-adapter source modules | `19` |
| Runtime-adapter test, harness and inert-probe files | `17` |
| Total product files | `36` |

Pepper-specific adaptations:

| Boundary | P14 authority | P15.M7 Pepper application |
| --- | --- | --- |
| Dashboard profile ID | `hermes.dashboard.experimental` | `pepper.dashboard.provider_null` |
| Runtime profile class | `hermes_dashboard_experimental` | `pepper_dashboard_provider_null` |
| Product ID readiness | `agent-platform-hermes` | `pepper` |
| Product UI readiness | `experimental` | `disabled` |
| Extension modules | `9` activated modules | `0` modules, `extension_modules = []` |
| Root package exports | contract-only | contract-only |

## Register And Manifest

P15.M7 updated the Pepper product modification register and created the runtime
adapter application manifest.

| Artifact | Rows | Columns | SHA-256 | Duplicate IDs | Duplicate Paths | Hash mismatches |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` | `58` total, `36` P15.M7 | `18` | `c7d3f6b114a071468b6e3523f8edb7256ef64838aa8193e29a96dbc5472254d1` | `0` | `0` | `0` for P15.M7 rows |
| `0_architecture/governance/agent_platform_hermes_0_19_runtime_adapter_application_manifest.tsv` | `36` | `19` | `539aa878ed3fa4d3a5dcea4eb00d8fba9ea5ee33893ba03d482402f6589b6518` | `0` | `not_applicable` | `0` |

The register records all P15.M7 product files as
`AGENT_PLATFORM_product_addition` against upstream commit
`3ef6bbd201263d354fd83ec55b3c306ded2eb72a` with
`baseline_source_object_or_none = none` and
`baseline_source_sha256_or_none = none`, matching the product-addition register
contract. The application manifest records the P14 source authority paths and
hashes.

## Validation

| Lane | Command | Result |
| --- | --- | --- |
| Runtime-adapter target suite | `python -m pytest tests\\hermes_cli\\test_agent_platform_runtime_adapter_contracts.py tests\\hermes_cli\\test_agent_platform_runtime_profiles.py tests\\hermes_cli\\test_agent_platform_runtime_environment.py tests\\hermes_cli\\test_agent_platform_runtime_workspace.py tests\\hermes_cli\\test_agent_platform_runtime_path_containment.py tests\\hermes_cli\\test_agent_platform_runtime_event_normalization.py tests\\hermes_cli\\test_agent_platform_runtime_audit_normalization.py tests\\hermes_cli\\test_agent_platform_runtime_process_owner.py tests\\hermes_cli\\test_agent_platform_runtime_lifecycle_control.py tests\\hermes_cli\\test_agent_platform_runtime_rollback.py tests\\hermes_cli\\runtime_adapter_conformance_harness.py tests\\hermes_cli\\runtime_adapter_lifecycle_probe.py tests\\hermes_cli\\test_agent_platform_runtime_adapter_conformance.py tests\\hermes_cli\\test_agent_platform_runtime_adapter_failure_conformance.py tests\\hermes_cli\\test_agent_platform_runtime_listener_discovery.py tests\\hermes_cli\\test_agent_platform_runtime_readiness.py tests\\hermes_cli\\test_agent_platform_runtime_adapter_integration.py` from `2_products/pepper-agent` | `143 passed, 5 skipped` |
| Pepper baseline-governance suite | `python -m pytest 12_tests\\governance\\test_pepper_baseline_integrity.py` | `14 passed` |
| Committed Pepper identity | `python 10_scripts\\governance\\pepper_baseline_integrity.py --repo-root C:\\Users\\pablo\\OneDrive\\Escritorio\\AGENT-PLATFORM-P15M --product-root 2_products/pepper-agent --format json` | matched P15.M6R authority |
| P15.M7 register and manifest hash validation | custom row/hash validation over P15.M7 rows and manifest rows | `0` duplicate IDs, `0` duplicate paths, `0` P15.M7 hash mismatches, `0` manifest hash mismatches |

Generated `__pycache__` and `.pytest_cache` directories from validation were
removed after test execution.

## Authority Denials

```yaml
provider_credentials_authorized: false
provider_inference_authorized: false
worker_launch_authorized: false
agent_launch_authorized: false
tool_execution_authorized: false
MCP_execution_authorized: false
public_runtime_HTTP_API_authorized: false
runtime_UI_controls_authorized: false
audit_persistence_authorized: false
event_publication_authorized: false
frontend_modification_authorized: false
web_server_modification_authorized: false
product_configuration_modification_authorized: false
package_manifest_or_lockfile_modification_authorized: false
baseline_json_modification_authorized: false
import_or_exclusion_manifest_modification_authorized: false
third_party_notice_modification_authorized: false
desktop_or_workspace_modification_authorized: false
Graphify_regeneration_authorized: false
P15U_state_authorized: false
git_staging_commit_push_authorized: false
```

## Known Constraints

```text
runtime adapter remains internal
only loopback local execution is covered
provider-null runtime only
product UI remains disabled
extension module registry remains empty
no worker runtime
no agent runtime
no tool execution
no MCP execution
no public lifecycle API
no lifecycle UI controls
no durable audit persistence
no dependency or lockfile change
no frontend change
no backend route change
no baseline JSON update
no import or exclusion manifest update
no third-party notice update
no Desktop or Workspace enablement
no Graphify regeneration
no Git mutation by agent
```

## Final State For Human Review

```yaml
P15_M7_GovernedRuntimeAdapterApplication:
  final_verdict: hermes_0_19_governed_runtime_adapter_application_ready_with_constraints
  product_id: pepper
  upstream_product_name: Hermes Agent
  upstream_version: 0.19.0
  upstream_commit: 3ef6bbd201263d354fd83ec55b3c306ded2eb72a
  runtime_profile_ids:
    - test.lifecycle_probe
    - pepper.dashboard.provider_null
  product_ui: disabled
  extension_modules: []
  product_files_added: 36
  register_rows_added: 36
  manifest_rows: 36
  manifest_columns: 19
  tests:
    runtime_adapter_target_suite: 143_passed_5_skipped
    pepper_baseline_governance: 14_passed
  P15U_state_used: false
  git_staged_by_agent: false
  git_committed_by_agent: false
  git_pushed_by_agent: false
```
