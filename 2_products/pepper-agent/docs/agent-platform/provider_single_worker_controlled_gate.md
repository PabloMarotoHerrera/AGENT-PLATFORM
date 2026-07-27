# Provider Single Worker Controlled Gate

P15.7 defines the governed runtime seam for one OpenAI Codex ChatGPT OAuth worker request.

## Scope

The controlled gate owns exactly one bounded worker request, one temporary credential lease, one Responses API dispatch, one worker result and the required secret-free accounting/failure links.

It does not authorize production rollout, automatic retry, fallback, credential rotation, model replacement, tool use, MCP use, billing lookup, quota lookup or persistent evidence storage.

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
| Credential store | `openai-codex.primary` |

## Execution Limits

| Limit | Value |
| --- | ---: |
| Concurrent workers | `1` |
| Concurrent requests per worker | `1` |
| Requests per worker lifetime | `1` |
| Responses create calls per request | `1` |
| SDK retries | `0` |
| Worker retries | `0` |
| Fallback attempts | `0` |
| Credential refresh calls | `0` |
| Model-list calls | `0` |
| Temporary lease TTL | `300000` ms |
| Minimum remaining credential lifetime | `300000` ms |

## Dispatch Seam

The only provider dispatch seam is a direct streamed Responses create call with `stream=True`.

The gate does not call the generic Hermes Codex stream helper because that helper can retry for normal interactive sessions. The gate uses only the shared raw-event consumer `agent.codex_runtime._consume_codex_event_stream` after its single create call has returned an event stream.

The fixed dispatch payload contains:

```yaml
model: gpt-5.5
instructions: Return only the exact literal requested by the user. Do not call tools. Do not include commentary, markdown, punctuation or additional text.
input:
  - role: user
    content: bounded worker request user_content
store: false
reasoning:
  effort: medium
  summary: auto
include:
  - reasoning.encrypted_content
prompt_cache_key: source-native bounded content-addressed cache key
stream: true
```

The gate reuses the source-native Codex Responses request builder as a formatting authority with `is_codex_backend=true`, `tools=None` and reasoning effort `medium`, then adds `stream=True` only in the single-dispatch seam.

Wire request fields that must be absent are `max_output_tokens`, `tools`, `tool_choice`, `parallel_tool_calls`, `service_tier`, `fallback_model`, caller generation overrides, caller timeout overrides and unsupported body-level headers.

The output limit remains local. The worker result envelope still enforces its existing maximum output UTF-8 byte policy, and the live validation gate additionally requires an exact `PEPPER_P15_7_OK` output match.

Caller-supplied model, provider, endpoint, system instruction, generation parameters, timeout parameters, tools, hosted tools, MCP, metadata and raw transport options are rejected or absent.

## Credential Gate

The runtime creates one temporary projection from the governed durable store and releases it in a `finally` path after success or failure.

Credential behavior:

- no OAuth acquisition;
- no device-code polling;
- no automatic refresh;
- no credential rotation;
- no alternate credential selection;
- no durable credential deletion.

The provider-runtime resolver validates secret-free credential status and pathless lease metadata before worker execution. Expired, missing or near-expiry credentials block before dispatch.

## Worker Protocol

The runtime reads one deterministic worker request frame from stdin and writes one deterministic worker result frame to stdout. Public worker results retain bounded text output or a bounded safe failure envelope only.

Raw provider responses, provider headers, credential metadata, reasoning traces, tool calls and stream chunks are not retained in the worker result.

## Accounting And Failure Links

Successful dispatch creates a P15.5 accounting record, sets the worker result `usage_record_id` and validates the worker-result/accounting link.

Failed post-dispatch requests create:

- a P15.6 failure record;
- a P15.6 retry decision with automatic retry and fallback disabled;
- a P15.5 accounting record when a provider dispatch was attempted;
- a worker-result/accounting link;
- a failure/accounting link.

Failure records keep only bounded safe metadata and do not retain raw provider response IDs on failure, raw error messages, raw response bodies, headers, prompts, outputs, reasoning traces or credential metadata.

## Live Validation Constraint

The intended bounded live validation request is:

```text
User: Reply with exactly: PEPPER_P15_7_OK
Expected output: PEPPER_P15_7_OK
```

Live validation may run only when the governed credential is present, unexpired and has at least the required remaining lifetime. If not, the gate is blocked with credential-missing, credential-expired or credential-near-expiry evidence instead of attempting OAuth or refresh.

## Historical Correction Evidence

The first P15.7 live attempt is retained only as bounded historical product evidence:

| Field | Value |
| --- | ---: |
| Provider dispatches | `1` |
| Result | `failed` |
| Category | `request_invalid` |
| Automatic retries | `0` |
| Fallback | `0` |
| Credential refresh | `0` |
| Cleanup | `passed` |

Root cause: the first P15.7 request sent the previously expected `max_output_tokens` wire field, but the accepted Hermes Codex transport deliberately omits `max_output_tokens` when `is_codex_backend=true`. The corrected gate keeps output bounds local and sends the source-native Codex backend request shape without that field.

## Dispatch Diagnostics

The second authorized P15.7 live attempt produced only bounded runtime evidence: result `failed`, category `unknown`, failure stage `stream`, provider dispatches `0`, automatic retries `0`, fallback `0` and cleanup `passed`. No retained raw provider body, headers, prompt, output, credential metadata, provider response ID, traceback or host path evidence is available for that attempt.

That bounded evidence is insufficient for exact root-cause attribution and the `stream`/`0` pair is not a valid P15.7 phase/counter combination. Current gate diagnostics therefore record only an allowed checkpoint trail, the local phase, safe exception class/module names and cleanup status. They reject `stream`, `terminal` or `accounting` phases unless the provider dispatch counter is `1`.

The corrected phase ownership is:

- pre-`responses.create` failures are `preflight` or `client_construction` with provider dispatches `0`;
- exceptions raised by `responses.create` are `dispatch` with provider dispatches `1`;
- exceptions raised while iterating an event stream returned by `responses.create` are `stream` with provider dispatches `1`;
- local terminal validation and accounting failures after a returned stream keep provider dispatches `1`;
- cleanup failures are recorded as local cleanup status and do not erase an already observed dispatch count.

## Residual Constraints

P15.7 is a controlled runtime seam, not a production activation. Persistent evidence storage, UI exposure, manual resubmission execution and broader provider fleet behavior remain outside this boundary.
