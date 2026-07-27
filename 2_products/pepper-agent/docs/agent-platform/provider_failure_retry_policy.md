# Provider Failure and Retry Policy

P15.6 defines deterministic, secret-free failure classification and retry policy for the governed OpenAI Codex ChatGPT OAuth route.

## Ticket Authority

P15.6 owns Provider Failure and Retry Policy after P15.5 usage, cost and timeout accounting and P15.5R post-commit integrity closure.

The P15.6 verdict means the failure taxonomy, classification, retry decision, failure-to-accounting projection and failure-accounting link validation are ready with constraints. It does not authorize live provider execution, credential access, retry execution, fallback, credential rotation, persistent storage or production activation.

## Fixed Identity

| Field | Value |
| --- | --- |
| Provider | `openai-codex` |
| Authentication | `chatgpt_oauth` |
| Endpoint | `https://chatgpt.com/backend-api/codex` |
| Model | `gpt-5.5` |
| Transport | `codex_responses` |
| Provider profile | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Worker profile | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Accounting policy | `accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Failure policy | `failure.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |

The fixed execution posture remains:

- automatic retry disabled;
- automatic fallback disabled;
- credential rotation disabled;
- provider calls per request maximum `1`;
- requests per worker lifetime maximum `1`;
- concurrent workers maximum `1`.

## Relationship To P15.5 Accounting

P15.6 does not create or mutate P15.5 accounting records. It projects safe metadata that P15.7 can use when it creates a controlled worker result and accounting record.

Timeout failures map to P15.5 timeout stages:

| Failure category | Accounting outcome | Accounting timeout stage |
| --- | --- | --- |
| `connection_timeout` | `timed_out` | `connection` |
| `response_header_timeout` | `timed_out` | `response_header` |
| `complete_inference_timeout` | `timed_out` | `complete_inference` |
| `cancellation_timeout` | `timed_out` | `cancellation` |
| `worker_shutdown_timeout` | `timed_out` | `worker_shutdown` |

Owner cancellation maps to `cancelled`. All non-timeout non-cancellation failures map to `failed`.

## Failure Categories

The exact failure categories are:

```text
authentication
authorization
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

Retryability is not a category. It is represented by retry disposition.

## Lifecycle Stages

The exact stages are:

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

Category and stage are distinct. For example, `connection_timeout` has stage `connection`.

## Evidence Origins

The exact origins are:

```text
local_validation
SDK_exception
HTTP_response
SSE_error
terminal_event
owner_cancellation
accounting_validation
```

Origin describes where the bounded synthetic signal arrived from. Origin does not imply retryability.

## Classification Precedence

Classification is deterministic and precedence-ordered:

1. Owner cancellation.
2. Accounting integrity failure.
3. Explicit timeout stage.
4. TLS certificate verification failure.
5. Credential-expired structured signal.
6. HTTP/provider-code classification.
7. Terminal incomplete or failed state.
8. Stream truncation.
9. Unknown.

A specific structured signal wins over a generic status. For example, HTTP `401` plus `token_expired` is `credential_expired`, not generic `authentication`.

## Authentication And Credential Failures

Authentication signals such as HTTP `401`, invalid authentication, invalid access token and missing bearer credential map to:

- category `authentication`;
- recovery `reauthenticate`;
- retry disposition `new_request_after_human_action`.

Credential-expired signals such as `token_expired`, `access_token_expired` and explicit expired credential text map to:

- category `credential_expired`;
- recovery `reauthenticate`;
- retry disposition `new_request_after_human_action`.

Authorization signals such as HTTP `403` without entitlement evidence, forbidden and access denied map to:

- category `authorization`;
- recovery `review_authorization`;
- retry disposition `new_request_after_human_action`.

P15.6 performs no OAuth, automatic refresh, credential rotation or automatic retry.

## Entitlement, Quota And Rate Limits

Entitlement signals such as model not included in plan, model not available for account, plan does not include model, account not entitled and subscription does not permit model map to:

- category `entitlement`;
- recovery `review_entitlement`;
- retry disposition `new_request_after_external_condition`.

Quota signals such as `insufficient_quota`, usage allocation exhausted, account quota exhausted and credit or subscription capacity exhausted map to:

- category `quota`;
- recovery `wait_for_external_reset`;
- retry disposition `new_request_after_external_condition`.

Rate-limit signals such as HTTP `429`, `rate_limit`, too many requests, retry after and throttled map to:

- category `rate_limit`;
- recovery `wait_for_external_reset`;
- retry disposition `new_request_after_external_condition`.

Caller-supplied normalized `retry_after_ms` may be retained as advisory metadata up to `86400000` ms. P15.6 does not retain raw headers, calculate wall-clock retry timestamps, sleep or resubmit.

P15.6 performs no billing API calls, quota API calls or account-tier inspection.

## Provider And Transport Failures

Provider overload signals such as HTTP `503`, HTTP `529`, overloaded, at capacity and temporarily overloaded map to `provider_overloaded` with recovery `wait_for_external_reset`.

Provider server errors HTTP `500`, HTTP `502` and HTTP `504` without more specific timeout-stage evidence map to `provider_server_error` with recovery `wait_for_external_reset`.

Transport mappings:

| Signal | Category | Stage | Recovery | Retry disposition |
| --- | --- | --- | --- | --- |
| connect error | `connection_failure` | `connection` | `preserve_evidence_and_escalate` | `operator_review_required` |
| read timeout at connection | `connection_timeout` | `connection` | `preserve_evidence_and_escalate` | `operator_review_required` |
| read timeout before headers | `response_header_timeout` | `response_header` | `preserve_evidence_and_escalate` | `operator_review_required` |
| read timeout during stream | `complete_inference_timeout` | `stream` | `preserve_evidence_and_escalate` | `operator_review_required` |
| remote protocol error | `transport_protocol` | `dispatch` | `correct_transport` | `new_request_after_configuration_change` |
| TLS verification error | `tls_verification` | `connection` | `correct_configuration` | `new_request_after_configuration_change` |

The historical HTTP `400` failure `Stream must be set to true` maps to:

- category `transport_protocol`;
- stage `dispatch`;
- recovery `correct_transport`;
- retry disposition `new_request_after_configuration_change`.

The failed P15.M11 dispatch consumed its single-call authority. P15.M11A was a new explicitly authorized request, not an automatic retry.

## Request And Terminal Failures

Invalid HTTP `400` requests map to `request_invalid` with recovery `correct_configuration` and disposition `new_request_after_request_change`.

HTTP `413` maps to `request_too_large` with recovery `reduce_request` and disposition `new_request_after_request_change`.

Context overflow signals such as context length, context window, too many tokens, prompt too long and maximum context map to `context_overflow` with recovery `reduce_request`. P15.6 does not compress context, modify messages, strip content or issue a second request.

HTTP `404`, `model_not_found`, unknown model and unsupported model map to `model_unavailable`. The fixed model remains `gpt-5.5`; P15.6 does not select another model.

Content-policy signals map to `content_policy`, recovery `preserve_evidence_and_escalate` and disposition `never`. Rejected prompt content is not retained.

Terminal and stream failures:

| Signal | Category | Stage | Accounting outcome | Retry disposition |
| --- | --- | --- | --- | --- |
| `response.incomplete` | `provider_incomplete` | `terminal` | `failed` | `operator_review_required` |
| `response.failed` | `provider_failed` | `terminal` | `failed` | `operator_review_required` |
| stream ended without terminal event | `stream_truncated` | `stream` | `failed` | `operator_review_required` |

Partial output is not retained in failure records.

Owner cancellation maps to `cancelled_by_owner`, stage `cancellation`, accounting outcome `cancelled`, recovery `cancel_and_cleanup` and disposition `never`.

Accounting integrity failures such as missing mandatory usage-record link, mismatched request identity, runtime identity, correlation identity or provider-dispatch count map to `accounting_invalid`. They never trigger another provider call.

Unknown failures map to `unknown`, recovery `preserve_evidence_and_escalate` and disposition `operator_review_required`. Unknown failures fail closed and are not retryable by default.

## Failure Records And Safe Summaries

Failure records preserve only bounded, catalogued metadata:

- deterministic failure record ID;
- request, runtime and correlation IDs;
- fixed provider, worker and accounting policy IDs;
- category, stage and origin;
- provider dispatch occurred and dispatch count;
- accounting outcome and optional timeout stage;
- optional usage record ID when dispatch occurred;
- optional HTTP status;
- presence booleans for provider response ID, provider error code and provider message;
- advisory retry delay metadata;
- safe summary.

Failure records explicitly retain no provider response ID value, provider error code value, provider message value, raw exception, raw provider response, headers, request content, response content, reasoning trace or credential metadata.

Safe summaries are catalogued strings such as:

- `Provider authentication failed.`
- `The governed provider credential is expired.`
- `The configured model is not currently available to this account.`
- `Provider usage capacity is unavailable.`
- `The provider rate limit was reached.`
- `The provider is temporarily overloaded.`
- `The provider request did not satisfy the required transport protocol.`
- `The request exceeds the governed context boundary.`
- `The provider rejected the request under its content policy.`
- `The provider request failed for an unclassified reason.`

Raw provider messages, prompt excerpts, response excerpts, credential details and account identity are not included in summaries.

## Deterministic Failure ID

The failure-record ID uses:

```text
runtime_id
NUL
correlation_id
NUL
request_id
NUL
failure_category
```

The ID is `failure-` plus the first 24 lowercase hexadecimal characters of a SHA-256 digest. It uses no random input, timestamp input, secret input, provider message input or provider response input.

## Retry Decision

P15.6 retry decisions always enforce:

- automatic retry false;
- automatic retry attempts zero;
- same request retry false;
- same worker retry false;
- same request ID reuse false;
- same usage-record ID reuse false;
- credential rotation false;
- automatic refresh false;
- model fallback false;
- endpoint fallback false.

Manual resubmission is not automatic retry. Automatic retry means the same governed work request issues another provider dispatch without a new authorization boundary. Manual or separately governed resubmission means a new request is created after human, external, configuration or request-change conditions have been satisfied.

Every disposition other than `never` requires a new request ID, new worker lifecycle, new usage record, new temporary credential lease when provider access is required, and later execution authority. P15.6 records metadata only; it does not execute resubmission.

## No Credential Rotation

The governed credential store remains `openai-codex.primary` with credential count `1` and maximum active leases `1`.

Credential rotation, pool failover, alternate credential selection, local Codex CLI import and VS Code credential import are prohibited. Authentication failure recovery is stop, clean temporary lease when one exists, preserve durable credential, and require human review or reauthentication. P15.6 does not clear credentials.

## No Fallback

Fallback provider, model and endpoint remain null. Automatic fallback after rate limit, entitlement, server error or timeout is false. Changing the model or provider requires a separate strategy ticket.

## Cleanup Projection

P15.6 projects cleanup requirements only. It does not perform cleanup.

Required cleanup flags include:

- release temporary credential lease when one exists;
- close provider stream when one exists;
- stop owned worker;
- remove temporary projected `HERMES_HOME` when present;
- preserve durable credential;
- preserve secret-free accounting;
- preserve secret-free failure record;
- preserve partial output false;
- preserve raw provider response false;
- preserve headers false.

P15.7 owns runtime execution of cleanup.

## Generic Hermes Runtime Retry Boundary

The upstream-derived generic Hermes helper `agent.codex_runtime.run_codex_stream` currently has a transport retry budget of `1` for general interactive sessions. It is not authoritative for the governed Pepper single-request worker.

The P15.7 governed worker must not call a helper that can issue a second provider dispatch. The required P15.7 seam is a single-dispatch Responses create call with stream enabled, SDK retries disabled and provider dispatches capped at one.

P15.6 does not modify `agent/codex_runtime.py` or `agent/error_classifier.py`.

## P15.7 Handoff

P15.7 owns controlled worker lifecycle, one temporary credential lease, one request, one provider dispatch maximum, one accounting record, one failure record when applicable, one worker result, mandatory identity linkage, runtime failure classification and runtime cleanup.

P15.7 remains blocked until P15.6R is committed and pushed.

## Residual Constraints

Live failure validation was not performed. Automatic retry, runtime retry execution, manual resubmission execution, credential refresh, credential rotation and fallback are absent or prohibited. Provider quota and future account entitlement are unknown. Retry-after accuracy is provider-dependent and unverified. Persistent failure storage, runtime failure linkage and the controlled worker gate remain pending P15.7. Production readiness is not claimed.
