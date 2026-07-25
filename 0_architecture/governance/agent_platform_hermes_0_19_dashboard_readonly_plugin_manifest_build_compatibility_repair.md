# P15.M10A - Dashboard Readonly Plugin Manifest Build Compatibility Repair

Status: P15.M10A dashboard readonly plugin manifest build compatibility repaired with constraints.

Final verdict: `hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints`

## Ticket Authority

P15.M10A is a bounded product compatibility repair after P15.M10 stopped at the
source Dockerfile frontend build stage with a TypeScript readonly-variance
diagnostic in the dashboard `App.tsx` route and navigation assembly helpers.

Authorized mutations were limited to:

```text
2_products/pepper-agent/web/src/App.tsx
2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md
```

No Docker pilot retry, Docker build, Compose start, WSL mutation, Linux checkout
mutation, runtime evidence mutation, dependency installation, package or lock
mutation, OAuth, credential inspection, provider call, inference, worker start,
agent start, staging, commit or push was authorized or performed.

## Repository And Branch State

| Check | Result |
| --- | --- |
| Repository root | `<WINDOWS_REPOSITORY_ROOT>` |
| Branch | `p15.m-hermes-0.19-migration` |
| HEAD | `cc5ea5c3ef425274f56affb2b10e02401e619774` |
| `origin/p15.m-hermes-0.19-migration` | `cc5ea5c3ef425274f56affb2b10e02401e619774` |
| HEAD equals branch remote at start | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |
| Visible untracked task candidates at start | `0` |

P15.M9 was present in `HEAD`, locally unmodified and unstaged:

```text
0_architecture/governance/agent_platform_hermes_0_19_wsl2_development_architecture.md
```

P15.M9 verdict:

```text
hermes_0_19_wsl2_development_architecture_ready_with_constraints
```

P15.M10 blocker state at P15.M10A start:

| Check | Result |
| --- | --- |
| P15.M10 governance record in `HEAD` | `false` |
| P15.M10 governance record in worktree | `false` |
| P15.M10 product candidate changes | `0` |
| P15.M10 containers | `0` |
| P15.M10 networks | `0` |
| P15.M10 tagged image created | `false` |
| Build process remaining | `false` |
| Linux checkout clean | `true` |
| OAuth activity | `0` |
| Provider activity | `0` |
| Inference activity | `0` |
| Worker activity | `0` |
| Agent activity | `0` |

## Committed Prerequisites

| Record | Required verdict | State |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_workspace_adoption_assessment.md` | `hermes_0_19_workspace_adoption_assessment_ready_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` | `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_governed_runtime_adapter_post_commit_integrity_closure.md` | `hermes_0_19_governed_runtime_adapter_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_wsl2_development_architecture.md` | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |

Required product state before repair:

| Field | Value |
| --- | --- |
| Product ID | `pepper` |
| Product version | `0.1.0-dev` |
| Upstream version | `0.19.0` |
| Upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Product UI | `disabled` |
| Extension modules | `0` |

Current committed product identity before repair:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6768` | `149234329` | `f0dceedbe9ae1b6b0738c00b0d643678d8bc5acd2b9766729f7adcb238c08e59` |
| Payload | `6681` | `145409765` | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |
| Baseline record | n/a | `34254` | `478f1cd5279806e808b562193a993f391f98a4e8513ef4ee8d41e35a0d7c4dda` |

The canonical governance integrity suite ran against committed `HEAD`:

```text
python -m unittest discover -s 12_tests/governance -p test_pepper_baseline_integrity.py
```

Result: `14` tests, `0` failures, `0` errors.

## P15.M10 Blocker

Accepted P15.M10 stop classification:

```text
P15.M10-IMAGE-BUILD-BLOCKED
```

Observed P15.M10 source Dockerfile frontend build state:

| Field | Value |
| --- | --- |
| Build duration before failure | `1114` seconds |
| Docker build stage | source Dockerfile frontend build |
| Failing command | `RUN cd web && npm run build && cd ../ui-tui && npm run build` |

Exact original diagnostics:

```text
web/src/App.tsx(495,43): readonly PluginManifest[] is not assignable to PluginManifest[]
web/src/App.tsx(507,38): readonly PluginManifest[] is not assignable to PluginManifest[]
```

The retained P15.M10 build log was not present inside the repository. P15.M10A
therefore used the accepted P15.M10 stop evidence and locally reproduced the same
frontend production-build diagnostics without restarting Docker.

Local pre-repair reproduction:

| Command | Result |
| --- | --- |
| `npm run typecheck` | passed; this script invokes `tsc -p . --noEmit` over a reference-only root config |
| `npm run build` | failed before Vite with exactly the two readonly manifest diagnostics and no unrelated TypeScript diagnostics |

## Root Cause

Source readonly contract:

```typescript
export interface FilteredPluginManifests {
  readonly blockedManifestCount: number;
  readonly manifests: readonly PluginManifest[];
}
```

Filtering behavior:

```typescript
return Object.freeze({
  blockedManifestCount,
  manifests: Object.freeze(accepted),
});
```

App flow:

```text
usePlugins().manifests
filterProtectedPluginManifests(...)
filteredPluginManifests.manifests
shellPluginManifests
partitionSidebarNav(...)
buildRoutes(...)
```

Failure classification:

| Field | Value |
| --- | --- |
| Failure kind | `compile_time_readonly_parameter_variance` |
| Runtime failure | `false` |
| Plugin filter failure | `false` |
| Route logic failure | `false` |
| Navigation logic failure | `false` |
| Dockerfile failure | `false` |
| Dependency resolution failure | `false` |
| Lockfile failure | `false` |
| Upstream source failure | `false` |

The filtered manifest collection must remain readonly. Local consumers that do
not mutate the collection must accept readonly input.

## Exact Repair

Modified file:

```text
2_products/pepper-agent/web/src/App.tsx
```

Changed function signatures:

| Helper | Previous parameter | Repaired parameter |
| --- | --- | --- |
| `buildNavItems` | `manifests: PluginManifest[]` | `manifests: readonly PluginManifest[]` |
| `partitionSidebarNav` | `manifests: PluginManifest[]` | `manifests: readonly PluginManifest[]` |
| `buildRoutes` | `manifests: PluginManifest[]` | `manifests: readonly PluginManifest[]` |

Scope validation:

| Check | Result |
| --- | --- |
| Changed function signatures | `3` |
| Changed runtime expressions | `0` |
| Changed imports | `0` |
| Changed exports | `0` |
| Changed hooks | `0` |
| Changed routes | `0` |
| Changed navigation items | `0` |
| Changed plugin filters | `0` |
| Changed plugin activation | `0` |
| Changed rendering | `0` |
| Runtime statements changed | `0` |
| Casts added | `0` |
| Array copies added to silence type error | `0` |
| Compiler suppressions added | `0` |
| Immutability weakened | `false` |
| Resulting `App.tsx` encoding | UTF-8 without BOM |
| Resulting `App.tsx` line endings | LF |

No `@ts-ignore`, `@ts-expect-error`, `eslint-disable`, `any`, `unknown` cast
chain, mutable cast, array spread copy or `Array.from` bypass was added.

## Runtime Semantic Equivalence

| Behavior | Result |
| --- | --- |
| `buildNavItems` runtime body changed | `false` |
| `partitionSidebarNav` runtime body changed | `false` |
| `buildRoutes` runtime body changed | `false` |
| Protected plugin filtering changed | `false` |
| Plugin order behavior changed | `false` |
| Plugin override behavior changed | `false` |
| Hidden plugin route behavior changed | `false` |
| Built-in route behavior changed | `false` |
| Product extension behavior changed | `false` |
| Sidebar grouping behavior changed | `false` |
| Chat override behavior changed | `false` |
| Protected namespace changed | `false` |

The generated JavaScript behavior of the three helpers remains semantically
equivalent; only TypeScript input variance changed.

## Frontend Validation

Commands ran from `2_products/pepper-agent/web` using the externally prepared
dependency environment. No install, clean install, update or audit-fix command
was run.

| Command | Result |
| --- | --- |
| `npm run typecheck` | passed, exit code `0`, TypeScript errors `0`, readonly manifest errors `0` |
| `npm run test` | passed |
| `npm run lint` | exit code `0`, lint errors `0`, warnings `24`, warnings affecting acceptance `0` |
| `npm run build` | passed, exit code `0` |

Frontend test result:

| Field | Value |
| --- | --- |
| Test files | `21` passed |
| Tests | `134` passed |
| Failed test files | `0` |
| Failed tests | `0` |
| Unhandled errors | `0` |
| Unexpected skips | `0` |
| Duration | `1.47s` |

Existing coverage lanes represented by the suite and production build:

```text
agent-platform shell
protected plugin filtering
product configuration
product extension registry
App route composition
navigation grouping
```

Production build result:

| Field | Value |
| --- | --- |
| TypeScript build | passed |
| Vite build | passed |
| Modules transformed | `505` |
| Build duration | `475ms` |
| Output asset count | `10` |
| Readonly manifest errors | `0` |
| Warnings | `1` chunk-size warning |
| Security warning | `0` |
| Credential warning | `0` |
| Provider warning | `0` |
| Unhandled resource warning | `0` |
| Warnings affecting acceptance | `0` |

The chunk-size warning is an existing frontend bundle-size warning from Vite and
does not affect the readonly manifest compatibility repair.

## Modification Register

Modified register:

```text
2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

Register reconciliation result:

| Check | Result |
| --- | --- |
| Columns | `18` |
| Rows | `87` |
| Reconciled row | `P15.M6-021` |
| Reconciled path | `web/src/App.tsx` |
| Preimage hash | `8ca66b772754824ac4ecada6f11c20ea8af518657bb3d272daef7d86d4987972` |
| Candidate App bytes | `44709` |
| Candidate App SHA-256 | `fcb51f78c1912f836cdc2bbf9db4483210db9f2ce30af7a882cfc8ba5f6b1fb2` |
| Fields changed in `P15.M6-021` | `1` |
| Changed field | `current_product_sha256_or_none` |
| Other row changes | `0` |
| New register rows | `0` |
| Duplicate modification IDs | `0` |
| Duplicate paths | `0` |
| Blank mandatory fields | `0` |
| Invalid classifications | `0` |
| `P15.M6-021` occurrences | `1` |
| `web/src/App.tsx` occurrences | `1` |
| Unaffected rows checked against `HEAD` blobs | `86` |
| Unaffected `HEAD` blob hash mismatches | `0` |
| Candidate App hash matches register | `true` |
| Current `HEAD` App hash differs from candidate App hash | `true` |

`P15.M6-021` remains the semantic product-divergence owner. P15.M10A updates
only the current content identity after a bounded compatibility repair to that
same divergence.

Post-commit register, candidate and payload integrity are pending P15.M10AR.

## Canonical Integrity Boundary

The canonical utility uses committed `HEAD` blobs. Because P15.M10A is
uncommitted, the current committed identity remains unchanged:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6768` | `149234329` | `f0dceedbe9ae1b6b0738c00b0d643678d8bc5acd2b9766729f7adcb238c08e59` |
| Payload | `6681` | `145409765` | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |

`2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json` was not
modified. P15.M10AR owns post-commit candidate identity, payload identity and
baseline JSON closure after the human commits and pushes P15.M10A.

## Docker, WSL And Runtime Boundary

| Activity | Count |
| --- | ---: |
| Docker Desktop starts by P15.M10A | `0` |
| Docker daemon starts by P15.M10A | `0` |
| Docker builds | `0` |
| Image pulls | `0` |
| Image creations | `0` |
| Container starts | `0` |
| Compose starts | `0` |
| Compose network creations | `0` |
| WSL distribution starts by P15.M10A | `0` |
| Linux checkout mutations | `0` |
| Runtime root mutations | `0` |
| Pilot evidence mutations | `0` |

P15.M10A did not delete BuildKit cache, prune Docker resources or modify the
retained Linux-native checkout.

## Provider And Credential Boundary

| Activity | Count |
| --- | ---: |
| Real auth stores inspected | `0` |
| Real credentials read | `0` |
| Real credentials written | `0` |
| Live OAuth attempts | `0` |
| Browser open attempts | `0` |
| Device code requests | `0` |
| Token exchange requests | `0` |
| Provider calls | `0` |
| Inference calls | `0` |
| Model-list calls | `0` |
| Usage calls | `0` |
| Provider worker starts | `0` |
| Agent worker starts | `0` |
| Gateway starts | `0` |
| MCP starts | `0` |
| Tool execution | `0` |

P15.M11 remains the sole owner of live OAuth and first inference.

## Dependency And Lock Boundary

| Boundary | Result |
| --- | --- |
| Externally prepared `node_modules` available | `true` |
| TypeScript command available | `true` |
| Vitest command available | `true` |
| ESLint command available | `true` |
| Vite command available | `true` |
| `npm install` commands | `0` |
| `npm ci` commands | `0` |
| `npm update` commands | `0` |
| `npm audit fix` commands | `0` |
| Package downloads by P15.M10A | `0` |
| Python dependency installations | `0` |
| `package.json` changes | `0` |
| `package-lock.json` changes | `0` |
| `web/package.json` changes | `0` |
| `pyproject.toml` changes | `0` |
| `uv.lock` changes | `0` |
| Dockerfile changes | `0` |
| Compose file changes inside repository | `0` |

The human-controlled dependency preparation is external evidence only.

## Candidate Set

Required modified files:

```text
2_products/pepper-agent/web/src/App.tsx
2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

Required created file:

```text
0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md
```

Candidate-set validation:

| Check | Result |
| --- | --- |
| Candidate files | `3` |
| Unexpected candidates | `0` |
| Missing candidates | `0` |
| Modified product files | `1` |
| Modified register files | `1` |
| Created governance files | `1` |
| Test files modified | `0` |
| Shell files modified | `0` |
| Extension files modified | `0` |
| `main.tsx` modified | `false` |
| Package manifests modified | `0` |
| Lockfiles modified | `0` |
| Dockerfiles modified | `0` |
| Compose files modified | `0` |
| Baseline JSON modified | `false` |
| Graphify modified | `false` |

Diff validation:

| File | Result |
| --- | --- |
| `App.tsx` added lines | `3` |
| `App.tsx` deleted lines | `3` |
| `App.tsx` semantic runtime changes | `0` |
| Register rows changed | `1` |
| Register fields changed in `P15.M6-021` | `1` |
| `git diff --check` whitespace errors | `0` |

Hygiene validation:

| Check | Result |
| --- | --- |
| Markdown trailing whitespace | `0` |
| TypeScript trailing whitespace | `0` |
| TSV schema valid | `true` |
| Unexpected binary files | `0` |
| New executable files | `0` |
| `__pycache__` inside repository | `0` |
| `.pytest_cache` inside repository | `0` |
| `node_modules` candidate paths | `0` |
| `dist` candidate paths | `0` |
| `coverage` candidate paths | `0` |

Ignored frontend build output was not force-added.

## Rollback

If P15.M10A is rejected before commit, rollback is limited to restoring only:

```text
2_products/pepper-agent/web/src/App.tsx
2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

and removing only:

```text
0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md
```

Rollback must not modify the retained WSL checkout, Docker state, BuildKit cache,
runtime evidence, P15.M9, package manifests, lockfiles or any P15.M10 record.

## Sequencing

P15.M10A is ready for human review, staging, commit and push.

After P15.M10A is committed and pushed, P15.M10AR must close post-commit
register, candidate, payload and baseline JSON integrity. P15.M10 remains blocked
until P15.M10AR is committed and pushed. P15.M11 remains the owner of live OAuth
and first inference.

Final verdict:

```text
hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints
```
