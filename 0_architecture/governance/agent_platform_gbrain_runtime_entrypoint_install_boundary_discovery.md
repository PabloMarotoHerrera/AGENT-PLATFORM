# GBrain Runtime Entrypoint Install Boundary Discovery

## Summary

P12.CMD performed a read-only runtime-entrypoint and install-boundary discovery for the local GBrain source repository at `4_external/sources/gbrain-master`.

The GBrain source repo declares a CLI binary named `gbrain` in `package.json`, mapped directly to `src/cli.ts`. The entrypoint is a TypeScript file with a Bun shebang, so the local repository is Bun + TypeScript oriented. The repo has a `bun.lock` lockfile and `engines.bun >=1.3.10`, but it does not have a `packageManager` field and does not have the specifically checked `bun.lockb` file.

`gbrain` is not discoverable on `PATH` from the current shell. `node` and `npm` are discoverable, but the GBrain repo itself indicates Bun as the expected runtime/package manager. `pnpm`, `yarn`, `bun`, and `ollama` are not discoverable from this shell.

P12.CMD did not execute GBrain, Bun, Node, npm, Ollama, Graphify, package managers, tests, builds, scripts, TypeScript, or JavaScript. It did not install dependencies, create `node_modules`, create databases, create caches, initialize GBrain, generate embeddings, create sandbox outputs, inspect credentials, or mutate Git.

Decision markers:

```text
gbrain_source_repo_entrypoint_discovered
gbrain_cli_not_installed_confirmed
gbrain_install_boundary_requires_dependency_audit
gbrain_runtime_command_candidate_identified_but_not_executed
gbrain_runtime_setup_blocked_until_p12_1
```

Final marker:

```text
gbrain_runtime_entrypoint_install_boundary_discovery_ready
```

## Files Inspected

Governance and scope files inspected:

```text
0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
.graphifyignore
```

GBrain source files inspected read-only:

```text
4_external/sources/gbrain-master/package.json
4_external/sources/gbrain-master/bun.lock
4_external/sources/gbrain-master/tsconfig.json
4_external/sources/gbrain-master/README.md
4_external/sources/gbrain-master/INSTALL_FOR_AGENTS.md
4_external/sources/gbrain-master/docs/INSTALL.md
4_external/sources/gbrain-master/src/cli.ts
4_external/sources/gbrain-master/src/commands/init.ts
4_external/sources/gbrain-master/src/commands/import.ts
4_external/sources/gbrain-master/src/commands/export.ts
4_external/sources/gbrain-master/src/core/config.ts
4_external/sources/gbrain-master/src/core/ai/recipes/ollama.ts
```

Discovery-only file globs also observed:

```text
4_external/sources/gbrain-master/README.md
4_external/sources/gbrain-master/INSTALL_FOR_AGENTS.md
4_external/sources/gbrain-master/docs/INSTALL.md
4_external/sources/gbrain-master/CONTRIBUTING.md
4_external/sources/gbrain-master/tsconfig.json
4_external/sources/gbrain-master/admin/tsconfig.json
4_external/sources/gbrain-master/bun.lock
4_external/sources/gbrain-master/admin/bun.lock
```

The `admin/**`, `test/**`, `tests/**`, `evals/**`, `recipes/**`, and other discovered README/lockfile paths were not opened except for the root-level files listed above.

## Files Created

```text
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
```

## Files Modified

No existing file was modified. The only file change is the new P12.CMD governance report.

## Commands Run

Allowed presence-only commands run:

```powershell
Test-Path -LiteralPath "0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md"
Test-Path -LiteralPath "4_external/sources/gbrain-master"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/pnpm-lock.yaml"
Test-Path -LiteralPath "4_external/sources/gbrain-master/package-lock.json"
Test-Path -LiteralPath "4_external/sources/gbrain-master/yarn.lock"
Test-Path -LiteralPath "4_external/sources/gbrain-master/bun.lockb"
Test-Path -LiteralPath "4_external/sources/gbrain-master/src/cli.ts"
Get-Command gbrain -ErrorAction SilentlyContinue
Get-Command node -ErrorAction SilentlyContinue
Get-Command npm -ErrorAction SilentlyContinue
Get-Command pnpm -ErrorAction SilentlyContinue
Get-Command yarn -ErrorAction SilentlyContinue
Get-Command bun -ErrorAction SilentlyContinue
Get-Command ollama -ErrorAction SilentlyContinue
```

Allowed read-only tool searches and file reads were used to inspect source text. No package manager, runtime, test, build, provider, Graphify, GBrain, Ollama, Node, Python, Docker, or CI command was executed.

Observed command results:

| Check | Result |
| --- | --- |
| P12.0C file | `True` |
| GBrain source root | `True` |
| `package.json` | `True` |
| `pnpm-lock.yaml` | `False` |
| `package-lock.json` | `False` |
| `yarn.lock` | `False` |
| `bun.lockb` | `False` |
| `src/cli.ts` | `True` |
| `Get-Command gbrain` | No output |
| `Get-Command node` | `node.exe` discoverable at `C:\Program Files\nodejs\node.exe` |
| `Get-Command npm` | `npm.ps1` discoverable at `C:\Program Files\nodejs\npm.ps1` |
| `Get-Command pnpm` | No output |
| `Get-Command yarn` | No output |
| `Get-Command bun` | No output |
| `Get-Command ollama` | No output |

Initial `git status --short` observed before this report existed:

```text
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

That implementation file was not inspected or modified.

## P12.0C Dependency Status

P12.0C exists at:

```text
0_architecture/governance/agent_platform_gbrain_ollama_controlled_sandbox_plan.md
```

P12.0C final marker is present:

```text
gbrain_ollama_controlled_sandbox_plan_ready
```

P12.0C explicitly says the immediate next gate is command discovery because `gbrain` and `ollama` were not discoverable on `PATH`, and it keeps P12.0D runtime execution unauthorized.

## GBrain Source Root Status

The expected local GBrain source root exists:

```text
4_external/sources/gbrain-master
```

The source root is a local source repository, not an installed CLI confirmation. The source root itself is sufficient for source-review and install-boundary planning, but not for P12.0D runtime execution.

## CLI Availability Status

`Get-Command gbrain -ErrorAction SilentlyContinue` returned no output.

Decision:

```yaml
gbrain_cli_available_on_current_path: false
gbrain_cli_absent_globally_proven: false
gbrain_cli_not_installed_confirmed_for_current_shell: true
runtime_execution_authorized: false
```

`Get-Command node` and `Get-Command npm` returned command records, but neither command was executed. Their presence does not satisfy the GBrain runtime requirement because the repo declares Bun as its runtime/package-manager path.

`Get-Command bun` returned no output. This blocks Bun-based source execution and Bun-based install/setup until a future gate resolves the Bun availability/install boundary.

## Package Manager Evidence

Package-manager evidence points to Bun.

Manifest evidence from `package.json`:

```json
{
  "type": "module",
  "main": "src/core/index.ts",
  "bin": {
    "gbrain": "src/cli.ts"
  },
  "scripts": {
    "dev": "bun run src/cli.ts",
    "build": "bun build --compile --outfile bin/gbrain src/cli.ts"
  },
  "engines": {
    "bun": ">=1.3.10"
  }
}
```

Additional manifest evidence:

```text
The scripts use `bun run`, `bun build`, and `bun test` patterns.
The dev dependencies include `bun-types` and `@types/bun`.
The package has no `packageManager` field.
The package has `trustedDependencies: ["@electric-sql/pglite"]`.
```

Documentation evidence:

```text
INSTALL_FOR_AGENTS.md says: "Bun is required - gbrain is a Bun + TypeScript runtime".
README.md and docs/INSTALL.md both use `bun install -g github:garrytan/gbrain` as the install path.
docs/INSTALL.md describes a deterministic fallback as `git clone ... && cd ~/gbrain && bun install && bun link`.
```

Source evidence:

```text
src/cli.ts line 1 has `#!/usr/bin/env bun`.
```

## Lockfile Evidence

Presence-only checks from the required list:

```yaml
pnpm_lock_yaml_present: false
package_lock_json_present: false
yarn_lock_present: false
bun_lockb_present: false
```

Additional local-source discovery observed a modern Bun lockfile:

```text
4_external/sources/gbrain-master/bun.lock
```

The root `bun.lock` declares `lockfileVersion: 1`, `name: gbrain`, production dependencies, dev dependencies, and `trustedDependencies` including `@electric-sql/pglite`.

Decision:

```yaml
lockfile_present: true
lockfile_kind: "bun.lock"
package_manager_candidate: "bun"
package_manager_version_candidate_from_packageManager_field: null
package_manager_version_candidate_from_engines: ">=1.3.10"
```

## Package Manifest Bin Mapping

`package.json` declares:

```json
"bin": {
  "gbrain": "src/cli.ts"
}
```

Decision:

```yaml
binary_name: "gbrain"
bin_mapping_source: "package.json"
entrypoint_file: "4_external/sources/gbrain-master/src/cli.ts"
entrypoint_status: "confirmed_from_manifest"
```

## Runtime Entrypoint

The CLI entrypoint is:

```text
4_external/sources/gbrain-master/src/cli.ts
```

Source evidence:

```text
src/cli.ts has `#!/usr/bin/env bun`.
src/cli.ts imports TypeScript modules directly, including `./core/config.ts`, `./core/operations.ts`, and command modules.
src/cli.ts handles `--help` and `--version` inside the CLI source, but running either would still execute the Bun/TypeScript entrypoint and module loading.
src/cli.ts lists CLI-only commands including `init`, `import`, `export`, `serve`, `config`, `doctor`, `sync`, `extract`, `graph-query`, `sources`, `code-def`, `code-refs`, `code-callers`, and `code-callees`.
```

Decision:

```yaml
source_repo_entrypoint_discovered: true
runtime_command_candidate_identified: true
runtime_executed: false
```

## Script Inventory

Selected package scripts relevant to install/setup/runtime boundary:

| Script | Command Text | Boundary Assessment |
| --- | --- | --- |
| `dev` | `bun run src/cli.ts` | Source-runtime candidate, not executed. Requires Bun and installed dependencies. |
| `build` | `bun build --compile --outfile bin/gbrain src/cli.ts` | Compiled-binary candidate, not executed. Would create `bin/gbrain`. |
| `build:all` | `bun build --compile --target=... --outfile bin/... src/cli.ts` | Multi-target compiled-binary candidate, not executed. Would create binaries. |
| `build:admin` | `cd admin && bun run build && cd .. && bun run scripts/build-admin-embedded.ts` | Admin build candidate, not needed for P12.0D and not executed. |
| `build:schema` | `bash scripts/build-schema.sh` | Generated schema candidate, not executed. |
| `build:llms` | `bun run scripts/build-llms.ts` | Generated docs/map candidate, not executed. |
| `build:pglite-snapshot` | `bun run scripts/build-pglite-snapshot.ts` | Generated PGLite snapshot candidate, not executed. |
| `test` | `bash scripts/run-unit-parallel.sh` | Test command, prohibited in P12.CMD and not executed. |
| `verify` | `bash scripts/run-verify-parallel.sh` | Verification script, prohibited in P12.CMD and not executed. |
| `typecheck` | `tsc --noEmit` | TypeScript command, prohibited in P12.CMD and not executed. |
| `postinstall` | `command -v gbrain ... && gbrain apply-migrations --yes --non-interactive || echo ...` | Material side-effect risk. May execute GBrain migration command during install if `gbrain` is discoverable. Must be audited before any package-manager command. |

The `postinstall` script is a key install-boundary blocker. Any future setup plan must decide whether postinstall scripts are allowed, suppressed, sandboxed, or otherwise controlled. P12.CMD does not authorize package-manager execution.

## Install Requirement Assessment

Running the local source as a CLI requires at least:

```text
Bun runtime availability
dependency installation or otherwise available dependencies
TypeScript runtime support through Bun
controlled handling of package postinstall behavior
controlled GBrain home/config/database path selection before any GBrain runtime command
```

Current shell state:

```yaml
gbrain_on_path: false
bun_on_path: false
node_on_path: true
npm_on_path: true
pnpm_on_path: false
yarn_on_path: false
ollama_on_path: false
```

Assessment:

```yaml
install_required_before_plain_gbrain_runtime: true
dependency_install_required_before_source_runtime: true
dependency_state_validated: false
postinstall_risk_present: true
install_authorized_by_P12_CMD: false
```

The repo likely can be run from source after Bun and dependencies are available because `dev` maps to `bun run src/cli.ts` and the bin entry maps directly to `src/cli.ts`. That source-runtime path is a future candidate only, not an authorization.

## Build Requirement Assessment

The manifest bin maps directly to TypeScript source and `src/cli.ts` has a Bun shebang. That indicates a build is not strictly required for a Bun source-runtime path.

The `build` and `build:all` scripts exist for compiled binaries and would create output under `bin/`. They are not required to identify the entrypoint, and P12.CMD did not run them.

Assessment:

```yaml
build_required_for_bun_source_runtime: false
build_required_for_standalone_binary: true
build_state_validated: false
build_authorized_by_P12_CMD: false
```

## Runtime Side-Effect Assessment

Source review shows future GBrain runtime can write configuration, database, gitignore, import data, and export output.

Runtime side-effect evidence:

```text
src/core/config.ts `saveConfig()` creates the active GBrain config directory and writes `config.json`.
src/core/config.ts `ensureGitignore()` can create `.gitignore` inside the GBrain home.
src/core/config.ts honors `GBRAIN_HOME` as an absolute parent path and appends `.gbrain`.
src/core/config.ts defaults to the user home `.gbrain` when `GBRAIN_HOME` is not set.
src/commands/init.ts defaults PGLite to `gbrainPath('brain.pglite')`, or uses `--path <DIR>`.
src/commands/init.ts connects a PGLite engine and calls `initSchema()`.
src/commands/init.ts writes `database_path`, embedding config, MCP config defaults, and self-upgrade config into config.
src/commands/import.ts imports files and can create chunks; without `--no-embed`, it validates embedding credentials.
src/commands/export.ts creates directories and writes markdown plus `.raw/*.json` sidecar files under the export directory.
```

Runtime side effects to block without future gate:

```text
global or default user-home `.gbrain` writes
non-sandbox PGLite database creation
Postgres connection or migration
provider/API calls
embedding generation
imported chunks
exports
logs
cache writes
self-upgrade/update heartbeat behavior
config or `.gitignore` creation under GBrain home
```

P12.0D must use a sandbox-only `GBRAIN_HOME`, sandbox-only DB path, and explicit no-embedding posture if runtime is later approved.

## Install Side-Effect Assessment

Potential install/setup side effects for future gates:

```text
`node_modules/` creation
Bun package-manager cache writes
lockfile mutation risk
postinstall script execution risk
global binary/link creation risk
compiled output under `bin/` if build scripts run
admin build output if admin scripts run
generated schema/docs/snapshot artifacts if build helper scripts run
```

The `postinstall` script is especially important because it conditionally invokes `gbrain apply-migrations --yes --non-interactive` if `gbrain` is discoverable. Future setup must explicitly decide whether package-manager lifecycle scripts are allowed and how to prevent global/default GBrain state mutation.

No install side effect was created by P12.CMD.

## Command Candidates Not Executed

Future setup command candidates, not executed:

| Candidate | Purpose | Status | Gate Required |
| --- | --- | --- | --- |
| `bun install -g github:garrytan/gbrain` | Upstream documented global install | `candidate_not_executed` | P12.SETUP after P12.1 |
| `bun install` | Local dependency install inside source repo | `candidate_not_executed` | P12.SETUP after P12.1 |
| `bun link` | Deterministic fallback link from local clone | `candidate_not_executed` | P12.SETUP after P12.1 |
| `bun run src/cli.ts --help` | Source-run help smoke | `candidate_not_executed` | Future runtime/setup gate only |
| `bun run src/cli.ts --version` | Source-run version smoke | `candidate_not_executed` | Future runtime/setup gate only |
| `bun run build` | Compile standalone `bin/gbrain` | `candidate_not_executed` | Future build gate only |
| `bun run dev -- --help` | Scripted source-run help smoke | `candidate_not_executed` | Future runtime/setup gate only |

Future runtime command candidates from P12.0C and source/docs, not executed:

| Candidate | Purpose | Status |
| --- | --- | --- |
| `gbrain --help` | Help discovery | `candidate_not_executed` |
| `gbrain --version` | Version discovery | `candidate_not_executed` |
| `gbrain init --pglite --path "<sandbox-db>" --no-embedding` | Sandbox no-embedding init | `candidate_not_executed` |
| `gbrain config set search.mcp_keyword_only true` | Force keyword-only search posture | `candidate_not_executed` |
| `gbrain import "<sandbox-fixture>" --no-embed` | Import fixture without embeddings | `candidate_not_executed` |
| `gbrain search "<query>"` | Keyword-only retrieval smoke after config | `candidate_not_executed` |
| `gbrain graph-query <fixture-slug> --depth 2 --direction both` | Graph traversal smoke | `candidate_not_executed` |
| `gbrain export --dir "<sandbox-export>"` | Local export smoke | `candidate_not_executed` |
| `gbrain query "<query>" --no-expand` | Optional later query path avoiding expansion | `candidate_not_executed` |

Future Ollama command candidates, not executed and still blocked:

| Candidate | Purpose | Status |
| --- | --- | --- |
| `ollama list` | Model inventory | `candidate_not_executed` |
| `ollama show <model>` | Model metadata | `candidate_not_executed` |
| `ollama pull <model>` | Model download | `candidate_not_executed`, separate approval required |
| `ollama serve` | Start local service | `candidate_not_executed`, separate approval required |

## Install Boundary Model

```yaml
GBrainInstallBoundary:
  source_root: "4_external/sources/gbrain-master"
  cli_installed_on_path: false
  package_manager_candidate: "bun"
  lockfile_present: true
  lockfile_kind: "bun.lock"
  package_manager_field_present: false
  package_manager_version_candidate: null
  engine_version_candidate: ">=1.3.10"
  install_required_before_runtime: true
  build_required_before_runtime: false
  node_modules_side_effect: true
  global_install_required: false
  local_install_candidate: true
  postinstall_script_present: true
  postinstall_requires_separate_audit: true
  execution_authorized_by_P12_CMD: false
  install_authorized_by_P12_CMD: false
```

Notes:

```text
`global_install_required: false` means a global install is not the only possible route because the repo has a Bun source-runtime path. Plain `gbrain` on PATH would still require a global install, link, or controlled shim.
`build_required_before_runtime: false` applies to the Bun source-runtime path. Building is required only if a compiled standalone binary is selected in a future gate.
```

## Runtime Entrypoint Model

```yaml
GBrainRuntimeEntrypoint:
  binary_name: "gbrain"
  bin_mapping_source: "package.json"
  entrypoint_file: "4_external/sources/gbrain-master/src/cli.ts"
  entrypoint_status: "confirmed_from_manifest"
  source_runtime_status: "confirmed_from_source"
  source_runtime: "bun TypeScript entrypoint"
  command_candidates:
    - command_text: "gbrain --help"
      purpose: "help"
      status: "candidate_not_executed"
    - command_text: "gbrain --version"
      purpose: "version"
      status: "candidate_not_executed"
    - command_text: "gbrain init --pglite --path <sandbox-db> --no-embedding"
      purpose: "init"
      status: "candidate_not_executed"
    - command_text: "gbrain config set search.mcp_keyword_only true"
      purpose: "config"
      status: "candidate_not_executed"
    - command_text: "gbrain import <sandbox-fixture> --no-embed"
      purpose: "import"
      status: "candidate_not_executed"
    - command_text: "gbrain search <query>"
      purpose: "search"
      status: "candidate_not_executed"
    - command_text: "gbrain query <query> --no-expand"
      purpose: "query"
      status: "candidate_not_executed"
    - command_text: "gbrain graph-query <fixture-slug> --depth 2 --direction both"
      purpose: "graph-query"
      status: "candidate_not_executed"
    - command_text: "gbrain export --dir <sandbox-export>"
      purpose: "export"
      status: "candidate_not_executed"
  execution_authorized_by_P12_CMD: false
```

## Side-Effect Boundary Model

```yaml
GBrainSideEffectBoundary:
  install_side_effects:
    - node_modules
    - package manager cache
    - lockfile mutation risk
    - postinstall scripts risk
    - global binary or link risk
  build_side_effects:
    - bin/gbrain
    - platform-specific binaries under bin
    - generated JS or compiled executable output
    - generated type or schema artifacts if helper scripts run
    - build cache
  runtime_side_effects:
    - GBRAIN_HOME
    - PGLite/Postgres DB
    - config files
    - GBrain home `.gitignore`
    - imported chunks
    - embeddings
    - logs
    - exports
    - raw sidecar JSON exports
    - temporary files
  blocked_side_effects_without_future_gate:
    - global install
    - package manager execution
    - postinstall scripts
    - global user home writes
    - non-sandbox database writes
    - provider/API calls
    - credential reads
    - Ollama model calls
    - Graphify execution
    - generated output tracking
```

## Discovery Questions

| Question | Answer |
| --- | --- |
| Is GBrain installed as a CLI? | Not discoverable on current `PATH`; treated as not installed for this shell. |
| Is GBrain only present as source? | For current workspace evidence, yes: source root exists and CLI is not discoverable. |
| What package manager is indicated? | Bun. |
| Is there a lockfile? | Yes, `bun.lock`; no `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, or `bun.lockb`. |
| What does `package.json` declare under `bin`? | `gbrain` maps to `src/cli.ts`. |
| What scripts are present? | Bun-oriented `dev`, `build`, `build:all`, build helpers, tests/checks, and `postinstall`. |
| What entrypoint file does the CLI use? | `4_external/sources/gbrain-master/src/cli.ts`. |
| Does running the CLI require dependencies? | Yes for source runtime; it imports many package modules and TypeScript files. Dependency state was not installed or validated. |
| Does running the CLI require a build? | Not for Bun source runtime; yes if a standalone compiled binary route is selected. |
| Does the repo support running from source? | Source evidence indicates yes via Bun shebang and `dev: bun run src/cli.ts`, but not authorized or tested. |
| Does the repo require TypeScript runtime tooling? | Yes for source path: Bun runs the TypeScript entrypoint directly. |
| Would setup create `node_modules`? | A local dependency install likely would. Not created by P12.CMD. |
| Would setup change any repo files? | It could create `node_modules`, possibly mutate lockfiles, and build scripts could create `bin/` or generated artifacts. |
| Would setup create caches outside the repo? | Package managers commonly use external caches; Bun cache location was not inspected. |
| Would setup create GBrain config/home/db outside sandbox? | Runtime could, if `GBRAIN_HOME` and `--path` are not controlled. |
| Can setup be done inside the repo safely? | Not yet. It needs P12.1 dependency/license/storage audit and P12.SETUP postinstall/rollback planning. |
| Should dependency/license/storage audit happen first? | Yes. |
| What is the safest next ticket? | `P12.1 - GBrain License / Dependency / Storage Audit`. |

## P12.0D Handoff Decision

P12.0D remains blocked.

```yaml
P12_0D_HandoffDecision:
  status: blocked
  reason: "source repo entrypoint exists, but CLI is not installed on PATH and dependency/install/storage boundaries are not accepted"
  p12_0d_execution_authorized: false
  gbrain_executable_path_known: false
  install_build_state_known: false
  dependency_storage_risk_accepted: false
  sandbox_roots_approved_for_execution: false
  exact_runtime_commands_approved: false
  human_runtime_approval_present: false
```

P12.0D must remain blocked unless all of the following become true in later gates:

```text
GBrain executable path is known.
Install/build state is known.
Dependency/storage risk is accepted.
Sandbox GBRAIN_HOME and DB roots are approved.
Exact commands are approved.
Human approval is present.
```

## Recommended Next Ticket

Recommended next ticket:

```text
P12.1 - GBrain License / Dependency / Storage Audit
```

Then, if P12.1 accepts dependency/storage posture:

```text
P12.SETUP - GBrain Controlled Local Install / Build Plan
```

Then, if setup is approved and completed:

```text
P12.0D - GBrain Ollama Controlled Sandbox Execution
```

P12.CMD2 is not needed because the entrypoint is resolved.

## Future Setup Approval Boundary

A future setup/install ticket must require a statement like:

```text
Human approval present for controlled local GBrain setup planning only. Do not execute package managers, do not install dependencies, do not run GBrain, do not initialize databases, do not write global user config, do not inspect credentials, do not run provider APIs, do not create embeddings, do not mutate Git, and do not track generated files.
```

A future actual install/build ticket must explicitly list:

```text
package manager
exact command
working directory
expected created files
expected modified files
node_modules/cache behavior
postinstall script posture
rollback plan
human approval
```

## Created / Not Created Register

Created:

```text
0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
```

Not created / not approved:

```text
No GBrain execution
No gbrain --help
No gbrain --version
No Node execution
No package manager execution
No dependency installation
No node_modules
No build output
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

P12.CMD did not validate whether dependencies are already present locally because inspecting or relying on runtime dependency state is setup territory.

P12.CMD did not execute Bun, Node, npm, GBrain, or any TypeScript/JavaScript runtime.

P12.CMD did not inspect package-manager cache locations, global install state, user home GBrain config, environment variables, credentials, provider configs, Ollama configs, product paths, `9_artifacts/**`, or generated outputs.

P12.CMD did not prove that `gbrain` is absent from every possible shell or global location. It proves only that `Get-Command gbrain` returned no output in the current shell.

## Commit Commands

If this governance record is accepted for commit, stage only the intended file. Do not use `git add .`.

```powershell
git status --short
git add 0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
git commit -m "Discover GBrain runtime entrypoint install boundary"
```

Push only if explicitly requested after review:

```powershell
git push
```

## Verification Plan

Allowed post-creation verification:

```powershell
rg "gbrain_runtime_entrypoint_install_boundary_discovery_ready|gbrain_source_repo_entrypoint_discovered|gbrain_cli_not_installed_confirmed|gbrain_install_boundary_requires_dependency_audit|gbrain_runtime_command_candidate_identified_but_not_executed|gbrain_runtime_setup_blocked_until_p12_1" 0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
git status --short
```

No runtime verification is authorized by P12.CMD.

## Verification Result

Non-mutating marker verification after creation found the final marker and required decision markers.

Observed `git status --short` after creation:

```text
?? 0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md
?? 0_architecture/implementation/graphify_command_candidate_confirmation.md
```

The implementation file was observed before this report was created and was not inspected or modified by P12.CMD.

## Final Decision Record

```yaml
GBrainRuntimeEntrypointInstallBoundaryDiscovery:
  ticket: P12.CMD
  date: "2026-07-09"
  target_file: "0_architecture/governance/agent_platform_gbrain_runtime_entrypoint_install_boundary_discovery.md"
  p12_0c_dependency_present: true
  p12_0c_final_marker_present: true
  source_root_present: true
  gbrain_cli_on_path: false
  source_repo_entrypoint_discovered: true
  package_manager_candidate: "bun"
  package_manager_field_present: false
  lockfile_present: true
  lockfile_kind: "bun.lock"
  binary_name: "gbrain"
  entrypoint_file: "4_external/sources/gbrain-master/src/cli.ts"
  source_runtime: "Bun TypeScript"
  dependencies_installed_or_validated: false
  build_required_for_source_runtime: false
  postinstall_risk_present: true
  install_authorized_by_P12_CMD: false
  runtime_execution_authorized_by_P12_CMD: false
  p12_0d_execution_authorized: false
  recommended_next_ticket: "P12.1 - GBrain License / Dependency / Storage Audit"
  final_marker: "gbrain_runtime_entrypoint_install_boundary_discovery_ready"
```

Final marker:

```text
gbrain_runtime_entrypoint_install_boundary_discovery_ready
```

gbrain_runtime_entrypoint_install_boundary_discovery_ready
