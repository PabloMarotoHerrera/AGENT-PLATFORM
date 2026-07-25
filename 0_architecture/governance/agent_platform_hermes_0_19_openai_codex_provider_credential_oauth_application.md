# AGENT PLATFORM Hermes 0.19 OpenAI Codex Provider Credential OAuth Application

Status: P15.M8 provider and credential migration candidate for human review.

Final verdict: `hermes_0_19_openai_codex_provider_credential_oauth_application_ready_with_constraints`.

Verdict meaning: implementation and dry-run boundary readiness only. This verdict does not claim live OAuth, real credential configuration, real provider reachability, a real delivery lease, worker execution or successful inference.

## Dynamic Start

- Dynamic start SHA: `d2a985e580ee908b309c8468f4ebeee8fafdcb3b`.
- `origin/p15.m-hermes-0.19-migration` at start: `d2a985e580ee908b309c8468f4ebeee8fafdcb3b`.
- Branch: `p15.m-hermes-0.19-migration`.
- Index empty at start: true.
- Tracked working tree clean at start: true.
- P15.M8 migration authorization: no real credential read, OAuth, provider call or inference.
- Graphify commands executed during P15.M8: `0`.

## Candidate Set

Authorized P15.M8 candidate paths: 32.

- `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_oauth_application.md`
- `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_manifest.tsv`
- `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_credentials/__init__.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_credentials/contracts.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_credentials/client_tokens.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_credentials/store.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_credentials/delivery.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_credentials/oauth_acquisition.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_credential_contracts.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_client_tokens.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_credential_store.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_credential_delivery.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_openai_codex_oauth_acquisition.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_runtime/__init__.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_runtime/enums.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_runtime/contracts.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_runtime/profiles.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_runtime/resolution.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_runtime_contracts.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_runtime_profiles.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_runtime_resolution.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker/__init__.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker/enums.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker/contracts.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker/profiles.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker/resolution.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_worker/protocol.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_worker_contracts.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_worker_profiles.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_worker_resolution.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_worker_protocol.py`

No other task-specific candidate path is authorized.

## Prerequisites

- P15.0 provider-model strategy was present with verdict `hermes_provider_model_strategy_ready_with_constraints`.
- P15.1 credential-delivery boundary was present with verdict `hermes_openai_codex_credential_delivery_boundary_ready_with_constraints`.
- P15.2 provider-runtime profile was present with verdict `hermes_openai_codex_provider_runtime_profile_ready_with_constraints`.
- P15.3 bounded worker profile was present with verdict `hermes_openai_codex_bounded_worker_profile_ready_with_constraints`.
- P15.M7R Pepper product identity and governed runtime-adapter post-commit integrity closures were present.
- Pre-mutation Pepper baseline integrity and governance integrity tests passed before P15.M8 mutation.

## Fixed Provider Selection

| Field | Value |
| --- | --- |
| Strategy ID | `p15.provider-model.chatgpt-oauth.initial.v1` |
| Provider | `openai-codex` |
| Authentication | `chatgpt_oauth` |
| Endpoint | `https://chatgpt.com/backend-api/codex` |
| Model | `gpt-5.5` |
| Transport | `codex_responses` |
| Credential store ID | `openai-codex.primary` |
| Provider runtime profile ID | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Worker profile ID | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |

Denied provider authority:

- API-key route;
- fallback providers or fallback models;
- automatic retry;
- streaming;
- tools, hosted tools or MCP;
- model-list calls;
- endpoint, model, generation or timeout overrides;
- live provider calls or inference in P15.M8.

## Authority State

P15.M8 distinguishes implemented contract capability from real credential configuration.

| Authority | P15.M8 state |
| --- | --- |
| Implemented credential contract capability | ready with constraints |
| Real credential configuration | not configured |
| Dry-run OAuth boundary | validated |
| Live OAuth completion | not attempted |
| Provider-runtime profile readiness | ready, runtime unverified |
| Provider reachability | not claimed |
| Bounded-worker profile readiness | ready, worker unexecuted |
| Worker execution | not attempted |

Required live-state counters:

| Counter | Value |
| --- | ---: |
| `live_OAuth_attempts` | `0` |
| `real_credentials_read` | `0` |
| `real_credentials_written` | `0` |
| `real_durable_store_created` | `false` |
| `real_delivery_lease_created` | `false` |
| `provider_calls` | `0` |
| `inference_calls` | `0` |
| `model_list_calls` | `0` |
| `usage_calls` | `0` |
| `worker_starts` | `0` |
| `agent_starts` | `0` |

Future live owner:

| Future action | Owner |
| --- | --- |
| Live OAuth and inference revalidation | `P15.M11` |

## Credential Store Application

P15.M8 migrates the P15.1 credential boundary onto Hermes Agent 0.19.0 source with a pool-only durable store adaptation. This is implemented contract capability, not evidence that a real credential is configured.

Durable store policy:

- exactly one governed `credential_pool.openai-codex` entry when a trusted synthetic or future governed store is supplied;
- entry ID `openai-codex.primary`;
- `auth_type = oauth`;
- no account rotation or account switching;
- no singleton `providers.openai-codex.tokens` mirror retained;
- singleton `device_code` source suppressed from the governed durable store;
- existing durable stores are rejected before promotion;
- Windows broad principals and unprotected POSIX modes fail closed.

P15.M8 does not claim a real credential count of one, real token expiry, real account entitlement, real remote token validity or a real durable store.

Client-token policy:

- access-token values remain `SecretStr` only;
- public metadata exposes no token bytes;
- JWT-like expiry metadata may be derived without validating signatures;
- `signature_validation_claimed = false` is explicit.

Lease policy:

- maximum active leases: `1`;
- maximum lease TTL: `900000` ms;
- minimum remaining credential lifetime: `300000` ms;
- public lease references are pathless and token-free;
- internal projection is trusted composition only;
- release validates runtime ID, correlation ID, store ID and provider ID.

## OAuth Acquisition Boundary

Locked Hermes 0.19 command shape:

```text
python -m hermes_cli.main auth add openai-codex --type oauth
```

P15.M8 did not run live OAuth because the P15.M8 migration authorization prohibits OAuth and real credential reads. The P15.M8 product boundary validates only fixed argv construction, isolated environment projection, dry-run default behavior, synthetic credentials and explicit injected-executor behavior.

Dry-run smoke result:

```text
imports=passed credential_exports=21 runtime_exports=19 worker_exports=21 oauth_execution_attempted=False oauth_completed=False argv_suffix=-m hermes_cli.main auth add openai-codex --type oauth
```

Dry-run OAuth boundary validation is not live OAuth completion. P15.M11 owns the first tool-free live OAuth and inference revalidation.

## Runtime And Worker Application

P15.M8 migrates the P15.2 provider-runtime metadata and P15.3 bounded-worker metadata into Pepper without starting a provider runtime or worker process.

Provider runtime profile ready is not provider reachable. Bounded worker profile ready is not worker executed.

Provider-runtime result:

- one immutable profile ID: `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1`;
- endpoint pinned to `https://chatgpt.com/backend-api/codex`;
- transport pinned to `codex_responses`;
- selected model pinned to mutable backend slug `gpt-5.5`;
- successful internal resolution state remains `ready_for_worker_profile`;
- runtime entitlement, token remote validity, transport success and provider reachability remain unverified.

Bounded-worker result:

- one immutable profile ID: `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1`;
- maximum workers `1`, maximum concurrent requests `1`, queue capacity `0`;
- maximum provider calls per request `1`;
- model-list calls per request `0`;
- credential-refresh calls per request `0`;
- tools, hosted tools, MCP, streaming, retry, fallback, process reuse and persistent memory disabled;
- successful internal resolution state remains `ready_for_inference_gate`;
- worker start, inference and provider output remain unverified.

## Validation Evidence

Interpreter:

```text
Python 3.12.3 from the available user environment; no product-local .venv exists in this checkout.
```

P15.M8 targeted product tests:

- Command: `python -m pytest` on the 12 P15.M8 provider credential, client-token, OAuth acquisition, provider-runtime and provider-worker test files.
- Result: `119 passed, 3 warnings`.
- Warnings: existing Pydantic protected-namespace warnings for bounded `model_*` field names.

Warning classification:

| Warning counter | Value |
| --- | ---: |
| `warnings_total` | `3` |
| `credential_or_token_leak_warning` | `0` |
| `security_boundary_warning` | `0` |
| `unhandled_resource_warning` | `0` |
| `unexpected_deprecation_warning` | `0` |
| `warnings_affecting_acceptance` | `0` |

Warning details:

| Originating module | Category | Bounded message |
| --- | --- | --- |
| `hermes_cli/agent_platform/provider_runtime/contracts.py` | `UserWarning` from `pydantic._internal._fields:161` | Field `model_id` conflicts with protected namespace `model_`; no credential or token content. |
| `hermes_cli/agent_platform/provider_runtime/contracts.py` | `UserWarning` from `pydantic._internal._fields:161` | Field `model_policy` conflicts with protected namespace `model_`; no credential or token content. |
| `hermes_cli/agent_platform/provider_worker/contracts.py` | `UserWarning` from `pydantic._internal._fields:161` | Field `model_list_calls_per_request_maximum` conflicts with protected namespace `model_`; no credential or token content. |

Adjacent regressions:

- Product config command: `python -m pytest tests/hermes_cli/test_agent_platform_product_config.py`.
- Product config result: `10 passed`.
- Runtime adapter command: `python -m pytest` on the 15 P15.M7 runtime-adapter test files.
- Runtime adapter result: `143 passed, 5 skipped`.
- Runtime adapter first full attempt hit transient `PROCESS-001` conformance failure; no implementation changed; immediate complete rerun passed.
- Product routes command attempted with product config/routes together.
- Product routes result: blocked by environment, `ModuleNotFoundError: No module named 'fastapi'`, because no product-local `.venv` exists and the available interpreter lacks FastAPI.

Runtime-adapter skip classification:

| Skip counter | Value |
| --- | ---: |
| `runtime_adapter_passed` | `143` |
| `runtime_adapter_skipped` | `5` |
| `unexpected_skips` | `0` |
| `skips_hiding_contract_failure` | `0` |
| `skips_hiding_process_cleanup_failure` | `0` |
| `skips_hiding_environment_failure` | `0` |
| `skips_hiding_containment_failure` | `0` |

Skipped runtime-adapter test IDs:

| Test ID | Reason |
| --- | --- |
| `tests/hermes_cli/test_agent_platform_runtime_workspace.py::test_workspace_paths_are_contained_and_symlink_workspace_root_rejected` | Host does not allow directory symlink creation. |
| `tests/hermes_cli/test_agent_platform_runtime_path_containment.py::test_trusted_base_root_rejects_symlink_and_reparse_point` | Host does not allow directory symlink creation. |
| `tests/hermes_cli/test_agent_platform_runtime_path_containment.py::test_symlink_redirect_rejected_even_when_target_is_inside_root` | Host does not allow directory symlink creation. |
| `tests/hermes_cli/test_agent_platform_runtime_rollback.py::test_oversized_and_symlink_marker_are_rejected_without_deleting` | Symlink creation unavailable. |
| `tests/hermes_cli/test_agent_platform_runtime_rollback.py::test_safe_preflight_rejects_redirects_special_files_depth_and_entry_bounds` | Symlink creation unavailable. |

Static checks:

- Ruff check on 29 P15.M8 Python files: passed.
- Ruff format check on 29 P15.M8 Python files: `29 files already formatted`.
- `python -m py_compile` on 29 P15.M8 Python files: passed.
- Windows footgun scanner: `No Windows footguns found (821 file(s) scanned)`.
- `git diff --check`: passed with no output.

Import and API smoke:

- Provider credential package import: passed.
- Provider runtime package import: passed.
- Provider worker package import: passed.
- Public root export counts: credential `21`, runtime `19`, worker `21`.
- OAuth acquisition smoke: dry-run only, execution not attempted.

Static safety scan:

- Provider credential and runtime packages contain no `subprocess`, browser, HTTP client, environment-token, socket, FastAPI or route-authority markers.
- Provider worker package scan produced only benign `requests` substrings in worker policy names and comments.
- Governed credential package retains expected internal `auth.json` and `credential_pool` handling only.

Cache and residue scan:

- P15.M8-attributable `__pycache__`: `0` found under `2_products/pepper-agent`.
- P15.M8-attributable `.pytest_cache`: `0` found under `2_products/pepper-agent`.
- Temporary OAuth smoke path: not created.
- Real auth stores read or written: `0`.
- Real durable store created: false.
- Real delivery lease created: false.
- Provider/model-list/usage/inference calls: `0`.
- Worker or agent starts: `0`.

## Register And Manifest Reconciliation

`2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv` state after P15.M8 append:

- rows: `87`;
- columns: `18`;
- duplicate IDs: `0`;
- duplicate paths: `0`;
- missing fields: `0`;
- P15.M8 rows: `29`;
- P15.M8 IDs: `P15.M8-001` through `P15.M8-029`;
- P15.M8 hash mismatches: `0`.

Corrected whole-register validation using exact committed Git blob bytes for all pre-P15.M8 rows:

- pre-P15.M8 `HEAD` blob hash mismatches: `0`;
- P15.M8 candidate hash mismatches: `0`;
- invalid classifications: `0`;
- missing files: `0`;
- unregistered P15.M8 product files: `0`;
- P15.M8 register rows without product file: `0`.

Specific P15.M6 normalization check:

| Modification ID | Path | Recorded SHA-256 | Exact `HEAD` blob SHA-256 | Working tree differs | Difference only checkout line-ending normalization |
| --- | --- | --- | --- | --- | --- |
| `P15.M6-002` | `hermes_cli/web_server.py` | `d08e29db31bb044f248e1593ddb06db486e6b04f9f05144f6daba421fc04c46e` | `d08e29db31bb044f248e1593ddb06db486e6b04f9f05144f6daba421fc04c46e` | true | true |
| `P15.M6-020` | `web/src/main.tsx` | `fc83d0f55f392c936231725731ff55deabb6f70b624c5aa6b5ff9cbb8bfd3dc9` | `fc83d0f55f392c936231725731ff55deabb6f70b624c5aa6b5ff9cbb8bfd3dc9` | true | true |
| `P15.M6-021` | `web/src/App.tsx` | `8ca66b772754824ac4ecada6f11c20ea8af518657bb3d272daef7d86d4987972` | `8ca66b772754824ac4ecada6f11c20ea8af518657bb3d272daef7d86d4987972` | true | true |

`0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_manifest.tsv` state:

- rows: `29`;
- columns: `23`;
- duplicate record IDs: `0`;
- duplicate product paths: `0`;
- blank mandatory fields: `0`;
- invalid component families: `0`;
- invalid component roles: `0`;
- invalid reapplication classifications: `0`;
- register-manifest ID mismatches: `0`;
- register-manifest path mismatches: `0`;
- register-manifest hash mismatches: `0`;
- unverified records: `0`;
- live OAuth claim violations: `0`.

No P15.M8 register rows exist for:

- `0_architecture/**` governance records;
- source-authority files under `2_products/hermes-agent/**`.

## Git State

Current git state at record creation:

- HEAD: `d2a985e580ee908b309c8468f4ebeee8fafdcb3b`.
- `origin/p15.m-hermes-0.19-migration`: `d2a985e580ee908b309c8468f4ebeee8fafdcb3b`.
- Branch: `p15.m-hermes-0.19-migration`.
- Staged files: none.
- Commits by agent: none.
- Pushes by agent: none.
- Modified tracked file: `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv`.
- New task files: 31 untracked P15.M8 candidate files, including this governance record, the manifest and 29 product files.

## Handoff

- P15.M8 is ready for human review and commit after reviewer acceptance.
- P15.M8R must perform post-commit implementation integrity closure after the human commit, not live OAuth validation.
- P15.M11 owns the first live OAuth, credential remote validation and tool-free inference revalidation.
- P15.M8 does not authorize API-key fallback, model-list probing, provider calls, inference, worker start, agent start, tools, MCP, streaming expansion, fallback, automatic retry, Graphify mutation, staging, committing or pushing.

## Final Verdict

`hermes_0_19_openai_codex_provider_credential_oauth_application_ready_with_constraints`
