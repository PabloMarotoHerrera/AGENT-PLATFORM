# Graphify Local Runtime / CLI Discovery Authorization

## 0. Contexto obligatorio

P9 is closed as External Integration Foundation. P10.0-P10.4 are accepted. P10.1 patched `.graphifyignore`. P10.5 stopped correctly before execution because P10.3 recorded `pending_graphify_exact_command_candidate` and `P10.5_blocked_until_exact_command_is_approved`.

GRAPHIFY-HARD-01 confirmed that the exact command could not be derived from P10.0-P10.4 alone.

P9.7 authorizes a narrow, read-only, local inspection of Graphify documentation and runtime metadata under `4_external/sources/graphify` for CLI discovery only.

Result markers:

```text
graphify_local_runtime_cli_discovery_authorized
graphify_cli_command_discovered
```

Graphify remains evidence map only, not authority, not source of truth, not approval engine, not runtime, and not Cognitive Semantic System substrate.

## 1. Tipo

Governance / external-source-read-authorization / CLI-discovery.

## 2. Objetivo

Confirm the local Graphify runtime / CLI command candidate needed to unblock a future P10.3A command amendment and then a later P10.5 retry.

P9.7 determines the official executable, official CLI command candidate, working directory candidate, input scope behavior, ignore-file behavior, output root, expected output paths, runtime/package prerequisites, network/provider/API/MCP posture, install/build posture, allowed flags, forbidden flags, and P10.3/P10.5 follow-up recommendations.

P9.7 does not execute Graphify, does not run `/graphify`, does not install dependencies, does not run package managers, does not modify Graphify, does not adopt Graphify, does not create adapters, does not create `graphify-out/`, does not generate outputs, does not inspect secrets, does not inspect product/Siamese source, does not inspect generated outputs, and does not mutate Git.

## 3. Discovery scope

Allowed local inspection root:

```text
4_external/sources/graphify
```

Inspection mode:

- read-only
- documentation-only
- manifest-level
- CLI-discovery-only
- runtime-entrypoint-discovery-only

Files and metadata inspected were limited to Graphify-local allowed documentation, manifests, and launcher metadata, including `README.md`, `pyproject.toml`, `ARCHITECTURE.md`, `docs/how-it-works.md`, and allowed path metadata under `4_external/sources/graphify`.

No unrelated external source was inspected. No `4_external/sources/gstack-main`, Hermes, GBrain, ECC-main, product/Siamese, generated output, secret, credential, provider config, token store, browser auth, local credential store, API key, or root `graphify-out/` content was inspected.

## 4. Discovery result

Final decision:

```text
graphify_cli_command_discovered
```

P9.7 discovered a documented command candidate suitable for a future P10.3A amendment, not direct execution by P9.7.

P10.5 must not retry directly from P9.7. P10.5 may be retried only after P10.3A accepts the exact command, output root, provider/network posture, rollback/incident posture, and human approval wording.

## 5. Command source evidence

| Evidence | Source path | Discovery |
| --- | --- | --- |
| Console script entry point | `4_external/sources/graphify/pyproject.toml` | `[project.scripts]` declares `graphify = "graphify.__main__:main"`. |
| Package/executable name | `4_external/sources/graphify/pyproject.toml` | Project package is `graphifyy`; installed executable is `graphify`. |
| Current-folder graph command | `4_external/sources/graphify/README.md` | Common command documents `/graphify .` as build graph for current folder. |
| PowerShell invocation | `4_external/sources/graphify/README.md` | PowerShell note says use `graphify .`, not `/graphify .`, because leading slash is a path separator. |
| Minimal output flag | `4_external/sources/graphify/README.md` | `/graphify . --no-viz` is documented to skip HTML and produce report plus JSON. |
| Ignore behavior | `4_external/sources/graphify/README.md` | `.gitignore` is respected automatically; `.graphifyignore` is merged and evaluated last. |
| Output root | `4_external/sources/graphify/README.md` and `ARCHITECTURE.md` | Default output root is `graphify-out/`; expected primary files include `GRAPH_REPORT.md` and `graph.json`. |
| Runtime/provider posture | `4_external/sources/graphify/README.md` | Code-only extraction is local; docs/markdown semantic extraction may require assistant/model/backend path or configured provider/local backend. |

## 6. Official command candidate

`GraphifyCommandCandidate`:

```yaml
GraphifyCommandCandidate:
  official_executable: graphify
  package_name: graphifyy
  entrypoint_source: 4_external/sources/graphify/pyproject.toml
  entrypoint: graphify.__main__:main
  command_candidate_for_P10_3A: graphify . --no-viz
  command_source:
    - 4_external/sources/graphify/README.md
    - 4_external/sources/graphify/pyproject.toml
  status: graphify_cli_command_discovered
  execution_authorized_by_P9_7: false
```

The future command candidate is:

```text
graphify . --no-viz
```

Rationale:

- `graphify` is the documented console script.
- `.` targets the current working directory.
- `--no-viz` is documented to skip HTML visualization and keep output limited to report plus JSON.
- The no-slash form is required for PowerShell / Windows shell posture.

This command candidate is not execution approval. It must be accepted by P10.3A before P10.5 can retry.

## 7. Working directory candidate

`GraphifyWorkingDirectory`:

```yaml
GraphifyWorkingDirectory:
  candidate: repository_root
  reason: command uses current directory target "."
  forbidden_working_directories:
    - 4_external/sources/**
    - external/sources/**
    - 4_external/sources/gstack-main/**
    - 9_artifacts/**
    - graphify-out/**
    - 2_products/**
    - product/**
    - products/**
  execution_authorized_by_P9_7: false
```

## 8. Input scope behavior

The command candidate targets `.` and relies on repository ignore rules plus the P10.1 `.graphifyignore` patch to constrain the effective input scope.

Required P10 input scope remains:

- `README.md`
- `0_architecture/**/*.md`
- `3_platform/_governed_skeleton/**/*.py`

No direct Graphify flag was discovered that precisely enumerates those three scopes in one command without relying on `.graphifyignore`.

P10.3A must therefore state that the exact command is valid only if the accepted P10.1 `.graphifyignore` remains present and effective.

## 9. Ignore-file behavior

Graphify documentation states that `.gitignore` is respected automatically and `.graphifyignore` is merged with `.gitignore`, evaluated last, and supports gitignore-style negation.

P10.1 already patched `.graphifyignore` with the approved P10 scope and blockers. P9.7 did not modify `.graphifyignore`.

P10.3A and P10.5 must stop if `.graphifyignore` no longer blocks:

- `.env`, secrets, credentials, provider/auth/token material
- `4_external/sources/**`
- `external/sources/**`
- `4_external/sources/gstack-main/**`
- `9_artifacts/**`
- `graphify-out/**` as input
- `2_products/**`, `product/**`, `products/**`

## 10. Output root candidate

`GraphifyOutputRoot`:

```yaml
GraphifyOutputRoot:
  candidate: graphify-out/
  source:
    - 4_external/sources/graphify/README.md
    - 4_external/sources/graphify/ARCHITECTURE.md
  status: discovered_candidate
  execution_authorized_by_P9_7: false
```

P9.7 did not create `graphify-out/` and did not inspect `graphify-out/`.

## 11. Expected output paths

Expected output path metadata from documentation:

- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/graph.json`
- `graphify-out/cache/**` may be produced as generated cache material
- `graphify-out/cost.json` may be local-only generated metadata

With `--no-viz`, HTML visualization output is expected to be skipped according to the README command comment.

All outputs remain generated evidence only, not authority, not source of truth, not imported, not tracked by default, and not promoted.

## 12. Runtime / package prerequisites

Runtime/package posture:

- `graphify` executable must already be available on `PATH` or otherwise available through an already installed Graphify environment.
- Documentation recommends `uv tool install graphifyy` or `pipx install graphifyy` when `graphify` is missing.
- P9.7 does not install anything.
- P10.5 must not install anything.
- If `graphify` is not available when P10.5 executes, P10.5 must fail safe rather than installing dependencies.

Can the command be run without installation? Only if `graphify` is already installed or otherwise available. P9.7 did not verify runtime availability by executing `graphify --version` because that would be Graphify execution.

## 13. Network / provider / API / MCP posture

Documentation indicates:

- Code-only extraction is local and requires no API key.
- Markdown/docs/PDF/images semantic extraction may use the assistant/model/backend path.
- Headless extraction may require a backend/API key, local Ollama, Bedrock credentials, Claude CLI, or another configured backend.
- MCP serving/query commands exist but are not part of the command candidate.

Because P10 scope includes markdown, P10.3A must explicitly resolve provider/network/backend posture before P10.5 execution. Under current P10.5 constraints, any requirement for provider/API/MCP, external network, credentials, package managers, or installation remains a stop condition.

## 14. Install / build requirement

P9.7 did not find evidence that `graphify . --no-viz` itself requires a build step if the `graphify` CLI is already installed.

Installation may be required if the CLI is absent. Installation is not authorized by P9.7 or P10.5.

No build, package manager, Python, node, npm, pnpm, yarn, pip, poetry, cargo, make, cmake, docker, tests, or scripts were executed.

## 15. Allowed flags

Allowed flag candidate for P10.3A:

- `--no-viz`

Reason: documented to skip HTML visualization and keep output to report plus JSON.

No other flags are approved by P9.7.

## 16. Forbidden flags and behaviors

Forbidden flags and behaviors include:

- `--watch`
- `--mcp`
- `--neo4j`
- `--neo4j-push`
- `--falkordb`
- `--falkordb-push`
- `--google-workspace`
- `--backend` unless a future exact gate approves provider/local backend posture
- `--dedup-llm`
- `--global`
- `--force` unless future exact gate approves overwrite posture
- install/uninstall/hook/platform commands
- any command that reads blocked paths
- any command that writes outside `graphify-out/`
- any command that imports or tracks generated output
- any command that activates provider/API/MCP
- any command that uses credentials
- any command that mutates Git

## 17. P10.3 update recommendation

P10.3 should be updated or superseded by:

```text
P10.3A - Graphify Controlled Rerun Plan Command Amendment
```

P10.3A should accept or reject this exact command candidate:

```text
graphify . --no-viz
```

P10.3A must also resolve:

- whether the command is acceptable when it relies on `.graphifyignore` for scope restriction
- whether markdown semantic extraction requires provider/API/network/credentials
- whether P10.5 is allowed to fail safe if `graphify` is not on `PATH`
- whether `graphify-out/` is the exact approved output root
- whether expected output paths are limited to generated evidence metadata
- whether `--no-viz` is the only allowed flag

## 18. P10.5 retry recommendation

P10.5 should not be retried directly from P9.7.

P10.5 may be retried only after:

- P10.3A accepts the exact command candidate
- P10.3A resolves provider/network/backend posture
- P10.3A confirms output root and expected output path metadata
- P10.1-P10.4 remain accepted
- `.graphifyignore` remains unchanged from the approved P10.1 posture
- explicit human approval is present

## 19. Created / Not Created Register

Created:

- `0_architecture/governance/agent_platform_graphify_local_runtime_cli_discovery_authorization.md`

Not created / not approved:

- No Graphify execution
- No `/graphify` execution
- No Codegraph execution
- No package installation
- No package manager execution
- No build
- No tests
- No `graphify-out/`
- No generated outputs
- No Graphify output import
- No generated output tracking
- No source tracking expansion
- No runtime activation
- No adapter creation
- No provider/API/MCP
- No network call
- No product/Siamese inspection
- No secret/credential inspection
- No Git mutation
- No git add .

## 20. Final decision

| Question | Answer |
| --- | --- |
| Was local Graphify path present? | Yes, `4_external/sources/graphify`. |
| What inspection was authorized? | Read-only docs/manifest/launcher metadata for CLI discovery only. |
| Was command discovered? | Yes, `graphify_cli_command_discovered`. |
| Official executable? | `graphify`. |
| Package name? | `graphifyy`. |
| Entry point? | `graphify.__main__:main`. |
| Exact command candidate for P10.3A? | `graphify . --no-viz`. |
| Working directory candidate? | Repository root. |
| Input scope behavior? | Target `.` and rely on approved P10.1 `.graphifyignore` plus `.gitignore` behavior. |
| Output root candidate? | `graphify-out/`. |
| Expected output paths? | `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`, and local generated cache/metadata under `graphify-out/**`. |
| Runtime prerequisite? | `graphify` executable must already be available; no install authorized. |
| Network/provider/API/MCP posture? | Must be resolved by P10.3A because markdown/docs may require model/backend path. |
| Can P10.3 be updated or superseded? | Yes, recommended P10.3A. |
| Can P10.5 be retried now? | No, only after P10.3A and human approval. |
| Did P9.7 execute Graphify? | No. |
| Did P9.7 inspect unrelated external sources? | No. |
| Did P9.7 inspect product/Siamese source? | No. |
| Did P9.7 inspect generated outputs? | No generated output content was inspected. |
| Did P9.7 mutate Git? | No. |

Recommended next ticket:

```text
P10.3A - Graphify Controlled Rerun Plan Command Amendment
```
