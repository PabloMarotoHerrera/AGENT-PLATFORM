# Provider Usage, Cost and Timeout Accounting

P15.5 adds a contract-only accounting boundary for the governed OpenAI Codex ChatGPT OAuth `gpt-5.5` route.

The boundary records deterministic usage, subscription-cost posture and timeout evidence for one bounded worker request. It does not start a worker, read credentials, call a provider, query usage or billing APIs, fetch model pricing, run tools, run MCP, contact remote hosts or persist records.

## Fixed Scope

| Field | Value |
| --- | --- |
| Accounting policy | `accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Provider profile | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Worker profile | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Model | `gpt-5.5` |
| Billing mode | `subscription_included` |
| Provider calls per record | `1` maximum |
| Usage fixtures | Synthetic only |

## Evidence Shape

Usage records accept only normalized token counters:

- uncached input tokens;
- cache-read input tokens;
- cache-write input tokens;
- output tokens;
- reasoning-output tokens;
- optional provider total tokens;
- request count fixed to `1`.

Raw request bodies, raw response bodies, provider headers and credential metadata are not accounting fields.

## Cost Posture

OpenAI Codex ChatGPT OAuth is tracked as a subscription-included route for this boundary.

P15.5 records `amount_usd = 0` only for the included marginal request posture and marks exact marginal request cost as unavailable. It does not estimate price from model metadata and does not call usage, quota or billing APIs.

## Timeout Posture

Timeout accounting uses injected UTC timestamps and fixed budgets:

| Stage | Budget |
| --- | ---: |
| connection | `10000` ms |
| response header | `30000` ms |
| complete inference | `120000` ms |
| cancellation | `10000` ms |
| worker shutdown | `15000` ms |

Completed, failed and cancelled records must not carry timeout-stage evidence. Timed-out records must identify one timeout stage.

## Worker Link

`BoundedProviderWorkerResult.usage_record_id` is the linking seam. P15.5 validates that the worker result and accounting record share the same usage record, request, runtime and correlation identifiers.

The link validator emits bounded metadata only and never includes result text.
