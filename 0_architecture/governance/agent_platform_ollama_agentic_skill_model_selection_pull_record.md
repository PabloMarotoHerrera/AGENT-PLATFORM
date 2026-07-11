# Ollama Agentic Skill Model Selection / Pull Record

## Summary

P10.OLLAMA-MODEL selected and locally provisioned exactly one materially different Ollama model candidate for a future Graphify OpenCode agentic execution:

```text
qwen3.5:9b
```

Outcome:

```text
Outcome A - new model pull succeeds
```

The exact model was absent during preflight. Hardware and storage metadata passed the ticket thresholds. The exact authorized pull command was executed once, downloaded the model, verified its SHA-256 digest, wrote its manifest, and returned success.

Post-pull inventory contains the exact `qwen3.5:9b` tag. Model metadata is readable and reports a Qwen35 architecture, 9.7B parameters, Q4_K_M quantization, 262,144-token model context, and tool capability. Existing `qwen2.5-coder:7b` and `nomic-embed-text:latest` models remain present.

No model inference, OpenCode launch/configuration, Graphify execution, credential inspection, output inspection, dependency installation, or Git mutation occurred.

Result marker:

```text
ollama_agentic_skill_model_selection_pull_record_ready
```

Success markers:

```text
ollama_agentic_model_qwen3_5_9b_selected
ollama_qwen3_5_9b_hardware_fit_candidate_confirmed
ollama_qwen3_5_9b_pull_authorized
ollama_qwen3_5_9b_pull_success
ollama_qwen3_5_9b_local_inventory_verified
ollama_qwen3_5_9b_metadata_verified
ollama_qwen2_5_coder_7b_preserved
ollama_no_model_inference
ollama_no_opencode_config_mutation
ollama_no_graphify_runtime
ollama_no_credentials_inspected
ollama_no_git_mutation
p10_5i_qwen3_5_9b_opencode_integration_ready
```

```yaml
P10_OLLAMA_MODEL_Agentic_Skill_Model_Selection_Pull_Record:
  ticket: "P10.OLLAMA-MODEL"
  date: "2026-07-11"
  outcome: "Outcome A - new model pull succeeds"
  output_file: "0_architecture/governance/agent_platform_ollama_agentic_skill_model_selection_pull_record.md"
  explicit_human_approval_present: true
  p10_5h_dependency_confirmed: true
  p10_5h_same_model_retry_exhaustion_confirmed: true
  selected_model: "qwen3.5:9b"
  selected_model_initially_present: false
  alternate_model_selected: false
  ollama_executable: "C:\\Users\\pablo\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
  ollama_version: "0.31.2"
  gpu_name: "NVIDIA GeForce RTX 4060 Ti"
  gpu_memory_mib: 16380
  total_physical_memory_bytes: 34163974144
  pre_pull_c_drive_free_bytes: 203980992512
  post_pull_c_drive_free_bytes: 195701702656
  storage_threshold_gib: 12
  storage_preflight_passed: true
  hardware_fit_classification: "candidate feasible for controlled evaluation"
  pull_command: "ollama pull qwen3.5:9b"
  pull_command_execution_count: 1
  download_began: true
  download_completed: true
  downloaded_primary_layer_size: "6.6 GB"
  sha256_verification_completed: true
  manifest_written: true
  pull_success: true
  exact_model_tag_local_after_pull: true
  selected_model_inventory_id: "6488c96fa5fa"
  selected_model_inventory_size: "6.6 GB"
  selected_model_architecture: "qwen35"
  selected_model_parameters: "9.7B"
  selected_model_context_length: 262144
  selected_model_embedding_length: 4096
  selected_model_quantization: "Q4_K_M"
  selected_model_minimum_ollama_version: "0.17.1"
  selected_model_capabilities:
    - "completion"
    - "vision"
    - "tools"
    - "thinking"
  qwen2_5_coder_7b_preserved: true
  nomic_embed_text_preserved: true
  model_inference_executed: false
  opencode_launched: false
  opencode_model_selected: false
  opencode_configuration_modified: false
  graphify_executed: false
  slash_skill_executed: false
  context_configuration_changed: false
  ollama_server_manually_started_or_restarted: false
  dependency_install_attempted: false
  credentials_inspected: false
  provider_config_contents_inspected: false
  normal_user_app_config_contents_inspected: false
  graphify_output_contents_inspected: false
  git_staging_performed: false
  git_mutated: false
  recommended_next_ticket: "P10.5I - Graphify OpenCode qwen3.5:9b Context and Reduced-Scope Controlled Execution"
  final_marker: "ollama_agentic_skill_model_selection_pull_record_ready"
```

## Files Inspected

The P10.5H dependency record was inspected by marker search only:

```text
0_architecture/governance/agent_platform_graphify_opencode_explicit_current_session_subagent_routing_retry_record.md
```

No credentials, provider configurations, `.env` files, token stores, normal-user application configuration contents, Graphify outputs, product paths, external source contents, artifacts, or dependency directories were inspected.

## Files Created

Ollama created local model state for:

```text
qwen3.5:9b
```

This ticket created exactly one repository governance record:

```text
0_architecture/governance/agent_platform_ollama_agentic_skill_model_selection_pull_record.md
```

## Files Modified

The authorized Ollama pull changed local Ollama model inventory only.

P10.OLLAMA-MODEL did not modify:

```text
.opencode/**
AGENTS.md
.graphifyignore
.gitignore
graphify-out/**
OpenCode configuration
normal-user application configuration
existing Ollama models
Git index or history
```

## Commands Run

Dependency marker searches were performed with repository search tooling.

Read-only hardware and storage commands:

```powershell
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

Get-CimInstance Win32_ComputerSystem |
  Select-Object TotalPhysicalMemory

Get-PSDrive -PSProvider FileSystem |
  Select-Object Name,Used,Free
```

Ollama executable and preflight commands:

```powershell
Get-Command ollama -ErrorAction SilentlyContinue
ollama --version
ollama list
```

Exact pull command, executed once:

```powershell
ollama pull qwen3.5:9b
```

Post-pull verification commands:

```powershell
ollama list
ollama show qwen3.5:9b
```

Worktree metadata command:

```powershell
git status --short
```

Explicitly not run:

```text
ollama run
ollama launch opencode
ollama serve
ollama create
ollama cp
ollama rm
ollama stop
another ollama pull
model prompt
model benchmark
OpenCode
/graphify
/graphify .
graphify extract
graphify install
graphify update
dependency installers
tests
builds
CI
MCP servers
graph database commands
git add
git commit
git push
```

## Human Approval Status

Explicit approval existed outside the ticket body for:

```text
selection of exactly qwen3.5:9b
read-only hardware and storage checks
read-only Ollama executable/version/inventory checks
at most one network-backed ollama pull qwen3.5:9b if absent
post-pull inventory and model metadata checks
one governance record
```

No approval existed for inference, OpenCode launch/model selection/configuration, Graphify execution, alternate model pulls, model deletion, dependency installation, credentials, generated-output inspection, staging, commit, or push.

## P10.5H Dependency Status

P10.5H exists and confirms these required markers:

```text
graphify_explicit_routing_instruction_not_followed
graphify_local_model_skill_routing_failure_confirmed
graphify_slash_skill_agentic_path_not_verified
graphify_same_model_retry_exhausted
```

The exhausted `qwen2.5-coder:7b` Graphify path was not retried.

## Selected Model

Exactly one model was selected:

```text
qwen3.5:9b
```

Marker:

```text
ollama_agentic_model_qwen3_5_9b_selected
```

No alternate tag, larger model, fallback model, cloud model, or comparative candidate was pulled.

## Selection Rationale

`qwen3.5:9b` is materially different from the exhausted `qwen2.5-coder:7b` route and is a risk-adjusted local candidate for future agentic/tool-oriented evaluation.

Confirmed post-pull properties relevant to that rationale:

```text
9.7B parameter class
Q4_K_M quantization
tools capability
thinking capability
262,144-token model context metadata
local Ollama availability
6.6 GB inventory size
```

Selection does not establish Graphify compatibility, OpenCode compatibility, runtime stability, performance, or 64K context stability.

## Hardware Metadata

GPU:

```text
NVIDIA GeForce RTX 4060 Ti
16380 MiB total GPU memory
```

System RAM:

```text
34163974144 bytes
approximately 31.8 GiB
```

Hardware-fit classification:

```text
candidate feasible for controlled evaluation
not production-qualified
not performance-qualified
not guaranteed to remain fully GPU-resident at a future 64K context
```

Marker:

```text
ollama_qwen3_5_9b_hardware_fit_candidate_confirmed
```

No stress test, benchmark, inference, context allocation, or offloading test was run.

## Storage Preflight

C: volume metadata before pull:

```text
used: 795209170944 bytes
free: 203980992512 bytes
approximately 190 GiB free
```

Required threshold:

```text
at least 12 GiB free
```

Result:

```text
pass
```

C: volume metadata after pull:

```text
used: 803488460800 bytes
free: 195701702656 bytes
approximately 182 GiB free
```

No files or existing models were deleted to create space.

## Ollama Executable/Version

Executable:

```text
C:\Users\pablo\AppData\Local\Programs\Ollama\ollama.exe
```

Version:

```text
0.31.2
```

Ollama was not installed, updated, started manually, restarted, or reconfigured.

## Existing Model Inventory

Pre-pull inventory:

| Model | ID | Size |
| --- | --- | --- |
| `qwen2.5-coder:7b` | `dae161e27b0e` | 4.7 GB |
| `nomic-embed-text:latest` | `0a109f422b47` | 274 MB |

Exact selected tag preflight result:

```text
qwen3.5:9b absent
```

The absence authorized proceeding with the one exact pull.

## Model Pull Status

Command:

```text
ollama pull qwen3.5:9b
```

Execution count:

```text
1
```

Observed pull result:

```text
manifest resolved
6.6 GB primary layer downloaded to 100%
supporting layers downloaded to 100%
SHA-256 digest verified
manifest written
success returned
```

Marker:

```text
ollama_qwen3_5_9b_pull_success
```

No retry, alternate tag, concurrent pull, fallback, or cleanup was performed.

## Post-Pull Model Inventory

Post-pull inventory:

| Model | ID | Size |
| --- | --- | --- |
| `qwen3.5:9b` | `6488c96fa5fa` | 6.6 GB |
| `qwen2.5-coder:7b` | `dae161e27b0e` | 4.7 GB |
| `nomic-embed-text:latest` | `0a109f422b47` | 274 MB |

Markers:

```text
ollama_qwen3_5_9b_local_inventory_verified
ollama_qwen2_5_coder_7b_preserved
```

All pre-existing models remained present.

## Selected-Model Metadata

`ollama show qwen3.5:9b` reported:

| Field | Value |
| --- | --- |
| architecture | `qwen35` |
| parameters | `9.7B` |
| context length | `262144` |
| embedding length | `4096` |
| quantization | `Q4_K_M` |
| requires | `0.17.1` |
| capability | `completion` |
| capability | `vision` |
| capability | `tools` |
| capability | `thinking` |
| license | Apache License 2.0 |

Marker:

```text
ollama_qwen3_5_9b_metadata_verified
```

This is static model metadata only. It is not proof of tool-call correctness, context allocation, agentic execution, or Graphify success.

## Existing-Model Preservation Status

Preserved:

```text
qwen2.5-coder:7b
nomic-embed-text:latest
```

No `ollama rm`, replacement, copy, or model cleanup command was run.

## Inference Status

Inference status:

```text
not executed
```

Marker:

```text
ollama_no_model_inference
```

No prompt, completion, vision request, thinking request, tool call, structured-output test, benchmark, or context-allocation test was performed.

## OpenCode Configuration Status

OpenCode was not launched through Ollama or otherwise by this ticket.

No OpenCode model was selected, exposed, registered, or configured. No OpenCode configuration content was inspected or modified.

Marker:

```text
ollama_no_opencode_config_mutation
```

## Graphify Runtime Status

Graphify runtime status:

```text
not executed
```

No Graphify CLI command or slash skill was invoked. No Graphify output was created, inspected, accepted, cleaned, or tracked.

Marker:

```text
ollama_no_graphify_runtime
```

## Outcome Classification

Final outcome:

```text
Outcome A - new model pull succeeds
```

Requirements satisfied:

```text
dependency markers present
hardware metadata compatible with candidate evaluation
storage above threshold
exact model initially absent
one exact pull completed
integrity verification completed
exact tag appears in local inventory
metadata is readable
existing models remain present
no inference occurred
```

Handoff marker:

```text
p10_5i_qwen3_5_9b_opencode_integration_ready
```

This marker means only that the selected model is locally available for a separately authorized integration/runtime gate.

## Authority Classification

The selected model is:

```text
execution substrate candidate
not authority
not approval
not source of truth
not memory authority
not architecture authority
```

This pull record is governance evidence. It is not model-runtime validation, OpenCode agentic validation, Graphify validation, structured-output validation, or performance qualification.

## Created / Not Created Register

Created:

```text
local Ollama model state for qwen3.5:9b
0_architecture/governance/agent_platform_ollama_agentic_skill_model_selection_pull_record.md
```

Not created, run, or approved:

```text
qwen3.5 inference
OpenCode session
OpenCode provider modification
opencode.jsonc modification
.opencode modification
AGENTS.md modification
Graphify execution
/graphify
/graphify .
graph.json
graph.html
GRAPH_REPORT.md
model benchmark
model comparison
context-length change
Ollama server restart
dependency installation
hosted-provider call
credential inspection
model deletion
output tracking
Git mutation
git add .
```

## Limitations

The pull and metadata verification establish only local availability.

Not validated:

```text
model inference
OpenCode model visibility
OpenCode provider exposure
tool-call correctness
subagent routing
Graphify skill instruction following
Graphify structured output
actual allocated context
64K context stability
GPU/CPU offloading
runtime VRAM/RAM pressure
latency or performance
full GPU residency
```

Although model metadata advertises a 262,144-token context length, no context setting was changed and no runtime context was allocated. A future 64K configuration remains separately gated.

## Recommended Next Ticket

Recommended next ticket:

```text
P10.5I - Graphify OpenCode qwen3.5:9b Context and Reduced-Scope Controlled Execution
```

That ticket must separately authorize and verify:

```text
64K context configuration
OpenCode model exposure or temporary launch
runtime offloading and memory metadata
one reduced-scope Graphify invocation
current-session and OpenCode-subagent routing
metadata-only output validation
```

It must not authorize `/graphify .` until the reduced-scope smoke succeeds.

## Commit Commands

No Git mutation command was run. If this record is accepted, stage only this governance record:

```powershell
git status --short

git add 0_architecture/governance/agent_platform_ollama_agentic_skill_model_selection_pull_record.md

git commit -m "Select and provision Graphify local agentic model"

git push
```

Do not stage:

```text
.opencode/**
AGENTS.md
graphify-out/**
0_architecture/implementation/graphify_command_candidate_confirmation.md
```

Do not use `git add .`.

## Final Declaration

P10.OLLAMA-MODEL selected and provisioned exactly `qwen3.5:9b` through one successful authorized pull. The exact tag is local, metadata is readable, existing models are preserved, and no inference, OpenCode configuration, Graphify runtime, credential inspection, generated-output inspection, or Git mutation occurred.

Final marker:

```text
ollama_agentic_skill_model_selection_pull_record_ready
```
