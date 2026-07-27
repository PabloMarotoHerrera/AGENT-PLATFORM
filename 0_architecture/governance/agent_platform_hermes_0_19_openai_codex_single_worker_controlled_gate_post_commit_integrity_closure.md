# Hermes 0.19 OpenAI Codex Single Worker Controlled Gate Post-Commit Integrity Closure

Final verdict: `hermes_0_19_openai_codex_single_worker_controlled_gate_post_commit_integrity_closed_with_constraints`

## Ticket Authority

P15.7R closes the committed integrity state of P15.7 - Single Worker Controlled Gate.

P15.7R is a post-commit integrity validation and governance closure only. It does not authorize another live provider request, credential access, OAuth, refresh, rotation, Docker execution, Graphify, retry, fallback, worker execution, remote host contact, production rollout or VPS deployment.

## Repository State

| Field | Value |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `0df2277f8b6fcde4714c21ba55c32fa2d77655da` |
| Remote HEAD | `0df2277f8b6fcde4714c21ba55c32fa2d77655da` |
| HEAD equals remote | `true` |
| Index empty before P15.7R record | `true` |
| Staged files before P15.7R record | `0` |
| Tracked worktree clean before P15.7R record | `true` |
| Visible untracked candidates before P15.7R record | `0` |
| P15.7R record present before creation | `false` |
| Post-P15.7 commits before P15.7R | `0` |

## P15.7 Commit Authority

The unique commit that introduced `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_single_worker_controlled_gate.md` is `0df2277f8b6fcde4714c21ba55c32fa2d77655da`.

```yaml
P15_7_commit: 0df2277f8b6fcde4714c21ba55c32fa2d77655da
P15_7_commit_is_ancestor_of_HEAD: true
HEAD_equals_P15_7_commit: true
P15_7_parent: 22a759693c2bae018b839139cf4a167f9cd50924
P15_7_parent_message: P15.6R Close provider failure policy integrity
P15_7_commit_message: P15.7 Add single worker controlled gate
P15_7_governance_verdict: hermes_0_19_openai_codex_single_worker_controlled_gate_ready_with_constraints
```

## P15.7 Commit Path Set

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_single_worker_controlled_gate.md` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Added | `2_products/pepper-agent/docs/agent-platform/provider_single_worker_controlled_gate.md` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker_gate/__init__.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker_gate/contracts.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker_gate/runtime.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker_gate/single_dispatch.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_worker_controlled_gate.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_worker_gate_contracts.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_worker_single_dispatch.py` |

```yaml
commit_files: 11
created_files: 9
modified_files: 2
unexpected_commit_paths: 0
product_additions: 8
governance_additions: 1
TSV_modifications: 2
package_files: 4
test_files: 3
product_documentation_files: 1
```

The two TSV modifications added eight P15.7 rows each and removed zero rows.

## P15.6R Prerequisite Authority

Required prerequisite record: `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_failure_retry_policy_post_commit_integrity_closure.md`.

```yaml
P15_6R_commit: 22a759693c2bae018b839139cf4a167f9cd50924
P15_6R_is_parent_of_P15_7: true
P15_6R_verdict: hermes_0_19_openai_codex_provider_failure_retry_policy_post_commit_integrity_closed_with_constraints
automatic_retry_allowed: false
maximum_automatic_retries: 0
same_request_retry_allowed: false
same_worker_retry_allowed: false
credential_rotation_allowed: false
automatic_fallback_allowed: false
maximum_provider_dispatches_per_request: 1
```

## Candidate Integrity

Pre-P15.7 committed candidate identity:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6784
bytes: 149411321
SHA256: d655fec6b50ddccc36a7fcd061bbafb8d0752bfde55954993e6ca1fcd19146dc
```

Post-P15.7 committed candidate identity:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6792
bytes: 149523599
SHA256: f3b4bdd5ae57ad69fad41c3cf9c0ce39ac92fc846578f2cc14e8aa4c6f465c91
candidate_file_delta: 8
candidate_bytes_greater_than_pre_P15_7: true
candidate_SHA_changed: true
```

## Payload And Baseline

Upstream payload identity is unchanged:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6681
bytes: 145409792
SHA256: 1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c
payload_file_delta: 0
payload_byte_delta: 0
payload_SHA_changed: false
```

Baseline record identity is unchanged:

```yaml
path: 2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
algorithm: sha256-git-blob-v1
bytes: 38693
SHA256: fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030
upstream_version: 0.19.0
upstream_commit: 3ef6bbd201263d354fd83ec55b3c306ded2eb72a
baseline_modified_by_P15_7: false
dependency_inventory_changed: false
source_integrity_changed: false
```

Governance integrity tests: `14 passed, 0 failures, 0 errors`.

## Modification Register Closure

P15.7 modification-register rows are valid:

```yaml
P15_7_rows: 8
required_IDs:
  - P15.7-001
  - P15.7-002
  - P15.7-003
  - P15.7-004
  - P15.7-005
  - P15.7-006
  - P15.7-007
  - P15.7-008
duplicate_modification_IDs: 0
duplicate_P15_7_paths: 0
owner_ticket: P15.7
change_class: AGENT_PLATFORM_product_addition
baseline_upstream_commit: 3ef6bbd201263d354fd83ec55b3c306ded2eb72a
baseline_source_object: none
baseline_source_SHA256: none
conflict_owner: AGENT_PLATFORM_provider_worker_gate_owner
mixed_conflict_owners: 0
upstream_disposition: retain_product_divergence
rollback_target: delete_path
status: implemented_pending_human_approval
path_present_in_HEAD: true
current_product_SHA256_equals_committed_blob_SHA256: true
```

| Path | SHA-256 |
| --- | --- |
| `hermes_cli/agent_platform/provider_worker_gate/__init__.py` | `45a1238ccd89c627ad5c90bd25ed5da114a5767c3439b4356ef86caafcdd1a90` |
| `hermes_cli/agent_platform/provider_worker_gate/contracts.py` | `d83c02cac288fd1d96a114975157f90b95d35ee6c4d5d828c7b56535a42e165e` |
| `hermes_cli/agent_platform/provider_worker_gate/single_dispatch.py` | `553d374681fb979b94f49875268ffdd28516bc05241e0e9c2e6b7fad49fb2b4d` |
| `hermes_cli/agent_platform/provider_worker_gate/runtime.py` | `63f477b7b70293d190b33312b070b06a0b3238b477b196b49d1f9c8e8bb388d2` |
| `tests/hermes_cli/test_agent_platform_provider_worker_gate_contracts.py` | `4c4d30fd37c14aa421c9f79eaaf7c022149ebbbb7f7b2a5ee7bd3be1c59d260b` |
| `tests/hermes_cli/test_agent_platform_provider_worker_single_dispatch.py` | `a8832927dffa4d68043091755da01243d48f15226a104ce00d5137109259665f` |
| `tests/hermes_cli/test_agent_platform_provider_worker_controlled_gate.py` | `e847e66823e862f9abd44cc9bc28c5dddde4aa5f641d080931723339ed457d91` |
| `docs/agent-platform/provider_single_worker_controlled_gate.md` | `fb27fadce723c8570c21737317e0e008f3cdb875b101131ee7d3ac3cb537eefd` |

## Import Manifest Closure

P15.7 import-manifest rows are valid:

```yaml
P15_7_rows: 8
classification: AGENT_PLATFORM_product_addition
duplicate_destination_paths: 0
committed_destination_present: true
committed_SHA256_matches: true
included_in_upstream_payload: false
existing_non_P15_7_rows_modified: 0
forbidden_upstream_payload_classifications: 0
```

No P15.7 row uses `included_byte_exact`, `included_canonical_text_lf` or `transformed_by_canonical_compliance_rule`.

## Controlled Gate Package Closure

Committed package: `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker_gate`.

Required files are present: `__init__.py`, `contracts.py`, `single_dispatch.py`, `runtime.py`.

```yaml
gate_policy: present
gate_counters: present
gate_diagnostics: present
gate_envelope: present
cleanup_projection: present
single_dispatch_seam: present
stdio_runtime: present
deterministic_serialization: present
workers_per_attempt_maximum: 1
requests_per_worker_lifetime: 1
provider_dispatches_per_request_maximum: 1
automatic_retries: 0
fallback_calls: 0
credential_rotations: 0
model_list_calls: 0
tool_calls: 0
MCP_calls: 0
```

## Gate Identity Closure

```yaml
schema_version: 1
gate_id: gate.openai-codex.chatgpt-oauth.gpt-5.5.single-worker.v1
provider_profile: provider.openai-codex.chatgpt-oauth.gpt-5.5.v1
worker_profile: worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
accounting_policy: accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
failure_policy: failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
provider_wire_streaming: true
application_streaming: false
```

## Single-Dispatch Seam Closure

Committed source contains the required direct call:

```text
client.responses.create(**create_kwargs)
```

```yaml
responses_create_call_sites: 1
responses_create_calls_per_request_maximum: 1
SDK_max_retries: 0
worker_level_retries: 0
run_codex_stream_imported: false
run_codex_stream_called: false
generic_retry_loop_called: false
generic_fallback_called: false
conversation_loop_called: false
provider_dispatch_increment: immediately_before_responses_create
responses_create_failure:
  dispatch_count: 1
  phase: dispatch
stream_iterator_failure:
  dispatch_count: 1
  phase: stream
stream_phase_with_dispatch_zero: impossible
outer_runtime_counter_reset: prohibited
```

The package imports only the allowed raw event consumer `agent.codex_runtime._consume_codex_event_stream` and does not call the generic retrying or fallback Codex runtime helpers.

## Corrected Codex Request Shape

Required present wire keys:

```text
model
instructions
input
store
reasoning
include
prompt_cache_key
stream
```

Required values:

```yaml
model: gpt-5.5
store: false
stream: true
reasoning_effort: medium
```

Required absent wire keys:

```text
max_output_tokens
tools
tool_choice
parallel_tool_calls
service_tier
fallback_model
caller_generation_overrides
caller_timeout_overrides
unsupported_body_headers
```

Local controls:

```yaml
exact_output_validation: true
local_output_UTF8_bound: enforced
provider_response_ID_retained: false
raw_provider_response_retained: false
reasoning_trace_retained: false
```

## Diagnostic Checkpoint Closure

Required bounded checkpoints are present and validated:

```text
request_validated
client_construction_started
client_constructed
dispatch_started
event_stream_obtained
stream_iteration_started
first_event_observed
terminal_event_observed
accounting_started
accounting_completed
worker_result_completed
cleanup_started
cleanup_completed
```

Diagnostics remain bounded and secret-free:

```yaml
phase: bounded_enum
last_completed_checkpoint: bounded_enum
safe_exception_class: class_name_only
safe_exception_module: module_name_only
provider_dispatches: bounded_0_or_1
cleanup_status: bounded
raw_exception_message: absent
raw_traceback: absent
request_body: absent
response_body: absent
provider_headers: absent
credentials: absent
account_identity: absent
provider_response_ID: absent
personal_absolute_runtime_paths: absent
```

## Worker Protocol Closure

```yaml
entrypoint: run_worker_stdio
stdin_frames: exactly_1
stdout_envelopes: exactly_1
stdout_JSON_parseable: true
second_request: rejected_or_worker_already_exited
worker_process_reuse: false
stdout_logs: prohibited
stderr: bounded_secret_free_only
session_database: absent
conversation_history: absent
persistent_memory: absent
context_file_loading: absent
trajectory_writes: absent
arbitrary_product_writes: absent
```

## Offline Execution Substrate Evidence

The committed P15.7 governance record documents the retained offline-qualified image and the source/tests verify the actual entrypoint behavior.

```yaml
image_tag: pepper-agent:p15-m10-990d153cd370
image_ID: sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd
current_source_authority: mounted_P15_7_working_tree
baked_image_source_authority: false
qualification_network: none
container_user: non_root
Python: 3.13.5
openai: 2.24.0
pydantic: 2.13.4
httpx: 0.28.1
entrypoint: run_worker_stdio
stdin_frames: 1
stdout_envelopes: 1
worker_result_state: completed
exact_output: PEPPER_P15_7_OK
synthetic_provider_dispatches: 1
synthetic_responses_create_calls: 1
accounting_records: 1
failure_records: 0
automatic_retries: 0
fallback_calls: 0
cleanup: passed
```

P15.7R did not rerun Docker.

## Live Attempt History Closure

First attempt:

```yaml
authorization: explicit
result: failed
confirmed_provider_dispatches: 1
failure_category: request_invalid
root_cause: noncanonical_codex_backend_request_shape
automatic_retries: 0
fallback_calls: 0
credential_refresh_calls: 0
cleanup: passed
```

Second attempt:

```yaml
authorization: explicit
reported_result: blocked
originally_reported_category: unknown
originally_reported_stage: stream
originally_reported_dispatches: 0
retrospective_runtime_evidence: insufficient
exact_provider_dispatches: not_asserted
exact_failure_stage: not_asserted
cleanup: passed
```

Third attempt:

```yaml
authorization: explicit
result: completed
provider_dispatches: 1
responses_create_calls: 1
actual_output: PEPPER_P15_7_OK
exact_output_match: true
worker_result_state: completed
accounting_records: 1
failure_records: 0
automatic_retries: 0
fallback_calls: 0
identity_linkage: passed
cleanup: passed
active_leases_after: 0
containers_after: 0
runtime_residue: 0
```

## Cumulative Evidence Closure

```yaml
explicit_authorizations: 3
attempts: 3
confirmed_provider_dispatches_minimum: 2
provider_dispatches_maximum_possible: 3
exact_cumulative_provider_dispatches: not_asserted
successful_inferences: 1
confirmed_failed_inferences_minimum: 1
automatic_retries: 0
fallback_calls: 0
credential_rotations: 0
OAuth_attempts: 0
```

Each explicitly authorized request had at most one provider dispatch. No request performed an automatic retry. The only historical uncertainty concerns the second attempt's exact dispatch count. The final accepted gate implementation has deterministic counter ownership and makes stream phase with zero dispatch impossible.

## Credential Boundary Closure

```yaml
credential_store: openai-codex.primary
configured: true
credential_count: 1
token_pair_present: true
credential_state: ready
durable_store_visible_to_worker: false
temporary_lease_created_for_successful_attempt: 1
temporary_lease_released: 1
projected_HERMES_HOME: used
automatic_refresh: false
credential_rotation: false
durable_credential_retained: true
active_leases_after: 0
projected_auth_files_after: 0
```

No credential values, account identity, `auth.json` contents or personal absolute credential paths are retained in this record.

## Accounting And Identity Link Closure

```yaml
accounting_records: 1
outcome: completed
cost_status: included
billing_mode: subscription_included
exact_marginal_request_cost: unavailable
provider_usage_API_called: false
provider_billing_API_called: false
provider_response_ID_retained: false
raw_usage_retained: false
worker_result_usage_record_ID_matches: true
worker_result_request_ID_matches: true
worker_result_runtime_ID_matches: true
worker_result_correlation_ID_matches: true
accounting_provider_call_count: 1
failure_records: 0
retry_decisions: 0
```

## Cleanup And Residue Closure

```yaml
containers: 0
P15_7_networks: 0
provider_worker_processes: 0
active_leases: 0
projected_auth_files: 0
temporary_HERMES_HOME_directories: 0
temporary_runner_files: 0
temporary_virtualenvs: 0
host_listeners: 0
durable_credential: retained
repository_source: unchanged
cleanup: passed
```

## Regression And Static Validation

Required tests passed from committed source:

```yaml
P15_7_targeted:
  passed: 22
  failed: 0
  errors: 0
  skipped: 0
P15_6_failure_policy:
  passed: 56
  failed: 0
  errors: 0
  skipped: 0
P15_5_accounting:
  passed: 19
  failed: 0
  errors: 0
  skipped: 0
prior_provider_credential_worker_regression:
  passed: 119
  failed: 0
  errors: 0
  warnings: 3
new_P15_7_regressions: 0
```

Warning classification:

```yaml
expected_inherited_Pydantic_warnings:
  - model_id
  - model_policy
  - model_list_calls_per_request_maximum
new_P15_7_warnings: 0
```

Focused static validation:

```yaml
ruff_check: passed
ruff_format_check: passed
ty_availability: unavailable
type_check: not_run_tool_unavailable
type_errors: not_asserted
dependency_installation: 0
```

## Operational Authority Scan

Committed production source under `hermes_cli/agent_platform/provider_worker_gate` is restricted to the controlled runtime and single-dispatch seam.

```yaml
automatic_retry_loop: absent
fallback_execution: absent
credential_store_discovery: absent_beyond_fixed_controlled_store_root
durable_credential_read_by_worker: absent
credential_refresh: absent
credential_rotation: absent
model_list_call: absent
tool_execution: absent
MCP_execution: absent
session_persistence: absent
conversation_persistence: absent
arbitrary_file_write: absent
subprocess_shell: absent
provider_network_call_sites: exactly_1
call: client.responses.create
dispatch_counter_guarded: true
```

The runtime can request one authorized temporary credential projection through the governed delivery boundary. The worker-facing provider call uses only the projected home and never mounts or exposes the durable credential store to the worker.

## Secret Safety

Secret-safety scan scope:

```text
eight P15.7 product additions
both TSV files
committed P15.7 governance record
this P15.7R candidate
```

Retained secret-bearing evidence counts:

```yaml
access_tokens: 0
refresh_tokens: 0
authorization_headers: 0
device_codes: 0
verification_URLs: 0
account_identifiers: 0
JWT_claims: 0
credential_contents: 0
raw_provider_responses: 0
raw_provider_headers: 0
raw_provider_failure_messages: 0
provider_response_ID_values: 0
real_prompt_content_beyond_fixed_gate_prompt: 0
reasoning_traces: 0
private_keys: 0
personal_absolute_runtime_paths: 0
```

Allowed bounded literals are `PEPPER_P15_7_OK`, `request_invalid` and `unknown`. Synthetic test placeholders are not credential evidence and are not retained runtime secrets.

## No-Execution Counters

P15.7R performed no live or credentialed execution:

```yaml
Docker: 0
OAuth: 0
credential_reads: 0
credential_writes: 0
credential_leases: 0
credential_refreshes: 0
credential_rotations: 0
provider_dispatches: 0
provider_streams: 0
automatic_retries: 0
fallback_calls: 0
model_list_calls: 0
usage_API_calls: 0
quota_API_calls: 0
billing_API_calls: 0
worker_processes: 0
remote_hosts_contacted: 0
Graphify_commands: 0
```

## Repository Non-Mutation Closure

P15.7R created exactly one untracked governance candidate and modified no tracked file.

```yaml
candidate_files: 1
created_files: 1
modified_files: 0
unexpected_candidates: 0
tracked_changes: 0
product_files_modified: 0
tests_modified: 0
documentation_modified: 0
register_modified: false
manifest_modified: false
baseline_modified: false
dependency_files_modified: 0
Dockerfiles_modified: 0
Compose_files_modified: 0
frontend_files_modified: 0
Graphify_modified: false
staged_files: 0
```

Created candidate:

```text
0_architecture/governance/agent_platform_hermes_0_19_openai_codex_single_worker_controlled_gate_post_commit_integrity_closure.md
```

No modification-register row is required for P15.7R.

## Residual Constraints

```yaml
worker_process_reuse: disabled
multi_request_workers: disabled
concurrent_workers: disabled
automatic_retry: disabled
manual_resubmission_execution: absent
credential_refresh: unexercised
credential_rotation: prohibited
fallback: prohibited
tools: disabled
MCP: disabled
persistent_accounting_store: absent
persistent_failure_store: absent
long_running_worker_service: absent
unattended_24_7_operation: unavailable
second_attempt_exact_dispatch_count: unknown
VPS: deferred
production_readiness: not_claimed
```

## P15.R Handoff

After P15.7R is reviewed, staged by the human, committed and pushed, P15.R - Secure Provider and Worker Enablement Closure may reconcile P15.0 through P15.7R.

P15.R must not require another live provider request, require OAuth, require credential refresh, require a VPS, enable retries, enable fallback, enable tools or MCP, or claim production readiness.

## Final Verdict

`hermes_0_19_openai_codex_single_worker_controlled_gate_post_commit_integrity_closed_with_constraints`
