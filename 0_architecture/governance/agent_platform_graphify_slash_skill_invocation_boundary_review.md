# Graphify Slash Skill Invocation Boundary Review

## Summary

P10.5F performed a no-runtime boundary review of the installed Graphify OpenCode slash-skill path versus the previously failed direct Ollama CLI path.

Result marker:

```text
graphify_slash_skill_invocation_boundary_review_ready
graphify_slash_skill_path_distinct_from_direct_cli_path
graphify_slash_skill_execution_not_authorized_now
graphify_opencode_install_not_authorized_now
graphify_opencode_local_model_boundary_required_next
graphify_outputs_remain_raw_generated_evidence_only
```

Decision outcome:

```text
OpenCode local-model boundary
```

Decision markers:

```text
graphify_slash_skill_invocation_boundary_review_ready
```

```yaml
P10_5F_Graphify_Slash_Skill_Invocation_Boundary_Review:
  ticket: "P10.5F"
  date: "2026-07-11"
  status: "diagnostic_review_only_no_runtime"
  output_file: "0_architecture/governance/agent_platform_graphify_slash_skill_invocation_boundary_review.md"
  selected_next_path: "OpenCode local-model boundary"
  controlled_slash_skill_execution_selected_now: false
  different_ollama_model_selection_selected_now: false
  graphify_closure_selected_now: false
  graphify_executable: "C:\\Users\\pablo\\anaconda3\\Scripts\\graphify.exe"
  graphify_package_root: "C:\\Users\\pablo\\anaconda3\\Lib\\site-packages\\graphify"
  graphify_distribution: "graphifyy 0.9.5"
  opencode_executable_found: "C:\\Users\\pablo\\AppData\\Roaming\\npm\\opencode.ps1"
  direct_cli_failure_dependency_confirmed: true
  p10_5d_dependency_confirmed: true
  p10_5e_dependency_confirmed: true
  p12_4_skill_boundary_confirmed: true
  slash_skill_executed: false
  graphify_extract_executed: false
  graphify_install_executed: false
  graphify_opencode_install_executed: false
  opencode_runtime_executed: false
  opencode_provider_config_inspected: false
  ollama_generation_executed: false
  ollama_model_pull_attempted: false
  dependency_install_attempted: false
  credential_inspection_attempted: false
  generated_output_contents_inspected: false
  generated_output_tracking_approved: false
  git_mutated: false
  final_marker: "graphify_slash_skill_invocation_boundary_review_ready"
```

## Scope

This review inspected installed Graphify package source and existing governance records only. It did not execute Graphify, OpenCode, Ollama generation, skill installation, slash commands, package installation, provider calls, subagents, tests, builds, cleanup, staging, commits, or output validation.

The question reviewed was whether `/graphify` in OpenCode is the same operational path as the failed direct command:

```text
graphify extract . --backend ollama --model qwen2.5-coder:7b --token-budget 4096 --api-timeout 240 --out graphify-out/p10_5e_ollama_configured_01
```

Conclusion:

```text
The OpenCode slash-skill path is materially distinct from the direct CLI path, but it is still a gated skill/tool/write/provider surface and is not executable without a later exact gate.
```

## Dependencies Confirmed

P10.5D marker confirmed:

```text
graphify_ollama_json_compliance_resolution_review_ready
```

P10.5E marker confirmed:

```text
graphify_ollama_configured_structured_output_retry_record_ready
```

P10.5E boundary marker confirmed:

```text
graphify_slash_skill_not_executed
```

P12.4 marker confirmed:

```text
skills_require_explicit_execution_gate
```

Graphify output authority posture confirmed from P10.4:

```text
Graphify output is generated evidence by default.
Graphify output is not authority.
Graphify output is not source of truth operativo.
Graphify output is not approval.
Graphify output is not runtime.
Graphify output is not Cognitive Semantic System substrate.
```

GBrain posture remains unchanged:

```text
GBrain Mode A remains valid for local memory/retrieval evidence. Graphify failures do not invalidate GBrain Mode A.
```

## Files Inspected

Governance and scope files inspected read-only:

```text
0_architecture/governance/agent_platform_graphify_ollama_json_compliance_resolution_review.md
0_architecture/governance/agent_platform_graphify_ollama_configured_structured_output_retry_record.md
0_architecture/governance/agent_platform_graphify_ollama_controlled_rerun_retry_record.md
0_architecture/governance/agent_platform_graphify_evidence_output_classification.md
0_architecture/governance/agent_platform_skill_authority_execution_boundary.md
0_architecture/governance/agent_platform_gbrain_adoption_graphify_semantic_replacement_decision.md
.graphifyignore
.gitignore
```

Installed package source inspected read-only:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skill-opencode.md
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skill-agents.md
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skills\agents\references\extraction-spec.md
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\__main__.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\detect.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\paths.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\export.py
```

Path metadata checked without inspecting contents:

```text
.opencode/: absent
opencode.json: absent
AGENTS.md: absent
0_architecture/governance/agent_platform_graphify_slash_skill_invocation_boundary_review.md: absent before creation
```

## Not Inspected

Blocked scopes not inspected:

```text
.env
.env.*
credentials/**
secrets/**
provider configs
browser auth
local credential stores
API keys
normal user OpenCode config contents
normal user Ollama config contents
normal user .gbrain contents
normal user .gstack contents
graphify-out/** contents
9_artifacts/** contents
2_products/**
product/**
products/**
4_external/sources/** contents
```

## Slash Skill Invocation Syntax

The installed OpenCode skill declares these relevant slash invocations:

```text
/graphify
/graphify <path>
/graphify .
/graphify https://github.com/<owner>/<repo>
/graphify <path> --mode deep
/graphify <path> --update
/graphify <path> --cluster-only
/graphify query "<question>"
/graphify path "A" "B"
/graphify explain "X"
```

The skill also declares this defaulting rule:

```text
If no path was given, use . (current directory). Do not ask the user for a path.
```

Therefore `/graphify` and `/graphify .` both imply current-directory processing when invoked as a build command.

## Direct CLI Path Classification

The failed P10.5B-RERUN and P10.5E attempts used the direct CLI path:

```text
graphify extract . --backend ollama ...
```

Installed `__main__.py` classifies `graphify extract` as headless full-pipeline extraction for CI/scripts. Its source explicitly says this path is unlike the skill path and calls `extract_corpus_parallel` directly using the selected backend.

Direct CLI extraction flow:

```text
detect
AST extraction on code
semantic LLM extraction on docs/papers/images through selected backend
merge
build
cluster
write graph.json and analysis sidecar
```

For `--backend ollama`, `llm.py` uses the OpenAI-compatible client against `OLLAMA_BASE_URL` with model defaults from `OLLAMA_MODEL` or `qwen2.5-coder:7b`.

No `response_format` or `json_schema` enforcement was found in the direct Ollama client path. JSON compliance is prompt-driven, parsed with strict JSON loading, and recovered through hollow-response and adaptive retry behavior.

## Slash Skill Path Classification

The OpenCode slash-skill path is not a direct wrapper around `graphify extract .` for the default build. The skill orchestrates an agent workflow and inline Python snippets.

Default slash-skill build flow:

```text
ensure Graphify import/interpreter
write graphify-out/.graphify_python
write graphify-out/.graphify_root
run graphify.detect.detect(INPUT_PATH)
write graphify-out/.graphify_detect.json
run graphify.extract.extract() for code files
write graphify-out/.graphify_ast.json
perform semantic extraction for docs/papers/images through Gemini or host agents
write graphify-out/.graphify_semantic*.json and chunk files
merge AST and semantic extraction
write graphify-out/.graphify_extract.json
build graph with graphify.build.build_from_json()
cluster, analyze, generate report
write graphify-out/graph.json
write graphify-out/GRAPH_REPORT.md
write graphify-out/.graphify_analysis.json
write graphify-out/.graphify_labels.json
export graph.html unless disabled
write graphify-out/cost.json
write/update manifest
cleanup selected intermediate files
```

For OpenCode semantic extraction, the skill states:

```text
OpenCode platform: Uses @mention dispatch instead of the Agent tool. All mentions in a single message run in parallel.
```

The exact extraction subagent prompt requires:

```text
Output ONLY valid JSON matching the schema below - no explanation, no markdown fences, no preamble.
Then write the JSON to disk using the Write tool at this exact absolute path.
```

This means slash-skill semantic extraction is host-agent-owned unless the Gemini environment path is explicitly used.

## Host Model Ownership

The OpenCode slash-skill path has these model ownership branches:

| Condition | Semantic owner | Boundary |
| --- | --- | --- |
| Code-only corpus | Graphify AST extractor only | No semantic LLM needed. |
| `GEMINI_API_KEY` or `GOOGLE_API_KEY` present | Graphify Python Gemini backend | Provider/API boundary required. |
| No Gemini key and docs/papers/images present | Host agent/subagents | OpenCode provider/model boundary required. |
| Direct `graphify extract --backend ollama` | Graphify Python Ollama backend | Direct CLI Ollama path; already failed with current model/settings. |

The current repository input scope includes governance markdown and README material, so a full allowed-scope `/graphify .` run would not be code-only. It would need semantic extraction for markdown unless narrowed to a code-only path.

OpenCode local Ollama feasibility is not confirmed in this ticket. Confirming it would require a future exact boundary for OpenCode provider/model metadata and possibly configuration. Current user-level OpenCode provider config contents were not inspected.

## Install And Registration Surfaces

OpenCode project install is mutating.

Installed Graphify source shows project-scope OpenCode installation can write:

```text
.opencode/skills/graphify/SKILL.md
.opencode/skills/graphify/.graphify_version
AGENTS.md
.opencode/plugins/graphify.js
.opencode/opencode.json
```

The OpenCode plugin is a `tool.execute.before` hook. It writes a reminder into bash command output when `graphify-out/graph.json` exists.

The OpenCode project install path registers the plugin in `.opencode/opencode.json` under `plugin`.

Therefore installation maps to settings/plugin/hook mutation, not just documentation placement.

No OpenCode project install, user install, plugin registration, skill registration, AGENTS.md write, or slash command setup was performed by P10.5F.

## Agent And Write Surfaces

The slash-skill default build can use these execution/write surfaces:

| Surface | Observed source | Boundary classification |
| --- | --- | --- |
| Shell/local commands | skill bash blocks | `SKILL_RUN_LOCAL_COMMANDS` |
| File writes under `graphify-out/` | skill Python snippets and exports | `SKILL_WRITE_APPROVED_FILES` |
| OpenCode `@agent` semantic chunks | skill Step B2 | agent/subagent execution gate |
| Subagent Write tool for chunk JSON | extraction spec | file-write gate plus agent gate |
| Gemini path if keys present | skill Step 3 | provider/API gate |
| OpenCode host model if no Gemini key | skill Step B2 | OpenCode provider/model boundary |
| OpenCode plugin install | `__main__.py` | settings/hook registration gate |
| GitHub clone flow | skill Step 0 | network/external-source gate |
| Neo4j/FalkorDB/MCP/export flags | skill usage section | database/MCP/network gates when flags present |

These surfaces are not authorized by slash-skill presence alone.

## Input Scope Enforcement

The repository `.graphifyignore` is a default-deny profile with explicit allow patterns for governed evidence scope and hard blockers for credentials, provider material, products, external sources, artifacts, and `graphify-out/**`.

Relevant allowed patterns:

```text
README.md
0_architecture/**/*.md
3_platform/_governed_skeleton/**/*.py
```

Relevant blocked patterns:

```text
.env
.env.*
credentials/**
secrets/**
**/*credential*/**
**/*secret*/**
**/*token*/**
**/*provider*config*/**
**/*auth*/**
4_external/sources/**
9_artifacts/**
graphify-out/**
2_products/**
product/**
products/**
```

Installed `detect.py` loads `.gitignore` and `.graphifyignore` from the VCS ceiling down to the scan root. `.gitignore` is read first and `.graphifyignore` is read last, so later `.graphifyignore` rules win under last-match-wins semantics.

Installed `detect.py` also skips common sensitive files and directories, including `.env`, `.envrc`, private keys, cloud credentials, `.ssh`, `.aws`, `.gcloud`, `secrets`, and `credentials`.

Installed `detect.py` also skips generated/noise directories including `graphify-out`, dependency folders, build outputs, caches, and `.graphify`.

## Output And Overwrite Risks

Default slash-skill writes are concentrated under `graphify-out/` but are not zero-risk. Expected outputs and intermediates include:

```text
graphify-out/.graphify_python
graphify-out/.graphify_root
graphify-out/.graphify_detect.json
graphify-out/.graphify_ast.json
graphify-out/.graphify_semantic.json
graphify-out/.graphify_semantic_new.json
graphify-out/.graphify_cached.json
graphify-out/.graphify_uncached.txt
graphify-out/.graphify_chunk_NN.json
graphify-out/.graphify_extract.json
graphify-out/graph.json
graphify-out/GRAPH_REPORT.md
graphify-out/.graphify_analysis.json
graphify-out/.graphify_labels.json
graphify-out/cost.json
graphify-out/manifest.json
graphify-out/graph.html
```

Optional flags can add other outputs, including Obsidian vault files, SVG, GraphML, Cypher files, wiki files, MCP behavior, or database pushes.

The skill path includes a shrink guard before overwriting `graphify-out/graph.json`; if a new graph is smaller than the existing graph, `to_json()` can refuse the write and the skill stops rather than continuing with report output.

Installed `export.py` can back up protected graph artifacts before overwrite when a semantic marker or curated labels exist. Backup failure does not block writing.

Partial-output risk remains because the skill writes multiple intermediate files and chunk files before final outputs. A failure can leave incomplete `graphify-out/` intermediates. P10.5F did not inspect, clean, delete, validate, stage, or import any generated output contents.

## P12.4 Permission Mapping

Under P12.4, the slash-skill path requires gates beyond documentation review.

Permission mapping:

| Slash-skill behavior | P12.4 permission class | Current posture |
| --- | --- | --- |
| Read skill docs/source metadata | `SKILL_READ_DOCS`, `SKILL_READ_SOURCE_METADATA` | Allowed after source review. |
| Run local Python/bash snippets | `SKILL_RUN_LOCAL_COMMANDS` | Gated. |
| Write `graphify-out/*` | `SKILL_WRITE_APPROVED_FILES` | Gated. |
| Dispatch OpenCode subagents | Agent/subagent execution boundary | Gated. |
| Use host model/provider | `SKILL_USE_PROVIDER` or OpenCode provider/model boundary | Blocked until exact gate. |
| Use Gemini API path | `SKILL_USE_PROVIDER` | Blocked until exact provider gate. |
| Install OpenCode plugin/config | `SKILL_REGISTER_HOOKS`, `SKILL_MODIFY_SETTINGS` | Blocked. |
| Use MCP/database/network flags | `SKILL_USE_MCP`, provider/network/database gates | Blocked. |
| Mutate Git or stage outputs | `SKILL_MUTATE_GIT` | Blocked. |

P12.4 boundary rule applies:

```text
A skill can recommend; governance approves; execution gates execute.
```

Therefore `/graphify` is not self-authorizing.

## Local Ollama Through OpenCode

Local Ollama through OpenCode remains an unconfirmed future path.

Current facts:

```text
OpenCode executable exists.
OpenCode help metadata exists.
User OpenCode config root exists by prior metadata check.
OpenCode provider config contents were not inspected.
No repo-local .opencode skill/config exists.
No project AGENTS.md exists.
No project opencode.json exists.
```

Boundary classification:

```text
OpenCode local-model use is possible only after a future exact boundary determines whether OpenCode is already configured for a local model or authorizes a controlled local-model configuration path.
```

This review does not authorize inspecting OpenCode provider config contents, editing OpenCode config, selecting OpenCode models, starting OpenCode runtime, spawning subagents, or sending corpus content through the current host model.

## Outcome Selection

Exactly one next path is selected:

```text
OpenCode local-model boundary
```

Rationale:

```text
Controlled slash-skill execution is not selected now because `/graphify .` would require local command execution, file writes, OpenCode subagent/tool use, and host-model/provider clarity.

Different Ollama model selection is not selected now because it continues the already-failed direct CLI Ollama branch and does not resolve the OpenCode slash-skill host boundary.

Graphify closure is not selected now because the slash-skill path is materially distinct from the failed direct CLI path and may remain useful as a governed evidence-map workflow.

OpenCode local-model boundary is selected because it is the minimum next governance step before any slash-skill execution can be considered without provider ambiguity.
```

## Next Gate Requirements

The selected next gate should answer only the OpenCode local-model boundary question.

Minimum required decisions:

```text
whether OpenCode provider/model metadata may be inspected
whether current OpenCode model ownership can be classified without credential exposure
whether local Ollama use through OpenCode is already available, unavailable, or requires configuration
whether configuration is prohibited, deferred, or separately approvable
whether slash-skill semantic extraction may use the host model at all
whether a code-only narrowed `/graphify` run can avoid semantic host-model use
```

Still blocked until a later exact gate:

```text
/graphify
/graphify .
graphify extract
graphify install
graphify opencode install
OpenCode runtime execution
OpenCode subagent spawning
Ollama generation
Ollama model pull
provider/API calls
credential inspection
provider config content inspection without exact approval
graphify-out/** content inspection
output cleanup/deletion
generated output tracking
Git staging/commit/push
```

## Final Declaration

P10.5F is complete as a no-runtime diagnostic review. The OpenCode slash-skill path is distinct from the failed direct Ollama CLI path, but it remains blocked for execution and installation until future exact gates approve the required local command, write, agent/subagent, provider/model, and settings/plugin surfaces.

Final marker:

```text
graphify_slash_skill_invocation_boundary_review_ready
```
