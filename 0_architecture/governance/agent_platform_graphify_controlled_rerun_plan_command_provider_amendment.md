# Graphify Controlled Rerun Plan Command / Provider Amendment

## 0. Contexto obligatorio

P10.5 attempted to proceed and stopped correctly before execution because P10.3 recorded `pending_graphify_exact_command_candidate` and `P10.5_blocked_until_exact_command_is_approved`.

GRAPHIFY-HARD-01 confirmed that the exact command could not be derived from P10.0-P10.4 alone.

P9.7 performed authorized local read-only CLI discovery under `4_external/sources/graphify` and discovered the command candidate `graphify . --no-viz`, official executable `graphify`, package name `graphifyy`, entrypoint `graphify.__main__:main`, repository-root working directory candidate, output root candidate `graphify-out/`, and expected generated evidence paths under `graphify-out/**`.

The user explicitly allows OpenAI provider/API/network use for the future controlled Graphify rerun, provided secrets are not inspected, printed, modified, committed, or exposed.

Result marker:

```text
graphify_controlled_rerun_command_provider_amendment_ready
```

P10.3A does not execute Graphify. P10.3A does not call OpenAI. P10.3A does not inspect OpenAI credentials. P10.3A does not modify `.graphifyignore`. P10.3A does not create `graphify-out/`. P10.3A does not import or track generated outputs. P10.3A does not mutate Git.

Graphify remains evidence map only, not authority, not source of truth, not approval engine, not runtime, and not Cognitive Semantic System substrate.

## 1. Tipo

Governance / execution-plan amendment / provider-gate amendment.

## 2. Objetivo

P10.3A amends the P10.3 controlled rerun plan with the exact command candidate, provider/network posture, working directory, input scope, blocked scope, output root, expected output paths, allowed flags, forbidden flags, human approval wording, and P10.5 handoff readiness.

This amendment enables a future P10.5 retry only if P10.1-P10.4 remain accepted, P9.7 command evidence is accepted, `.graphifyignore` remains the approved P10.1 version, provider posture is explicit, OpenAI provider use is limited to the Graphify P10.5 rerun, credentials are not inspected or exposed, output root is exact, and the required human approval statement is present.

## 3. Prerequisite status

| Prerequisite | Path | Status |
| --- | --- | --- |
| P10.0 scope authorization | `0_architecture/governance/agent_platform_graphify_integration_scope_markdown_authorization.md` | present |
| P10.1 ignore policy patch | `0_architecture/implementation/agent_platform_graphify_ignore_policy_patch.md` | present |
| P10.2 markdown scope safety review | `0_architecture/governance/agent_platform_graphify_markdown_scope_safety_review.md` | present |
| P10.3 controlled rerun plan | `0_architecture/governance/agent_platform_graphify_controlled_rerun_plan.md` | present; previous command blocker confirmed |
| P10.4 evidence output classification | `0_architecture/governance/agent_platform_graphify_evidence_output_classification.md` | present |
| P9.7 local CLI discovery | `0_architecture/governance/agent_platform_graphify_local_runtime_cli_discovery_authorization.md` | present; `graphify_cli_command_discovered` and `graphify . --no-viz` confirmed |
| `.graphifyignore` | `.graphifyignore` | present; P10 controlled block and required blockers confirmed |

P10.3 still contains the previous command blocker. P10.3A supersedes that blocker only for the exact future command candidate and provider posture defined here. P10.3A does not modify P10.3.

## 4. P9.7 command evidence status

P9.7 command evidence status:

```text
graphify_cli_command_discovered
```

P9.7 accepted command candidate:

```text
graphify . --no-viz
```

P9.7 did not itself record OpenAI as provider evidence. OpenAI provider allowance in this amendment comes from the user's explicit P10.3A instruction, not from P9.7 discovery.

## 5. P10.3 amendment decision

P10.3A accepts `graphify . --no-viz` as the future P10.5 command candidate.

P10.3A accepts OpenAI provider/API/network use as a future P10.5 gate allowance only for Graphify markdown/docs semantic extraction over the approved P10 input scope.

P10.3A does not authorize immediate execution. P10.5 still requires exact human approval before running.

## 6. GraphifyCommandAmendment

```yaml
GraphifyCommandAmendment:
  ticket: P10.3A
  source: P9.7
  command_candidate: "graphify . --no-viz"
  executable: "graphify"
  package_name: "graphifyy"
  entrypoint: "graphify.__main__:main"
  target: "."
  allowed_flag:
    - "--no-viz"
  working_directory: "repository root"
  execution_authorized_by_P10_3A: false
  execution_candidate_for_P10_5: true
```

P10.3A authorizes the command as a future P10.5 candidate only. P10.3A does not execute the command.

## 7. GraphifyProviderAmendment

```yaml
GraphifyProviderAmendment:
  provider_allowed_for_future_P10_5: true
  provider_name: "OpenAI"
  allowed_purpose:
    - "Graphify markdown/docs semantic extraction for approved P10 input scope"
  blocked_purpose:
    - "general provider activation"
    - "MCP activation"
    - "tool execution outside Graphify"
    - "external source traversal"
    - "product/Siamese traversal"
    - "generated output import"
    - "generated output tracking"
    - "runtime integration"
  credential_inspection_allowed: false
  credential_printing_allowed: false
  credential_modification_allowed: false
  credential_commit_allowed: false
  provider_config_inspection_allowed: false
  environment_listing_allowed: false
  execution_authorized_by_P10_3A: false
  execution_candidate_for_P10_5: true
```

OpenAI provider use is limited to the future P10.5 Graphify run and only for Graphify markdown/docs semantic extraction. This is not general provider/API/MCP activation.

## 8. GraphifyNetworkAmendment

```yaml
GraphifyNetworkAmendment:
  network_allowed_for_future_P10_5: true
  allowed_destination_class:
    - "OpenAI provider/API calls required by Graphify"
  forbidden_destination_class:
    - "MCP servers"
    - "GitHub or external source fetching"
    - "package registries"
    - "dependency installation"
    - "unrelated APIs"
    - "telemetry not required for Graphify execution"
  network_scope: "P10.5 Graphify run only"
  execution_authorized_by_P10_3A: false
```

Network/API access is not generally authorized for AGENT PLATFORM. It is a future P10.5 allowance only if Graphify requires OpenAI-backed markdown/docs semantic extraction.

## 9. GraphifyCredentialBoundary

```yaml
GraphifyCredentialBoundary:
  allowed:
    - "Graphify may use already-configured local OpenAI credentials indirectly at runtime during P10.5"
  forbidden:
    - "reading .env"
    - "printing environment variables"
    - "listing credential stores"
    - "printing OPENAI_API_KEY"
    - "modifying credentials"
    - "writing credentials"
    - "committing credentials"
    - "asking the user to paste secrets into the ticket output"
    - "passing API keys as command-line arguments"
  missing_credentials_behavior: "fail safe; do not install, configure, or request secrets inside the ticket"
```

P10.5 must not expose secrets in logs, reports, output summaries, or commit advice. If Graphify fails because credentials are missing, P10.5 must stop and report safe metadata only.

## 10. GraphifyWorkingDirectory

```yaml
GraphifyWorkingDirectory:
  approved_candidate_for_P10_5: "repository root"
  reason: "command target is '.'"
  forbidden_working_directories:
    - "4_external/sources/**"
    - "external/sources/**"
    - "9_artifacts/**"
    - "graphify-out/**"
    - "2_products/**"
    - "product/**"
    - "products/**"
```

## 11. GraphifyInputScope

```yaml
GraphifyInputScope:
  allowed_paths:
    - "README.md"
  allowed_patterns:
    - "0_architecture/**/*.md"
    - "3_platform/_governed_skeleton/**/*.py"
  reliance:
    - ".graphifyignore"
    - ".gitignore"
  command_target: "."
```

The command is valid only if the accepted P10.1 `.graphifyignore` remains present and effective.

## 12. GraphifyBlockedScope

```yaml
GraphifyBlockedScope:
  blocked_patterns:
    - ".env"
    - ".env.*"
    - "credentials/**"
    - "**/credentials/**"
    - "secrets/**"
    - "**/secrets/**"
    - "**/*secret*"
    - "**/*credential*"
    - "**/*token*"
    - "**/*api_key*"
    - "provider configs"
    - "token stores"
    - "browser auth"
    - "local credential stores"
    - "4_external/sources/**"
    - "external/sources/**"
    - "4_external/sources/gstack-main/**"
    - "9_artifacts/**"
    - "graphify-out/** as input"
    - "2_products/**"
    - "product/**"
    - "products/**"
    - "product/Siamese source"
    - "raw generated outputs"
    - "raw Graphify outputs"
    - "generated outputs no aprobados"
```

Any attempt to read blocked scope must stop P10.5.

## 13. GraphifyIgnorePolicyReliance

```yaml
GraphifyIgnorePolicyReliance:
  required: true
  source: "P10.1"
  must_allow:
    - "README.md"
    - "0_architecture/**/*.md"
    - "3_platform/_governed_skeleton/**/*.py"
  must_block:
    - ".env"
    - ".env.*"
    - "credentials/**"
    - "secrets/**"
    - "provider/auth/token material"
    - "4_external/sources/**"
    - "external/sources/**"
    - "4_external/sources/gstack-main/**"
    - "9_artifacts/**"
    - "graphify-out/** as input"
    - "2_products/**"
    - "product/**"
    - "products/**"
  stop_if_changed_from_approved_P10_1: true
```

P10.3A does not modify `.graphifyignore`.

## 14. GraphifyOutputRoot

```yaml
GraphifyOutputRoot:
  approved_candidate_for_P10_5: "graphify-out/"
  generated_output: true
  trackable_by_default: false
  import_by_default: false
  authority: false
```

P10.3A does not create the output root. P10.5 may create it only during the approved controlled rerun.

## 15. GraphifyExpectedOutputPaths

```yaml
GraphifyExpectedOutputPaths:
  expected_primary_outputs:
    - "graphify-out/GRAPH_REPORT.md"
    - "graphify-out/graph.json"
  expected_generated_metadata_or_cache:
    - "graphify-out/cache/**"
    - "graphify-out/cost.json"
  visualization_outputs:
    - "skipped by --no-viz if Graphify behavior matches P9.7 evidence"
  classification:
    - "raw_generated_evidence"
    - "local-only generated evidence"
    - "review_required"
    - "not_trackable_by_default"
```

If Graphify creates additional outputs under `graphify-out/`, P10.5 must report them as generated local-only evidence and classify them under P10.4. If Graphify writes outside `graphify-out/`, P10.5 must stop and report incident metadata.

## 16. AllowedFlags

```yaml
AllowedFlags:
  command: "graphify . --no-viz"
  flags:
    - "--no-viz"
```

No other flags are accepted by P10.3A.

## 17. Forbidden flags and behaviors

Forbidden flags and behaviors:

- `--watch`
- `--mcp`
- `--neo4j`
- `--neo4j-push`
- `--falkordb`
- `--falkordb-push`
- `--google-workspace`
- `--dedup-llm`
- `--global`
- `--force`
- install commands
- uninstall commands
- hook commands
- platform commands
- dependency installation
- package manager execution
- external source fetching
- product/Siamese traversal
- secrets traversal
- credential printing
- provider config inspection
- MCP activation
- Graph DB push
- Vector DB creation
- embedding generation outside Graphify's necessary internal processing
- runtime activation beyond the one Graphify process
- Git mutation
- output import
- generated output tracking
- source tracking expansion

`--backend` or equivalent provider-selection flags are not approved because the allowed documents did not provide exact syntax selected for this run and P10.3A does not approve additional flags. P10.5 may only rely on already-configured local Graphify/OpenAI provider posture.

## 18. P10.5 preflight checklist

P10.5 may execute only if all are true:

- P10.1 accepted.
- P10.2 accepted.
- P10.3 accepted.
- P10.4 accepted.
- P9.7 accepted.
- P10.3A accepted.
- `.graphifyignore` present.
- `.graphifyignore` still matches approved P10.1 posture.
- exact command is `graphify . --no-viz`.
- working directory is repository root.
- output root is `graphify-out/`.
- OpenAI provider use is explicitly approved for this run.
- credentials are already configured locally if required.
- credentials are not inspected, printed, modified, or committed.
- network/API use is limited to OpenAI provider calls required by Graphify.
- no MCP activation.
- no package installation.
- no external source traversal.
- no product/Siamese traversal.
- no generated output input traversal.
- no output import.
- no generated output tracking.
- no Git mutation.
- human approval statement is present.

## 19. P10.5HumanApprovalStatement

P10.5 must require this exact approval statement, or a stricter equivalent, before execution:

```text
Human approval present for one controlled Graphify rerun using command `graphify . --no-viz` from the repository root, relying on the accepted P10.1 `.graphifyignore` scope, with input limited to README.md, 0_architecture/**/*.md, and 3_platform/_governed_skeleton/**/*.py; blocked scopes preserved; output root limited to graphify-out/; OpenAI provider/API/network use allowed only for Graphify markdown/docs semantic extraction during this run; credentials must already be configured locally and must not be inspected, printed, modified, or committed; no MCP, no package installation, no external source traversal, no product/Siamese traversal, no output import, no generated output tracking, no authority promotion, and no Git mutation.
```

P10.3A records the required approval wording. P10.3A does not itself execute P10.5.

## 20. P10.5HandoffDecision

```yaml
P10.5HandoffDecision:
  status: ready_after_human_approval
  command: "graphify . --no-viz"
  working_directory: "repository root"
  output_root: "graphify-out/"
  provider: "OpenAI allowed for this run only"
  credentials: "existing local config only; not inspected"
  p10_5_may_execute_after_exact_approval: true
```

P10.5 remains blocked until the exact human approval statement is present and preflight passes.

## 21. Acceptance criteria

| Criterion | Status |
| --- | --- |
| Creates exactly the P10.3A amendment file. | satisfied |
| Records P9.7 as command source. | satisfied |
| Accepts or rejects `graphify . --no-viz`. | accepted as future P10.5 command candidate |
| Defines OpenAI provider posture. | satisfied |
| Defines network/API posture. | satisfied |
| Defines credential boundary. | satisfied |
| Defines working directory. | satisfied |
| Defines input scope. | satisfied |
| Defines blocked scope. | satisfied |
| Defines `.graphifyignore` reliance. | satisfied |
| Defines output root. | satisfied |
| Defines expected output paths. | satisfied |
| Defines allowed flags. | satisfied |
| Defines forbidden flags. | satisfied |
| Defines P10.5 preflight checklist. | satisfied |
| Defines exact human approval statement. | satisfied |
| Defines P10.5 handoff decision. | satisfied |
| Does not execute Graphify. | satisfied |
| Does not call OpenAI. | satisfied |
| Does not inspect credentials. | satisfied |
| Does not modify `.graphifyignore`. | satisfied |
| Does not create `graphify-out/`. | satisfied |
| Does not mutate Git. | satisfied |

## 22. Stop rules

Stop if P10.1 is missing, P10.2 is missing, P10.3 is missing, P10.4 is missing, P9.7 is missing, `.graphifyignore` is missing, P9.7 does not contain `graphify . --no-viz`, P9.7 does not contain `graphify_cli_command_discovered`, command amendment requires executing Graphify, provider amendment requires calling OpenAI, provider amendment requires inspecting credentials, provider amendment requires printing environment variables, provider amendment requires reading `.env`, provider amendment requires package installation, provider amendment requires MCP activation, provider amendment requires external source traversal, provider amendment requires product/Siamese traversal, provider amendment requires generated output inspection, provider amendment requires modifying `.graphifyignore`, provider amendment requires creating `graphify-out/`, provider amendment requires Git mutation, or provider amendment requires recommending `git add .`.

## 23. Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_command_provider_amendment.md`

Not created / not approved:

- No Graphify execution
- No `/graphify` execution
- No Codegraph execution
- No OpenAI call
- No API call
- No MCP activation
- No credential inspection
- No credential printing
- No `.env` inspection
- No provider config inspection
- No package installation
- No package manager execution
- No build
- No tests
- No `graphify-out/`
- No generated outputs
- No Graphify output import
- No generated output tracking
- No source tracking expansion
- No runtime integration
- No adapter creation
- No external source inspection
- No product/Siamese inspection
- No Git mutation
- No git add .

## 24. Recommended next ticket

If this P10.3A amendment is accepted, the next ticket is:

```text
P10.5 - Graphify Controlled Rerun Execution
```

P10.5 must still require exact human approval and must stop if any preflight condition fails.

## 25. Final verdict

| Question | Answer |
| --- | --- |
| What did P10.3A create? | `0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_command_provider_amendment.md`. |
| Was P9.7 present? | Yes. |
| Did P9.7 contain `graphify . --no-viz`? | Yes. |
| Did P9.7 contain `graphify_cli_command_discovered`? | Yes. |
| Did P10.3A accept the command candidate? | Yes, as a future P10.5 candidate only. |
| Exact command candidate? | `graphify . --no-viz`. |
| Provider amendment? | OpenAI allowed for future P10.5 Graphify markdown/docs semantic extraction only. |
| Network/API amendment? | OpenAI provider/API calls allowed only during the future controlled P10.5 Graphify run. |
| Credential boundary? | Existing local credentials may be used indirectly; no inspection, printing, modification, or committing. |
| Working directory? | Repository root. |
| Input scope? | `README.md`, `0_architecture/**/*.md`, and `3_platform/_governed_skeleton/**/*.py`, relying on `.graphifyignore` and `.gitignore`. |
| Blocked scope? | Secrets, credentials, provider/auth/token material, external sources, generated output inputs, product/Siamese source, runtime surfaces, and Git mutation. |
| Output root? | `graphify-out/`. |
| Expected output paths? | `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`, cache/metadata under `graphify-out/**`. |
| Allowed flags? | `--no-viz` only. |
| Did P10.3A execute Graphify? | No. |
| Did P10.3A call OpenAI? | No. |
| Did P10.3A inspect credentials or `.env`? | No. |
| Did P10.3A modify `.graphifyignore`? | No. |
| Did P10.3A create `graphify-out/`? | No. |
| Did P10.3A mutate Git? | No. |
| P10.5 handoff status? | `ready_after_human_approval`. |
| Recommended next ticket? | P10.5 - Graphify Controlled Rerun Execution. |
