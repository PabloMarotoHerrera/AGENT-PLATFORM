# AGENT PLATFORM Hermes OpenAI Codex Bounded Worker Profile

Status: P15.3 bounded worker profile candidate.

Final verdict: `hermes_openai_codex_bounded_worker_profile_ready_with_constraints`.

## Dynamic Start

- Dynamic start SHA: `8efab62965aafe9b74a90ef30893b433918e9c90`.
- `origin/main` at start: `8efab62965aafe9b74a90ef30893b433918e9c90`.
- Branch: `main`.
- Index empty at start: true.
- Tracked working tree clean at start: true.
- Allowed unrelated untracked paths: `.opencode/**`; `AGENTS.md`; `graphify-out/**`.
- Product tracked file count at start: `6236`.
- Modification register rows at start: `118`.
- Register baseline: columns `18`, duplicate IDs `0`, duplicate paths `0`, missing fields `0`, hash mismatches `0`.
- Graphify query/update/extract processes executed by P15.3: `0`.

## Candidate Set

Authorized candidate paths: 14.

- `0_architecture/governance/agent_platform_hermes_openai_codex_bounded_worker_profile.md`
- `10_scripts/hermes/agent_platform_openai_codex_worker_profile.py`
- `12_tests/hermes/test_agent_platform_openai_codex_worker_profile.py`
- `2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_worker/__init__.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_worker/enums.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_worker/contracts.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_worker/profiles.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_worker/resolution.py`
- `2_products/hermes-agent/hermes_cli/agent_platform/provider_worker/protocol.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_worker_contracts.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_worker_profiles.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_worker_resolution.py`
- `2_products/hermes-agent/tests/hermes_cli/test_agent_platform_provider_worker_protocol.py`

No other task-specific candidate path is authorized.

## Prerequisites

- P14 runtime-adapter closure was present with verdict `hermes_governed_runtime_adapter_closed_with_constraints`.
- P15.0 provider-model strategy was present with verdict `hermes_provider_model_strategy_ready_with_constraints`.
- P15.1 credential-delivery boundary was present with verdict `hermes_openai_codex_credential_delivery_boundary_ready_with_constraints`.
- P15.2 provider-runtime profile was present with verdict `hermes_openai_codex_provider_runtime_profile_ready_with_constraints`.
- P15.2 package import smoke passed for profile ID `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1`.
- Selected provider: `openai-codex`.
- Selected authentication: `chatgpt_oauth`.
- Selected transport: `codex_responses`.
- Selected model: `gpt-5.5`.
- Selected endpoint: `https://chatgpt.com/backend-api/codex`.
- Credential store ID: `openai-codex.primary`.
- P15.3 provider-worker package did not exist at prerequisite inspection.

## Architectural Role

P15.3 composes safe metadata only:

```text
P15.1 safe credential status and lease metadata
        -> P15.2 safe provider-runtime binding
        -> P15.3 bounded worker profile binding
```

The bounded worker profile is not a worker process. A validated request is not a provider call. A provider binding is not model entitlement. A result envelope is not proof that provider output is available.

P15.3 keeps the worker runtime-unverified and hands off authenticated inference to P15.4 and full worker lifecycle to P15.7.

## Public Contract Surface

The package root exports exactly these public names:

```text
PROVIDER_WORKER_PROFILE_SCHEMA_VERSION
ProviderWorkerProfileState
ProviderWorkerInputKind
ProviderWorkerOutputKind
ProviderWorkerFeaturePolicy
ProviderWorkerRequestState
ProviderWorkerResultState
ProviderWorkerFailureStage
ProviderWorkerOversizedRequestPolicy
ProviderWorkerExecutionPolicy
ProviderWorkerRequestPolicy
ProviderWorkerResultPolicy
ProviderWorkerTimeoutPolicy
BoundedProviderWorkerProfile
BoundedProviderWorkerRequest
BoundedProviderWorkerResult
BoundedProviderWorkerFailure
ProviderWorkerResolutionRequest
get_provider_worker_profile
list_provider_worker_profiles
list_provider_worker_profile_ids
```

The package root intentionally does not export:

```text
ResolvedProviderWorkerBinding
resolve_provider_worker_profile
serialize_worker_request
deserialize_worker_request
serialize_worker_result
deserialize_worker_result
operational errors
provider bindings
credential paths
process commands
```

## Worker Profile Identity

| Field | Value |
| --- | --- |
| Schema version | `1` |
| Worker profile ID | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Worker profile state | `profile_ready_runtime_unverified` |
| Successful internal resolved state | `ready_for_inference_gate` |
| Provider-runtime profile ID | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Credential store ID | `openai-codex.primary` |
| Worker process required | true |
| Inference gate required | true |
| Controlled lifecycle gate required | true |
| Runtime entitlement verified | false |
| Runtime transport verified | false |
| Worker runtime verified | false |

## Execution Policy

| Policy | Value |
| --- | ---: |
| Maximum concurrent workers | `1` |
| Maximum concurrent requests per worker | `1` |
| Maximum requests per worker lifetime | `1` |
| Request queue capacity | `0` |
| Provider calls per request maximum | `1` |
| Model-list calls per request maximum | `0` |
| Credential-refresh calls per request maximum | `0` |

Disabled feature posture:

- Process reuse: `disabled`.
- Persistent memory: `disabled`.
- Conversation history: `disabled`.
- Background tasks: `disabled`.
- Subworkers: `disabled`.
- Subagents: `disabled`.
- Hermes tools: `disabled`.
- Hosted tools: `disabled`.
- MCP: `disabled`.
- Streaming: `disabled`.
- Automatic retry: `disabled`.
- Automatic fallback: `disabled`.

## Request Policy

- Input kind: `text`.
- Maximum prompt tokens: `32768`.
- Reserved system-instruction tokens: `8192`.
- Maximum user-content tokens: `24576`.
- Maximum request UTF-8 bytes: `131072`.
- Maximum user-content UTF-8 bytes: `98304`.
- Oversized request policy: `fail_before_provider_call`.

Denied caller authority:

- Caller system instructions: false.
- Caller provider override: false.
- Caller model override: false.
- Caller endpoint override: false.
- Caller generation parameters: false.
- Caller timeout parameters: false.
- Caller tools: false.
- Caller metadata passthrough: false.

Required invariant:

```text
8192 + 24576 <= 32768
```

P15.3 performs byte-bound validation only. Exact token preflight remains P15.4.

## System Instruction Authority

- System instruction policy ID: `worker.system.openai-codex.p15-pilot.v1`.
- System instruction source: `tracked_internal_template`.
- Caller system instruction allowed: false.
- Frontend system instruction allowed: false.
- Provider-supplied system instruction allowed: false.

P15.3 does not define final instruction text. P15.4 may introduce the first synthetic inference-gate instruction under this tracked policy.

## Result Policy

- Output kind: `text`.
- Maximum output tokens: `4096`.
- Maximum output UTF-8 bytes: `32768`.
- Maximum result envelope UTF-8 bytes: `65536`.
- Raw provider response allowed: false.
- Reasoning trace allowed: false.
- Tool calls allowed: false.
- Stream chunks allowed: false.
- Provider headers allowed: false.
- Credential metadata allowed: false.
- Automatic file write allowed: false.
- Persistent output allowed: false.

The protocol accepts one bounded final text result or one bounded failure/cancellation envelope. P15.3 does not embed usage dictionaries or raw provider usage.

## Timeout Policy

| Timeout | Value |
| --- | ---: |
| `startup_timeout_ms` | `30000` |
| `connection_timeout_ms` | `10000` |
| `response_header_timeout_ms` | `30000` |
| `complete_inference_timeout_ms` | `120000` |
| `cancellation_deadline_ms` | `10000` |
| `worker_shutdown_deadline_ms` | `15000` |
| `maximum_worker_lifetime_ms` | `180000` |

Caller, frontend and environment timeout overrides are not allowed. P15.3 provider timeouts are equal to P15.2 maxima, never higher.

## Request, Result And Failure Contracts

`BoundedProviderWorkerRequest` carries schema version, request/profile/runtime/correlation/requester IDs, submitted UTC timestamp, text input kind and bounded user content. It does not carry system instructions, provider/model/endpoint overrides, generation parameters, timeout values, tool configuration, MCP configuration, streaming, retry, fallback, conversation history, repository paths, environment mappings, command data or binary attachments.

`repr(request)` excludes `user_content`.

`BoundedProviderWorkerResult` carries schema version, request/profile/runtime/correlation IDs, terminal state, completed UTC timestamp, text output kind, optional output text, optional usage record ID and optional failure. Completed results require output text and no failure. Failed results require failure and no output text. Cancelled results require cancellation-stage failure and no output text.

`repr(result)` excludes `output_text`.

`BoundedProviderWorkerFailure` carries schema version, stable failure code, bounded failure stage, `retryable=false` and bounded safe message only.

## Protocol Serialization

`provider_worker/protocol.py` implements deterministic in-memory serialization:

- UTF-8 JSON object only.
- Sorted keys.
- No JSONL stream.
- No multipart payload.
- No binary payload.
- No attachments.
- No compression.
- No logging.
- No file writes.
- No persistence.

Deserialization rejects invalid UTF-8, oversized payloads before parse, duplicate JSON object keys, multiple concatenated JSON values, unknown fields, `NaN` and `Infinity`.

## Resolver Behavior

`ProviderWorkerResolutionRequest` carries schema version, worker profile ID, safe P15.2 `ProviderRuntimeResolutionRequest` and evaluated UTC timestamp.

The internal `resolve_provider_worker_profile` composes only safe metadata. It calls the P15.2 internal resolver and then validates:

- worker profile exists;
- worker profile state is `profile_ready_runtime_unverified`;
- provider-runtime profile ID matches exactly;
- credential store is `openai-codex.primary`;
- provider is `openai-codex`;
- authentication is `chatgpt_oauth`;
- transport is `codex_responses`;
- model is `gpt-5.5`;
- worker concurrency is one;
- request concurrency is one;
- worker lifetime request count is one;
- queue capacity is zero;
- provider call maximum is one;
- model-list call maximum is zero;
- credential-refresh call maximum is zero;
- tools, hosted tools, MCP, streaming, retry, fallback, persistent memory and process reuse are disabled;
- token budgets match P15.2;
- timeout limits do not exceed P15.2.

Successful resolution returns internal `ResolvedProviderWorkerBinding` with `resolved_state="ready_for_inference_gate"`. It does not prove credential remote validity, account entitlement, model availability, transport compatibility, provider reachability, worker process functionality or inference success.

## Negative Authorization

P15.3 does not authorize:

- starting OAuth, browser login, device-code login, token refresh, logout or revocation;
- reading, writing, validating, printing, copying, importing or probing real provider credentials;
- acquiring a lease against the real credential store;
- reading host auth stores, Codex CLI auth stores, OS credential stores or credential environment variables;
- calling OpenAI, ChatGPT, Codex, Nous, GitHub Copilot, Anthropic, OpenRouter, xAI or any other provider/model-list/usage API;
- running inference;
- starting workers, agents, tools, MCP servers, lifecycle gates or runtime adapters;
- creating worker entrypoints, serve loops, stdin loops, socket servers, HTTP routes, queue consumers or provider clients;
- persisting prompts, outputs, conversation memory, result cache, checkpoints or sessions;
- changing Hermes provider source, credential source, provider-runtime source, runtime-adapter source, frontend source, manifests or lockfiles;
- modifying Graphify output or running Graphify update/extract/query processes.

## Validation Evidence

Interpreter:

`C:\Users\pablo\OneDrive\Escritorio\AGENT PLATFORM\2_products\hermes-agent\.venv\Scripts\python.exe`

Targeted P15.3 product tests:

- Command: product Python `-m pytest tests/hermes_cli/test_agent_platform_provider_worker_contracts.py tests/hermes_cli/test_agent_platform_provider_worker_profiles.py tests/hermes_cli/test_agent_platform_provider_worker_resolution.py tests/hermes_cli/test_agent_platform_provider_worker_protocol.py`.
- Result: `58 passed`.

P15.2 provider-runtime regression:

- Command: product Python `-m pytest` on the three P15.2 provider-runtime test files.
- Result: `33 passed`.

P15.1 provider-credential regression:

- Command: product Python `-m pytest` on the four P15.1 provider-credential and OAuth-acquisition test files.
- Result: `21 passed`.

Complete committed P14 runtime-adapter regression:

- Command: product Python `-m pytest` on all 15 `test_agent_platform_runtime_*.py` files accepted in P15.2.
- Result: `148 passed`.

Adjacent product regression:

- Command: product Python `-m pytest test_agent_platform_product_config.py test_agent_platform_product_routes.py`.
- Result: `16 passed`.

Runner tests:

- Command: product Python `-m pytest 12_tests/hermes/test_agent_platform_openai_codex_worker_profile.py`.
- Result: `4 passed`.

Read-only status runner:

- Command: product Python `10_scripts/hermes/agent_platform_openai_codex_worker_profile.py status`.
- Result: verdict `hermes_openai_codex_bounded_worker_profile_ready_with_constraints`, worker profile ID `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1`, provider-runtime profile ID `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1`, credential store `openai-codex.primary`, one worker, one request, zero queue, one provider call maximum and all feature flags false.

Import and API smokes:

- Import smoke: `provider-worker-import`.
- Internal resolver smoke: `resolve_provider_worker_profile`.
- Root export guard: `provider-worker-contract-root`.
- Exact `__all__`: passed for the accepted package-root public surface.

Static checks:

- Compileall: six package files, four product tests, runner and runner test passed.
- Product Ruff format check: 10 files already formatted.
- Product Ruff check: passed.
- Runner Ruff format check: 2 files already formatted.
- Runner Ruff check: passed.
- Windows footgun scanner: `No Windows footguns found (790 file(s) scanned).`
- `git diff --check`: whitespace errors `0`; only the existing TSV CRLF warning was emitted.

Register validator:

- rows: `128`;
- columns: `18`;
- duplicate IDs: `0`;
- duplicate paths: `0`;
- missing fields: `0`;
- hash mismatches: `0`;
- P15.3 rows: `10`;
- P15.3 IDs: `P15.3-001` through `P15.3-010`;
- P15.3 non-product rows: `0`.

Candidate audit:

- authorized candidates: `14`;
- changed candidates: `14`;
- unexpected candidates: `0`;
- missing candidates: `0`.

Product inventory:

- current tracked product files before commit: `6236`;
- new P15.3 product files: `10`;
- candidate product inventory after commit: `6246`.

Implementation and content safety:

- Product implementation package scan found credential-store reads `0`, network operations `0`, process launch markers `0`, environment reads `0` and persistence markers `0`.
- P15.3 candidate content scan found real credential values `0`, token values `0`, account identifiers `0`, auth-store paths `0`, credential-lease paths `0`, real prompts `0`, repository content dumps `0`, provider responses `0` and reasoning traces `0`.
- Runtime process scan found OAuth processes `0`, provider processes `0`, worker processes `0` and agent processes `0` attributable to P15.3.
- P15.3-attributable residue scan found artifact paths `0`, temporary auth stores `0`, temporary leases `0`, worker request files `0` and worker result files `0`.
- Generated Python cache residue: `0`.

Git state:

- HEAD: `8efab62965aafe9b74a90ef30893b433918e9c90`.
- `origin/main`: `8efab62965aafe9b74a90ef30893b433918e9c90`.
- Branch: `main`.
- Index: empty at implementation time.
- Staged files: none.
- Commits by agent: none.
- Pushes by agent: none.

Graphify:

- `graphify-out/graph.json` SHA-256 remained `02e3e4c8b32e77e6e71d8f6fdfb5cc647309b55713a3327c2534c2dace0291a2`.
- `graphify-out/provenance.json` SHA-256 remained `952a9f58997bb72974ef73a636d01800bf6f1c2862a6fa03044556d150ee6550`.
- Graphify commands executed during P15.3: `0`.
- No Graphify update was run under the P15.3 frozen-graph constraint.

## Register Reconciliation

`2_products/hermes-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` contains exactly ten P15.3 product rows:

- `P15.3-001` through `P15.3-010`.

No P15.3 register rows exist for:

- `0_architecture/**`;
- `10_scripts/**`;
- `12_tests/**`.

## Sequencing

- P15.3 is ready for human review after final validation.
- P15.4 remains blocked until P15.3 is committed.
- P15.4 owns the first authenticated tool-free inference.
- P15.5 owns usage and cost accounting.
- P15.7 owns the first complete governed worker lifecycle.
- Worker launch remains unauthorized.
- P17 WorkPacket execution remains unauthorized.

## Final Verdict

`hermes_openai_codex_bounded_worker_profile_ready_with_constraints`
