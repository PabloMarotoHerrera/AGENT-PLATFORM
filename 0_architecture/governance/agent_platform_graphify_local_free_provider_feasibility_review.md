# Graphify Local Free Provider Feasibility Review

## Document Header

| Field | Value |
| --- | --- |
| Title | Graphify Local Free Provider Feasibility Review |
| Ticket | P10.5A-ALT |
| Status | Claude Code provider feasible at documentation level; P10.3B required before retry |
| Date | 2026-07-09 |
| Scope | Documentation-only feasibility review for Graphify local, free-tier, or subscription-backed provider paths that avoid paid OpenAI API usage. |
| Authority | Feasibility review only; not Graphify execution, Claude Code execution, provider login, provider installation, credential inspection, credential configuration, API validation, output import, generated output tracking, runtime integration, source tracking expansion, Git mutation, or Cognitive Semantic System substrate selection. |
| Target file | `0_architecture/governance/agent_platform_graphify_local_free_provider_feasibility_review.md` |

Final declaration: `graphify_claude_code_provider_feasible`.

Supporting provider markers:

```text
graphify_ollama_provider_feasible
graphify_gemini_free_tier_provider_candidate
```

## Summary

P10.5A-ALT reviewed only allowed governance records and Graphify local documentation/manifests.

Graphify documentation supports a Claude Code CLI backend:

```text
graphify extract ./docs --backend claude-cli
```

The documented Claude Code CLI path is distinct from the Anthropic API-key backend:

```text
--backend claude      -> Anthropic Claude API, uses ANTHROPIC_API_KEY
--backend claude-cli  -> Claude Code CLI, no API key, uses Claude subscription
```

Graphify documentation also supports Ollama local inference:

```text
graphify extract ./docs --backend ollama
```

Graphify documentation supports Gemini as an API-key backend:

```text
graphify extract ./docs --backend gemini
```

P10.3A currently authorizes OpenAI only and does not approve `--backend` or equivalent provider-selection flags. Therefore P10.5B should not be generated directly from this review. The next governance step should be P10.3B to amend the controlled rerun plan with a Claude Code provider posture and exact command syntax.

## Files Inspected

Governance files checked:

- `0_architecture/governance/agent_platform_graphify_controlled_rerun_execution_record.md`
- `0_architecture/governance/agent_platform_graphify_openai_provider_availability_credential_boundary_resolution.md`
- `0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_command_provider_amendment.md`
- `0_architecture/governance/agent_platform_graphify_local_runtime_cli_discovery_authorization.md`
- `.graphifyignore`

Graphify docs/manifests inspected for provider/backend discovery only:

- `4_external/sources/graphify/README.md`
- `4_external/sources/graphify/ARCHITECTURE.md`
- `4_external/sources/graphify/docs/how-it-works.md`
- `4_external/sources/graphify/pyproject.toml`

No Graphify source code, generated output, credentials, provider config, product source, or external source outside `4_external/sources/graphify/**` was inspected.

## Files Created

- `0_architecture/governance/agent_platform_graphify_local_free_provider_feasibility_review.md`

## Files Modified

- None beyond creating this P10.5A-ALT feasibility review document.

## Commands Run

Allowed shell commands run:

```text
git status --short
powershell -NoProfile -Command "Test-Path '0_architecture/governance/agent_platform_graphify_controlled_rerun_execution_record.md'"
powershell -NoProfile -Command "Test-Path '0_architecture/governance/agent_platform_graphify_openai_provider_availability_credential_boundary_resolution.md'"
powershell -NoProfile -Command "Test-Path '0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_command_provider_amendment.md'"
powershell -NoProfile -Command "Test-Path '4_external/sources/graphify'"
powershell -NoProfile -Command "Select-String -Path '0_architecture/governance/agent_platform_graphify_controlled_rerun_execution_record.md' -Pattern 'safe_failure_missing_llm_api_key','graphify . --no-viz'"
powershell -NoProfile -Command "Select-String -Path '0_architecture/governance/agent_platform_graphify_openai_provider_availability_credential_boundary_resolution.md' -Pattern 'OPENAI_API_KEY_PRESENT=false','graphify_openai_provider_missing_safe_stop'"
powershell -NoProfile -Command "Select-String -Path '0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_command_provider_amendment.md' -Pattern 'OpenAI','provider_name: \"OpenAI\"','provider: \"OpenAI allowed for this run only\"','Anthropic','Claude','Ollama','Gemini'"
```

Allowed documentation searches were also performed over Graphify docs/manifests using provider/backend terms for Claude, Anthropic, Ollama, Gemini, Google, OpenAI, backend, provider, model, LLM, and API key.

No forbidden command was run.

## P10.5 Safe Failure Status

P10.5 execution record present: true.

P10.5 approved command marker present: `graphify . --no-viz`.

P10.5 safe failure reason present: `safe_failure_missing_llm_api_key`.

P10.5 executed Graphify exactly once and stopped before semantic extraction because no LLM API key/backend was available.

## P10.5A OpenAI Provider Status

P10.5A OpenAI boundary record present: true.

P10.5A marker present: `graphify_openai_provider_missing_safe_stop`.

P10.5A recorded:

```text
OPENAI_API_KEY_PRESENT=false
```

P10.5A did not inspect or print the credential value.

## Graphify Provider Discovery Scope

Documentation/manifests showed:

- `pyproject.toml` declares package `graphifyy` and console script `graphify = "graphify.__main__:main"`.
- `pyproject.toml` optional dependencies include `ollama`, `anthropic`, `gemini`, `openai`, and `bedrock` extras.
- `README.md` documents `--backend` values including `gemini`, `kimi`, `claude`, `openai`, `deepseek`, `ollama`, `bedrock`, and `claude-cli`.
- `README.md` distinguishes IDE/skill operation from headless extraction.
- `README.md` says docs, PDFs, and images require semantic extraction through an assistant/model/backend path.
- `ARCHITECTURE.md` states Graphify is a Claude Code skill backed by a Python library.
- `docs/how-it-works.md` describes docs/papers/images extraction as Claude subagent semantic extraction.

## Claude Code Feasibility

Claude Code provider feasibility: feasible at documentation level.

Graphify docs support Claude Code in two relevant ways:

- As a Claude Code skill/platform install target.
- As a headless backend named `claude-cli`.

Key documented backend path:

```text
graphify extract ./docs --backend claude-cli
```

Graphify docs state that the Claude Code CLI path uses the `claude` CLI binary, requires no API key, and uses the user's Claude subscription.

This is not the same as the Anthropic API-key backend.

P10.5A-ALT did not execute Claude Code, did not run `claude --version`, did not log in, did not inspect provider config, and did not validate subscription status.

Claude Code future boundary requirements:

- Claude Code must already be installed outside the ticket workflow.
- Claude Code must already be authenticated outside the ticket workflow.
- No `claude login` may be run by the agent.
- No credential or session token may be inspected or printed.
- No provider config may be printed.
- No general MCP/tool activation is authorized.

Claude Code subdecision:

```text
graphify_claude_code_provider_feasible
```

## Anthropic API-Key Feasibility

Anthropic API-key backend feasibility: documented, but not accepted for the user's no-new-paid-API preference.

Documented backend path:

```text
graphify extract ./docs --backend claude
```

Documented credential variable:

```text
ANTHROPIC_API_KEY
```

This path is API-key-backed and may involve Anthropic API billing. It should not be used for P10.5 retry unless the user explicitly accepts paid Anthropic API usage in a future gate.

## Ollama Local Feasibility

Ollama/local provider feasibility: feasible at documentation level.

Documented backend path:

```text
graphify extract ./docs --backend ollama
```

Documented posture:

- Local Ollama inference.
- No API key needed for loopback.
- Default local URL is `http://localhost:11434` through `OLLAMA_BASE_URL`.
- `OLLAMA_MODEL` is optional and can select the model.
- `GRAPHIFY_OLLAMA_NUM_CTX`, `GRAPHIFY_OLLAMA_KEEP_ALIVE`, `--token-budget`, and `--max-concurrency` are documented tuning knobs.

P10.5A-ALT did not run `ollama`, did not check whether Ollama is installed, did not start a server, did not pull a model, and did not validate model quality.

Ollama is a viable no-paid-API path if a future gate authorizes local Ollama availability checks or the user confirms Ollama is already installed, running, and has a suitable model.

Ollama subdecision:

```text
graphify_ollama_provider_feasible
```

## Gemini Free-Tier Feasibility

Gemini provider feasibility: documented as an API-key backend and CLI platform, but free-tier/billing status is outside Graphify documentation.

Documented backend path:

```text
graphify extract ./docs --backend gemini
```

Documented credential variables:

```text
GEMINI_API_KEY
GOOGLE_API_KEY
```

Graphify also documents Gemini CLI as a platform install target. P10.5A-ALT did not inspect Gemini credentials, execute Gemini CLI, call Gemini, or validate free-tier status.

Gemini may be a future candidate only if the user separately confirms acceptable free-tier limits, privacy posture, and billing controls outside Graphify execution.

Gemini subdecision:

```text
graphify_gemini_free_tier_provider_candidate
```

## OpenAI-Compatible Local Feasibility

Graphify docs also document an OpenAI-compatible local endpoint path:

```text
OPENAI_BASE_URL=http://localhost:8080/v1 OPENAI_MODEL=my-model graphify extract ./docs --backend openai
```

Docs state local servers accept any non-empty `OPENAI_API_KEY` for the OpenAI-compatible path.

This can avoid paid OpenAI API billing when the endpoint is truly local, but it is less clean for this governance path because it still uses OpenAI-shaped environment variables and endpoint configuration. It should remain secondary behind `claude-cli` and `ollama` unless a future gate specifically approves local OpenAI-compatible configuration without exposing values.

## Provider Comparison

| Provider path | Documented by Graphify | Requires API key | Paid API billing risk | Local/subscription posture | Feasibility decision |
| --- | --- | --- | --- | --- | --- |
| Claude Code CLI, `--backend claude-cli` | yes | no | no Anthropic API key path; uses Claude subscription | subscription-backed | preferred feasible path |
| Anthropic Claude API, `--backend claude` | yes | `ANTHROPIC_API_KEY` | yes or unknown paid API billing | API-key-backed | documented but not preferred |
| Ollama, `--backend ollama` | yes | no for loopback | no paid API billing if local | local | feasible secondary path |
| Gemini, `--backend gemini` | yes | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | free-tier/billing outside Graphify | API-key-backed/free-tier candidate | candidate only |
| OpenAI-compatible local, `--backend openai` with local `OPENAI_BASE_URL` | yes | non-empty OpenAI-shaped key | no paid OpenAI billing if local endpoint | local endpoint | secondary candidate requiring tighter gate |
| Bedrock, `--backend bedrock` | yes | no direct API key, uses AWS IAM | AWS billing likely | cloud IAM | not aligned with no-new-billing preference |

## Credential Subscription Boundary

```yaml
CredentialSubscriptionBoundary:
  allowed:
    - "documentation-only provider feasibility review"
    - "recording whether provider path appears subscription-backed, API-key-backed, local, or unknown"
    - "boolean/policy-level availability statements"
  forbidden:
    - "reading .env"
    - "printing environment variables"
    - "printing API keys"
    - "validating API keys by network request"
    - "logging into Claude Code"
    - "logging into any provider"
    - "installing provider tools"
    - "modifying provider config"
    - "committing provider config"
```

Claude Code future execution must still require:

- Claude Code already installed and authenticated outside the ticket workflow.
- No credential inspection.
- No login command inside the ticket.
- No API key exposure.
- No provider config printing.
- No general MCP/tool activation.

## Provider Decision

```yaml
GraphifyProviderFeasibility:
  ticket: P10.5A-ALT
  preferred_provider_candidate: "Claude Code"
  preferred_backend_name: "claude-cli"
  preferred_provider_feasible: true
  preferred_provider_feasibility_marker: "graphify_claude_code_provider_feasible"
  secondary_provider_candidates:
    - provider: "Ollama"
      backend_name: "ollama"
      feasibility_marker: "graphify_ollama_provider_feasible"
      posture: "local no-paid-API path if Ollama is already installed, running, and has a suitable model"
    - provider: "Gemini"
      backend_name: "gemini"
      feasibility_marker: "graphify_gemini_free_tier_provider_candidate"
      posture: "API-key-backed candidate; free-tier/billing limits must be resolved outside Graphify"
    - provider: "OpenAI-compatible local endpoint"
      backend_name: "openai"
      feasibility_marker: "graphify_openai_compatible_local_candidate"
      posture: "local endpoint candidate requiring explicit local endpoint and non-secret config boundary"
  paid_openai_api_allowed: false
  paid_anthropic_api_allowed: false
  credential_value_inspection_allowed: false
  provider_execution_allowed: false
  graphify_execution_allowed: false
  install_allowed: false
```

## P10.3 Follow-Up Recommendation

P10.3A needs amendment or replacement before any retry because:

- P10.3A authorizes OpenAI provider/API/network use only.
- P10.3A does not approve `--backend` or equivalent provider-selection flags.
- P10.3A's human approval wording is OpenAI-specific.
- P9.7 previously treated `--backend` as forbidden unless a future exact gate approves provider/local backend posture.

Recommended next ticket:

```text
P10.3B - Graphify Controlled Rerun Plan Claude Code Provider Amendment
```

P10.3B should define:

- Exact backend/provider posture for `claude-cli`.
- Exact command form for the controlled rerun.
- Whether the top-level command may be amended with `--backend claude-cli` or whether a documented `graphify extract . --backend claude-cli --no-viz` command form must replace it.
- Whether `--no-viz` remains valid with the selected command form.
- Working directory and output root.
- Input scope reliance on `.graphifyignore`.
- Stop rules for missing Claude Code installation or missing authentication.
- No login, no credential inspection, no provider config printing, no MCP, no package installation, no external source traversal, no product/Siamese traversal, no output import, no generated output tracking, no authority promotion, and no Git mutation.

## P10.5 Retry Recommendation

P10.5B should not be generated directly from P10.5A-ALT.

P10.5B may be prepared only after a P10.3B amendment resolves the Claude Code provider boundary and exact command syntax.

Recommended sequence:

```text
P10.3B - Graphify Controlled Rerun Plan Claude Code Provider Amendment
P10.5B - Graphify Controlled Rerun Retry With Claude Code Provider Available
```

If Claude Code is unavailable, the next best no-paid-API path is an Ollama-specific P10.3B local provider amendment.

## Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_graphify_local_free_provider_feasibility_review.md`

Not created / not approved:

- No Graphify execution.
- No `/graphify` execution.
- No Claude Code execution.
- No Claude login.
- No Ollama execution.
- No OpenAI API call.
- No Anthropic API call.
- No Gemini API call.
- No API key validation request.
- No credential value inspection.
- No credential value printing.
- No `.env` inspection.
- No credential store inspection.
- No provider config inspection.
- No credential modification.
- No package installation.
- No package manager execution.
- No `graphify-out/` creation by P10.5A-ALT.
- No generated outputs.
- No Graphify output import.
- No generated output tracking.
- No source tracking expansion.
- No runtime integration.
- No adapter creation.
- No external source inspection outside Graphify docs/manifests.
- No product/Siamese inspection.
- No Git mutation.
- No `git add .`.

## Limitations

P10.5A-ALT is documentation-only.

P10.5A-ALT did not confirm that Claude Code is installed.

P10.5A-ALT did not confirm that Claude Code is authenticated.

P10.5A-ALT did not confirm that Ollama is installed, running, or has a suitable model.

P10.5A-ALT did not confirm Gemini free-tier limits, billing status, privacy posture, or credential availability.

P10.5A-ALT did not validate any provider by network request.

P10.5A-ALT did not determine whether `graphify . --no-viz --backend claude-cli` is accepted by the installed CLI. The docs clearly document `graphify extract ./docs --backend claude-cli`, while P9.7/P10.3A approved `graphify . --no-viz`. P10.3B must resolve the exact command syntax before execution.

## Recommended Next Ticket

```text
P10.3B - Graphify Controlled Rerun Plan Claude Code Provider Amendment
```

If P10.3B cannot confirm a safe Claude Code command form, use:

```text
P10.3B - Graphify Controlled Rerun Plan Local Provider Amendment
```

for Ollama.

## Commit Commands

Not run by P10.5A-ALT because Git mutation is prohibited in this ticket.

If a future human-approved commit gate authorizes tracking this file, use scoped commands only:

```bash
git status --short
git add 0_architecture/governance/agent_platform_graphify_local_free_provider_feasibility_review.md
git commit -m "Review Graphify local free provider feasibility"
git push
```
