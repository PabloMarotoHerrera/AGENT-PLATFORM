# AGENT PLATFORM Hermes OpenAI Codex Provider Runtime Profile

Status: P15.2 provider-runtime profile candidate with public-contract drift correction applied.

Final verdict: `hermes_openai_codex_provider_runtime_profile_ready_with_constraints`.

## Dynamic Start

- Dynamic start SHA: `5d93876a658347b03d4ce127856f3aa255e7ca4a`.
- `origin/main` at start: `5d93876a658347b03d4ce127856f3aa255e7ca4a`.
- Branch: `main`.
- Index empty at start: true.
- Tracked working tree clean at start: true.
- Allowed unrelated untracked paths: `.opencode/**`; `AGENTS.md`; `graphify-out/**`.
- Product tracked file count at start: `6228`.
- Modification register rows at start: `110`.
- Register baseline: columns `18`, duplicate IDs `0`, duplicate paths `0`, missing fields `0`, hash mismatches `0`.

## Candidate Set

Authorized candidate paths: 12.

- `0_architecture/governance/agent_platform_hermes_openai_codex_provider_runtime_profile.md`
- `10_scripts/hermes/agent_platform_openai_codex_provider_profile.py`
- `12_tests/hermes/test_agent_platform_openai_codex_provider_profile.py`
- `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_runtime/__init__.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_runtime/enums.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_runtime/contracts.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_runtime/profiles.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_runtime/resolution.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_runtime_contracts.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_runtime_profiles.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_runtime_resolution.py`

No other task-specific candidate path is authorized.

## Prerequisites

- P14 runtime-adapter closure was present with verdict `hermes_governed_runtime_adapter_closed_with_constraints`.
- P15.0 provider-model strategy was present with verdict `hermes_provider_model_strategy_ready_with_constraints`.
- P15.0 selected provider: `openai-codex`.
- P15.0 selected auth: `chatgpt_oauth`.
- P15.0 selected endpoint: `https://chatgpt.com/backend-api/codex`.
- P15.0 selected model: `gpt-5.5`.
- P15.1 credential-delivery boundary was present with verdict `hermes_openai_codex_credential_delivery_boundary_ready_with_constraints`.
- P15.1 fixed credential store ID: `openai-codex.primary`.
- P15.1 maximum active credential leases: `1`.
- P15.1 maximum lease TTL: `900000` ms.
- P15.1 minimum remaining credential lifetime: `300000` ms.

## Runtime Profile Identity

P15.2 adds profile-only metadata, not live runtime integration.

| Field | Value |
| --- | --- |
| Schema version | `1` |
| Profile ID | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Strategy ID | `p15.provider-model.chatgpt-oauth.initial.v1` |
| Provider enum value | `ProviderRuntimeProvider.OPENAI_CODEX = "openai-codex"` |
| Hermes provider ID | `openai-codex` |
| Provider label | `OpenAI Codex` |
| Authentication enum value | `ProviderRuntimeAuthentication.CHATGPT_OAUTH = "chatgpt_oauth"` |
| Credential store ID | `openai-codex.primary` |
| Endpoint | `https://chatgpt.com/backend-api/codex` |
| Endpoint source | `DEFAULT_CODEX_BASE_URL` |
| Model ID | `gpt-5.5` |
| Model identifier kind | `mutable_backend_slug` |
| Transport enum value | `ProviderRuntimeTransport.CODEX_RESPONSES = "codex_responses"` |
| Public profile state | `runtime_unverified` |
| Internal successful binding state | `ready_for_worker_profile` |

## Endpoint Policy

The P15.2 profile pins the Codex backend endpoint from Hermes source and rejects every endpoint override source.

- Base URL override allowed: false.
- Caller endpoint allowed: false.
- Frontend endpoint allowed: false.
- Config endpoint allowed: false.
- Custom-provider endpoint allowed: false.
- Proxy endpoint allowed: false.
- Aggregator endpoint allowed: false.

The public resolution request exposes no endpoint field. Strict public models reject extra endpoint metadata before the internal resolver runs because P15.2 does not authorize caller, config, frontend, environment, alias or custom-provider endpoint authority.

## Model, Generation And Usage Policy

- Selected model: `gpt-5.5`.
- Immutable snapshot: false.
- Mutable backend slug: true.
- Dynamic model replacement: false.
- Live model-list replacement: false.
- Fallback model: none.
- Maximum prompt tokens: `32768`.
- Reserved system-instruction tokens: `8192`.
- Maximum user-content tokens: `24576`.
- Maximum output tokens: `4096`.
- Reasoning effort: `medium`.
- Oversized request posture: `fail_before_provider_call`.
- Streaming: `disabled`.
- Hermes tools: `disabled`.
- MCP: `disabled`.
- Automatic retry: `disabled`.
- Automatic fallback: `disabled`.

Usage evidence is classified without granting runtime authority:

- Input tokens: `provider_reported_when_available`.
- Cached input tokens: `provider_reported_when_available`.
- Output tokens: `provider_reported_when_available`.
- Total tokens: `provider_reported_or_locally_summed`.
- Returned model ID: `provider_reported`.
- Finish reason: `provider_reported_when_available`.
- Provider request ID: `provider_reported_when_safe`.
- Elapsed time: `locally_derived`.
- Subscription quota signal: `account_specific_when_exposed`.
- Credit consumption signal: `account_specific_when_exposed`.
- Exact marginal request cost: `unavailable_by_default`.

Required invariant verified in contracts:

```text
8192 + 24576 <= 32768
```

## Timeout Policy

| Timeout | Value |
| --- | ---: |
| `connection_timeout_ms` | `10000` |
| `response_header_timeout_ms` | `30000` |
| `complete_inference_timeout_ms` | `120000` |
| `cancellation_deadline_ms` | `10000` |

Caller timeout overrides are not allowed. SDK default timeouts are not accepted by the profile.

OAuth initiation, polling and refresh timeouts remain P15.1/P15.4 concerns. Worker shutdown and process lifecycle values are intentionally not implemented in P15.2 because this ticket is a provider-runtime profile only, not a worker or runtime-adapter profile.

## Public Contract Surface

The package root exports exactly these public names:

```text
PROVIDER_RUNTIME_PROFILE_SCHEMA_VERSION
ProviderRuntimeProvider
ProviderRuntimeAuthentication
ProviderRuntimeTransport
ProviderModelIdentifierKind
ProviderRuntimeProfileState
ProviderFeaturePolicy
ProviderUsageEvidenceSource
ProviderEndpointPolicy
ProviderModelPolicy
ProviderCredentialRequirement
ProviderGenerationPolicy
ProviderTimeoutPolicy
ProviderUsageEvidencePolicy
ProviderRuntimeProfile
ProviderRuntimeResolutionRequest
get_provider_runtime_profile
list_provider_runtime_profiles
list_provider_runtime_profile_ids
```

The package root intentionally does not export these legacy or internal names:

```text
ResolvedProviderRuntimeBinding
resolve_provider_runtime_profile
ProviderRuntimeResolution
ProviderRuntimeAuthKind
ProviderRuntimeBillingRoute
ProviderRuntimeCredentialPolicy
ProviderRuntimeExecutionPolicy
ProviderRuntimeIdentity
ProviderRuntimeOverrideSource
ProviderRuntimeRequestPolicy
```

The public registry functions are `get_provider_runtime_profile`, `list_provider_runtime_profiles`, and `list_provider_runtime_profile_ids`. They expose exactly one immutable profile ID: `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1`.

## Resolver Behavior

`ProviderRuntimeResolutionRequest` is the public, strict, secret-free input model for internal provider-runtime metadata resolution. It carries only schema/profile identity, runtime/correlation/request metadata, and caller-supplied P15.1 credential status plus delivery-lease metadata.

`resolve_provider_runtime_profile`, `ProviderRuntimeResolutionError`, and `ResolvedProviderRuntimeBinding` are internal-only names imported from implementation modules, not from the package root. The resolver does not read tokens, auth stores, lease directories, environment variables or provider state.

It rejects:

- unknown profile IDs;
- extra provider, model, endpoint, tool, hosted-tool, MCP, streaming, retry or fallback metadata through strict public models;
- non-one credential counts;
- unconfigured credential metadata;
- invalid durable-store or protection metadata;
- missing token-pair presence metadata;
- missing credential-expiry metadata;
- expired credential metadata;
- inactive lease metadata;
- expired lease metadata;
- insufficient remaining credential lifetime for the lease;
- runtime mismatch;
- correlation mismatch;
- credential-store mismatch;
- provider mismatch.

Successful worker-readiness resolution returns an internal `ResolvedProviderRuntimeBinding` with `resolved_state="ready_for_worker_profile"` and still claims no remote token validity, model entitlement, transport success or provider reachability.

Resolver error messages intentionally do not echo rejected endpoint strings, tool payloads, credential paths or token-like values.

## Hermes Source Evidence

- `hermes_cli/auth.py` defines `DEFAULT_CODEX_BASE_URL = "https://chatgpt.com/backend-api/codex"` and registers `PROVIDER_REGISTRY["openai-codex"]` with `auth_type="oauth_external"` and that inference base URL.
- `hermes_cli/providers.py` maps `HERMES_OVERLAYS["openai-codex"]` to `transport="codex_responses"`, `auth_type="oauth_external"`, and `base_url_override="https://chatgpt.com/backend-api/codex"`.
- `hermes_cli/codex_models.py` starts `DEFAULT_CODEX_MODELS` with `"gpt-5.5"`.
- `hermes_cli/runtime_provider.py` sets `api_mode="codex_responses"` for `provider == "openai-codex"` and defaults the base URL to `DEFAULT_CODEX_BASE_URL`.
- `agent/transports/codex.py` builds Responses API kwargs with `model`, `instructions`, `input`, `store=False`, optional reasoning/include/cache fields, and only includes `tools` when response tools are non-empty.
- `agent/usage_pricing.py` treats `openai-codex` usage as `subscription_included`.

## Negative Authorization

P15.2 does not authorize:

- starting OAuth, browser login, device-code login, token refresh, logout or revocation;
- reading, writing, validating, printing, copying, importing or probing provider credentials;
- reading host auth stores, Codex CLI auth stores, OS credential stores or credential environment variables;
- calling OpenAI, ChatGPT, Codex, Nous, GitHub Copilot, Anthropic, OpenRouter, xAI or any other provider/model-list/usage API;
- running inference;
- starting workers, agents, tools, MCP servers, lifecycle gates or runtime adapters;
- changing Hermes provider source, credential source, runtime-adapter source, frontend source, manifests or lockfiles;
- enabling fallback providers, API-key fallback, automatic provider routing, dynamic model replacement, streaming, hosted tools, Hermes tools, MCP or automatic retry.

## Validation Evidence

Interpreter:

`C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent\.venv\Scripts\python.exe`

Targeted P15.2 product tests:

- Command: product Python `-m pytest tests/hermes_cli/test_agent_platform_provider_runtime_contracts.py tests/hermes_cli/test_agent_platform_provider_runtime_profiles.py tests/hermes_cli/test_agent_platform_provider_runtime_resolution.py`.
- Result: `33 passed`.

Full P15.1 provider-credential regression:

- Command: product Python `-m pytest` on the four P15.1 provider-credential and OAuth-acquisition test files.
- Result: `21 passed`.

Complete committed P14 runtime-adapter regression:

- Command: product Python `-m pytest` on all 15 `test_agent_platform_runtime_*.py` files accepted in P15.1.
- Final result: `148 passed`, `0 skipped`, `0 failed`.
- Note: the first complete rerun hit one transient `PROCESS-001` conformance process-harness failure; the immediate rerun of the same full 15-file lane passed.

Adjacent product regression:

- Command: product Python `-m pytest test_agent_platform_product_config.py test_agent_platform_product_routes.py`.
- Result: `16 passed`.

Runner tests:

- Command: product Python `-m pytest 12_tests/hermes/test_agent_platform_openai_codex_provider_profile.py`.
- Result: `3 passed`.

Read-only status runner:

- Command: product Python `10_scripts/hermes/agent_platform_openai_codex_provider_profile.py status`.
- Result: `status=passed`, verdict `hermes_openai_codex_provider_runtime_profile_ready_with_constraints`.
- Evidence flags: `auth_default_endpoint_matches_profile=true`, `overlay_endpoint_matches_profile=true`, `overlay_transport=codex_responses`, `profile_transport_matches_overlay=true`, `codex_catalog_contains_model=true`, `codex_catalog_first_model=gpt-5.5`.
- Public API flags: exact root `__all__` present, forbidden root exports absent, registry profile count `1`.

Ruff:

- Product Ruff format check: 8 files already formatted.
- Product Ruff check: passed.
- Runner Ruff format check: 2 files already formatted.
- Runner Ruff check: passed.

Compileall:

- Product candidate compileall: 8 product Python files, passed.
- Runner compileall: 2 Python files, passed.

Import smoke:

- Result: `import_smoke=passed`.
- Internal resolver smoke: `internal_resolver_smoke=passed` for internal `resolve_provider_runtime_profile`.
- Exact root export smoke: `exact_root_all_smoke=passed` for the accepted package-root `__all__` list.
- Forbidden root export guard: `root_forbidden_export_guard=passed`; `ResolvedProviderRuntimeBinding`, `resolve_provider_runtime_profile` and legacy aliases are not exported from the package root.

Windows footgun scanner:

- Command: product Python `scripts/check-windows-footguns.py --all`.
- Result: `No Windows footguns found (784 file(s) scanned).`

Register validator:

- rows: `118`;
- columns: `18`;
- duplicate IDs: `0`;
- duplicate paths: `0`;
- missing fields: `0`;
- hash mismatches: `0`;
- P15.2 rows: `8`.

Candidate audit:

- authorized candidates: `12`;
- changed candidates: `12`;
- unexpected candidates: `0`;
- missing candidates: `0`.

Product inventory:

- current tracked product files before commit: `6228`;
- new P15.2 product files: `8`;
- candidate product inventory after commit: `6236`.

Implementation residue scan:

- Product implementation package scan found no operational credential, provider-call, environment-token, process-launch or Codex auth-store authority markers.
- Source-safety value scan found token values `0`, credential values `0`, account identifiers `0`, auth-store paths in public models `0`, lease paths in public models `0`, network operations `0`, provider calls `0`, model-list calls `0`, inference calls `0`.
- Status-runner forbidden-activity counters found OAuth started `false`, worker started `false`, agent started `false`, provider calls `0`, model-list calls `0`, inference calls `0` and real credential reads `0`.
- P15.2-attributable residue scan found artifact paths `0`, auth.json files `0`, temporary auth stores `0` and temporary credential leases `0`. Pre-existing `9_artifacts/hermes/p12.4` test residue was present and not attributed to P15.2.

Git state:

- HEAD: `5d93876a658347b03d4ce127856f3aa255e7ca4a`.
- `origin/main`: `5d93876a658347b03d4ce127856f3aa255e7ca4a`.
- Branch: `main`.
- Index: empty.
- Tracked changes: `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` only.
- New task files: the 11 non-register candidate paths listed above.
- Pre-existing unrelated untracked paths remain: `.opencode/`, `AGENTS.md`, `graphify-out/`.

Graphify:

- `graphify-out/graph.json` SHA-256 remained `02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2`.
- `graphify-out/provenance.json` SHA-256 remained `952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550`.
- Graphify commands executed during this validation pass: `0`.
- No Graphify update was run under the P15.2 frozen-graph constraint.

## Register Reconciliation

`2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` contains exactly eight P15.2 product rows:

- `P15.2-001` through `P15.2-008`.

No P15.2 register rows exist for:

- `0_architecture/**`;
- `10_scripts/**`;
- `12_tests/**`.

## Final Verdict

`hermes_openai_codex_provider_runtime_profile_ready_with_constraints`
