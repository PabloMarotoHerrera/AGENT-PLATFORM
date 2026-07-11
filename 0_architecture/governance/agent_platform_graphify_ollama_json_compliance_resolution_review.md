# Graphify Ollama JSON Compliance Resolution Review

## Summary

P10.5D performed a diagnostic, no-runtime review of the installed Graphify package source used by the local `graphify.exe`, focused on the P10.5B-RERUN Ollama structured-output failure.

P10.5B-RERUN posture was confirmed from the existing retry record:

```text
graphify_ollama_controlled_rerun_retry_record_ready
graphify_ollama_rerun_retry_runtime_safe_failure
graphify_outputs_not_validated_after_retry
```

The remaining failure is classified as an Ollama structured-output / JSON-compliance failure, not the prior missing Python `openai` dependency. P10.5B-RERUN verified `openai 2.45.0`, reached the local Ollama backend, then recorded invalid JSON / hollow response behavior before timeout.

Result marker:

```text
graphify_ollama_json_compliance_resolution_review_ready
```

Decision markers:

```text
graphify_ollama_json_failure_classified
graphify_installed_package_source_inspected_readonly
graphify_ollama_prompt_contract_identified
graphify_ollama_structured_output_knobs_identified
graphify_model_suitability_risk_classified
graphify_no_runtime_retry_authorized_by_p10_5d
graphify_no_model_pull_authorized_by_p10_5d
graphify_no_dependency_install_authorized_by_p10_5d
p10_next_resolution_path_selected
```

Selected diagnostic outcome:

```text
Outcome A - supported configuration fix exists, with model suitability risk documented
```

Outcome A markers:

```text
graphify_ollama_supported_configuration_fix_identified
p10_5e_graphify_ollama_configured_retry_ready
```

Slash-skill / agentic invocation marker:

```text
graphify_slash_skill_agentic_invocation_path_identified
```

```yaml
P10_5D_Graphify_Ollama_JSON_Compliance_Resolution_Review:
  ticket: "P10.5D"
  date: "2026-07-11"
  status: "diagnostic_review_only_no_runtime"
  output_file: "0_architecture/governance/agent_platform_graphify_ollama_json_compliance_resolution_review.md"
  p10_5b_rerun_record_confirmed: true
  p10_5b_rerun_runtime_safe_failure_confirmed: true
  p10_5b_rerun_outputs_not_validated_confirmed: true
  openai_dependency_remediation_verified_by_prior_record: true
  graphify_reached_ollama_confirmed_by_prior_record: true
  invalid_json_hollow_response_confirmed_by_prior_record: true
  graphify_executable: "C:\\Users\\pablo\\anaconda3\\Scripts\\graphify.exe"
  graphify_package_file: "C:\\Users\\pablo\\anaconda3\\Lib\\site-packages\\graphify\\__init__.py"
  graphify_package_root: "C:\\Users\\pablo\\anaconda3\\Lib\\site-packages\\graphify"
  installed_distribution: "graphifyy 0.9.5"
  source_inspection_mode: "read_only"
  graphify_runtime_executed: false
  graphify_extract_executed: false
  ollama_generation_executed: false
  ollama_model_pull_attempted: false
  dependency_install_attempted: false
  credential_inspection_attempted: false
  generated_output_contents_inspected: false
  git_mutated: false
  selected_outcome: "Outcome A - supported configuration fix exists, with model suitability risk documented"
  selected_next_ticket: "P10.5E - Graphify Ollama Configured Structured Output Retry"
  fallback_if_configured_retry_rejected_or_fails: "P10.OLLAMA-MODEL - Ollama Structured Output Model Selection / Pull Authorization"
  final_marker: "graphify_ollama_json_compliance_resolution_review_ready"
```

## Files Inspected

Governance and scope files inspected read-only by path check, bounded read, or marker search:

```text
0_architecture/governance/agent_platform_graphify_ollama_controlled_rerun_retry_record.md
0_architecture/governance/agent_platform_graphify_ollama_controlled_rerun_execution_record.md
0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_ollama_provider_amendment.md
0_architecture/governance/agent_platform_graphify_evidence_output_classification.md
.graphifyignore
.gitignore
```

Installed Graphify package source inspected read-only:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\__main__.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\extract.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\paths.py
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skill-opencode.md
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skill-agents.md
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skills\agents\references\extraction-spec.md
```

Installed package source search was performed read-only across allowed `*.py` and `*.md` package files for approved patterns including Ollama, OpenAI-compatible client usage, JSON/schema/prompt terms, tuning variables, and slash-skill / agentic invocation terms.

Generated output metadata checked only by path existence:

```text
graphify-out/
graphify-out/p10_5b_ollama_rerun_01/
```

No generated output contents were inspected. No recursive `graphify-out/**` inspection was performed.

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
normal user .ollama configs
normal user .gbrain
normal user .gstack
browser cookie stores
9_artifacts/** contents
2_products/**
product/**
products/**
raw Graphify outputs
4_external/sources/**
4_external/sources/gbrain-master/node_modules/**
4_external/sources/gstack-main/node_modules/**
4_external/sources/graphify/node_modules/**
global package caches
Bun cache contents
DB internals under 9_artifacts/**
generated home internals under 9_artifacts/**
```

## Files Created

Created exactly one diagnostic governance file:

```text
0_architecture/governance/agent_platform_graphify_ollama_json_compliance_resolution_review.md
```

## Files Modified

No existing governance, source, ignore, product, external, GBrain, GStack, Graphify package, generated-output, or Git file was intentionally modified by P10.5D.

## Commands Run

Allowed commands run:

```text
git status --short
Test-Path 0_architecture/governance/agent_platform_graphify_ollama_controlled_rerun_retry_record.md
Test-Path 0_architecture/governance/agent_platform_graphify_ollama_controlled_rerun_execution_record.md
Test-Path 0_architecture/governance/agent_platform_graphify_controlled_rerun_plan_ollama_provider_amendment.md
Test-Path 0_architecture/governance/agent_platform_graphify_evidence_output_classification.md
Test-Path .graphifyignore
Test-Path .gitignore
Get-Command graphify -ErrorAction SilentlyContinue
& "C:\Users\pablo\anaconda3\python.exe" -c "import graphify, inspect; print(graphify.__file__)"
& "C:\Users\pablo\anaconda3\python.exe" -c "import importlib.metadata as m; candidates=['graphify','graphifyy']; names={d.metadata['Name']: d for d in m.distributions()}; [print(c, m.version(c)) for c in candidates if c in names]"
graphify --help
graphify extract --help
ollama list
Test-Path graphify-out
Test-Path graphify-out/p10_5b_ollama_rerun_01
```

Read-only repository/package searches and bounded file reads were also performed using approved inspection tooling.

Explicitly not run:

```text
graphify extract
graphify runtime commands
ollama run
ollama pull
ollama serve
pip
pip install
python -m pip
conda install
OpenAI commands
Anthropic commands
Claude Code commands
Gemini commands
provider commands
bun
npm
node
docker
tests
builds
scripts
CI
MCP servers
browser daemons
ngrok
git add
git commit
git push
git add .
```

## P10.5B-RERUN Dependency Status

P10.5B-RERUN record exists:

```text
0_architecture/governance/agent_platform_graphify_ollama_controlled_rerun_retry_record.md
```

Confirmed markers:

```text
graphify_ollama_controlled_rerun_retry_record_ready
graphify_ollama_rerun_retry_runtime_safe_failure
graphify_outputs_not_validated_after_retry
```

Confirmed from the retry record:

```text
openai 2.45.0
qwen2.5-coder:7b
Graphify selected the Ollama backend
LLM returned invalid JSON, skipping chunk
ollama returned a hollow response
```

Classification:

```text
graphify_ollama_json_failure_classified
```

The prior missing dependency issue is not the active P10.5D failure class. The active failure class is local Ollama structured-output non-compliance and/or resource/context pressure causing invalid JSON, hollow responses, adaptive splitting, and timeout before validated completion.

## Graphify Package Path Discovery

Graphify command path:

```text
C:\Users\pablo\anaconda3\Scripts\graphify.exe
```

Python package file:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\__init__.py
```

Package root:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify
```

Distribution metadata:

```text
graphifyy 0.9.5
```

Decision marker:

```text
graphify_installed_package_source_inspected_readonly
```

## Graphify Installed Package Source Inspection

The installed package contains two relevant invocation paths.

Direct headless CLI path:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\__main__.py:4343-4349
```

The direct path is described in source as headless extraction for CI/scripts and explicitly differs from the skill path:

```text
Runs detect -> AST extraction on code -> semantic LLM extraction on docs/papers/images -> merge -> build -> cluster -> write outputs.
Unlike the skill.md path (which runs through Claude Code subagents), this calls extract_corpus_parallel directly using whichever backend has an API key set.
```

Slash-skill / agentic path:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skill-opencode.md
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skill-agents.md
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skills\agents\references\extraction-spec.md
```

The tutorial-style workflow is primarily `/graphify` through a host agent/skill. The installed CLI help advertises `graphify install`, `graphify opencode install`, and many platform integrations. The installed `skill-opencode.md` documents `/graphify`, OpenCode `@mention` dispatch, and the agentic semantic-extraction prompt file.

Decision marker:

```text
graphify_slash_skill_agentic_invocation_path_identified
```

Implication for P10.5B-RERUN:

```text
P10.5B-RERUN used the direct headless CLI path, not the slash-skill host-agent path.
The observed JSON compliance failure therefore belongs to Graphify's direct OpenAI-compatible Ollama backend path.
```

## Graphify Ollama Backend Implementation

Ollama backend configuration is defined in:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py:85-92
```

Relevant source facts:

```text
base_url: OLLAMA_BASE_URL or http://localhost:11434/v1
default_model: OLLAMA_MODEL or qwen2.5-coder:7b
max_tokens: 16384
```

Graphify calls Ollama through the OpenAI-compatible Python client in:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py:900-996
```

The request shape includes:

```text
OpenAI(api_key=..., base_url=..., timeout=..., max_retries=...)
client.chat.completions.create(...)
messages = system extraction prompt + user content
max_completion_tokens
stream = False
temperature when not omitted
extra_body for supported backend options
```

For `backend == "ollama"`, Graphify derives an Ollama `num_ctx` value and sends it through `extra_body`:

```text
extra_body = {"options": {"num_ctx": num_ctx}, "keep_alive": keep_alive}
```

The no-key local Ollama behavior is implemented in:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py:1362-1374
```

Graphify uses placeholder key `ollama` when local Ollama has no `OLLAMA_API_KEY` and emits a warning. P10.5B-RERUN observed that exact warning. No credential value is required for local loopback Ollama.

Ollama base URL validation is implemented in:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py:2054-2099
```

Graphify warns on non-loopback Ollama endpoints and blocks link-local/metadata hosts.

## Graphify Prompt / Schema Contract

Direct CLI semantic extraction uses `_EXTRACTION_SYSTEM` in:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py:391-420
```

The prompt requires:

```text
Output ONLY valid JSON - no explanation, no markdown fences, no preamble.
```

The direct CLI schema contract is exactly shaped as:

```text
{
  "nodes": [
    {
      "id": "stem_entity",
      "label": "Human Readable Name",
      "file_type": "code|document|paper|image|rationale|concept",
      "source_file": "relative/path",
      "source_location": null,
      "source_url": null,
      "captured_at": null,
      "author": null,
      "contributor": null
    }
  ],
  "edges": [
    {
      "source": "node_id",
      "target": "node_id",
      "relation": "calls|implements|references|cites|conceptually_related_to|shares_data_with|semantically_similar_to",
      "confidence": "EXTRACTED|INFERRED|AMBIGUOUS",
      "confidence_score": 1.0,
      "source_file": "relative/path",
      "source_location": null,
      "weight": 1.0
    }
  ],
  "hyperedges": [
    {
      "id": "snake_case_id",
      "label": "Human Readable Label",
      "nodes": ["node_id1", "node_id2", "node_id3"],
      "relation": "participate_in|implement|form",
      "confidence": "EXTRACTED|INFERRED",
      "confidence_score": 0.75,
      "source_file": "relative/path"
    }
  ],
  "input_tokens": 0,
  "output_tokens": 0
}
```

Graphify wraps file content in `<untrusted_source>` blocks and instructs the model to treat all source text as data, not instructions:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py:400-406
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py:478-521
```

The slash-skill / host-agent extraction contract is documented separately in:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\skills\agents\references\extraction-spec.md:6-70
```

That path instructs host agents/subagents to output JSON and write chunk files. It includes a more detailed schema/rubric, deterministic node-ID rules, absolute `source_file` behavior for chunk prompts, confidence-score rubric, and a `rationale_for` relation not present in the direct CLI `_EXTRACTION_SYSTEM` relation list.

Decision marker:

```text
graphify_ollama_prompt_contract_identified
```

## Structured Output Controls

Supported direct CLI / environment controls identified:

```text
--model M
OLLAMA_MODEL
--token-budget N
--max-concurrency N
--api-timeout S
GRAPHIFY_API_TIMEOUT
GRAPHIFY_MAX_OUTPUT_TOKENS
GRAPHIFY_LLM_TEMPERATURE
GRAPHIFY_MAX_RETRIES
GRAPHIFY_OLLAMA_NUM_CTX
GRAPHIFY_OLLAMA_KEEP_ALIVE
GRAPHIFY_OLLAMA_VISION
GRAPHIFY_OLLAMA_PARALLEL
```

Important defaults / behavior:

```text
temperature defaults to 0 for Ollama
max output tokens defaults to 16384 for Ollama
token_budget defaults to 60000
Ollama max concurrency is forced to 1 unless GRAPHIFY_OLLAMA_PARALLEL=1
Ollama num_ctx is auto-derived unless GRAPHIFY_OLLAMA_NUM_CTX is set
keep_alive defaults to 30m
```

No installed package source match was found for direct built-in Ollama use of:

```text
response_format
json_schema
json_object
```

Therefore Graphify's built-in direct Ollama path enforces JSON primarily by prompt contract and parse/retry behavior, not by a native OpenAI-compatible JSON mode or response schema parameter.

Custom provider source support for `extra_body` exists, but it is not selected by P10.5D as a remediation path because it would require provider configuration governance and P10.5D did not inspect provider config files.

Decision marker:

```text
graphify_ollama_structured_output_knobs_identified
```

## Chunking / Max-Token Controls

Chunking and adaptive retry implementation is in:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\llm.py:1438-1859
```

Key behavior:

```text
Files are token-estimated and packed by token budget.
Default token_budget is 60000.
Each file read into prompt is capped at 20000 characters unless represented as a slice.
Oversized splittable documents can be sliced.
When finish_reason == length, Graphify bisects the chunk and retries.
Hollow Ollama responses are relabeled as length so the same bisection path runs.
Default max_retry_depth is 3.
Failed chunks are logged and skipped.
If every requested semantic chunk fails, graphify extract exits with an error.
```

The direct CLI wires chunking knobs in:

```text
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\__main__.py:4430-4459
C:\Users\pablo\anaconda3\Lib\site-packages\graphify\__main__.py:4706-4738
```

The installed source itself recommends smaller chunks for the observed symptom class:

```text
[graphify] warning: ollama returned very few tokens - likely causes:
(1) VRAM pressure: check `nvidia-smi` and reduce chunk size with --token-budget (e.g. --token-budget 4096) or set GRAPHIFY_OLLAMA_NUM_CTX to a smaller value;
(2) model too small for JSON instruction following - try a larger model with --model (e.g. --model qwen2.5-coder:14b).
```

P10.5D did not run `nvidia-smi`, did not inspect hardware state, did not run Ollama generation, and did not retry extraction.

## Model Selection Controls

Model selection is supported by:

```text
--model M
OLLAMA_MODEL
```

The installed Ollama default is:

```text
qwen2.5-coder:7b
```

Current local Ollama inventory confirmed by metadata-only `ollama list`:

```text
qwen2.5-coder:7b
nomic-embed-text:latest
```

No model generation was run. No model was pulled. No normal user `.ollama` config was inspected.

Installed package Markdown did not surface an Ollama tutorial/manual recommendation for a specific model. The model guidance found in source is a runtime warning suggesting `qwen2.5-coder:14b` when Ollama returns very few tokens or when the model is too small for JSON instruction following.

## Model Suitability Classification

Classification:

```text
qwen2.5-coder:7b is a material suitability risk for Graphify's strict JSON contract, but P10.5D does not prove it unsuitable by source inspection alone.
```

Rationale:

```text
Graphify's direct Ollama path relies on prompt-following for strict JSON.
No response_format/json_schema enforcement was identified for built-in Ollama.
The observed P10.5B-RERUN symptoms match Graphify's own warning class: hollow/very-low-token/invalid JSON responses.
The installed source explicitly names model size / JSON instruction following as a possible cause and suggests a larger qwen2.5-coder:14b model as an example.
The installed source also identifies VRAM/context pressure as another possible cause, which may be mitigated by supported configuration without a model pull.
```

Decision marker:

```text
graphify_model_suitability_risk_classified
```

P10.5D does not authorize model testing or model pulling. A direct manual Ollama prompt test would be Ollama generation and must be separately gated if desired.

## Generated Output Metadata Status

Path metadata only:

```text
Test-Path graphify-out: true
Test-Path graphify-out/p10_5b_ollama_rerun_01: true
```

Output directory behavior from source:

```text
--out DIR makes Graphify write to <DIR>/graphify-out/
```

Because P10.5B-RERUN used:

```text
--out graphify-out/p10_5b_ollama_rerun_01
```

the expected generated output root shape is:

```text
graphify-out/p10_5b_ollama_rerun_01/graphify-out/
```

P10.5D did not inspect that directory's contents and did not validate any generated output.

## GBrain Mode B Implication

GBrain distinction preserved:

```text
GBrain Mode A keyword-only retrieval remains valid.
Graphify Ollama structured JSON failure does not invalidate GBrain Mode A.
Graphify Ollama structured JSON failure increases risk for future GBrain Mode B / LLM-backed graph extraction / structured-output workflows.
Any future GBrain Mode B must require its own model suitability and output validation gate.
```

P10.5D does not alter P12 closure. GBrain remains the preferred local semantic/retrieval candidate from P12, while Graphify remains evidence-map / visualization / report candidate only.

## Decision Outcome

Selected outcome:

```text
Outcome A - supported configuration fix exists
```

Markers:

```text
graphify_ollama_supported_configuration_fix_identified
p10_5e_graphify_ollama_configured_retry_ready
p10_next_resolution_path_selected
```

Why Outcome A is selected:

```text
The installed direct Ollama path exposes local-only configuration controls that match the observed failure class: --token-budget, --model, --api-timeout, GRAPHIFY_OLLAMA_NUM_CTX, GRAPHIFY_MAX_OUTPUT_TOKENS, GRAPHIFY_LLM_TEMPERATURE, GRAPHIFY_OLLAMA_KEEP_ALIVE, and default serial Ollama execution.
```

Important limitation on Outcome A:

```text
No native response_format/json_schema enforcement was identified for built-in Ollama. The configured retry path can reduce context/resource pressure and improve determinism, but it cannot guarantee JSON compliance at the API schema layer.
```

Model suitability risk remains material. If a configured retry is not approved, or if it fails with the same invalid JSON/hollow response class, the next decision should move to explicit model selection / pull authorization instead of repeated same-model retries.

P10.5D authorization boundaries:

```text
graphify_no_runtime_retry_authorized_by_p10_5d
graphify_no_model_pull_authorized_by_p10_5d
graphify_no_dependency_install_authorized_by_p10_5d
```

## Recommended Next Ticket

Recommended next ticket:

```text
P10.5E - Graphify Ollama Configured Structured Output Retry
```

P10.5E should be a separate explicit runtime gate. It should decide whether to authorize exactly one local configured retry, likely using the already-installed `qwen2.5-coder:7b` model first with smaller chunks and explicit local-only controls.

Candidate configuration direction for P10.5E to evaluate, not execute under P10.5D:

```text
Use --token-budget to reduce chunk size from the 60000 default.
Preserve or explicitly set serial Ollama concurrency.
Set a retry-specific --out root with no output collision.
Consider GRAPHIFY_OLLAMA_NUM_CTX only if the ticket explicitly approves an environment override.
Keep temperature deterministic.
Keep outputs local/untracked and unvalidated until completion is confirmed.
```

P10.5E must not automatically authorize:

```text
model pull
hosted provider fallback
credential inspection
provider config inspection
normal user .ollama config inspection
dependency install
generated output content inspection before a success gate
Git mutation
```

Fallback if P10.5E is rejected or fails with the same symptom class:

```text
P10.OLLAMA-MODEL - Ollama Structured Output Model Selection / Pull Authorization
```

That fallback must be explicit because model pull changes local disk state and may use network.

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_graphify_ollama_json_compliance_resolution_review.md
```

Not created / not approved:

```text
No Graphify rerun
No Ollama generation
No Ollama model pull
No dependency install
No pip
No conda install
No hosted provider call
No credential inspection
No .env inspection
No provider config inspection
No token store inspection
No normal user .ollama config inspection
No generated output validation
No generated output import
No generated output cleanup
No generated output tracking
No Graphify output staging
No GBrain execution
No GStack execution
No memory reindex
No Git mutation
No git add .
```

## Limitations

P10.5D is source-inspection only. It did not test any model response, run any Graphify extraction, or validate any generated output.

No official external Graphify documentation was fetched. Installed package Markdown did not provide a local Ollama-specific tutorial recommending a model.

P10.5D did not inspect provider configuration files, normal user Ollama configuration, hardware state, GPU memory, generated output contents, or Graphify caches.

The selected Outcome A is a governed next-step recommendation, not runtime authorization.

## Commit Commands

If the diagnostic review is accepted, stage only the diagnostic governance file. Do not stage Graphify outputs, sandbox outputs, unrelated files, or use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_graphify_ollama_json_compliance_resolution_review.md
git commit -m "Review Graphify Ollama structured output failure"
git push
```

## Final Decision

P10.5D confirms that Graphify's direct Ollama backend uses the OpenAI-compatible chat completion path with a prompt-only strict JSON contract, deterministic temperature, adaptive chunk splitting, and Ollama-specific context/keep-alive controls. Built-in Ollama `response_format` / JSON schema enforcement was not identified. The next governed path is P10.5E, a separately approved configured local retry using supported chunk/context/model controls. Model suitability risk for `qwen2.5-coder:7b` is material and should move to a separate model selection / pull authorization gate if the configured retry is rejected or fails.

Final marker:

```text
graphify_ollama_json_compliance_resolution_review_ready
```
