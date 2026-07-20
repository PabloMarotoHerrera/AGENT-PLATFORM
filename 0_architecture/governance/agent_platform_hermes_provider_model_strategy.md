# P15.0 - Hermes Provider Model Strategy

## Verdict

```text
hermes_provider_model_strategy_ready_with_constraints
```

P15.0 selects the existing Hermes `openai-codex` provider route with
ChatGPT OAuth and the `gpt-5.5` Codex model slug for later governed
implementation planning. This replaces the rejected `openai-api` API-key
strategy in this same canonical record. It is a strategy record only and does
not authorize provider calls, OAuth flows, credential inspection, credential
writes, runtime execution, fallback routing, worker launch, agent launch, tool
execution, MCP execution, model-list calls, frontend endpoint entry, caller
endpoint entry, runtime-adapter changes, product code changes, manifest changes,
lockfile changes, register changes, Graphify mutation, staging, commit, push or
release.

## Dynamic Start State

| Field | Value |
| --- | --- |
| Dynamic start SHA | `0742bf883dde7deb72de4c159d962f73851f996a` |
| `origin/main` at start | `0742bf883dde7deb72de4c159d962f73851f996a` |
| Branch | `main` |
| HEAD equals origin/main | `true` |
| P14.R committed | `true` |
| Index empty at start | `true` |
| Tracked working tree clean at start | `true` |
| Product tracked file count | `6219` |
| Modification register rows | `101` |
| Modification register columns | `18` |
| Register duplicate IDs | `0` |
| Register duplicate paths | `0` |
| Register missing fields | `0` |
| Register hash mismatches | `0` |
| Allowed unrelated untracked paths | `.opencode/**`; `AGENTS.md`; `graphify-out/**` |
| Agent Git mutation | No staging, commit or push performed. |

P14.R commitment was verified by the tracked file
`0_architecture/governance/agent_platform_hermes_governed_runtime_adapter_closure.md`
with no tracked or staged diff at the P15.0 start state.

## Strategy Selection

| Field | Selected Value |
| --- | --- |
| Strategy ID | `p15.provider-model.chatgpt-oauth.initial.v1` |
| Active provider count | `1` |
| Provider slug | `openai-codex` |
| Provider label | `OpenAI Codex` |
| Provider endpoint | `https://chatgpt.com/backend-api/codex` |
| Provider endpoint source | Tracked `DEFAULT_CODEX_BASE_URL` in `hermes_cli/auth.py`. |
| Provider auth shape | ChatGPT OAuth through Hermes `oauth_external` flow. |
| Authentication selected | `chatgpt_oauth` |
| Subscription-backed route selected | `true` |
| API-key route selected | `false` |
| API billing selected | `false` |
| Credential delivery owner | P15.1 |
| Hermes transport | `codex_responses` |
| Active primary model count | `1` |
| Selected model slug | `gpt-5.5` |
| Immutable model snapshot selected | `false` |
| Mutable backend slug selected | `true` |
| Account entitlement check | Deferred to P15.4. |
| Runtime acceptance check | Deferred to P15.4. |
| Active fallback count | `0` |
| Active workers | `0` |
| Active agents | `0` |
| Streaming now | `false` |
| Tools now | `false` |
| MCP now | `false` |
| Automatic retry now | `false` |
| Automatic fallback now | `false` |
| Provider calls now | `false` |

Canonical planning shape, not applied by this ticket:

```yaml
strategy_id: p15.provider-model.chatgpt-oauth.initial.v1
provider:
  slug: openai-codex
  label: OpenAI Codex
  auth: chatgpt_oauth
  hermes_auth_type: oauth_external
  subscription_backed: true
  api_key_route_selected: false
  api_billing_selected: false
  endpoint: https://chatgpt.com/backend-api/codex
  endpoint_source: DEFAULT_CODEX_BASE_URL
model:
  selected_model: gpt-5.5
  immutable_snapshot: false
  mutable_backend_slug: true
  dynamic_model_replacement_allowed: false
execution:
  api_mode: codex_responses
  active_provider_count: 1
  active_primary_model_count: 1
  active_fallback_count: 0
  active_workers: 0
  active_agents: 0
  streaming: false
  tools: false
  mcp: false
  automatic_retry: false
  automatic_fallback: false
  provider_calls: false
```

## Rejected Prior Strategy

The prior draft selected `openai-api`, `OPENAI_API_KEY`,
`https://api.openai.com/v1`, API billing, and an exact `gpt-5.5` snapshot. That
route is rejected for P15.0 because the human-selected strategy is the
ChatGPT-OAuth, plan-backed Codex route already represented in Hermes as
`openai-codex`. This record keeps `openai-api` only as a compared candidate.

The P15 governed route must not use `OPENAI_API_KEY`, must not use
`https://api.openai.com/v1`, must not use public API token pricing as its
primary cost model, and must not pin an API model snapshot for this ChatGPT
backend. The selected model is the Codex backend slug `gpt-5.5`, whose backing
model can change under OpenAI account and product controls.

## Endpoint Policy

| Field | Value |
| --- | --- |
| Provider endpoint | `https://chatgpt.com/backend-api/codex` |
| Provider endpoint source | `DEFAULT_CODEX_BASE_URL` in `2_products/hermes-agent/hermes_cli/auth.py`. |
| Base URL override allowed | `false` |
| `HERMES_CODEX_BASE_URL` inherited | `false` |
| `OPENAI_BASE_URL` inherited | `false` |
| Caller endpoint allowed | `false` |
| Frontend endpoint allowed | `false` |
| Config endpoint allowed | `false` |
| Custom endpoint allowed | `false` |
| Proxy endpoint allowed | `false` |
| Aggregator endpoint allowed | `false` |
| Regional/data-residency endpoint allowed | `false` |

Binding P15.2 policy shape:

```yaml
endpoint_policy:
  provider_endpoint: https://chatgpt.com/backend-api/codex
  provider_endpoint_source: DEFAULT_CODEX_BASE_URL
  base_url_override_allowed: false
  HERMES_CODEX_BASE_URL_inherited: false
  OPENAI_BASE_URL_inherited: false
  caller_endpoint_allowed: false
  frontend_endpoint_allowed: false
  config_endpoint_allowed: false
  custom_endpoint_allowed: false
  proxy_endpoint_allowed: false
  aggregator_endpoint_allowed: false
```

Hermes currently has broader generic behavior than this strategy allows:
`resolve_codex_runtime_credentials()` can derive `base_url` from
`HERMES_CODEX_BASE_URL`, and explicit runtime resolution can accept a caller
base URL for `openai-codex`. P15.2 must narrow that behavior for the governed
profile by forcing `https://chatgpt.com/backend-api/codex` and rejecting caller,
frontend, config, environment, custom-provider, and alias-derived endpoint
changes.

This endpoint is derived from the locked Hermes implementation, not from a
public guarantee that the endpoint is permanently stable. A future endpoint
change requires source compatibility review, OAuth compatibility review,
security review, and human approval.

## Model Policy

| Field | Value |
| --- | --- |
| Model ID | `gpt-5.5` |
| Selected model | `gpt-5.5` |
| Immutable snapshot | `false` |
| Mutable backend slug | `true` |
| Dynamic model replacement | `false` |
| Live model-list replacement | `false` |
| Fallback model | None. |
| Entitlement assertion in P15.0 | None. |
| Runtime acceptance assertion in P15.0 | None. |

```yaml
model_policy:
  model_id: gpt-5.5
  immutable_snapshot: false
  mutable_backend_slug: true
  dynamic_replacement_allowed: false
```

`gpt-5.5` is selected as the Codex backend model slug because Hermes'
`DEFAULT_CODEX_MODELS` starts with `gpt-5.5`, the `openai-codex` provider list
is derived from that catalog, and OpenAI Codex documentation lists `gpt-5.5` as
a Codex model available through ChatGPT and API surfaces. Current official Codex
recommendations also include GPT-5.6 models. GPT-5.5 is retained intentionally
because it is the locked Hermes catalog selection approved for this strategy;
this is not a claim that GPT-5.5 is the newest or default Codex model. P15.4
must fail closed if the authenticated account cannot use `gpt-5.5`; it must not
silently substitute GPT-5.6 Sol, GPT-5.6 Terra, GPT-5.6 Luna, or any other
model.

## Initial Context and Output Policy

These are recommended initial tracked values for P15.2/P15.3 pilot use, not
statements about the model's technical maximum:

```yaml
context_and_output_policy:
  maximum_prompt_tokens: 32768
  reserved_system_instruction_tokens: 8192
  maximum_user_content_tokens: 24576
  maximum_output_tokens: 4096
  reasoning_effort: medium
  streaming: false
  oversized_request_posture: fail_before_provider_call
```

Required invariant:

```text
reserved_system_instruction_tokens + maximum_user_content_tokens <= maximum_prompt_tokens
8192 + 24576 <= 32768
```

Oversized requests must fail before any provider call. Implementation must not
silently truncate security instructions, authority boundaries, acceptance
criteria, or provenance requirements. P15.3 may reduce these values, but must
not increase them without governed review.

## Initial Timeout Strategy

Recommended maximum tracked values:

| Timeout | Value |
| --- | ---: |
| `oauth_initiation_timeout_ms` | `600000` |
| `oauth_polling_timeout_ms` | `900000` |
| `token_refresh_timeout_ms` | `30000` |
| `connection_timeout_ms` | `10000` |
| `response_header_timeout_ms` | `30000` |
| `complete_inference_timeout_ms` | `120000` |
| `cancellation_deadline_ms` | `10000` |
| `worker_shutdown_deadline_ms` | `15000` |

P15.1 owns OAuth initiation, polling, refresh, token storage, and revocation
timeout values. P15.2/P15.3 own provider and worker values. P15.4 validates
actual runtime behavior. Callers cannot override these values. Implementation
may choose lower values, but no SDK default is accepted without explicit
validation.

## Provider Inventory

| Candidate | Hermes Status | Strengths | P15.0 Decision |
| --- | --- | --- | --- |
| `openai-codex` | Canonical provider; `oauth_external`; `codex_responses`; endpoint `https://chatgpt.com/backend-api/codex`; catalog starts with `gpt-5.5`; usage pricing marks route as `subscription_included`. | Matches human-selected ChatGPT OAuth route, uses existing Hermes provider, avoids API-key billing, supports selected model slug, and is direct to OpenAI's Codex backend. | Selected with endpoint, model, tool, streaming, retry, and entitlement constraints. |
| `openai-api` | Canonical provider; `api_key`; endpoint `https://api.openai.com/v1`; supports `OPENAI_API_KEY` and `OPENAI_BASE_URL`; `codex_responses`. | Direct OpenAI route and existing GPT-5.5 catalog entries. | Rejected because P15 selected ChatGPT OAuth subscription/credits, not API-key billing or API endpoint. |
| `nous` | Canonical provider; `oauth_device_code`; endpoint `https://inference-api.nousresearch.com/v1`; OpenAI chat transport. | Existing OAuth path and broad model access. | Rejected because it is Nous account/portal OAuth, not ChatGPT OAuth, and does not bind to OpenAI Codex backend. |
| `copilot` | Canonical provider; GitHub token or `gh` auth token; `openai_chat`; endpoint `https://api.githubcopilot.com`. | Existing GitHub Copilot integration. | Rejected because it uses GitHub/Copilot entitlement and provider mediation, not ChatGPT OAuth. |
| `copilot-acp` | Canonical provider; `external_process`; `codex_responses`; endpoint shape `acp://copilot`. | Existing ACP path with Responses-like semantics. | Rejected because it requires a spawned external Copilot process and separate contract boundary. |
| `anthropic` | Canonical provider; API key plus Claude Code token env support; `anthropic_messages`. | Strong direct provider route and native Messages transport. | Rejected because it is not ChatGPT OAuth, not Codex backend, and not the selected `gpt-5.5` model route. |
| `openrouter` | Canonical aggregator; OpenAI-compatible chat transport. | Broad model access and catalog reach. | Rejected because aggregator indirection conflicts with the one-provider direct Codex route. |

This inventory is not a removal or deprecation decision for any Hermes provider.
It is the scoped P15.0 comparison used to select one initial governed route.

## Weighted Decision Matrix

The matrix below scores only serious inspected candidates. It does not include
unverified model benchmarks and is not an absolute model-quality ranking; it is
a bounded P15.0 governance-fit score for this specific strategy.

| Candidate | Hermes compatibility `25` | Subscription-intent compatibility `20` | Credential-boundary compatibility `15` | Usage and quota observability `10` | Timeout and cancellation support `10` | Model suitability for coding and planning `10` | Model lifecycle stability `5` | Operational predictability `5` | Total `100` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `openai-codex` | 23 | 20 | 13 | 8 | 6 | 9 | 3 | 4 | 86 |
| `openai-api` | 22 | 4 | 7 | 8 | 7 | 8 | 4 | 4 | 64 |
| `nous` | 18 | 10 | 10 | 6 | 7 | 7 | 3 | 3 | 64 |
| `anthropic` | 19 | 3 | 8 | 7 | 7 | 8 | 4 | 4 | 60 |
| `copilot` | 17 | 5 | 8 | 5 | 6 | 7 | 3 | 3 | 54 |
| `copilot-acp` | 15 | 5 | 6 | 4 | 4 | 7 | 2 | 2 | 45 |

### Weighted Matrix Rationale

| Criterion | Weight | Candidate | Score | Bounded rationale | Evidence source | Uncertainty |
| --- | ---: | --- | ---: | --- | --- | --- |
| Hermes compatibility | 25 | `openai-codex` | 23 | Existing canonical provider, auth registry, overlay, `codex_responses` transport, and catalog route; points held back for P15 endpoint narrowing and non-streaming proof. | `hermes_cli/auth.py`; `hermes_cli/providers.py`; `hermes_cli/models.py`; `agent/codex_runtime.py` | Non-streaming implementation and governed endpoint enforcement remain unvalidated. |
| Hermes compatibility | 25 | `openai-api` | 22 | Existing direct OpenAI API provider and `codex_responses` overlay, but rejected API-key route and `OPENAI_BASE_URL` capability conflict with this strategy. | `hermes_cli/auth.py`; `hermes_cli/providers.py`; `hermes_cli/models.py` | P15 route would require a different credential and billing strategy. |
| Hermes compatibility | 25 | `nous` | 18 | Existing provider and OAuth device-code path with OpenAI-chat transport; does not bind to Codex backend. | `hermes_cli/auth.py`; `hermes_cli/providers.py`; `hermes_cli/models.py` | Exact model and quota semantics are Nous-specific. |
| Hermes compatibility | 25 | `anthropic` | 19 | Existing canonical provider with native Messages transport and Claude model catalog; not a Codex Responses route. | `hermes_cli/auth.py`; `hermes_cli/providers.py`; `hermes_cli/models.py` | Claude Code token path is present but not selected or validated here. |
| Hermes compatibility | 25 | `copilot` | 17 | Existing GitHub Copilot provider with token-based route; different transport and provider authority. | `hermes_cli/auth.py`; `hermes_cli/models.py`; `hermes_cli/providers.py` | GitHub entitlement behavior is external to P15 evidence. |
| Hermes compatibility | 25 | `copilot-acp` | 15 | Existing ACP provider with `codex_responses` overlay, but requires external process lifecycle. | `hermes_cli/auth.py`; `hermes_cli/providers.py`; `hermes_cli/models.py` | ACP process behavior was not launched or validated. |
| Subscription-intent compatibility | 20 | `openai-codex` | 20 | Matches selected ChatGPT OAuth subscription/credit route and excludes API-key billing. | OpenAI Codex auth/pricing docs; `agent/usage_pricing.py` | Account tier and credit state are account-specific and unverified. |
| Subscription-intent compatibility | 20 | `openai-api` | 4 | Official route is API-key usage-based billing, not ChatGPT OAuth subscription access. | OpenAI Codex auth/pricing docs; `hermes_cli/auth.py` | None material for P15 because route is rejected. |
| Subscription-intent compatibility | 20 | `nous` | 10 | OAuth provider route exists, but it is Nous portal/account intent, not ChatGPT OAuth. | `hermes_cli/auth.py`; `hermes_cli/providers.py` | Nous subscription/free-tier semantics are separate from OpenAI Codex. |
| Subscription-intent compatibility | 20 | `anthropic` | 3 | Provider is not ChatGPT OAuth and not subscription-backed through OpenAI Codex. | `hermes_cli/auth.py`; `hermes_cli/providers.py` | Anthropic plan semantics not inspected for P15. |
| Subscription-intent compatibility | 20 | `copilot` | 5 | May rely on GitHub/Copilot entitlement, but not ChatGPT OAuth or OpenAI Codex credits. | `hermes_cli/auth.py`; `hermes_cli/models.py` | Copilot plan and token scope were not validated. |
| Subscription-intent compatibility | 20 | `copilot-acp` | 5 | External Copilot process may reflect Copilot subscription, but not selected ChatGPT OAuth route. | `hermes_cli/auth.py`; `hermes_cli/providers.py` | ACP entitlement and process contract were not validated. |
| Credential-boundary compatibility | 15 | `openai-codex` | 13 | Hermes implements OAuth auth-store and credential-pool paths; held back because official docs do not certify Hermes as supported third-party OAuth client and endpoint override must be narrowed. | `hermes_cli/auth.py`; OpenAI Codex auth docs | OAuth client acceptance, redirect/device-code behavior, refresh, and revocation remain live-validation items. |
| Credential-boundary compatibility | 15 | `openai-api` | 7 | API key boundary is simple but violates selected no-API-key route and generic `OPENAI_BASE_URL` must be denied. | `hermes_cli/auth.py`; OpenAI Codex auth docs | Secret delivery was not validated and route is rejected. |
| Credential-boundary compatibility | 15 | `nous` | 10 | OAuth device-code boundary exists in Hermes, but credential authority is Nous rather than ChatGPT. | `hermes_cli/auth.py` | Account-specific portal behavior unverified. |
| Credential-boundary compatibility | 15 | `anthropic` | 8 | API key and Claude Code token env support exist, but are not the selected credential shape. | `hermes_cli/auth.py`; `hermes_cli/providers.py` | OAuth-like Claude token path not validated. |
| Credential-boundary compatibility | 15 | `copilot` | 8 | Uses GitHub token or `gh` token route, but unrelated to ChatGPT OAuth. | `hermes_cli/auth.py` | GitHub token scope and Copilot entitlement unverified. |
| Credential-boundary compatibility | 15 | `copilot-acp` | 6 | External process owns part of credential boundary, reducing Hermes-contained assurance. | `hermes_cli/auth.py`; `hermes_cli/providers.py` | ACP process and credential handling not validated. |
| Usage and quota observability | 10 | `openai-codex` | 8 | Hermes marks route as `subscription_included`; OpenAI docs expose plan limits and credit rates. | `agent/usage_pricing.py`; OpenAI Codex pricing docs | Exact account balance and subscription quota signal are exposed only when account/backend provides them. |
| Usage and quota observability | 10 | `openai-api` | 8 | API usage/pricing observability is clearer, but it is the rejected billing route. | OpenAI API/Codex auth and pricing docs; `agent/usage_pricing.py` | API invoices are outside selected strategy. |
| Usage and quota observability | 10 | `nous` | 6 | Existing provider has account/tier concepts, but not selected OpenAI Codex credit pool. | `hermes_cli/models.py`; `hermes_cli/auth.py` | Free-tier and quota details remain account-specific. |
| Usage and quota observability | 10 | `anthropic` | 7 | Direct provider route and pricing-style accounting are clearer than aggregator routes, but not selected. | `agent/usage_pricing.py`; `hermes_cli/auth.py` | Anthropic account usage was not inspected. |
| Usage and quota observability | 10 | `copilot` | 5 | GitHub/Copilot usage visibility is mediated outside Hermes evidence. | `hermes_cli/auth.py`; `hermes_cli/models.py` | Quota fields were not validated. |
| Usage and quota observability | 10 | `copilot-acp` | 4 | External process reduces direct usage and quota observability. | `hermes_cli/providers.py`; `hermes_cli/models.py` | ACP usage reporting unverified. |
| Timeout and cancellation support | 10 | `openai-codex` | 6 | Hermes has timeout and runtime code paths, but current Codex runtime is streaming-oriented and P15 requires non-streaming proof. | `hermes_cli/timeouts.py`; `agent/codex_runtime.py`; `agent/transports/codex.py` | P15.4 must validate actual cancellation and non-streaming behavior. |
| Timeout and cancellation support | 10 | `openai-api` | 7 | Direct API route can use provider timeouts, but would still require P15-specific non-streaming and no-retry validation. | `hermes_cli/timeouts.py`; `agent/codex_runtime.py` | Route is rejected; no live validation. |
| Timeout and cancellation support | 10 | `nous` | 7 | Existing chat transport path can use Hermes timeout mechanisms. | `hermes_cli/timeouts.py`; provider runtime source | No P15 runtime validation. |
| Timeout and cancellation support | 10 | `anthropic` | 7 | Native Messages route and timeout plumbing exist. | `hermes_cli/timeouts.py`; `hermes_cli/providers.py` | No P15 runtime validation. |
| Timeout and cancellation support | 10 | `copilot` | 6 | Token route has ordinary provider timeout possibilities, but mediated backend behavior is less predictable. | `hermes_cli/timeouts.py`; `hermes_cli/auth.py` | Copilot-specific cancellation behavior unverified. |
| Timeout and cancellation support | 10 | `copilot-acp` | 4 | External process lifecycle adds process shutdown and IPC cancellation risk. | `hermes_cli/providers.py`; runtime-adapter evidence | ACP process not launched or tested. |
| Model suitability for coding and planning | 10 | `openai-codex` | 9 | `gpt-5.5` is selected, in Hermes Codex catalog, and official docs describe it for complex coding and planning-style work. | `hermes_cli/codex_models.py`; OpenAI Codex models docs | No unverified benchmark claim is made. |
| Model suitability for coding and planning | 10 | `openai-api` | 8 | GPT-5.5 family appears in Hermes API catalog, but selected route is not API billing. | `hermes_cli/models.py`; OpenAI docs | No live acceptance or benchmark validation. |
| Model suitability for coding and planning | 10 | `nous` | 7 | Broad catalog includes coding-capable OpenAI/Anthropic-style model names, but not fixed Codex `gpt-5.5`. | `hermes_cli/models.py` | Exact available tenant model set unverified. |
| Model suitability for coding and planning | 10 | `anthropic` | 8 | Claude model catalog is coding/planning plausible, but different model family. | `hermes_cli/models.py`; `hermes_cli/providers.py` | No benchmark or account validation. |
| Model suitability for coding and planning | 10 | `copilot` | 7 | Copilot path is coding-oriented and catalog includes multiple coding-capable model names. | `hermes_cli/models.py` | No benchmark or entitlement validation. |
| Model suitability for coding and planning | 10 | `copilot-acp` | 7 | ACP route is coding-agent oriented, but external process and model selection are not P15-bound. | `hermes_cli/models.py`; `hermes_cli/providers.py` | No runtime acceptance validation. |
| Model lifecycle stability | 5 | `openai-codex` | 3 | Selected slug is mutable backend label, intentionally not an immutable snapshot. | OpenAI Codex models docs; `hermes_cli/codex_models.py` | Backend mapping can change under OpenAI controls. |
| Model lifecycle stability | 5 | `openai-api` | 4 | API route can use snapshots or clearer API model lifecycle, but that is rejected here. | OpenAI API/Codex docs; `hermes_cli/models.py` | Snapshot availability for tenant not validated. |
| Model lifecycle stability | 5 | `nous` | 3 | Aggregated portal model availability may vary by account/tier. | `hermes_cli/models.py` | Tenant availability unverified. |
| Model lifecycle stability | 5 | `anthropic` | 4 | Direct provider model naming is comparatively stable, but different provider family. | `hermes_cli/models.py`; `hermes_cli/providers.py` | Future provider deprecation behavior not inspected. |
| Model lifecycle stability | 5 | `copilot` | 3 | GitHub-mediated model catalog can change outside Hermes. | `hermes_cli/models.py` | Backend catalog behavior unverified. |
| Model lifecycle stability | 5 | `copilot-acp` | 2 | ACP process and backend catalog add lifecycle uncertainty. | `hermes_cli/providers.py`; `hermes_cli/models.py` | ACP behavior unverified. |
| Operational predictability | 5 | `openai-codex` | 4 | Fixed governed endpoint and one selected slug improve predictability; private endpoint stability and OAuth acceptance remain open. | `hermes_cli/auth.py`; OpenAI Codex docs | Endpoint is locked source evidence, not public permanence guarantee. |
| Operational predictability | 5 | `openai-api` | 4 | Public API route is operationally predictable, but conflicts with selected credential/billing route. | `hermes_cli/auth.py`; OpenAI docs | Rejected route. |
| Operational predictability | 5 | `nous` | 3 | Existing route, but account/tier/model availability are separate. | `hermes_cli/auth.py`; `hermes_cli/models.py` | Portal state not validated. |
| Operational predictability | 5 | `anthropic` | 4 | Direct provider route is predictable, but not selected model/auth. | `hermes_cli/auth.py`; `hermes_cli/providers.py` | Account state not validated. |
| Operational predictability | 5 | `copilot` | 3 | GitHub-mediated provider adds entitlement and token-scope uncertainty. | `hermes_cli/auth.py` | Copilot state not validated. |
| Operational predictability | 5 | `copilot-acp` | 2 | External ACP process and endpoint shape reduce predictability. | `hermes_cli/providers.py` | Process availability not validated. |

`openai-codex` remains selected because it is the only inspected serious
candidate that matches the accepted ChatGPT OAuth, subscription-backed,
tool-free, non-fallback Codex strategy while also existing in locked Hermes
source.

## Hermes Evidence

| Evidence | Observation |
| --- | --- |
| Auth constants | `2_products/hermes-agent/hermes_cli/auth.py` defines `DEFAULT_CODEX_BASE_URL = "https://chatgpt.com/backend-api/codex"`, `CODEX_OAUTH_CLIENT_ID`, and `CODEX_OAUTH_TOKEN_URL = "https://auth.openai.com/oauth/token"`. |
| Provider auth registry | `PROVIDER_REGISTRY["openai-codex"]` has `auth_type="oauth_external"` and `inference_base_url=DEFAULT_CODEX_BASE_URL`. |
| Provider overlay | `HERMES_OVERLAYS["openai-codex"]` maps to `transport="codex_responses"`, `auth_type="oauth_external"`, and `base_url_override="https://chatgpt.com/backend-api/codex"`. |
| Canonical provider list | `ProviderEntry("openai-codex", "OpenAI Codex", "OpenAI Codex (Codex CLI via ChatGPT subscription or API key)")` is present in `hermes_cli/models.py`. |
| Model catalog | `DEFAULT_CODEX_MODELS` starts with `gpt-5.5`; `_PROVIDER_MODELS["openai-codex"]` is derived from that list through `_codex_curated_models()`. |
| Credential resolution | `resolve_codex_runtime_credentials()` returns `provider="openai-codex"`, `auth_mode="chatgpt"`, and an access token from Hermes auth storage or credential pool; it can currently honor `HERMES_CODEX_BASE_URL`, which P15.2 must narrow. |
| Runtime resolution | `runtime_provider.py` sets `api_mode="codex_responses"` for `openai-codex` and defaults the base URL to `DEFAULT_CODEX_BASE_URL`. |
| Responses request construction | `agent/transports/codex.py` builds `model`, `instructions`, `input`, `store=False`, and only includes `tools` when response tools exist. Tool-free requests are representable. |
| Responses preflight | `agent/codex_responses_adapter.py` validates `model`, `instructions`, `input`, optional `tools`, and allowed request keys. |
| Current runtime dispatch | `agent/codex_runtime.py` uses `responses.create(stream=True)` in `run_codex_stream()`. This conflicts with the P15.0 streaming-disabled posture until P15.4 proves a safe non-streaming path or records a blocker. |
| Usage/cost accounting | `agent/usage_pricing.py` returns `BillingRoute(..., billing_mode="subscription_included")` for `provider_name == "openai-codex"` and `pricing_version="included-route"`. |
| Runtime adapter registry | P14 runtime-adapter profiles currently include only `test.lifecycle_probe` and `hermes.dashboard.experimental`; P15 must introduce a new later profile and must not reuse the dashboard lifecycle identity. |

## Official OpenAI Facts

Public documentation reviewed on 2026-07-20:

| Source | Relevant Facts |
| --- | --- |
| `https://help.openai.com/en/articles/11369540-codex-in-chatgpt` | Codex is an AI agent for writing, reviewing, and shipping code. Users start by signing in with a ChatGPT account. Codex is included across ChatGPT plans, including Free and Go, with usage limits varying by plan. |
| Same Help Center article | Codex usage, ChatGPT Work, ChatGPT for Excel, and Workspace Agents draw from the same agentic usage and credit pool when available. Usage varies by task size, model, and run surface. |
| Same Help Center article | If a user nears or reaches the Codex limit, the usage page or limit banner describes options such as additional credits, upgrade, or waiting for reset. |
| Same Help Center article | ChatGPT training data controls apply to content processed through Codex. Local workflows run on the device; cloud tasks run in OpenAI-managed environments. |
| `https://developers.openai.com/codex/auth` | OpenAI authentication for Codex supports two modes: Sign in with ChatGPT for subscription access, and API key for usage-based access. This strategy selects only the ChatGPT mode. |
| Same Auth page | ChatGPT desktop app, Codex CLI, and IDE extension support both sign-in methods for local work. Codex cloud requires ChatGPT sign-in. |
| Same Auth page | With ChatGPT sign-in, Codex usage follows ChatGPT workspace permissions, RBAC, and ChatGPT Enterprise retention and residency settings. With API key sign-in, usage follows the API organization's retention and data-sharing settings. |
| Same Auth page | API-key usage is billed through the OpenAI Platform account at standard API rates, and API-key authentication uses standard API pricing instead of included ChatGPT plan credits. |
| Same Auth page | Codex caches login details locally in `~/.codex/auth.json` or in the OS credential store. File-based `~/.codex/auth.json` contains access tokens and should be treated like a password. |
| Same Auth page | Headless device-code authentication and copying `~/.codex/auth.json` are documented fallback patterns for Codex CLI. P15 forbids copying or importing real-user auth caches for the governed Hermes route. |
| `https://developers.openai.com/codex/models` | Codex model selection supports CLI `--model` or `-m`; `gpt-5.5` is listed as a previous-generation frontier model for complex coding, computer use, knowledge work, and research workflows. |
| Same Models page | When users sign in with ChatGPT, Codex works best with recommended models, and the current default recommendations may change. P15 keeps the selected slug fixed at `gpt-5.5` unless later governance changes it. |
| `https://developers.openai.com/codex/pricing` | Work mode and Codex are included in ChatGPT Free, Go, Plus, Pro, Business, Edu, or Enterprise plans. API Key is a separate usage-based option. |
| Same Pricing page | `gpt-5.5` appears in Codex usage-limit tables for Plus, Pro, Business, and API Key. Plus/Business local messages are documented as `15-80` per 5-hour window, Pro 5x as `75-400`, and Pro 20x as `300-1600`, subject to shared limits and additional weekly limits. |
| Same Pricing page | Codex credits per 1M tokens for `gpt-5.5` are documented as `125` input credits, `12.50` cached-input credits, and `750` output credits. |
| Same Pricing page | After included limits, credits can allow continued work for eligible plans; all users may run extra local chats using an API key, charged at standard API rates. P15 does not select the API-key extension path. |
| `https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance` | For individual services such as ChatGPT and Codex, content may be used to train models unless the user opts out. For business products including ChatGPT Business, ChatGPT Enterprise, and API, OpenAI states it does not train on inputs or outputs by default. |
| `https://help.openai.com/en/articles/7730893-data-controls-faq` | ChatGPT Data Controls allow users to turn off model training for conversations; Temporary Chats are deleted after 30 days, are not used for training, may be reviewed only for abuse, and do not create memories. |
| `https://openai.com/business-data/` | OpenAI states business data is not used for training by default, business data is encrypted at rest and in transit, and qualifying organizations have retention, data residency, and compliance controls. |

P15.0 records these facts as public documentation evidence only. It does not
verify account entitlement, workspace membership, RBAC settings, plan tier,
credit balance, usage limit state, training setting, retention setting,
residency setting, EKM, ZDR, DPA, BAA, or availability of `gpt-5.5` for any
specific tenant.

## OAuth Compatibility Authority Limitation

Official OpenAI documentation verifies ChatGPT sign-in for supported Codex
clients and surfaces. It does not by itself certify Hermes as an officially
supported third-party OAuth client. The locked Hermes source proves that Hermes
implements an `openai-codex` OAuth path, but that implementation remains an
unverified compatibility path until P15.1 and P15.4 complete live validation.

P15.0 does not claim OpenAI endorsement of Hermes. P15.1 must validate login
initiation, redirect/callback or device-code behavior, token storage, refresh,
and revocation. P15.4 must validate account entitlement, endpoint acceptance,
and exact `gpt-5.5` acceptance. Any OAuth client rejection, redirect mismatch,
or unsupported-client response must fail closed. No fallback to API key is
permitted.

## OAuth and Credential Boundary

| Field | Strategy Posture |
| --- | --- |
| OAuth start in P15.0 | Not authorized. |
| Browser or device-code flow in P15.0 | Not authorized. |
| Credential read in P15.0 | Not authorized. |
| Credential write in P15.0 | Not authorized. |
| Hermes auth store | Later governed work may use `get_hermes_home() / "auth.json"` only through approved Hermes auth functions. |
| Codex CLI auth store | `~/.codex/auth.json` must not be read, copied, imported, printed, or used as a fixture source for this strategy. |
| Real-user auth import | Prohibited. |
| Test credentials | Synthetic fixtures only; no live account state. |
| Token refresh | P15.1/P15.4 only after explicit authorization; no refresh in P15.0. |

The official Codex docs describe copying `~/.codex/auth.json` as a fallback for
trusted headless Codex CLI environments. That pattern is intentionally rejected
for P15. The governed Hermes route must use an explicit Hermes-owned auth flow
and must not import a user's existing Codex CLI or ChatGPT desktop credentials.

## Privacy and Data Posture

| Field | Strategy Posture |
| --- | --- |
| Product policy family | ChatGPT/Codex policy family, not OpenAI API policy family, because ChatGPT OAuth is selected. |
| Personal-plan training | Not assumed off. Users may need ChatGPT Data Controls to opt out. |
| Business-plan training | OpenAI states business products are not used for training by default. P15 does not verify workspace type. |
| Retention/residency | Follows ChatGPT workspace settings for ChatGPT sign-in. Not asserted by P15.0. |
| Temporary Chat | Not selected as a runtime primitive. |
| Memories, plugins, browser, computer use | Not selected. |
| Local vs cloud | P15 selects no runtime surface. Later implementation must state whether execution is local Hermes runtime, Codex cloud, or another surface before any call. |
| Data minimization | Later prompts must be limited to necessary runtime context and no optional Codex features may be enabled by default. |

Because the selected route is ChatGPT OAuth, later implementation must document
the workspace and user-plan data controls that actually govern the run. API
Platform data policies and public API pricing can be referenced for comparison
only; they are not the primary governance basis for this selected route.

## Tool-Free, MCP-Free, and Streaming-Disabled Posture

| Surface | P15.0 Posture | Later Requirement |
| --- | --- | --- |
| Hermes tools | Disabled. | P15 profile must pass no tools and reject any non-empty tool schema. |
| OpenAI/Codex hosted tools | Disabled. | No web search, file search, shell, code interpreter, apply patch, browser, computer use, plugins, skills, connectors, or other hosted tools. |
| MCP | Disabled. | No MCP servers or MCP tool schemas. |
| Subagents/workers | Disabled. | No subagent or worker launch. |
| Streaming | Disabled. | P15.4 must either prove a safe non-streaming Responses path or fail with `P15.4-NON_STREAMING_COMPATIBILITY_BLOCKED`. |
| Automatic retry | Disabled. | Retry policy remains disabled until P15.6 records bounded retry rules. |
| Fallback | Disabled. | No fallback provider, model, endpoint, worker, or API-key route. |

The tracked Hermes Codex runtime currently streams via
`responses.create(stream=True)`. That is a known compatibility risk for this
strategy because P15.0 explicitly selects `streaming=false`. P15.4 owns the
runtime proof; if non-streaming cannot be safely supported without changing the
governance posture, the implementation must stop with
`P15.4-NON_STREAMING_COMPATIBILITY_BLOCKED` rather than enabling streaming by
default.

## Usage and Quota Strategy

| Field | Strategy Posture |
| --- | --- |
| Primary cost route | ChatGPT plan usage and credits for `openai-codex`. |
| Public API USD pricing | Not primary for selected route. |
| Hermes pricing behavior | Existing code treats `openai-codex` as `subscription_included` and `included-route`. |
| Usage capture | Later ticket must preserve provider-reported token and credit-relevant usage when available. |
| Quota checks | Deferred; no model-list, usage-dashboard, or provider call in P15.0. |
| Limit exhaustion | Later runtime must surface quota/rate-limit status and must not auto-switch to API key. |
| API-key extension path | Explicitly not selected. A later governance record is required before API-key fallback or extra local API-key chats can be used. |

OpenAI documents plan-dependent Codex message ranges, shared 5-hour windows,
additional weekly limits, and credit consumption per million tokens. P15 records
those as planning evidence only. Account-specific quotas and credit balances are
runtime facts owned by P15.4/P15.5 and must not be inferred in P15.0.

## Usage and Quota Evidence Schema

P15.5 owns implementation and reconciliation for usage and quota evidence:

```yaml
usage_and_quota_evidence:
  input_tokens:
    classification: provider_reported_when_available
  cached_input_tokens:
    classification: provider_reported_when_available
  output_tokens:
    classification: provider_reported_when_available
  total_tokens:
    classification: provider_reported_or_locally_summed
  returned_model_id:
    classification: provider_reported
  finish_reason:
    classification: provider_reported_when_available
  provider_request_id:
    classification: provider_reported_when_safe
  elapsed_time_ms:
    classification: locally_derived
  subscription_quota_signal:
    classification: account_specific_when_exposed
  credit_consumption_signal:
    classification: account_specific_when_exposed
  exact_marginal_request_cost:
    classification: unavailable_by_default
```

Required distinctions:

- Token usage is not an API invoice.
- Subscription entitlement is not unlimited usage.
- Credit estimate is not account balance.
- Locally derived usage is not provider-reported usage.

## Failure and Retry Policy

P15.0 authorizes no runtime retry behavior. Existing Hermes code may contain
transport retries for current product behavior, but the governed strategy starts
with `automatic_retry=false` and `fallback_providers=[]`.

Later implementation must handle these cases explicitly before execution:

- `401` or `403`: credential, workspace, RBAC, or entitlement failure.
- `404`, `model_not_found`, unsupported model, or equivalent: `gpt-5.5` acceptance failure; do not substitute another model.
- `400` unsupported operation or invalid request: route/schema bug; do not retry blindly.
- `429` or Codex usage-limit exhaustion: surface quota state; do not auto-switch to API key.
- Timeout, stale stream, or transient connection failure: retry only if P15.6 defines bounds.
- `5xx`: provider transient failure; no fallback provider may activate under this record.
- Non-streaming incompatibility: fail with `P15.4-NON_STREAMING_COMPATIBILITY_BLOCKED` unless a later record authorizes streaming.

## Handoffs

| Area | Owner | Requirement |
| --- | --- | --- |
| OAuth credential governance | P15.1 | Define explicit user-initiated ChatGPT OAuth flow, Hermes auth-store writes, logout/clear semantics, token refresh bounds, no `~/.codex/auth.json` import, no secret logging, and synthetic-only tests. |
| Runtime profile and endpoint enforcement | P15.2 | Add a new P15 runtime profile, not `hermes.dashboard.experimental`; pin `DEFAULT_CODEX_BASE_URL`; reject `HERMES_CODEX_BASE_URL`, `OPENAI_BASE_URL`, caller, frontend, config, and custom endpoint overrides. |
| Provider/model binding | P15.2 | Apply exactly `provider=openai-codex`, `model=gpt-5.5`, `api_mode=codex_responses`, one provider, one model, no fallback, no dynamic model replacement. |
| User-facing configuration | P15.3 | Present the selected provider/model without exposing endpoint or API-key override controls for the governed route. |
| Runtime acceptance | P15.4 | With explicit authorization only, verify ChatGPT OAuth credential presence, account entitlement, endpoint acceptance, and `gpt-5.5` runtime acceptance. No live calls in P15.0. |
| Non-streaming compatibility | P15.4 | Prove a safe non-streaming route or fail closed with `P15.4-NON_STREAMING_COMPATIBILITY_BLOCKED`. |
| Usage and quota accounting | P15.5 | Record token usage, credit-relevant usage, quota/rate-limit outcomes, and `included-route` cost semantics; public API USD pricing is comparison-only. |
| Retry and failure bounds | P15.6 | Define bounded retry/backoff if desired; keep fallback disabled unless a later strategy changes it. |
| Closure | P15.R | Verify implementation matches this strategy and no unauthorized endpoint/model/auth/tool/streaming/fallback behavior was introduced. |

## Negative Authorization

This record does not authorize:

- Starting OAuth, browser login, device-code login, token refresh, or logout.
- Reading, writing, validating, printing, copying, importing, or probing provider credentials.
- Reading `~/.hermes/auth.json`, `~/.codex/auth.json`, OS credential stores, shell credential env vars, or account profile state.
- Calling OpenAI, ChatGPT, Codex, Nous, GitHub Copilot, Anthropic, OpenRouter, xAI, Gemini, Bedrock or any other inference/provider/model-list/usage API.
- Running `hermes model`, `hermes chat`, Codex CLI, workers, agents, tools, MCP servers, lifecycle gates, or runtime adapters.
- Modifying Hermes product code, runtime adapter code, frontend code, backend routes, registers, manifests, dependency files or lockfiles.
- Adding fallback providers, automatic provider routing, API-key fallback, cost controls, credential pools, auxiliary model routing or deployment behavior.
- Treating `HERMES_CODEX_BASE_URL`, `OPENAI_BASE_URL`, caller input, frontend input, config input, or custom provider settings as part of the governed route.
- Dynamically replacing `gpt-5.5` with a newer Codex recommendation or another account-available model.
- Enabling hosted tools, Hermes tools, MCP, plugins, skills, browser, computer use, web search, shell, code interpreter, file search, apply patch, image generation, streaming or automatic retry.

## Reconciliation

| Field | Reconciled Value |
| --- | --- |
| HEAD | `0742bf883dde7deb72de4c159d962f73851f996a` |
| `origin/main` | `0742bf883dde7deb72de4c159d962f73851f996a` |
| HEAD equals origin/main | `true` |
| Index empty | `true` |
| Staged files | None. |
| Strategy document path | `0_architecture/governance/agent_platform_hermes_provider_model_strategy.md` |
| Exact task candidate | `0_architecture/governance/agent_platform_hermes_provider_model_strategy.md` |
| Candidate paths | `1` |
| Unexpected tracked candidates | `0` |
| Unexpected task-specific untracked candidates | `0` |
| Editable paths for P15.0 | This strategy document only. |
| Product inventory | `6219` |
| Register rows | `101` |
| Register columns | `18` |
| Register duplicate IDs | `0` |
| Register duplicate paths | `0` |
| Register missing fields | `0` |
| Register hash mismatches | `0` |
| Product code changes | `0` |
| Product-source changes | `0` |
| Manifest/lockfile changes | `0` |
| Manifest changes | `0` |
| Lockfile changes | `0` |
| Register changes | `0` |
| Graphify mutation | `0` |
| Runtime/provider calls | `0` |
| Provider calls | `0` |
| Inference calls | `0` |
| OAuth flows | `0` |
| Credential reads | `0` |
| Credential environment inspection | `0` |
| Workers started | `0` |
| Agents started | `0` |
| Staging/commit/push | `0` |
| Selected provider | `openai-codex` |
| Selected auth | `chatgpt_oauth` |
| Selected route | ChatGPT OAuth, subscription/credits-backed Codex backend. |
| API-key route | Not selected. |
| API billing | Not selected. |
| Selected model | `gpt-5.5` |
| Immutable snapshot | Not selected. |
| Mutable backend slug | Selected. |
| Endpoint override | Not allowed. |
| Fallback providers | None. |

This reconciliation resolves the earlier stale draft mismatch by replacing the
API-key `openai-api` strategy with the human-selected ChatGPT OAuth
`openai-codex` strategy in the single canonical P15.0 record.

## Secret Scan

Secret scan scope is this strategy document only. Real environment variables,
auth files, OS credential stores, and account files were not inspected.

Allowed conceptual terms in this document:

- `OPENAI_API_KEY` as the name of the rejected credential type.
- `access_token` as a conceptual field.
- `refresh_token` as a conceptual field.
- `auth.json` as a conceptual path name.

Required scan result:

| Finding Type | Count |
| --- | ---: |
| Credential-value findings | `0` |
| Account-specific identifier findings | `0` |

## Validation Performed

Validation for this record is read-only except for editing this document:

```text
git rev-parse HEAD
git rev-parse origin/main
git status --short
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard -- "0_architecture/governance/*provider_model_strategy*.md"
git diff --name-only -- "2_products/hermes-agent" "2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv" "pyproject.toml" "uv.lock"
git diff --cached --name-only -- "2_products/hermes-agent" "2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv" "pyproject.toml" "uv.lock"
git diff --check -- 0_architecture/governance/agent_platform_hermes_provider_model_strategy.md
```

Additional read-only content validations performed for this strategy document:

```text
Strategy ID.*p15.provider-model.chatgpt-oauth.initial.v1
Selected provider.*openai-codex
Selected auth.*chatgpt_oauth
Subscription-backed route selected.*true
API-key route selected.*false
Selected model.*gpt-5.5
Mutable backend slug.*true
https://chatgpt.com/backend-api/codex
HERMES_CODEX_BASE_URL_inherited: false
OPENAI_BASE_URL_inherited: false
maximum_prompt_tokens: 32768
maximum_output_tokens: 4096
oauth_initiation_timeout_ms
complete_inference_timeout_ms
exact_marginal_request_cost
[ \t]+$
sk-[A-Za-z0-9_-]{20,}|sess-[A-Za-z0-9_-]{20,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}|BEGIN (RSA|OPENSSH|PRIVATE) KEY|access_token\s*[:=]\s*["']?[A-Za-z0-9_./+=-]{20,}|refresh_token\s*[:=]\s*["']?[A-Za-z0-9_./+=-]{20,}
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b|\borg-[A-Za-z0-9_-]+\b|\bproj_[A-Za-z0-9_-]+\b|\bws-[A-Za-z0-9_-]+\b|\bapp_[A-Za-z0-9_-]{10,}\b|\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b
gpt-5\.5-2026-[0-9]{2}-[0-9]{2}
```

The required-binding validations matched this document. The trailing-whitespace,
credential-value, account-specific identifier, and dated API snapshot scans
returned no matches.

No tests, builds, runtime gates, provider calls, credential checks, dependency
installs, register updates, Graphify updates, staging, commits or pushes are
performed for P15.0 because it is a strategy-record-only ticket.

## Final Decision

`openai-codex` with ChatGPT OAuth and model slug `gpt-5.5` is ready for the
next governed Hermes planning stage only under the constraints in this record:
fixed Codex backend endpoint, no endpoint override, no API-key route, no API
billing, no immutable API snapshot, no dynamic model replacement, no fallback,
no tools, no MCP, no streaming unless later authorized, no automatic retry, no
runtime execution, no credentials in P15.0, and no implementation without later
P15.1 through P15.R authorization.
