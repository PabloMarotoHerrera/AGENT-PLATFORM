# AGENT PLATFORM Hermes 0.19 OpenAI Codex Provider Failure Retry Policy

Status: P15.6 provider failure and retry policy candidate for human review.

Final verdict: `hermes_0_19_openai_codex_provider_failure_retry_policy_ready_with_constraints`.

Verdict meaning: a fixed failure taxonomy, deterministic classifier, secret-free failure record, retry decision, safe summary catalog, cleanup projection, failure-to-accounting projection and failure-accounting link validator exist for the governed OpenAI Codex route. Automatic retry, credential rotation and fallback remain prohibited. This verdict does not claim P15.7 controlled worker execution, live provider recovery validation, usage or billing visibility, persistent failure storage, runtime failure linkage or production readiness.

## Ticket Authority

P15.6 is the original-roadmap owner for Provider Failure and Retry Policy.

Accepted predecessor chain:

```text
P15.0 Provider and Model Strategy
P15.1 Credential Delivery Boundary
P15.1A Windows Credential Store Protection Backend Correction retained for Windows fallback
P15.2 Provider Runtime Profile
P15.3 Bounded Worker Profile
P15.4 Tool-Free Inference Gate completed by replacement
P15.5 Usage, Cost and Timeout Accounting
P15.5R Usage, Cost and Timeout Accounting Post-Commit Integrity Closure
P15.6 Provider Failure and Retry Policy current ticket
```

## Repository And Branch State

| Gate | Result |
| --- | --- |
| Repository root | `C:/Users/pablo/OneDrive/Escritorio/AGENT-PLATFORM-P15M` |
| Branch | `p15.m-hermes-0.19-migration` |
| Local HEAD | `89809119b577057e4169e582ed3ab9d49b9b40a0` |
| Remote branch HEAD | `89809119b577057e4169e582ed3ab9d49b9b40a0` |
| HEAD equals remote | `true` |
| Pre-ticket worktree and index | clean |
| P15.5R commit | `89809119b577057e4169e582ed3ab9d49b9b40a0` |
| P15.5R commit message | `P15.5R Close accounting post-commit integrity` |
| P15.5R verdict | `hermes_0_19_openai_codex_usage_cost_timeout_accounting_post_commit_integrity_closed_with_constraints` |
| P15.5 commit | `777c9d02c6f6d347f36c473f6e11c2f727e6d5cf` |

## P15.5 Accounting Prerequisite

| Authority | Value |
| --- | --- |
| Accounting policy ID | `accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Provider calls per accounting record maximum | `1` |
| Usage record ID required on worker result | `true` |
| Timeout accounting | ready |
| Cost accounting | `subscription_included` |
| Raw provider response allowed | `false` |
| Provider headers allowed | `false` |
| Credential metadata allowed | `false` |

## Pre-Change Product Identity

The committed-HEAD integrity utility still reads committed `HEAD`; it does not include uncommitted P15.6 working-tree files.

| Identity | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6776` | `149294378` | `38545fecd8dbf5c8823c4efec47d0c9dca4e5cc0666a72283f9797ded5d2fd08` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Baseline record | not applicable | `38693` | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |

Governance integrity tests: `14 passed`.

The P15.6 working-tree candidate set is validated by exact path, tests, content hashes, register rows and import-manifest rows. The new committed Pepper candidate identity must be computed after human commit and push by P15.6R. Expected post-commit candidate file count is `6784`; bytes and SHA-256 are intentionally not predicted.

## Existing Provider And Worker Authority

| Field | Value |
| --- | --- |
| Provider profile | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Worker profile | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Provider | `openai-codex` |
| Authentication | `chatgpt_oauth` |
| Endpoint | `https://chatgpt.com/backend-api/codex` |
| Model | `gpt-5.5` |
| Transport | `codex_responses` |
| Automatic retry | disabled |
| Automatic fallback | disabled |
| Credential refresh calls per request maximum | `0` |
| Provider calls per request maximum | `1` |
| Model-list calls per request maximum | `0` |
| Requests per worker lifetime maximum | `1` |
| Concurrent workers maximum | `1` |

Timeout values:

| Timeout | Value |
| --- | ---: |
| Startup timeout | `30000` ms |
| Connection timeout | `10000` ms |
| Response-header timeout | `30000` ms |
| Complete-inference timeout | `120000` ms |
| Cancellation deadline | `10000` ms |
| Worker shutdown deadline | `15000` ms |
| Maximum worker lifetime | `180000` ms |

## Generic Runtime Retry Boundary

Observed generic helper: `agent.codex_runtime.run_codex_stream`.

Observed generic transport retry budget: `1`.

Governed worker authority: `false`.

The upstream-derived generic Hermes runtime may contain transport retry behavior for general interactive sessions. That helper is not authoritative for the governed Pepper single-request worker. The P15.7 governed worker must use a one-dispatch seam with SDK retries disabled and must not call a helper that can issue a second provider dispatch.

P15.7 boundary:

```yaml
run_codex_stream_direct_use: prohibited
generic_retry_loop_use: prohibited
single_dispatch_seam: required
SDK_max_retries: 0
provider_dispatches: 1_maximum
```

P15.6 did not modify `agent/codex_runtime.py` or `agent/error_classifier.py`.

## Failure-Policy Package

Created package:

```text
2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/
```

Package files:

```text
__init__.py
contracts.py
policy.py
```

Operational authority:

| Authority | Count |
| --- | ---: |
| Network authority | `0` |
| Credential authority | `0` |
| Persistence authority | `0` |
| Process authority | `0` |
| Retry execution authority | `0` |
| Fallback execution authority | `0` |
| Sleep or wall-clock waiting authority | `0` |
| Randomness or secret input authority | `0` |

## Policy Identity

```yaml
schema_version: 1
policy_id: failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
provider_runtime_profile_id: provider.openai-codex.chatgpt-oauth.gpt-5.5.v1
worker_profile_id: worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
accounting_policy_id: accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1
provider: openai-codex
authentication: chatgpt_oauth
model: gpt-5.5
endpoint: https://chatgpt.com/backend-api/codex
transport: codex_responses
automatic_retry_allowed: false
maximum_automatic_retries: 0
maximum_provider_dispatches_per_request: 1
same_worker_retry_allowed: false
same_request_retry_allowed: false
credential_rotation_allowed: false
automatic_fallback_allowed: false
model_fallback_allowed: false
endpoint_fallback_allowed: false
automatic_refresh_allowed: false
```

## Failure Categories

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

No generic `retryable`, `temporary`, `fatal` or `other` category was added. Retry disposition remains separate from category.

## Stages And Origins

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

Category and stage are distinct.

## Classification Precedence

```text
1. Owner cancellation
2. Accounting integrity failure
3. Explicit timeout stage
4. TLS certificate verification failure
5. Credential-expired structured signal
6. HTTP/provider-code classification
7. Terminal incomplete or failed state
8. Stream truncation
9. Unknown
```

Specific structured signals cannot be overridden by generic status handling. HTTP `401` plus `token_expired` classifies as `credential_expired`, not generic `authentication`.

## Authentication, Credential And Authorization Handling

Authentication maps to category `authentication`, recovery `reauthenticate` and retry disposition `new_request_after_human_action`.

Credential-expired maps to category `credential_expired`, recovery `reauthenticate` and retry disposition `new_request_after_human_action`.

Authorization maps to category `authorization`, recovery `review_authorization` and retry disposition `new_request_after_human_action`.

Automatic OAuth, automatic refresh, automatic retry and credential rotation remain `false`.

## Entitlement, Quota And Rate Limit Handling

Entitlement maps to category `entitlement`, recovery `review_entitlement` and retry disposition `new_request_after_external_condition`.

Quota maps to category `quota`, recovery `wait_for_external_reset` and retry disposition `new_request_after_external_condition`.

Rate limit maps to category `rate_limit`, recovery `wait_for_external_reset` and retry disposition `new_request_after_external_condition`.

Normalized `retry_after_ms` is retained only as advisory metadata. Raw retry-after headers are not retained. P15.6 performs no sleep, jitter, backoff execution or automatic resubmission.

Billing API calls, quota API calls, account-tier inspection and future entitlement claims: `0`.

## Provider, Transport And Timeout Handling

Provider overload maps to category `provider_overloaded`, recovery `wait_for_external_reset` and retry disposition `new_request_after_external_condition`.

Provider server errors map to category `provider_server_error`, recovery `wait_for_external_reset` and retry disposition `new_request_after_external_condition`.

Transport and timeout mappings:

| Signal | Category | Stage | Recovery | Retry disposition |
| --- | --- | --- | --- | --- |
| connect error | `connection_failure` | `connection` | `preserve_evidence_and_escalate` | `operator_review_required` |
| read timeout at connection | `connection_timeout` | `connection` | `preserve_evidence_and_escalate` | `operator_review_required` |
| read timeout before headers | `response_header_timeout` | `response_header` | `preserve_evidence_and_escalate` | `operator_review_required` |
| read timeout during stream | `complete_inference_timeout` | `stream` | `preserve_evidence_and_escalate` | `operator_review_required` |
| cancellation timeout | `cancellation_timeout` | `cancellation` | `preserve_evidence_and_escalate` | `operator_review_required` |
| worker shutdown timeout | `worker_shutdown_timeout` | `shutdown` | `preserve_evidence_and_escalate` | `operator_review_required` |
| remote protocol error | `transport_protocol` | `dispatch` | `correct_transport` | `new_request_after_configuration_change` |
| TLS verification error | `tls_verification` | `connection` | `correct_configuration` | `new_request_after_configuration_change` |

Historical `stream=true` mapping:

```yaml
HTTP_status: 400
message: Stream must be set to true
category: transport_protocol
stage: dispatch
recovery: correct_transport
retry_disposition: new_request_after_configuration_change
```

The failed P15.M11 dispatch consumed its single-call authority. P15.M11A was a new explicitly authorized request, not an automatic retry.

## Request, Model, Terminal And Unknown Handling

Invalid request maps to `request_invalid`, recovery `correct_configuration` and disposition `new_request_after_request_change`.

Request too large maps to `request_too_large`, recovery `reduce_request` and disposition `new_request_after_request_change`.

Context overflow maps to `context_overflow`, recovery `reduce_request` and disposition `new_request_after_request_change`; P15.6 does not compress context, modify messages, strip content or issue a second request.

Model unavailable maps to `model_unavailable`, recovery `review_entitlement` and disposition `new_request_after_configuration_change`; fallback remains false and the fixed model remains `gpt-5.5`.

Content policy maps to `content_policy`, recovery `preserve_evidence_and_escalate` and disposition `never`. Rejected prompt content is not retained.

Provider incomplete maps to `provider_incomplete`, stage `terminal`, accounting outcome `failed` and disposition `operator_review_required`.

Provider failed maps to `provider_failed`, stage `terminal`, accounting outcome `failed` and disposition `operator_review_required`.

Stream truncated maps to `stream_truncated`, stage `stream`, accounting outcome `failed` and disposition `operator_review_required`.

Owner cancellation maps to `cancelled_by_owner`, stage `cancellation`, accounting outcome `cancelled`, recovery `cancel_and_cleanup` and disposition `never`.

Accounting integrity failure maps to `accounting_invalid`, stage `accounting`, accounting outcome `failed`, recovery `preserve_evidence_and_escalate` and disposition `never`. Accounting failures never trigger provider retry.

Unknown maps to `unknown`, recovery `preserve_evidence_and_escalate` and disposition `operator_review_required`. Unknown fails closed.

## Failure Record Contract

Failure records are immutable and include only bounded safe fields: failure record ID, request ID, runtime ID, correlation ID, fixed provider and policy identities, category, stage, origin, dispatch occurred, dispatch count, accounting outcome, optional timeout stage, optional usage record ID, optional HTTP status, presence booleans, advisory retry delay metadata and a safe summary.

Retained fields:

| Raw evidence | Retained |
| --- | --- |
| Provider response ID value | `false` |
| Provider error code value | `false` |
| Provider message value | `false` |
| Raw exception | `false` |
| Raw provider response | `false` |
| Provider headers | `false` |
| Request content | `false` |
| Response content | `false` |
| Reasoning trace | `false` |
| Credential metadata | `false` |

Dispatch invariants:

```yaml
provider_dispatch_occurred_false:
  provider_dispatch_count: 0
  usage_record_id: null
provider_dispatch_occurred_true:
  provider_dispatch_count: 1
  usage_record_id: required
```

## Deterministic Failure ID

Canonical byte stream:

```text
runtime_id
NUL
correlation_id
NUL
request_id
NUL
failure_category
```

Algorithm: SHA-256. Prefix: `failure-`. Digest length: 24 lowercase hexadecimal characters. Random input, timestamp input, secret input, provider message input and provider response input are all absent.

## Retry Decision Contract

Retry decisions are immutable and always preserve:

```yaml
automatic_retry_allowed: false
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

Every disposition other than `never` requires a new request, new worker lifecycle, new usage record and new credential lease when provider access is required.

Manual resubmission metadata is supported. Manual resubmission execution is absent and requires a later explicit execution authority.

## No Credential Rotation And No Fallback

Current governed credential store: `openai-codex.primary`. Credential count: `1`. Maximum active leases: `1`.

Credential rotation, pool failover, alternate credential selection, local Codex CLI import and VS Code credential import are prohibited. P15.6 does not clear durable credentials.

Fallback model, provider and endpoint remain null. Automatic fallback after rate limit, entitlement, server error or timeout is false.

## Failure-To-Accounting Projection

Projection returns safe metadata only and does not create or mutate P15.5 accounting records.

Mappings:

| Category group | Accounting outcome |
| --- | --- |
| Authentication, authorization, credential, entitlement, quota, rate-limit, provider, transport, request, model, content, terminal, stream, unknown and accounting-invalid failures | `failed` |
| Owner cancellation | `cancelled` |
| Connection, response-header, complete-inference, cancellation and worker-shutdown timeouts | `timed_out` |

Timeout stage mapping follows P15.5 stages: `connection`, `response_header`, `complete_inference`, `cancellation`, `worker_shutdown`.

## Failure-Accounting Linkage

The link validator compares:

```text
usage_record_id
request_id
runtime_id
correlation_id
accounting outcome
provider call count
```

Link states are `matched`, `matched_without_accounting`, `missing` and `mismatched`.

Provider dispatch with absent accounting returns `missing`. Pre-dispatch failure with absent accounting returns `matched_without_accounting`. Identity, outcome, timeout-stage or provider-call-count differences return `mismatched`.

## Safe Summaries

Safe summaries are catalogued and do not include raw provider messages, prompt excerpts, response excerpts, credential details or account identity. Examples include `Provider authentication failed.`, `The governed provider credential is expired.`, `The provider rate limit was reached.` and `The provider request failed for an unclassified reason.`

## Cleanup Projection

Retry decisions project cleanup flags only; they do not execute cleanup.

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

## Public API

The package root exposes schema version, failure-policy constants, public enums, failure policy contract, synthetic failure signal contract, classification result contract, failure record contract, retry decision contract, failure-accounting projection contract, failure-accounting link contract, deterministic failure-record ID helper, OpenAI Codex failure classifier, failure-record builder, retry-decision builder, failure-to-accounting projection, failure-accounting link validator and safe-summary resolver.

It does not expose raw pattern tables, internal normalization helpers, network exception adapters, credential helpers, runtime clients, sleep helpers, fallback helpers or generic Hermes failover internals.

## Validation Evidence

| Gate | Command summary | Result |
| --- | --- | --- |
| Isolated P15.6 suites | `python -m pytest -q` on the three P15.6 test files with `-p no:cacheprovider` | `56 passed, 3 warnings` |
| P15.5 accounting regression | `python -m pytest -q` on the three accounting test files with `-p no:cacheprovider` | `19 passed, 3 warnings` |
| Prior provider/credential/worker regression | `python -m pytest -q` on the 12-file provider regression inventory with `-p no:cacheprovider` | `119 passed, 3 warnings` |
| Ruff check | `python -m ruff check` on the seven P15.6 Python files | passed |
| Ruff format check | `python -m ruff format --check` on the seven P15.6 Python files | passed after scoped formatting of three authorized P15.6 files |
| Ty availability | `python -m ty check` and `where ty` | unavailable: `No module named ty`, no executable found |

Warning classification: all three warnings are inherited P15.M8 Pydantic protected-namespace warnings for `model_id`, `model_policy` and `model_list_calls_per_request_maximum`. New P15.6 warnings: `0`. Security, credential, network and unhandled resource warnings: `0`.

Dependency installation: `0`.

## Modification Register Rows

P15.6 appended exactly eight modification-register rows: `P15.6-001` through `P15.6-008`.

```yaml
P15_6_rows: 8
conflict_owner: AGENT_PLATFORM_provider_failure_policy_owner
mixed_P15_6_conflict_owners: 0
duplicate_modification_IDs: 0
duplicate_P15_6_paths: 0
committed_or_working_tree_SHA256_matches: true
all_other_required_row_fields: unchanged_and_valid
```

## Import Manifest Rows

P15.6 appended exactly eight import-manifest rows with `canonical_rule=P15_6_PRODUCT_ADDITION`.

```yaml
P15_6_rows: 8
classification: AGENT_PLATFORM_product_addition
payload_inclusion: false
upstream_source: not_applicable
duplicate_P15_6_destination_paths: 0
destination_SHA256_matches: true
```

## Secret Safety

Candidate files retain no access tokens, refresh tokens, authorization headers, device codes, OAuth verification URLs, account identifiers, JWT claims, credential file contents, raw provider responses, raw provider headers, raw provider messages in records, provider request ID values, real prompts, real outputs, reasoning traces, browser cookies or private keys.

Synthetic error messages in tests are classifier inputs only and are not projected into durable failure records.

## No-Execution Counters

| Counter | Value |
| --- | ---: |
| Docker containers started | `0` |
| Docker networks created | `0` |
| Docker images built | `0` |
| OAuth attempts | `0` |
| Credential reads | `0` |
| Credential writes | `0` |
| Credential promotions | `0` |
| Credential refreshes | `0` |
| Credential leases | `0` |
| Credential rotations | `0` |
| Provider dispatches | `0` |
| Automatic retries | `0` |
| Manual provider resubmissions | `0` |
| Fallback calls | `0` |
| Model-list calls | `0` |
| Usage API calls | `0` |
| Quota API calls | `0` |
| Billing API calls | `0` |
| Worker processes | `0` |
| Sleep calls | `0` |
| Tool calls | `0` |
| MCP calls | `0` |
| Remote hosts contacted | `0` |
| Graphify commands | `0` |

## Exact Candidate Set

Authorized creations:

```text
2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/__init__.py
2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/enums.py
2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/contracts.py
2_products/pepper-agent/hermes_cli/agent_platform/provider_failure_policy/policy.py
2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_failure_policy_contracts.py
2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_failure_classification.py
2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_retry_policy.py
2_products/pepper-agent/docs/agent-platform/provider_failure_retry_policy.md
0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_failure_retry_policy.md
```

Authorized modifications:

```text
2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv
```

Expected final working-tree candidate state:

```yaml
candidate_files: 11
created_files: 9
modified_files: 2
unexpected_candidates: 0
existing_product_source_files_modified: 0
existing_tests_modified: 0
provider_runtime_modified: false
provider_worker_modified: false
provider_accounting_modified: false
generic_error_classifier_modified: false
Codex_runtime_modified: false
credential_files_modified: 0
baseline_record_modified: false
dependency_files_modified: 0
Dockerfiles_modified: 0
Compose_files_modified: 0
frontend_files_modified: 0
Graphify_modified: false
```

## P15.6R Handoff

After human review, staging, commit and push, P15.6R must resolve the P15.6 commit, verify the exact 11-file commit path set, compute the new committed candidate identity, confirm committed candidate file count `6784`, confirm payload and baseline identities unchanged, validate `P15.6-001` through `P15.6-008`, validate eight import-manifest rows, rerun P15.6 targeted tests, rerun P15.5 accounting regression, rerun the prior 119-test provider regression and create one governance-only closure record.

P15.7 remains blocked until P15.6R is committed and pushed.

## P15.7 Sequencing

P15.7 owns controlled worker lifecycle, one temporary credential lease, one request, one provider dispatch maximum, one accounting record, one failure record when applicable, one worker result, mandatory identity linkage, runtime failure classification, runtime cleanup, no automatic retry, no fallback, no credential rotation, and bounded success and failure evidence.

Required P15.7 seam:

```yaml
generic_run_codex_stream_retry_loop: prohibited
single_dispatch_Responses_create_stream_true: required
SDK_max_retries: 0
provider_dispatches: 1_maximum
```

## Residual Constraints

```yaml
live_failure_validation: not_performed
runtime_retry_execution: absent
manual_resubmission_execution: absent
credential_refresh: not_exercised
credential_rotation: prohibited
fallback: prohibited
provider_quota: unknown
account_entitlement_future: not_guaranteed
retry_after_accuracy: provider_dependent_and_unverified
persistent_failure_store: absent
runtime_failure_linkage: pending_P15_7
controlled_worker_gate: pending_P15_7
production_readiness: not_claimed
VPS_dependency: none
```
