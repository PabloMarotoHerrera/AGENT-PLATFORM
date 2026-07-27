# AGENT PLATFORM Hermes 0.19 OpenAI Codex Usage Cost Timeout Accounting

Status: P15.5 usage, cost and timeout accounting candidate for human review.

Final verdict: `hermes_0_19_openai_codex_usage_cost_timeout_accounting_ready_with_constraints`.

Verdict meaning: contract and synthetic-fixture readiness only. This verdict does not claim live provider execution, real usage retrieval, billing retrieval, quota retrieval, worker execution, runtime activation, credential reads or product activation.

## Dynamic Start

- Branch: `p15.m-hermes-0.19-migration`.
- P15.MR authority present at start: yes.
- P15.MR accepted next ticket: P15.5 - Usage, Cost and Timeout Accounting.
- Worktree/index before P15.5 mutation: clean.
- P15.5 VPS dependency: none.

## Candidate Set

Authorized P15.5 candidate paths: 11.

- `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_usage_cost_timeout_accounting.md`
- `2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv`
- `2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_accounting/__init__.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_accounting/enums.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_accounting/contracts.py`
- `2_products/pepper-agent/hermes_cli/agent_platform/provider_accounting/accounting.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_accounting_contracts.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_accounting_normalization.py`
- `2_products/pepper-agent/tests/hermes_cli/test_agent_platform_provider_timeout_accounting.py`
- `2_products/pepper-agent/docs/agent-platform/provider_usage_cost_timeout_accounting.md`

Created product files: 8. Modified product files: 2. Created governance records: 1.

## Fixed Accounting Selection

| Field | Value |
| --- | --- |
| Accounting policy ID | `accounting.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Provider runtime profile ID | `provider.openai-codex.chatgpt-oauth.gpt-5.5.v1` |
| Worker profile ID | `worker.openai-codex.chatgpt-oauth.gpt-5.5.single-request.v1` |
| Provider | `openai-codex` |
| Authentication | `chatgpt_oauth` |
| Transport | `codex_responses` |
| Model | `gpt-5.5` |
| Billing mode | `subscription_included` |
| Provider calls per record | `1` maximum |

## Scope

P15.5 implements immutable Pydantic contracts and pure helpers for:

- provider usage normalization from synthetic Codex Responses and synthetic Codex app-server payloads;
- subscription-included cost posture without model-pricing, usage, quota or billing API calls;
- deterministic timeout accounting from injected UTC timestamps and fixed worker/profile budgets;
- validation of `BoundedProviderWorkerResult.usage_record_id` links to accounting records.

P15.5 does not modify runtime dispatch, worker execution, session persistence, credential acquisition, credential delivery, provider runtime profiles or bounded worker profiles.

## Denied Authority

P15.5 denies:

- Docker start, build, pull or push;
- OAuth attempt or credential read;
- credential lease creation, refresh or release against real stores;
- provider dispatch, inference, model-list, usage, quota or billing calls;
- tools, hosted tools, MCP, agents or workers;
- VPS, SSH, remote host, cloud API or file transfer access;
- Graphify execution;
- Git staging, commit, push, merge, rebase, reset, clean, stash, worktree or tag operations.

## No-Execution Counters

| Counter | Value |
| --- | ---: |
| Docker containers started | `0` |
| OAuth attempts | `0` |
| Real credentials read | `0` |
| Credential leases created | `0` |
| Provider dispatches | `0` |
| Inference calls | `0` |
| Model-list calls | `0` |
| Usage API calls | `0` |
| Quota API calls | `0` |
| Billing API calls | `0` |
| Worker starts | `0` |
| Tool calls | `0` |
| MCP calls | `0` |
| Remote hosts contacted | `0` |
| Graphify runs | `0` |
| Git staging operations | `0` |
| Git commits | `0` |
| Git pushes | `0` |

## Validation Evidence

Required P15.5 validation lane:

```text
python -m pytest tests/hermes_cli/test_agent_platform_provider_accounting_contracts.py tests/hermes_cli/test_agent_platform_provider_accounting_normalization.py tests/hermes_cli/test_agent_platform_provider_timeout_accounting.py
```

Observed result: `19 passed, 3 warnings`.

Warning classification:

| Warning counter | Value |
| --- | ---: |
| warnings total | `3` |
| credential or token leak warning | `0` |
| security boundary warning | `0` |
| unhandled resource warning | `0` |
| warning affecting acceptance | `0` |

The three warnings are existing Pydantic protected-namespace warnings emitted by P15.M8 provider runtime and worker contracts for `model_id`, `model_policy` and `model_list_calls_per_request_maximum`. P15.5 provider accounting contracts set `protected_namespaces = ()` and emitted no new protected-namespace warning.

Additional validation:

- `git diff --check`: passed.
- P15.5 row/hash validation: `8` modification-register rows, `8` import-manifest rows, paths match, SHA-256 values match current product files.
- `git status --short --untracked-files=all`: showed exactly two modified product governance tables and the nine created P15.5 files.

## Residual Constraints

P15.5 does not prove provider reachability, live usage availability, account quota visibility, billing-plan state, exact real marginal cost, worker execution, session database integration, dashboard rendering or production readiness.

Human review remains required before Git integration or any runtime expansion.
