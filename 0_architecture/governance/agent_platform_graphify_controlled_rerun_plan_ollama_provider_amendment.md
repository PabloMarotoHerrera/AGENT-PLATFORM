# Graphify Controlled Rerun Plan Ollama Provider Amendment

## Summary

P10.3B amends the existing Graphify controlled rerun plan for a possible future local Ollama-backed visualization/evidence-map attempt.

P10.3B is governance-only and plan-only. It does not execute Graphify, run Ollama, pull models, inspect credentials, inspect generated outputs, modify ignore files, create outputs, or mutate Git.

Result marker:

```text
graphify_controlled_rerun_plan_ollama_provider_amendment_ready
```

Decision markers:

```text
graphify_ollama_provider_amendment_defined
graphify_ollama_command_resolution_required
graphify_ollama_execution_not_authorized_by_p10_3b
graphify_visualization_only_scope_preserved
graphify_semantic_authority_still_rejected
graphify_input_scope_reconfirmed
graphify_output_classification_reconfirmed
graphify_ollama_model_pull_blocked
p10_5b_graphify_ollama_controlled_execution_ready_after_amendment
graphify_ollama_command_candidate_resolved
graphify_ollama_provider_boundary_defined
```

```yaml
P10_3B_Graphify_Ollama_Provider_Amendment:
  ticket: "P10.3B"
  date: "2026-07-10"
  status: "governance_plan_only"
  output_file: "0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_ollama_provider_amendment.md"
  graphify_execution_authorized: false
  ollama_execution_authorized: false
  ollama_model_pull_authorized: false
  provider_api_call_authorized: false
  credential_inspection_authorized: false
  git_mutation_authorized: false
  command_resolution_outcome: "Outcome A - exact Ollama command candidate resolved from accepted P10.5A-ALT Graphify documentation evidence"
  command_candidate_for_p10_5b: "graphify extract . --backend ollama"
  include_no_viz_flag: false
  no_viz_reason: "not confirmed for the documented extract command form"
  custom_output_root_flag_confirmed: false
  output_root_policy: "prefer graphify-out/p10_5b_ollama_01 if future syntax discovery confirms output flag; otherwise default graphify-out with collision preflight"
  final_marker: "graphify_controlled_rerun_plan_ollama_provider_amendment_ready"
```

## Files Inspected

Governance files inspected read-only:

```text
0_architecture/governance/agent_platform_graphify_integration_scope_markdown_authorization.md
0_architecture/governance/agent_platform_graphify_markdown_scope_safety_review.md
0_architecture/governance/agent_platform_graphify_controlled_rerun_plan.md
0_architecture/governance/agent_platform_graphify_evidence_output_classification.md
0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_command_provider_amendment.md
0_architecture/governance/agent_platform_graphify_controlled_rerun_execution_record.md
0_architecture/governance/agent_platform_graphify_openai_provider_availability_credential_boundary_resolution.md
0_architecture/governance/agent_platform_graphify_local_free_provider_feasibility_review.md
0_architecture/governance/agent_platform_gbrain_adoption_graphify_semantic_replacement_decision.md
0_architecture/governance/agent_platform_gbrain_gstack_integration_closure.md
.graphifyignore
.gitignore
```

Graphify local source/docs path check:

```text
4_external/sources/graphify
```

Status: absent at P10.3B inspection time.

Because the allowed local Graphify source/docs path was absent, P10.3B did not inspect fresh Graphify source bodies. P10.3B uses accepted P10.5A-ALT evidence that previously inspected Graphify docs/manifests and recorded Ollama syntax.

Not inspected:

```text
.env
.env.*
credentials/**
secrets/**
provider configs
token stores
browser auth
local credential stores
API keys
Claude credentials
Claude session files
Anthropic credentials
OpenAI credentials
Gemini credentials
Ollama config files
normal user .gbrain
normal user .gstack
normal user .ollama configs
browser cookie stores
graphify-out/**
9_artifacts/** contents
2_products/**
product/**
products/**
raw Graphify outputs
4_external/sources/gbrain-master/node_modules/**
4_external/sources/gstack-main/node_modules/**
4_external/sources/graphify/node_modules/**
global package caches
Bun cache contents
DB internals under 9_artifacts/**
generated home internals under 9_artifacts/**
```

## Files Created

Created exactly one governance amendment file:

```text
0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_ollama_provider_amendment.md
```

## Files Modified

No existing file was modified.

## Commands Run

Allowed command run:

```text
git status --short
```

Read-only file/path inspections and marker searches were performed using repository read/search tooling. No Graphify, Ollama, GBrain, GStack, provider, MCP, browser, package manager, test, build, script, output cleanup, or Git mutation command was run.

Explicitly not run:

```text
graphify
graphify --help
graphify extract
/graphify
ollama
ollama list
ollama run
ollama pull
ollama serve
curl http://127.0.0.1:11434
gbrain
gstack
bun
npm
node
python
pip
docker
builds
scripts
CI
provider commands
MCP servers
browser daemons
ngrok
git add
git commit
git push
```

## Prior P10 Scope Status

P10.0 scope authorization is present and records:

```text
graphify_markdown_scope_authorization_ready
```

Allowed P10 Graphify input remains:

```text
README.md
0_architecture/**/*.md
3_platform/_governed_skeleton/**/*.py
```

P10.2 scope safety review is present and records the same allowed scope with blocked secret, external source, generated output, and product/source boundaries.

`.graphifyignore` currently records the P10 controlled scope and includes the allowed patterns plus explicit blockers for:

```text
.env
.env.*
credentials/**
secrets/**
4_external/sources/**
external/sources/**
4_external/sources/gstack-main/**
9_artifacts/**
graphify-out/**
2_products/**
product/**
products/**
```

`.gitignore` keeps external sources, artifacts, products, generated/cache directories, and credential patterns ignored or local-only.

Decision marker:

```text
graphify_input_scope_reconfirmed
```

## Graphify Evidence Role Confirmation

Graphify remains an evidence-map / visualization / report candidate only.

Graphify is not:

```text
authority
source of truth
approval engine
runtime authority
memory authority
Cognitive Semantic System substrate
semantic retrieval authority
```

P10.4 confirms Graphify outputs default to `raw_generated_evidence`, are not trackable by default, are not authority by classification alone, and cannot become imported, approved, or substrate by classification alone.

Decision markers:

```text
graphify_visualization_only_scope_preserved
graphify_semantic_authority_still_rejected
graphify_output_classification_reconfirmed
```

## P12 / GBrain Relationship Confirmation

P12 adopted GBrain as the preferred local semantic/retrieval and memory-indexing candidate.

P12 records:

```text
graphify_semantic_replacement_confirmed
graphify_visualization_reporting_role_deferred
graphify_not_memory_authority
graphify_semantic_replacement_closed
graphify_visualization_reporting_deferred
```

Therefore P10.3B is not a semantic authority recovery path. It only prepares a possible local Ollama-backed Graphify visualization/evidence-map attempt if future P10.5B approval is granted.

## Graphify Ollama Command Syntax Evidence

The allowed local Graphify source/docs path was absent during P10.3B:

```text
4_external/sources/graphify: absent
```

Accepted P10.5A-ALT evidence states that Graphify documentation supports Ollama local inference and records this documented backend path:

```text
graphify extract ./docs --backend ollama
```

Accepted P10.5A-ALT also records:

```text
graphify_ollama_provider_feasible
```

and states that Ollama is local, requires no API key for loopback, defaults to `http://localhost:11434` through `OLLAMA_BASE_URL`, and can use `OLLAMA_MODEL` optionally.

P10.3B uses that accepted governance evidence to resolve the command form:

```text
graphify extract <input> --backend ollama
```

P10.3B does not confirm fresh local source syntax because the allowed source/docs path is absent. P10.5B must preserve a preflight command-syntax stop rule before runtime.

## Command Resolution Outcome

Outcome A applies at governance-evidence level:

```text
graphify_ollama_command_candidate_resolved
```

The exact P10.5B command candidate is:

```text
graphify extract . --backend ollama
```

Rationale:

| Evidence | Decision |
| --- | --- |
| P10.5A-ALT documents `graphify extract ./docs --backend ollama`. | Supports `graphify extract <input> --backend ollama`. |
| P10.3/P10.3A use repository root with `.graphifyignore` to constrain scope. | Candidate input is `.` from repository root. |
| `--no-viz` is not confirmed for `graphify extract`. | Do not include `--no-viz`. |
| No output directory flag is confirmed in accepted evidence. | Do not include an output flag. |

P10.5B must still perform preflight checks before execution. If the Graphify executable does not accept this syntax, P10.5B must safe-block and stop without trying alternatives.

Decision marker:

```text
graphify_ollama_command_resolution_required
```

## P10.5B Command Candidate

```yaml
P10_5B_Graphify_Ollama_Command_Candidate:
  command_text: "graphify extract . --backend ollama"
  working_directory: "repository root"
  input_target: "."
  provider_backend: "ollama"
  allowed_flags:
    - "--backend ollama"
  omitted_flags:
    - flag: "--no-viz"
      reason: "not confirmed for the documented extract command form"
  output_flag: "none confirmed"
  custom_output_root_supported: false
  execution_authorized_by_p10_3b: false
  requires_p10_5b_human_approval: true
```

P10.5B must not invent additional flags. P10.5B must not try alternate Graphify commands if this command fails syntax validation or runtime startup.

## P10.5B Preflight Model

P10.5B must perform preflight checks before any Graphify runtime attempt. P10.3B defines these checks but does not execute them.

Required P10.5B preflight checks:

```text
git status --short
Graphify executable availability
Graphify command syntax availability for: graphify extract . --backend ollama
Ollama executable availability
Ollama server availability
Ollama local model inventory
.graphifyignore exists
allowed input root exists
blocked input roots are not included
output root collision status
```

P10.5B safe-block conditions:

| Condition | Required behavior |
| --- | --- |
| Graphify executable missing. | Stop before runtime. |
| Exact command syntax cannot be resolved safely. | Stop; do not try alternatives; route to `P10.3C - Graphify CLI Command Syntax Discovery Gate`. |
| Ollama executable or server unavailable. | Stop before Graphify runtime. |
| No suitable local Ollama model is present. | Stop; do not pull a model. |
| `.graphifyignore` missing or missing P10 markers. | Stop. |
| Output root collision exists and overwrite/mixing behavior is unclear. | Stop; do not delete or clean outputs. |
| Any blocked input scope would be included. | Stop. |
| Any credential/provider config inspection is needed. | Stop. |

Recommended safe-block marker for P10.5B:

```text
graphify_ollama_rerun_blocked_before_execution
graphify_ollama_missing_model_or_command_or_preflight
```

## Ollama Model Availability Rule

P10.5B may use only a locally available Ollama model.

P10.5B must not:

```text
pull models
select a remote model
call hosted providers
inspect Ollama config files
inspect normal user .ollama configs
inspect credentials
modify Ollama settings
start long-running unmanaged daemons without explicit approval
```

If no suitable local model is present:

```text
safe block
recommend separate explicit model-pull gate if desired
```

Possible future model-pull gate:

```text
P10.OLLAMA-MODEL - Ollama Local Model Pull Authorization
```

Decision marker:

```text
graphify_ollama_model_pull_blocked
```

## Output Directory / Collision Policy

Preferred output root if a future exact command-syntax discovery confirms a Graphify custom output directory flag:

```text
graphify-out/p10_5b_ollama_01/
```

Current P10.3B command candidate does not include a custom output directory flag because accepted evidence did not confirm one.

Fallback output root:

```text
graphify-out/
```

P10.5B must stop before runtime if:

```text
output root already exists and overwrite behavior is unclear
output root would mix with previous run outputs
output root would require deletion or cleanup not explicitly approved
output root would require inspecting generated output contents
```

Generated outputs classification:

```text
raw generated evidence
local/untracked by default
not source of truth
not approval
not memory authority
not production memory
not imported into GBrain
not imported into operational memory
not tracked unless future exact gate approves
```

## Input Scope Confirmation

P10.5B must use only the approved repository input scope through repository-root execution and `.graphifyignore`:

```text
README.md
0_architecture/**/*.md
3_platform/_governed_skeleton/**/*.py
```

Blocked from input:

```text
4_external/sources/**
9_artifacts/**
graphify-out/**
2_products/**
product/**
products/**
.env
.env.*
credentials/**
secrets/**
provider configs
normal user homes
```

Graphify source/docs evidence used for command syntax is not P10.5B extraction input.

Decision marker:

```text
graphify_input_scope_reconfirmed
```

## Provider / Credential Boundary

P10.5B may use only local Ollama if exact command, local server, and local model availability are confirmed.

Blocked:

```text
OpenAI API
Anthropic API
Claude Code
Gemini API
hosted providers
provider fallback
provider key lookup
credential inspection
model pull without explicit gate
remote model use
```

P10.5B must preserve:

```text
no API keys
no credentials
no provider configs
no token stores
local-only execution
single approved attempt
safe block if local model missing
```

Decision marker:

```text
graphify_ollama_provider_boundary_defined
```

## Runtime Authorization Boundary

P10.3B does not authorize runtime.

P10.5B requires explicit human approval because it runs Graphify and may call local Ollama.

Required approval text for P10.5B:

```text
I approve P10.5B Graphify Controlled Rerun Execution With Ollama only, for one controlled local attempt using the exact command approved by P10.3B. Use only the approved Graphify input scope governed by `.graphifyignore`. Use only local Ollama. Do not pull models. Do not call hosted providers. Do not inspect credentials. Do not include product/Siamese, 4_external/sources, 9_artifacts, graphify-out as input, or secrets. Keep Graphify outputs local/untracked. Do not mutate Git. Do not use git add .
```

Decision marker:

```text
graphify_ollama_execution_not_authorized_by_p10_3b
```

## Expected P10.5B Outcomes

Outcome A - successful Ollama-backed Graphify rerun:

```text
graphify_ollama_controlled_rerun_execution_success
graphify_outputs_generated_local_untracked
graphify_visualization_evidence_candidate_created
```

Then proceed to:

```text
P10.6 - Graphify Markdown Evidence Refresh Report
P10.7 - Graphify Evidence Import Boundary
P10.R - Graphify Evidence Integration Closure
```

Outcome B - safe block before execution:

```text
graphify_ollama_rerun_blocked_before_execution
graphify_ollama_missing_model_or_command_or_preflight
```

Do not open a debug chain automatically.

Outcome C - runtime safe failure:

```text
graphify_ollama_runtime_safe_failure
graphify_outputs_not_validated
```

Stop immediately. Do not try alternative commands. Do not pull models. Do not switch provider. Do not inspect credentials.

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_ollama_provider_amendment.md
```

Not created / not approved:

```text
No Graphify execution
No Ollama execution
No Ollama model pull
No embeddings
No provider/API call
No Graphify output
No graphify-out changes
No GBrain execution
No GStack execution
No skill execution
No MCP registration
No browser daemon
No credential inspection
No product/Siamese source access
No generated output inspection
No .graphifyignore patch
No .gitignore patch
No Git mutation
No git add .
```

## Limitations

P10.3B did not inspect fresh Graphify source/docs because the allowed local path `4_external/sources/graphify` was absent.

The command candidate is resolved from accepted P10.5A-ALT governance evidence that previously inspected Graphify documentation. P10.5B must still stop if local executable syntax cannot be safely confirmed before runtime.

P10.3B does not determine whether Ollama is installed, running, authenticated, configured, or has a suitable model. It does not inspect `.ollama` config or normal user home state.

P10.3B does not determine whether `graphify-out/` currently contains output contents. P10.5B must handle output collision by path metadata only and must not inspect generated output contents without a future exact gate.

## Recommended Next Ticket

Recommended next ticket if P10.5B preflight is approved by the user:

```text
P10.5B - Graphify Ollama Controlled Execution
```

If command syntax cannot be confirmed safely before runtime, use:

```text
P10.3C - Graphify CLI Command Syntax Discovery Gate
```

If no local Ollama model is available and the user wants one, use:

```text
P10.OLLAMA-MODEL - Ollama Local Model Pull Authorization
```

Decision marker:

```text
p10_5b_graphify_ollama_controlled_execution_ready_after_amendment
```

## Commit Commands

If the amendment is accepted, stage only the intended governance amendment file. Do not stage Graphify outputs, sandbox outputs, unrelated files, or use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_ollama_provider_amendment.md
git commit -m "Amend Graphify rerun plan for Ollama"
git push
```

## Final Decision

P10.3B defines the Ollama provider amendment for a future P10.5B controlled Graphify attempt. The future command candidate is `graphify extract . --backend ollama`, using only approved input scope governed by `.graphifyignore`, local Ollama only, no model pull, no hosted providers, no credentials, and no output tracking. P10.3B does not authorize execution.

Final marker:

```text
graphify_controlled_rerun_plan_ollama_provider_amendment_ready
```
