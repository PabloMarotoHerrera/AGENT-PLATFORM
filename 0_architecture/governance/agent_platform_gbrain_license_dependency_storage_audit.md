# GBrain License Dependency Storage Audit

## Summary

P12.1 audited the local GBrain source repository at `4_external/sources/gbrain-master` before any install, setup, build, or runtime sandbox.

The root license posture is acceptable for controlled setup planning: the repository has a root `LICENSE` file containing the MIT License and `package.json` declares `"license": "MIT"`.

The dependency posture requires hardening before any setup/install: the repo is Bun + TypeScript based, has a Bun lockfile, includes provider/network/database/native/WASM-capable direct dependencies, lacks local transitive license metadata in `bun.lock`, and has package lifecycle/build scripts with material side effects. The `postinstall` script is blocked by default because it can invoke `gbrain apply-migrations --yes --non-interactive` if a `gbrain` command is discoverable.

The storage posture is acceptable only with an explicit sandbox boundary. Most core config/audit paths can be constrained with `GBRAIN_HOME`, and PGLite database path can be constrained with `--path`, but runtime commands can write config, `.gitignore`, databases, audit JSONL, logs, exports, generated fixtures, and provider/vector state. One reviewed autopilot error-log path writes to `$HOME/.gbrain/autopilot.log`, so daemon/autopilot paths must remain outside any minimal P12.SETUP/P12.0D plan unless separately gated.

P12.1 did not execute GBrain, Bun, Node, npm, package managers, scripts, tests, builds, providers, Ollama, migrations, databases, embeddings, or Git mutation.

Decision markers:

```text
gbrain_license_posture_acceptable_for_controlled_setup
gbrain_dependency_posture_requires_hardening
gbrain_postinstall_lifecycle_risk_requires_setup_gate
gbrain_storage_posture_acceptable_with_sandbox_boundary
gbrain_setup_can_proceed_to_controlled_plan
gbrain_runtime_remains_blocked
```

Final marker:

```text
gbrain_license_dependency_storage_audit_ready
```

## Files Inspected

Governance and scope files inspected:

```text
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
.graphifyignore
```

GBrain source files inspected read-only:

```text
4_external/sources/gbrain-master/LICENSE
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
4_external/sources/gbrain-master/SECURITY.md
4_external/sources/gbrain-master/tsconfig.json
4_external/sources/gbrain-master/README.md
4_external/sources/gbrain-master/INSTALL_FOR_AGENTS.md
4_external/sources/gbrain-master/docs/INSTALL.md
4_external/sources/gbrain-master/docs/architecture/system-of-record.md
4_external/sources/gbrain-master/docs/architecture/topologies.md
4_external/sources/gbrain-master/docs/integrations/embedding-providers.md
4_external/sources/gbrain-master/src/cli.ts
4_external/sources/gbrain-master/src/commands/init.ts
4_external/sources/gbrain-master/src/commands/import.ts
4_external/sources/gbrain-master/src/commands/export.ts
4_external/sources/gbrain-master/src/commands/autopilot.ts
4_external/sources/gbrain-master/src/core/config.ts
4_external/sources/gbrain-master/src/core/self-upgrade.ts
4_external/sources/gbrain-master/src/core/audit-week-file.ts
4_external/sources/gbrain-master/src/core/audit/audit-writer.ts
4_external/sources/gbrain-master/src/core/ai/build-gateway-config.ts
4_external/sources/gbrain-master/src/core/ai/gateway.ts
4_external/sources/gbrain-master/src/core/ai/recipes/index.ts
4_external/sources/gbrain-master/src/core/ai/recipes/ollama.ts
4_external/sources/gbrain-master/src/core/ai/recipes/llama-server.ts
4_external/sources/gbrain-master/src/core/ai/recipes/litellm-proxy.ts
4_external/sources/gbrain-master/scripts/build-admin-embedded.ts
4_external/sources/gbrain-master/scripts/build-llms.ts
4_external/sources/gbrain-master/scripts/build-pglite-snapshot.ts
4_external/sources/gbrain-master/scripts/build-schema.sh
4_external/sources/gbrain-master/admin/package.json
4_external/sources/gbrain-master/admin/bun.lock
```

Files searched or presence-checked only:

```text
4_external/sources/gbrain-master/LICENSE.md
4_external/sources/gbrain-master/NOTICE*
4_external/sources/gbrain-master/COPYING*
```

No credentials, `.env`, provider configs, `node_modules`, global package caches, user home GBrain state, generated outputs, product paths, Graphify outputs, or external source roots outside `4_external/sources/gbrain-master/**` were inspected.

## Files Created

```text
0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
```

## Files Modified

No existing file was modified. The only file change is the new P12.1 audit document.

## Commands Run

Allowed presence-only commands run:

```powershell
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master"
Test-Path -LiteralPath "4_external/sources/gbrain-master/LICENSE"
Test-Path -LiteralPath "4_external/sources/gbrain-master/LICENSE.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/bun.lock"
Test-Path -LiteralPath "4_external/sources/gbrain-master/src/cli.ts"
git status --short
```

Observed command results:

| Check | Result |
| --- | --- |
| P12.CMD report | `True` |
| GBrain source root | `True` |
| `LICENSE` | `True` |
| `LICENSE.md` | `False` |
| `package.json` | `True` |
| `bun.lock` | `True` |
| `src/cli.ts` | `True` |

Initial `git status --short` observed before this report existed:

```text
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

That implementation file was not inspected or modified.

Read-only file tools were also used to inspect allowed source files and search allowed source text. No forbidden runtime command was executed.

## P12.CMD Dependency Status

P12.CMD exists at:

```text
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
```

P12.CMD final marker is present in that document:

```text
gbrain_runtime_entrypoint_install_boundary_discovery_ready
```

P12.CMD found:

```yaml
source_root: "4_external/sources/gbrain-master"
gbrain_cli_on_current_path: false
package_manager_candidate: "bun"
lockfile_kind: "bun.lock"
binary_name: "gbrain"
entrypoint_file: "4_external/sources/gbrain-master/src/cli.ts"
source_runtime: "Bun TypeScript"
postinstall_risk_present: true
runtime_setup_blocked_until_p12_1: true
```

P12.1 accepts P12.CMD as the controlling dependency for this audit.

## License Audit

Root license file status:

```yaml
license_file_present: true
license_file_path: "4_external/sources/gbrain-master/LICENSE"
license_md_present: false
notice_files_present: false
copying_files_present: false
```

Root license evidence:

```text
LICENSE line 1: MIT License
LICENSE line 3: Copyright (c) 2026 Garry Tan
LICENSE lines 5-10: permission to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies.
LICENSE lines 12-13: copyright and permission notice must be included in copies or substantial portions.
LICENSE lines 15-21: software provided as-is without warranty.
package.json line 146: "license": "MIT"
```

License posture:

```yaml
license_type: "MIT"
permissive: true
copyleft: false
commercial_product_restriction_observed: false
attribution_required: true
copy_fork_wrapper_implication: "copyright and MIT permission notice must be preserved in copies/substantial portions"
license_compatibility_with_agent_platform_controlled_setup: "acceptable"
license_blocker_status: false
decision_marker: "gbrain_license_posture_acceptable_for_controlled_setup"
```

The license posture is acceptable for controlled local setup planning. This does not approve vendoring, redistribution, product integration, frontend reuse, source copying into product code, or public packaging beyond the current governance scope.

## Dependency Audit

Package manager posture:

```yaml
package_manager_candidate: "bun"
package_manager_field_present: false
engines_bun: ">=1.3.10"
root_lockfile: "bun.lock"
admin_lockfile: "admin/bun.lock"
source_runtime: "Bun TypeScript"
node_runtime_candidate_from_manifest: false
npm_package_manager_candidate_from_manifest: false
package_manager_execution_authorized: false
```

Root direct runtime dependencies from `package.json`:

| Dependency | Classification | Audit Notes |
| --- | --- | --- |
| `@ai-sdk/anthropic` | `provider_dependency`, `network_capable_dependency` | Anthropic model/provider integration. Hosted provider use remains blocked. |
| `@ai-sdk/google` | `provider_dependency`, `network_capable_dependency` | Google/Gemini provider integration. Hosted provider use remains blocked. |
| `@ai-sdk/openai` | `provider_dependency`, `network_capable_dependency` | OpenAI provider integration. Hosted provider use remains blocked. |
| `@ai-sdk/openai-compatible` | `provider_dependency`, `network_capable_dependency` | OpenAI-compatible path including local and proxy providers. Calls remain blocked until gated. |
| `@anthropic-ai/sdk` | `provider_dependency`, `network_capable_dependency` | Direct Anthropic SDK. Hosted provider use remains blocked. |
| `@aws-sdk/client-s3` | `database_storage_dependency`, `network_capable_dependency` | S3 storage/attachment capability; must not be used in local sandbox unless gated. |
| `@dqbd/tiktoken` | `native_binary_or_wasm_dependency` | Tokenizer dependency with native/WASM-style risk class. |
| `@electric-sql/pglite` | `database_storage_dependency`, `native_binary_or_wasm_dependency` | Embedded Postgres/PGLite dependency; listed in `trustedDependencies`. |
| `@jsquash/avif` | `native_binary_or_wasm_dependency` | Image codec/WASM-style dependency. |
| `@jsquash/png` | `native_binary_or_wasm_dependency` | Image codec/WASM-style dependency. |
| `@modelcontextprotocol/sdk` | `network_capable_dependency` | MCP protocol/server/client capability. |
| `ai` | `provider_dependency`, `network_capable_dependency` | AI SDK abstraction used for provider calls. |
| `chokidar` | `allowed_candidate_dependency` | File watcher; runtime side effects if watch/sync modes are used. |
| `cookie-parser` | `network_capable_dependency` | HTTP server middleware. |
| `cors` | `network_capable_dependency` | HTTP server middleware. |
| `eventsource-parser` | `network_capable_dependency` | SSE/EventSource parsing. |
| `exifr` | `allowed_candidate_dependency` | Metadata parser; file processing risk. |
| `express` | `network_capable_dependency` | HTTP server/admin/API capability. |
| `express-rate-limit` | `network_capable_dependency` | HTTP rate limiting. |
| `gray-matter` | `allowed_candidate_dependency` | Markdown/frontmatter parsing. |
| `heic-decode` | `native_binary_or_wasm_dependency` | Image decode dependency. |
| `js-yaml` | `allowed_candidate_dependency` | YAML parsing. |
| `marked` | `allowed_candidate_dependency` | Markdown rendering/parsing. |
| `openai` | `provider_dependency`, `network_capable_dependency` | OpenAI SDK. Hosted provider use remains blocked. |
| `pgvector` | `database_storage_dependency` | Vector storage/query support. |
| `postgres` | `database_storage_dependency`, `network_capable_dependency` | Postgres client. External DB use remains blocked. |
| `tree-sitter-wasms` | `native_binary_or_wasm_dependency` | Parser WASM package. |
| `web-tree-sitter` | `native_binary_or_wasm_dependency` | Tree-sitter WASM runtime. |
| `zod` | `allowed_candidate_dependency` | Validation. |

Root dev dependencies from `package.json`:

| Dependency | Classification | Audit Notes |
| --- | --- | --- |
| `@types/bun` | `dev_only_dependency` | Bun type definitions. |
| `@types/cookie-parser` | `dev_only_dependency` | Type definitions. |
| `@types/cors` | `dev_only_dependency` | Type definitions. |
| `@types/express` | `dev_only_dependency` | Type definitions. |
| `@types/js-yaml` | `dev_only_dependency` | Type definitions. |
| `bun-types` | `dev_only_dependency` | Bun TypeScript type support. |
| `fast-check` | `test_build_dependency`, `dev_only_dependency` | Test/property testing dependency. |
| `typescript` | `test_build_dependency`, `dev_only_dependency` | Typecheck/build dependency. |

Trusted dependencies:

```yaml
trustedDependencies:
  - "@electric-sql/pglite"
```

Admin package dependency posture:

```yaml
admin_package_private: true
admin_runtime_dependencies:
  - react
  - react-dom
admin_dev_dependencies:
  - "@types/react"
  - "@types/react-dom"
  - "@vitejs/plugin-react"
  - vite
  - typescript
admin_classification: "admin_ui_dependency"
admin_build_required_for_minimal_p12_setup: false
```

Lockfile posture:

```yaml
root_bun_lock_present: true
root_bun_lock_declares_direct_deps: true
root_bun_lock_declares_trusted_dependencies: true
root_bun_lock_license_metadata_observed: false
admin_bun_lock_present: true
admin_bun_lock_license_metadata_observed: false
transitive_dependency_source_audited: false
package_manager_audit_run: false
online_license_fetch_performed: false
```

Dependency decision:

```yaml
dependency_posture: "requires_hardening"
reasons:
  - "package lifecycle scripts can run side-effectful commands"
  - "postinstall can invoke gbrain migrations if gbrain is discoverable"
  - "direct dependencies include hosted-provider SDKs and network-capable packages"
  - "direct dependencies include database/vector/native/WASM-capable packages"
  - "lockfiles do not expose local transitive license metadata"
  - "package-manager execution and dependency resolution were not performed"
decision_marker: "gbrain_dependency_posture_requires_hardening"
```

This is not a blocker to planning P12.SETUP, but P12.SETUP must explicitly address dependency/license evidence, lifecycle script posture, offline/locked install behavior, cache locations, `node_modules`, rollback, and generated-file handling.

## Lockfile / Package-Manager Audit

Root lockfile evidence:

```text
bun.lock declares lockfileVersion 1 and configVersion 1.
bun.lock workspaces root name is `gbrain`.
bun.lock lists the same direct dependencies and devDependencies as `package.json`.
bun.lock lists `trustedDependencies` containing `@electric-sql/pglite`.
```

Admin lockfile evidence:

```text
admin/bun.lock declares lockfileVersion 1 and configVersion 1.
admin/bun.lock workspace name is `gbrain-admin`.
admin/bun.lock includes React/Vite build dependencies and optional native/binary package entries such as esbuild/Rollup platform packages.
```

Package-manager risk:

```yaml
node_modules_creation_risk: true
package_manager_cache_risk: true
lockfile_mutation_risk: true
lifecycle_script_risk: true
postinstall_risk: true
global_install_risk: true
network_resolution_risk: true
supply_chain_risk_requires_setup_gate: true
```

P12.1 did not run `bun`, `bun install`, or any package-manager command.

## Lifecycle / Postinstall Audit

Lifecycle scripts reviewed from root `package.json`:

| Script | Command Text | Side Effects | Network Risk | DB Risk | Provider Risk | Generated Output Risk | Credential Risk | Future Setup Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `postinstall` | `command -v gbrain >/dev/null 2>&1 && gbrain apply-migrations --yes --non-interactive || echo ...` | Can execute GBrain migrations if `gbrain` is discoverable; otherwise prints hint. | Low direct network risk observed. | High: migration command can touch configured DB. | Low direct provider risk. | Possible migration state changes. | Could touch configured GBrain state. | Blocked by default; requires explicit P12.SETUP lifecycle decision. |
| `dev` | `bun run src/cli.ts` | Runs TypeScript CLI from source. | Depends on invoked CLI command. | Depends on invoked CLI command. | Depends on invoked CLI command. | Depends on invoked CLI command. | Depends on invoked CLI command. | Blocked until setup/runtime gate. |
| `build` | `bun build --compile --outfile bin/gbrain src/cli.ts` | Compiles standalone binary to `bin/gbrain`. | Package/runtime dependent. | None expected from command text. | None expected from command text. | Creates `bin/gbrain`. | None expected from command text. | Not needed for minimal source-runtime plan; separate build gate if selected. |
| `build:all` | `bun build --compile --target=... --outfile bin/... src/cli.ts && ...` | Compiles platform binaries. | Package/runtime dependent. | None expected from command text. | None expected from command text. | Creates platform binaries under `bin/`. | None expected from command text. | Blocked; unnecessary for local sandbox. |
| `build:admin` | `cd admin && bun run build && cd .. && bun run scripts/build-admin-embedded.ts` | Builds admin UI and embeds assets. | Admin package-manager/build dependency risk. | None expected from command text. | None expected from command text. | Creates `admin/dist` and rewrites `src/admin-embedded.ts`. | None expected from command text. | Blocked; admin UI not needed for P12.0D Mode A. |
| `build:admin-embedded` | `bun run scripts/build-admin-embedded.ts` | Reads `admin/dist`, rewrites `src/admin-embedded.ts`. | Low direct network risk observed. | None expected. | None expected. | Rewrites generated source file. | None expected. | Blocked unless build artifacts gate approves. |
| `build:schema` | `bash scripts/build-schema.sh` | Reads `src/schema.sql`, rewrites `src/core/schema-embedded.ts`. | Low direct network risk observed. | None expected from command text. | None expected. | Rewrites generated source file. | None expected. | Blocked unless build artifacts gate approves. |
| `build:llms` | `bun run scripts/build-llms.ts` | Reads docs and rewrites `llms.txt` / `llms-full.txt`. | URL text generation only; no fetch observed in script. | None expected. | None expected. | Rewrites generated docs files. | None expected. | Blocked unless generated docs gate approves. |
| `build:pglite-snapshot` | `bun run scripts/build-pglite-snapshot.ts` | Boots in-memory PGLite, runs schema/migrations, writes snapshot fixtures. | Low direct network risk observed. | High: initializes PGLite schema in memory. | None expected. | Writes `test/fixtures/pglite-snapshot.tar` and `.version`. | None expected. | Blocked; not needed for setup/sandbox. |
| `test` | `bash scripts/run-unit-parallel.sh` | Runs tests. | Unknown without execution; prohibited. | Possible test DB behavior. | Possible test provider mocks/calls. | Test artifacts possible. | Unknown. | Blocked. |
| `verify` | `bash scripts/run-verify-parallel.sh` | Runs verification scripts. | Unknown without execution; prohibited. | Unknown. | Unknown. | Possible generated outputs. | Unknown. | Blocked. |
| `typecheck` | `tsc --noEmit` | Typecheck only by command text, but still executes TypeScript tooling. | Low direct network risk expected. | None expected. | None expected. | No emit by command text. | None expected. | Blocked in P12.1; future setup may allow as a separate verification gate. |

Postinstall decision:

```yaml
postinstall_allowed_by_default: false
postinstall_requires_setup_gate: true
postinstall_suppression_or_sandboxing_required: true
decision_marker: "gbrain_postinstall_lifecycle_risk_requires_setup_gate"
```

P12.SETUP must explicitly decide whether lifecycle scripts are disabled, allowed in a sandbox, or run only after `GBRAIN_HOME` and database boundaries are proven safe.

## Storage / Database Audit

GBRAIN_HOME and config behavior:

```text
src/core/config.ts `configDir()` honors `GBRAIN_HOME` as an absolute parent directory and appends `.gbrain`.
If `GBRAIN_HOME` is absent, `configDir()` falls back to the normal user home `.gbrain`.
`saveConfig()` creates the config directory and writes `config.json` with mode `0600`.
`saveConfig()` calls `ensureGitignore()`.
`ensureGitignore()` creates `.gitignore` inside the active GBrain home containing `*` when absent or empty.
```

Database behavior:

```text
`gbrain init --pglite` uses `gbrainPath('brain.pglite')` by default.
`gbrain init --pglite --path <DIR>` can override the PGLite database path.
PGLite init creates/connects a PGLite engine and runs `initSchema()`.
Init persists `engine: pglite`, `database_path`, embedding config or `embedding_disabled`, MCP defaults, and self-upgrade config.
Docs state Postgres/Supabase is recommended for larger/shared brains and PGLite is default for small/local installs.
Docs state the database is a derived cache over markdown/frontmatter, but DB-only runtime/infrastructure state exists.
```

Embedding/vector behavior:

```text
`--no-embedding` skips embedding provider resolution and persists deferred setup.
Without `--no-embedding`, init resolves provider/dimensions and can run embedding-key validation.
`gbrain import` refuses when embedding is disabled unless `--no-embed` is passed.
Without `--no-embed`, import validates embedding credentials and can create embeddings/chunks.
The system-of-record doc describes `content_chunks` as derived from markdown and embedded by configured model.
```

Export/log/cache behavior:

```text
`gbrain export --dir <DIR>` creates directories and writes markdown plus `.raw/*.json` sidecar files.
Audit writers default to `gbrainPath('audit')` and can write JSONL audit files under active GBrain home.
Self-upgrade state is file-based under `.gbrain`, honors `GBRAIN_HOME`, and can use cache/snooze/lock state.
CLI startup can spawn detached `gbrain check-update --refresh-cache` for real commands unless skipped/off; this is runtime behavior and remains blocked.
Autopilot error logging writes to `$HOME/.gbrain/autopilot.log`, not `GBRAIN_HOME`, in the reviewed `logError()` path.
```

Storage decision:

```yaml
storage_posture: "acceptable_with_sandbox_boundary"
required_future_boundary:
  GBRAIN_HOME: "absolute path under approved sandbox root"
  pglite_database_path: "explicit path under approved sandbox root"
  exports: "explicit path under approved sandbox root"
  audit_logs: "must remain under GBRAIN_HOME or separately overridden/gated"
  autopilot: "blocked unless separately gated because reviewed error log path uses HOME"
  postinstall: "blocked unless sandboxed and lifecycle-approved"
global_state_risk: true
cleanup_requires_explicit_rollback_plan: true
decision_marker: "gbrain_storage_posture_acceptable_with_sandbox_boundary"
```

Storage is not acceptable for unrestricted setup. It is acceptable only for a future P12.SETUP/P12.0D plan that forces all intended writes under `9_artifacts/gbrain_sandbox/p12_0d/` or another explicitly approved generated-local sandbox root, and avoids daemon/autopilot/global-home paths.

## Provider / API / Ollama Audit

Provider documentation and source evidence:

```text
GBrain documents 16 embedding-provider recipes including hosted providers, local providers, and LiteLLM proxy.
Init provider resolution uses explicit flags first, then shorthand, then env detection.
`--no-embedding` skips embedding tier resolution and persists deferred setup.
Local-only providers without required auth, including Ollama and llama-server, are skipped from silent env auto-pick and require explicit `--embedding-model` selection.
OpenAI embedding/chat/expansion requires `OPENAI_API_KEY`.
Google/Gemini embedding/chat/expansion requires `GOOGLE_GENERATIVE_AI_API_KEY`.
Anthropic expansion/chat requires `ANTHROPIC_API_KEY`; Anthropic has no embedding model in the reviewed gateway path.
Ollama recipe has default base URL `http://localhost:11434/v1`, no required auth env, optional `OLLAMA_BASE_URL` and `OLLAMA_API_KEY`, model names `nomic-embed-text`, `mxbai-embed-large`, and `all-minilm`, and default dimensions 768.
llama-server recipe has default base URL `http://localhost:8080/v1`, no required auth env, and requires user-provided model/dimensions.
LiteLLM proxy can front arbitrary providers and has optional local proxy auth/base URL, so it is not automatically local-only unless the proxy boundary is separately proven.
```

Provider/API decision:

```yaml
openai_dependency_present: true
anthropic_dependency_present: true
gemini_google_dependency_present: true
ollama_dependency_source_recipe_present: true
llama_server_dependency_source_recipe_present: true
litellm_dependency_source_recipe_present: true
provider_auto_detection_present: true
hosted_provider_fallback_risk: true
credential_inspection_authorized: false
provider_call_authorized: false
ollama_call_authorized: false
local_only_provider_feasible_for_future_gate: true
required_future_provider_boundary: "Mode A no-embedding first; Mode B explicit local model/dimensions only after approval"
```

No provider/API/Ollama call was made in P12.1.

## Setup / Install Risk Decision

P12.SETUP may be planned, but it must be a controlled local install/build plan with hardening requirements. It must not directly proceed to install or runtime execution.

Decision:

```yaml
P12_1_SetupDecision:
  license_posture: "acceptable"
  dependency_posture: "requires_hardening"
  lifecycle_postinstall_risk: "requires_setup_gate"
  storage_posture: "acceptable_with_sandbox_boundary"
  setup_plan_may_be_generated: true
  setup_execution_authorized: false
  runtime_execution_authorized: false
  recommended_next_ticket: "P12.SETUP - GBrain Controlled Local Install / Build Plan"
```

Required P12.SETUP hardening items:

```text
exact package manager and version/source
whether Bun is already available or must be installed under a separate gate
offline/lockfile posture
node_modules location and cleanup
package manager cache location and cleanup
postinstall/lifecycle script posture
whether lifecycle scripts are disabled or sandboxed
whether global install/link is prohibited or allowed
expected created files
expected modified files
generated artifact prohibition
GBRAIN_HOME absolute sandbox path
PGLite DB explicit sandbox path
provider/API disabled posture
no-embedding Mode A default
rollback/delete plan
human approval text
```

## Runtime / Storage Risk Decision

Runtime remains blocked.

```yaml
P12_1_RuntimeStorageDecision:
  runtime_authorized: false
  install_authorized: false
  build_authorized: false
  package_manager_authorized: false
  storage_authorized: false
  database_creation_authorized: false
  embeddings_authorized: false
  provider_calls_authorized: false
  ollama_calls_authorized: false
  sandbox_execution_authorized: false
  decision_marker: "gbrain_runtime_remains_blocked"
```

## P12.0D Handoff Decision

P12.0D remains blocked.

```yaml
P12_0D_HandoffDecision:
  status: blocked
  reason: "P12.1 audit only; install/setup/runtime still not authorized"
  p12_0d_execution_authorized: false
  prerequisites_remaining:
    - "P12.SETUP accepted"
    - "controlled setup completed or executable path otherwise available under gate"
    - "sandbox GBRAIN_HOME and DB roots approved"
    - "exact commands approved"
    - "postinstall/lifecycle posture resolved"
    - "provider/API/Ollama posture resolved"
    - "human approval present"
```

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
```

Not created / not approved:

```text
No GBrain execution
No gbrain --help
No gbrain --version
No Bun execution
No Node execution
No package manager execution
No dependency installation
No node_modules
No build output
No postinstall execution
No migrations
No GBrain init
No GBrain import
No GBrain search
No GBrain query
No GBrain graph-query
No GBrain export
No Ollama execution
No Ollama model pull
No provider/API call
No credential inspection
No .env inspection
No provider configuration
No vector DB creation
No graph DB creation
No embeddings generated
No memory store created
No sandbox output path creation
No runtime activation
No adapter creation
No Graphify frontend copied
No Graphify source modified
No GBrain source modified
No product/Siamese inspection
No generated output inspection
No Graphify output import
No GBrain output import
No generated output tracking
No source tracking expansion
No authority promotion
No Cognitive Semantic System substrate selection
No Git mutation
No git add .
```

## Limitations

P12.1 used only local source, manifest, lockfile, documentation, and governance evidence.

P12.1 did not audit transitive dependency source code, did not fetch license metadata online, did not run package-manager audit commands, and did not validate installed dependency state.

P12.1 did not inspect credential files, `.env`, provider configs, global caches, `node_modules`, user home GBrain state, product paths, `9_artifacts/**`, `graphify-out/**`, or generated outputs.

P12.1 did not prove install success, runtime behavior, PGLite schema behavior, provider behavior, or model availability.

## Recommended Next Ticket

Recommended next ticket:

```text
P12.SETUP - GBrain Controlled Local Install / Build Plan
```

The P12.SETUP plan must include explicit postinstall/lifecycle suppression or sandboxing. If the reviewer requires complete transitive dependency license verification before setup planning, route first to:

```text
P12.RISK - GBrain License / Dependency / Storage Risk Resolution
```

P12.0D remains blocked in all P12.1 outcomes.

## Commit Commands

If this governance record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
git commit -m "Audit GBrain license dependencies and storage"
```

Push only if explicitly requested after review:

```powershell
git push
```

## Verification Plan

Allowed post-creation verification:

```text
Read/search the created audit document for required markers.
Run `git status --short`.
```

No runtime verification is authorized by P12.1.

## Verification Result

Non-mutating marker verification after creation found the final marker and required decision markers.

Observed `git status --short` after creation:

```text
?? 0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

The implementation file was observed before this report was created and was not inspected or modified by P12.1.

## Final Decision Record

```yaml
GBrainLicenseDependencyStorageAudit:
  ticket: P12.1
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_license_dependency_storage_audit.md"
  p12_cmd_dependency_present: true
  p12_cmd_marker_present: true
  source_root_present: true
  license_file_present: true
  package_license: "MIT"
  license_posture: "acceptable_for_controlled_setup"
  package_manager_candidate: "bun"
  lockfile_present: true
  dependency_posture: "requires_hardening"
  postinstall_lifecycle_risk: "requires_setup_gate"
  storage_posture: "acceptable_with_sandbox_boundary"
  setup_plan_may_be_generated: true
  install_authorized: false
  build_authorized: false
  runtime_authorized: false
  p12_0d_execution_authorized: false
  recommended_next_ticket: "P12.SETUP - GBrain Controlled Local Install / Build Plan"
  final_marker: "gbrain_license_dependency_storage_audit_ready"
```

Final marker:

```text
gbrain_license_dependency_storage_audit_ready
```

gbrain_license_dependency_storage_audit_ready
