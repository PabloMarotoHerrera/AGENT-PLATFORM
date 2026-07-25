# P15.M10AR - Dashboard Readonly Manifest Repair Post-Commit Integrity Closure

Status: P15.M10AR dashboard readonly manifest repair post-commit integrity closed with constraints.

Final verdict: `hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closed_with_constraints`

## Ticket Authority

P15.M10AR closes the aggregate post-commit integrity transition created by
P15.M10A. P15.M10A repaired a frontend compile-time compatibility defect where a
`readonly PluginManifest[]` produced by the protected plugin filter was passed to
local App helpers typed as mutable `PluginManifest[]`.

P15.M10AR verified the committed repair, reran frontend validation, reconciled
the current candidate and payload identities, updated the self-excluded baseline
record, and created this closure record.

P15.M10AR did not modify implementation source, tests, modification register,
import manifest, dependency manifests, lockfiles, Docker configuration, WSL state,
runtime evidence, provider code, credential code, Graphify output, staging state,
commits or remotes.

## Repository And Branch State

| Check | Result |
| --- | --- |
| Repository root | `<WINDOWS_REPOSITORY_ROOT>` |
| Branch | `p15.m-hermes-0.19-migration` |
| Starting HEAD | `85c77f82b52088826c7c7c7fffb7236343e2ca91` |
| Branch remote HEAD | `85c77f82b52088826c7c7c7fffb7236343e2ca91` |
| HEAD equals branch remote | `true` |
| Index empty at start | `true` |
| Staged files at start | `0` |
| Tracked worktree clean at start | `true` |
| Visible untracked task candidates at start | `0` |
| P15.M10 governance record present | `false` |
| P15.M10 product changes | `0` |

Resolved P15.M10A commit:

| Field | Value |
| --- | --- |
| Commit | `85c77f82b52088826c7c7c7fffb7236343e2ca91` |
| Commit message | `P15.M10A Repair readonly plugin manifest build compatibility` |
| Commit is ancestor of HEAD | `true` |
| HEAD equals P15.M10A commit | `true` |
| Post-P15.M10A commits | `0` |
| Post-P15.M10A product mutation commits | `0` |

Exact P15.M10A commit set:

```text
0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md
2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
2_products/pepper-agent/web/src/App.tsx
```

| Commit-set check | Result |
| --- | --- |
| Committed files | `3` |
| Product implementation files | `1` |
| Product control files | `1` |
| Governance files | `1` |
| Unexpected committed files | `0` |
| Missing expected files | `0` |
| Forbidden mutations | `0` |

## Committed Prerequisites

| Record | Required verdict | State |
| --- | --- | --- |
| `0_architecture/governance/agent_platform_hermes_0_19_migration_authorization.md` | `hermes_0_19_migration_authorized_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_workspace_adoption_assessment.md` | `hermes_0_19_workspace_adoption_assessment_ready_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_pepper_product_identity_post_commit_integrity_closure.md` | `hermes_0_19_pepper_product_identity_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_governed_runtime_adapter_post_commit_integrity_closure.md` | `hermes_0_19_governed_runtime_adapter_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closure.md` | `hermes_0_19_openai_codex_provider_credential_post_commit_integrity_closed_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_wsl2_development_architecture.md` | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |
| `0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md` | `hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints` | tracked, committed in `HEAD`, locally unmodified, unstaged |

Product state:

| Field | Value |
| --- | --- |
| Product ID | `pepper` |
| Product version | `0.1.0-dev` |
| Upstream version | `0.19.0` |
| Upstream commit | `3ef6bbd201263d354fd83ec55b3c306ded2eb72a` |
| Product UI | `disabled` |
| Extension modules | `0` |

Provider posture:

| Field | Value |
| --- | --- |
| Provider | `openai-codex` |
| Authentication | `chatgpt_oauth` |
| Model | `gpt-5.5` |
| Real credentials configured | `false` |
| Live OAuth attempts | `0` |
| Provider calls | `0` |
| Inference calls | `0` |

## P15.M10 Blocker Context

P15.M10 stopped before acceptance with:

```text
P15.M10-IMAGE-BUILD-BLOCKED
```

The stopped source Dockerfile frontend build failed after `1114` seconds at:

```text
RUN cd web && npm run build && cd ../ui-tui && npm run build
```

Original diagnostics:

```text
web/src/App.tsx(495,43): readonly PluginManifest[] is not assignable to PluginManifest[]
web/src/App.tsx(507,38): readonly PluginManifest[] is not assignable to PluginManifest[]
```

P15.M10A repaired the source. It did not complete P15.M10, did not produce a
Docker image, did not start Compose and did not create runtime acceptance.

## App Repair Verification

App path:

```text
2_products/pepper-agent/web/src/App.tsx
```

Exact committed App blob identity:

| Field | Value |
| --- | --- |
| Parent App bytes | `44682` |
| Parent App SHA-256 | `8ca66b772754824ac4ecada6f11c20ea8af518657bb3d272daef7d86d4987972` |
| Committed App bytes | `44709` |
| Committed App SHA-256 | `fcb51f78c1912f836cdc2bbf9db4483210db9f2ce30af7a882cfc8ba5f6b1fb2` |
| UTF-8 BOM | `false` |
| Line endings | LF |
| Committed byte delta | `27` |

Exact App diff:

```diff
-  manifests: PluginManifest[],
+  manifests: readonly PluginManifest[],
```

The same one-line annotation change appears in exactly these helpers:

```text
buildNavItems
partitionSidebarNav
buildRoutes
```

App repair checks:

| Check | Result |
| --- | --- |
| Mutable annotations removed | `3` |
| Readonly annotations added | `3` |
| Runtime statements changed | `0` |
| Imports changed | `0` |
| Exports changed | `0` |
| Hooks changed | `0` |
| Routes changed | `0` |
| Navigation items changed | `0` |
| Plugin filters changed | `0` |
| Plugin activation changed | `0` |
| Rendering changed | `0` |
| Whitespace-only changes outside target annotations | `0` |
| Reconstructed parent equals actual parent blob | `true` |

Immutability preservation:

| Check | Result |
| --- | --- |
| Readonly producer contract preserved | `true` |
| `Object.freeze` filter result preserved | `true` |
| Casts added | `0` |
| Array copies added to bypass readonly | `0` |
| Compiler suppressions added | `0` |
| `@ts-ignore` added | `0` |
| `@ts-expect-error` added | `0` |
| `any` cast added | `0` |
| Unknown cast chain added | `0` |
| Immutability weakened | `false` |

The repair expands local consumer type compatibility while preserving the
immutable filtered-manifest authority.

## P15.M10A Governance Record Validation

Record path:

```text
0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repair.md
```

Governance validation:

| Evidence | Result |
| --- | --- |
| Verdict | `hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints` |
| Originating blocker | `P15.M10-IMAGE-BUILD-BLOCKED` |
| Failure kind | `compile_time_readonly_parameter_variance` |
| Original diagnostics | `2` |
| Changed parameter annotations | `3` |
| Runtime behavior changes | `0` |
| App preimage SHA-256 | `8ca66b772754824ac4ecada6f11c20ea8af518657bb3d272daef7d86d4987972` |
| App candidate bytes | `44709` |
| App candidate SHA-256 | `fcb51f78c1912f836cdc2bbf9db4483210db9f2ce30af7a882cfc8ba5f6b1fb2` |
| Register row | `P15.M6-021` |
| New register rows | `0` |
| Frontend typecheck | passed |
| Frontend tests | `134` passed |
| Frontend lint | `0` errors |
| Frontend production build | passed |
| Docker builds by P15.M10A | `0` |
| OAuth attempts | `0` |
| Provider calls | `0` |
| Inference calls | `0` |

Authority distinctions preserved:

```text
frontend production build passed != Docker pilot passed
P15.M10A repaired the source != P15.M10 completed
P15.M10AR closes aggregate integrity != P15.M10 runtime acceptance
```

## Frontend Validation

Frontend validation used the existing dependency environment. No dependency
installation, clean installation, update or audit-fix command was run.

Dependency environment:

| Check | Result |
| --- | --- |
| Workspace `node_modules` available | `true` |
| TypeScript command available | `true` |
| Vitest command available | `true` |
| ESLint command available | `true` |
| Vite command available | `true` |
| Product `package.json` changed | `false` |
| Product `package-lock.json` changed | `false` |
| Web `package.json` changed | `false` |

Validation results:

| Command | Result |
| --- | --- |
| `npm run typecheck` | passed, exit code `0`, TypeScript errors `0`, readonly manifest errors `0` |
| `npm run test` | passed |
| `npm run lint` | exit code `0`, lint errors `0`, lint warnings `24` |
| `npm run build` | passed, exit code `0` |

Test result:

| Field | Value |
| --- | --- |
| Test files | `21` |
| Tests passed | `134` |
| Tests skipped | `0` |
| Failed test files | `0` |
| Failed tests | `0` |
| Unhandled errors | `0` |
| Unexpected skips | `0` |
| Duration | `905ms` |

Lint warning classification:

| Classification | Count |
| --- | ---: |
| Existing React hooks and React refresh warnings | `24` |
| New warning introduced by P15.M10A | `false` |
| Security warning | `0` |
| Credential warning | `0` |
| Provider warning | `0` |
| Unhandled resource warning | `0` |
| Warnings affecting acceptance | `0` |

Production build result:

| Field | Value |
| --- | --- |
| TypeScript build | passed |
| Vite build | passed |
| Modules transformed | `505` |
| Output assets | `10` |
| Build duration | `496ms` |
| Expected Vite warning | one chunk-size warning |
| Security warning | `0` |
| Credential warning | `0` |
| Provider warning | `0` |
| Unhandled resource warning | `0` |
| Warnings affecting acceptance | `0` |

## Runtime Semantic Equivalence

Validated by exact source diff, tests and production build evidence:

| Behavior | Result |
| --- | --- |
| `buildNavItems` runtime body changed | `false` |
| `partitionSidebarNav` runtime body changed | `false` |
| `buildRoutes` runtime body changed | `false` |
| Route behavior changed | `false` |
| Navigation behavior changed | `false` |
| Plugin filtering behavior changed | `false` |
| Plugin order behavior changed | `false` |
| Plugin override behavior changed | `false` |
| Hidden plugin route behavior changed | `false` |
| Built-in route behavior changed | `false` |
| Product extension behavior changed | `false` |
| Sidebar grouping behavior changed | `false` |
| Chat override behavior changed | `false` |
| Protected namespace behavior changed | `false` |

The committed JavaScript behavior is semantically equivalent. Only TypeScript
parameter acceptance changed.

## Modification Register Integrity

Register path:

```text
2_products/pepper-agent/AGENT_PLATFORM_MODIFICATIONS.tsv
```

Whole-register validation against exact committed `HEAD` blobs:

| Check | Result |
| --- | --- |
| Columns | `18` |
| Rows | `87` |
| Duplicate modification IDs | `0` |
| Duplicate product paths | `0` |
| Blank mandatory fields | `0` |
| Invalid classifications | `0` |
| Missing committed blobs | `0` |
| Committed blob hash mismatches | `0` |
| Register rows without product file | `0` |
| Unregistered modified product paths | `0` |

`P15.M6-021` reconciliation:

| Field | Value |
| --- | --- |
| Row occurrences | `1` |
| Path occurrences | `1` |
| Path | `web/src/App.tsx` |
| Owner ticket | `P15.M6` |
| Old hash | `8ca66b772754824ac4ecada6f11c20ea8af518657bb3d272daef7d86d4987972` |
| Current hash | `fcb51f78c1912f836cdc2bbf9db4483210db9f2ce30af7a882cfc8ba5f6b1fb2` |
| Current hash equals HEAD App blob | `true` |
| New `P15.M10A` register row | `false` |
| Rows changed from parent to P15.M10A | `1` |
| Changed row | `P15.M6-021` |
| Fields changed | `1` |
| Changed field | `current_product_sha256_or_none` |
| Other fields changed | `0` |
| New rows | `0` |
| Deleted rows | `0` |

## Import-Manifest Drift Reconciliation

Import manifest path:

```text
2_products/pepper-agent/AGENT_PLATFORM_IMPORT_MANIFEST.tsv
```

Import-manifest validation:

| Check | Result |
| --- | --- |
| Included import rows | `6681` |
| Missing import destinations | `0` |
| Duplicate import destinations | `0` |
| Unsupported import classifications | `0` |
| P15.M10A modified imported destinations | `1` |
| P15.M10A modified imported path | `web/src/App.tsx` |
| P15.M10A register authorization | `P15.M6-021` |
| P15.M10A App HEAD hash | `fcb51f78c1912f836cdc2bbf9db4483210db9f2ce30af7a882cfc8ba5f6b1fb2` |
| Total destination hash mismatches | `3` |
| New unregistered import destination mismatches | `0` |
| Unexplained destination hash mismatches | `0` |
| Destination mismatches without modification row | `0` |

The three current destination mismatches are all registered downstream
divergences: `hermes_cli/web_server.py` by `P15.M6-002`, `web/src/main.tsx` by
`P15.M6-020`, and `web/src/App.tsx` by `P15.M6-021`.

Authority model:

```text
import manifest: upstream provenance authority
modification register: downstream divergence authority
canonical integrity utility: current committed candidate and payload authority
```

## Canonical Identity

Pre-P15.M10A identity preserved as historical evidence:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6768` | `149234329` | `f0dceedbe9ae1b6b0738c00b0d643678d8bc5acd2b9766729f7adcb238c08e59` |
| Payload | `6681` | `145409765` | `56a538886ac9cc98050be853f173e631e8f568495a6c5aeef27a2128981524e7` |
| Baseline record | n/a | `34254` | `478f1cd5279806e808b562193a993f391f98a4e8513ef4ee8d41e35a0d7c4dda` |

Post-P15.M10A committed identity computed twice before baseline update and twice
after baseline update:

| Mode | Files | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Candidate | `6768` | `149234356` | `a71af0be624cb3f00b37d651248717c38f5bed18e460c6f159636c75a8875df3` |
| Payload | `6681` | `145409792` | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |

Integrity deltas:

| Check | Result |
| --- | --- |
| Candidate file delta | `0` |
| Candidate byte delta | `27` |
| Payload file delta | `0` |
| Payload byte delta | `27` |
| Candidate SHA changed | `true` |
| Payload SHA changed | `true` |
| Repeat candidate digest match | `true` |
| Repeat payload digest match | `true` |

## Baseline JSON Update

Updated path:

```text
2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
```

Baseline JSON update result:

| Check | Result |
| --- | --- |
| Baseline JSON valid | `true` |
| Candidate baseline-record bytes | `38693` |
| Candidate baseline-record SHA-256 | `fd74d3a61e5c17f679a7e781e02b9c0dd6c56908bb1c03795c489f601c99c030` |
| Self-reference | `false` |
| Current candidate identity updated | `true` |
| Current payload identity updated | `true` |
| Pre-P15.M10A candidate identity preserved | `true` |
| Pre-P15.M10A payload identity preserved | `true` |
| P15.M10A repair state recorded | `true` |
| P15.M10 retry authority recorded | `true` |
| Baseline JSON excluded from candidate | `true` |
| Baseline JSON excluded from payload | `true` |
| Candidate identity after baseline update unchanged | `true` |
| Payload identity after baseline update unchanged | `true` |
| Post-update candidate repeatability | `true` |
| Post-update payload repeatability | `true` |

The baseline JSON does not store its own SHA-256. The candidate baseline-record
identity above is recorded only in this closure record for human review.

Governance integrity tests:

| Timing | Result |
| --- | --- |
| Before baseline update | `14` tests, `0` failures, `0` errors |
| After baseline update | `14` tests, `0` failures, `0` errors |

## Static Security And Authority Validation

| Check | Result |
| --- | --- |
| Raw token logging | `0` |
| Raw token serialization | `0` |
| Credential path exports | `0` |
| Provider endpoint changes | `0` |
| Provider model changes | `0` |
| `OPENAI_API_KEY` authority changes | `0` |
| OAuth authority changes | `0` |
| Provider HTTP calls | `0` |
| Inference calls | `0` |
| Model-list calls | `0` |
| Usage calls | `0` |
| Worker process starts | `0` |
| Agent process starts | `0` |
| Tool execution | `0` |
| MCP execution | `0` |
| Frontend dynamic code loading changes | `0` |
| Plugin activation changes | `0` |
| Real auth stores inspected | `0` |
| Real credentials read | `0` |
| Real credentials written | `0` |
| Live OAuth attempts | `0` |
| Real credential leases | `0` |

## Docker, WSL And Dependency Boundary

| Activity | Count |
| --- | ---: |
| Docker Desktop starts | `0` |
| Docker daemon starts | `0` |
| Docker daemon stops | `0` |
| Docker builds | `0` |
| Image pulls | `0` |
| Image creations | `0` |
| Container starts | `0` |
| Compose starts | `0` |
| Compose network creations | `0` |
| WSL distribution starts by P15.M10AR | `0` |
| Linux checkout fetches | `0` |
| Linux checkout mutations | `0` |
| Runtime root mutations | `0` |
| P15.M10 evidence mutations | `0` |
| `npm install` commands | `0` |
| `npm ci` commands | `0` |
| `npm update` commands | `0` |
| Package downloads | `0` |
| Python dependency installations | `0` |
| Package manifest changes | `0` |
| Lockfile changes | `0` |
| Dockerfile changes | `0` |
| Repository Compose changes | `0` |

## Candidate Set And Repository Integrity

Authorized modification:

```text
2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
```

Authorized creation:

```text
0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closure.md
```

Candidate-set result:

| Check | Result |
| --- | --- |
| Candidate files | `2` |
| Unexpected candidates | `0` |
| Modified product files | `0` |
| Modified baseline files | `1` |
| Created governance files | `1` |
| App modified during P15.M10AR | `false` |
| Modification register modified during P15.M10AR | `false` |
| Import manifest modified | `false` |
| Tests modified | `0` |
| Frontend source modified | `0` |
| Package manifests modified | `0` |
| Lockfiles modified | `0` |
| Dockerfiles modified | `0` |
| Compose files modified | `0` |
| Runtime adapter modified | `false` |
| Provider packages modified | `false` |
| Graphify modified | `false` |

Repository integrity:

| Check | Result |
| --- | --- |
| P15.M10A App changes during P15.M10AR | `0` |
| P15.M10A register changes during P15.M10AR | `0` |
| P15.M10A governance changes during P15.M10AR | `0` |
| P15.M8 implementation changes | `0` |
| P15.M8R changes | `0` |
| P15.M9 changes | `0` |
| Runtime adapter changes | `0` |
| Provider credential changes | `0` |
| Provider runtime changes | `0` |
| Provider worker changes | `0` |
| Product configuration changes | `0` |
| Web server changes | `0` |
| Other frontend changes | `0` |
| Auth source changes | `0` |
| Credential pool changes | `0` |
| Codex transport changes | `0` |
| Workspace changes | `0` |
| Desktop changes | `0` |
| Dependency manifest changes | `0` |
| Lockfile changes | `0` |
| Source Dockerfile changes | `0` |
| Repository Compose changes | `0` |
| Graphify commands | `0` |
| Graphify changes | `0` |

## P15.M10 Retry Handoff

P15.M10 may be retried only after P15.M10AR has been accepted by the human
reviewer, staged by the human, committed and pushed.

Future P15.M10 retry prerequisites:

| Field | Value |
| --- | --- |
| P15.M9 verdict | `hermes_0_19_wsl2_development_architecture_ready_with_constraints` |
| P15.M10A verdict | `hermes_0_19_dashboard_readonly_plugin_manifest_build_compatibility_repaired_with_constraints` |
| P15.M10AR verdict | `hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closed_with_constraints` |
| Candidate files | `6768` |
| Candidate bytes | `149234356` |
| Candidate SHA-256 | `a71af0be624cb3f00b37d651248717c38f5bed18e460c6f159636c75a8875df3` |
| Payload files | `6681` |
| Payload bytes | `145409792` |
| Payload SHA-256 | `1472224d58182eac232e700b3e586fe5d70fd167eb484659c623921b9b66b34c` |
| Frontend typecheck | passed |
| Frontend tests | `134` passed |
| Frontend lint | `0` errors |
| Frontend production build | passed |

The retained Linux-native checkout must be updated through Git fast-forward only:

```text
git fetch origin
verify current branch
fast-forward only to the expected P15.M10AR HEAD
verify exact HEAD
verify HEAD equals origin branch
verify clean worktree
run canonical integrity utility
```

Manual App, register or baseline copies from the Windows checkout are not
authorized. The future P15.M10 retry may reuse valid Docker build cache but must
not assume the previous failed build created a valid image.

Previous P15.M10 retry state:

| Field | Value |
| --- | --- |
| Previous P15.M10 tagged image | absent |
| Previous P15.M10 governance record | absent |
| Previous P15.M10 runtime acceptance | `false` |

P15.M10 must rerun the original pilot gates from the beginning using the new
committed identities.

## P15.M11 Boundary

P15.M11 remains the sole owner of first live OAuth, real credential acquisition,
real token validation, GPT-5.5 entitlement validation, provider reachability,
first tool-free inference, live cancellation, credential cleanup and provider
rollback evidence.

P15.M10AR state:

| Field | Value |
| --- | --- |
| Real credentials configured | `false` |
| Live OAuth attempts | `0` |
| Provider calls | `0` |
| Inference calls | `0` |
| Model-list calls | `0` |
| Usage calls | `0` |
| Provider worker starts | `0` |
| Agent worker starts | `0` |
| P15.M11 authority preserved | `true` |

P15.M10AR does not unblock P15.M11 directly. P15.M11 remains blocked until the
retried P15.M10 Docker Compose local pilot is accepted, committed and pushed.

## Rollback

If P15.M10AR is rejected before commit, rollback is limited to restoring only:

```text
2_products/pepper-agent/AGENT_PLATFORM_UPSTREAM_BASELINE.json
```

and removing only:

```text
0_architecture/governance/agent_platform_hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closure.md
```

Rollback must preserve the P15.M10A commit, App repair, register reconciliation,
import manifest, frontend dependencies, Docker state, WSL state and credential
boundary.

Final verdict:

```text
hermes_0_19_dashboard_readonly_plugin_manifest_build_post_commit_integrity_closed_with_constraints
```
