# Hermes 0.19 OpenAI Codex Single Worker Controlled Gate

Verdict: `hermes_0_19_openai_codex_single_worker_controlled_gate_ready_with_constraints`

## Scope

This governance record accepts only the P15.7 controlled-gate seam for one bounded OpenAI Codex ChatGPT OAuth worker request, one temporary credential projection, one streamed Responses dispatch and one bounded worker result.

It does not authorize production rollout, automatic retry, fallback, credential refresh, credential rotation, OAuth acquisition, model replacement, tool use, MCP use, usage API calls, quota API calls, billing API calls, Graphify execution or additional live requests.

## Explicit Authorizations

P15.7 had three explicit live authorizations.

First authorization:

- result: `failed`
- confirmed provider dispatches: `1`
- category: `request_invalid`
- root cause: `noncanonical_codex_backend_request_shape`
- automatic retries: `0`
- fallback calls: `0`
- cleanup: `passed`

The first request sent the previous non-canonical `max_output_tokens` wire field. The corrected gate delegates request formatting to the source-native Codex Responses builder with `is_codex_backend=true` and keeps output bounds local.

Second authorization:

- reported result: `blocked`
- originally reported category: `unknown`
- originally reported stage: `stream`
- originally reported dispatches: `0`
- retrospective runtime evidence: `insufficient`
- exact provider dispatches: `not_asserted`
- exact failure stage: `not_asserted`
- cleanup: `passed`

The second attempt is not rewritten as definitively pre-dispatch or post-dispatch. The historical uncertainty concerns only that attempt's dispatch counter and stage evidence, not the corrected implementation.

Third authorization:

- result: `completed`
- confirmed provider dispatches: `1`
- worker result state: `completed`
- exact output: `PEPPER_P15_7_OK`
- automatic retries: `0`
- fallback calls: `0`
- credential rotations: `0`
- OAuth attempts: `0`
- cleanup: `passed`

## Diagnostics Correction

The current gate records bounded diagnostics only:

- allowed checkpoint names;
- local failure phase;
- safe exception class and module names;
- provider dispatch counter;
- cleanup status.

It retains no raw provider bodies, headers, provider response IDs, credential metadata, tracebacks, prompts, outputs, host paths or account identity.

Corrected phase and counter ownership:

- pre-`responses.create` failures have dispatches `0` and phase `preflight` or `client_construction`;
- `responses.create` exceptions have dispatches `1` and phase `dispatch`;
- stream iterator exceptions after a returned stream have dispatches `1` and phase `stream`;
- terminal validation and accounting failures after a returned stream keep dispatches `1`;
- cleanup failures do not erase already observed dispatch counters.

The `stream` phase with dispatches `0` is rejected by the P15.7 diagnostics contract.

## Offline Substrate Qualification

The retained offline Docker substrate was qualified before the third live attempt:

- image tag: `pepper-agent:p15-m10-990d153cd370`
- image ID: `sha256:8e7d45adab5b5fa4b34a7c196929490521ac39d2d909e54d4866ddd772eebcfd`
- Python: `3.13.5`
- `openai`: `2.24.0`
- `pydantic`: `2.13.4`
- `httpx`: `0.28.1`
- source authority: mounted P15.7 working tree
- baked image source authority: `false`
- required imports: `passed`

Offline synthetic entrypoint qualification used the real `run_worker_stdio` entrypoint with fake provider streams and confirmed success, dispatch, stream, accounting, cleanup and zero-dispatch stream invariants without provider access.

## Third Live Request

The third live request used a new request identity, runtime identity, correlation identity, deterministic usage-record identity and one new lease identity. First-attempt and second-attempt identities were not reused.

The live prompt was:

```text
Reply with exactly: PEPPER_P15_7_OK
```

The fixed system instruction required an exact literal answer and prohibited tools, commentary, markdown, punctuation and additional text.

Observed bounded result:

- runtime entrypoint invoked: `true`
- stdin frames: `1`
- stdout envelopes: `1`
- stdout JSON parseable: `true`
- worker result state: `completed`
- exact output match: `true`
- provider dispatches: `1`
- `responses.create` calls: `1`
- event stream obtained: `true`
- stream iteration started: `true`
- first event observed: `true`
- terminal event observed: `true`
- accounting records: `1`
- failure records: `0`
- retry decisions: `0`
- automatic retries: `0`
- fallback calls: `0`
- credential refresh calls: `0`
- model-list calls: `0`
- tool calls: `0`
- MCP calls: `0`
- SDK retries: `0`

Observed checkpoints:

- `request_validated`
- `client_construction_started`
- `client_constructed`
- `dispatch_started`
- `event_stream_obtained`
- `stream_iteration_started`
- `first_event_observed`
- `terminal_event_observed`
- `accounting_started`
- `accounting_completed`
- `worker_result_completed`
- `cleanup_started`
- `cleanup_completed`

## Request Shape

The successful live request used the direct seam `client.responses.create(**create_kwargs)`.

Present wire keys:

- `model`
- `instructions`
- `input`
- `store`
- `reasoning`
- `include`
- `prompt_cache_key`
- `stream`

Required values:

- model: `gpt-5.5`
- store: `false`
- stream: `true`
- reasoning effort: `medium`

Absent wire keys:

- `max_output_tokens`
- `tools`
- `tool_choice`
- `parallel_tool_calls`
- `service_tier`
- `fallback_model`
- `caller_generation_overrides`
- `caller_timeout_overrides`
- `unsupported_body_headers`

The gate did not call `agent.codex_runtime.run_codex_stream`, `agent.codex_runtime.run_codex_create_stream_fallback`, conversation-loop retry helpers or fallback helpers.

## Accounting And Linkage

The third request created one P15.5 accounting record after dispatch.

Accounting result:

- outcome: `completed`
- worker-result/accounting link state: `matched`
- accounting provider call count: `1`
- worker result usage-record identity matched accounting: `true`
- worker result request identity matched accounting: `true`
- worker result runtime identity matched accounting: `true`
- worker result correlation identity matched accounting: `true`
- billing mode: `subscription_included`
- cost status: `included`
- exact marginal request cost: `unavailable`
- provider usage API called: `false`
- provider billing API called: `false`
- provider response ID retained: `false`
- raw usage retained: `false`
- reasoning trace retained: `false`

Provider usage was bounded to non-negative accounting fields. Zero token buckets mean unavailable or not observed for that specific bucket, not zero provider work.

## Docker Security Posture

The live provider-worker ran in the retained image with:

- outbound-only Docker networking;
- no published ports;
- host networking disabled;
- host PID namespace disabled;
- Docker socket absent;
- repository root absent;
- Git metadata absent;
- product source mounted read-only;
- projected credential home mounted read-only;
- durable credential store absent;
- read-only root filesystem;
- non-root container user;
- all capabilities dropped;
- `no_new_privileges` enabled;
- privileged mode disabled;
- bounded tmpfs;
- PID limit not greater than `128`;
- memory limit not greater than `2 GiB`;
- CPU limit not greater than `2`.

The credential controller created exactly one temporary projection from the governed durable store before the worker started. The worker container never mounted the durable credential store.

## Cleanup And Residue

Cleanup completed after the third live request:

- provider stream closed by the gate;
- worker container removed;
- exact temporary lease released;
- projected credential home removed;
- projected auth files: `0`;
- active leases: `0`;
- P15.7 Docker networks created: `0`;
- provider-worker containers remaining: `0`;
- credential-controller containers remaining: `0`;
- temporary virtualenvs: `0`;
- host listeners: `0`;
- durable credential retained;
- repository source unchanged.

The live worker emitted only bounded, secret-free local-state warnings caused by optional local state being unavailable under the read-only projected home. No provider response IDs, credentials, account identity or host paths were retained.

## Cumulative History

P15.7 cumulative bounded history:

- explicit authorizations: `3`
- attempts: `3`
- first attempt confirmed dispatches: `1`
- first attempt result: `failed`
- second attempt exact dispatches: `not_asserted`
- second attempt result: `blocked`
- second attempt retrospective evidence: `insufficient`
- third attempt confirmed dispatches: `1`
- third attempt result: `completed`
- cumulative confirmed provider dispatches minimum: `2`
- cumulative provider dispatches maximum possible: `3`
- cumulative exact provider dispatches: `not_asserted`
- cumulative successful inferences: `1`
- cumulative confirmed failed inferences minimum: `1`
- cumulative automatic retries: `0`
- cumulative fallback calls: `0`
- cumulative credential rotations: `0`
- cumulative OAuth attempts: `0`

Each explicitly authorized request had at most one dispatch. No attempt performed an automatic retry.

## Validation

Validated before this record:

- P15.7 targeted tests: `22 passed`
- P15.6 failure-policy tests: `56 passed`
- P15.5 accounting tests: `19 passed`
- provider regression tests: `119 passed`
- Ruff: `passed`
- offline Docker substrate qualification: `passed`
- source freeze: `passed`
- `git diff --check`: `passed`

Final validation after this record must confirm candidate count `11`, staged files `0`, this record present and no unexpected candidates.

## P15.7R Handoff

P15.7R may consume this controlled-gate result as evidence that the P15.7 source can perform one bounded OpenAI Codex ChatGPT OAuth request under Docker with exact output, matched accounting and no automatic retry or fallback.

P15.7R must still treat this as a constrained gate, not a production rollout. Any broader runtime integration, UI exposure, persisted evidence store, retry/resubmission workflow, credential lifecycle automation, model replacement handling or provider fleet behavior requires separate authorization.

## Residual Constraints

Residual constraints remain:

- no fourth live request is authorized by this record;
- no automatic retry or fallback authority is introduced;
- no OAuth, refresh or credential rotation authority is introduced;
- no raw provider evidence retention is authorized;
- no account-specific quota, billing or usage API lookup is authorized;
- no tool or MCP execution is authorized;
- no Graphify execution is authorized.
