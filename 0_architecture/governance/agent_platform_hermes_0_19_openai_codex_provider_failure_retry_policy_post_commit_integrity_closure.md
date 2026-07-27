# AGENT PLATFORM Hermes 0.19 OpenAI Codex Provider Failure Retry Policy Post-Commit Integrity Closure

Status: P15.6R provider failure and retry policy post-commit integrity closure.

Final verdict: `hermes_0_19_openai_codex_provider_failure_retry_policy_post_commit_integrity_closed_with_constraints`.

Verdict meaning: the committed P15.6 provider failure and retry policy is exact, synchronized with the remote branch, internally reconciled, validated against committed product identity, and regression-tested after commit. Automatic retry, fallback and credential rotation remain disabled. P15.7 becomes unblocked only after this P15.6R record is reviewed, committed and pushed.

This verdict does not mean a controlled worker has executed, a live failure has been injected, a provider request has been retried, a credential has been refreshed, manual resubmission is implemented, runtime accounting/failure persistence is implemented or production readiness is established.

## Repository State

| Gate | Result |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Local HEAD | `4250c1c5d40663e40b2529efd0927b0c28f561f9` |
| Remote HEAD | `4250c1c5d40663e40b2529efd0927b0c28f561f9` |
| HEAD equals remote | `true` |
| Resolved P15.6 commit | `4250c1c5d40663e40b2529efd0927b0c28f561f9` |
| P15.6 parent | `89809119b577057e4169e582ed3ab9d49b9b40a0` |
| P15.6 commit message | `P15.6 Add provider failure and retry policy` |
| P15.6 verdict | `hermes_0_19_openai_codex_provider_failure_retry_policy_ready_with_constraints` |
| Pre-record worktree and index | clean |

## P15.6 Commit Path Set

The committed P15.6 path set contains exactly 11 paths: 9 additions and 2 modified TSV files.

| Status | Path |
| --- | --- |
| Added | `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_failure_retry_policy.md` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv` |
| Modified | `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` |
| Added | `2_products/pepper-agent/docs/agent-platform/provider_failure_retry_policy.md` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/__init__.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/contracts.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/enums.py` |
| Added | `2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/policy.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_failure_classification.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_failure_policy_contracts.py` |
| Added | `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_retry_policy.py` |

Commit-path summary:

```yaml
commit_files: 11
created_files: 9
modified_files: 2
unexpected_commit_paths: 0
package_files: 4
test_files: 3
documentation_files: 1
governance_files: 1
```

## P15.5R Prerequisite

P15.5R prerequisite record: `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_usage_cost_timeout_accounting_post_commit_integrity_closure.md`.

P15.5R commit: `89809119b577057e4169e582ed3ab9d49b9b40a0`.

P15.5R is parent of P15.6: `true`.

P15.5R verdict: `hermes_0_19_openai_codex_usage_cost_timeout_accounting_post_commit_integrity_closed_with_constraints`.

Accounting policy authority:

```yaml
accounting_policy_id: accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
provider_calls_per_record_maximum: 1
raw_provider_response_allowed: false
provider_headers_allowed: false
credential_metadata_allowed: false
```

## Governance Summary Reconciliation

The committed P15.6 governance record contains a non-authoritative package summary that lists `__init__.py`, `contracts.py` and `policy.py` but omits `enums.py`. Durable authorities prove the four-file package.

```yaml
classification: governance_summary_omission_non_authoritative
omitted_summary_path: hermes_cli/agent_platform/provider_failure_policy/enums.py
committed_path_present: true
modification_register_row_present: true
import_manifest_row_present: true
committed_hash_valid: true
public_API_uses_enums: true
repository_defect: false
product_correction_required: false
P15_6_governance_rewrite_required: false
```

The committed P15.6 path set, modification register, import manifest, committed tree and public API all include `provider_failure_policy/enums.py`. No product or governance correction is required.

## Candidate Integrity

Pre-P15.6 committed candidate identity:

```yaml
files: 6776
bytes: 149294378
SHA256: 38545fecd8dbf5c8823c4efec47d0c9dca4e5cc0666a72283f9797ded5d2fd08
```

Post-P15.6 committed candidate identity:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6784
bytes: 149411321
SHA256: d655fec6b50ddccc36a7fcd061bbafb8d0752bfde55954993e6ca1fcd19146dc
candidate_file_delta: 8
candidate_bytes_greater_than_pre_P15_6: true
candidate_SHA_changed: true
```

The committed candidate delta is exactly the eight product-local P15.6 additions.

## Payload And Baseline

Payload identity is unchanged:

```yaml
algorithm: agent-platform-git-tree-sha256-v2
files: 6681
bytes: 145409792
SHA256: 1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c
payload_file_delta: 0
payload_byte_delta: 0
payload_SHA_changed: false
```

Baseline identity is unchanged:

```yaml
path: 2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
algorithm: sha256-git-blob-v1
bytes: 38693
SHA256: fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030
upstream_version: 0.19.0
upstream_commit: 3ef6bbd201263d354fd83ec55b3c306ded2eb72a
baseline_modified_by_P15_6: false
dependency_inventory_changed: false
source_integrity_changed: false
```

Governance integrity tests: `14 passed`.

## Modification Register Closure

P15.6 modification-register rows are valid:

```yaml
P15_6_rows: 8
required_IDs:
  - P15.6-001
  - P15.6-002
  - P15.6-003
  - P15.6-004
  - P15.6-005
  - P15.6-006
  - P15.6-007
  - P15.6-008
duplicate_modification_IDs: 0
owner_ticket: P15.6
change_class: AGENT_PLATFORM_product_addition
baseline_upstream_commit: 3ef6bbd201263d354fd83ec55b3c306ded2eb72a
baseline_source_object: none
baseline_source_SHA256: none
conflict_owner: AGENT_PLATFORM_provider_failure_policy_owner
mixed_conflict_owners: 0
upstream_disposition: retain_product_divergence
rollback_target: delete_path
status: implemented_pending_human_approval
path_present_in_HEAD: true
current_product_SHA256_equals_committed_blob_SHA256: true
```

## Import Manifest Closure

P15.6 import-manifest rows are valid:

```yaml
P15_6_rows: 8
classification: AGENT_PLATFORM_product_addition
duplicate_destination_paths: 0
committed_destination_present: true
committed_SHA256_matches: true
included_in_upstream_payload: false
existing_non_P15_6_rows_modified: 0
```

No P15.6 row uses `included_byte_exact`, `included_canonical_text_lf` or `transformed_by_canonical_compliance_rule`.

## Failure Policy Public Boundary

Committed package: `2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy`.

Required files present: `__init__.py`, `enums.py`, `contracts.py`, `policy.py`.

Capabilities present:

```yaml
failure_policy_identity: present
failure_categories: present
failure_stages: present
failure_origins: present
retry_dispositions: present
recovery_actions: present
synthetic_failure_signal: present
failure_record: present
retry_decision: present
deterministic_failure_ID: present
classifier: present
safe_summary: present
failure_to_accounting_projection: present
failure_accounting_link_validator: present
cleanup_projection: present
```

Operational absences:

```yaml
provider_client: absent
network_client: absent
credential_access: absent
retry_execution: absent
fallback_execution: absent
sleep: absent
persistence: absent
process_execution: absent
```

## Fixed Policy Closure

```yaml
schema_version: 1
policy_id: failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
provider_runtime_profile_id: provider.openai-codex.chatgpt-oauth.gpt-5.5.v1
worker_profile_id: worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
accounting_policy_id: accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
automatic_retry_allowed: false
maximum_automatic_retries: 0
same_request_retry_allowed: false
same_worker_retry_allowed: false
same_request_ID_reuse_allowed: false
same_usage_record_ID_reuse_allowed: false
credential_rotation_allowed: false
automatic_refresh_allowed: false
model_fallback_allowed: false
endpoint_fallback_allowed: false
maximum_provider_dispatches: 1
```

No committed policy path permits automatic retry, same-request retry, same-worker retry, credential rotation, automatic refresh or fallback.

## Taxonomy Closure

Categories:

```text
authentication
credential_expired
entitlement
quota
rate_limit
provider_overloaded
provider_server_error
connection_failure
connection_timeout
response_header_timeout
complete_inference_timeout
cancellation_timeout
worker_shutdown_timeout
tls_verification
transport_protocol
request_invalid
request_too_large
context_overflow
model_unavailable
content_policy
provider_incomplete
provider_failed
stream_truncated
cancelled_by_owner
accounting_invalid
unknown
```

Stages:

```text
preflight
credential
connection
response_header
stream
terminal
cancellation
shutdown
accounting
```

Origins:

```text
local_validation
SDK_exception
HTTP_response
SSE_error
terminal_event
owner_cancellation
accounting_validation
```

Category-stage separation is true. Generic `retryable`, `temporary` and `other` categories are absent.

## Classification Precedence Closure

Precedence:

```text
1. owner cancellation
2. accounting integrity
3. explicit timeout stage
4. TLS verification
5. credential-expired structured evidence
6. HTTP/provider code
7. terminal state
8. stream truncation
9. unknown
```

Required examples:

```yaml
HTTP_401_plus_token_expired: credential_expired
HTTP_429_plus_quota_exhausted: quota
HTTP_429_without_quota_evidence: rate_limit
HTTP_400_plus_Stream_must_be_set_to_true: transport_protocol
unknown_signal: unknown
unknown_fail_closed: true
```

## Generic Runtime Retry Boundary

Observed helper: `agent.codex_runtime.run_codex_stream`.

```yaml
generic_transport_retry_budget: 1
governed_worker_authority: false
modified_by_P15_6: false
generic_helper_use_for_P15_7: prohibited
generic_retry_loop_use_for_P15_7: prohibited
single_dispatch_seam: required
SDK_max_retries: 0
provider_dispatches_maximum: 1
```

P15.6R did not modify the generic helper.

## Historical Transport Failure Closure

```yaml
HTTP_status: 400
safe_message: Stream must be set to true
category: transport_protocol
stage: dispatch
recovery: correct_transport
retry_disposition: new_request_after_configuration_change
automatic_retry: false
```

Historical interpretation: P15.M11 consumed its one dispatch. P15.M11A was a separately authorized new request. It was not an automatic retry.

## Failure Handling Closure

Authentication maps to category `authentication`, recovery `reauthenticate` and retry disposition `new_request_after_human_action`.

Credential expiry maps to category `credential_expired`, recovery `reauthenticate` and retry disposition `new_request_after_human_action`.

Authorization maps to category `authorization`, recovery `review_authorization` and retry disposition `new_request_after_human_action`.

Entitlement maps to category `entitlement`, recovery `review_entitlement` and retry disposition `new_request_after_external_condition`.

Quota maps to category `quota`, recovery `wait_for_external_reset` and retry disposition `new_request_after_external_condition`.

Rate limit maps to category `rate_limit`, recovery `wait_for_external_reset` and retry disposition `new_request_after_external_condition`. Retry-after metadata is advisory only.

Provider overload maps to `provider_overloaded`. Provider server errors map to `provider_server_error`. Both require an external condition and never authorize automatic retry.

Timeout mappings use P15.5 stages: `connection`, `response_header`, `complete_inference`, `cancellation`, `worker_shutdown`.

Request invalid, request too large and context overflow require request or configuration changes. Model unavailable requires configuration change without fallback. Content policy failures preserve evidence and have disposition `never`.

Terminal incomplete and failed states map to `provider_incomplete` and `provider_failed`. Stream truncation maps to `stream_truncated`. Owner cancellation maps to `cancelled_by_owner`. Unknown failures fail closed with operator review required.

## Failure Record Closure

Failure records retain bounded safe fields only: deterministic failure record ID, request ID, runtime ID, correlation ID, fixed policy identities, category, stage, origin, provider dispatch occurred, provider dispatch count, accounting outcome, optional timeout stage, optional usage record ID, optional HTTP status, presence booleans, advisory retry-delay metadata and safe summary.

Raw provider message values are absent. Provider headers are absent. Provider response ID values are absent. Raw exceptions, raw provider responses, request content, response content, reasoning traces and credential metadata are absent.

Dispatch-count invariants:

```yaml
provider_dispatch_occurred_false:
  provider_dispatch_count: 0
  usage_record_id: null
provider_dispatch_occurred_true:
  provider_dispatch_count: 1
  usage_record_id: required
```

## Retry Decision Closure

Retry decisions always project:

```yaml
automatic_retry_allowed: false
automatic_retry_attempts: 0
same_request_retry_allowed: false
same_worker_retry_allowed: false
same_request_id_reuse_allowed: false
same_usage_record_id_reuse_allowed: false
credential_rotation_allowed: false
automatic_refresh_allowed: false
model_fallback_allowed: false
endpoint_fallback_allowed: false
delay_is_advisory_only: true
```

Manual resubmission is not automatic retry. Later resubmission requires a new request ID, new worker lifecycle, new usage record, new failure record on failure, new temporary credential lease when provider access is needed and explicit later execution authority. Manual resubmission execution is absent.

Credential rotation is prohibited. Fallback is prohibited.

## Accounting Integration Closure

Outcome projection:

```yaml
non_timeout_failure: failed
owner_cancellation: cancelled
timeout_failure: timed_out
```

Timeout stages: `connection`, `response_header`, `complete_inference`, `cancellation`, `worker_shutdown`.

Link dimensions:

```text
usage_record_id
request_id
runtime_id
correlation_id
accounting outcome
timeout stage
provider call count
```

Link behavior:

```yaml
matched: all dimensions match
missing: provider dispatch occurred and accounting is absent
mismatched: identity, outcome, timeout-stage or provider-call-count difference
pre_dispatch_without_accounting: matched_without_accounting
accounting_failure_triggers_provider_retry: false
```

## Cleanup Projection

```yaml
release_temporary_credential_lease: true_when_lease_exists
close_provider_stream: true_when_stream_exists
stop_owned_worker: true
remove_temporary_projected_HERMES_HOME: true_when_present
preserve_durable_credential: true
preserve_secret_free_accounting: true
preserve_secret_free_failure_record: true
preserve_partial_output: false
preserve_raw_provider_response: false
preserve_headers: false
```

The package projects cleanup metadata only. P15.7 owns runtime cleanup execution.

## Regression And Static Validation

| Gate | Result |
| --- | --- |
| P15.6 targeted failure-policy suite | `56 passed, 3 warnings` |
| P15.5 accounting regression | `19 passed, 3 warnings` |
| Prior provider/credential/worker regression | `119 passed, 3 warnings` |
| Governance integrity tests | `14 passed` |
| Ruff check on exact seven P15.6 Python files | passed |
| Ruff format check on exact seven P15.6 Python files | passed |
| `ty` availability | unavailable: `No module named ty`, no executable found |

Warnings are inherited P15.M8 Pydantic protected-namespace warnings for `model_id`, `model_policy` and `model_list_calls_per_request_maximum`. New P15.6 warnings: `0`. Warnings affecting closure: `0`.

Type check status: `not_run_tool_unavailable`. Type errors are not asserted. Dependency installation: `0`.

## Operational Authority Scan

Committed production source under `hermes_cli/agent_platform/provider_failure_policy` contains no forbidden operational authority.

```yaml
network_authority: 0
credential_authority: 0
persistence_authority: 0
process_authority: 0
retry_execution_authority: 0
fallback_execution_authority: 0
```

## Secret Safety

Secret-safety scan result for the eight P15.6 product additions, both TSV files, the P15.6 governance record and this P15.6R candidate:

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
raw_provider_messages_in_records: 0
provider_request_ID_values: 0
real_prompts: 0
real_outputs: 0
reasoning_traces: 0
private_keys: 0
```

Synthetic failure fixtures are classifier inputs only and are not retained as durable failure-record payloads.

## No-Execution Counters

```yaml
Docker: 0
OAuth: 0
credential_reads: 0
credential_writes: 0
credential_leases: 0
credential_rotations: 0
provider_dispatches: 0
automatic_retries: 0
manual_provider_resubmissions: 0
fallback_calls: 0
model_list_calls: 0
usage_API_calls: 0
quota_API_calls: 0
billing_API_calls: 0
worker_processes: 0
sleep_calls: 0
remote_hosts_contacted: 0
Graphify_commands: 0
```

## Repository Non-Mutation Closure

P15.6R created exactly one untracked governance candidate and modified no tracked file.

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
0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_failure_retry_policy_post_commit_integrity_closure.md
```

No modification-register row is required for P15.6R.

## P15.7 Handoff

After P15.6R is reviewed, staged by the human, committed and pushed, the next ticket is P15.7 - Single Worker Controlled Gate.

Required P15.7 runtime boundary:

```yaml
temporary_credential_leases: 1_maximum
workers: 1
requests: 1
provider_dispatches: 1_maximum
SDK_retries: 0
automatic_retries: 0
fallback: 0
credential_rotation: 0
generic_run_codex_stream: prohibited
single_dispatch_responses_create_stream_true: required
accounting_record: exactly_1
failure_record: 0_or_1
worker_result: exactly_1
mandatory_identity_linkage: true
cleanup: mandatory
```

P15.7 may require live provider execution. Its exact human-interaction and OAuth requirements must be determined from retained credential status when the ticket is issued.

## Residual Constraints

```yaml
live_failure_validation: not_performed
controlled_worker_execution: pending_P15_7
runtime_failure_record_creation: pending_P15_7
runtime_accounting_linkage: pending_P15_7
automatic_retry: disabled
manual_resubmission_execution: absent
credential_refresh: not_exercised
credential_rotation: prohibited
fallback: prohibited
provider_quota: unknown
future_entitlement: not_guaranteed
retry_after_accuracy: unverified
persistent_failure_store: absent
production_readiness: not_claimed
VPS_dependency: none
```
