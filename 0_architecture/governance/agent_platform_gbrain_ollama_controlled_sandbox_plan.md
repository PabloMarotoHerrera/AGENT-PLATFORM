# GBrain Ollama Controlled Sandbox Plan

## Document Header

| Field | Value |
| --- | --- |
| Title | GBrain Ollama Controlled Sandbox Plan |
| Ticket | P12.0C |
| Status | Plan-only sandbox design ready; runtime execution blocked until command discovery and explicit approval |
| Date | 2026-07-09 |
| Scope | Define a future controlled local sandbox for GBrain and optional Ollama evaluation without executing GBrain, Ollama, Graphify, package managers, tests, builds, providers, embeddings, databases, graph stores, or generated output inspection. |
| Authority | Governance plan only; not runtime execution, provider activation, credential inspection, package installation, dependency resolution, embedding generation, database creation, graph/vector store creation, generated output import, frontend reuse, runtime integration, authority promotion, source-of-truth promotion, Git mutation, or Cognitive Semantic System substrate selection. |
| Target file | `0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md` |

Final declaration: `gbrain_ollama_controlled_sandbox_plan_ready`.

Supporting markers:

```text
gbrain_ollama_sandbox_plan_blocked_command_unknown
gbrain_mode_a_keyword_only_sandbox_preferred
gbrain_mode_b_ollama_embedding_sandbox_gated
gbrain_runtime_command_discovery_required
gbrain_sandbox_outputs_generated_local_only_review_required
```

## Summary

P12.0C defines the next safe sandbox shape after P12.0A and P12.0B. It does not authorize execution. The immediate next gate is command discovery because `gbrain` and `ollama` were not discoverable on `PATH` from the current shell during prior metadata checks.

The preferred future path is Mode A: initialize a disposable GBrain sandbox with no embeddings, force keyword-only search behavior, import only a small governed fixture, and inspect deterministic search/graph/export behavior. Mode B remains separate and optional: local Ollama embeddings only after command discovery, model inventory, model dimensions, and local-only provider configuration are explicitly approved.

```yaml
P12_0C_Decision:
  plan_only: true
  p12_0d_runtime_execution_authorized_now: false
  gbrain_command_discoverable_from_current_shell: false
  ollama_command_discoverable_from_current_shell: false
  local_ollama_port_observed_reachable_previously: true
  local_ollama_port_proves_model_inventory: false
  preferred_future_mode: "Mode A keyword-only no-embedding sandbox"
  mode_b_ollama_embeddings_authorized_now: false
  graphify_runtime_retry_authorized_now: false
  sandbox_outputs_trackable_by_default: false
  cognitive_semantic_system_substrate_selected: false
  final_marker: "gbrain_ollama_controlled_sandbox_plan_ready"
```

## Prior Authority

P12.0A declared `gbrain_partially_replaces_graphify_semantic_layer` and kept Graphify as a visualization/report/export candidate, not an approved runtime or authority source.

P12.0B declared `gbrain_ollama_local_provider_graph_generation_feasibility_review_ready`, found GBrain plus Ollama feasible at source-review level for a future local/no-paid-API sandbox, and kept graph generation as a candidate requiring runtime validation.

The local `.graphifyignore` remains controlling scope evidence. It states that Graphify is an evidence map only and not authority, source of truth, approval engine, runtime, or Cognitive Semantic System substrate. It also blocks sensitive, generated, external, artifact, and product scopes including `.env*`, credentials, provider configs, `4_external/sources/**`, `9_artifacts/**`, `graphify-out/**`, and product paths.

## Planning Inputs

Only metadata and source-review observations feed this plan.

| Input | Observed Result | P12.0C Use |
| --- | --- | --- |
| P12.0A governance file | Present in prior checks | Establishes GBrain as partial semantic-layer candidate and Graphify retry as still gated. |
| P12.0B governance file | Present in prior checks | Establishes Ollama/local provider feasibility candidate and graph-generation candidate posture. |
| `4_external/sources/gbrain-master` | Present in prior checks | Source-review root for command and provider planning. |
| `.graphifyignore` | Present in prior checks | Scope and sensitive-path boundary. |
| `Get-Command gbrain -ErrorAction SilentlyContinue` | No output in prior checks | Blocks runtime execution handoff until command path is resolved. |
| `Get-Command ollama -ErrorAction SilentlyContinue` | No output in prior checks | Blocks model inventory/inference assumptions. |
| `Test-NetConnection 127.0.0.1 -Port 11434` | `TcpTestSucceeded : True` in prior checks | Compatible with an Ollama-style listener, but not proof of Ollama, models, dimensions, or inference readiness. |
| Existing untracked implementation file | `?? 0_architecture/implementation/graphify_command_candidate_confirmation.md` in prior status | Must not be modified or staged by this plan unless separately authorized. |

No GBrain, Graphify, `/graphify`, Ollama list/show/run/pull/serve/ps, package-manager command, test, build, CI, provider API, embedding generation, vector DB creation, graph DB creation, generated output inspection, credential inspection, or Git mutation was performed for this plan.

## Command Classification Legend

`confirmed_from_manifest` means the command entry point or package surface is declared in the package manifest, but the runtime was not executed.

`confirmed_from_docs` means first-party documentation describes the command or flag, but P12.0C did not execute it.

`confirmed_from_source_interface` means first-party source code routes or parses the command or flag, but P12.0C did not execute it.

`candidate_unconfirmed` means the command shape is plausible for a future gate but not validated enough to rely on.

`blocked_unknown` means the command cannot be used as a P12.0D execution dependency yet because local discoverability, exact path, model inventory, or runtime behavior is unknown.

## Source Interface Evidence

`package.json` declares a `gbrain` binary mapped to `src/cli.ts`, so the CLI entry point is `confirmed_from_manifest` at source-review level.

`README.md`, `INSTALL_FOR_AGENTS.md`, and GBrain operation docs describe `gbrain init --pglite`, `gbrain import`, `gbrain query`, `gbrain search`, `gbrain config set`, and graph traversal usage. These are `confirmed_from_docs` at planning level.

`src/cli.ts` routes CLI-only commands and shared operations, including `init`, `import`, `sync`, `sources`, `search`, `query`, `graph-query`, `export`, `code-def`, `code-refs`, `code-callers`, `code-callees`, and `config`. These are `confirmed_from_source_interface` at planning level.

`src/commands/init.ts` confirms `--pglite`, `--path`, `--no-embedding`, `--embedding-model`, and `--embedding-dimensions` surfaces. P12.0C did not run them.

`src/commands/import.ts` confirms `gbrain import <dir>` and `--no-embed`. P12.0C did not run them.

`src/commands/sources.ts` confirms source registration with `sources add <id> --path <path>`. P12.0C did not run it.

`src/commands/graph-query.ts` confirms `graph-query <slug> [--type T] [--depth N] [--direction in|out|both]`. P12.0C did not run it.

`src/commands/export.ts` confirms export behavior to a target directory. P12.0C did not run it and did not inspect generated output.

`src/core/config.ts` confirms `GBRAIN_HOME` is honored as an absolute parent directory and `gbrainPath(...)` resolves beneath it. This supports a future sandbox-only home boundary.

`src/core/config.ts` also declares the `search.` prefix as a known config namespace for `gbrain config set`, and `src/core/operations.ts` reads `search.mcp_keyword_only` to route `search` to keyword-only retrieval when set to `true`.

`src/core/ai/recipes/ollama.ts` confirms the Ollama provider recipe is local/OpenAI-compatible with default base URL `http://localhost:11434/v1`, no required auth env, supported embedding model names, default dimensions of 768, and zero listed cost. P12.0C did not contact this endpoint or validate model availability.

## Future Sandbox Root

Future root candidate only:

```text
9_artifacts/gbrain_sandbox/p12_0d/
```

This path must not be created by P12.0C. It may be created only by a later approved execution gate.

Future planned subdirectories:

```text
9_artifacts/gbrain_sandbox/p12_0d/input_fixture/
9_artifacts/gbrain_sandbox/p12_0d/gbrain_home/
9_artifacts/gbrain_sandbox/p12_0d/db/
9_artifacts/gbrain_sandbox/p12_0d/exports/
9_artifacts/gbrain_sandbox/p12_0d/logs/
9_artifacts/gbrain_sandbox/p12_0d/reports/
```

The future `GBRAIN_HOME` value must point only to the sandbox home candidate, not to the user's normal home, not to any existing `.gbrain`, and not to a shared project config location.

## Future Fixture

Fixture input must be copied into the sandbox root only after future approval. It must remain small, governed, non-sensitive, and reviewable.

Primary fixture candidates:

```text
README.md
0_architecture/governance/agent_platform_gbrain_source_review_authorization_graphify_replacement_feasibility.md
0_architecture/governance/agent_platform_gbrain_ollama_local_provider_graph_generation_feasibility_review.md
3_platform/_governed_skeleton/agent_platform_mvp0/contracts.py
```

Fallback fixture candidate:

```text
one existing 3_platform/_governed_skeleton/agent_platform_mvp0/**/*.py file
```

Fixture exclusions:

```text
.env*
credentials/**
secrets/**
tokens/**
provider configs
4_external/sources/**
9_artifacts/** other than the approved sandbox root
graphify-out/**
2_products/**
product/**
products/**
```

## Mode A: No-Embedding Keyword Sandbox

Mode A is the preferred first runtime sandbox because it avoids embeddings, paid APIs, model inventory assumptions, and Ollama dependency. It is still blocked until command discovery and explicit approval.

Mode A goal:

```text
Validate whether GBrain can initialize in an isolated local PGLite path, ingest a tiny governed fixture without embeddings, perform keyword-only search, expose deterministic graph traversal where available, and export reviewable local-only evidence artifacts.
```

Mode A future command matrix:

| Step | Future Command Candidate | Classification | P12.0C Decision |
| --- | --- | --- | --- |
| Discover GBrain executable | `Get-Command gbrain -ErrorAction SilentlyContinue` | `blocked_unknown` | Required before any runtime handoff. |
| Set sandbox home | `$env:GBRAIN_HOME = "<absolute path to 9_artifacts/gbrain_sandbox/p12_0d/gbrain_home>"` | `candidate_unconfirmed` | Future shell-scoped boundary only; do not persist globally. |
| Initialize no-embedding PGLite | `gbrain init --pglite --path "9_artifacts/gbrain_sandbox/p12_0d/db" --no-embedding` | `confirmed_from_docs`, `confirmed_from_source_interface`, runtime still `blocked_unknown` | Preferred init candidate after command discovery. |
| Force keyword-only search | `gbrain config set search.mcp_keyword_only true` | `confirmed_from_docs`, `confirmed_from_source_interface`, runtime still `blocked_unknown` | Required before `gbrain search` so search does not default to cheap-hybrid embeddings. |
| Register fixture source | `gbrain sources add p12_0d_fixture --path "9_artifacts/gbrain_sandbox/p12_0d/input_fixture"` | `confirmed_from_source_interface`, runtime still `blocked_unknown` | Candidate if source registration is needed for scoping. |
| Import fixture without embeddings | `gbrain import "9_artifacts/gbrain_sandbox/p12_0d/input_fixture" --no-embed` | `confirmed_from_docs`, `confirmed_from_source_interface`, runtime still `blocked_unknown` | Candidate import path; must not read outside fixture. |
| Keyword retrieval smoke | `gbrain search "controlled sandbox graph evidence"` | `confirmed_from_docs`, `confirmed_from_source_interface`, runtime still `blocked_unknown` | Candidate only after keyword-only config is set. |
| Graph traversal smoke | `gbrain graph-query <fixture-slug> --depth 2 --direction both` | `confirmed_from_docs`, `confirmed_from_source_interface`, runtime still `blocked_unknown` | Candidate only after imported slug is known from sandbox output. |
| Export local evidence | `gbrain export --dir "9_artifacts/gbrain_sandbox/p12_0d/exports"` | `confirmed_from_source_interface`, runtime still `blocked_unknown` | Candidate export path; generated output remains local-only review evidence. |

Mode A expected allowed outputs if future-approved:

```text
disposable PGLite/cache files under the sandbox root
logs under the sandbox root
exports under the sandbox root
reports under the sandbox root
plain-text command transcript copied into a sandbox report
```

Mode A forbidden outputs:

```text
tracked generated outputs by default
Graphify outputs
product-derived outputs
credential snapshots
provider configuration snapshots
global user GBrain state
normal user home `.gbrain` state
```

## Mode B: Optional Ollama Embedding Sandbox

Mode B is not approved by P12.0C. It requires a separate explicit approval after Mode A or command discovery, because it can create embeddings and contacts a local model service.

Mode B goal:

```text
Validate whether GBrain can use a local Ollama embedding model in the same disposable sandbox without paid APIs, credentials, model pulls, or non-local provider fallback.
```

Mode B future command matrix:

| Step | Future Command Candidate | Classification | P12.0C Decision |
| --- | --- | --- | --- |
| Discover Ollama executable | `Get-Command ollama -ErrorAction SilentlyContinue` | `blocked_unknown` | Required before any Ollama command. |
| Confirm local model inventory | `ollama list` | `blocked_unknown` | Not authorized by P12.0C; candidate only for a later explicit gate. |
| Confirm selected model metadata | `ollama show <model>` | `blocked_unknown` | Not authorized by P12.0C; needed before assuming dimensions. |
| Pull missing model | `ollama pull <model>` | `blocked_unknown` | Not authorized by P12.0C; network and disk side effects require separate approval. |
| Initialize local embedding GBrain | `gbrain init --pglite --path "9_artifacts/gbrain_sandbox/p12_0d/db" --embedding-model ollama:<model> --embedding-dimensions <N>` | `confirmed_from_docs`, `confirmed_from_source_interface`, runtime still `blocked_unknown` | Candidate only after model and dimensions are approved. |
| Import with local embeddings | `gbrain import "9_artifacts/gbrain_sandbox/p12_0d/input_fixture"` | `confirmed_from_docs`, `confirmed_from_source_interface`, runtime still `blocked_unknown` | Candidate only after local-only provider behavior is proven. |
| Query without expansion | `gbrain query "controlled sandbox graph evidence" --no-expand` | `confirmed_from_docs`, parser support `confirmed_from_source_interface`, runtime still `blocked_unknown` | Candidate to avoid LLM expansion path; provider behavior still requires review. |

Mode B local-only provider requirements:

```text
no paid API key
no credential inspection
no provider config inspection
no hosted provider fallback
no model pull unless separately approved
no assumption that port 11434 equals usable Ollama inventory
explicit model name
explicit embedding dimensions
recorded evidence that base URL is local-only
recorded evidence that generated embeddings remain inside sandbox storage
```

## Graph Boundaries

GBrain is a candidate evidence/runtime sandbox only. It is not authority, source of truth, approval engine, runtime control plane, or Cognitive Semantic System substrate.

Ollama is a local provider candidate only. It is not authority, and local port reachability does not prove model availability, model quality, embedding compatibility, or inference readiness.

Graphify remains a visualization/report/export candidate. P12.0C does not unblock Graphify runtime retry, frontend reuse, generated-output import, or Graphify output tracking.

Generated sandbox outputs must be classified as:

```text
generated_local_only_sandbox_output
raw_sandbox_evidence
review_required
not_trackable_by_default
```

Any future relation or graph row must carry evidence references, source paths, confidence/review status, and staleness markers before it can be used beyond sandbox analysis.

## Storage Boundaries

Future GBrain home must be shell-scoped to the sandbox path only.

Future database path must be under `9_artifacts/gbrain_sandbox/p12_0d/db/` only.

Future exports, logs, and reports must be under `9_artifacts/gbrain_sandbox/p12_0d/` only.

Future command transcripts must redact nothing by reading credentials in the first place; the sandbox should avoid commands that print secrets, env vars, tokens, provider configs, or global paths.

The future sandbox must not write to or inspect:

```text
normal user home `.gbrain`
global GBrain config
existing project runtime databases
graphify-out/**
9_artifacts/** outside the approved sandbox root
2_products/**
product/**
products/**
credentials, secrets, tokens, or provider configs
```

## Stop Conditions

Stop immediately in any future gate if one of these occurs:

```text
`gbrain` command remains undiscoverable
`ollama` command is required but remains undiscoverable
GBrain attempts to use a hosted provider
GBrain asks for credentials or provider login
GBrain writes outside the sandbox root
Ollama requires model pull without prior approval
any command would inspect `.env`, credentials, secrets, tokens, or provider configs
any command would inspect product/Siamese paths
any command would inspect `graphify-out/**`
any command would run Graphify or `/graphify`
any command would run package managers, tests, builds, CI, Python, or Node outside a separately approved command-discovery gate
any output would be tracked by Git without explicit review
```

## Rollback Plan

P12.0C creates no runtime state, so no runtime rollback is needed now.

If a future approved sandbox creates state, rollback should be explicit and limited:

```text
stop only sandbox-started processes, if any
clear only the shell-scoped GBRAIN_HOME variable
delete only `9_artifacts/gbrain_sandbox/p12_0d/` after review approval
do not delete normal user GBrain state
do not delete Graphify outputs
do not delete product files
do not use `git reset --hard`
do not use `git checkout --`
do not stage generated outputs by default
```

Future cleanup command candidates are not authorized by P12.0C and must be reviewed before use.

## Human Approval Wording

Minimum approval for command discovery only:

```text
I approve P12.CMD command discovery only for GBrain/Ollama path resolution. Do not initialize GBrain, run Ollama model commands, create sandbox directories, generate embeddings, inspect credentials, inspect product/Siamese paths, run Graphify, install packages, run tests/builds/CI, or mutate Git.
```

Minimum approval for Mode A:

```text
I approve P12.0D Mode A only: create `9_artifacts/gbrain_sandbox/p12_0d/`, copy only the named fixture files into `input_fixture/`, set sandbox-only `GBRAIN_HOME`, initialize GBrain PGLite with `--no-embedding`, set `search.mcp_keyword_only true`, run the approved import/search/graph-query/export command candidates, and record outputs as local generated untracked review-required evidence. I do not authorize Ollama model commands, embeddings, model pulls, package installation, credential inspection, product/Siamese inspection, Graphify execution, generated-output tracking, or Git mutation.
```

Minimum approval for Mode B:

```text
I approve P12.0D Mode B local Ollama embeddings only after Mode A or command discovery: use only the named local Ollama model and explicit dimensions, keep all GBrain home/database/exports under `9_artifacts/gbrain_sandbox/p12_0d/`, prohibit hosted provider fallback and paid APIs, prohibit model pulls unless separately approved, and keep all outputs untracked review-required sandbox evidence.
```

## P12.0D Handoff

P12.0D is not ready for execution from P12.0C alone because the GBrain command path is unknown.

Recommended next gate:

```text
P12.CMD - GBrain Runtime Command Discovery
```

P12.CMD should resolve only:

```text
where `gbrain` is callable from
whether a safe version/help command can be used without initializing runtime state
whether `ollama` is callable if Mode B is later desired
whether command discovery itself creates any files
```

P12.CMD should not run:

```text
gbrain init
gbrain import
gbrain search
gbrain query
gbrain graph-query
gbrain export
ollama list/show/run/pull/serve/ps
Graphify
package managers
tests/builds/CI
credential or environment dumps
```

P12.0D can be proposed only after P12.CMD or equivalent explicit user approval resolves the `gbrain` runtime command path.

## Commit Commands

If this governance record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
git commit -m "Add GBrain Ollama controlled sandbox plan"
```

If `0_architecture/implementation/graphify_command_candidate_confirmation.md` should also be committed, stage it explicitly in a separate decision or include it explicitly after review. This P12.0C document does not authorize staging unrelated untracked files.

## Verification Plan

Allowed verification after creating this file:

```powershell
rg "gbrain_ollama_controlled_sandbox_plan_ready|gbrain_ollama_sandbox_plan_blocked_command_unknown|gbrain_mode_a_keyword_only_sandbox_preferred|gbrain_mode_b_ollama_embedding_sandbox_gated|gbrain_runtime_command_discovery_required|gbrain_sandbox_outputs_generated_local_only_review_required" 0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
git status --short
```

No runtime verification is authorized by P12.0C.

## Final Decision Record

```yaml
GBrainOllamaControlledSandboxPlan:
  ticket: P12.0C
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md"
  plan_ready: true
  gbrain_executed: false
  graphify_executed: false
  ollama_executed: false
  package_install_performed: false
  tests_or_builds_run: false
  credentials_inspected: false
  provider_config_inspected: false
  product_source_inspected: false
  generated_output_inspected: false
  database_created: false
  embeddings_generated: false
  sandbox_root_created: false
  p12_0d_execution_authorized: false
  p12_cmd_required_first: true
  preferred_future_mode: "Mode A keyword-only no-embedding sandbox"
  mode_b_authorized: false
  final_marker: "gbrain_ollama_controlled_sandbox_plan_ready"
```

Final marker:

```text
gbrain_ollama_controlled_sandbox_plan_ready
```

gbrain_ollama_controlled_sandbox_plan_ready
